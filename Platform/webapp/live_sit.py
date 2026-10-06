"""Real-time view of sit runs: Robot Framework output.xml (read WHILE the run is writing it) and the ticket print
records the device writes to a folder. Read-only: nothing here starts or changes a run.

Where the data comes from is a setting (data/live_sources.json): `results_dir` = a folder holding Robot output.xml
files (a local run's --outputdir, or a downloaded CI artifact), `tickets_dir` = the folder tickets print to
(sit's PrintJobRecordPath). Nothing is invented: with no folder set, or no files in it, the page says so.
"""
from __future__ import annotations

import json
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"
CONFIG = DATA / "live_sources.json"
MAX_RUNS = 25
MAX_TICKET_BYTES = 6000


def get_config() -> dict:
    try:
        return {"results_dir": "", "tickets_dir": "", **json.loads(CONFIG.read_text(encoding="utf-8"))}
    except (OSError, ValueError):
        return {"results_dir": "", "tickets_dir": ""}


def set_config(results_dir: str | None, tickets_dir: str | None) -> dict:
    cfg = get_config()
    for key, val in (("results_dir", results_dir), ("tickets_dir", tickets_dir)):
        if val is not None:
            val = val.strip()
            if val and not Path(val).is_dir():
                raise ValueError(f"{key}: '{val}' is not a folder on this machine.")
            cfg[key] = val
    DATA.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(json.dumps(cfg, indent=1), encoding="utf-8")
    return cfg


def _iso(ts: str | None) -> str | None:
    """Robot 7 writes ISO starts; Robot <=6 writes '20260101 12:00:00.123'. Return ISO or None."""
    if not ts:
        return None
    try:
        if " " in ts and "-" not in ts:
            return datetime.strptime(ts[:21], "%Y%m%d %H:%M:%S.%f").replace(tzinfo=timezone.utc).isoformat()
        return datetime.fromisoformat(ts).isoformat()
    except ValueError:
        return None


def _elapsed(st: ET.Element) -> float | None:
    if st.get("elapsed"):
        try:
            return float(st.get("elapsed"))
        except ValueError:
            return None
    a, b = _iso(st.get("starttime")), _iso(st.get("endtime"))
    if a and b:
        return (datetime.fromisoformat(b) - datetime.fromisoformat(a)).total_seconds()
    return None


def parse_output(path: Path) -> dict:
    """Parse a (possibly still-growing) output.xml. Tests that have finished come from <test> end events; the one
    that has started but not finished is `running`. A half-written tail is expected, not an error."""
    parser = ET.XMLPullParser(events=("start", "end"))
    tests, suites, running, last_msgs = [], [], None, []
    stack: list[str] = []
    depth_kw = 0
    complete = False
    try:
        with path.open("rb") as f:
            while chunk := f.read(1 << 20):
                parser.feed(chunk)
                for ev, el in parser.read_events():
                    tag = el.tag
                    if ev == "start":
                        if tag == "suite":
                            stack.append(el.get("name") or "")
                        elif tag == "test":
                            running = {"name": el.get("name"), "suite": ".".join(stack), "id": el.get("id")}
                        elif tag == "kw":
                            depth_kw += 1
                    else:
                        if tag == "kw":
                            depth_kw -= 1
                        elif tag == "msg" and el.text:
                            last_msgs.append({"level": el.get("level") or "INFO", "text": el.text.strip()[:400],
                                              "time": _iso(el.get("time") or el.get("timestamp"))})
                            del last_msgs[:-40]
                        elif tag == "test":
                            st = el.find("status")
                            tags = [t.text for t in el.findall("./tag") if t.text] or [t.text for t in el.findall("./tags/tag") if t.text]
                            tests.append({"name": el.get("name"), "suite": ".".join(stack), "id": el.get("id"),
                                          "status": (st.get("status") if st is not None else "?"),
                                          "start": _iso(st.get("start") or st.get("starttime")) if st is not None else None,
                                          "seconds": _elapsed(st) if st is not None else None,
                                          "message": ((st.text or "").strip()[:400] if st is not None else ""), "tags": tags})
                            running = None
                            el.clear()
                        elif tag == "suite":
                            if stack:
                                stack.pop()
                        elif tag == "robot":
                            complete = True
    except ET.ParseError:
        pass  # run still writing: everything parsed so far stands
    counts = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    for t in tests:
        counts[t["status"]] = counts.get(t["status"], 0) + 1
    return {"tests": tests, "running": None if complete else running, "complete": complete, "counts": counts,
            "log": last_msgs[-25:]}


