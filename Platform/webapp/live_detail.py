"""Everything about ONE test in a sit run, for the Live page: its scenario (documentation), tags, the steps it took with their
arguments and results, the smartcard XML it presented, the log lines it produced, the files printed while it ran, and the
evidence the failure teardown captured. Read-only.

Sources, in order of richness:
  * Robot output.xml (a finished run or a downloaded artifact): the whole keyword tree, arguments and log messages.
  * the live listener's live-events.jsonl: what the listener emitted so far (test start with tags/doc, step events, log lines).
Nothing is invented: a section the source does not hold is returned empty and the UI says so.
"""
from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

MAX_ARG = 600
MAX_XML = 40_000
MAX_STEPS = 400
MAX_LOG = 600
LEVELS_SHOWN = ("INFO", "WARN", "ERROR", "FAIL")
CARD_KEYWORDS = re.compile(r"(smartcard|card).*(present)|present.*(smartcard|raw)", re.I)
TAG_GROUPS = ("area", "tid", "testrail", "kind", "op", "feature", "severity", "known_defect", "covers")


def _iso(s: str | None) -> float | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def group_tags(tags: list[str]) -> dict:
    """Tags split into the named ones (area=, tid=, ...) and the plain ones (Smoke, destructive, ...)."""
    named: dict[str, str] = {}
    plain: list[str] = []
    for t in tags:
        k, sep, v = t.partition("=")
        if sep and k.lower() in TAG_GROUPS:
            named[k.lower()] = v
        else:
            plain.append(t)
    return {"named": named, "plain": plain}


def _looks_like_xml(s: str) -> bool:
    s = (s or "").lstrip()
    return s.startswith("<") and len(s) > 20 and ">" in s


def _steps(test: ET.Element) -> tuple[list[dict], list[dict]]:
    """(steps, cards): the keyword tree up to depth 3, and every smartcard XML a keyword was given."""
    steps: list[dict] = []
    cards: list[dict] = []

    def walk(kw: ET.Element, depth: int, parent_log: list[str]):
        if len(steps) >= MAX_STEPS:
            return
        st = kw.find("status")
        args = [(a.text or "") for a in kw.findall("./arg")]
        name = kw.get("name") or kw.get("type") or "?"
        kind = (kw.get("type") or "KEYWORD").upper()
        shown = [a[:MAX_ARG] + ("…" if len(a) > MAX_ARG else "") if not _looks_like_xml(a) else f"<xml, {len(a)} chars>" for a in args]
        steps.append({"depth": depth, "name": name, "owner": kw.get("owner"), "kind": kind, "args": shown,
                      "status": st.get("status") if st is not None else "?", "elapsed": float(st.get("elapsed") or 0) if st is not None and (st.get("elapsed") or "").replace(".", "", 1).isdigit() else None})
        local_log = list(parent_log)
        for m in kw.findall("./msg"):
            if m.text:
                local_log.append(m.text.strip()[:200])
        if CARD_KEYWORDS.search(name) or any(_looks_like_xml(a) and "card" in a.lower()[:400] for a in args):
            for a in args:
                if _looks_like_xml(a):
                    cards.append({"step": name, "xml": a[:MAX_XML], "truncated": len(a) > MAX_XML, "status": steps[-1]["status"],
                                  "card": next((m for m in reversed(local_log) if re.search(r"present", m, re.I)), None)})
        if depth < 3:
            for child in kw.findall("./kw"):
                walk(child, depth + 1, local_log)

    for kw in test.findall("./kw"):
        walk(kw, 1, [])
    return steps, cards


def _log(test: ET.Element) -> list[dict]:
    out = []
    for m in test.iter("msg"):
        lvl = (m.get("level") or "INFO").upper()
        if lvl in LEVELS_SHOWN and m.text and m.text.strip():
            out.append({"level": lvl, "time": m.get("time"), "text": m.text.strip()[:500]})
            if len(out) >= MAX_LOG:
                break
    return out


def _find_test(path: Path, test_id: str | None, name: str | None):
    """The <test> element asked for (by id, else name), read with iterparse so a big output.xml is not held in memory."""
    stack: list[str] = []
    try:
        for ev, el in ET.iterparse(path, events=("start", "end")):
            if ev == "start" and el.tag == "suite":
                stack.append(el.get("name") or "")
            elif ev == "end" and el.tag == "suite":
                if stack:
                    stack.pop()
            elif ev == "end" and el.tag == "test":
                if (test_id and el.get("id") == test_id) or (not test_id and name and el.get("name") == name):
                    return el, ".".join(stack)
                el.clear()
    except ET.ParseError:
        pass
    return None, ""


def _evidence(results_dir: Path | None, test_name: str) -> list[dict]:
    """state_failure_<name>.png/.json (and start_/end_) written by the capture keywords, found beside the results."""
    if not results_dir or not results_dir.is_dir():
        return []
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", test_name)
    found = []
    for p in sorted(results_dir.rglob(f"state_*{safe}.*")):
        found.append({"name": p.name, "path": str(p), "kind": "image" if p.suffix.lower() in (".png", ".jpg") else "layout"})
    return found[:12]


