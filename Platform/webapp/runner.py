"""Real pipeline execution — the first proof case for the disabled "Run" buttons.

Deliberately scoped to ONE pipeline today: `audit` (read-only Gherkin-standard lint). Per
George's explicit choice (2026-09-08): read-only pipelines get wired up and proven safe
first; write-capable pipelines (onboard-suite, push, add-feature) stay disabled in the UI
until that's shown to work reliably. Nothing here can write to TestRail — system-test-ops'
own TestRailClient has no write endpoints at all (see that repo's CLAUDE.md).

How a run actually happens, matching `audit.yaml`'s two real steps:
  1. `run_audit` (cli, deterministic): shell out to system-test-ops' own venv running
     `python -m system_test_ops audit --suite <id> --no-gate`, with cwd set to the
     system-test-ops repo root. That CLI's own `testrail/client.py` calls `load_dotenv()`
     at import time, so it picks up system-test-ops/.env's real TestRail credentials
     itself — nothing from this app's credential store needs passing through for this
     pipeline. The CLI prints "Report -> <path>" on success; we parse that line rather
     than guessing the date-stamped output path ourselves.
  2. `summarise` (agent): shell out to a real headless Claude Code session
     (`claude -p ... --allowedTools Read --permission-prompts none`) to read that report
     and write a plain-language summary. `--permission-prompts none` means anything that
     would need a prompt is auto-denied rather than hanging; `--allowedTools Read` means
     it structurally cannot do anything but read the one file, whatever the prompt says.

Runs go in a background thread (store.create_run/update_run track status) since a `claude
-p` call can take well over the timeout of a single HTTP request.
"""
from __future__ import annotations

import json
import re
import subprocess
import threading
import uuid
from pathlib import Path

from Platform.webapp import store

_PLATFORM_ROOT = Path(__file__).resolve().parent.parent
SYSTEM_TEST_OPS_ROOT = _PLATFORM_ROOT.parent.parent / "system-test-ops"
_VENV_PYTHON = SYSTEM_TEST_OPS_ROOT / ".venv" / "Scripts" / "python.exe"

RUNNABLE_PIPELINES = {"audit"}  # the only pipeline actually wired to execute, on purpose


def is_runnable(pipeline_id: str) -> bool:
    return pipeline_id in RUNNABLE_PIPELINES


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
        "                'created_on': result.get('created_on'),\n"
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


def start_audit_run(project: str, device: str) -> str:
    """Kicks off a real `audit` run in the background, returns a run id to poll."""
    suite_id = store.get_new_suite_id(project, device)
    if suite_id is None:
        raise ValueError(f"No new_suite_id configured for {project}/{device} — add one in Settings first.")
    run_id = str(uuid.uuid4())
    store.create_run(run_id, "audit", project, device)
    thread = threading.Thread(target=_run_audit_job, args=(run_id, project, suite_id), daemon=True)
    thread.start()
    return run_id


def _run_audit_job(run_id: str, project: str, suite_id: int) -> None:
    try:
        cli_result = subprocess.run(
            [str(_VENV_PYTHON), "-m", "system_test_ops", "audit", "--suite", str(suite_id), "--no-gate"],
            cwd=str(SYSTEM_TEST_OPS_ROOT),
            capture_output=True,
            text=True,
            timeout=180,
        )
    except subprocess.TimeoutExpired:
        store.update_run(run_id, status="failed", error="audit CLI step timed out after 180s")
        return
    except OSError as exc:
        store.update_run(run_id, status="failed", error=f"could not start audit CLI: {exc}")
        return

    cli_output = (cli_result.stdout or "") + (("\n--- stderr ---\n" + cli_result.stderr) if cli_result.stderr else "")
    if cli_result.returncode not in (0, 1):  # 1 = blocking findings found, still a valid completed run
        store.update_run(run_id, status="failed", cli_output=cli_output, error=f"audit CLI exited {cli_result.returncode}")
        return

    match = re.search(r"Report -> (.+)$", cli_result.stdout, re.MULTILINE)
    report_path = match.group(1).strip() if match else None
    store.update_run(run_id, cli_output=cli_output, report_path=report_path)

    if not report_path:
        store.update_run(run_id, status="succeeded", summary="Audit ran, but no report path was found in its output to summarise.")
        return

    full_report_path = SYSTEM_TEST_OPS_ROOT / report_path
    if not full_report_path.is_file():
        store.update_run(run_id, status="succeeded", summary=f"Audit ran and reported {report_path}, but that file wasn't found to summarise.")
        return

    try:
        summarise_result = subprocess.run(
            [
                "claude", "-p",
                f"Read the audit report at {report_path} and write a short, plain-language "
                f"summary: how many cases were audited, how many blocking findings there are "
                f"(if any, name them briefly), and whether this suite is clean to work in. "
                f"No preamble, no markdown headers, 3-6 sentences.",
                "--allowedTools", "Read",
                "--permission-prompts", "none",
                "--output-format", "text",
            ],
            cwd=str(SYSTEM_TEST_OPS_ROOT),
            capture_output=True,
            text=True,
            timeout=120,
        )
        summary = summarise_result.stdout.strip() or "(the summarising agent returned no output)"
    except subprocess.TimeoutExpired:
        summary = "(summarising agent timed out after 120s — see the raw report instead)"
    except OSError as exc:
        summary = f"(could not run the summarising agent: {exc})"

    store.update_run(run_id, status="succeeded", summary=summary)
