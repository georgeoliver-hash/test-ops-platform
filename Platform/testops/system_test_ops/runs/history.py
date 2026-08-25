"""Aggregate the last N TestRail runs into per-case health stats.

This is deterministic: given the same runs it always produces the same flags.
The run-historian agent reads the resulting RunHealthReport JSON and turns the
flags into recommendations (remove / edit / investigate) — that's the judgment
layer; this module only counts and thresholds.
"""

from __future__ import annotations

from datetime import datetime, timezone

from system_test_ops.models import RunHealthReport, TestHealth
from system_test_ops.testrail.client import TestRailClient

# TestRail's built-in status ids. Custom statuses fall back to label heuristics.
_PASSED_IDS = {1}
_BLOCKED_IDS = {2}
_UNTESTED_IDS = {3}
_RETEST_IDS = {4}
_FAILED_IDS = {5}


def _category(status_id: int | None, label_map: dict[int, str]) -> str:
    """Map a TestRail status id to: passed / failed / blocked / untested / other."""
    if status_id is None:
        return "untested"
    if status_id in _PASSED_IDS:
        return "passed"
    if status_id in _FAILED_IDS:
        return "failed"
    if status_id in _BLOCKED_IDS:
        return "blocked"
    if status_id in _UNTESTED_IDS:
        return "untested"
    label = (label_map.get(status_id) or "").lower()
    if "pass" in label:
        return "passed"
    if "fail" in label:
        return "failed"
    if "block" in label:
        return "blocked"
    if "untested" in label:
        return "untested"
    return "other"


def _run_sort_key(run: dict) -> int:
    return int(run.get("created_on") or run.get("completed_on") or 0)


def build_run_health(
    client: TestRailClient,
    *,
    project: str,
    project_id: int,
    suite_id: int | None,
    suite_name: str,
    last_n: int = 10,
) -> RunHealthReport:
    label_map = client.status_label_map()

    runs = client.get_runs(project_id)
    if suite_id is not None:
        # In suite-mode projects each run targets a suite; single-suite projects omit suite_id.
        runs = [r for r in runs if r.get("suite_id") in (None, suite_id)]
    runs.sort(key=_run_sort_key, reverse=True)
    selected = runs[:last_n]
    selected_ids = [int(r["id"]) for r in selected]

    # case_id -> ordered list of (run_id, category), newest run first
    per_case: dict[int, list[tuple[int, str]]] = {}
    case_titles: dict[int, str] = {}
    for run in selected:
        run_id = int(run["id"])
        for test in client.get_tests(run_id):
            cid = test.get("case_id")
            if cid is None:
                continue
            cid = int(cid)
            cat = _category(test.get("status_id"), label_map)
            per_case.setdefault(cid, []).append((run_id, cat))
            if test.get("title"):
                case_titles.setdefault(cid, test["title"])

    # The full case inventory of the suite — lets us detect orphaned cases
    # (never appear in any recent run) as well as case titles.
    suite_case_ids: set[int] = set()
    try:
        for c in client.get_cases(project_id, suite_id):
            cid = int(c["id"])
            suite_case_ids.add(cid)
            if c.get("title"):
                case_titles.setdefault(cid, c["title"])
    except Exception:  # noqa: BLE001 - inventory is best-effort enrichment
        pass

    all_case_ids = suite_case_ids | set(per_case.keys())

    healths: list[TestHealth] = []
    for cid in sorted(all_case_ids):
        history = per_case.get(cid, [])  # newest-first
        cats = [c for _, c in history]
        executed = [c for c in cats if c in ("passed", "failed", "blocked", "other")]
        passed = cats.count("passed")
        failed = cats.count("failed")
        blocked = cats.count("blocked")
        other = cats.count("other")

        h = TestHealth(
            case_id=cid,
            title=case_titles.get(cid),
            runs_considered=len(selected_ids),
            executed_count=len(executed),
            passed=passed,
            failed=failed,
            blocked=blocked,
            other=other,
            last_status_label=cats[0].capitalize() if cats else None,
            run_ids=[rid for rid, _ in history],
        )
        h.orphaned = cid not in per_case
        h.never_executed = (cid in per_case) and len(executed) == 0
        h.always_failing = len(executed) > 0 and failed == len(executed)
        h.flaky = passed > 0 and failed > 0
        # newest executed result is a fail, but an earlier executed result passed
        exec_cats = [c for c in cats if c in ("passed", "failed")]
        h.recently_regressed = bool(exec_cats) and exec_cats[0] == "failed" and "passed" in exec_cats[1:]
        healths.append(h)

    return RunHealthReport(
        project=project,
        suite=suite_name,
        suite_id=suite_id,
        last_n=last_n,
        generated_at=datetime.now(timezone.utc),
        run_ids=selected_ids,
        cases=healths,
    )