def _printed(tickets_dir: Path | None, start: float | None, end: float | None, slack: float = 5.0) -> list[dict]:
    """Files that appeared in the ticket folder while this test ran (modified between its start and end, plus a little slack)."""
    if not tickets_dir or not tickets_dir.is_dir() or start is None or end is None:
        return []
    out = []
    for p in tickets_dir.rglob("*"):
        try:
            if p.is_file() and start - slack <= p.stat().st_mtime <= end + slack:
                text = p.read_bytes()[:6000].decode("utf-8", errors="replace")
                out.append({"name": p.name, "modified": p.stat().st_mtime, "text": text})
        except OSError:
            continue
    return sorted(out, key=lambda x: x["modified"])[:10]


def from_output_xml(path: Path, *, test_id: str | None = None, name: str | None = None, tickets_dir: Path | None = None) -> dict | None:
    el, suite = _find_test(path, test_id, name)
    if el is None:
        return None
    st = el.find("status")
    start = _iso(st.get("start") or st.get("starttime")) if st is not None else None
    elapsed = float(st.get("elapsed")) if st is not None and (st.get("elapsed") or "").replace(".", "", 1).isdigit() else None
    end = (start + elapsed) if start is not None and elapsed is not None else None
    steps, cards = _steps(el)
    tags = [t.text for t in el.findall("./tag") if t.text]
    doc = (el.findtext("doc") or "").strip()
    return {"source": "output.xml", "id": el.get("id"), "name": el.get("name"), "suite": suite, "status": st.get("status") if st is not None else "?",
            "message": ((st.text or "").strip()[:1500] if st is not None else ""), "seconds": elapsed, "start": start,
            "scenario": doc, "tags": group_tags(tags), "steps": steps, "cards": cards, "log": _log(el),
            "printed": _printed(tickets_dir, start, end), "evidence": _evidence(path.parent, el.get("name") or "")}


def from_events(path: Path, *, name: str, tickets_dir: Path | None = None) -> dict | None:
    """Detail from the live listener's events: what has arrived so far for this test."""
    tags: list[str] = []
    doc, status, message, start, end = "", "RUNNING", "", None, None
    steps: list[dict] = []
    cards: list[dict] = []
    log: list[dict] = []
    inside = False
    seen = False
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    for line in lines:
        try:
            e = json.loads(line)
        except ValueError:
            continue
        ev = e.get("ev")
        if ev == "test_start" and e.get("name") == name:
            inside, seen, start = True, True, e.get("t")
            tags, doc = e.get("tags") or [], e.get("doc") or ""
            steps, cards, log, status, message, end = [], [], [], "RUNNING", "", None
        elif ev == "test_end" and e.get("name") == name and inside:
            inside, status, message, end = False, e.get("status") or "?", e.get("message") or "", e.get("t")
            tags = e.get("tags") or tags
        elif inside and ev == "step_start":
            steps.append({"seq": e.get("seq"), "depth": e.get("depth", 1), "name": e.get("name"), "owner": e.get("owner"), "kind": e.get("kind", "KEYWORD"),
                          "args": e.get("args") or [], "status": "RUNNING", "elapsed": None})
            if e.get("card_xml"):
                cards.append({"seq": e.get("seq"), "step": e.get("name"), "xml": e["card_xml"][:MAX_XML], "truncated": len(e["card_xml"]) > MAX_XML,
                              "status": "RUNNING", "card": e.get("card")})
        elif inside and ev == "step_end":
            for coll in (steps, cards):
                for item in coll:
                    if item.get("seq") == e.get("seq"):
                        item["status"] = e.get("status") or "?"
                        if coll is steps:
                            item["elapsed"] = e.get("elapsed")
        elif inside and ev == "step":
            steps.append({"depth": e.get("depth", 1), "name": e.get("name"), "owner": e.get("owner"), "kind": e.get("kind", "KEYWORD"),
                          "args": e.get("args") or [], "status": e.get("status") or "RUNNING", "elapsed": e.get("elapsed")})
            if e.get("card_xml"):
                cards.append({"step": e.get("name"), "xml": e["card_xml"][:MAX_XML], "truncated": len(e["card_xml"]) > MAX_XML,
                              "status": e.get("status") or "RUNNING", "card": e.get("card")})
        elif inside and ev == "log" and e.get("level") in LEVELS_SHOWN:
            log.append({"level": e["level"], "time": e.get("t"), "text": (e.get("text") or "")[:500]})
    if not seen:
        return None
    return {"source": "live events", "id": None, "name": name, "suite": "", "status": status, "message": message[:1500],
            "seconds": (end - start) if (start and end) else None, "start": start, "scenario": doc, "tags": group_tags(tags), "steps": steps[:MAX_STEPS],
            "cards": cards, "log": log[:MAX_LOG], "printed": _printed(tickets_dir, start, end or (start or 0) + 600), "evidence": []}
