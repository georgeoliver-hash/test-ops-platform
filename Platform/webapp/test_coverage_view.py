"""Automation coverage metrics: counted from the two draft CSVs, nothing guessed."""
import csv

from Platform.webapp import coverage_view as cv


def _write(folder, mapping, audit):
    folder.mkdir(parents=True)
    with (folder / cv.MAPPING).open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["file", "test", "tid", "how_found", "candidate_case_ids", "candidate_titles", "approved_case_id"])
        w.writerows(mapping)
    with (folder / cv.AUDIT).open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["section", "cases", "ready", "linked_live_tests", "provisional_tests", "linked_kinds", "flag", "proposed_functional_smoke", "approve"])
        w.writerows(audit)


def test_missing_drafts_are_reported_not_invented(tmp_path):
    out = cv.coverage(tmp_path / "proposals", "Translink", "POS")
    assert out["available"] is False and "No coverage drafts" in out["reason"]


def test_counts_come_straight_from_the_files(tmp_path):
    _write(tmp_path / "proposals" / "Translink-POS-suite-restructure",
           [["a.robot", "t1", "POS-1", "explicit", "C1", "x", ""], ["a.robot", "t2", "POS-2", "title", "C2", "x", ""],
            ["a.robot", "t3", "POS-3", "similar", "C3", "x", ""], ["a.robot", "t4", "POS-4", "map-edge", "", "", ""],
            ["a.robot", "t5", "POS-5", "none", "", "", ""], ["a.robot", "t6", "POS-6", "none", "", "", "C99"]],
           [["Top > A", "4", "2", "0", "0", "", "ZERO", "C1 First", ""], ["Top > B", "3", "0", "1", "0", "functional", "OK", "", ""],
            ["Top > C", "2", "1", "0", "1", "", "PROVISIONAL", "C5 Fifth", ""]])
    out = cv.coverage(tmp_path / "proposals", "Translink", "POS")
    t = out["tests"]
    assert (t["total"], t["map_edge"], t["should_have_a_case"]) == (6, 1, 5)
    assert t["linked"] == 2 and t["approved_in_csv"] == 1            # one explicit + one approved row
    assert (t["title"], t["similar"], t["none"]) == (1, 1, 2)
    s = out["sections"]
    assert (s["total"], s["ZERO"], s["PROVISIONAL"], s["OK"], s["REACH_ONLY"]) == (3, 1, 1, 1, 0)


def test_gaps_are_listed_worst_first_then_by_ready_cases(tmp_path):
    _write(tmp_path / "proposals" / "Translink-POS-x", [],
           [["OK one", "1", "1", "1", "0", "functional", "OK", "", ""], ["Zero few", "1", "1", "0", "0", "", "ZERO", "C1 a", ""],
            ["Zero many", "5", "4", "0", "0", "", "ZERO", "C2 b", ""], ["Prov", "2", "2", "0", "1", "", "PROVISIONAL", "C3 c", ""]])
    names = [g["section"] for g in cv.coverage(tmp_path / "proposals", "Translink", "POS")["gaps"]]
    assert names == ["Zero many", "Zero few", "Prov", "OK one"]


def test_another_target_does_not_borrow_these_files(tmp_path):
    _write(tmp_path / "proposals" / "Translink-POS-x", [], [["S", "1", "0", "0", "0", "", "ZERO", "", ""]])
    assert cv.coverage(tmp_path / "proposals", "NJT", "ETM")["available"] is False
