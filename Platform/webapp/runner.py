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
import re
import shlex
import subprocess
import sys
import threading
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

_CLI_TIMEOUT = 180
# 180s was fine for a one-file summarise (audit.yaml's "summarise" step) but nowhere near
# enough for a step that reads and carefully cites multiple real source documents (found
# live: ingest-docs' distil timed out reading 10 real PDFs). Generous ceiling for real work;
# a genuinely hung agent still gets caught, just later.
_AGENT_TIMEOUT = 900

_cancel_events: dict[str, threading.Event] = {}
_run_procs: dict[str, subprocess.Popen] = {}
_procs_lock = threading.Lock()

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


_OPTIONAL_FLAG_RE = re.compile(r"\[(--[\w-]+)\]")


def _resolve_optional_flags(command: str, params: dict) -> str:
    """A YAML command like `export-automation --suite {suite_id} [--include-manual]` uses
    `[--flag]` as documentation shorthand for "pass this only if the matching run input is
    truthy" — not something a real subprocess argv should ever see literally. Resolves
    `[--include-manual]` -> `--include-manual` if params['include_manual'] is truthy
    (from a declared pipeline input, e.g. export-automation.yaml's), else strips it
    entirely, generically for any `[--flag-name]` token."""
    def repl(match: re.Match) -> str:
        flag = match.group(1)
        key = flag.lstrip("-").replace("-", "_")
        value = params.get(key)
        truthy = value is not None and str(value).strip().lower() in ("1", "true", "yes")
        return flag if truthy else ""
    resolved = _OPTIONAL_FLAG_RE.sub(repl, command)
    return re.sub(r"\s{2,}", " ", resolved).strip()


_AREA_PREFIX_RE = re.compile(r"^(fs\d+|hmi\d+|is\d+|ss\d+)-", re.IGNORECASE)


def _slugify_area(spec_stem: str) -> str:
    """A spec filename like `fs002-cloudfare-communication` -> `cloudfare-communication` —
    strips the doc-numbering prefix these filenames use (fs002-/hmi01-/is001-/ss003-,
    per the real system-test-ops naming convention), keeping the human-meaningful part."""
    return _AREA_PREFIX_RE.sub("", spec_stem)


def _functional_areas(project: str) -> list[str]:
    """One functional area per ingested spec file for this project — generic, not
    NJT-hardcoded: any project with knowledge/{project}/specs/*.md (via ingest-docs) gets
    this fan-out. Empty if that folder doesn't exist yet (ingest-docs hasn't run) —
    callers must fail loudly on empty, never silently produce zero sub-steps."""
    specs_dir = SYSTEM_TEST_OPS_ROOT / "knowledge" / project.lower() / "specs"
    if not specs_dir.is_dir():
        return []
    return [_slugify_area(f.stem) for f in sorted(specs_dir.glob("*.md"))]


def step_area(step_id: str) -> str | None:
    """Extracts the area slug from a fanned-out step id like `author_area[fare-structure]`
    -> `fare-structure`; None for a step that was never fanned out."""
    if step_id.endswith("]") and "[" in step_id:
        return step_id[step_id.rindex("[") + 1:-1]
    return None


def _flatten_steps(pipeline: Pipeline, project: str, _seen: frozenset[str] = frozenset()) -> list[Step]:
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
    out: list[Step] = []
    for step in pipeline.steps:
        if step.is_composite_ref:
            nested_pipeline = load_pipeline(step.ref)
            for nested in _flatten_steps(nested_pipeline, project, seen):
                out.append(nested.model_copy(update={"id": f"{step.id}.{nested.id}"}))
        elif getattr(step, "loop", None):
            areas = _functional_areas(project)
            if not areas:
                out.append(step)  # loop stays set -> _dispatch_step fails it with a clear message
            else:
                for area in areas:
                    out.append(step.model_copy(update={"id": f"{step.id}[{area}]", "loop": None}))
        else:
            out.append(step)
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


def _build_params(project: str, device: str, steps: list[Step], extra_inputs: dict[str, str] | None = None) -> dict:
    # extra_inputs first, so a pipeline's own declared inputs (e.g. ingest-docs' docs_path)
    # can never clobber the system-derived project/device/suite id params assigned below.
    params: dict = dict(extra_inputs or {})
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
    return params


def _run_subprocess(cmd: list[str], cwd: str, timeout: int, run_id: str | None = None):
    """The one place an actual subprocess gets spawned — using Popen (not subprocess.run)
    so an in-flight process is reachable by `cancel_run` via `_run_procs`. Returns
    (returncode, stdout, stderr); raises TimeoutExpired/OSError like subprocess.run would."""
    proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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


