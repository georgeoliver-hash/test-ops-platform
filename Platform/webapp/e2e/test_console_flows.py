"""Flow tests on a fully set-up target: things a person actually does, not just page loads."""
import json
import urllib.request

import pytest

from .conftest import _api


def _settle(page):
    page.wait_for_function("!document.querySelector('#content .loading')", timeout=20000)


def test_seeded_target_is_ready_and_pipelines_unlock(spage, seeded):
    st = _api(seeded, "GET", "/api/setup-status?project=Translink&device=POS")
    assert st["ready"] is True
    spage.wait_for_selector("button.navitem[data-pipeline]:not(.disabled)")
    assert spage.query_selector_all("button.navitem[data-pipeline].disabled") == []


def _mapping(seeded):
    return next(m for m in _api(seeded, "GET", "/api/suite-mappings") if m["project"] == "Translink" and m["device"] == "POS")


def test_target_chip_shows_mapped_suite(spage, seeded):
    spage.wait_for_function("document.getElementById('targetChip').innerText.includes('New E2E')")
    chip = spage.inner_text("#targetChip")
    assert "Translink" in chip and "POS" in chip and _mapping(seeded)["new_suite"] in chip


def test_change_target_lists_the_saved_pair_and_apply_needs_approval(spage, seeded):
    spage.click("#changeTargetBtn")
    assert _mapping(seeded)["new_suite"] in spage.inner_text("#suiteReadout")
    spage.wait_for_function("document.getElementById('approveCheck').checked")  # seeded target is already approved
    assert not spage.is_disabled("#modalApply")
    spage.click("#modalApply")
    assert not spage.is_visible("#targetModal .modal")


def test_add_new_pair_through_the_second_popup(spage, seeded):
    spage.click("#changeTargetBtn")
    spage.click("#suiteAddProjectBtn")
    spage.wait_for_selector("#editNewProject", state="visible")
    spage.fill("#editNewProject", "E2EProj")
    spage.fill("#editNewDevice", "POS")
    spage.check("#editFreshBuild")
    spage.fill("#editNewSuite", "E2E ETM suite")
    spage.fill("#editNewSuiteId", "900777")
    spage.click("#suiteEditSave")
    spage.wait_for_selector("#pairModal .pair-modal", state="hidden")
    maps = _api(seeded, "GET", "/api/suite-mappings")
    assert any(m["project"] == "E2EProj" and m["new_suite_id"] == 900777 for m in maps)
    _api(seeded, "DELETE", "/api/suite-mappings/E2EProj/POS")


def test_docs_page_lists_the_uploaded_doc(spage):
    spage.evaluate("VIEWS.docs()")
    _settle(spage)
    assert "e2e-spec.md" in spage.inner_text("#content")


def test_gaps_answer_is_logged(spage, seeded):
    spage.click('button.navitem[data-view="gaps"]')
    _settle(spage)
    rows = spage.query_selector_all("[data-gap-open-idx]")
    if not rows:
        pytest.skip("no gap markers in this checkout's knowledge base")
    rows[0].click()
    spage.fill("#gapModalQuestion", "E2E question?")
    spage.fill("#gapModalAnswer", "E2E answer")
    spage.click("#gapModalSave")
    spage.wait_for_selector("#gapModalOverlay.open", state="detached", timeout=10000) if False else spage.wait_for_function(
        "!document.getElementById('gapModalOverlay').classList.contains('open')")
    answers = _api(seeded, "GET", "/api/gap-answers")
    assert any(a["answer"] == "E2E answer" for a in answers)


def test_live_page_loads_a_saved_events_file(spage, seeded, tmp_path):
    events = [{"ev": "run_start", "t": 1.0}, {"ev": "suite_start", "t": 2.0, "name": "E2E", "total": 2},
              {"ev": "test_start", "t": 3.0, "name": "Passes", "suite": "E2E", "tags": []},
              {"ev": "test_end", "t": 4.0, "name": "Passes", "suite": "E2E", "status": "PASS", "message": "", "seconds": 1.0},
              {"ev": "test_start", "t": 5.0, "name": "Fails", "suite": "E2E", "tags": []},
              {"ev": "test_end", "t": 6.0, "name": "Fails", "suite": "E2E", "status": "FAIL", "message": "boom", "seconds": 1.0},
              {"ev": "run_end", "t": 7.0}]
    (tmp_path / "live-events.jsonl").write_text("\n".join(json.dumps(e) for e in events), encoding="utf-8")
    req = urllib.request.Request(seeded + "/api/live/config", method="PUT", data=json.dumps({"results_dir": str(tmp_path)}).encode(),
                                 headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=10).read()
    runs = _api(seeded, "GET", "/api/live/runs")
    mine = [r for r in runs["runs"] if r["path"].startswith(str(tmp_path))]
    assert mine and (mine[0]["total"], mine[0]["passed"], mine[0]["failed"]) == (2, 1, 1)
    spage.click("#tabAutomation")
    _settle(spage)
    spage.evaluate("AUTOMATION_VIEWS.dashboard()")
    _settle(spage)
    text = spage.inner_text("#content")
    assert "Fails" in text or "boom" in text or "E2E" in text
