"""Click a test on the Live page and see it in full: scenario, tags, steps, the card XML presented, the log, what printed meanwhile."""
import json
import os
import urllib.request

from Platform.webapp.test_live_detail import CARD, XML, ld


def test_a_test_opens_with_everything_about_it(spage, server, tmp_path):
    results, tickets = tmp_path / "results", tmp_path / "tickets"
    results.mkdir(), tickets.mkdir()
    (results / "output.xml").write_text(XML, encoding="utf-8")
    start = ld._iso("2026-10-08T10:00:00.000000")
    (tickets / "ticket_1.txt").write_text("ADULT SINGLE 3.10", encoding="utf-8")
    os.utime(tickets / "ticket_1.txt", (start + 3, start + 3))
    (results / "state_failure_Present_A_Concession_Card.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    req = urllib.request.Request(server + "/api/live/config", method="PUT", data=json.dumps({"results_dir": str(results), "tickets_dir": str(tickets)}).encode(),
                                 headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=10).read()

    spage.click("#tabAutomation")
    spage.click('button.navitem[data-aview="dashboard"]')
    row = spage.locator('[data-lv-test="Present A Concession Card"]')
    row.wait_for(timeout=60000)
    row.click()
    spage.wait_for_selector("#lvTestBox .lvm-body", timeout=20000)
    spage.wait_for_function("document.querySelector('#lvTestBox').innerText.toLowerCase().includes('scenario')")
    text = spage.inner_text("#lvTestBox")
    assert "Given a concession card is presented" in text                       # scenario
    assert "area: Smartcard" in text and "Smoke" in text and "testrail: C4111026" in text   # tags
    assert "Device: Smartcard: Present Card" in text and "POS: Assert On Screen" in text   # steps
    assert "Expected ConcessionAccepted, got CardRejected" in text              # the failure
    assert "ADULT SINGLE 3.10" in text                                          # printed while it ran
    assert "Presenting Concession card card_a.xml" in text                      # log
    spage.click("#lvTestBox details summary")                                   # the card XML opens and is pretty-printed
    xml_text = spage.inner_text("#lvTestBox details pre")
    assert "<SmartCard>" in xml_text and "  <Id>12345</Id>" in xml_text
    assert spage.locator('#lvTestBox img[alt^="state_failure_"]').count() == 1  # the evidence capture
    spage.click("#lvmClose")
    assert not spage.is_visible("#lvTestBox")