def parse_events(path: Path) -> dict:
    """Read the JSONL tools/robot_live_listener.py appends: real time, unlike Robot's buffered output.xml."""
    tests, running, log, complete, total, started = [], None, [], False, None, None
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        lines = []
    for line in lines:
        try:
            e = json.loads(line)
        except ValueError:
            continue  # a half-written last line is expected
        ev = e.get("ev")
        if ev == "run_start":
            started = e["t"]
        elif ev == "suite_start":
            total = e.get("total") or total
        elif ev == "test_start":
            running = {"name": e["name"], "suite": e.get("suite"), "start": e["t"]}
        elif ev == "test_end":
            tests.append({"name": e["name"], "suite": e.get("suite"), "status": e.get("status"), "seconds": e.get("seconds"),
                          "message": e.get("message") or "", "tags": e.get("tags") or [], "start": None})
            running = None
        elif ev == "log":
            log.append({"level": e.get("level"), "text": e.get("text"), "time": None})
        elif ev == "run_end":
            complete, running = True, None
    counts = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    for t in tests:
        counts[t["status"]] = counts.get(t["status"], 0) + 1
    return {"tests": tests, "running": running, "complete": complete, "counts": counts, "log": log[-25:], "total": total, "started": started}


def _parse(p: Path) -> dict:
    return parse_events(p) if p.suffix == ".jsonl" else parse_output(p)


def _safe_under(root: str, p: Path) -> bool:
    try:
        p.resolve().relative_to(Path(root).resolve())
        return True
    except (ValueError, OSError):
        return False


def list_runs() -> dict:
    root = get_config()["results_dir"]
    if not root or not Path(root).is_dir():
        return {"configured": False, "runs": []}
    files = []
    for p in [*Path(root).rglob("output*.xml"), *Path(root).rglob("*.jsonl")]:
        try:
            files.append((p.stat().st_mtime, p))
        except OSError:
            continue
    files.sort(reverse=True)
    # one run = one row: when a folder has both the live listener file and Robot's output.xml, show the live one
    jsonl_dirs = {p.parent for _, p in files if p.suffix == ".jsonl"}
    files = [(m, p) for m, p in files if not (p.suffix == ".xml" and p.parent in jsonl_dirs)]
    now = time.time()
    runs = []
    for mtime, p in files[:MAX_RUNS]:
        info = _parse(p)
        c = info["counts"]
        runs.append({"path": str(p), "name": p.parent.name if (p.name == "output.xml" or p.suffix == ".jsonl") else p.stem, "kind": "live" if p.suffix == ".jsonl" else "xml", "modified": mtime,
                     "live": (not info["complete"]) and now - mtime < 600, "complete": info["complete"],
                     "total": len(info["tests"]), "passed": c.get("PASS", 0), "failed": c.get("FAIL", 0), "skipped": c.get("SKIP", 0),
                     "running": info["running"]["name"] if info["running"] else None})
    return {"configured": True, "results_dir": root, "runs": runs}


def run_detail(path: str) -> dict:
    cfg = get_config()
    p = Path(path)
    if not cfg["results_dir"] or not _safe_under(cfg["results_dir"], p) or not p.is_file():
        raise FileNotFoundError("That run is not inside the configured results folder.")
    info = _parse(p)
    info["path"], info["modified"] = str(p), p.stat().st_mtime
    info["live"] = (not info["complete"]) and time.time() - info["modified"] < 600
    return info


def tickets(limit: int = 25) -> dict:
    root = get_config()["tickets_dir"]
    if not root or not Path(root).is_dir():
        return {"configured": False, "tickets": []}
    files = []
    for p in Path(root).rglob("*"):
        try:
            if p.is_file():
                files.append((p.stat().st_mtime, p))
        except OSError:
            continue
    files.sort(reverse=True)
    out = []
    for mtime, p in files[:limit]:
        try:
            raw = p.read_bytes()[:MAX_TICKET_BYTES]
            text = raw.decode("utf-8", errors="replace")
        except OSError:
            continue
        out.append({"name": p.name, "modified": mtime, "text": text})
    return {"configured": True, "tickets_dir": root, "tickets": out}
