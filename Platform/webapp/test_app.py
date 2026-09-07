"""Smoke tests for the real (wired-up) Test-Ops Console API.

Every endpoint here is backed by real data (model/ against the live SIT mirror + a real
.claude checkout, or a genuinely-generated build-stats/run-health/gap-register fixture) —
these tests pin that the wiring works, not that the model data itself is correct (see the
model/ test suites for that).
"""
from __future__ import annotations

from fastapi.testclient import TestClient

from Platform.webapp.app import app

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
    assert "card_reading.tap" in data["gaps"].get("njt", [])


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
