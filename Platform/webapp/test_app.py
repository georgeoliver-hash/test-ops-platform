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

from fastapi.testclient import TestClient  # noqa: E402

from Platform.webapp import app as app_module  # noqa: E402
from Platform.webapp.app import app  # noqa: E402

client = TestClient(app)


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
    res = client.get("/api/pipelines")
    assert res.status_code == 200
    by_id = {p["id"]: p for p in res.json()}
    assert by_id["audit"]["runnable"] is True
    assert by_id["onboard-suite"]["runnable"] is False


def test_run_rejects_a_non_runnable_pipeline():
    res = client.post("/api/pipelines/onboard-suite/run", json={"project": "Translink", "device": "POS"})
    assert res.status_code == 400


def test_run_rejects_a_target_with_no_suite_id_configured():
    res = client.post("/api/pipelines/audit/run", json={"project": "NoSuchProject", "device": "NoSuchDevice"})
    assert res.status_code == 400
    assert "new_suite_id" in res.json()["detail"] or "No new_suite_id" in res.json()["detail"]


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
