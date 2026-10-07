"""Real-time view of sit runs: Robot Framework output.xml (read WHILE the run is writing it) and the ticket print
records the device writes to a folder. Read-only: nothing here starts or changes a run.

Where the data comes from is a setting (data/live_sources.json): `results_dir` = a folder holding Robot output.xml
files (a local run's --outputdir, or a downloaded CI artifact), `tickets_dir` = the folder tickets print to
(sit's PrintJobRecordPath). Nothing is invented: with no folder set, or no files in it, the page says so.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

# Honours the same override as store.py so tests/e2e never touch the real console data.
DATA = Path(os.environ.get("TESTOPS_WEBAPP_DATA_DIR") or (Path(__file__).resolve().parent / "data"))
CONFIG = DATA / "live_sources.json"
MAX_RUNS = 25
GH_REPO = "flowbird-group/sit"
GH_WORKFLOW = "trigger-pipeline.yml"
PUSH_DIR = DATA / "live" / "pushed"      # events POSTed by a runner (see ingest), one folder per run id
MAX_PUSH_BATCH_BYTES = 1_000_000
MAX_PUSH_RUN_BYTES = 50_000_000
GH_CACHE = DATA / "live" / "gh"          # downloaded "robot-results-*" artifacts, one folder per Actions run id
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


def _robot_xmls(root: str) -> list[Path]:
    """Robot result files, found by content (CI names them '<suite>-<id>.xml', local runs 'output.xml')."""
    out = []
    for p in Path(root).rglob("*.xml"):
        try:
            with p.open("rb") as f:
                if b"<robot" in f.read(600):
                    out.append(p)
        except OSError:
            continue
    return out


def _roots() -> list[str]:
    cfg = get_config()
    return [r for r in (cfg["results_dir"], str(GH_CACHE), str(PUSH_DIR)) if r and Path(r).is_dir()]


def _safe_under(root: str, p: Path) -> bool:
    try:
        p.resolve().relative_to(Path(root).resolve())
        return True
    except (ValueError, OSError):
        return False


def list_runs() -> dict:
    roots = _roots()
    root = get_config()["results_dir"]
    if not roots:
        return {"configured": False, "runs": []}
    files = []
    for r in roots:
        for p in [*_robot_xmls(r), *Path(r).rglob("*.jsonl")]:
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
        gh = _gh_label(p)
        runs.append({"path": str(p), "name": gh or (p.parent.name if (p.name == "output.xml" or p.suffix == ".jsonl") else p.stem), "source": "github" if gh else "local", "kind": "live" if p.suffix == ".jsonl" else "xml", "modified": mtime,
                     "live": (not info["complete"]) and now - mtime < 600, "complete": info["complete"],
                     "total": len(info["tests"]), "passed": c.get("PASS", 0), "failed": c.get("FAIL", 0), "skipped": c.get("SKIP", 0),
                     "running": info["running"]["name"] if info["running"] else None})
    return {"configured": bool(root) or bool(runs), "results_dir": root, "runs": runs}


def run_detail(path: str) -> dict:
    p = Path(path)
    if not any(_safe_under(r, p) for r in _roots()) or not p.is_file():
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


# ---- GitHub Actions source: sit's own runs (self-hosted lab runners) upload their Robot results as an artifact ----
def _gh_label(p: Path) -> str | None:
    try:
        rel = p.resolve().relative_to(PUSH_DIR.resolve())
        return f"Pushed {rel.parts[0]}"
    except (ValueError, OSError):
        pass
    try:
        rel = p.resolve().relative_to(GH_CACHE.resolve())
    except (ValueError, OSError):
        return None
    parts = rel.parts
    return f"GitHub {parts[1].removeprefix('robot-results-')}" if len(parts) > 2 else f"GitHub run {parts[0]}"


def _gh(args: list[str], timeout: int = 180) -> tuple[int, str]:
    try:
        r = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return 127, "The GitHub CLI (gh) is not installed on this machine."
    except subprocess.TimeoutExpired:
        return 124, f"Timed out after {timeout}s."
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def gh_runs(limit: int = 20) -> dict:
    rc, out = _gh(["run", "list", "-R", GH_REPO, "--workflow", GH_WORKFLOW, "-L", str(max(1, min(limit, 50))),
                   "--json", "databaseId,displayTitle,status,conclusion,createdAt,event,url"], timeout=60)
    if rc != 0:
        return {"ok": False, "detail": out.strip().splitlines()[-1] if out.strip() else "gh failed"}
    cached = {p.name for p in GH_CACHE.iterdir()} if GH_CACHE.is_dir() else set()
    runs = json.loads(out)
    for r in runs:
        r["loaded"] = str(r["databaseId"]) in cached
    return {"ok": True, "repo": GH_REPO, "runs": runs}


def gh_load(run_id: str) -> dict:
    """Download the run's robot-results artifact(s) into the cache and return the output.xml files found."""
    if not re.fullmatch(r"\d{5,15}", run_id or ""):
        raise ValueError("That is not a GitHub run id.")
    dest = GH_CACHE / run_id
    if dest.is_dir() and _robot_xmls(str(dest)):
        pass  # already downloaded: runs that have finished do not change
    else:
        dest.mkdir(parents=True, exist_ok=True)
        rc, out = _gh(["run", "download", run_id, "-R", GH_REPO, "-p", "robot-results-*", "-D", str(dest)])
        if rc != 0 or not _robot_xmls(str(dest)):
            shutil.rmtree(dest, ignore_errors=True)
            msg = out.strip().splitlines()[-1] if out.strip() else "no output"
            raise FileNotFoundError(f"No Robot results for run {run_id}: {msg}. The run may still be going, may not have produced results, or the artifact has expired.")
    return {"run_id": run_id, "files": [str(p) for p in sorted(_robot_xmls(str(dest)))]}


# ---- Push transport: a lab runner POSTs its listener events to the console (no shared folder needed) ----
TOKEN_FILE = DATA / "live_token"


def push_token() -> str:
    """Shared secret the runner sends. TOPS_LIVE_TOKEN wins; otherwise one is generated once and kept in data/."""
    env = os.environ.get("TOPS_LIVE_TOKEN")
    if env:
        return env
    try:
        tok = TOKEN_FILE.read_text(encoding="utf-8").strip()
        if tok:
            return tok
    except OSError:
        pass
    import secrets
    tok = secrets.token_urlsafe(24)
    DATA.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(tok, encoding="utf-8")
    return tok


def ingest(run_id: str, events: list[dict], token: str | None) -> dict:
    import hmac
    if not token or not hmac.compare_digest(token, push_token()):
        raise PermissionError("bad or missing live token")
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", run_id or "").strip("-.")[:80]
    if not safe:
        raise ValueError("run_id is required (letters, digits, . _ -).")
    lines = []
    for e in events:
        if isinstance(e, dict) and isinstance(e.get("ev"), str):
            lines.append(json.dumps(e, ensure_ascii=False))
    body = ("\n".join(lines) + "\n").encode("utf-8") if lines else b""
    if len(body) > MAX_PUSH_BATCH_BYTES:
        raise ValueError("batch too large")
    folder = PUSH_DIR / safe
    folder.mkdir(parents=True, exist_ok=True)
    f = folder / "live-events.jsonl"
    if f.exists() and f.stat().st_size + len(body) > MAX_PUSH_RUN_BYTES:
        raise ValueError("run is over its size cap")
    if body:
        with f.open("ab") as fh:
            fh.write(body)
    return {"ok": True, "accepted": len(lines)}
