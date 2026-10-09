"""Real pipeline execution — a generic step-executor for every pipeline in
.claude/pipelines/*.yaml, not just `audit`.

Until 2026-09-14 this module only knew how to run one hardcoded pipeline (`audit`, two
fixed subprocess.run calls). That doesn't fit anything write-capable — onboard-suite,
ingest-docs, export-automation all have loops, gates, human checkpoints, and (for
onboard-suite/new-suite-from-docs) a real TestRail push. This rewrite walks any
pipeline's real `steps[]` (Platform/model/pipelines.py's typed view of the YAML) and
dispatches by `kind`, instead of hand-rolling one pipeline's shape.

Safety rules that hold regardless of what a pipeline YAML declares:
  - A step whose rendered command contains both "push" and "--commit" is ALWAYS treated
    as a human approval gate, never auto-run — this is the one thing this module refuses
    to let a YAML edit override. That's the runner-level backstop behind the UI's
    "Approve & Push" button; the button can only ever *resolve* a paused step, never skip
    this check on the way in.
  - `human` steps stop the run (status becomes `waiting_human`) until something calls
    `resolve_step` — no auto-advance.
  - A composite pipeline's `{id, ref: <other-pipeline-id>}` steps are inlined (that other
    pipeline's own steps run in place, ids qualified as `<step_id>.<nested_id>`) rather
    than treated as an opaque black box, so the UI's step list shows real granular
    progress through e.g. new-suite-from-docs' full ingest-docs + onboard-suite chain.
  - A step's `when:` field (e.g. onboard-suite's fresh-build skip, added separately in
    that repo) is evaluated against a small run context (currently just `fresh_build`,
    derived from suite_mappings' old_suite_id being NULL) — a falsy `when` marks the step
    `skipped`, not run.

Runs (and resumptions past a human/gate step) go in a background thread; store.py tracks
both the overall run (`pipeline_runs`) and each step's own status (`pipeline_run_steps`).
"""
from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from Platform.webapp import store

_PLATFORM_ROOT = Path(__file__).resolve().parent.parent
SYSTEM_TEST_OPS_ROOT = _PLATFORM_ROOT.parent.parent / "system-test-ops"
# write-automation's write_tests step runs against this SEPARATE sibling repo/remote
# (its own git history, its own origin/main) -- never system-test-ops'.
TEST_AUTOMATION_SIT_ROOT = _PLATFORM_ROOT.parent.parent / "test-automation-sit"

# A step's `repo:` field (e.g. write-automation.yaml's write_tests: repo: test-automation-sit)
# picks which sibling checkout a cli/agent step actually runs in. Absent -> system-test-ops,
# the default every other pipeline already assumes.
_REPO_ROOTS = {
    "system-test-ops": SYSTEM_TEST_OPS_ROOT,
    "test-automation-sit": TEST_AUTOMATION_SIT_ROOT,
}


def _step_cwd(step: Step) -> Path:
    return _REPO_ROOTS.get(getattr(step, "repo", None), SYSTEM_TEST_OPS_ROOT)
_VENV_PYTHON = SYSTEM_TEST_OPS_ROOT / ".venv" / "Scripts" / "python.exe"

if str(_PLATFORM_ROOT) not in sys.path:
    sys.path.insert(0, str(_PLATFORM_ROOT))
from model.pipelines import Pipeline, Step, StepKind, load_pipeline  # noqa: E402

# Minimal, least-privilege --allowedTools grant per named agent (see
# system-test-ops/.claude/agents/*.md frontmatter). Anything not listed here — including
# the unnamed "summarise" step audit.yaml uses — gets Read only.
AGENT_TOOL_GRANTS = {
    "gherkin-author": "Read,Write,Edit",
    "test-lead": "Read,Write",
    "standards-keeper": "Read",
    "coverage-analyst": "Read",
    "run-historian": "Read",
    # test-automation-sit's own agent (frontmatter: Read, Edit, Write, Glob, Grep) — no
    # Bash, so it can't itself run `git commit`/`git push`; that stays a separate human
    # step (write-automation.yaml's commit_push) this engine never auto-executes.
    "test-author": "Read,Write,Edit,Glob,Grep",
}
_DEFAULT_AGENT_TOOLS = "Read"

# Raised from 180s (2026-09-23): the real Translink ingest_docs convert measured 163s --
# inside the old limit, but only by 10%, so a slightly slower day would have timed out a
# perfectly healthy run. Most cli steps are fast TestRail calls; a generous ceiling costs
# nothing except how long a genuinely hung step takes to be noticed.
_CLI_TIMEOUT = 600
# 180s was fine for a one-file summarise (audit.yaml's "summarise" step) but nowhere near
# enough for a step that reads and carefully cites multiple real source documents (found
# live: ingest-docs' distil timed out reading 10 real PDFs). Generous ceiling for real work;
# a genuinely hung agent still gets caught, just later.
_AGENT_TIMEOUT = 900

_cancel_events: dict[str, threading.Event] = {}
_run_procs: dict[str, subprocess.Popen] = {}
_procs_lock = threading.Lock()
# George, 2026-09-30: "there should be a way to approve all... plus auto mode seems to not
# actual work?" -- first built as a browser-side (JS Set) toggle, which only "worked" while
# that exact browser tab stayed on that exact page; navigating away, reloading, or even just
# the run outliving the tab silently reset it with no visible sign it had turned off. The
# run itself lives entirely server-side (this dict, same as _cancel_events/_run_procs) --
# auto-approve needs to too, so it survives page navigation/reload and doesn't depend on any
# one browser tab being open. In-memory only, same as its siblings -- doesn't survive a
# server restart, which is an accepted, pre-existing limit of this whole tracking approach.
_auto_approve_runs: set[str] = set()

# Extra, pipeline-declared run inputs beyond project/device/suite ids (e.g. ingest-docs'
# {docs_path}) -- keyed by run_id so a resumed (post-human-step) continuation can still see
# them. In-memory only, same non-survives-a-restart tradeoff as _cancel_events/_run_procs.
_run_extra_inputs: dict[str, dict[str, str]] = {}


def is_runnable(pipeline_id: str) -> bool:
    """Every pipeline is runnable now (2026-09-14) — the old RUNNABLE_PIPELINES allowlist
    is gone. What used to gate execution at the pipeline level now gates at the STEP
    level instead: any step that would push --commit is always a human-approval gate
    (see module docstring), so a write-capable pipeline can run but can't silently write
    without a person clicking "Approve & Push" first."""
    return True


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class _SafeFormatDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


def _split_command(command: str) -> list[str]:
    """shlex.split(command) alone mangles Windows paths -- its default POSIX mode treats
    backslash as an escape character, so `C:\\Users\\...` comes out as `C:UsersDocuments...`
    with every backslash silently eaten (found live: ingest-docs' --src {docs_path} arrived
    at the CLI as a garbled, nonexistent path, so it silently converted 0 files while still
    reporting "succeeded"). posix=False stops that, but then leaves surrounding quote marks
    on a quoted token (e.g. a path containing spaces) instead of stripping them -- so strip
    those manually here rather than trusting either mode alone."""
    tokens = shlex.split(command, posix=False)
    return [t[1:-1] if len(t) >= 2 and t[0] == t[-1] and t[0] in ("\"", "'") else t for t in tokens]


def _render(template: str, params: dict) -> str:
    """`str.format_map` that leaves an unresolved `{placeholder}` alone instead of raising
    — a pipeline whose extra inputs (e.g. ingest-docs' {docs_path}) haven't been supplied
    yet still gets a step row and a (harmlessly unrunnable) rendered command, rather than
    crashing the whole run before it can even show the step list."""
    return template.format_map(_SafeFormatDict(params))


_OPTIONAL_FLAG_RE = re.compile(r"\[(--[\w-]+)(?:\s+([^\]]+))?\]")
_UNRESOLVED_PLACEHOLDER_RE = re.compile(r"\{[\w.]+\}")


def _command_params(params: dict) -> dict:
    """`params` minus `intent` -- for rendering a CLI step's `command:` template only.

    `intent` (George 2026-09-24's free-text "what are you trying to achieve" field) must be
    PURELY informational: read by an agent step as context to weigh, never a source of real
    argv. No pipeline YAML declares `{intent}` in a `command:` template today, but nothing
    stopped one from doing so tomorrow -- `_render` is a blind `str.format_map`, so a future
    `push --commit [--suite {intent}]`-style typo (or a deliberate one) would let arbitrary
    user prose become real subprocess arguments to a write-capable CLI call. Strip it here,
    at the one place CLI commands are rendered, so that channel is closed structurally
    rather than by convention/code-review vigilance alone."""
    return {k: v for k, v in params.items() if k != "intent"}


def _resolve_optional_flags(command: str, params: dict) -> str:
    """A YAML command uses `[--flag]` as documentation shorthand for "pass this only if the
    matching run input is truthy" (e.g. export-automation's `[--include-manual]`), and
    `[--flag {value}]` for "pass this flag with a real value if one was supplied, else omit
    the flag entirely" (e.g. onboard-suite's `[--project {testrail_project_id}]` — added
    2026-09-14 after a target got audited against the wrong TestRail project because a
    single global .env default can't correctly serve every target). Neither shape should
    ever reach a real subprocess argv literally.

    By the time this runs, `_render()` has already substituted any real `{placeholder}`
    value into the command -- so `[--flag {value}]` has already become `[--flag 27]` if the
    param was supplied, or is still literally `[--flag {value}]` if it wasn't (a missing key
    is left alone by `_render`'s SafeFormatDict, never turned into the string "None")."""
    def repl(match: re.Match) -> str:
        flag, value = match.group(1), match.group(2)
        if value is None:
            key = flag.lstrip("-").replace("-", "_")
            v = params.get(key)
            truthy = v is not None and str(v).strip().lower() in ("1", "true", "yes")
            return flag if truthy else ""
        if _UNRESOLVED_PLACEHOLDER_RE.search(value):
            return ""  # the param behind {value} was never supplied -- drop the whole flag
        return f"{flag} {value}"
    resolved = _OPTIONAL_FLAG_RE.sub(repl, command)
    return re.sub(r"\s{2,}", " ", resolved).strip()


_AREA_PREFIX_RE = re.compile(r"^(fs\d+|hmi\d+|is\d+|ss\d+)-", re.IGNORECASE)


def _slugify_area(spec_stem: str) -> str:
    """A spec filename like `fs002-cloudfare-communication` -> `cloudfare-communication` —
    strips the doc-numbering prefix these filenames use (fs002-/hmi01-/is001-/ss003-,
    per the real system-test-ops naming convention), keeping the human-meaningful part."""
    return _AREA_PREFIX_RE.sub("", spec_stem)


_DOCUMENT_ROLE_RE = re.compile(r"\*\*Document role:\*\*\s*(functional|reference)", re.IGNORECASE)


def _note_document_role(note_path: Path) -> str | None:
    """Real content-based classification `spec-distiller` writes into a note's own header --
    'functional' (defines testable device behaviour -> a real authored area) or 'reference'
    (environment/config/topology/endpoint/protocol/data-setup knowledge -> grounding only,
    never its own area). See spec-distiller.md for why this can't be a filename guess.

    None (not "unknown"/"functional" by default) for a note distilled before this convention
    existed, or if the file can't be read -- callers decide their own safe fallback rather
    than this silently assuming either role."""
    try:
        head = note_path.read_text(encoding="utf-8", errors="replace")[:2000]
    except OSError:
        return None
    m = _DOCUMENT_ROLE_RE.search(head)
    return m.group(1).lower() if m else None


