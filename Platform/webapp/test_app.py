"""Smoke tests for the real (wired-up) Test-Ops Console API.

Every endpoint here is backed by real data (model/ against the live SIT mirror + a real
.claude checkout, or a genuinely-generated build-stats/run-health/gap-register fixture) —
these tests pin that the wiring works, not that the model data itself is correct (see the
model/ test suites for that).

TESTOPS_WEBAPP_DATA_DIR is set BEFORE importing the app module, since app.py calls
store.init_db() at import time — without this, running tests would create/mutate the real
developer's Platform/webapp/data/console.db. Set at module level (not a fixture) because
the import itself happens at module load, before any pytest fixture could run first.
"""
from __future__ import annotations

import os
import tempfile

os.environ["TESTOPS_WEBAPP_DATA_DIR"] = tempfile.mkdtemp(prefix="testops-webapp-test-")
# Isolated from the real, committed Platform/config/suite_targets.yaml -- without this, any
# test that upserts a suite mapping would write through to the actual repo file on disk.
os.environ["TESTOPS_SUITE_TARGETS_PATH"] = os.path.join(
    tempfile.mkdtemp(prefix="testops-webapp-test-targets-"), "suite_targets.yaml"
)

from fastapi.testclient import TestClient  # noqa: E402

from Platform.webapp import app as app_module  # noqa: E402
from Platform.webapp import store  # noqa: E402
from Platform.webapp.app import app  # noqa: E402

client = TestClient(app)


class _SyncThread:
    """Drop-in for threading.Thread that runs its target synchronously on .start() —
    lets a test drive runner.py's background job deterministically without real
    subprocess/CLI/claude availability, and without a sleep-and-hope race."""

    def __init__(self, target=None, args=(), kwargs=None, daemon=None):
        self._target = target
        self._args = args
        self._kwargs = kwargs or {}

    def start(self):
        self._target(*self._args, **self._kwargs)


def test_taxonomy_returns_real_projects():
    res = client.get("/api/taxonomy")
    assert res.status_code == 200
    data = res.json()
    assert "Translink" in data
    assert "POS_Way6" in data["Translink"]["POS"]


def test_features_returns_real_gap_for_njt():
    res = client.get("/api/features")
    assert res.status_code == 200
    data = res.json()
    # card_reading.tap used to be this gap; filled in 2026-09-08 with a real cEMV-tap
    # variant from knowledge/njt/specs/fs002-obv-barcode-emv.md — transaction.annulment
    # is the current real, unfilled gap for njt.
    assert "transaction.annulment" in data["gaps"].get("njt", [])


def test_pipelines_list_has_real_descriptions():
    res = client.get("/api/pipelines")
    assert res.status_code == 200
    data = res.json()
    ids = {p["id"] for p in data}
    assert "onboard-suite" in ids
    assert "audit-flows" in ids
    onboard = next(p for p in data if p["id"] == "onboard-suite")
    assert onboard["description"]  # real text from the YAML, not blank


def test_pipeline_detail_has_real_steps():
    res = client.get("/api/pipelines/onboard-suite")
    assert res.status_code == 200
    data = res.json()
    step_ids = {s["id"] for s in data["steps"]}
    assert "author_area" in step_ids


def test_unknown_pipeline_is_404():
    res = client.get("/api/pipelines/does-not-exist")
    assert res.status_code == 404


def test_build_stats_fixture_marked_as_fixture():
    res = client.get("/api/build-stats")
    assert res.status_code == 200
    data = res.json()
    assert data["is_fixture"] is True
    assert data["cases_total"] == 799


def test_run_health_fixture_real_flags():
    res = client.get("/api/run-health")
    assert res.status_code == 200
    data = res.json()
    assert data["is_fixture"] is True
    assert data["cases_total"] == 822
    # real finding: this suite is dominated by orphaned cases, not flaky ones
    assert data["counts"]["orphaned"] > data["counts"]["flaky"]
    assert len(data["shown"]) <= 15


def test_run_health_limit_respected():
    res = client.get("/api/run-health?limit=3")
    assert res.status_code == 200
    assert len(res.json()["shown"]) == 3


def test_gap_register_fixture_capped_but_total_shown():
    res = client.get("/api/gap-register?limit=5")
    assert res.status_code == 200
    data = res.json()
    assert len(data["shown"]) == 5
    assert data["total"] > 5


def test_index_html_served():
    res = client.get("/")
    assert res.status_code == 200
    assert "Test-Ops Console" in res.text


def test_logo_asset_served():
    res = client.get("/assets/arrive-logo.png")
    assert res.status_code == 200
    assert res.headers["content-type"] == "image/png"


def test_me_returns_seeded_user():
    res = client.get("/api/me")
    assert res.status_code == 200
    assert res.json()["display_name"] == "George Oliver"


def test_suite_mappings_seeded_with_real_pair():
    res = client.get("/api/suite-mappings")
    assert res.status_code == 200
    data = res.json()
    assert any(m["project"] == "Translink" and m["device"] == "POS" for m in data)


def test_suite_mapping_upsert_and_delete_roundtrip():
    res = client.post("/api/suite-mappings", json={
        "project": "NJT", "device": "ETM", "old_suite": "Old", "new_suite": "New",
    })
    assert res.status_code == 200
    res = client.get("/api/suite-mappings")
    assert any(m["project"] == "NJT" and m["device"] == "ETM" for m in res.json())

    res = client.delete("/api/suite-mappings/NJT/ETM")
    assert res.status_code == 200
    res = client.get("/api/suite-mappings")
    assert not any(m["project"] == "NJT" and m["device"] == "ETM" for m in res.json())


