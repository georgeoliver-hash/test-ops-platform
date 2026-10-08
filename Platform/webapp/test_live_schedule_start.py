"""Schedule display and the guarded manual start. gh and the lab are never touched: the CLI call is faked."""
import json

from fastapi.testclient import TestClient

from Platform.webapp import app as app_module
from Platform.webapp import runner

client = TestClient(app_module.app)


def test_the_schedule_is_passed_through(monkeypatch):
    monkeypatch.setattr(runner, "_cli", lambda args, timeout=180: (0, json.dumps({"sam_job_id": 169, "entries": [{"cron": "30 4 * * *", "next_run_utc": "2026-10-09 04:30 UTC", "comment": "POS daily"}], "note": "n"})))
    r = client.get("/api/live/schedule", params={"project": "Translink", "device": "POS"}).json()
    assert r["available"] and r["entries"][0]["next_run_utc"] == "2026-10-09 04:30 UTC"


def test_an_unregistered_target_says_why(monkeypatch):
    monkeypatch.setattr(runner, "_cli", lambda args, timeout=180: (1, "error: No sit pipeline is registered for X/Y."))
    r = client.get("/api/live/schedule", params={"project": "X", "device": "Y"}).json()
    assert r["available"] is False and "registered" in r["reason"]


def test_without_confirm_the_cli_is_never_asked_to_start(monkeypatch):
    seen = []
    monkeypatch.setattr(runner, "_cli", lambda args, timeout=180: seen.append(args) or (0, json.dumps({"started": False, "would_run": "gh workflow run ..."})))
    r = client.post("/api/live/start-run", json={"project": "Translink", "device": "POS", "tag_filter": "diag", "smoke_only": "false"}).json()
    assert r["started"] is False and "--confirm" not in seen[0] and "--tag-filter" in seen[0]


def test_confirm_is_passed_on_only_when_true_and_the_start_is_reported(monkeypatch):
    seen = []
    monkeypatch.setattr(runner, "_cli", lambda args, timeout=180: seen.append(args) or (0, json.dumps({"started": True, "ran": "gh workflow run ...", "output": "https://run/1"})))
    r = client.post("/api/live/start-run", json={"project": "Translink", "device": "POS", "confirm": True}).json()
    assert r["started"] is True and "--confirm" in seen[0]


def test_a_refusal_from_the_cli_is_a_400_with_its_reason(monkeypatch):
    monkeypatch.setattr(runner, "_cli", lambda args, timeout=180: (1, "error: the tag filter must be one exact tag (letters, digits, - _ =; no AND, OR or NOT)"))
    res = client.post("/api/live/start-run", json={"project": "Translink", "device": "POS", "tag_filter": "aORb", "confirm": True})
    assert res.status_code == 400 and "one exact tag" in res.json()["detail"]