def _functional_areas(project: str, device: str) -> list[str]:
    """One functional area per DEVICE-RELEVANT ingested spec file -- generic, not
    NJT-hardcoded: any project with knowledge/{project}/specs/*.md (via ingest-docs) gets
    this fan-out. Empty if that folder doesn't exist yet (ingest-docs hasn't run) --
    callers must fail loudly on empty, never silently produce zero sub-steps.

    Found live, 2026-09-24 (George: "if im not on POS and uploaded docs for it, it should
    onboard those docs for POS, not everything for translink"): this used to list EVERY
    spec file in the project's shared knowledge/{project}/specs/ folder regardless of
    device -- onboarding POS would fan out author_area/push_area steps for TVM-only,
    Gate-only, Bus-Validator-only specs too. Reuses the sibling `tools/archive_knowledge.py
    --dry-run`'s device classification (same engine, same knowledge/projects/
    <project>-doc-classifier.yaml config already built and grounded for this) to filter to
    just this device's matches -- its 'archived' list (its own name for 'things that would
    be archived FROM this device's view', i.e. exactly the specs classified as relevant to
    it) is the device-relevant subset we want here, not a second scoping mechanism.

    Falls back to the OLD project-wide behaviour if the classifier tool/config isn't
    available for this project yet (e.g. a project with no
    knowledge/projects/<project>-doc-classifier.yaml) -- never silently produces zero
    areas just because classification isn't set up, since that would look identical to
    "no specs ingested yet" to every caller."""
    specs_dir = SYSTEM_TEST_OPS_ROOT / "knowledge" / project.lower() / "specs"
    if not specs_dir.is_dir():
        return []
    all_specs = sorted(specs_dir.glob("*.md"))
    try:
        # Via _run_subprocess (this module's one mockable subprocess wrapper), not a raw
        # subprocess.run call -- every test that fans out a loop step mocks this exact
        # function; a second, un-mocked subprocess path here broke them (real Popen
        # internals vs. these tests' synchronous-Thread test double for _run_pipeline_job).
        returncode, stdout, stderr = _run_subprocess(
            [str(_VENV_PYTHON), "tools/archive_knowledge.py", "--project", project, "--device", device, "--dry-run"],
            cwd=str(SYSTEM_TEST_OPS_ROOT), timeout=60,
        )
        if returncode != 0:
            raise RuntimeError(stderr.strip() or stdout.strip())
        payload = json.loads(stdout)
        # George, 2026-09-30, found live (real onboard-suite run for Translink/POS): "still
        # see the ETM device endpoints and stuff... when i push them there gonna push test
        # cases for it to the POS SUITE?" -- confirmed real. archive_knowledge.py's "medium"
        # confidence tier (a bare device-code MENTION anywhere in the body) is too loose for
        # this decision: every Device-Endpoints-STE12-*.md file opens with the same
        # boilerplate "...companion to the POS Functional Specification" cross-reference
        # line, and Device-Endpoints-ETM-HHD.md/PV-GV.md only mention POS in a "differences
        # from POS" comparison heading -- neither means the file IS about POS. Every genuine
        # POS note matches at "high" confidence (a clean title hit); only "high" is trusted
        # here. Checked directly against the real Translink knowledge (2026-09-30): "high"
        # keeps exactly the 22 real POS-*.md notes + the one note that genuinely covers POS
        # (Device-Endpoints-STE12-pv-and-pos-local-services.md, itself a clean title hit),
        # and correctly drops all 13 "medium" Device-Endpoints false positives.
        matched = {m["file"] for m in payload["archived"] if m["confidence"] == "high"}
        # George, 2026-09-30, the actual root-cause fix (not just the confidence tightening
        # above): "some documents are probably worth having ingested but are like for
        # knowledge... the test suite we write manual cases for will mainly always be the
        # functional and non functional tests for the device targeted... we use our
        # knowledge from the other specifications to understand how the functional test
        # behaves... that basically like add to the functional spec". Even at "high"
        # confidence, Device-Endpoints-STE12-pv-and-pos-local-services.md genuinely covers
        # BOTH PV and POS -- it's not a device-specific functional-behaviour document at
        # all, it's a shared cross-device endpoint/protocol REFERENCE. Authoring it as its
        # own area mixed PV-only sections into a file meant to be pushed as POS's, exactly
        # the suite-clutter this whole filter exists to prevent -- one layer deeper than a
        # file-level device mismatch. Reference material should ground a real functional
        # case (gherkin-author can still read it), never generate its own pushed section.
        #
        # George, 2026-09-30 (the real fix, generalised): "specs might always be different
        # for different projects... we need to ensure we are smart enough to distinct
        # between test case writing [and] anything extra [that] is knowledge." A filename
        # check (the "Device-Endpoints" prefix this used to test) is exactly the kind of
        # project-specific guess that won't generalise -- a different project's reference
        # docs won't share Translink's naming convention. `spec-distiller` now classifies
        # each note's real **Document role** (functional/reference) from its own content, in
        # the note's own header -- that's the real, project-agnostic signal to trust. The
        # filename check survives ONLY as a fallback for notes distilled before this
        # convention existed (no header field to read yet), so older knowledge isn't broken.
        def _role(f: str) -> str:
            role = _note_document_role(specs_dir / f)
            if role is not None:
                return role
            # Legacy fallback ONLY -- every note distilled before spec-distiller existed
            # has no real Document-role header to read. Without this, today's real
            # Translink knowledge (still all legacy) would silently regress to the exact
            # bug this whole fix exists to prevent, the moment a note has no tag to trust.
            return "reference" if Path(f).stem.lower().startswith("device-endpoints") else "functional"
        matched = {f for f in matched if _role(f) != "reference"}
        if matched:
            return [_slugify_area(Path(f).stem) for f in sorted(matched)]
        # Classifier ran fine but found zero matches for this device -- a project-wide
        # fallback here would silently rebuild the "onboard everything" bug this exists to
        # fix, so an empty, genuinely-classified result stays empty (the "no areas" path
        # above already fails loudly rather than running zero sub-steps).
        return []
    except (subprocess.TimeoutExpired, OSError, RuntimeError, json.JSONDecodeError, KeyError):
        # No classifier config for this project yet, or the tool itself errored -- fall
        # back to the full, unfiltered list rather than a hard failure; this is strictly
        # the pre-2026-09-24 behaviour, not a new regression, for a project that hasn't
        # been set up for device-classification at all.
        return [_slugify_area(f.stem) for f in all_specs]


def step_area(step_id: str) -> str | None:
    """Extracts the area slug from a fanned-out step id like `author_area[fare-structure]`
    -> `fare-structure`; None for a step that was never fanned out."""
    if step_id.endswith("]") and "[" in step_id:
        return step_id[step_id.rindex("[") + 1:-1]
    return None


def _flatten_steps(pipeline: Pipeline, project: str, device: str, _seen: frozenset[str] = frozenset()) -> list[Step]:
    """Real, ordered step list with composite `{id, ref: <pipeline-id>}` steps inlined —
    so e.g. new-suite-from-docs shows ingest-docs' and onboard-suite's real steps, not two
    opaque "run this whole other pipeline" boxes. Nested step ids are qualified
    `<ref-step-id>.<nested-step-id>` to stay unique.

    A `loop:`-annotated step (e.g. onboard-suite's `author_area`/`push_area`, "one per
    functional area") is expanded here into one real step per functional area, ids
    qualified `<step-id>[<area>]`, each with its own `loop` cleared so dispatch treats it
    as a normal single step — that's what gives each area its own pipeline_run_steps row,
    its own status pill, and (for push_area) its own independent Approve & Push gate. If
    no areas can be derived yet (no ingested specs for this project), the ORIGINAL
    unexpanded step is kept (with `loop` still set) so _dispatch_step can fail it loudly
    rather than silently running zero sub-steps."""
    if pipeline.id in _seen:
        raise RuntimeError(f"Circular composite pipeline reference at '{pipeline.id}'")
    seen = _seen | {pipeline.id}
    steps = pipeline.steps
    out: list[Step] = []
    i = 0
    while i < len(steps):
        step = steps[i]
        if step.is_composite_ref:
            nested_pipeline = load_pipeline(step.ref)
            for nested in _flatten_steps(nested_pipeline, project, device, seen):
                out.append(nested.model_copy(update={"id": f"{step.id}.{nested.id}"}))
            i += 1
            continue
        if getattr(step, "loop", None):
            areas = _functional_areas(project, device)
            if not areas:
                out.append(step)  # loop stays set -> _dispatch_step fails it with a clear message
                i += 1
                continue
            # A run of consecutive loop steps sharing the same `loop:` text (e.g.
            # onboard-suite's author_area/push_area, both "one per functional area") is
            # interleaved per area -- author[A1] -> push[A1] -> author[A2] -> push[A2] --
            # rather than running one step across every area before the next starts. That
            # matches the real ask (ISSUES.md): review + approve each area's drafted cases
            # before the next area is even drafted, not draft everything then push
            # everything. Guarded on matching `loop` text so unrelated loop steps elsewhere
            # never get grouped by accident.
            group = [step]
            j = i + 1
            while j < len(steps) and getattr(steps[j], "loop", None) == step.loop:
                group.append(steps[j])
                j += 1
            for area in areas:
                for gstep in group:
                    out.append(gstep.model_copy(update={"id": f"{gstep.id}[{area}]", "loop": None}))
            i = j
            continue
        out.append(step)
        i += 1
    return out


def _eval_when(expr: str, context: dict) -> bool:
    """Tiny, whitelisted evaluator for a step's `when:` — no `eval()`. Supports a bare
    context variable, optionally negated ("fresh_build" / "not fresh_build"). Unknown
    variables default to falsy rather than raising, so a `when:` referencing a context key
    this engine doesn't populate yet just skips the step rather than crashing the run."""
    expr = expr.strip()
    negate = expr.lower().startswith("not ")
    var = expr[4:].strip() if negate else expr
    value = bool(context.get(var, False))
    return (not value) if negate else value


def _is_fresh_build(project: str, device: str) -> bool:
    ids = store.get_suite_ids(project, device)
    return bool(ids) and ids.get("old_suite_id") is None


_REQUIREMENTS_ROOT = Path.home() / "TestOpsRequirements"


def _docs_changed(project: str) -> bool:
    """True if anything changed in this project's local requirements folder since the
    last check -- backs scheduled-scan's `when: docs_changed` gate on its ingest step.

    STATEFUL, same as store.check_docs_for_changes itself: every call resets the
    comparison baseline to now, so this must be called at most ONCE per real run, never
    speculatively -- which is why it's gated to the scheduled-scan pipeline specifically
    in _run_pipeline_job below, not computed unconditionally for every pipeline the way
    _is_fresh_build is (that one's a plain read, safe to compute every time; this one
    consumes the diff it reports). Fixed 2026-09-22: was pointing at the project folder's
    top level, which also holds ingest_docs.py's own reconciliation logs -- same bug,
    same fix as app.py's refresh-check endpoint, via the same shared resolution."""
    real = store.resolve_ingest_docs_source(project)
    req_dir = Path(real["path"]) if real["path"] else (_REQUIREMENTS_ROOT / project.lower())
    result = store.check_docs_for_changes(project, req_dir)
    return bool(result["new"] or result["changed"] or result["removed"])


