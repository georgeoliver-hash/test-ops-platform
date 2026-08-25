"""Command-line entry point for the deterministic core.

Produces reproducible JSON baselines (+ a markdown eyeball) that the Claude
agents consume. Read-only: nothing here mutates TestRail.

    python -m system_test_ops check
    python -m system_test_ops cases --project translink --suite POS
    python -m system_test_ops runs  --project translink --suite POS --last 10
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from system_test_ops import audit as audit_mod
from system_test_ops import doctor as doctor_mod
from system_test_ops.coverage.normalise import build_cases_baseline
from system_test_ops.reporting.jira import render_run_health_jira
from system_test_ops.reporting.markdown import render_cases_baseline, render_run_health
from system_test_ops.runs.history import build_run_health
from system_test_ops.testrail.client import (
    TestRailClient,
    TestRailConfigError,
    TestRailError,
)
from system_test_ops.testrail.writer import (
    TestRailWriter,
    TestRailWriteError,
    load_write_suite_id,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = REPO_ROOT / "reports"


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-") or "x"


def _resolve_project(client: TestRailClient, value: str | None) -> tuple[int, str]:
    if not value:
        env_id = os.environ.get("TESTRAIL_PROJECT_ID")
        if env_id:
            value = env_id
        else:
            raise SystemExit("error: --project is required (id or name), or set TESTRAIL_PROJECT_ID")
    projects = client.get_projects()
    if str(value).isdigit():
        pid = int(value)
        match = next((p for p in projects if int(p["id"]) == pid), None)
        return pid, (match.get("name") if match else str(value))
    match = next((p for p in projects if p.get("name", "").lower() == value.lower()), None)
    if not match:
        names = ", ".join(p.get("name", "?") for p in projects) or "(none)"
        raise SystemExit(f"error: project '{value}' not found. Available: {names}")
    return int(match["id"]), match["name"]


def _resolve_suite(client: TestRailClient, project_id: int, value: str | None) -> tuple[int | None, str]:
    suites = client.get_suites(project_id)
    if value is None:
        # Single-suite project: TestRail still returns one suite; use it implicitly.
        if len(suites) == 1:
            return int(suites[0]["id"]), suites[0].get("name", "suite")
        return None, "all-suites"
    if str(value).isdigit():
        sid = int(value)
        match = next((s for s in suites if int(s["id"]) == sid), None)
        return sid, (match.get("name") if match else str(value))
    match = next((s for s in suites if s.get("name", "").lower() == value.lower()), None)
    if not match:
        names = ", ".join(s.get("name", "?") for s in suites) or "(none)"
        raise SystemExit(f"error: suite '{value}' not found in project. Available: {names}")
    return int(match["id"]), match["name"]


def _write(out_dir: Path, name: str, content: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / name
    path.write_text(content, encoding="utf-8")
    return path


def _out_dir(project_name: str, suite_name: str, override: str | None) -> Path:
    if override:
        return Path(override)
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return REPORTS_DIR / _slug(project_name) / _slug(suite_name) / date


# --------------------------------------------------------------------------- #
# subcommands
# --------------------------------------------------------------------------- #
def cmd_check(args: argparse.Namespace) -> int:
    client = TestRailClient()
    projects = client.get_projects()
    print(f"OK — connected to TestRail. {len(projects)} project(s) visible:")
    for p in projects:
        print(f"  [{p['id']}] {p.get('name')}")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    """Readiness preflight: environment, credentials, connectivity. Read-only.

    Informational by default (exit 0). With --gate, exits non-zero when a
    human-action item is still outstanding.
    """
    checks = doctor_mod.run_checks()
    print(doctor_mod.render(checks))
    if args.gate and doctor_mod.has_blockers(checks):
        return 1
    return 0


def cmd_cases(args: argparse.Namespace) -> int:
    client = TestRailClient()
    project_id, project_name = _resolve_project(client, args.project)
    suite_id, suite_name = _resolve_suite(client, project_id, args.suite)
    baseline = build_cases_baseline(
        client,
        project=project_name,
        project_id=project_id,
        suite_id=suite_id,
        suite_name=suite_name,
    )
    out_dir = _out_dir(project_name, suite_name, args.out)
    json_path = _write(out_dir, "cases.json", baseline.model_dump_json(indent=2))
    md_path = _write(out_dir, "cases.md", render_cases_baseline(baseline))
    print(f"Wrote {len(baseline.cases)} cases ->")
    print(f"  {json_path}")
    print(f"  {md_path}")
    return 0


def cmd_runs(args: argparse.Namespace) -> int:
    client = TestRailClient()
    project_id, project_name = _resolve_project(client, args.project)
    suite_id, suite_name = _resolve_suite(client, project_id, args.suite)
    report = build_run_health(
        client,
        project=project_name,
        project_id=project_id,
        suite_id=suite_id,
        suite_name=suite_name,
        last_n=args.last,
    )
    out_dir = _out_dir(project_name, suite_name, args.out)
    json_path = _write(out_dir, "run-health.json", report.model_dump_json(indent=2))
    md_path = _write(out_dir, "run-health.md", render_run_health(report))
    jira_path = _write(out_dir, "run-health.jira.txt", render_run_health_jira(report))
    print(f"Analysed {len(report.run_ids)} run(s), {len(report.cases)} case(s) ->")
    print(f"  {json_path}")
    print(f"  {md_path}")
    print(f"  {jira_path}")
    return 0


_KW = re.compile(r"\*\*(GIVEN|WHEN|THEN|AND)\*\*", re.I)


def _gherkin_to_fields(gherkin: str) -> tuple[str, list[dict], str]:
    """Map a **GIVEN/AND/WHEN/THEN** block into (preconds, steps_separated, expected).

    Mirrors how this project's template-1 cases are structured:
      * leading GIVEN/AND  -> custom_preconds
      * each WHEN(+AND)/THEN(+AND) pair -> a custom_steps_seperated row {content, expected}
      * all THEN/then-side AND lines -> custom_expected
    """
    lines = [ln.strip() for ln in gherkin.splitlines() if ln.strip()]
    preconds: list[str] = []
    steps: list[dict[str, list[str]]] = []
    expected: list[str] = []
    section = "given"
    cur: dict[str, list[str]] | None = None
    last = None
    for ln in lines:
        m = _KW.match(ln)
        kw = m.group(1).upper() if m else None
        if kw == "GIVEN" or (kw == "AND" and last == "GIVEN" and section == "given"):
            preconds.append(ln)
            last = "GIVEN"
            continue
        if kw == "WHEN":
            section = "steps"
            cur = {"content": [ln], "expected": []}
            steps.append(cur)
            last = "WHEN"
            continue
        if kw == "THEN":
            section = "steps"
            if cur is None:
                cur = {"content": [], "expected": [ln]}
                steps.append(cur)
            else:
                cur["expected"].append(ln)
            expected.append(ln)
            last = "THEN"
            continue
        if kw == "AND" and cur is not None:
            (cur["content"] if last == "WHEN" else cur["expected"]).append(ln)
            if last == "THEN":
                expected.append(ln)
            continue
        # continuation / non-keyword line: attach to the current bucket
        if section == "given":
            preconds.append(ln)
        elif cur is not None:
            (cur["expected"] if last == "THEN" else cur["content"]).append(ln)
    sep = [
        {"content": "\n".join(s["content"]), "expected": "\n".join(s["expected"])}
        for s in steps
        if "".join(s["content"]).strip()
    ]
    return "\n".join(preconds), sep, "\n".join(expected)


def cmd_push(args: argparse.Namespace) -> int:
    import yaml

    spec = yaml.safe_load(Path(args.file).read_text(encoding="utf-8")) or {}
    defaults = spec.get("defaults") or {}
    client = TestRailClient()
    project_arg = args.project or (str(spec["project_id"]) if spec.get("project_id") else None)
    project_id, project_name = _resolve_project(client, project_arg)

    write_suite = load_write_suite_id()
    if write_suite is None:
        raise SystemExit(
            "error: TESTRAIL_WRITE_SUITE_ID is not set. Writes are disabled until you point it at "
            "the NEW suite id. Refusing to push."
        )
    spec_suite = spec.get("suite_id")
    if spec_suite is not None and int(spec_suite) != write_suite:
        raise SystemExit(
            f"error: spec suite_id {spec_suite} does not match TESTRAIL_WRITE_SUITE_ID {write_suite}. "
            "Refusing to push to the wrong suite."
        )

    if args.commit and not args.allow_active_runs:
        active_runs = client.get_active_runs_for_suite(project_id, write_suite)
        if active_runs:
            lines = "\n".join(f"  - run {r['id']}: {r.get('name', '(unnamed)')}" for r in active_runs)
            raise SystemExit(
                f"error: suite {write_suite} has {len(active_runs)} run(s) still in progress:\n{lines}\n"
                "Editing cases while a run is live can desync that run's results from what a tester "
                "is looking at right now. Confirm this is safe, then re-run with --allow-active-runs "
                "to proceed anyway."
            )

    writer = TestRailWriter(client, project_id, write_suite, commit=args.commit)
    mode = "COMMIT" if args.commit else "DRY-RUN"
    print(f"[{mode}] push -> project '{project_name}' (id {project_id}), write suite_id {write_suite}")
    n_sec = n_case = 0
    attach_supported = True
    for section in spec.get("sections", []):
        path = section.get("path")
        if isinstance(path, str):
            path = [p.strip() for p in path.split("/")]
        leaf = writer.find_or_create_section_path(path)
        print(f"  section: {' / '.join(path)}  -> {('id ' + str(leaf)) if leaf else '(would create)'}")
        n_sec += 1
        for case in section.get("cases", []):
            preconds, sep, then_text = _gherkin_to_fields(case.get("steps", ""))
            objective = case.get("objective") or f"This test is to confirm: {case['title']}"
            if case.get("overflow"):
                objective = objective + "\n\nDesign reference (Overflow): " + case["overflow"]
            if case.get("attach"):
                objective = objective + "\nScreen image (repo): " + case["attach"]
            # Expected = a short prose summary; fall back to the THEN lines if none authored.
            expected = case.get("expected") or then_text
            fields = dict(defaults)
            fields.update(
                {
                    "custom_preface": objective,
                    "custom_preconds": preconds,
                    "custom_steps_seperated": sep,
                    "custom_expected": expected,
                }
            )
            title = case["title"]
            # `match` lets us find an existing case by its OLD title while setting a new (shorter) one.
            match_title = case.get("match") or title
            exists = match_title.strip().lower() in writer.existing_by_title
            if exists and args.update:
                case_id = (writer.existing_by_title.get(match_title.strip().lower()) or {}).get("id")
                res = writer.update_case(match_title, new_title=title, refs=case.get("refs"), extra=fields)
                label = "(would update)" if res.get("_dry_run") else "(updated)"
            else:
                res = writer.add_case(leaf, title, refs=case.get("refs"), extra=fields)
                case_id = res.get("id")
                label = "(exists, skipped)" if res.get("skipped") else (f"-> C{case_id}" if case_id else "(dry-run)")
            # Attach a local image on a fresh create — non-fatal if this TestRail lacks the API.
            if case.get("attach") and case_id and not res.get("skipped") and attach_supported:
                path = case["attach"]
                if not Path(path).is_absolute():
                    path = str(REPO_ROOT / path)
                try:
                    writer.add_attachment(int(case_id), path)
                    label += " +img"
                except (TestRailWriteError, OSError) as exc:
                    # OSError covers a missing local image file; TestRailWriteError covers a
                    # TestRail that lacks the attachment API (404). Either way it is non-fatal —
                    # the Overflow link + image filename already live in the case preface.
                    attach_supported = False
                    print(f"      note: image attachments unavailable ({exc}). "
                          "Continuing with the Overflow link + image filename in each case.")
            print(f"      case: {title[:60]}  {label}")
            n_case += 1
    print(f"[{mode}] {n_sec} section(s), {n_case} case(s) processed.")
    if not args.commit:
        print("Dry-run only — nothing written. Re-run with --commit to create them in the new suite.")
        return 0
    # After a real write, ALWAYS audit the target suite so no authoring happens without a
    # conformance read-out. Opt out only with --no-audit.
    if not getattr(args, "no_audit", False):
        print("\n--- standard-conformance audit (target suite) ---")
        _run_suite_audit(client, project_id, project_name, write_suite, out_override=None, gate=False)
    return 0


def _run_suite_audit(client, project_id, project_name, suite_id, out_override, gate):
    """Audit a suite, print the per-rule summary, write the report. Returns blocking count."""
    suite_name = next(
        (s.get("name", "suite") for s in client.get_suites(project_id) if int(s["id"]) == int(suite_id)),
        "suite",
    )
    cases = client.get_cases(project_id, suite_id)
    counted = [c for c in cases if not str(c.get("title", "")).startswith(audit_mod.SKIP_TITLE_PREFIX)]
    findings = audit_mod.audit_cases(cases)
    blocking, advisory = audit_mod.summarize(findings)
    for key, desc in audit_mod.ORDER:
        n = len(findings.get(key, []))
        tag = " (advisory)" if key in audit_mod.ADVISORY else ""
        flag = "  " if n == 0 or key in audit_mod.ADVISORY else "!!"
        print(f"  {flag} {n:4d}  {key}{tag}")
    out_dir = _out_dir(project_name, suite_name, out_override)
    report_path = _write(out_dir, "alignment-audit.md",
                         audit_mod.render_report(int(suite_id), len(counted), findings))
    verdict = "CLEAN" if blocking == 0 else f"{blocking} BLOCKING finding(s) — fix before opening a PR"
    print(f"  audited {len(counted)} cases: {verdict}; {advisory} advisory. Report -> {report_path}")
    return blocking


def cmd_audit(args: argparse.Namespace) -> int:
    client = TestRailClient()
    project_id, project_name = _resolve_project(client, args.project)
    suite_value = args.suite if args.suite is not None else os.environ.get("TESTRAIL_WRITE_SUITE_ID")
    suite_id, _ = _resolve_suite(client, project_id, suite_value)
    if suite_id is None:
        raise SystemExit("error: --suite is required (or set TESTRAIL_WRITE_SUITE_ID).")
    blocking = _run_suite_audit(client, project_id, project_name, suite_id, args.out, gate=not args.no_gate)
    return 1 if (blocking and not args.no_gate) else 0


_FIELD_TYPES = {1: "String", 2: "Integer", 3: "Text", 4: "URL", 5: "Checkbox", 6: "Dropdown",
                7: "User", 8: "Date", 9: "Milestone", 10: "Steps", 11: "Steps(sep)", 12: "Multi-select"}


def cmd_discover_fields(args: argparse.Namespace) -> int:
    """Inspect a project's case fields (+ optional sample case) and suggest a push `defaults:` block.

    Run this FIRST for any new project so the `defaults` (template_id + required custom fields) are
    correct — these differ per project/template.
    """
    client = TestRailClient()
    project_id, project_name = _resolve_project(client, args.project)
    fields = client.get_case_fields()
    print(f"Case fields for project '{project_name}' (id {project_id}):\n")
    required = []
    for f in fields:
        sn = f.get("system_name", "?")
        cfgs = f.get("configs") or []
        is_req = any((cfg.get("options") or {}).get("is_required") for cfg in cfgs)
        items = ""
        for cfg in cfgs:
            opts = cfg.get("options") or {}
            if opts.get("items"):
                items = " | options: " + str(opts["items"]).replace("\n", " ")[:120]
        flag = "REQUIRED" if is_req else "        "
        print(f"  {flag}  {sn:26} {_FIELD_TYPES.get(f.get('type_id'), f.get('type_id'))}{items}")
        if is_req:
            required.append(sn)

    print("\nSuggested `defaults:` block for the push YAML:")
    if args.sample_case:
        case = client.get_case(int(args.sample_case))
        print(f"  # mirrored from sample case C{args.sample_case} (template_id {case.get('template_id')})")
        print("defaults:")
        print(f"  template_id: {case.get('template_id')}")
        for sn in sorted(set(required) | {"custom_devtypes", "custom_autoconfirmation"}):
            if sn in case and case[sn] not in (None, "", []):
                print(f"  {sn}: {json.dumps(case[sn])}")
        print("\n  # NOTE: confirm the Steps field name (custom_steps vs custom_steps_seperated) from the sample,")
        print("  # and that the Gherkin maps into preconds/steps/expected as in docs/gherkin-standard.md.")
    else:
        print("  # (pass --sample-case <id> from an existing case in this project to fill real values)")
        print("defaults:")
        print("  template_id: <from a sample case>")
        for sn in required:
            print(f"  {sn}: <required — set a sensible default>")
    return 0


# --------------------------------------------------------------------------- #
# export-automation: hand the automatable cases to the sibling automation-tests repo
# --------------------------------------------------------------------------- #
# Device id -> marker name (this TestRail instance / project 42). Falls back to devtype:<id>.
_DEVICE_BY_ID = {5: "POS", 25: "ETMS", 10: "PV", 11: "TVM", 12: "GV", 13: "BV", 14: "HHD"}
_PRIO_NAME = {1: "High", 2: "High", 3: "Normal", 4: "Low", 5: "Low", 6: "None"}
# The enrichment tag appended to Expected: "[Automatable: Yes|Partial|No · Cross-check: A / B]".
_AUTOMATABLE_TAG = re.compile(
    r"\[Automatable:\s*(Yes|Partial|No)\s*(?:[·|]\s*Cross-check:\s*([^\]]+))?\]", re.I)
# A case is destructive if it can lock out / take down the device (per the destructive-test policy).
_DESTRUCTIVE = re.compile(
    r"lock[ -]?out|locked out|device locked|locks the device|failed (pin|attempt)|"
    r"after the configured failed|cash limit|reboot|power interrupt|out of service|disable", re.I)


def _device_name(devtypes) -> str:
    if isinstance(devtypes, list) and devtypes:
        return _DEVICE_BY_ID.get(int(devtypes[0]), f"devtype:{devtypes[0]}")
    if devtypes not in (None, "", []):
        return _DEVICE_BY_ID.get(int(devtypes), f"devtype:{devtypes}")
    return "unknown"


def _parse_automatable(expected: str) -> tuple[str | None, list[str], str]:
    """Return (tier, cross_check_systems, expected_without_tag). tier is 'Yes'|'Partial'|'No'|None."""
    m = _AUTOMATABLE_TAG.search(expected or "")
    if not m:
        return None, [], (expected or "").strip()
    tier = m.group(1).title()
    systems = [s.strip() for s in re.split(r"[/,]", m.group(2) or "") if s.strip()]
    clean = _AUTOMATABLE_TAG.sub("", expected or "").strip()
    return tier, systems, clean


def cmd_export_automation(args: argparse.Namespace) -> int:
    """Export the automatable-marked cases as a backlog the automation-tests repo consumes.

    Read-only. Emits automation-backlog.json (machine-readable handoff) + .md (human view),
    ordered High->Normal->Low. Each entry carries the TestRail case id for traceability, the
    Gherkin, the device marker, the cross-check systems to verify, and a destructive flag.
    """
    client = TestRailClient()
    project_id, project_name = _resolve_project(client, args.project)
    suite_value = args.suite if args.suite is not None else os.environ.get("TESTRAIL_WRITE_SUITE_ID")
    suite_id, suite_name = _resolve_suite(client, project_id, suite_value)
    if suite_id is None:
        raise SystemExit("error: --suite is required (or set TESTRAIL_WRITE_SUITE_ID).")

    secs = {s["id"]: s for s in client.get_sections(project_id, suite_id)}

    def path(sid):
        parts, cur = [], secs.get(sid)
        while cur:
            parts.append(cur["name"])
            cur = secs.get(cur.get("parent_id"))
        return list(reversed(parts))

    cases = [c for c in client.get_cases(project_id, suite_id)
             if not str(c.get("title", "")).startswith(audit_mod.SKIP_TITLE_PREFIX)]

    entries, n_yes, n_partial, n_no, n_untagged, n_destructive = [], 0, 0, 0, 0, 0
    for c in cases:
        tier, systems, clean_expected = _parse_automatable(c.get("custom_expected") or "")
        if tier is None:
            n_untagged += 1
            continue
        t = tier.lower()
        if t == "yes":
            n_yes += 1
        elif t == "partial":
            n_partial += 1
        else:
            n_no += 1
            if not args.include_manual:
                continue
        sp = path(c["section_id"])
        blob = (c.get("title", "") + " " + (c.get("custom_preface") or "") + " "
                + " ".join((r.get("content", "") + " " + r.get("expected", ""))
                           for r in (c.get("custom_steps_seperated") or []) if isinstance(r, dict)))
        destructive = bool(_DESTRUCTIVE.search(blob))
        if destructive and t != "no":
            n_destructive += 1
        steps = [{"when": r.get("content", ""), "then": r.get("expected", "")}
                 for r in (c.get("custom_steps_seperated") or []) if isinstance(r, dict)]
        entries.append({
            "ref": f"C{c['id']}",
            "case_id": int(c["id"]),
            "title": c.get("title", ""),
            "section_path": sp,
            "feature": sp[-1] if sp else "",
            "device": _device_name(c.get("custom_devtypes")),
            "priority": _PRIO_NAME.get(c.get("priority_id"), "Normal"),
            "priority_id": c.get("priority_id"),
            "estimate": c.get("estimate"),
            "automation": t,
            "automatable": t != "no",
            "cross_check": systems,
            "destructive": destructive,
            "refs": c.get("refs") or "",
            "gherkin": {
                "given": c.get("custom_preconds") or "",
                "steps": steps,
                "expected": clean_expected,
            },
        })

    order = {1: 0, 2: 0, 3: 1, 4: 2, 5: 2, 6: 3}
    entries.sort(key=lambda e: (order.get(e["priority_id"], 1), e["section_path"], e["case_id"]))

    backlog = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "system-test-ops",
        "project": {"id": project_id, "name": project_name},
        "suite": {"id": suite_id, "name": suite_name,
                  "device": _device_name((cases[0].get("custom_devtypes") if cases else None))},
        "contract": {
            "traceability": "Reference `ref` (TestRail case id, e.g. C4099911) in each automated "
                            "test so a result maps back to its case.",
            "markers": "Mirror device + feature as pytest markers; add @pytest.mark.destructive "
                       "where destructive is true (deselected by default).",
            "cross_check": "cross_check lists the back-office systems the case asserts — the test "
                           "must verify the event landed there (CloudFare / MERIT / SmartTrack).",
            "note": "automatable/priority are system-test-ops judgements and a starting point; "
                    "the automation engineer may override with rationale.",
        },
        "counts": {"total_cases": len(cases), "automatable_full": n_yes,
                   "automatable_partial": n_partial, "manual_only": n_no,
                   "untagged": n_untagged, "destructive_in_backlog": n_destructive},
        "cases": entries,
    }

    out_dir = _out_dir(project_name, suite_name, args.out)
    json_path = _write(out_dir, "automation-backlog.json", json.dumps(backlog, indent=2, ensure_ascii=False))
    md_path = _write(out_dir, "automation-backlog.md", _render_automation_md(backlog))
    print(f"Automation backlog for '{suite_name}' (suite {suite_id}) of {len(cases)} cases: "
          f"{n_yes} full + {n_partial} partial automatable "
          f"({n_destructive} destructive, {n_no} manual-only, {n_untagged} untagged) ->")
    print(f"  {json_path}")
    print(f"  {md_path}")
    return 0


def _render_automation_md(backlog: dict) -> str:
    s = backlog["suite"]
    out = [f"# Automation backlog — {s['name']} ({s['device']})", "",
           f"_Generated {backlog['generated_utc']} by system-test-ops. "
           f"Suite id {s['id']}, project {backlog['project']['name']}._", "",
           f"**{backlog['counts']['automatable_full']} fully automatable + "
           f"{backlog['counts']['automatable_partial']} partial** of "
           f"{backlog['counts']['total_cases']} cases "
           f"({backlog['counts']['destructive_in_backlog']} destructive, "
           f"{backlog['counts']['manual_only']} manual-only). "
           f"_Partial = the UI flow is automatable but a step (card tap / print / cash) needs a "
           f"hardware fixture or human eye._", "",
           "## How to consume", "",
           f"- {backlog['contract']['traceability']}",
           f"- {backlog['contract']['markers']}",
           f"- {backlog['contract']['cross_check']}",
           f"- {backlog['contract']['note']}", ""]
    cur_prio = None
    for e in backlog["cases"]:
        if e["priority"] != cur_prio:
            cur_prio = e["priority"]
            out += ["", f"## Priority: {cur_prio}", ""]
        flags = [e["automation"].upper()] if e["automation"] == "partial" else []
        if e["destructive"]:
            flags.append("**DESTRUCTIVE**")
        if e["cross_check"]:
            flags.append("cross-check: " + " / ".join(e["cross_check"]))
        if e["refs"]:
            flags.append("refs: " + e["refs"])
        tail = ("  — " + "; ".join(flags)) if flags else ""
        out.append(f"### {e['ref']} · {e['title']}  ({e['estimate'] or '?'}){tail}")
        out.append(f"_{' / '.join(e['section_path'])}_")
        if e["gherkin"]["given"]:
            out.append("")
            out.append(e["gherkin"]["given"])
        for st in e["gherkin"]["steps"]:
            if st["when"]:
                out.append(st["when"])
            if st["then"]:
                out.append(st["then"])
        out.append("")
    return "\n".join(out) + "\n"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="system-test-ops", description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)

    c = sub.add_parser("check", help="Validate TestRail credentials and list visible projects.")
    c.set_defaults(func=cmd_check)

    c = sub.add_parser(
        "doctor",
        help="Readiness preflight (read-only): environment, credentials, connectivity. Prints a "
        "who-does-what punch-list. The engine behind /start.",
    )
    c.add_argument("--gate", action="store_true",
                   help="Exit non-zero if a human-action item is outstanding (for CI/pre-commit).")
    c.set_defaults(func=cmd_doctor)

    c = sub.add_parser(
        "discover-fields",
        help="Inspect a project's case fields and suggest the push `defaults:` block. Run first per project.",
    )
    c.add_argument("--project", help="Project id or name (or TESTRAIL_PROJECT_ID).")
    c.add_argument("--sample-case", help="An existing case id in this project, to mirror real field values.")
    c.set_defaults(func=cmd_discover_fields)

    c = sub.add_parser("cases", help="Export a suite's case inventory to cases.json.")
    c.add_argument("--project", help="TestRail project id or name (or set TESTRAIL_PROJECT_ID).")
    c.add_argument("--suite", help="TestRail suite id or name (optional for single-suite projects).")
    c.add_argument("--out", help="Override output directory.")
    c.set_defaults(func=cmd_cases)

    c = sub.add_parser("runs", help="Aggregate the last N runs into run-health.json.")
    c.add_argument("--project", help="TestRail project id or name (or set TESTRAIL_PROJECT_ID).")
    c.add_argument("--suite", help="TestRail suite id or name (optional for single-suite projects).")
    c.add_argument("--last", type=int, default=10, help="How many recent runs to consider (default 10).")
    c.add_argument("--out", help="Override output directory.")
    c.set_defaults(func=cmd_runs)

    c = sub.add_parser(
        "push",
        help="Create sections/cases in the NEW suite from a YAML spec. Dry-run unless --commit. "
        "Writes ONLY to TESTRAIL_WRITE_SUITE_ID.",
    )
    c.add_argument("--file", required=True, help="YAML spec of sections/cases to create.")
    c.add_argument("--project", help="Project id or name (or TESTRAIL_PROJECT_ID / spec project_id).")
    c.add_argument("--commit", action="store_true", help="Actually write to TestRail (default: dry-run).")
    c.add_argument("--update", action="store_true", help="Update existing cases (matched by title) instead of skipping.")
    c.add_argument("--no-audit", action="store_true", help="Skip the post-commit conformance audit (not recommended).")
    c.add_argument(
        "--allow-active-runs", action="store_true",
        help="Proceed even if the target suite has an in-progress run (default: refuse and list them).",
    )
    c.set_defaults(func=cmd_push)

    c = sub.add_parser(
        "export-automation",
        help="Export the automatable-marked cases as a backlog (JSON + MD) for the automation-tests repo.",
    )
    c.add_argument("--project", help="Project id or name (or TESTRAIL_PROJECT_ID).")
    c.add_argument("--suite", help="Suite id or name (or TESTRAIL_WRITE_SUITE_ID).")
    c.add_argument("--include-manual", action="store_true",
                   help="Also list cases marked Automatable: No (default: automatable only).")
    c.add_argument("--out", help="Override output directory.")
    c.set_defaults(func=cmd_export_automation)

    c = sub.add_parser(
        "audit",
        help="Lint a suite against the Gherkin standard (read-only). Defaults to TESTRAIL_WRITE_SUITE_ID. "
        "Exits non-zero if there are blocking findings (use --no-gate to always exit 0).",
    )
    c.add_argument("--project", help="Project id or name (or TESTRAIL_PROJECT_ID).")
    c.add_argument("--suite", help="Suite id or name (or TESTRAIL_WRITE_SUITE_ID).")
    c.add_argument("--out", help="Override report output directory.")
    c.add_argument("--no-gate", action="store_true", help="Always exit 0 even with blocking findings.")
    c.set_defaults(func=cmd_audit)

    return p


def main(argv: list[str] | None = None) -> int:
    # Windows consoles default to cp1252 and crash on em-dashes / special chars; make output safe.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except TestRailConfigError as exc:
        print(f"config error: {exc}", file=sys.stderr)
        return 2
    except TestRailWriteError as exc:
        print(f"write refused: {exc}", file=sys.stderr)
        return 3
    except TestRailError as exc:
        print(f"TestRail API error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
