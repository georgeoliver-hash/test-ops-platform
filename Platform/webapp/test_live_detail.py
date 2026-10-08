"""One test in full: scenario, tags, steps with arguments, the card XML presented, the log, files printed meanwhile, evidence."""
import os
import time

import pytest

from Platform.webapp import live_detail as ld

CARD = "<SmartCard><Id>12345</Id><Type>Concession</Type><Expiry>2027-01-01</Expiry></SmartCard>"
XML = f"""<?xml version="1.0"?><robot generator="Robot 7.4.2"><suite name="POS" id="s1"><suite name="Flow" id="s1-s1">
<test id="s1-s1-t1" name="Present A Concession Card"><kw name="Show Screen" owner="Res"><arg>Idle</arg><status status="PASS" start="2026-10-08T10:00:00.000000" elapsed="1.5"/></kw>
 <kw name="Device: Smartcard: Present Card" owner="Device"><arg>{CARD.replace('<', '&lt;').replace('>', '&gt;')}</arg><arg>False</arg>
   <kw name="present raw smartcard" owner="Device"><arg>payload</arg><msg level="INFO" time="2026-10-08T10:00:03.000000">POST sent</msg><status status="PASS" start="2026-10-08T10:00:03.000000" elapsed="0.3"/></kw>
   <msg level="INFO" time="2026-10-08T10:00:02.500000">Presenting Concession card card_a.xml</msg><msg level="DEBUG" time="2026-10-08T10:00:02.600000">debug noise</msg>
   <status status="PASS" start="2026-10-08T10:00:02.000000" elapsed="1.0"/></kw>
 <kw name="POS: Assert On Screen" owner="Res"><arg>ConcessionAccepted</arg><msg level="FAIL" time="2026-10-08T10:00:05.000000">Expected ConcessionAccepted, got CardRejected</msg><status status="FAIL" start="2026-10-08T10:00:04.000000" elapsed="1.0"/></kw>
 <doc>Given a concession card is presented. Then the POS accepts it.</doc><tag>area=Smartcard</tag><tag>tid=POS-ABC123</tag><tag>testrail=C4111026</tag><tag>Smoke</tag><tag>kind=functional</tag>
 <status status="FAIL" start="2026-10-08T10:00:00.000000" elapsed="6.0">Expected ConcessionAccepted, got CardRejected</status></test>
<test id="s1-s1-t2" name="Other"><status status="PASS" start="2026-10-08T10:00:07.000000" elapsed="1.0"/></test></suite></suite></robot>"""


@pytest.fixture
def run(tmp_path):
    p = tmp_path / "output.xml"
    p.write_text(XML, encoding="utf-8")
    return p


def test_the_scenario_and_tags_are_split_into_named_and_plain(run):
    d = ld.from_output_xml(run, test_id="s1-s1-t1")
    assert d["scenario"].startswith("Given a concession card") and d["status"] == "FAIL" and d["suite"] == "POS.Flow"
    assert d["tags"]["named"] == {"area": "Smartcard", "tid": "POS-ABC123", "testrail": "C4111026", "kind": "functional"} and d["tags"]["plain"] == ["Smoke"]


def test_steps_show_arguments_nesting_and_results(run):
    d = ld.from_output_xml(run, test_id="s1-s1-t1")
    names = [(s["depth"], s["name"], s["status"]) for s in d["steps"]]
    assert names == [(1, "Show Screen", "PASS"), (1, "Device: Smartcard: Present Card", "PASS"), (2, "present raw smartcard", "PASS"), (1, "POS: Assert On Screen", "FAIL")]
    present = d["steps"][1]
    assert present["args"][0].startswith("<xml,") and present["args"][1] == "False"      # the XML itself is not stuffed into the step line


def test_the_card_xml_that_was_presented_is_kept_whole_with_its_card_name(run):
    d = ld.from_output_xml(run, test_id="s1-s1-t1")
    assert len(d["cards"]) == 1 and d["cards"][0]["xml"] == CARD and d["cards"][0]["status"] == "PASS"
    assert "Presenting Concession card card_a.xml" in d["cards"][0]["card"]


def test_the_log_has_the_useful_levels_only(run):
    d = ld.from_output_xml(run, test_id="s1-s1-t1")
    levels = {l["level"] for l in d["log"]}
    assert "FAIL" in levels and "INFO" in levels and "DEBUG" not in levels and all("debug noise" not in l["text"] for l in d["log"])


def test_a_test_is_found_by_name_and_a_missing_one_is_none(run):
    assert ld.from_output_xml(run, name="Other")["status"] == "PASS"
    assert ld.from_output_xml(run, test_id="nope") is None