def _build_params(project: str, device: str, steps: list[Step], extra_inputs: dict[str, str] | None = None) -> dict:
    # extra_inputs first, so a pipeline's own declared inputs (e.g. ingest-docs' docs_path)
    # can never clobber the system-derived project/device/suite id params assigned below.
    # An empty string (e.g. an optional input's text box left blank, like onboard-suite's
    # flow_data_path) is treated the same as "not supplied" -- included as-is, `_render`
    # would substitute a blank rather than leaving `{flow_data_path}` unresolved, so the
    # "skip a step with a missing input" check never triggers and the command runs with a
    # blank argument instead (found live: mine_flows ran with an empty first argument and
    # printed its own usage/help text as a confusing "failure").
    params: dict = {k: v for k, v in (extra_inputs or {}).items() if v not in (None, "")}
    params["project"] = project
    params["device"] = device
    all_commands = " ".join(s.command or "" for s in steps)
    ids = store.get_suite_ids(project, device) or {}
    if ids.get("old_suite_id") is not None:
        params["old_suite_id"] = ids["old_suite_id"]
    if ids.get("new_suite_id") is not None:
        params["new_suite_id"] = ids["new_suite_id"]
    if "{suite_id}" in all_commands:
        suite_id = store.get_new_suite_id(project, device)
        if suite_id is None:
            raise ValueError(f"No new_suite_id configured for {project}/{device} — add one in Settings first.")
        params["suite_id"] = suite_id
    # Same value as {suite_id} above, but genuinely OPTIONAL (e.g. ingest-docs' pull_live_cases,
    # which should still let the rest of ingest-docs run for a project with no suite target
    # configured yet -- only that one step cleanly skips, via the unresolved-placeholder check,
    # rather than {suite_id}'s hard-required-or-refuse-to-start-the-whole-run behaviour above).
    if "{live_suite_id}" in all_commands:
        live_suite_id = store.get_new_suite_id(project, device)
        if live_suite_id is not None:
            params["live_suite_id"] = live_suite_id
    # Only set when a real value is confirmed for this target -- omitted (not None) so
    # _render's SafeFormatDict leaves {testrail_project_id} literally unresolved rather than
    # rendering the string "None", which [--project {testrail_project_id}]-style optional
    # flags rely on to know the value was never supplied.
    testrail_project_id = store.get_testrail_project_id(project, device)
    if testrail_project_id is not None:
        params["testrail_project_id"] = testrail_project_id
    # The NEW suite's project can genuinely differ from the OLD suite's (found live: a
    # dry-run target's old suite sat under project 27, its new suite under project 12) --
    # kept as a separate param so push_area/definition_of_done use the right one.
    new_testrail_project_id = store.get_new_testrail_project_id(project, device)
    if new_testrail_project_id is not None:
        params["new_testrail_project_id"] = new_testrail_project_id
    # George, 2026-09-28: "docs_path why is it still editable... take away the field" logic
    # extended to flow_data_path too, as part of the new Functional/Design docs split --
    # onboard-suite no longer asks for a manually-typed flow_data_path; if one wasn't
    # already supplied, auto-resolve the first real .json export sitting in this target's
    # real Design docs upload folder (Settings > Design docs), same "system-resolved, not
    # hand-typed" treatment docs_path already gets. None found = genuinely none uploaded
    # yet, not an error -- mine_flows already skips cleanly with no flow_data_path.
    if "{flow_data_path}" in all_commands and "flow_data_path" not in params:
        design_dir = Path(store.uploads_dir_path(project, device, kind="design"))
        if design_dir.is_dir():
            json_files = sorted(design_dir.glob("*.json"))
            if json_files:
                params["flow_data_path"] = str(json_files[0])
    return params


def _run_subprocess(cmd: list[str], cwd: str, timeout: int, run_id: str | None = None):
    """The one place an actual subprocess gets spawned — using Popen (not subprocess.run)
    so an in-flight process is reachable by `cancel_run` via `_run_procs`. Returns
    (returncode, stdout, stderr); raises TimeoutExpired/OSError like subprocess.run would.

    George, 2026-09-30: "why is there these weird characters anyway always being caught
    and causing problems" -- the real, confirmed root cause of the mojibake (Â£, â€")
    flagged repeatedly all session (Reports tab, run summaries, onboard-suite's cli_output):
    `text=True` alone makes Python decode the child's stdout/stderr using
    `locale.getpreferredencoding(False)` -- cp1252 on this machine, not UTF-8. Every
    UTF-8 multi-byte character a CLI step writes (£, —, etc.) was silently misdecoded into
    2-3 garbled cp1252 characters, EVERY time, since every cli/agent step routes through
    this one function. `refresh_gap_register` already used the correct fix
    (`encoding="utf-8", errors="replace"`) for its own separate subprocess call -- this was
    simply the one place that pattern was missed. Not "weird characters" in the content;
    real characters in real spec text, corrupted by this one decode step every time."""
    proc = subprocess.Popen(
        cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace",
    )
    if run_id:
        with _procs_lock:
            _run_procs[run_id] = proc
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
        return proc.returncode, stdout, stderr
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        raise
    finally:
        if run_id:
            with _procs_lock:
                _run_procs.pop(run_id, None)


def _extract_report_path(stdout: str | None) -> str | None:
    """Pull the trailing "-> <path>" line a system_test_ops CLI prints (several different
    commands each end with their own "<did this> -> <output file>" line -- render-report,
    gap-register, push, audit, ... -- so this stays a generic arrow match, not tied to any
    one command's exact wording)."""
    match = re.search(r"-> (\S.*)$", stdout or "", re.MULTILINE)
    return match.group(1).strip() if match else None


# Only `audit`'s own result line combines a real human sentence with its report path on one
# line: "audited 842 cases: 12 BLOCKING finding(s) -- fix before opening a PR; 193 advisory.
# Report -> <path>". Matched narrowly on this literal phrasing (unlike the generic arrow
# match above) so it only ever fires for that one line, never misreads another command's
# own "-> <path>" line as if it were a summary sentence.
_AUDIT_SUMMARY_RE = re.compile(r"^(?P<summary>.*?)\s*Report -> \S.*$", re.MULTILINE)


def _extract_plain_summary(stdout: str | None) -> str | None:
    """The part of `audit`'s result line before "Report -> " is already a real, human
    sentence the tool wrote about itself, just sharing a line with the file path. Surface it
    as the run's plain-language summary (this repo's own words, not an invented one) so a
    failed gate step's card has something better to show than raw jargon, in the common case
    where no agent "summarise" step ever gets to run after a hard failure."""
    match = _AUDIT_SUMMARY_RE.search(stdout or "")
    if not match:
        return None
    summary = match.group("summary").strip()
    return summary or None


def _run_cli_step(run_id: str, step: Step, command: str) -> str:
    parts = _split_command(command)
    if parts and parts[0] == "python":
        parts[0] = str(_VENV_PYTHON)
    try:
        returncode, stdout, stderr = _run_subprocess(parts, cwd=str(_step_cwd(step)), timeout=_CLI_TIMEOUT, run_id=run_id)
    except subprocess.TimeoutExpired:
        msg = f"Timed out after {_CLI_TIMEOUT}s."
        store.update_step(run_id, step.id, status="failed", output=msg, finished_at=_now())
        store.update_run(run_id, cli_output=msg)
        return "failed"
    except OSError as exc:
        msg = f"Could not start: {exc}"
        store.update_step(run_id, step.id, status="failed", output=msg, finished_at=_now())
        store.update_run(run_id, cli_output=msg)
        return "failed"

    output = (stdout or "") + (("\n--- stderr ---\n" + stderr) if stderr else "")
    # Was `returncode in (0, 1)` on the theory that 1 means "ran fine, found blocking
    # findings" for audit-style CLIs -- but system_test_ops's own SystemExit("error: ...")
    # usage-error path (bad --project, bad --suite, etc.) ALSO exits 1, and every pipeline
    # step that actually wants "found findings, still fine" (audit.yaml) already passes
    # --no-gate specifically to force exit 0 on that case. So the (0, 1) leniency only
    # ever masked real errors in practice -- found live: a bad --project value ("NJTdryrun"
    # -- the console's own project label, not a real TestRail project name) printed a
    # clear "error: project not found" to stderr and still got marked succeeded. Strict
    # now, matching _run_gate_step's existing behaviour.
    ok = returncode == 0
    store.update_step(run_id, step.id, status="succeeded" if ok else "failed", output=output, finished_at=_now())
    # Extract this step's own "Report -> <path>" line regardless of exit code -- a gate-style
    # CLI (audit, audit-coverage) still writes a real report even when it fails on blocking
    # findings, and that freshly-written report is exactly what a following summarise step
    # needs. Was previously only extracted on success, so a failing step left the run's
    # report_path pointing at whatever a PRIOR successful step had last written -- see the
    # matching cli_output fix below for the same bug class.
    report_path = _extract_report_path(stdout)
    plain_summary = _extract_plain_summary(stdout)
    extra = {}
    if report_path:
        extra["report_path"] = report_path
    if plain_summary:
        extra["summary"] = plain_summary
    if not ok:
        # Was left unset on failure -- the run's own cli_output stayed whatever a PRIOR
        # successful step had last written, so the UI's "Run failed" card showed that
        # earlier step's output instead of the real failure. Found live, repeatedly, across
        # this whole project: a failed push_area's displayed "Result" was actually the
        # previous area's successful push output, making every failure look like it was
        # reporting the wrong step.
        #
        # George, 2026-09-30, found live AGAIN: the exact same staleness bug, just in the
        # `summary` field specifically -- `extra["summary"]` above is only ever set when
        # `_extract_plain_summary(stdout)` finds a real line to extract, which `push` never
        # prints, so `extra` stayed empty and this call never touched `summary` at all,
        # leaving the run showing author_area's PRIOR successful narrative as if it
        # explained push_area's real failure. `summary` must be explicitly cleared on
        # failure when there's nothing real to put there -- never silently left stale.
        extra.setdefault("summary", None)
        store.update_run(run_id, cli_output=output, **extra)
        return "failed"

    store.update_run(run_id, cli_output=output, **extra)
    return "succeeded"


def _run_gate_step(run_id: str, step: Step, command: str) -> str:
    """A gate re-runs a check command and must be a clean pass (returncode 0) — no
    "1 = blocking findings, still fine" leniency like a plain cli step gets, since a gate
    (e.g. onboard-suite's definition_of_done, must_be: clean_of_blocking) exists
    specifically to fail loudly when the suite isn't clean."""
    parts = _split_command(command)
    if parts and parts[0] == "python":
        parts[0] = str(_VENV_PYTHON)
    try:
        returncode, stdout, stderr = _run_subprocess(parts, cwd=str(_step_cwd(step)), timeout=_CLI_TIMEOUT, run_id=run_id)
    except (subprocess.TimeoutExpired, OSError) as exc:
        store.update_step(run_id, step.id, status="failed", output=str(exc), finished_at=_now())
        store.update_run(run_id, cli_output=str(exc))
        return "failed"
    output = (stdout or "") + (("\n--- stderr ---\n" + stderr) if stderr else "")
    ok = returncode == 0
    store.update_step(run_id, step.id, status="succeeded" if ok else "failed", output=output, finished_at=_now())
    # See _run_cli_step for why cli_output/report_path/summary all matter here, and why
    # they're captured even when the gate fails (clean_of_blocking) -- the audit CLI still
    # writes a real, fresh report (and its own plain-language result line) naming exactly
    # which findings failed the gate.
    report_path = _extract_report_path(stdout)
    plain_summary = _extract_plain_summary(stdout)
    extra = {}
    if report_path:
        extra["report_path"] = report_path
    if plain_summary:
        extra["summary"] = plain_summary
    if not ok:
        # Same staleness bug as _run_cli_step's failure branch, same fix -- see its comment.
        extra.setdefault("summary", None)
    store.update_run(run_id, cli_output=output, **extra)
    return "succeeded" if ok else "failed"


_FILE_PRODUCES_RE = re.compile(r"\.\w{1,5}$")


