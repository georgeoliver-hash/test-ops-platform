"""Gaps list + group-gaps: each marker carries its group, other-device gaps leave a POS list, counts per group."""
from __future__ import annotations

import json
import os
import tempfile

os.environ.setdefault("TESTOPS_WEBAPP_DATA_DIR", tempfile.mkdtemp(prefix="testops-webapp-test-"))

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from Platform.webapp import app as app_mod, runner  # noqa: E402

client = TestClient(app_mod.app)
POS_FILE = "knowledge/translink/specs/POS-FS-x.md"


def _marker(line, text="q"):
    return {"file": POS_FILE, "line": line, "kind": "GAP", "text": text}


@pytest.fixture
def env(tmp_path, monkeypatch):
    fixtures = tmp_path / "fx"
    fixtures.mkdir()
    (fixtures / "gaps.json").write_text(json.dumps([_marker(1), _marker(2), _marker(3), _marker(4)]), encoding="utf-8")
    monkeypatch.setattr(app_mod, "FIXTURES", fixtures)
    monkeypatch.setattr(runner, "SYSTEM_TEST_OPS_ROOT", tmp_path)
    d = tmp_path / "reports" / "translink" / "clarify-gaps"
    d.mkdir(parents=True)

    def groups(rows):
        (d / "gap-groups.expanded.json").write_text(json.dumps(rows), encoding="utf-8")
    return groups


def _g(line, cat, devices=("POS",)):
    return {"file": POS_FILE, "line": line, "category": cat, "devices": list(devices), "evidence": "e", "spec_ref": None}


def test_markers_carry_their_group_and_counts_are_reported(env):
    env([_g(1, "screen"), _g(2, "screen"), _g(3, "behaviour")])
    r = client.get("/api/gap-register", params={"project": "translink", "device": "POS", "limit": 50}).json()
    assert r["grouped"] is True
    assert r["category_counts"] == {"screen": 2, "behaviour": 1, "unclassified": 1}
    assert {m["line"]: m["category"] for m in r["shown"]} == {1: "screen", 2: "screen", 3: "behaviour", 4: None}


def test_a_gap_that_only_concerns_another_device_is_hidden_from_the_pos_list_and_counted(env):
    env([_g(1, "screen"), _g(2, "other-device", ["ETM"]), _g(3, "value", ["ETM", "PV"]), _g(4, "behaviour", ["ALL"])])
    r = client.get("/api/gap-register", params={"project": "translink", "device": "POS", "limit": 50}).json()
    assert [m["line"] for m in r["shown"]] == [1, 4]
    assert r["hidden_other_device"] == 2 and r["category_counts"] == {"screen": 1, "behaviour": 1}


def test_filtering_by_group_and_no_classification_yet(env):
    env([_g(1, "screen"), _g(2, "behaviour"), _g(3, "behaviour"), _g(4, "conflict")])
    r = client.get("/api/gap-register", params={"project": "translink", "device": "POS", "category": "behaviour"}).json()
    assert [m["line"] for m in r["shown"]] == [2, 3] and r["total"] == 2
    assert r["category_counts"]["screen"] == 1  # counts still describe the whole scope, not just the filter


def test_works_unchanged_when_nothing_has_been_grouped_yet(env):
    r = client.get("/api/gap-register", params={"project": "translink", "device": "POS", "limit": 50}).json()
    assert r["grouped"] is False and r["hidden_other_device"] == 0 and len(r["shown"]) == 4


# ---- export / import of answers --------------------------------------------------------------

from Platform.webapp import gap_exchange, store  # noqa: E402

HEAD = "Gap ID,Also answers (Gap IDs),Group,Devices,Summary of the issue,Question to answer,Spec reference,Where it appears,Verdict,Answer,Answered by,Evidence or notes"


def _inputs(env_root):
    d = env_root / "reports" / "translink" / "clarify-gaps"
    (d / "gap-inputs.json").write_text(json.dumps([
        {"id": "G-AAAA1111", "key": f"{POS_FILE}:1", "kind": "GAP", "text": "banner never triggered", "plain_english": "Is the banner ever shown?", "occurrences": [f"{POS_FILE}:1"]},
        {"id": "G-BBBB2222", "key": f"{POS_FILE}:2", "kind": "GAP", "text": "design vs as-built", "plain_english": "", "occurrences": [f"{POS_FILE}:2"]},
    ]), encoding="utf-8")
    return d


def _row(gid, verdict="", answer="", by="", notes="", q="q?", also=""):
    import csv
    import io
    buf = io.StringIO()
    csv.writer(buf, lineterminator="").writerow([gid, also, "g", "POS", "s", q, "", "", verdict, answer, by, notes])  # quotes commas like Excel does
    return buf.getvalue()