def _run_cli_step(run_id: str, step: Step, command: str) -> str:
    parts = _split_command(command)
    if parts and parts[0] == "python":
        parts[0] = str(_VENV_PYTHON)
    try:
        returncode, stdout, stderr = _run_subprocess(parts, cwd=str(_step_cwd(step)), timeout=_CLI_TIMEOUT, run_id=run_id)
    except subprocess.TimeoutExpired:
        store.update_step(run_id, step.id, status="failed", output=f"Timed out after {_CLI_TIMEOUT}s.", finished_at=_now())
        return "failed"
    except OSError as exc:
        store.update_step(run_id, step.id, status="failed", output=f"Could not start: {exc}", finished_at=_now())
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
    if not ok:
        return "failed"

    match = re.search(r"-> (\S.*)$", stdout or "", re.MULTILINE)
    if match:
        store.update_run(run_id, report_path=match.group(1).strip(), cli_output=output)
    else:
        store.update_run(run_id, cli_output=output)
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
        return "failed"
    output = (stdout or "") + (("\n--- stderr ---\n" + stderr) if stderr else "")
    ok = returncode == 0
    store.update_step(run_id, step.id, status="succeeded" if ok else "failed", output=output, finished_at=_now())
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
        produces_area = step.produces.replace("<area>", area) if isinstance(step.produces, str) else f"{area}.cases.yaml"
        prompt = (
            f"For the '{area}' functional area only, carry out the '{step.id.split('[')[0]}' step "
            f"of this pipeline ({step.note or 'see pipeline definition'}). Ground everything in "
            f"knowledge/{{project}}/specs/ for this area — never invent case content. Produce: {produces_area}."
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
            prompt = step.note or f"Carry out the '{step.id}' step of this pipeline."

    try:
        returncode, stdout, stderr = _run_subprocess(
            [
                "claude", "-p", prompt,
                "--allowedTools", allowed_tools,
                "--permission-prompts", "none",
                "--output-format", "text",
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
        return "failed"
    except OSError as exc:
        store.update_step(run_id, step.id, status="failed", output=f"Could not run agent: {exc}", finished_at=_now())
        return "failed"

    output = (stdout or "").strip() or "(the agent returned no output)"
    ok = returncode == 0
    store.update_step(run_id, step.id, status="succeeded" if ok else "failed", output=output, finished_at=_now())
    if ok:
        store.update_run(run_id, summary=output)
        return "succeeded"
    return "failed"


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
    command = _render(step.command, params) if step.command else None
    if command and area:
        command = command.replace("<area>", area)  # e.g. push --file <area>.cases.yaml --commit
    if command:
        command = _resolve_optional_flags(command, params)  # e.g. [--include-manual]
    forced_human = bool(command) and (
        ("push" in command and "--commit" in command)  # a real TestRail push --commit
        or "git push" in command  # a real push to a repo remote (e.g. test-automation-sit)
    )

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
    steps = _flatten_steps(pipeline, project)
    extra_inputs = _run_extra_inputs.get(run_id, {})
    try:
        params = _build_params(project, device, steps, extra_inputs)
    except ValueError as exc:
        store.update_run(run_id, status="failed", error=str(exc))
        return

    context = {"fresh_build": _is_fresh_build(project, device)}
    cancel_event = _cancel_events.setdefault(run_id, threading.Event())

    for idx in range(start_index, len(steps)):
        if cancel_event.is_set():
            store.update_run(run_id, status="failed", error="Run cancelled.")
            return
        step = steps[idx]
        outcome = _dispatch_step(run_id, step, params, context)
        if outcome == "waiting_human":
            store.update_run(run_id, status="waiting_human")
            return
        if outcome == "failed":
            store.update_run(run_id, status="failed", error=f"Step '{step.id}' failed.")
            return
        # succeeded / skipped -> keep going

    store.update_run(run_id, status="succeeded")


def start_run(pipeline_id: str, project: str, device: str, extra_inputs: dict[str, str] | None = None) -> str:
    """Kicks off a real run of ANY pipeline in the background, returns a run id to poll.
    `extra_inputs` covers whatever a pipeline declares beyond project/device/suite ids
    (e.g. ingest-docs' docs_path) — app.py validates required ones are present before
    calling this, using the pipeline's own `inputs:` list as the source of truth.
    Raises KeyError for an unknown pipeline id, ValueError if a required suite id isn't
    configured for this target — both map to HTTP 404/400 in app.py."""
    pipeline = load_pipeline(pipeline_id)
    steps = _flatten_steps(pipeline, project)
    extra_inputs = extra_inputs or {}
    _build_params(project, device, steps, extra_inputs)  # validate up front — don't create a run row if this will fail immediately

    run_id = str(uuid.uuid4())
    _run_extra_inputs[run_id] = extra_inputs
    store.create_run(run_id, pipeline_id, project, device)
    store.create_step_rows(run_id, [(s.id, s.kind.value if s.kind else None) for s in steps])
    _cancel_events[run_id] = threading.Event()

    thread = threading.Thread(target=_run_pipeline_job, args=(run_id, pipeline_id, project, device, 0), daemon=True)
    thread.start()
    return run_id


def start_audit_run(project: str, device: str) -> str:
    """Kept for existing callers — audit is now just start_run("audit", ...) going through
    the same generic engine as everything else (the explicit regression-check case)."""
    return start_run("audit", project, device)


class TargetNotApprovedError(RuntimeError):
    """Raised by resolve_step when a push+--commit gate is resolved for a target that has
    no persisted sign-off (store.is_target_approved) — independent of, and in addition to,
    the per-run human gate every push step already goes through. app.py maps this to 403."""


def _step_command(run_id: str, run: dict, step_id: str) -> str | None:
    """Re-derives a flattened step's rendered command, the same way _dispatch_step would
    have — needed here because pipeline_run_steps only stores the step's *output* summary,
    not its original templated command."""
    pipeline = load_pipeline(run["pipeline_id"])
    steps = _flatten_steps(pipeline, run["project"])
    step = next((s for s in steps if s.id == step_id), None)
    if step is not None:
        area = step_area(step_id)
        if area and step.command:
            step = step.model_copy(update={"command": step.command.replace("<area>", area)})
    if step is None or not step.command:
        return None
    extra_inputs = _run_extra_inputs.get(run_id, {})
    params = _build_params(run["project"], run["device"], steps, extra_inputs)
    return _resolve_optional_flags(_render(step.command, params), params)


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

    command = _step_command(run_id, run, step_id)
    is_push_gate = bool(command) and "push" in command and "--commit" in command
    if is_push_gate and not store.is_target_approved(run["project"], run["device"]):
        # Refused, but retryable: leave the step at waiting_human (not failed) so approving
        # the target and clicking "Approve & Push" again just works, rather than requiring
        # the whole run to be restarted from scratch.
        store.update_step(
            run_id, step_id, status="waiting_human",
            output=f"Refused: {run['project']}/{run['device']} has no persisted approval yet — "
                   "approve this target, then retry Approve & Push.",
        )
        raise TargetNotApprovedError(f"{run['project']}/{run['device']} is not approved.")

    store.update_step(run_id, step_id, status="succeeded", finished_at=_now())
    store.update_run(run_id, status="running")
    _cancel_events[run_id] = threading.Event()

    idx = ids_in_order.index(step_id)
    thread = threading.Thread(
        target=_run_pipeline_job,
        args=(run_id, run["pipeline_id"], run["project"], run["device"], idx + 1),
        daemon=True,
    )
    thread.start()


def cancel_run(run_id: str) -> None:
    """Best-effort: sets a flag the run loop checks between steps, and terminates an
    in-flight subprocess if one is running right now. In-memory only (`_cancel_events`/
    `_run_procs`) — doesn't survive a process restart, which is fine for a single-user
    local app; a run left `running` across a restart just won't ever cancel cleanly, it'll
    sit there until manually marked failed (a real gap, acceptable for now)."""
    event = _cancel_events.setdefault(run_id, threading.Event())
    event.set()
    with _procs_lock:
        proc = _run_procs.get(run_id)
    if proc is not None and proc.poll() is None:
        try:
            proc.terminate()
        except OSError:
            pass


def _case_count(suite_id: int) -> int | None:
    """Real, live case count for one suite via `system_test_ops cases` (read-only — that
    command only ever reads TestRail and writes local report files). Parses the CLI's own
    "Wrote N cases ->" line rather than re-implementing the TestRail call here."""
    try:
        result = subprocess.run(
            [str(_VENV_PYTHON), "-m", "system_test_ops", "cases", "--suite", str(suite_id)],
            cwd=str(SYSTEM_TEST_OPS_ROOT), capture_output=True, text=True, timeout=60,
        )
    except (subprocess.TimeoutExpired, OSError):
        return None
    match = re.search(r"Wrote (\d+) cases", result.stdout)
    return int(match.group(1)) if match else None


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


def compare_suite_case_counts(project: str, device: str) -> dict:
    """Real old-vs-new case counts for a target, live from TestRail (two read-only CLI
    calls) -- suggested in ISSUES.md, buildable now that credentials + both suite ids
    (old_suite_id added 2026-09-09) exist for the seeded Translink pairs."""
    ids = store.get_suite_ids(project, device)
    if not ids or ids["old_suite_id"] is None or ids["new_suite_id"] is None:
        return {"available": False, "reason": "old_suite_id and/or new_suite_id not configured for this target."}
    old_count = _case_count(ids["old_suite_id"])
    new_count = _case_count(ids["new_suite_id"])
    if old_count is None or new_count is None:
        return {"available": False, "reason": "Could not pull live case counts (check TestRail credentials/connectivity)."}
    return {
        "available": True,
        "old_suite_id": ids["old_suite_id"], "new_suite_id": ids["new_suite_id"],
        "old_case_count": old_count, "new_case_count": new_count,
        "diff": new_count - old_count,
    }
