import json

from Platform.webapp import live_sit


def _cfg(tmp_path, monkeypatch, results=True, tickets=True):
    monkeypatch.setattr(live_sit, "DATA", tmp_path)
    monkeypatch.setattr(live_sit, "CONFIG", tmp_path / "live_sources.json")
    r, t = tmp_path / "res", tmp_path / "tix"
    r.mkdir(); t.mkdir()
    live_sit.set_config(str(r) if results else "", str(t) if tickets else "")
    return r, t


def _events(path, *evs):
    path.write_text("\n".join(json.dumps(e) for e in evs) + "\n", encoding="utf-8")


def test_nothing_configured_says_so(tmp_path, monkeypatch):
    monkeypatch.setattr(live_sit, "CONFIG", tmp_path / "none.json")
    assert live_sit.list_runs() == {"configured": False, "runs": []}
    assert live_sit.tickets()["configured"] is False


def test_a_missing_folder_is_refused(tmp_path, monkeypatch):
    monkeypatch.setattr(live_sit, "DATA", tmp_path)
    monkeypatch.setattr(live_sit, "CONFIG", tmp_path / "c.json")
    try:
        live_sit.set_config(str(tmp_path / "nope"), None)
        assert False, "should refuse"
    except ValueError as e:
        assert "not a folder" in str(e)


def test_live_events_count_pass_fail_skip_and_show_the_running_test(tmp_path, monkeypatch):
    r, _ = _cfg(tmp_path, monkeypatch)
    f = r / "run1" / "live-events.jsonl"
    f.parent.mkdir()
    _events(f, {"ev": "run_start", "t": 1}, {"ev": "suite_start", "name": "S", "total": 4, "t": 1},
            {"ev": "test_start", "name": "a", "suite": "S", "t": 2}, {"ev": "test_end", "name": "a", "suite": "S", "status": "PASS", "seconds": 1.0},
            {"ev": "test_start", "name": "b", "suite": "S", "t": 3}, {"ev": "test_end", "name": "b", "suite": "S", "status": "FAIL", "seconds": 2.0, "message": "boom"},
            {"ev": "test_start", "name": "c", "suite": "S", "t": 4})
    d = live_sit.run_detail(str(f))
    assert d["counts"] == {"PASS": 1, "FAIL": 1, "SKIP": 0} and d["total"] == 4
    assert d["running"]["name"] == "c" and not d["complete"] and d["live"]
    assert d["tests"][1]["message"] == "boom"
    with f.open("a", encoding="utf-8") as fh:
        fh.write('{"ev": "test_end", "name": "c", "status": "SKIP"}\n{"ev": "run_end"}\n{"ev": "tes')  # half-written last line
    d = live_sit.run_detail(str(f))
    assert d["complete"] and d["running"] is None and d["counts"]["SKIP"] == 1


def test_a_run_with_both_files_is_one_row_and_paths_outside_the_folder_are_refused(tmp_path, monkeypatch):
    r, _ = _cfg(tmp_path, monkeypatch)
    (r / "run").mkdir()
    _events(r / "run" / "live-events.jsonl", {"ev": "run_start", "t": 1}, {"ev": "run_end", "t": 2})
    (r / "run" / "output.xml").write_text("<robot></robot>", encoding="utf-8")
    runs = live_sit.list_runs()["runs"]
    assert len(runs) == 1 and runs[0]["kind"] == "live" and runs[0]["name"] == "run"
    try:
        live_sit.run_detail(str(tmp_path / "live_sources.json"))
        assert False, "should refuse"
    except FileNotFoundError:
        pass


def test_output_xml_that_is_cut_off_still_yields_the_finished_tests(tmp_path, monkeypatch):
    r, _ = _cfg(tmp_path, monkeypatch)
    x = r / "output.xml"
    x.write_text('<robot><suite name="S"><test id="s1-t1" name="a"><status status="PASS" elapsed="1.5"/></test><test id="s1-t2" name="b"><kw name="x">', encoding="utf-8")
    d = live_sit.run_detail(str(x))
    assert [t["name"] for t in d["tests"]] == ["a"] and d["tests"][0]["seconds"] == 1.5 and not d["complete"]


def test_tickets_newest_first(tmp_path, monkeypatch):
    import os
    _, t = _cfg(tmp_path, monkeypatch)
    (t / "old.txt").write_text("OLD", encoding="utf-8")
    (t / "new.txt").write_text("NEW", encoding="utf-8")
    os.utime(t / "old.txt", (1000, 1000))
    out = live_sit.tickets()
    assert out["configured"] and [x["name"] for x in out["tickets"]] == ["new.txt", "old.txt"] and out["tickets"][0]["text"] == "NEW"
