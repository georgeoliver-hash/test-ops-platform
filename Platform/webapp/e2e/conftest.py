"""Browser tests for the console. Real server on a free port, throw-away data dir, TestRail forced unreachable
so every run is offline and deterministic. Any JS error, console error or HTTP 5xx during a test fails it."""
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def server(tmp_path_factory):
    data = tmp_path_factory.mktemp("console-data")
    port = _free_port()
    # The suite-target list is a git-tracked file in system-test-ops: NEVER let tests write the real one.
    targets = data / "suite_targets.yaml"
    targets.write_text("\n".join([
        "targets:", "- project: Translink", "  device: POS", "  old_suite: Old E2E", "  old_suite_id: 900000",
        "  new_suite: New E2E", "  new_suite_id: 900001", "  fresh_build: false", "  testrail_project_id: 99",
        "  new_testrail_project_id: null", ""]), encoding="utf-8")
    env = {**os.environ, "TESTOPS_WEBAPP_DATA_DIR": str(data), "TESTOPS_SUITE_TARGETS_PATH": str(targets), "HANDOFF_QUEUE_DIR": str(data / "handoff-queue"), "TESTRAIL_URL": "http://127.0.0.1:9/testrail",
           "PYTHONIOENCODING": "utf-8"}
    log = open(data / "server.log", "w", encoding="utf-8")
    proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "Platform.webapp.app:app", "--host", "127.0.0.1", "--port", str(port)],
                            cwd=str(ROOT), env=env, stdout=log, stderr=subprocess.STDOUT)
    base = f"http://127.0.0.1:{port}"
    for _ in range(60):
        try:
            urllib.request.urlopen(base + "/api/taxonomy", timeout=2)
            break
        except OSError:
            time.sleep(0.5)
    else:
        proc.kill()
        raise RuntimeError("console did not start; see " + str(data / "server.log"))
    yield base
    proc.terminate()
    proc.wait(timeout=10)


@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


@pytest.fixture
def page(browser, server):
    ctx = browser.new_context(viewport={"width": 1400, "height": 1000})
    pg = ctx.new_page()
    pg.set_default_timeout(8000)
    pg.allow_4xx = False  # a test that deliberately provokes a refusal sets this True
    problems: list[str] = []
    pg.on("pageerror", lambda e: problems.append(f"JS error: {e}"))
    pg.on("console", lambda m: problems.append(f"console error: {m.text}") if m.type == "error" and "status of 503" not in m.text and not (pg.allow_4xx and "status of 4" in m.text) else None)
    pg.on("response", lambda r: problems.append(f"HTTP {r.status} {r.url}") if r.status >= 500 and r.status != 503 else None)
    pg.base = server
    pg.goto(server + "/")
    pg.wait_for_selector(".navitem")
    yield pg
    ctx.close()
    assert not problems, "\n".join(problems)


def _api(base, method, path, body=None, files=None):
    import json
    import urllib.request
    data, headers = None, {}
    if body is not None:
        data, headers = json.dumps(body).encode(), {"Content-Type": "application/json"}
    req = urllib.request.Request(base + path, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    return json.loads(raw) if raw else None


@pytest.fixture(scope="session")
def seeded(server):
    """A fully set-up target (fake creds, mapped + approved suite, one doc) so gated pages are live."""
    import urllib.request
    _api(server, "POST", "/api/credentials", {"testrail_url": "http://127.0.0.1:9/testrail", "testrail_user": "e2e@example.com", "testrail_api_key": "e2e-fake-key"})
    _api(server, "POST", "/api/suite-mappings/Translink/POS/approve", {"approved_by": "e2e"})
    boundary = "e2eboundary"
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"e2e-spec.md\"\r\nContent-Type: text/markdown\r\n\r\n"
            "# E2E spec\nThe POS shows a welcome screen.\r\n" f"--{boundary}--\r\n").encode()
    req = urllib.request.Request(server + "/api/docs?project=Translink&device=POS", data=body, method="POST",
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    urllib.request.urlopen(req, timeout=30).read()
    return server


@pytest.fixture
def spage(page, seeded):
    page.reload()
    page.wait_for_selector(".navitem")
    # the landing Status page renders asynchronously and would overwrite a view opened too early
    page.wait_for_function("!document.querySelector('#content .loading') && document.querySelector('#content').innerText.includes('Status')")
    return page
