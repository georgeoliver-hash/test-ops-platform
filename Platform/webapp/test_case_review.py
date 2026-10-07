"""Case Review: the human half of the build's repair step. TestRail is never called -- the
`fix-case` / `repair` CLIs are faked at the subprocess boundary (case_review._cli)."""
from __future__ import annotations

import json
import os
import subprocess
import tempfile

import pytest

os.environ.setdefault("TESTOPS_WEBAPP_DATA_DIR", tempfile.mkdtemp(prefix="testops-webapp-test-"))

from fastapi.testclient import TestClient  # noqa: E402

from Platform.webapp import case_review, runner, store  # noqa: E402
from Platform.webapp.app import app  # noqa: E402

client = TestClient(app)
Q = "project=Translink&device=POS"


def _plan(*items):
    return {"suite_id": 7, "needs_review": list(items)}


def _item(cid, rule="steps-empty"):
    return {"case_id": cid, "title": f"T{cid}", "rule": rule, "detail": "", "action": "do it",
            "case": {"title": f"T{cid}", "custom_preface": "This test is to confirm x.",
                     "custom_steps_seperated": [], "custom_expected": "ok"}}


@pytest.fixture
def root(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "SYSTEM_TEST_OPS_ROOT", tmp_path)
    monkeypatch.setattr(store, "get_suite_ids", lambda p, d: {"new_suite_id": 7})
    monkeypatch.setattr(store, "get_new_testrail_project_id", lambda p, d: 2)
    d = tmp_path / "proposals" / "Translink-POS-suite-restructure"
    d.mkdir(parents=True)
    return d


def _write(root, plan):
    (root / "repair-plan.json").write_text(json.dumps(plan), encoding="utf-8")


def test_unavailable_without_a_plan(root):
    r = client.get(f"/api/case-review?{Q}").json()
    assert r["available"] is False and r["open"] == 0


def test_lists_open_items_and_waive_needs_reason_and_name(root):
    _write(root, _plan(_item(1), _item(2, "then-compound-genuine")))
    assert client.get(f"/api/case-review?{Q}").json()["open"] == 2
    bad = client.post(f"/api/case-review/1/waive?{Q}", json={"rule": "steps-empty", "reason": " ", "by": "G"})
    assert bad.status_code == 400
    ok = client.post(f"/api/case-review/1/waive?{Q}", json={"rule": "steps-empty", "reason": "screen only", "by": "George"})
    assert ok.status_code == 200 and ok.json()["status"] == "waived"
    r = client.get(f"/api/case-review?{Q}").json()
    assert (r["open"], r["resolved"]) == (1, 1)
    client.post(f"/api/case-review/1/reopen?{Q}", json={"rule": "steps-empty"})
    assert client.get(f"/api/case-review?{Q}").json()["open"] == 2
    assert client.post(f"/api/case-review/99/waive?{Q}", json={"rule": "steps-empty", "reason": "r", "by": "G"}).status_code == 404


def _fake_cli(result, rc=0):
    def run(args, timeout=300):
        return subprocess.CompletedProcess(args, rc, stdout="noise\nRESULT " + json.dumps(result) + "\n", stderr="")
    return run


FIX = {"rule": "steps-empty", "by": "George",
       "fields": {"custom_steps_seperated": [{"content": "**WHEN** a", "expected": "**THEN** b"}]}}


def test_fix_success_marks_fixed_and_updates_snapshot(root, monkeypatch):
    _write(root, _plan(_item(1)))
    monkeypatch.setattr(case_review, "_cli", _fake_cli({"ok": True, "committed": True, "case_id": 1}))
    r = client.post(f"/api/case-review/1/fix?{Q}", json=FIX)
    assert r.status_code == 200
    item = client.get(f"/api/case-review?{Q}").json()["items"][0]
    assert item["resolution"]["status"] == "fixed" and item["resolution"]["by"] == "George"
    assert item["case"]["custom_steps_seperated"][0]["content"] == "**WHEN** a"


def test_fix_refused_leaves_item_open_and_surfaces_reason(root, monkeypatch):
    _write(root, _plan(_item(1)))
    monkeypatch.setattr(case_review, "_cli", _fake_cli({"ok": False, "error": "Not saved: still breaks (steps-empty)."}, rc=2))
    r = client.post(f"/api/case-review/1/fix?{Q}", json=FIX)
    assert r.status_code == 422 and "still breaks" in r.json()["detail"]
    assert client.get(f"/api/case-review?{Q}").json()["open"] == 1


def test_fix_rejects_non_editable_fields(root):
    _write(root, _plan(_item(1)))
    r = client.post(f"/api/case-review/1/fix?{Q}", json={**FIX, "fields": {"title": "x"}})
    assert r.status_code == 400