def test_delete_unknown_mapping_is_404():
    res = client.delete("/api/suite-mappings/DoesNotExist/DEV")
    assert res.status_code == 404


def test_suite_mapping_upsert_persists_testrail_project_id():
    """A hand-typed console project label (e.g. "NJTdryrun") is never itself a real
    TestRail project -- the real one is stored separately and must round-trip."""
    res = client.post("/api/suite-mappings", json={
        "project": "Perth", "device": "POS", "old_suite": "Old", "new_suite": "New",
        "new_suite_id": 1, "testrail_project_id": 13,
    })
    assert res.status_code == 200
    mapping = next(m for m in client.get("/api/suite-mappings").json()
                   if m["project"] == "Perth" and m["device"] == "POS")
    assert mapping["testrail_project_id"] == 13
    client.delete("/api/suite-mappings/Perth/POS")


def test_get_testrail_projects_returns_parsed_json(monkeypatch):
    fake_result = type("R", (), {"returncode": 0, "stdout": '[{"id": 27, "name": "UK Bus Projects"}]', "stderr": ""})()
    monkeypatch.setattr(app_module.subprocess, "run", lambda *a, **kw: fake_result)
    res = client.get("/api/testrail/projects")
    assert res.status_code == 200
    assert res.json() == [{"id": 27, "name": "UK Bus Projects"}]


def test_get_testrail_projects_cli_failure_returns_500(monkeypatch):
    fake_result = type("R", (), {"returncode": 1, "stdout": "", "stderr": "error: no TestRail credentials"})()
    monkeypatch.setattr(app_module.subprocess, "run", lambda *a, **kw: fake_result)
    res = client.get("/api/testrail/projects")
    assert res.status_code == 500
    assert "no TestRail credentials" in res.json()["detail"]


def test_get_testrail_suites_passes_project_id(monkeypatch):
    captured = {}
    def fake_run(cmd, **kw):
        captured["cmd"] = cmd
        return type("R", (), {"returncode": 0, "stdout": '[{"id": 30169, "name": "NJT Farebox and Register Replacement"}]', "stderr": ""})()
    monkeypatch.setattr(app_module.subprocess, "run", fake_run)
    res = client.get("/api/testrail/suites", params={"project_id": 27})
    assert res.status_code == 200
    assert res.json()[0]["id"] == 30169
    assert "--project" in captured["cmd"] and "27" in captured["cmd"]


def test_suite_mapping_upsert_writes_through_to_shared_yaml():
    """Adding/editing a target via the existing "Add/edit this pair" endpoint must land in
    the git-trackable Platform/config/suite_targets.yaml (isolated to a temp path for tests
    -- see TESTOPS_SUITE_TARGETS_PATH at module load above), not just the local db, so a
    colleague who commits+pushes that file shares the new target."""
    res = client.post("/api/suite-mappings", json={
        "project": "Perth", "device": "POS", "old_suite": "Old Perth", "new_suite": "New Perth",
        "new_suite_id": 41000, "old_suite_id": 6000,
    })
    assert res.status_code == 200
    entries = store._load_suite_targets()
    match = [e for e in entries if e["project"] == "Perth" and e["device"] == "POS"]
    assert len(match) == 1
    assert match[0]["new_suite_id"] == 41000
    client.delete("/api/suite-mappings/Perth/POS")  # tidy up (yaml entry deliberately stays -- delete only removes the local db row, matching upsert_suite_mapping's own scope)


def test_git_status_endpoint_returns_a_known_status_value():
    res = client.get("/api/suite-mappings/git-status")
    assert res.status_code == 200
    assert res.json()["status"] in ("clean", "uncommitted", "unpushed", "unknown")


def test_git_status_endpoint_reports_unknown_outside_a_git_repo(monkeypatch, tmp_path):
    monkeypatch.setattr(store, "_repo_root", lambda: tmp_path)
    res = client.get("/api/suite-mappings/git-status")
    assert res.status_code == 200
    assert res.json()["status"] == "unknown"


def test_credentials_status_and_save_never_leaks_key():
    res = client.get("/api/credentials/status")
    assert res.json()["configured"] is False

    res = client.post("/api/credentials", json={
        "testrail_url": "https://example.testrail.io",
        "testrail_user": "george@arrive.com",
        "testrail_api_key": "top-secret-abc",
    })
    assert res.status_code == 200
    assert "top-secret-abc" not in res.text
    assert res.json()["configured"] is True

    res = client.get("/api/credentials/status")
    assert res.json()["configured"] is True
    assert "top-secret-abc" not in res.text

    res = client.delete("/api/credentials")
    assert res.status_code == 200
    assert client.get("/api/credentials/status").json()["configured"] is False


def test_credentials_rejects_blank_fields():
    res = client.post("/api/credentials", json={
        "testrail_url": "", "testrail_user": "x", "testrail_api_key": "y",
    })
    assert res.status_code == 400


def test_docs_upload_list_and_delete_roundtrip():
    res = client.get("/api/docs", params={"project": "NJT", "device": "BV"})
    assert res.status_code == 200
    assert res.json() == []

    res = client.post(
        "/api/docs",
        params={"project": "NJT", "device": "BV"},
        files={"file": ("spec.md", b"# a real spec", "text/markdown")},
    )
    assert res.status_code == 200

    res = client.get("/api/docs", params={"project": "NJT", "device": "BV"})
    assert res.status_code == 200
    names = [d["filename"] for d in res.json()]
    assert names == ["spec.md"]

    res = client.delete("/api/docs/NJT/BV/spec.md")
    assert res.status_code == 200
    assert client.get("/api/docs", params={"project": "NJT", "device": "BV"}).json() == []