def test_import_records_answered_rows_by_gap_id_and_logs_a_verdict_as_a_conflict_not_an_answer(env, tmp_path):
    _inputs(tmp_path)
    proj = f"Translink-{os.urandom(2).hex()}"
    # the answers log is keyed by the project name the Gaps page uses; reports live under its lower-case form
    csv_text = "\n".join([HEAD,
        _row("G-AAAA1111", "Mismatch (raise it)", "Device shows green, spec says orange", "Sam", "run 42"),
        _row("G-BBBB2222", "", "Design is intended", "Priya"),
        _row("G-AAAA1111"),                                  # blank: nothing to import
        _row("G-ZZZZ9999", "", "x", "Sam"),                   # not a gap we know
        _row("G-BBBB2222", "Perhaps", "y", "Sam"),            # bad verdict
        _row("G-BBBB2222", "", "no name given", "")])         # no 'Answered by' and no default
    r = gap_exchange.import_csv("translink", "POS", csv_text, default_by=None)
    assert (r["imported"], r["blank"], r["conflicts"]) == (2, 1, 1)
    assert r["unknown_ids"] == ["G-ZZZZ9999"] and len(r["errors"]) == 2
    log = {a["gap_ref"].split()[0]: a for a in store.list_gap_answers("translink")}
    assert log["G-AAAA1111"]["entry_type"] == "conflict" and "Mismatch" in log["G-AAAA1111"]["answer"] and "run 42" in log["G-AAAA1111"]["answer"]
    assert log["G-BBBB2222"]["entry_type"] == "answer" and log["G-BBBB2222"]["answered_by"] == "Priya"


def test_importing_the_same_sheet_twice_adds_nothing_new_and_a_default_name_fills_blanks(env, tmp_path):
    _inputs(tmp_path)
    csv_text = "\n".join([HEAD, _row("G-AAAA1111", "Needs a decision", "owner to say", "")])
    first = gap_exchange.import_csv("translink", "POS", csv_text, default_by="George")
    again = gap_exchange.import_csv("translink", "POS", csv_text, default_by="George")
    assert first["imported"] == 1 and first["decisions"] == 1
    assert again["imported"] == 0 and again["duplicates"] == 1


def test_export_and_import_say_plainly_when_the_gaps_have_not_been_grouped(env):
    r = client.get("/api/gap-export", params={"project": "translink", "device": "POS"})
    assert r.status_code == 409 and "Group gaps" in r.json()["detail"]
    r = client.post("/api/gap-import", params={"project": "translink"}, json={"csv_text": HEAD})
    assert r.status_code == 409


def test_an_answer_on_a_merged_row_is_recorded_against_every_id_it_covers(env, tmp_path):
    _inputs(tmp_path)
    csv_text = chr(10).join([HEAD, _row("G-AAAA1111", "", "Yes, it appears", "Sam", also="G-BBBB2222, G-NOPE0000")])
    r = gap_exchange.import_csv("translink", "POS", csv_text, default_by=None)
    assert r["imported"] == 2 and r["unknown_ids"] == ["G-NOPE0000"]
    refs = {a["gap_ref"].split()[0] for a in store.list_gap_answers("translink") if a["answer"] == "Yes, it appears"}
    assert refs == {"G-AAAA1111", "G-BBBB2222"}


def test_a_drafted_sheet_is_imported_as_drafts_and_duplicates_and_out_of_scope_rows_are_skipped(env, tmp_path):
    _inputs(tmp_path)
    csv_text = chr(10).join([HEAD,
        _row("G-AAAA1111", "Answered from code", "Yes, but only after a forced sign-off", "Claude (draft - review before use)", "DEFECTS.md D-49"),
        _row("G-BBBB2222", "Needs confirmation", "Probably; needs a device check", "Claude (draft - review before use)"),
        _row("G-AAAA1111", "Duplicate", "Same as G-BBBB2222", "Claude (draft - review before use)"),
        _row("G-ZZZZ9999", "Out of scope - not POS", "ETM only", "Claude (draft - review before use)"),
        _row("G-BBBB2222", "Not a gap", "A note about the marker convention", "Claude (draft - review before use)"),
        _row("G-AAAA1111", "Answered", "Shown on the Idle page", "Claude (draft - review before use)")])
    r = gap_exchange.import_csv("translink", "POS", csv_text, default_by=None)
    assert (r["imported"], r["drafts"], r["skipped_duplicate_or_out_of_scope"], r["errors"], r["unknown_ids"]) == (3, 3, 3, [], [])
    log = store.list_gap_answers("translink")
    texts = {a["answer"] for a in log}
    assert any(t.startswith("[DRAFT from code - not seen on a device] Yes, but only after a forced sign-off [Evidence: DEFECTS.md D-49]") for t in texts)
    assert any(t.startswith("[DRAFT - needs confirmation] ") for t in texts) and any(t.startswith("[DRAFT - review before use] ") for t in texts)
    types = {a["entry_type"] for a in log if a["answer"].startswith("[DRAFT - needs")}
    assert types == {"clarification_request"}
