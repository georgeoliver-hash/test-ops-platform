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
    env = {**os.environ, "TESTOPS_WEBAPP_DATA_DIR": str(data), "TESTRAIL_URL": "http://127.0.0.1:9/testrail",
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
    problems: list[str] = []
    pg.on("pageerror", lambda e: problems.append(f"JS error: {e}"))
    pg.on("console", lambda m: problems.append(f"console error: {m.text}") if m.type == "error" else None)
    pg.on("response", lambda r: problems.append(f"HTTP {r.status} {r.url}") if r.status >= 500 else None)
    pg.base = server
    pg.goto(server + "/")
    pg.wait_for_selector(".navitem")
    yield pg
    ctx.close()
    assert not problems, "\n".join(problems)