def _produces_a_file(produces) -> bool:
    """True if a step's `produces:` field looks like a real file path/glob to write (e.g.
    ingest-docs' distil: "knowledge/{project}/specs/*.md"), not just a description of an
    output's shape (e.g. cross_examine's "gap list (covered/missing/stale/wrong, cited)").
    Used to grant Write for specifically the steps that need to save a real file, without
    broadening every agent step that merely declares a produces: field -- most named
    agents' baseline grants are intentionally Read-only (e.g. standards-keeper is a
    reviewer elsewhere), but a step whose whole job is writing a real file needs it
    regardless of that baseline (found live: distil did real work reading 10 documents,
    then hit "the Write tool is denied for this entire session" with no way to save it)."""
    return isinstance(produces, str) and "/" in produces and bool(_FILE_PRODUCES_RE.search(produces))


def _run_agent_step(run_id: str, step: Step, params: dict, area: str | None = None) -> str:
    allowed_tools = AGENT_TOOL_GRANTS.get(step.agent or "", _DEFAULT_AGENT_TOOLS)
    reads = getattr(step, "reads", None)
    produces = getattr(step, "produces", None)
    if _produces_a_file(produces) and "Write" not in allowed_tools:
        allowed_tools = allowed_tools + ",Write,Edit"
    if area:
        # A fanned-out per-area step (e.g. author_area[fare-structure]) — one real, scoped
        # instruction per area, never "do all areas" or a copy of an old draft.
        produces_area = _render(step.produces, params).replace("<area>", area) if isinstance(step.produces, str) else f"{area}.cases.yaml"
        # Explicit real suite_id, not left for the agent to guess -- found live: without
        # this, gherkin-author wrote a literal "suite_id: TBD" placeholder (a reasonable
        # instinct given it wasn't told the real value, but it breaks push's own
        # int(spec_suite) check, which only tolerates a real number or YAML null).
        new_suite_id = params.get("new_suite_id")
        suite_line = (
            f" Use the real value suite_id: {new_suite_id} in the generated YAML's suite_id "
            f"field (not a placeholder like TBD)." if new_suite_id is not None else
            " No confirmed suite id yet -- write suite_id: null (not a placeholder like TBD)."
        )
        prompt = (
            f"For the '{area}' functional area only, carry out the '{step.id.split('[')[0]}' step "
            f"of this pipeline ({step.note or 'see pipeline definition'}). Ground everything in "
            f"knowledge/{params.get('project', '')}/specs/ for this area — never invent case content. "
            f"Produce: {produces_area}.{suite_line}"
        )
    elif reads:
        # A step with its own real reads/produces (e.g. ingest-docs' distil/cross_examine)
        # describes an actual multi-file job -- "read these sources, write this output" --
        # not "summarise the one report file a prior cli step just wrote". Build the prompt
        # from the step's own declared fields instead of guessing at report_path, which is
        # the wrong shape here and previously left distil doing nothing real (found live,
        # 2026-09-14: it reported "file wasn't found to read" against a bogus report_path
        # while the actual converted text sat untouched in dev/{project}-requirements/_text/).
        reads_list = reads if isinstance(reads, list) else [reads]
        reads_rendered = ", ".join(_render(str(r), params) for r in reads_list)
        produces_rendered = _render(str(produces), params) if produces else "the output this step describes"
        rule = getattr(step, "rule", None)
        guardrail = f" Guardrail: {rule}." if rule else ""
        prompt = (
            f"Read {reads_rendered} (paths are relative to this repo root; project={params.get('project', '')}). "
            f"{step.note or ''} Produce: {produces_rendered}.{guardrail} "
            f"Never invent facts not present in the source material — mark anything unclear GAP/UNCONFIRMED instead of guessing."
        )
    else:
        prior_run = store.get_run(run_id) or {}
        report_path = prior_run.get("report_path")
        if report_path and not (SYSTEM_TEST_OPS_ROOT / report_path).is_file():
            note = f"A prior step reported {report_path}, but that file wasn't found to read — nothing to summarise."
            store.update_step(run_id, step.id, status="succeeded", output=note, finished_at=_now())
            store.update_run(run_id, summary=note)
            return "succeeded"
        elif report_path:
            prompt = (
                f"Read the file at {report_path} and {step.note or 'summarise it in plain language'}. "
                f"No preamble, no markdown headers, 3-6 sentences."
            )
        else:
            # Found live, 2026-09-24: onboard-suite's `cross_tab` step has no `reads`/
            # `area`/prior report_path, so it fell all the way to `step.note` alone as the
            # WHOLE prompt -- "Proves shared vs device-specific dimension — never guessed."
            # with no project or device named anywhere. Reproduced directly: the agent (not
            # unreasonably) responded "I don't have a step called cross_tab -- which
            # project/device?" instead of doing real work. Every other branch above already
            # threads project/device into its prompt; this fallback is the one path that
            # didn't. A step with genuinely nothing else to go on should still at least say
            # what it's working on.
            target_line = f"Project: {params.get('project', '?')}, device: {params.get('device', '?')}. "
            prompt = target_line + (step.note or f"Carry out the '{step.id}' step of this pipeline.")

    # Optional, universal free-text field ("What are you trying to achieve with this run?",
    # George 2026-09-24: "sometimes we need prompt fields on pipelines so users can also give
    # a prompt to you about what there expecting to do with stuff you know") -- not a
    # per-pipeline declared input, available on every run regardless of pipeline. Framed
    # explicitly as context to WEIGH, not a literal instruction that overrides the step's own
    # job -- found live (in conversation, not in this codebase) that an agent given a stated
    # goal without that framing can silently widen or narrow scope past what the step actually
    # asked for.
    from Platform.webapp import reviews  # lazy: reviews imports this module
    prompt += reviews.decisions_prompt(run_id)  # what people decided earlier in this run

    intent = params.get("intent")
    if intent:
        prompt += (
            f"\n\nStated intent for this run (context for your judgment calls on this step -- "
            f"weigh it, but the step's own instructions above still govern what you actually "
            f"do): {intent}"
        )

    try:
        returncode, stdout, stderr = _run_subprocess(
            [
                "claude", "-p", prompt,
                "--allowedTools", allowed_tools,
                "--permission-prompts", "none",
                "--output-format", "json",
            ],
            cwd=str(_step_cwd(step)), timeout=_AGENT_TIMEOUT, run_id=run_id,
        )
    except subprocess.TimeoutExpired:
        # Was marked "succeeded" -- a timeout means the agent did NOT finish its work (found
        # live: distil timed out reading 10 real documents, got marked succeeded, and the
        # next step then correctly reported no specs existed since none had actually been
        # written -- a timeout must never look like a completed step).
        note = f"Timed out after {_AGENT_TIMEOUT}s before finishing — no output to trust. Re-run this step (consider fewer/smaller source files if this recurs)."
        store.update_step(run_id, step.id, status="failed", output=note, finished_at=_now())
        store.update_run(run_id, summary=note)
        return "failed"
    except OSError as exc:
        msg = f"Could not run agent: {exc}"
        store.update_step(run_id, step.id, status="failed", output=msg, finished_at=_now())
        store.update_run(run_id, summary=msg)
        return "failed"

    # `--output-format json` (was `text`, 2026-09-22) hands back real cost/token usage for
    # free alongside the same result text -- the data behind the AI-usage widget (George:
    # "a pipeline AI token usage visual to each pipeline"). A malformed/empty envelope
    # (found live possible on a killed/crashed subprocess) falls back to the raw stdout as
    # the output, with no cost recorded -- never fabricated, never crashes the step.
    cost_usd = input_tokens = output_tokens = None
    output = (stdout or "").strip() or "(the agent returned no output)"
    try:
        envelope = json.loads(stdout)
        output = (envelope.get("result") or "").strip() or "(the agent returned no output)"
        cost_usd = envelope.get("total_cost_usd")
        usage = envelope.get("usage") or {}
        input_tokens = usage.get("input_tokens")
        output_tokens = usage.get("output_tokens")
    except (json.JSONDecodeError, AttributeError):
        pass
    ok = returncode == 0
    if not ok and stderr and stderr.strip():
        # Found live, 2026-09-24: a failed agent step recorded only stdout-derived output
        # ("(the agent returned no output)" when stdout was empty), discarding stderr
        # entirely -- the one place that would actually explain a nonzero exit (crash,
        # auth error, bad --allowedTools value, etc.). Real error text beats a guess.
        output = f"{output}\n\n--- stderr (exit {returncode}) ---\n{stderr.strip()}"
    store.update_step(
        run_id, step.id, status="succeeded" if ok else "failed", output=output, finished_at=_now(),
        cost_usd=cost_usd, input_tokens=input_tokens, output_tokens=output_tokens,
    )
    store.update_run(run_id, summary=output)  # on failure too -- see _run_cli_step for why
    return "succeeded" if ok else "failed"


def _is_forced_human_command(command: str | None) -> bool:
    """True for any command that performs a real write this project's own tooling gates
    behind explicit confirmation -- regardless of what `kind:` a pipeline YAML declares.
    `--apply` added after finding tools/enrich_cases.py wired into export-automation with
    no gate at all: it's a real TestRail write (priority/estimate/[Automatable: ...] on
    Expected), same class of action as push --commit, and this codebase already uses
    --apply consistently for exactly that ("write for real", vs. a dry-run print) across
    every tool that has one -- never used for anything read-only."""
    if not command:
        return False
    return (
        ("push" in command and "--commit" in command)  # a real TestRail push --commit
        or "git push" in command  # a real push to a repo remote (e.g. test-automation-sit)
        or "--apply" in command  # a real TestRail write (e.g. enrich_cases.py --apply)
        # a real TestRail write (creates a new run) -- added for the targeted-run
        # pipeline (2026-09-22, "select EMV, not Sign On, run just that"). Doesn't
        # contain "push", so the first check above would have missed it -- found
        # BEFORE shipping, not live, by checking this function against the new command
        # rather than assuming the existing patterns already covered every write verb.
        or ("create-run" in command and "--commit" in command)
    )


def _dispatch_step(run_id: str, step: Step, params: dict, context: dict) -> str:
    """Returns one of: skipped | waiting_human | succeeded | failed."""
    when = getattr(step, "when", None)
    if when and not _eval_when(when, context):
        store.update_step(run_id, step.id, status="skipped", finished_at=_now())
        return "skipped"

    store.update_step(run_id, step.id, status="running", started_at=_now())

    # A loop-annotated step that _flatten_steps couldn't fan out (no ingested specs yet
    # for this project) reaches dispatch unexpanded — fail it clearly rather than running
    # it once as if it were a normal step.
    if getattr(step, "loop", None):
        msg = (f"Can't fan out '{step.id}' ({step.loop}) — no ingested functional-area "
               f"specs found for this project yet. Run ingest-docs first.")
        store.update_step(run_id, step.id, status="failed", output=msg, finished_at=_now())
        return "failed"

    area = step_area(step.id)
    command_params = _command_params(params)
    command = _render(step.command, command_params) if step.command else None
    if command and area:
        command = command.replace("<area>", area)  # e.g. push --file <area>.cases.yaml --commit
    if command:
        command = _resolve_optional_flags(command, command_params)  # e.g. [--include-manual]
    forced_human = _is_forced_human_command(command)

    if forced_human or step.kind is StepKind.human:
        actions = getattr(step, "actions", None)
        fallback = "; ".join(actions) if isinstance(actions, list) and actions else None
        output = f"[requires approval before this runs] {command}" if forced_human else (
            step.note or getattr(step, "action", None) or fallback or "Human step — awaiting confirmation."
        )
        store.update_step(run_id, step.id, status="waiting_human", output=output)
        return "waiting_human"

    # A cli/gate step with no real `command:` in its YAML (e.g. start.yaml's `route`, which
    # is a note describing manual orchestration logic, not a literal shell command) has
    # nothing to execute. Dispatching it as a subprocess call would crash the background
    # thread on shlex.split(None) and leave the step stuck at "running" forever — treat it
    # as informational instead, same as a step with no kind/ref at all.
    if step.kind in (StepKind.cli, StepKind.gate) and not command:
        store.update_step(run_id, step.id, status="succeeded", output=step.note or "(no command declared for this step — nothing to run)", finished_at=_now())
        return "succeeded"

    # A declared-but-not-supplied optional input (e.g. onboard-suite's flow_data_path --
    # a real Overflow UX export that genuinely may not exist for a from-scratch build)
    # leaves _render's placeholder literally in the command (`_SafeFormatDict` doesn't
    # raise on a missing key). Running that literally crashes the underlying CLI with a
    # confusing traceback (found live: mine_flows tried int('<id>')-style literal-argument
    # crashes before this existed) -- skip cleanly instead of pretending there's something
    # to execute.
    if command and re.search(r"\{[\w.]+\}", command):
        store.update_step(run_id, step.id, status="skipped", output=f"Skipped — missing input for: {command}", finished_at=_now())
        return "skipped"

    if step.kind is StepKind.cli:
        return _run_cli_step(run_id, step, command)
    if step.kind is StepKind.gate:
        return _run_gate_step(run_id, step, command)
    if step.kind is StepKind.agent:
        return _run_agent_step(run_id, step, params, area=area)

    # No kind and no ref (a pure note/informational step) — nothing to execute.
    store.update_step(run_id, step.id, status="succeeded", output=step.note or "(informational step, nothing to run)", finished_at=_now())
    return "succeeded"