def test_docs_delete_unknown_is_404():
    res = client.delete("/api/docs/NoSuch/DEV/missing.md")
    assert res.status_code == 404


def test_detect_env_reports_not_found_when_no_sibling_env(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "SIBLING_ENV_PATH", tmp_path / "does-not-exist.env")
    res = client.get("/api/credentials/detect-env")
    assert res.status_code == 200
    assert res.json() == {"found": False}


def test_detect_and_import_env_credentials_roundtrip(tmp_path, monkeypatch):
    env_file = tmp_path / "sibling.env"
    env_file.write_text(
        "TESTRAIL_URL=http://testraildb/testrail\n"
        "TESTRAIL_USER=george.oliver@arrive.com\n"
        "TESTRAIL_API_KEY=super-secret-value\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(app_module, "SIBLING_ENV_PATH", env_file)
    client.delete("/api/credentials")

    res = client.get("/api/credentials/detect-env")
    assert res.status_code == 200
    body = res.json()
    assert body["found"] is True
    assert body["testrail_user"] == "george.oliver@arrive.com"
    assert "super-secret-value" not in res.text

    res = client.post("/api/credentials/import-env")
    assert res.status_code == 200
    assert res.json()["configured"] is True
    assert "super-secret-value" not in res.text

    status = client.get("/api/credentials/status").json()
    assert status["configured"] is True
    assert status["testrail_url"] == "http://testraildb/testrail"
    client.delete("/api/credentials")


def test_import_env_404_when_nothing_to_import(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "SIBLING_ENV_PATH", tmp_path / "missing.env")
    res = client.post("/api/credentials/import-env")
    assert res.status_code == 404


def test_pipelines_list_flags_which_are_runnable():
    """2026-09-14: the RUNNABLE_PIPELINES allowlist is gone — every pipeline runs through
    the generic step-executor now. Safety moved to the step level (a push --commit step
    always pauses for human approval), not the pipeline level."""
    res = client.get("/api/pipelines")
    assert res.status_code == 200
    by_id = {p["id"]: p for p in res.json()}
    assert by_id["audit"]["runnable"] is True
    assert by_id["onboard-suite"]["runnable"] is True


def test_run_route_now_works_for_previously_blocked_pipelines(monkeypatch):
    """onboard-suite and ingest-docs used to 400 outright (RUNNABLE_PIPELINES). Now the
    route starts a real run — mock the background execution itself so this stays a route-
    level test, not a real subprocess/CLI integration test."""
    monkeypatch.setattr(app_module.runner, "_run_pipeline_job", lambda *a, **kw: None)
    monkeypatch.setattr(app_module.runner.threading, "Thread", _SyncThread)

    res = client.post("/api/pipelines/onboard-suite/run", json={"project": "Translink", "device": "POS"})
    assert res.status_code == 200
    assert "run_id" in res.json()

    res2 = client.post(
        "/api/pipelines/ingest-docs/run",
        json={"project": "Translink", "device": "POS", "extra_inputs": {"docs_path": "C:/docs/translink"}},
    )
    assert res2.status_code == 200
    assert "run_id" in res2.json()


def test_run_rejects_a_target_with_no_suite_id_configured():
    res = client.post("/api/pipelines/audit/run", json={"project": "NoSuchProject", "device": "NoSuchDevice"})
    assert res.status_code == 400
    assert "new_suite_id" in res.json()["detail"] or "No new_suite_id" in res.json()["detail"]


def test_ingest_docs_run_rejects_missing_required_docs_path():
    """docs_path is a required input declared on ingest-docs.yaml itself — the route reads
    that inputs list as the source of truth, not a hardcoded per-pipeline field."""
    res = client.post("/api/pipelines/ingest-docs/run", json={"project": "NJT", "device": "ETM"})
    assert res.status_code == 400
    assert "docs_path" in res.json()["detail"]


def test_ingest_docs_run_accepts_docs_path_and_templates_it_into_the_convert_step(monkeypatch):
    from Platform.webapp import runner as runner_module

    captured_cmds = []

    def fake_run_subprocess(cmd, cwd, timeout, run_id=None):
        captured_cmds.append(cmd)
        return 0, "ok\n", ""

    monkeypatch.setattr(runner_module, "_run_subprocess", fake_run_subprocess)
    monkeypatch.setattr(runner_module.threading, "Thread", _SyncThread)

    res = client.post(
        "/api/pipelines/ingest-docs/run",
        json={"project": "NJT", "device": "ETM", "extra_inputs": {"docs_path": "C:/docs/njt"}},
    )
    assert res.status_code == 200
    run_id = res.json()["run_id"]

    # sync_check (human, no command) resolves first; convert is the first real cli step.
    steps = client.get(f"/api/pipelines/runs/{run_id}/steps").json()
    by_id = {s["step_id"]: s for s in steps}
    assert by_id["sync_check"]["status"] == "waiting_human"
    resolve_res = client.post(f"/api/pipelines/runs/{run_id}/steps/sync_check/resolve")
    assert resolve_res.status_code == 200

    convert_cmd = next(cmd for cmd in captured_cmds if "ingest_docs.py" in " ".join(cmd))
    assert "C:/docs/njt" in convert_cmd
    assert "--project" in convert_cmd and "NJT" in convert_cmd


def test_ingest_docs_commit_pr_is_a_plain_human_step_not_a_push_gate(monkeypatch):
    """commit_pr is `kind: human` with no push --commit anywhere in it — it must render as
    a plain 'Continue'-style human step, never mistaken for a TestRail push approval gate."""
    from Platform.webapp import runner as runner_module

    def fake_run_subprocess(cmd, cwd, timeout, run_id=None):
        return 0, "ok\n", ""

    monkeypatch.setattr(runner_module, "_run_subprocess", fake_run_subprocess)
    monkeypatch.setattr(runner_module.threading, "Thread", _SyncThread)

    res = client.post(
        "/api/pipelines/ingest-docs/run",
        json={"project": "NJT", "device": "ETM", "extra_inputs": {"docs_path": "C:/docs/njt"}},
    )
    run_id = res.json()["run_id"]
    # sync_check (human) is the only pause before convert/distil/cross_examine (cli/agent —
    # both mocked to succeed) run straight through to the next human step, commit_pr.
    steps = client.get(f"/api/pipelines/runs/{run_id}/steps").json()
    assert next(s for s in steps if s["status"] == "waiting_human")["step_id"] == "sync_check"
    resolve_res = client.post(f"/api/pipelines/runs/{run_id}/steps/sync_check/resolve")
    assert resolve_res.status_code == 200

    steps = client.get(f"/api/pipelines/runs/{run_id}/steps").json()
    commit_pr = next(s for s in steps if s["step_id"] == "commit_pr")
    assert commit_pr["status"] == "waiting_human"
    output = commit_pr["output"] or ""
    assert not ("push" in output and "--commit" in output)
    assert "Commit" in output or "commit" in output


def test_audit_runs_through_generic_engine_same_externally_observable_behavior(monkeypatch, tmp_path):
    """The explicit regression gate: audit must behave identically now that it runs
    through the generic step-executor as it did with the old hardcoded runner — same
    status transitions, report_path/summary population."""
    from Platform.webapp import runner as runner_module

    monkeypatch.setattr(runner_module, "SYSTEM_TEST_OPS_ROOT", tmp_path)
    report_rel = "reports/Translink/30253/2026-09-14/alignment-audit.md"
    report_full = tmp_path / report_rel
    report_full.parent.mkdir(parents=True, exist_ok=True)
    report_full.write_text("fake report", encoding="utf-8")

    def fake_run_subprocess(cmd, cwd, timeout, run_id=None):
        if "claude" in cmd:
            return 0, "Audit ran cleanly on 42 cases, 0 blocking findings.", ""
        return 0, f"Report -> {report_rel}\n", ""

    monkeypatch.setattr(runner_module, "_run_subprocess", fake_run_subprocess)
    monkeypatch.setattr(runner_module.threading, "Thread", _SyncThread)

    res = client.post("/api/pipelines/audit/run", json={"project": "Translink", "device": "POS"})
    assert res.status_code == 200
    run_id = res.json()["run_id"]

    run = client.get(f"/api/pipelines/runs/{run_id}").json()
    assert run["status"] == "succeeded"
    assert run["report_path"] == report_rel
    assert "42 cases" in run["summary"]

    steps = client.get(f"/api/pipelines/runs/{run_id}/steps").json()
    step_ids = {s["step_id"] for s in steps}
    assert {"run_audit", "summarise"} <= step_ids
    assert all(s["status"] == "succeeded" for s in steps)


def test_human_step_pauses_run_until_resolved(monkeypatch):
    from model.pipelines import Pipeline, Step, StepKind, Trigger
    from Platform.webapp import runner as runner_module

    fake_pipeline = Pipeline(
        id="fake-human", trigger=Trigger(ui_action="fake_human"), description="test pipeline",
        steps=[
            Step(id="step_one", kind=StepKind.human, note="approve me"),
            Step(id="step_two", kind=StepKind.cli, command="python -m system_test_ops audit --suite 1"),
        ],
    )
    monkeypatch.setattr(runner_module, "load_pipeline", lambda pid: fake_pipeline)
    monkeypatch.setattr(runner_module.threading, "Thread", _SyncThread)

    run_id = runner_module.start_run("fake-human", "Translink", "POS")
    run = store.get_run(run_id)
    assert run["status"] == "waiting_human"
    by_id = {s["step_id"]: s for s in store.get_steps(run_id)}
    assert by_id["step_one"]["status"] == "waiting_human"
    assert by_id["step_two"]["status"] == "pending"  # never dispatched — no auto-advance

    def fake_run_subprocess(cmd, cwd, timeout, run_id=None):
        return 0, "ok\n", ""

    monkeypatch.setattr(runner_module, "_run_subprocess", fake_run_subprocess)
    resolve_res = client.post(f"/api/pipelines/runs/{run_id}/steps/step_one/resolve")
    assert resolve_res.status_code == 200

    run = store.get_run(run_id)
    assert run["status"] == "succeeded"
    by_id = {s["step_id"]: s for s in store.get_steps(run_id)}
    assert by_id["step_one"]["status"] == "succeeded"
    assert by_id["step_two"]["status"] == "succeeded"


def test_resolve_409s_when_step_not_waiting(monkeypatch):
    from model.pipelines import Pipeline, Step, StepKind, Trigger
    from Platform.webapp import runner as runner_module

    fake_pipeline = Pipeline(
        id="fake-human-2", trigger=Trigger(ui_action="fake_human_2"), description="test pipeline",
        steps=[Step(id="only_step", kind=StepKind.human, note="approve me")],
    )
    monkeypatch.setattr(runner_module, "load_pipeline", lambda pid: fake_pipeline)
    monkeypatch.setattr(runner_module.threading, "Thread", _SyncThread)

    run_id = runner_module.start_run("fake-human-2", "Translink", "POS")
    res = client.post(f"/api/pipelines/runs/{run_id}/steps/only_step/resolve")
    assert res.status_code == 200
    res2 = client.post(f"/api/pipelines/runs/{run_id}/steps/only_step/resolve")
    assert res2.status_code == 409


def test_push_commit_step_is_always_forced_human_regardless_of_declared_kind(monkeypatch):
    """The hardcoded safety override: a step whose command contains push + --commit is
    always treated as a human gate, even if the YAML marks it `kind: cli` (or `gate`)."""
    from model.pipelines import Pipeline, Step, StepKind, Trigger
    from Platform.webapp import runner as runner_module

    fake_pipeline = Pipeline(
        id="fake-push", trigger=Trigger(ui_action="fake_push"), description="test pipeline",
        steps=[Step(id="push_area", kind=StepKind.cli, command="python -m system_test_ops push --file area.cases.yaml --commit")],
    )
    monkeypatch.setattr(runner_module, "load_pipeline", lambda pid: fake_pipeline)
    monkeypatch.setattr(runner_module.threading, "Thread", _SyncThread)

    def fail_if_called(*a, **kw):
        raise AssertionError("push --commit must never be auto-executed")

    monkeypatch.setattr(runner_module, "_run_subprocess", fail_if_called)

    run_id = runner_module.start_run("fake-push", "Translink", "POS")
    run = store.get_run(run_id)
    assert run["status"] == "waiting_human"
    step = store.get_step(run_id, "push_area")
    assert step["status"] == "waiting_human"


def test_approve_target_endpoint_roundtrip():
    # Translink/PV, not touched by any earlier test that deletes/mutates suite mappings.
    res = client.post("/api/suite-mappings/Translink/PV/approve", json={"approved_by": "George Oliver"})
    assert res.status_code == 200
    body = res.json()
    assert body["approved_by"] == "George Oliver"
    assert body["approved_at"] is not None

    mappings = {m["project"] + "|" + m["device"]: m for m in client.get("/api/suite-mappings").json()}
    assert mappings["Translink|PV"]["approved_by"] == "George Oliver"


def test_approve_target_404s_for_unknown_target():
    res = client.post("/api/suite-mappings/NoSuchProject/NoSuchDevice/approve", json={"approved_by": "George Oliver"})
    assert res.status_code == 404


def test_resolve_push_commit_step_refused_when_target_not_approved(monkeypatch):
    """The Phase 4 precondition: even after a per-run human confirmation, resolving a
    push+--commit gate is refused (403) if the target itself has no persisted approval —
    a second, independent gate on top of the per-step one Phase 1 already built."""
    from model.pipelines import Pipeline, Step, StepKind, Trigger
    from Platform.webapp import runner as runner_module

    fake_pipeline = Pipeline(
        id="fake-push-unapproved", trigger=Trigger(ui_action="fake_push_unapproved"), description="test pipeline",
        steps=[Step(id="push_area", kind=StepKind.cli, command="python -m system_test_ops push --file area.cases.yaml --commit")],
    )
    monkeypatch.setattr(runner_module, "load_pipeline", lambda pid: fake_pipeline)
    monkeypatch.setattr(runner_module.threading, "Thread", _SyncThread)

    def fail_if_called(*a, **kw):
        raise AssertionError("push --commit must never execute when the target isn't approved")

    monkeypatch.setattr(runner_module, "_run_subprocess", fail_if_called)

    run_id = runner_module.start_run("fake-push-unapproved", "Translink", "GV")  # unapproved target, distinct from other tests
    res = client.post(f"/api/pipelines/runs/{run_id}/steps/push_area/resolve")
    assert res.status_code == 403

    # left retryable, not failed outright -- approving the target and clicking again just works
    step = store.get_step(run_id, "push_area")
    assert step["status"] == "waiting_human"
    run = store.get_run(run_id)
    assert run["status"] == "waiting_human"


def test_resolve_push_commit_step_succeeds_once_target_approved(monkeypatch):
    from model.pipelines import Pipeline, Step, StepKind, Trigger
    from Platform.webapp import runner as runner_module

    fake_pipeline = Pipeline(
        id="fake-push-approved", trigger=Trigger(ui_action="fake_push_approved"), description="test pipeline",
        steps=[Step(id="push_area", kind=StepKind.cli, command="python -m system_test_ops push --file area.cases.yaml --commit")],
    )
    monkeypatch.setattr(runner_module, "load_pipeline", lambda pid: fake_pipeline)
    monkeypatch.setattr(runner_module.threading, "Thread", _SyncThread)
    calls = []
    def _fake_run_subprocess(*a, **kw):
        calls.append(a[0] if a else kw.get("cmd"))
        return (0, "Wrote 3 cases -> out.md", "")
    monkeypatch.setattr(runner_module, "_run_subprocess", _fake_run_subprocess)

    approve_res = client.post("/api/suite-mappings/Translink/HHD/approve", json={"approved_by": "George Oliver"})
    assert approve_res.status_code == 200

    run_id = runner_module.start_run("fake-push-approved", "Translink", "HHD")
    # Regression guard: a real push step being approved MUST actually run the command, not
    # just mark itself succeeded and move on -- found live: George's onboard-suite push_area
    # was approved, the whole run then "succeeded" all the way through, but `push --commit`
    # was never actually executed and nothing ever reached TestRail. This assertion is the
    # one this test was missing before that bug shipped.
    assert calls == [], "the push command must not run before it's approved"
    res = client.post(f"/api/pipelines/runs/{run_id}/steps/push_area/resolve")
    assert res.status_code == 200
    run = store.get_run(run_id)
    assert run["status"] == "succeeded"
    assert len(calls) == 1, "approving the push gate must actually execute the real command exactly once"
    assert "push" in calls[0] and "--commit" in calls[0]


def test_loop_step_fans_out_one_per_ingested_spec(tmp_path, monkeypatch):
    """author_area's `loop: "one per functional area"` expands into one real step row per
    knowledge/{project}/specs/*.md file — not one generic step run once."""
    from model.pipelines import Pipeline, Step, StepKind, Trigger
    from Platform.webapp import runner as runner_module

    specs_dir = tmp_path / "knowledge" / "fakeproj" / "specs"
    specs_dir.mkdir(parents=True)
    (specs_dir / "fs002-fare-structure.md").write_text("x")
    (specs_dir / "fs002-operator-menu.md").write_text("x")
    monkeypatch.setattr(runner_module, "SYSTEM_TEST_OPS_ROOT", tmp_path)

    fake_pipeline = Pipeline(
        id="fake-loop", trigger=Trigger(ui_action="fake_loop"), description="test pipeline",
        steps=[Step(id="author_area", kind=StepKind.agent, agent="gherkin-author", loop="one per functional area", produces="<area>.cases.yaml")],
    )
    monkeypatch.setattr(runner_module, "load_pipeline", lambda pid: fake_pipeline)
    monkeypatch.setattr(runner_module.threading, "Thread", _SyncThread)
    monkeypatch.setattr(runner_module, "_run_subprocess", lambda *a, **kw: (0, "ok", ""))

    run_id = runner_module.start_run("fake-loop", "FakeProj", "ETM")
    steps = store.get_steps(run_id)
    ids = sorted(s["step_id"] for s in steps)
    assert ids == ["author_area[fare-structure]", "author_area[operator-menu]"]
    assert all(s["status"] == "succeeded" for s in steps)


def test_loop_step_fails_clearly_with_no_ingested_specs(tmp_path, monkeypatch):
    from model.pipelines import Pipeline, Step, StepKind, Trigger
    from Platform.webapp import runner as runner_module

    monkeypatch.setattr(runner_module, "SYSTEM_TEST_OPS_ROOT", tmp_path)  # empty -- no knowledge/ dir at all

    fake_pipeline = Pipeline(
        id="fake-loop-empty", trigger=Trigger(ui_action="fake_loop_empty"), description="test pipeline",
        steps=[Step(id="author_area", kind=StepKind.agent, agent="gherkin-author", loop="one per functional area")],
    )
    monkeypatch.setattr(runner_module, "load_pipeline", lambda pid: fake_pipeline)
    monkeypatch.setattr(runner_module.threading, "Thread", _SyncThread)

    run_id = runner_module.start_run("fake-loop-empty", "FakeProj", "ETM")
    steps = store.get_steps(run_id)
    assert [s["step_id"] for s in steps] == ["author_area"]
    assert steps[0]["status"] == "failed"
    assert "ingest-docs" in steps[0]["output"]


def test_fanned_out_push_steps_each_require_own_resolve_and_shared_target_approval(tmp_path, monkeypatch):
    """Two areas' push_area steps: each needs its OWN resolve call (independent step
    rows), but both check the SAME per-target approval flag — approving the target once
    unlocks both areas' push, matching Phase 4's per-target (not per-area) approval."""
    from model.pipelines import Pipeline, Step, StepKind, Trigger
    from Platform.webapp import runner as runner_module

    specs_dir = tmp_path / "knowledge" / "fakeproj2" / "specs"
    specs_dir.mkdir(parents=True)
    (specs_dir / "fs002-area-one.md").write_text("x")
    (specs_dir / "fs002-area-two.md").write_text("x")
    monkeypatch.setattr(runner_module, "SYSTEM_TEST_OPS_ROOT", tmp_path)

    fake_pipeline = Pipeline(
        id="fake-loop-push", trigger=Trigger(ui_action="fake_loop_push"), description="test pipeline",
        steps=[Step(id="push_area", kind=StepKind.cli, loop="one per functional area",
                     command="python -m system_test_ops push --file <area>.cases.yaml --commit")],
    )
    monkeypatch.setattr(runner_module, "load_pipeline", lambda pid: fake_pipeline)
    monkeypatch.setattr(runner_module.threading, "Thread", _SyncThread)
    monkeypatch.setattr(runner_module, "_run_subprocess", lambda *a, **kw: (0, "ok", ""))

    run_id = runner_module.start_run("fake-loop-push", "FakeProj2", "ETM")
    steps = {s["step_id"]: s for s in store.get_steps(run_id)}
    assert set(steps) == {"push_area[area-one]", "push_area[area-two]"}
    # the run engine is sequential -- it pauses at the FIRST push gate; the second area's
    # step doesn't reach waiting_human until the first is resolved past.
    assert steps["push_area[area-one]"]["status"] == "waiting_human"
    assert steps["push_area[area-two]"]["status"] == "pending"

    # unapproved -> refused, retryable (stays waiting_human)
    res = client.post(f"/api/pipelines/runs/{run_id}/steps/push_area[area-one]/resolve")
    assert res.status_code == 403
    assert store.get_step(run_id, "push_area[area-one]")["status"] == "waiting_human"

    # a mapping must exist before it can be approved (approve is UPDATE-only, not upsert)
    add_res = client.post("/api/suite-mappings", json={
        "project": "FakeProj2", "device": "ETM", "old_suite": "", "new_suite": "Fake Suite",
        "new_suite_id": 99999, "fresh_build": True,
    })
    assert add_res.status_code == 200

    # approve the TARGET once -> both areas' push steps succeed independently, each via
    # its own resolve call, both checking the same target-approval flag
    approve_res = client.post("/api/suite-mappings/FakeProj2/ETM/approve", json={"approved_by": "George Oliver"})
    assert approve_res.status_code == 200

    res = client.post(f"/api/pipelines/runs/{run_id}/steps/push_area[area-one]/resolve")
    assert res.status_code == 200
    assert store.get_step(run_id, "push_area[area-one]")["status"] == "succeeded"
    assert store.get_step(run_id, "push_area[area-two]")["status"] == "waiting_human"  # now reached, paused again

    res2 = client.post(f"/api/pipelines/runs/{run_id}/steps/push_area[area-two]/resolve")
    assert res2.status_code == 200
    assert store.get_step(run_id, "push_area[area-two]")["status"] == "succeeded"
    assert store.get_run(run_id)["status"] == "succeeded"


def test_export_automation_runs_end_to_end_with_optional_flag(monkeypatch):
    """export-automation's `export` step's `[--include-manual]` is documentation shorthand
    -- resolved to a real --include-manual flag only when that declared input is truthy,
    stripped entirely otherwise. report_counts (an unnamed agent step) runs the same
    default-Read-tools path audit.yaml's summarise step already uses."""
    from Platform.webapp import runner as runner_module

    monkeypatch.setattr(runner_module.threading, "Thread", _SyncThread)
    seen_cmds = []

    def fake_run_subprocess(cmd, cwd, timeout, run_id=None):
        seen_cmds.append(cmd)
        if cmd[0] == "claude":
            return 0, "12 of 40 cases automatable, 2 destructive, 5 manual-only.", ""
        return 0, "Wrote automation-backlog.json/.md", ""

    monkeypatch.setattr(runner_module, "_run_subprocess", fake_run_subprocess)

    run_id = runner_module.start_run(
        "export-automation", "Translink", "TVM", extra_inputs={"include_manual": "true"},
    )
    run = store.get_run(run_id)
    assert run["status"] == "succeeded"
    assert run["summary"] == "12 of 40 cases automatable, 2 destructive, 5 manual-only."

    export_cmd = seen_cmds[0]
    assert "--include-manual" in export_cmd
    assert not any("[" in part for part in export_cmd)  # bracket shorthand never reaches argv


def test_export_automation_strips_optional_flag_when_not_requested(monkeypatch):
    from Platform.webapp import runner as runner_module

    monkeypatch.setattr(runner_module.threading, "Thread", _SyncThread)
    seen_cmds = []

    def fake_run_subprocess(cmd, cwd, timeout, run_id=None):
        seen_cmds.append(cmd)
        return 0, "ok", ""

    monkeypatch.setattr(runner_module, "_run_subprocess", fake_run_subprocess)
    runner_module.start_run("export-automation", "Translink", "TVM")
    assert "--include-manual" not in seen_cmds[0]


def test_write_automation_loads_and_pauses_at_confirm_devices(monkeypatch):
    """write-automation's real, unresolved gap (device.yaml facts nobody has provided) is
    its FIRST step, a plain human confirmation — the run must pause there immediately,
    before any agent step runs, and never touch git."""
    from Platform.webapp import runner as runner_module

    monkeypatch.setattr(runner_module.threading, "Thread", _SyncThread)
    run_id = runner_module.start_run("write-automation", "Translink", "TVM")
    run = store.get_run(run_id)
    assert run["status"] == "waiting_human"
    step = store.get_step(run_id, "confirm_devices")
    assert step["status"] == "waiting_human"
    assert "devices.yaml" in step["output"]


def test_write_automation_agent_step_runs_in_test_automation_sit_cwd(monkeypatch):
    """write_tests declares repo: test-automation-sit — the agent subprocess must run
    with that repo as cwd, not system-test-ops (this is a SEPARATE checkout/remote)."""
    from Platform.webapp import runner as runner_module

    monkeypatch.setattr(runner_module.threading, "Thread", _SyncThread)
    seen_cwds = []

    def fake_run_subprocess(cmd, cwd, timeout, run_id=None):
        seen_cwds.append(cwd)
        return 0, "wrote 3 .robot files", ""

    monkeypatch.setattr(runner_module, "_run_subprocess", fake_run_subprocess)

    run_id = runner_module.start_run("write-automation", "Translink", "TVM")
    res = client.post(f"/api/pipelines/runs/{run_id}/steps/confirm_devices/resolve")
    assert res.status_code == 200

    # write_tests ran (succeeded) and the run advanced to commit_push, which pauses next
    assert store.get_step(run_id, "write_tests")["status"] == "succeeded"
    assert store.get_step(run_id, "commit_push")["status"] == "waiting_human"
    assert str(runner_module.TEST_AUTOMATION_SIT_ROOT) in seen_cwds


def test_write_automation_never_auto_pushes(monkeypatch):
    """commit_push is a human step describing `git commit && git push` — confirm nothing
    in this run ever actually invokes git, and the step pauses rather than executing."""
    from Platform.webapp import runner as runner_module

    monkeypatch.setattr(runner_module.threading, "Thread", _SyncThread)

    def fail_if_git(cmd, cwd, timeout, run_id=None):
        cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
        assert "git" not in cmd_str, "write-automation must never auto-run git"
        return 0, "wrote 3 .robot files", ""

    monkeypatch.setattr(runner_module, "_run_subprocess", fail_if_git)

    run_id = runner_module.start_run("write-automation", "Translink", "TVM")
    client.post(f"/api/pipelines/runs/{run_id}/steps/confirm_devices/resolve")
    step = store.get_step(run_id, "commit_push")
    assert step["status"] == "waiting_human"
    run = store.get_run(run_id)
    assert run["status"] == "waiting_human"


def test_git_push_command_is_always_forced_human_regardless_of_declared_kind(monkeypatch):
    """The same hardcoded safety override as TestRail's push+--commit, generalized: any
    rendered command containing "git push" is always a human gate."""
    from model.pipelines import Pipeline, Step, StepKind, Trigger
    from Platform.webapp import runner as runner_module

    fake_pipeline = Pipeline(
        id="fake-git-push", trigger=Trigger(ui_action="fake_git_push"), description="test pipeline",
        steps=[Step(id="push_it", kind=StepKind.cli, command="git push origin main")],
    )
    monkeypatch.setattr(runner_module, "load_pipeline", lambda pid: fake_pipeline)
    monkeypatch.setattr(runner_module.threading, "Thread", _SyncThread)

    def fail_if_called(*a, **kw):
        raise AssertionError("git push must never be auto-executed")

    monkeypatch.setattr(runner_module, "_run_subprocess", fail_if_called)

    run_id = runner_module.start_run("fake-git-push", "Translink", "POS")
    step = store.get_step(run_id, "push_it")
    assert step["status"] == "waiting_human"


def test_get_run_404_for_unknown_id():
    res = client.get("/api/pipelines/runs/does-not-exist")
    assert res.status_code == 404


def test_setup_status_ready_for_a_real_configured_target():
    client.post("/api/credentials", json={
        "testrail_url": "https://example.testrail.io", "testrail_user": "x", "testrail_api_key": "y",
    })
    res = client.get("/api/setup-status", params={"project": "Translink", "device": "POS"})
    assert res.status_code == 200
    body = res.json()
    assert body["suite_configured"] is True
    assert body["ready"] is True
    client.delete("/api/credentials")


def test_setup_status_not_ready_for_an_unconfigured_target():
    res = client.get("/api/setup-status", params={"project": "NoSuchProject", "device": "NoSuchDevice"})
    assert res.status_code == 200
    body = res.json()
    assert body["suite_configured"] is False
    assert body["docs_configured"] is False
    assert body["ready"] is False


def test_refresh_check_reports_no_folder_for_unknown_project():
    res = client.post("/api/docs/NoSuchProject/refresh-check")
    assert res.status_code == 200
    assert res.json()["exists"] is False


def test_refresh_check_detects_new_then_unchanged_then_modified(tmp_path, monkeypatch):
    home_dir = tmp_path / "fake-home"
    req_dir = home_dir / "TestOpsRequirements" / "testproj"
    req_dir.mkdir(parents=True)
    (req_dir / "spec.txt").write_text("v1", encoding="utf-8")
    monkeypatch.setattr(app_module.Path, "home", classmethod(lambda cls: home_dir))

    res = client.post("/api/docs/testproj/refresh-check")
    body = res.json()
    assert body["exists"] is True
    assert body["new"] == ["spec.txt"]

    res = client.post("/api/docs/testproj/refresh-check")
    body = res.json()
    assert body["new"] == [] and body["changed"] == [] and body["unchanged_count"] == 1

    (home_dir / "TestOpsRequirements" / "testproj" / "spec.txt").write_text("v2 - longer content now", encoding="utf-8")
    res = client.post("/api/docs/testproj/refresh-check")
    body = res.json()
    assert body["changed"] == ["spec.txt"]


def test_last_run_null_when_never_run():
    res = client.get("/api/pipelines/audit/last-run", params={"project": "NoSuchProject", "device": "NoSuchDevice"})
    assert res.status_code == 200
    assert res.json()["status"] is None


def test_suite_comparison_unavailable_for_unconfigured_target():
    res = client.get("/api/suite-comparison", params={"project": "NoSuchProject", "device": "NoSuchDevice"})
    assert res.status_code == 200
    assert res.json()["available"] is False


def test_gap_answer_add_list_and_delete_roundtrip():
    res = client.post("/api/gap-answers", json={
        "project": "TestProj", "device": "TVM", "gap_ref": "C123",
        "question": "Is this stale?", "answer": "No, confirmed current.",
    })
    assert res.status_code == 200
    answer_id = res.json()["id"]

    res = client.get("/api/gap-answers", params={"project": "TestProj"})
    assert res.status_code == 200
    assert any(a["id"] == answer_id and a["gap_ref"] == "C123" for a in res.json())

    res = client.delete(f"/api/gap-answers/{answer_id}")
    assert res.status_code == 200
    assert not any(a["id"] == answer_id for a in client.get("/api/gap-answers", params={"project": "TestProj"}).json())


def test_gap_answer_rejects_blank_fields():
    res = client.post("/api/gap-answers", json={
        "project": "TestProj", "gap_ref": "", "question": "q", "answer": "a",
    })
    assert res.status_code == 400


def test_run_comments_rejects_bad_which():
    res = client.get("/api/run-comments", params={"project": "Translink", "device": "POS", "which": "sideways"})
    assert res.status_code == 400


def test_run_comments_unavailable_for_unconfigured_target():
    res = client.get("/api/run-comments", params={"project": "NoSuchProject", "device": "NoSuchDevice"})
    assert res.status_code == 200
    assert res.json()["available"] is False
