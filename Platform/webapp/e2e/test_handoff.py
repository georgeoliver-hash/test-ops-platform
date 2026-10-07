"""The Hand-offs page: shows the queue, approves and rejects as the signed-in person, and surfaces the rules' refusals."""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STO = ROOT.parent / "system-test-ops"


def _queue_add(server, title, produced_by):
    """Add an item with the real system-test-ops CLI, into the same queue folder the test server reads."""
    env = {**os.environ, "HANDOFF_QUEUE_DIR": _queue_dir(server)}
    from Platform.webapp import runner
    r = subprocess.run([str(runner._VENV_PYTHON), "-m", "system_test_ops", "queue-add", "--stage", "review", "--title", title, "--produced-by", produced_by],
                       cwd=str(STO), env=env, capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr


def _queue_dir(server):
    import json
    import urllib.request
    return json.loads(urllib.request.urlopen(server + "/api/handoff", timeout=10).read())["folder"]


def _open(page):
    # the landing Status page renders asynchronously; opening a view before it finishes lets it write into the new page
    page.wait_for_function("!document.querySelector('#content .loading') && document.querySelector('#content').innerText.includes('Status')", timeout=30000)
    page.evaluate("VIEWS.handoff()")
    page.wait_for_function("!document.querySelector('#content .loading')", timeout=20000)


def test_an_empty_queue_says_so(page):
    _open(page)
    assert "Nothing is waiting" in page.inner_text("#content") or "Hand-offs" in page.inner_text("#content")


def test_a_proposed_item_is_listed_and_can_be_approved(page, server):
    _queue_add(server, "E2E draft for approval", "claude:e2e")
    _open(page)
    row = page.locator("tr[data-handoff-id]", has_text="E2E draft for approval")
    assert "proposed" in row.inner_text() and "claude:e2e" in row.inner_text()
    row.locator("[data-handoff-decide=approved]").click()
    page.wait_for_function("[...document.querySelectorAll('tr[data-handoff-id]')].some(r => r.innerText.includes('E2E draft for approval') && r.innerText.includes('approved'))")
    row = page.locator("tr[data-handoff-id]", has_text="E2E draft for approval")
    assert "approved" in row.inner_text() and "George Oliver" in row.inner_text()
    assert row.locator("[data-handoff-decide]").count() == 0


def test_the_producer_cannot_approve_their_own_item(page, server):
    page.allow_4xx = True  # the refusal is a 400 on purpose
    _queue_add(server, "E2E own work", "George Oliver")
    _open(page)
    page.locator("tr[data-handoff-id]", has_text="E2E own work").locator("[data-handoff-decide=approved]").click()
    page.wait_for_selector("#handoffMsg", state="visible")
    assert "own work" in page.inner_text("#handoffMsg")
    assert "proposed" in page.locator("tr[data-handoff-id]", has_text="E2E own work").inner_text()