def _run_pipeline_job(run_id: str, pipeline_id: str, project: str, device: str, start_index: int) -> None:
    pipeline = load_pipeline(pipeline_id)
    steps = _flatten_steps(pipeline, project, device)
    extra_inputs = _run_extra_inputs.get(run_id, {})
    try:
        params = _build_params(project, device, steps, extra_inputs)
    except ValueError as exc:
        store.update_run(run_id, status="failed", error=str(exc))
        return

    # `docs_changed` is ONLY computed for scheduled-scan specifically -- it's stateful
    # (see _docs_changed's own docstring: every call resets the comparison baseline), so
    # computing it for every pipeline run would silently consume the diff a later real
    # scheduled-scan run needed to see.
    context = {"fresh_build": _is_fresh_build(project, device)}
    if pipeline_id == "scheduled-scan":
        context["docs_changed"] = _docs_changed(project)
    cancel_event = _cancel_events.setdefault(run_id, threading.Event())

    for idx in range(start_index, len(steps)):
        if cancel_event.is_set():
            store.update_run(run_id, status="failed", error="Run cancelled.")
            return
        step = steps[idx]
        outcome = _dispatch_step(run_id, step, params, context)
        if outcome == "waiting_human":
            # George, 2026-09-30: "there should be a way to approve all so you dont have to
            # keep approving... put it into approve auto mode" -- only ever auto-acts on a
            # genuine push --commit gate (same check the console's own UI uses to decide
            # whether to show "Approve & Push" vs "Continue"), reading straight from the
            # step's own just-written output rather than re-rendering the command here.
            # Any OTHER kind of waiting_human (a real "Continue" checkpoint like
            # confirm_scope/human_cleanup) still stops here for a real look, same as always.
            if run_id in _auto_approve_runs:
                fresh = store.get_steps(run_id)
                this_step = next((s for s in fresh if s["step_id"] == step.id), None)
                out = (this_step or {}).get("output") or ""
                if "push" in out and "--commit" in out:
                    resolve_step(run_id, step.id)
                    return
                _auto_approve_runs.discard(run_id)
            store.update_run(run_id, status="waiting_human")
            return
        if outcome == "failed":
            # A cancel mid-step terminates the in-flight subprocess (see cancel_run), which
            # makes that step return "failed" like any other error -- so without this check
            # a genuinely cancelled run was reported as "Step 'X' failed", indistinguishable
            # from a real failure. Checked here, not inside the step runners themselves,
            # since any step kind (cli/gate/agent) can be the one mid-flight when cancel
            # fires, and this is the one place all of them funnel through.
            _auto_approve_runs.discard(run_id)  # any real failure needs a fresh, deliberate re-opt-in
            if cancel_event.is_set():
                store.update_run(run_id, status="failed", error="Run cancelled.")
            else:
                store.update_run(run_id, status="failed", error=f"Step '{step.id}' failed.")
            return
        # succeeded / skipped -> keep going

    _auto_approve_runs.discard(run_id)  # terminal -- nothing left to auto-approve
    store.update_run(run_id, status="succeeded")


def start_run(pipeline_id: str, project: str, device: str, extra_inputs: dict[str, str] | None = None) -> str:
    """Kicks off a real run of ANY pipeline in the background, returns a run id to poll.
    `extra_inputs` covers whatever a pipeline declares beyond project/device/suite ids
    (e.g. ingest-docs' docs_path) — app.py validates required ones are present before
    calling this, using the pipeline's own `inputs:` list as the source of truth.
    Raises KeyError for an unknown pipeline id, ValueError if a required suite id isn't
    configured for this target — both map to HTTP 404/400 in app.py."""
    pipeline = load_pipeline(pipeline_id)
    steps = _flatten_steps(pipeline, project, device)
    extra_inputs = extra_inputs or {}
    _build_params(project, device, steps, extra_inputs)  # validate up front — don't create a run row if this will fail immediately

    run_id = str(uuid.uuid4())
    _run_extra_inputs[run_id] = extra_inputs
    store.create_run(run_id, pipeline_id, project, device, extra_inputs=extra_inputs)
    store.create_step_rows(run_id, [(s.id, s.kind.value if s.kind else None) for s in steps])
    _cancel_events[run_id] = threading.Event()

    thread = threading.Thread(target=_run_pipeline_job, args=(run_id, pipeline_id, project, device, 0), daemon=True)
    thread.start()
    return run_id


def start_audit_run(project: str, device: str) -> str:
    """Kept for existing callers — audit is now just start_run("audit", ...) going through
    the same generic engine as everything else (the explicit regression-check case)."""
    return start_run("audit", project, device)


def start_scheduled_scan(project: str, device: str) -> str:
    """The one entry point for a scheduled-scan run, used identically by the periodic
    scheduler and the console's manual "Run now" button -- docs_path is supplied HERE,
    automatically, via the same real resolution the Ingest page and refresh-check use
    (TestOpsRequirements/<project>/_current/ when it exists), never left for a human to
    type in (there's no human present on a scheduled run, and the manual button
    shouldn't need to ask for something the system already knows)."""
    real = store.resolve_ingest_docs_source(project)
    docs_path = real["path"] or str(_REQUIREMENTS_ROOT / project.lower())
    return start_run("scheduled-scan", project, device, extra_inputs={"docs_path": docs_path})


class CaseReviewPendingError(RuntimeError):
    """Raised by resolve_step when a build's human_cleanup is approved while cases from the
    repair step are still open on the Case Review screen. app.py maps this to 409."""


class TargetNotApprovedError(RuntimeError):
    """Raised by resolve_step when a push+--commit gate is resolved for a target that has
    no persisted sign-off (store.is_target_approved) — independent of, and in addition to,
    the per-run human gate every push step already goes through. app.py maps this to 403."""


def _resolved_step(run_id: str, run: dict, step_id: str) -> tuple[Step | None, str | None]:
    """Re-derives a flattened step (with its <area> substituted, if fanned-out) and its
    fully rendered command, the same way _dispatch_step would have — needed here because
    pipeline_run_steps only stores the step's *output* summary, not its original templated
    command or Step object."""
    pipeline = load_pipeline(run["pipeline_id"])
    steps = _flatten_steps(pipeline, run["project"], run["device"])
    step = next((s for s in steps if s.id == step_id), None)
    if step is not None:
        area = step_area(step_id)
        if area and step.command:
            step = step.model_copy(update={"command": step.command.replace("<area>", area)})
    if step is None or not step.command:
        return step, None
    extra_inputs = _run_extra_inputs.get(run_id, {})
    params = _command_params(_build_params(run["project"], run["device"], steps, extra_inputs))
    return step, _resolve_optional_flags(_render(step.command, params), params)


def _step_command(run_id: str, run: dict, step_id: str) -> str | None:
    return _resolved_step(run_id, run, step_id)[1]


def _resume_index(run: dict, step_id: str, stored_idx: int) -> int:
    """Where `step_id` sits in the pipeline's CURRENT step list.

    A run stores its own step rows when it starts, but resuming (Continue / Retry) walks the
    pipeline's current YAML. If the YAML gained or lost a step after the run began, the stored
    position points at the wrong step -- found live 2026-10-01: a build started before `repair`
    was added kept restarting `human_cleanup` (one position later in the new list) instead of
    finishing. Looking the step up by id keeps both lists in agreement; the stored position is
    only the fallback if the step no longer exists in the YAML at all."""
    try:
        ids = [s.id for s in _flatten_steps(load_pipeline(run["pipeline_id"]), run["project"], run["device"])]
    except Exception:  # noqa: BLE001 -- resuming must never be blocked by a pipeline-load problem
        return stored_idx
    return ids.index(step_id) if step_id in ids else stored_idx


def resolve_step(run_id: str, step_id: str) -> None:
    """Advances a `waiting_human` step to `succeeded` and resumes the run from the next
    step — this is what the UI's "Approve & Push" / "Continue" button calls. Raises
    KeyError if the run or step doesn't exist; callers should check status themselves
    first (app.py returns 409 for a step that isn't actually waiting). Raises
    TargetNotApprovedError if this step is a push+--commit gate and the target
    (project/device) has no persisted approval yet (store.is_target_approved) — a second,
    independent precondition on top of this per-step human gate, not a substitute for it."""
    run = store.get_run(run_id)
    if run is None:
        raise KeyError(f"No such run '{run_id}'")
    steps_meta = store.get_steps(run_id)
    ids_in_order = [s["step_id"] for s in steps_meta]
    if step_id not in ids_in_order:
        raise KeyError(f"No such step '{step_id}' in run '{run_id}'")

    step, command = _resolved_step(run_id, run, step_id)
    if run["pipeline_id"] == "onboard-suite" and step_id == "human_cleanup":
        # The repair step handed these cases to a person because a machine must not guess at
        # them. The build is not done until each is fixed or knowingly accepted.
        from Platform.webapp import case_review
        n_open = case_review.open_count(run["project"], run["device"])
        if n_open:
            raise CaseReviewPendingError(
                f"{n_open} case(s) still need review. Open Case Review, fix or accept each one, then continue."
            )
    # A real write TO THE CONFIGURED TARGET (push --commit, or create-run --commit --
    # added 2026-09-22 for targeted-run) requires that target's own persisted approval,
    # in addition to this per-step human gate. Deliberately narrower than
    # _is_forced_human_command above -- --apply and "git push" are real writes too, but
    # not to this project/device's TestRail target specifically (--apply's target is
    # implied by --suite same as these; "git push" is a DIFFERENT repo's remote
    # entirely), so target-approval isn't the right check for those.
    is_write_to_target = bool(command) and "--commit" in command and ("push" in command or "create-run" in command)
    if is_write_to_target and not store.is_target_approved(run["project"], run["device"]):
        # Refused, but retryable: leave the step at waiting_human (not failed) so approving
        # the target and clicking "Approve & Push" again just works, rather than requiring
        # the whole run to be restarted from scratch.
        store.update_step(
            run_id, step_id, status="waiting_human",
            output=f"Refused: {run['project']}/{run['device']} has no persisted approval yet — "
                   "approve this target, then retry Approve & Push.",
        )
        raise TargetNotApprovedError(f"{run['project']}/{run['device']} is not approved.")

    forced_human = _is_forced_human_command(command)
    if forced_human and step is not None:
        # This step was forced into waiting_human specifically so a human could approve the
        # real command before it runs -- approving must actually RUN it now, not just mark
        # it succeeded and move on. Found live: George's onboard-suite push_area was
        # approved, advanced to "succeeded", and the run continued all the way through
        # definition_of_done -- but the real `push --commit` was never executed, so nothing
        # ever reached TestRail despite every downstream step looking like it had worked.
        outcome = _run_cli_step(run_id, step, command)
        if outcome != "succeeded":
            store.update_run(run_id, status="failed", error=f"Step '{step_id}' failed.")
            return
    else:
        store.update_step(run_id, step_id, status="succeeded", finished_at=_now())

    store.update_run(run_id, status="running")
    _cancel_events[run_id] = threading.Event()

    idx = _resume_index(run, step_id, ids_in_order.index(step_id))
    thread = threading.Thread(
        target=_run_pipeline_job,
        args=(run_id, run["pipeline_id"], run["project"], run["device"], idx + 1),
        daemon=True,
    )
    thread.start()


