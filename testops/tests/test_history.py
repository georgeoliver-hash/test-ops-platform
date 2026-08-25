"""Deterministic flag logic in runs/history.py, exercised with a fake client.

No network: FakeClient returns canned TestRail responses so the thresholds are
pinned. TestRail status ids used: 1=passed, 2=blocked, 3=untested, 5=failed.
"""

from __future__ import annotations

from system_test_ops.runs.history import build_run_health


class FakeClient:
    """Minimal stand-in for TestRailClient covering only what build_run_health calls."""

    def __init__(self, runs, tests_by_run, cases):
        self._runs = runs
        self._tests_by_run = tests_by_run
        self._cases = cases

    def status_label_map(self):
        return {1: "Passed", 2: "Blocked", 3: "Untested", 5: "Failed"}

    def get_runs(self, project_id):
        return self._runs

    def get_tests(self, run_id):
        return self._tests_by_run.get(run_id, [])

    def get_cases(self, project_id, suite_id):
        return self._cases


def _build(client):
    return build_run_health(
        client,
        project="translink",
        project_id=1,
        suite_id=None,
        suite_name="POS",
        last_n=10,
    )


def test_flags_cover_each_pattern():
    # newest run first by created_on; build_run_health sorts desc
    runs = [
        {"id": 3, "created_on": 300, "suite_id": None},
        {"id": 2, "created_on": 200, "suite_id": None},
        {"id": 1, "created_on": 100, "suite_id": None},
    ]
    tests = {
        3: [
            {"case_id": 10, "status_id": 5, "title": "always fail"},
            {"case_id": 11, "status_id": 5, "title": "regressed"},
            {"case_id": 12, "status_id": 1, "title": "flaky"},
            {"case_id": 13, "status_id": 3, "title": "never executed"},
        ],
        2: [
            {"case_id": 10, "status_id": 5, "title": "always fail"},
            {"case_id": 11, "status_id": 1, "title": "regressed"},
            {"case_id": 12, "status_id": 5, "title": "flaky"},
            {"case_id": 13, "status_id": 3, "title": "never executed"},
        ],
        1: [
            {"case_id": 10, "status_id": 5, "title": "always fail"},
        ],
    }
    # case 14 exists in the suite but never appears in a run -> orphaned
    cases = [{"id": i, "title": f"case {i}"} for i in (10, 11, 12, 13, 14)]

    report = _build(FakeClient(runs, tests, cases))
    by_id = {h.case_id: h for h in report.cases}

    assert report.run_ids == [3, 2, 1]

    assert by_id[10].always_failing is True
    assert by_id[10].flaky is False

    assert by_id[11].recently_regressed is True  # newest=fail, earlier pass
    assert by_id[11].flaky is True

    assert by_id[12].flaky is True

    assert by_id[13].never_executed is True
    assert by_id[13].executed_count == 0

    assert by_id[14].orphaned is True
    assert by_id[14].run_ids == []


def test_clean_case_has_no_flags():
    runs = [{"id": 1, "created_on": 100, "suite_id": None}]
    tests = {1: [{"case_id": 20, "status_id": 1, "title": "happy"}]}
    report = _build(FakeClient(runs, tests, [{"id": 20, "title": "happy"}]))
    h = {x.case_id: x for x in report.cases}[20]
    assert not any([h.always_failing, h.flaky, h.never_executed, h.recently_regressed, h.orphaned])
    assert h.passed == 1 and h.executed_count == 1
