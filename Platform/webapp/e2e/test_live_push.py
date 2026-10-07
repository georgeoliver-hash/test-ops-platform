"""Runner -> console push transport, end to end: a real Robot run with the listener posting to a real console."""
import json
import subprocess
import sys
import urllib.error
import urllib.request

from .conftest import _api


def test_push_without_token_is_refused(server):
    req = urllib.request.Request(server + "/api/live/ingest", method="POST", data=json.dumps({"run_id": "x", "events": []}).encode(),
                                 headers={"Content-Type": "application/json", "X-Live-Token": "wrong"})
    try:
        urllib.request.urlopen(req, timeout=10)
        assert False, "should have been refused"
    except urllib.error.HTTPError as e:
        assert e.code == 403


def test_robot_run_pushes_events_the_console_shows(server, tmp_path):
    info = _api(server, "GET", "/api/live/push-info")
    suite = tmp_path / "t.robot"
    suite.write_text("*** Test Cases ***\nGood\n    Log    hi\nBad\n    Fail    boom\n", encoding="utf-8")
    listener = str(__import__("pathlib").Path(__file__).resolve().parents[3] / "tools" / "robot_live_listener.py")
    env = {**__import__("os").environ, "TOPS_LIVE_URL": info["url"], "TOPS_LIVE_TOKEN": info["token"],
           "TOPS_LIVE_RUN_ID": "e2e-push-1", "TOPS_LIVE_EVENTS": str(tmp_path / "res" / "live-events.jsonl")}
    import shutil
    py = next((c for c in (sys.executable, shutil.which("python")) if c and subprocess.run([c, "-m", "robot", "--version"], capture_output=True).returncode in (0, 251)), None)
    if not py:
        import pytest
        pytest.skip("no Python with robotframework available")
    subprocess.run([py, "-m", "robot", "--outputdir", str(tmp_path / "res"), "--listener", listener, str(suite)],
                   env=env, capture_output=True, timeout=120)
    runs = _api(server, "GET", "/api/live/runs")["runs"]
    mine = [r for r in runs if "e2e-push-1" in r["path"]]
    assert mine, runs
    r = mine[0]
    assert (r["total"], r["passed"], r["failed"], r["complete"]) == (2, 1, 1, True)
    assert r["source"] == "github" or r["name"].startswith("Pushed")


def test_sources_panel_shows_push_settings(page):
    page.click("#tabAutomation")
    page.evaluate("AUTOMATION_VIEWS.dashboard()")
    page.wait_for_selector("#lvPushBtn", state="attached")
    page.evaluate("document.getElementById('lvCfg').style.display='block'")
    page.click("#lvPushBtn")
    page.wait_for_selector("#lvPushInfo code")
    assert "TOPS_LIVE_TOKEN=" in page.inner_text("#lvPushInfo")