def retry_failed_step(run_id: str, step_id: str) -> None:
    """Resumes a failed run from the step that actually failed, instead of the whole
    pipeline having to start over from step 1 -- some steps (author_area's per-area agent
    calls) genuinely take several minutes each, so a failure late in a long onboard-suite
    run shouldn't throw away everything before it. Raises KeyError if the run/step doesn't
    exist, ValueError if the run isn't actually failed or this isn't the step that failed
    (retry the real failure point, not an arbitrary earlier step) -- callers should map
    both to a 4xx, not silently retry the wrong thing."""
    run = store.get_run(run_id)
    if run is None:
        raise KeyError(f"No such run '{run_id}'")
    if run["status"] != "failed":
        raise ValueError(f"Run '{run_id}' isn't in a failed state (status: {run['status']}).")
    steps_meta = store.get_steps(run_id)
    ids_in_order = [s["step_id"] for s in steps_meta]
    if step_id not in ids_in_order:
        raise KeyError(f"No such step '{step_id}' in run '{run_id}'")
    failed_status = next((s["status"] for s in steps_meta if s["step_id"] == step_id), None)
    if failed_status != "failed":
        raise ValueError(f"Step '{step_id}' isn't the one that failed (status: {failed_status}).")

    store.update_step(run_id, step_id, status="pending", output=None, started_at=None, finished_at=None)
    store.update_run(run_id, status="running", error=None)
    _cancel_events[run_id] = threading.Event()

    idx = _resume_index(run, step_id, ids_in_order.index(step_id))
    thread = threading.Thread(
        target=_run_pipeline_job,
        args=(run_id, run["pipeline_id"], run["project"], run["device"], idx),
        daemon=True,
    )
    thread.start()


def cancel_run(run_id: str) -> None:
    """Sets a flag the run loop checks between steps, and terminates an in-flight
    subprocess if one is running right now. In-memory only (`_cancel_events`/`_run_procs`)
    — doesn't survive a process restart, which is fine for a single-user local app; a run
    left `running` across a restart just won't ever cancel cleanly, it'll sit there until
    manually marked failed (a real gap, acceptable for now).

    Found live (George, 2026-09-28: "not sure if cancelling runs actually works either"):
    a run paused at `waiting_human` has no live thread and no in-flight subprocess at all
    — the pipeline job already returned after writing that status. Setting the event alone
    did nothing observable; the run just sat as `waiting_human` forever, cancel button and
    all, looking exactly like cancel was broken. `waiting_human` (and any other non-running
    status — defensively, in case a future status is added) has nothing left to terminate,
    so mark it cancelled directly instead of only flagging for a loop that will never run
    again. A genuinely `running` run still goes through the flag+terminate path below,
    which the loop's own cancel_event check (between steps) and the newly-added
    mid-step-termination check (see _run_pipeline_job) both handle.

    George, 2026-09-30, found live AGAIN (same root cause, a different trigger this time):
    "i cancelled but nothing happened" -- a real onboard-suite author_area step's `claude`
    subprocess had already exited on its own (confirmed: no such process left running), but
    the background thread never noticed and the step sat at `running` in the database well
    past its own 900s timeout, with `_run_procs` holding nothing for this run_id by the time
    cancel ran. `status == "running"` took the "still has something to terminate" branch,
    found `proc is None`, and did NOTHING observable -- same failure shape as the
    `waiting_human` case above, just reached a different way. There is no meaningful
    difference, from the caller's side, between "nothing left to terminate because it
    already finished" (waiting_human) and "nothing left to terminate because it's already
    gone" (this case) -- both need the same direct mark-as-cancelled fallback, not silence."""
    _auto_approve_runs.discard(run_id)  # a deliberate cancel always needs a fresh re-opt-in too
    event = _cancel_events.setdefault(run_id, threading.Event())
    event.set()
    run = store.get_run(run_id)
    if run is not None and run.get("status") != "running":
        store.update_run(run_id, status="failed", error="Run cancelled.")
        return
    with _procs_lock:
        proc = _run_procs.get(run_id)
    if proc is not None and proc.poll() is None:
        try:
            proc.terminate()
        except OSError:
            pass
    elif run is not None:
        # No live process to terminate (already exited/orphaned, e.g. a subprocess that
        # finished or crashed without the tracking thread registering it) -- same real
        # outcome as the waiting_human case above: there's nothing left to actually stop,
        # so silently returning here just looks like cancel is broken. Mark it directly --
        # the run AND whichever step is still stuck at "running" (never leave the step
        # list itself showing "running" forever just because the run-level status moved on).
        for s in store.get_steps(run_id):
            if s["status"] == "running":
                store.update_step(
                    run_id, s["step_id"], status="failed",
                    output="Cancelled: the underlying process for this step had already "
                           "exited without being detected (no live process left to "
                           "terminate). Retry this step fresh.",
                    finished_at=_now(),
                )
        store.update_run(run_id, status="failed", error="Run cancelled.")


def set_auto_approve(run_id: str, enabled: bool) -> None:
    """Server-side toggle for onboard-suite's repeated push --commit gates (see
    _auto_approve_runs' own comment for why this had to move out of the browser). Enabling
    on a run currently sitting at a genuine push gate (waiting_human) must resume it right
    now, not just flip the flag and wait for the next unrelated poll/action to notice."""
    if not enabled:
        _auto_approve_runs.discard(run_id)
        return
    _auto_approve_runs.add(run_id)
    run = store.get_run(run_id)
    if run is None or run.get("status") != "waiting_human":
        return
    steps_meta = store.get_steps(run_id)
    waiting = next((s for s in steps_meta if s["status"] == "waiting_human"), None)
    if waiting is None:
        return
    out = waiting.get("output") or ""
    if "push" in out and "--commit" in out:
        resolve_step(run_id, waiting["step_id"])


# George, 2026-09-29: "how come we can't ensure a sync button to re-check ... if yes
# connected or not" -- real gap found while building this: Settings' "TestRail credentials"
# card only ever showed whether a row was SAVED in this app's own encrypted store
# (store.get_credentials_status), never whether that's a WORKING connection -- and, dug
# further, that saved row isn't even what any real TestRail call in this app actually uses.
# Every real call (this file's _case_count/get_run_comments, every CLI pipeline step) goes
# through system-test-ops/.env on disk via the `system_test_ops` CLI's own config loading --
# store.decrypt_api_key exists but nothing calls it. So a real "check connection" button has
# to test THAT real path, not the console's separately-stored, currently-unused row.
def check_testrail_connection() -> dict:
    """Real, live TestRail connectivity check -- runs `system_test_ops check`, the exact
    same command docs/CLAUDE.md's quick reference lists for this ("validate creds, list
    projects"). Real exit-code contract (system_test_ops/cli.py's main()): 0 = connected,
    2 = config error (missing/malformed env), 1 = TestRail API error (bad key, network).
    Never guesses -- reports the real stdout/stderr either way."""
    try:
        result = subprocess.run(
            [str(_VENV_PYTHON), "-m", "system_test_ops", "check"],
            cwd=str(SYSTEM_TEST_OPS_ROOT), capture_output=True, text=True, timeout=30,
            encoding="utf-8", errors="replace",
        )
    except subprocess.TimeoutExpired:
        return {"connected": False, "detail": "Timed out after 30s — check network/TestRail availability."}
    except OSError as exc:
        return {"connected": False, "detail": f"Could not run the check: {exc}"}

    if result.returncode == 0:
        # Matches only on the digit count, never surfaces the CLI's own decorative
        # "OK — connected..." line verbatim -- found live: that raw text comes back with a
        # mangled em-dash when the check runs under the long-running uvicorn process
        # specifically (a one-off script call decodes it fine; something about that
        # specific parent process's inherited console codepage doesn't) even with
        # encoding="utf-8" set here. Real, not just cosmetic-ignorable, so side-stepped
        # entirely -- build the message ourselves instead of trusting the child's raw text.
        match = re.search(r"(\d+) project\(s\) visible", result.stdout)
        count = int(match.group(1)) if match else None
        detail = f"Connected - {count} project(s) visible." if count is not None else "Connected."
        return {"connected": True, "detail": detail, "project_count": count}
    raw = (result.stderr or result.stdout or "").strip()
    first_line = raw.splitlines()[0] if raw else "Unknown failure."
    # Same mangled-non-ascii risk on the failure path (a real TestRail error message could
    # contain anything) -- strip to ascii rather than risk showing garbled bytes.
    detail = first_line.encode("ascii", errors="replace").decode("ascii")
    return {"connected": False, "detail": detail}


# George, 2026-09-29: "we need to be able to re-check these gaps against new specs
# uploaded, so a refresh button" -- the gap-register CLI is a cheap, read-only grep (no AI,
# no TestRail), so this can genuinely refresh the fixture live rather than staying frozen at
# whatever the last committed snapshot was.
_GAPS_FIXTURE = _PLATFORM_ROOT / "webapp" / "fixtures" / "gaps.json"


def _marker_keys(path) -> set[str]:
    try:
        return {re.sub(r"\s+", " ", (m.get("text") or "")).strip()[:160] for m in json.loads(path.read_text(encoding="utf-8"))}
    except (OSError, ValueError, AttributeError):
        return set()