def test_files_printed_while_the_test_ran_are_attached_and_others_are_not(run, tmp_path):
    tickets = tmp_path / "tickets"
    tickets.mkdir()
    start = ld._iso("2026-10-08T10:00:00.000000")
    during, long_before = tickets / "ticket_during.txt", tickets / "ticket_old.txt"
    during.write_text("ADULT SINGLE 3.10", encoding="utf-8")
    long_before.write_text("OLD", encoding="utf-8")
    os.utime(during, (start + 3, start + 3))
    os.utime(long_before, (start - 3600, start - 3600))
    d = ld.from_output_xml(run, test_id="s1-s1-t1", tickets_dir=tickets)
    assert [p["name"] for p in d["printed"]] == ["ticket_during.txt"] and "ADULT SINGLE" in d["printed"][0]["text"]


def test_evidence_captures_for_the_test_are_listed(run):
    (run.parent / "state_failure_Present_A_Concession_Card.png").write_bytes(b"png")
    (run.parent / "state_failure_Present_A_Concession_Card.json").write_text("{}", encoding="utf-8")
    (run.parent / "state_failure_Other.png").write_bytes(b"png")
    d = ld.from_output_xml(run, test_id="s1-s1-t1")
    assert sorted(e["name"] for e in d["evidence"]) == ["state_failure_Present_A_Concession_Card.json", "state_failure_Present_A_Concession_Card.png"]


def test_live_events_give_the_same_picture_as_far_as_they_have_arrived(tmp_path):
    import json
    ev = [{"ev": "test_start", "name": "T", "t": 100.0, "tags": ["area=X", "Smoke"], "doc": "Given X. Then Y."},
          {"ev": "step", "name": "Show Screen", "depth": 1, "args": ["Idle"], "status": "PASS"},
          {"ev": "step", "name": "Present Card", "depth": 1, "args": ["<xml, 40 chars>"], "status": "PASS", "card_xml": CARD, "card": "Presenting card a.xml"},
          {"ev": "log", "level": "INFO", "text": "hello", "t": 101.0}, {"ev": "log", "level": "DEBUG", "text": "noise", "t": 101.5}]
    p = tmp_path / "live-events.jsonl"
    p.write_text("\n".join(json.dumps(e) for e in ev) + "\n{half", encoding="utf-8")
    d = ld.from_events(p, name="T")
    assert d["status"] == "RUNNING" and d["scenario"].startswith("Given X") and d["cards"][0]["xml"] == CARD
    assert [s["name"] for s in d["steps"]] == ["Show Screen", "Present Card"] and [l["text"] for l in d["log"]] == ["hello"]
    assert ld.from_events(p, name="Nope") is None


def test_the_real_listener_emits_steps_cards_and_doc_that_the_reader_understands(tmp_path):
    """A real Robot run with tools/robot_live_listener.py, read back through from_events."""
    import shutil
    import subprocess
    import sys
    from pathlib import Path
    py = next((c for c in (sys.executable, shutil.which("python")) if c and subprocess.run([c, "-m", "robot", "--version"], capture_output=True).returncode in (0, 251)), None)
    if not py:
        pytest.skip("no Python with robotframework available")
    suite = tmp_path / "t.robot"
    suite.write_text(
        "*** Settings ***\nTest Tags    area=Card    Smoke\n\n*** Keywords ***\nDevice: Smartcard: Present Card\n    [Arguments]    ${xml}\n    Log    Presenting Concession card a.xml\n    Log    posted\n\n"
        "*** Test Cases ***\nPresents A Card\n    [Documentation]    Given a card. Then it works.\n    Log    start\n    Device: Smartcard: Present Card    <SmartCard><Id>7</Id><Type>Concession</Type></SmartCard>\n    Fail    nope\n",
        encoding="utf-8")
    events = tmp_path / "res" / "live-events.jsonl"
    listener = str(Path(__file__).resolve().parents[2] / "tools" / "robot_live_listener.py")
    subprocess.run([py, "-m", "robot", "--outputdir", str(tmp_path / "res"), "--listener", listener, str(suite)],
                   env={**__import__("os").environ, "TOPS_LIVE_EVENTS": str(events)}, capture_output=True, timeout=120)
    d = ld.from_events(events, name="Presents A Card")
    assert d["status"] == "FAIL" and d["scenario"] == "Given a card. Then it works." and d["tags"]["named"] == {"area": "Card"}
    names = [(s["depth"], s["name"], s["status"]) for s in d["steps"]]
    assert (1, "Device: Smartcard: Present Card", "PASS") in names and (1, "Fail", "FAIL") in names
    present = next(s for s in d["steps"] if s["name"] == "Device: Smartcard: Present Card")
    assert present["args"][0].startswith("<xml,") and present["elapsed"] is not None
    assert len(d["cards"]) == 1 and d["cards"][0]["xml"] == "<SmartCard><Id>7</Id><Type>Concession</Type></SmartCard>" and d["cards"][0]["status"] == "PASS"
    assert any("Presenting Concession card" in l["text"] for l in d["log"])
