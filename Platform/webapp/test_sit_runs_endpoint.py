"""The run picker's endpoint: lists the target's recent runs through system-test-ops, or says why it cannot."""
import json

from fastapi.testclient import TestClient

from Platform.webapp import app as app_module
from Platform.webapp import runner

client = TestClient(app_module.app)


def test_the_runs_are_passed_through_with_their_results_flag(monkeypatch):
    seen = {}

    def fake_cli(args, timeout=180):
        seen["args"] = args
        return 0, "noise on an earlier line\n" + json.dumps({"runs": [{"run_id": 7, "has_results": True}, {"run_id": 6, "has_results": False}]})

    monkeypatch.setattr(runner, "_cli", fake_cli)
    r = client.get("/api/sit-runs", params={"project": "Translink", "device": "POS", "limit": 5}).json()
    assert r["available"] is True and [x["run_id"] for x in r["runs"]] == [7, 6]
    assert seen["args"][:5] == ["list-sit-runs", "--project", "Translink", "--device", "POS"] and seen["args"][-1] == "5"


def test_a_failure_says_why_and_never_invents_runs(monkeypatch):
    monkeypatch.setattr(runner, "_cli", lambda args, timeout=180: (1, "error: No sit pipeline is registered for X/Y. Add it to knowledge/sit_runs.yaml"))
    r = client.get("/api/sit-runs", params={"project": "X", "device": "Y"}).json()
    assert r["available"] is False and "sit_runs.yaml" in r["reason"] and "runs" not in r


def test_the_limit_is_bounded(monkeypatch):
    got = {}
    monkeypatch.setattr(runner, "_cli", lambda args, timeout=180: (got.setdefault("a", args) and 0, json.dumps({"runs": []})))
    client.get("/api/sit-runs", params={"project": "A", "device": "B", "limit": 5000})
    assert got["a"][-1] == "50"