def refresh_gap_register() -> dict:
    before = _marker_keys(_GAPS_FIXTURE) if _GAPS_FIXTURE.is_file() else None
    try:
        result = subprocess.run(
            [str(_VENV_PYTHON), "-m", "system_test_ops", "gap-register", "--json-out", str(_GAPS_FIXTURE)],
            cwd=str(SYSTEM_TEST_OPS_ROOT), capture_output=True, text=True, timeout=60,
            encoding="utf-8", errors="replace",
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "detail": "Timed out after 60s."}
    except OSError as exc:
        return {"ok": False, "detail": f"Could not run the refresh: {exc}"}
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "Unknown failure.").strip().splitlines()[0] if (result.stderr or result.stdout) else "Unknown failure."
        return {"ok": False, "detail": detail}
    total = None
    if _GAPS_FIXTURE.is_file():
        try:
            total = len(json.loads(_GAPS_FIXTURE.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            pass
    out = {"ok": True, "total": total, "refreshed_at": _now()}
    if before is not None:
        after = _marker_keys(_GAPS_FIXTURE)
        out["closed"] = len(before - after)      # marker text no longer anywhere in the notes/cases
        out["new"] = len(after - before)         # markers that were not there at the last refresh
        out["unchanged"] = len(before & after)
    return out


def _case_counts(suite_id: int) -> tuple[int | None, int]:
    """(live case count, cases marked for delete) for one suite via `system_test_ops cases`
    (read-only -- it only reads TestRail and writes local report files). Parses the CLI's own
    "Wrote N cases (M more marked for delete, left out) ->" line rather than re-implementing the
    TestRail call here. Retired cases (ZZ_DELETE prefix, or sitting in the delete folder) are
    never part of N: every count on a dashboard is live cases only, with M reported separately."""
    try:
        result = subprocess.run(
            [str(_VENV_PYTHON), "-m", "system_test_ops", "cases", "--suite", str(suite_id)],
            cwd=str(SYSTEM_TEST_OPS_ROOT), capture_output=True, text=True, timeout=60,
        )
    except (subprocess.TimeoutExpired, OSError):
        return None, 0
    match = re.search(r"Wrote (\d+) cases(?: \((\d+) more marked for delete)?", result.stdout)
    if not match:
        return None, 0
    return int(match.group(1)), int(match.group(2) or 0)


def _case_count(suite_id: int) -> int | None:
    """Live case count only (see _case_counts)."""
    return _case_counts(suite_id)[0]


def get_run_comments(project: str, device: str, which: str = "new", last_n: int = 5) -> dict:
    """Real TestRail run comments (reviewer notes left when marking a result Passed/Failed/
    Invalid/etc) -- read-only, direct TestRailClient import (no CLI subprocess needed since
    this doesn't need to write any report file). Answers George's "is this a function
    already???" (2026-09-09): no, nothing in this app surfaced result comments before this.

    `which` picks old (read-only reference) or new (write target) suite -- useful either
    way: a comment on the OLD suite's last real run is exactly the kind of evidence a
    case-correctness question should cite; a comment on the NEW suite tracks review of
    work actually done here.
    """
    ids = store.get_suite_ids(project, device)
    if not ids or ids.get(f"{which}_suite_id") is None:
        return {"available": False, "reason": f"No {which}_suite_id configured for this target."}
    suite_id = ids[f"{which}_suite_id"]

    # Shelled out to system-test-ops' own venv (has requests/dotenv; this app's venv
    # doesn't) -- same execution boundary as the audit CLI step, just a read-only
    # TestRailClient call with no CLI subcommand of its own yet, so a small inline script
    # instead of a `python -m system_test_ops ...` invocation. Prints one JSON line.
    script = (
        "import json, os\n"
        "from system_test_ops.testrail.client import TestRailClient\n"
        "client = TestRailClient()\n"
        "project_id = int(os.environ['TESTRAIL_PROJECT_ID'])\n"
        f"suite_id = {suite_id}\n"
        f"last_n = {last_n}\n"
        "runs = [r for r in client.get_runs(project_id) if r.get('suite_id') == suite_id]\n"
        "runs.sort(key=lambda r: r.get('created_on', 0), reverse=True)\n"
        "runs = runs[:last_n]\n"
        "comments = []\n"
        "for run in runs:\n"
        "    test_to_case = {t['id']: t.get('case_id') for t in client.get_tests(run['id'])}\n"
        "    for result in client.get_results_for_run(run['id']):\n"
        "        if result.get('comment'):\n"
        "            comments.append({\n"
        "                'run_id': run['id'], 'run_name': run.get('name', f\"Run {run['id']}\"),\n"
        "                'case_id': test_to_case.get(result.get('test_id')), 'status_id': result.get('status_id'),\n"
        "                'comment': result['comment'], 'created_by': result.get('created_by'),\n"
        "                'created_on': result.get('created_on'), 'defects': result.get('defects'),\n"
        "            })\n"
        "comments.sort(key=lambda c: c.get('created_on') or 0, reverse=True)\n"
        "print(json.dumps({'runs_checked': len(runs), 'comments': comments}))\n"
    )
    try:
        result = subprocess.run(
            [str(_VENV_PYTHON), "-c", script],
            cwd=str(SYSTEM_TEST_OPS_ROOT), capture_output=True, text=True, timeout=60,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        return {"available": False, "reason": f"Could not run TestRail query: {exc}"}
    if result.returncode != 0:
        return {"available": False, "reason": f"TestRail call failed: {result.stderr.strip()[-500:]}"}
    try:
        payload = json.loads(result.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return {"available": False, "reason": "Could not parse TestRail response."}
    return {"available": True, "suite_id": suite_id, **payload}


# George, 2026-09-30: "POS TL suite name new one, is GG - POS - Claude Suite but on
# testrail it is something else? do we need to ensure the naming is correct for the ID or
# refresh if been changed" -- real, live check: does the display name stored in
# suite_targets.yaml still match what TestRail actually calls that suite id right now.
# Uses `list-suites` (one cheap API call, id+name for every suite in a project), not
# `cases` (which would download every case in the suite just to read its name).
def _real_suite_names(testrail_project_id: int) -> dict[int, str] | None:
    result = subprocess.run(
        [str(_VENV_PYTHON), "-m", "system_test_ops", "list-suites", "--project", str(testrail_project_id)],
        cwd=str(SYSTEM_TEST_OPS_ROOT), capture_output=True, text=True, timeout=30,
        encoding="utf-8", errors="replace",
    )
    if result.returncode != 0:
        return None
    try:
        suites = json.loads(result.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return None
    return {s["id"]: s.get("name") for s in suites}


def check_suite_name_drift(project: str, device: str) -> dict:
    mapping = next(
        (m for m in store.list_suite_mappings() if m["project"] == project and m["device"] == device),
        None,
    )
    if mapping is None:
        return {"available": False, "reason": "No suite mapping configured for this target."}
    ok, why = _testrail_reachable()
    if not ok:
        return {"available": False, "reason": why}
    checks = []
    by_tr_project: dict[int, dict[int, str] | None] = {}
    for label, suite_id, stored_name, tr_project in (
        ("old", mapping.get("old_suite_id"), mapping.get("old_suite"), mapping.get("testrail_project_id")),
        ("new", mapping.get("new_suite_id"), mapping.get("new_suite"),
         mapping.get("new_testrail_project_id") or mapping.get("testrail_project_id")),
    ):
        if suite_id is None or tr_project is None or not stored_name:
            continue
        if tr_project not in by_tr_project:
            by_tr_project[tr_project] = _real_suite_names(tr_project)
        real_names = by_tr_project[tr_project]
        if real_names is None:
            checks.append({"which": label, "suite_id": suite_id, "stored_name": stored_name,
                           "real_name": None, "drifted": None, "reason": "Could not reach TestRail."})
            continue
        real_name = real_names.get(suite_id)
        checks.append({
            "which": label, "suite_id": suite_id, "stored_name": stored_name, "real_name": real_name,
            "drifted": real_name is not None and real_name != stored_name,
        })
    return {"available": True, "checks": checks}


def preview_docs_relevance(project: str, docs_path: str) -> dict:
    """Runs ingest-docs' real convert + relevance_check steps synchronously, standalone --
    no tracked run, no AI, no distil/cross_examine/commit_pr (George, 2026-09-22: "an
    initial review of the docs before ingesting, so it can pass the gate"). Writes into
    the SAME real dev/{project}-requirements/_text/ work dir the actual Ingest run would
    use, so nothing here is thrown away -- a real Ingest run afterward doesn't redo this
    conversion, `ingest_docs.py` is idempotent."""
    convert = subprocess.run(
        [str(_VENV_PYTHON), "tools/ingest_docs.py", "--project", project, "--src", docs_path],
        # 120s was too short for a real library: Translink's 352 docs take ~2m45s
        # (measured 2026-09-23), so the preview button timed out on the exact project
        # it was built for. Generous ceiling; a genuinely hung convert still gets caught.
        cwd=str(SYSTEM_TEST_OPS_ROOT), capture_output=True, text=True, timeout=900,
    )
    if convert.returncode != 0:
        return {"ok": False, "stage": "convert", "output": (convert.stdout or "") + (convert.stderr or "")}
    text_dir = f"dev/{project}-requirements/_text"
    relevance = subprocess.run(
        [str(_VENV_PYTHON), "tools/check_doc_relevance.py", "--project", project, "--text-dir", text_dir, "--src", docs_path],
        cwd=str(SYSTEM_TEST_OPS_ROOT), capture_output=True, text=True, timeout=60,
    )
    return {
        "ok": relevance.returncode == 0,
        "stage": "relevance_check",
        "convert_output": convert.stdout,
        "output": (relevance.stdout or "") + (relevance.stderr or ""),
    }


def get_suite_sections(project: str, device: str) -> dict:
    """Real, live section tree for the new (write-target) suite -- the checkbox tree
    behind targeted-run's front end (George, 2026-09-22: "select EMV, not Sign On, run
    just that"). Read-only. `@feature(<area>)` IS the section, per docs/gherkin-
    standard.md -- this is the exact same data create-run --areas matches against, just
    fetched here so the console can render a real tree instead of free text."""
    ids = store.get_suite_ids(project, device)
    if not ids or ids.get("new_suite_id") is None:
        return {"available": False, "reason": "No new_suite_id configured for this target."}
    suite_id = ids["new_suite_id"]
    project_id = store.get_new_testrail_project_id(project, device) or store.get_testrail_project_id(project, device)
    if project_id is None:
        return {"available": False, "reason": "No TestRail project id configured for this target's new suite."}
    script = (
        "import json\n"
        "from system_test_ops.testrail.client import TestRailClient\n"
        "client = TestRailClient()\n"
        f"project_id = {project_id!r}\n"
        f"suite_id = {suite_id}\n"
        "sections = client.get_sections(project_id, suite_id)\n"
        "print(json.dumps([{'id': int(s['id']), 'name': s.get('name'), 'parent_id': (int(s['parent_id']) if s.get('parent_id') else None)} for s in sections]))\n"
    )
    try:
        result = subprocess.run(
            [str(_VENV_PYTHON), "-c", script],
            cwd=str(SYSTEM_TEST_OPS_ROOT), capture_output=True, text=True, timeout=60,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        return {"available": False, "reason": f"Could not run TestRail query: {exc}"}
    if result.returncode != 0:
        return {"available": False, "reason": f"TestRail call failed: {result.stderr.strip()[-500:]}"}
    try:
        sections = json.loads(result.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return {"available": False, "reason": "Could not parse TestRail response."}
    return {"available": True, "suite_id": suite_id, "sections": sections}


def compare_suite_case_counts(project: str, device: str) -> dict:
    """Real old-vs-new case counts for a target, live from TestRail (two read-only CLI
    calls) -- suggested in ISSUES.md, buildable now that credentials + both suite ids
    (old_suite_id added 2026-09-09) exist for the seeded Translink pairs."""
    ids = store.get_suite_ids(project, device)
    if not ids or ids["old_suite_id"] is None or ids["new_suite_id"] is None:
        return {"available": False, "reason": "old_suite_id and/or new_suite_id not configured for this target."}
    ok, why = _testrail_reachable()
    if not ok:
        return {"available": False, "reason": why}
    old_count, old_marked = _case_counts(ids["old_suite_id"])
    new_count, new_marked = _case_counts(ids["new_suite_id"])
    if old_count is None or new_count is None:
        return {"available": False, "reason": "Could not pull live case counts (check TestRail credentials/connectivity)."}
    return {
        "available": True,
        "old_suite_id": ids["old_suite_id"], "new_suite_id": ids["new_suite_id"],
        "old_case_count": old_count, "new_case_count": new_count,
        # Retired cases waiting to be binned: never counted above, shown beside them instead.
        "old_marked_for_delete": old_marked, "new_marked_for_delete": new_marked,
        "diff": new_count - old_count,
    }


# George, 2026-09-29: the "ask" box next to the target picker -- a single one-shot,
# read-only agent call (same claude -p / --output-format json mechanism _run_agent_step
# uses, but no run_id/pipeline scaffolding -- this is a synchronous question/answer, not a
# background job). Two grounding modes, agent picks which one(s) a question needs:
#   - "tool_usage": grounds ONLY on this repo's own real pipeline definitions
#     (.claude/pipelines/*.yaml) -- "what do I run for a new POS doc?" answers from the same
#     data the console's own pipeline pages render from, so it can't drift from what's true.
#   - "data": grounds ONLY on the current project/device's real knowledge pool
#     (knowledge/<project>/specs/, excluding _archive/, filtered to files matching the
#     device) plus that project/device's gap-register markers -- never the raw confidential
#     requirement library (that stays local-only, per CLAUDE.md).
# Never a bare "I don't know" -- every non-answer is one of the 5 honest states George asked
# for, verbatim: gap (not documented anywhere), unconfirmed (specified but unverified on the
# real system), out_of_scope (wrong device/project for this pool), partial (some of it is
# grounded, some isn't -- say which), not_ingested (the raw docs may cover it, but nothing's
# been ingested into knowledge/ yet -- a tool-coverage gap, not a real documentation gap).
_ASK_TIMEOUT = 90
_ASK_ALLOWED_TOOLS = "Read,Glob,Grep"
_ASK_VALID_KINDS = {"answer", "gap", "unconfirmed", "out_of_scope", "partial", "not_ingested"}


def _ask_prompt(project: str, device: str | None, question: str) -> str:
    target_line = f"Project: {project}, device: {device or '(none — project-wide)'}."
    return f"""{target_line} Question: {question}

You are answering ONE question for a test-ops engineer, read-only (Read/Glob/Grep only, no
writes, no shell). Decide which grounding pool the question needs:

- "tool_usage" -- questions about how to use THIS console/repo itself (which pipeline to run,
  what order, what a pipeline needs as input). Ground ONLY on the real pipeline definitions
  under .claude/pipelines/*.yaml (index.yaml lists them all) and docs/using-claude.md. Never
  guess at a pipeline's real inputs/steps -- read the actual YAML.
- "data" -- questions about what the project/device's real test suite/specs actually say.
  Ground ONLY on knowledge/{project.lower()}/specs/*.md (skip any _archive/ subfolder --
  archived, superseded) filtered to files genuinely about device={device or '(any)'}, plus
  that project/device's markers in proposals/**/gap-register.md if present. Do NOT read any
  raw confidential requirement library outside knowledge/ -- if the answer isn't in
  knowledge/, it counts as not there, not as "go check the raw docs yourself".

Never invent an answer. If you cannot ground a data question fully in what you actually read,
classify it as one of these 5 honest states (never a bare "I don't know"):
  - "gap": genuinely not documented anywhere you can see -- not in knowledge/, not implied.
  - "unconfirmed": a spec mentions/specifies it, but nothing confirms it's verified true on
    the real system -- state what's specified and that it's unconfirmed.
  - "out_of_scope": this is a real, answerable fact, but for a different device/project than
    the one asked about -- say which pool it would belong to instead, if you can tell.
  - "partial": some of the question is grounded, some isn't -- answer the grounded part and
    say exactly what's missing.
  - "not_ingested": you have a specific reason to believe the raw requirement library covers
    this (e.g. a knowledge note cites a spec section that sounds adjacent but the actual
    named fact isn't in the note) but nothing in knowledge/ actually contains it -- so this
    tool cannot see it yet, distinct from a real gap in the documentation itself.
A "tool_usage" question that's genuinely answerable from the pipeline definitions is always
kind "answer" -- the 5-state taxonomy above is for "data" questions only.

Reply with ONLY this JSON object, no other text, no markdown fences:
{{"mode": "tool_usage" or "data", "kind": "answer" or one of the 5 states above, "answer": "<the answer, or a plain-English explanation of the non-answer state>", "citations": ["<real file path you actually read>", ...], "next_step": "<optional -- e.g. which pipeline to run next, or what doc to go find/upload -- omit or empty string if not applicable>"}}"""


def ask_question(project: str, device: str | None, question: str) -> dict:
    prompt = _ask_prompt(project, device, question)
    try:
        returncode, stdout, stderr = _run_subprocess(
            ["claude", "-p", prompt, "--allowedTools", _ASK_ALLOWED_TOOLS,
             "--permission-prompts", "none", "--output-format", "json"],
            cwd=str(SYSTEM_TEST_OPS_ROOT), timeout=_ASK_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return {"mode": None, "kind": "error", "answer": f"Timed out after {_ASK_TIMEOUT}s -- try a narrower question.", "citations": [], "next_step": ""}
    except OSError as exc:
        return {"mode": None, "kind": "error", "answer": f"Could not run agent: {exc}", "citations": [], "next_step": ""}

    if returncode != 0:
        detail = (stderr or "").strip() or "(no stderr)"
        return {"mode": None, "kind": "error", "answer": f"Agent call failed (exit {returncode}): {detail}", "citations": [], "next_step": ""}

    try:
        envelope = json.loads(stdout)
        result_text = (envelope.get("result") or "").strip()
    except (json.JSONDecodeError, AttributeError):
        return {"mode": None, "kind": "error", "answer": "Agent returned no usable output.", "citations": [], "next_step": ""}

    try:
        parsed = json.loads(result_text)
    except json.JSONDecodeError:
        # The agent answered in free text instead of the strict JSON contract -- show the
        # real text rather than discarding it, but flag that the reply wasn't self-classified.
        return {"mode": None, "kind": "error", "answer": result_text or "(the agent returned no output)", "citations": [], "next_step": ""}

    kind = parsed.get("kind")
    if kind not in _ASK_VALID_KINDS:
        kind = "error"
    return {
        "mode": parsed.get("mode"),
        "kind": kind,
        "answer": parsed.get("answer") or "(no answer text)",
        "citations": parsed.get("citations") or [],
        "next_step": parsed.get("next_step") or "",
    }


# ---- live dashboard (George, 2026-10-06: "it shouldn't show old stuff") -----------------------------------
# The Status dashboard used to read August fixtures captured against one suite. This runs the same read-only,
# deterministic CLIs (`cases`, `runs`, `export-automation`, `build-stats`) against the target's CURRENT mapped
# suite and caches the result for a few minutes so every visit/refresh is real, never an old snapshot.
_LIVE_DIR = Path(os.environ.get("TESTOPS_WEBAPP_DATA_DIR") or (Path(__file__).resolve().parent / "data")) / "live"


def _cli(args: list[str], timeout: int = 180) -> tuple[int, str]:
    try:
        r = subprocess.run([str(_VENV_PYTHON), "-m", "system_test_ops", *args], cwd=str(SYSTEM_TEST_OPS_ROOT),
                           capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace",
                           env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    except subprocess.TimeoutExpired:
        return 124, f"Timed out after {timeout}s: {' '.join(args[:2])}"
    except OSError as exc:
        return 1, str(exc)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _testrail_reachable(timeout: float = 4.0) -> tuple[bool, str]:
    """Quick TCP probe of the TestRail host so an unreachable network fails in seconds, not after the CLI's 180s timeout."""
    import socket
    from urllib.parse import urlparse
    url = os.environ.get("TESTRAIL_URL", "")
    if not url:
        env = SYSTEM_TEST_OPS_ROOT / ".env"
        try:
            for line in env.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.startswith("TESTRAIL_URL="):
                    url = line.split("=", 1)[1].strip().strip('"')
        except OSError:
            pass
    u = urlparse(url if "//" in url else "//" + url)
    if not u.hostname:
        return True, ""  # unknown host: let the CLI report its own error
    try:
        with socket.create_connection((u.hostname, u.port or (443 if u.scheme == "https" else 80)), timeout=timeout):
            return True, ""
    except OSError:
        return False, f"TestRail ({u.hostname}) is not reachable from this machine (VPN / network?)."


def live_dashboard(project: str, device: str, max_age_s: int = 300, force: bool = False) -> dict:
    suite_id = store.get_new_suite_id(project, device)
    if suite_id is None:
        return {"available": False, "reason": f"No suite is mapped for {project}/{device} yet. Add one with Change target."}
    tr_pid = store.get_new_testrail_project_id(project, device) or store.get_testrail_project_id(project, device)
    if tr_pid is None:
        return {"available": False, "reason": f"No TestRail project id is set for {project}/{device}."}
    slug = re.sub(r"[^a-z0-9]+", "-", f"{project}-{device}-{suite_id}".lower()).strip("-")
    out = _LIVE_DIR / slug
    out.mkdir(parents=True, exist_ok=True)
    cache = out / "dashboard.json"
    if cache.is_file() and not force:
        try:
            cached = json.loads(cache.read_text(encoding="utf-8"))
            if time.time() - cached.get("_generated_epoch", 0) < max_age_s:
                return cached
        except (OSError, ValueError):
            pass
    ok, why = _testrail_reachable()
    if not ok:
        if cache.is_file():
            try:
                stale = json.loads(cache.read_text(encoding="utf-8"))
                stale["stale_note"] = f"{why} Showing the last pull from {stale.get('generated_at', 'earlier')}."
                return stale
            except (OSError, ValueError):
                pass
        return {"available": False, "reason": why}
    common = ["--project", str(tr_pid), "--suite", str(suite_id), "--out", str(out)]
    rc, msg = _cli(["cases", *common])
    if rc != 0 or not (out / "cases.json").is_file():
        return {"available": False, "reason": "Could not read the suite from TestRail: " + (msg.strip().splitlines()[-1] if msg.strip() else "no output")}
    rc_b, _ = _cli(["export-automation", *common])
    rc_r, _ = _cli(["runs", *common, "--last", "10"])
    bs_args = ["build-stats", "--cases", str(out / "cases.json"), "--snapshot-path", str(out / "_snapshot.json"), "--out", str(out)]
    if rc_b == 0 and (out / "automation-backlog.json").is_file():
        bs_args += ["--backlog", str(out / "automation-backlog.json")]
    if rc_r == 0 and (out / "run-health.json").is_file():
        bs_args += ["--run-health", str(out / "run-health.json")]
    rc_s, msg_s = _cli(bs_args)
    stats_path = out / "build-stats.json"
    if rc_s != 0 or not stats_path.is_file():
        return {"available": False, "reason": "Could not build the stats: " + (msg_s.strip().splitlines()[-1] if msg_s.strip() else "no output")}
    stats = json.loads(stats_path.read_text(encoding="utf-8"))
    run_health = None
    rh_path = out / "run-health.json"
    if rc_r == 0 and rh_path.is_file():
        data = json.loads(rh_path.read_text(encoding="utf-8"))
        cases = data.get("cases", [])
        flag_names = ("always_failing", "never_executed", "flaky", "recently_regressed", "orphaned")
        flagged = sorted([c for c in cases if any(c.get(f) for f in flag_names)],
                         key=lambda c: (c.get("failed", 0), c.get("executed_count", 0)), reverse=True)
        run_health = {"suite": data.get("suite"), "project": data.get("project"), "runs_considered": len(data.get("run_ids", [])),
                      "cases_total": len(cases), "flagged_total": len(flagged),
                      "counts": {f: sum(1 for c in cases if c.get(f)) for f in flag_names}, "shown": flagged[:15],
                      "total_passed": sum(int(c.get("passed") or 0) for c in cases), "total_failed": sum(int(c.get("failed") or 0) for c in cases),
                      "run_ids": data.get("run_ids") or []}
    result = {"available": True, "build_stats": stats, "run_health": run_health, "suite_id": suite_id,
              "generated_at": _now(), "_generated_epoch": time.time()}
    cache.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
    return result
