"""The SAM endpoints pass system-test-ops' read-only client output through, and say why when it cannot."""
import json

from fastapi.testclient import TestClient

from Platform.webapp import app as app_module
from Platform.webapp import runner

client = TestClient(app_module.app)


def test_jobs_are_passed_through(monkeypatch):
    seen = {}
    monkeypatch.setattr(runner, "_cli", lambda args, timeout=180: seen.setdefault("a", args) and (0, json.dumps({"jobs": [{"job_id": 169, "name": "POS", "registered_as": "Translink / POS"}]})))
    r = client.get("/api/sam/jobs").json()
    assert r["available"] and r["jobs"][0]["registered_as"] == "Translink / POS" and seen["a"] == ["sam-jobs"]


def test_job_detail_asks_for_outcomes_only_when_told_to(monkeypatch):
    calls = []
    monkeypatch.setattr(runner, "_cli", lambda args, timeout=180: calls.append(args) or (0, json.dumps({"health": {"runs_completed": 1}})))
    client.get("/api/sam/job/169")
    client.get("/api/sam/job/169", params={"outcomes": "true"})
    assert calls[0] == ["sam-job", "--job", "169"] and calls[1] == ["sam-job", "--job", "169", "--outcomes"]


def test_an_unreachable_sam_is_reported_not_invented(monkeypatch):
    monkeypatch.setattr(runner, "_cli", lambda args, timeout=180: (1, "error: SAM is not reachable at http://x (timed out). Is this machine on the lab network?"))
    r = client.get("/api/sam/jobs").json()
    assert r["available"] is False and "lab network" in r["reason"] and "jobs" not in r


def test_no_credential_field_can_be_present_in_what_assets_returns(monkeypatch):
    monkeypatch.setattr(runner, "_cli", lambda args, timeout=180: (0, json.dumps({"servers": [{"name": "s", "def_ip": "1.1.1.1"}], "devices": [], "environments": []})))
    body = json.dumps(client.get("/api/sam/assets").json()).lower()
    assert "password" not in body and "username" not in body