def test_build_cannot_pass_human_cleanup_while_cases_are_open(root):
    _write(root, _plan(_item(1)))
    run_id = "run-cr-test"
    store.create_run(run_id, "onboard-suite", "Translink", "POS")
    store.create_step_rows(run_id, [("human_cleanup", "human")])
    store.update_step(run_id, "human_cleanup", status="waiting_human")
    with pytest.raises(runner.CaseReviewPendingError):
        runner.resolve_step(run_id, "human_cleanup")


def test_every_decision_is_logged_and_survives_a_recheck(root, monkeypatch):
    _write(root, _plan(_item(1), _item(2)))
    base = client.get(f"/api/case-review/log?{Q}").json()["all_time"]
    client.post(f"/api/case-review/1/waive?{Q}", json={"rule": "steps-empty", "reason": "screen only", "by": "George"})
    monkeypatch.setattr(case_review, "_cli", _fake_cli({"ok": True, "committed": True, "case_id": 2}))
    client.post(f"/api/case-review/2/fix?{Q}", json={**FIX, "by": "Sam"})
    client.post(f"/api/case-review/1/reopen?{Q}", json={"rule": "steps-empty", "by": "George"})
    # a re-check rewrites the plan file and drops everything -- the log must not care
    _write(root, _plan())
    log = client.get(f"/api/case-review/log?{Q}").json()
    got = {a: log["all_time"][a] - base[a] for a in base}
    assert got == {"fixed": 1, "accepted": 1, "reopened": 1}
    assert {e["by"] for e in log["entries"][:3]} == {"George", "Sam"}
    assert log["today"]["accepted"] >= 1


def test_decisions_append_before_after_to_the_repo_writing_lessons(root, tmp_path, monkeypatch):
    _write(root, _plan(_item(1), _item(2)))
    monkeypatch.setattr(case_review, "_cli", _fake_cli({"ok": True, "committed": True, "case_id": 2}))
    client.post(f"/api/case-review/2/fix?{Q}", json={**FIX, "by": "Sam"})
    client.post(f"/api/case-review/1/waive?{Q}", json={"rule": "steps-empty", "reason": "screen only", "by": "George"})
    text = (tmp_path / "knowledge" / "translink" / "writing-lessons.md").read_text(encoding="utf-8")
    assert text.startswith("# Writing lessons -- Translink") and "propose it as a rule" in text
    assert "C2 T2 | steps-empty | **fixed** by Sam" in text
    assert "- before: steps_seperated: (no steps)" in text and "**WHEN** a -> **THEN** b" in text
    assert "C1 T1 | steps-empty | **accepted** by George -- screen only" in text


def test_resume_index_follows_the_current_pipeline_not_the_runs_stored_order(monkeypatch):
    """A run begun before a step was added to the YAML must resume at the right step."""
    class S:  # minimal stand-in for a flattened Step
        def __init__(self, i): self.id = i
    monkeypatch.setattr(runner, "_flatten_steps", lambda *a: [S("x"), S("repair"), S("gate"), S("human_cleanup")])
    monkeypatch.setattr(runner, "load_pipeline", lambda pid: object())
    run = {"pipeline_id": "onboard-suite", "project": "P", "device": "D"}
    # stored order lacked `repair`, so human_cleanup was stored at position 2 -- but it is 3 now
    assert runner._resume_index(run, "human_cleanup", 2) == 3
    assert runner._resume_index(run, "gone_step", 2) == 2  # removed from the YAML -> fall back


def test_suite_counts_leave_retired_cases_out_and_report_them_separately(monkeypatch):
    out = "Wrote 841 cases (463 more marked for delete, left out) ->\n  x\n"
    monkeypatch.setattr(runner.subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(a, 0, stdout=out, stderr=""))
    assert runner._case_counts(30607) == (841, 463)
    assert runner._case_count(30607) == 841
    monkeypatch.setattr(runner.subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(a, 0, stdout="Wrote 120 cases ->\n", stderr=""))
    assert runner._case_counts(9317) == (120, 0)  # an old suite with nothing marked still parses


def test_suite_comparison_reports_marked_for_delete_per_suite(monkeypatch):
    monkeypatch.setattr(store, "get_suite_ids", lambda p, d: {"old_suite_id": 9317, "new_suite_id": 30607})
    monkeypatch.setattr(runner, "_case_counts", lambda sid: (2193, 0) if sid == 9317 else (841, 463))
    monkeypatch.setattr(runner, "_testrail_reachable", lambda timeout=4.0: (True, ""))
    d = runner.compare_suite_case_counts("Translink", "POS")
    assert (d["old_case_count"], d["new_case_count"]) == (2193, 841)
    assert (d["old_marked_for_delete"], d["new_marked_for_delete"]) == (0, 463)
