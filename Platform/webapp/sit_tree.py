"""The real sit test tree for one project/device, read straight from the local sit checkout (George, 2026-10-09:
"how is this true to the SIT framework, how is this staying up to date?" and "a TREE of structured tests, and how
many tests are currently done in each area -- how many smoke, operator, area tests").

Read-only. Parses `Tests/<folder>/**/*.robot` for test names and tags (suite-level `Test Tags`/`Force Tags` plus each
test's `[Tags]`, with `...` continuation lines). Nothing is cached or guessed: every number is counted from the files
on disk now, and the checkout's own branch/commit/date is returned so the page can say exactly how current it is.
"""
from __future__ import annotations

import os
import re
import subprocess
from collections import Counter
from pathlib import Path

_DEFAULT_ROOT = Path(__file__).resolve().parents[3] / "sit"

_SECTION = re.compile(r"^\*\*\*\s*([A-Za-z ]+?)\s*\*\*\*")
_SPLIT = re.compile(r"\s{2,}|\t+")
# Tag families shown as their own breakdowns; everything else is counted under "other".
FAMILIES = ("area", "kind", "mode", "impl", "triage", "feature")
FLAGS = {"smoke": "Smoke", "bvt": "BVT", "destructive": "destructive", "stub": "generated-stub", "unverified": "unverified"}


def sit_root() -> Path:
    return Path(os.environ.get("TESTOPS_SIT_ROOT") or _DEFAULT_ROOT)


# sit folders that do not follow Tests/<project>/<device>. Checked 2026-10-09: Translink POS lives at Tests/POS. A bare
# device folder is NOT a safe guess -- Tests/ETM holds NJT's legacy farebox tests, not Translink ETM's.
SIT_FOLDERS = {("translink", "pos"): "POS"}


def _folder_for(root: Path, project: str, device: str) -> Path | None:
    tests = root / "Tests"
    for name in (p.name for p in tests.iterdir() if p.is_dir()) if tests.is_dir() else ():
        if name.lower() == project.lower():
            for sub in (tests / name).iterdir():
                if sub.is_dir() and sub.name.lower() == device.lower():
                    return sub
    mapped = SIT_FOLDERS.get((project.lower(), device.lower()))
    return tests / mapped if mapped and (tests / mapped).is_dir() else None


def _cells(line: str) -> list[str]:
    return [c for c in _SPLIT.split(line.strip()) if c]


def parse_file(path: Path) -> list[dict]:
    """Tests in one .robot file: [{name, tags}]. Suite-level Test/Force/Default Tags apply to every test."""
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    section, suite_tags, tests = "", [], []
    last_key = None  # which setting a `...` continuation belongs to
    for raw in lines:
        m = _SECTION.match(raw)
        if m:
            section, last_key = m.group(1).strip().lower(), None
            continue
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if section == "settings":
            cells = _cells(raw)
            if cells[0] == "...":
                if last_key == "tags":
                    suite_tags += cells[1:]
                continue
            last_key = "tags" if cells[0].lower() in ("test tags", "force tags", "default tags") else None
            if last_key:
                suite_tags += cells[1:]
        elif section in ("test cases", "tasks"):
            if not raw[0].isspace():
                tests.append({"name": raw.strip(), "tags": []})
                last_key = None
                continue
            if not tests:
                continue
            cells = _cells(raw)
            if cells[0].lower() == "[tags]":
                tests[-1]["tags"] += cells[1:]
                last_key = "tags"
            elif cells[0] == "..." and last_key == "tags":
                tests[-1]["tags"] += cells[1:]
            else:
                last_key = None
    for t in tests:
        t["tags"] = list(dict.fromkeys(suite_tags + t["tags"]))
    return tests


def _git(root: Path, *args: str) -> str:
    try:
        return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, timeout=10).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def _summarise(tests: list[dict]) -> dict:
    fam = {f: Counter() for f in FAMILIES}
    flags = Counter()
    linked = 0
    for t in tests:
        low = {x.lower() for x in t["tags"]}
        for key, tag in FLAGS.items():
            if tag.lower() in low:
                flags[key] += 1
        if any(x.lower().startswith(("testrail=", "testrailid=")) for x in t["tags"]):
            linked += 1
        seen = set()
        for x in t["tags"]:
            if "=" in x:
                k, v = x.split("=", 1)
                if k.lower() in fam and v and (k.lower(), v) not in seen:
                    seen.add((k.lower(), v))
                    fam[k.lower()][v] += 1
    return {"total": len(tests), "flags": dict(flags), "testrail_linked": linked,
            "families": {f: dict(c.most_common()) for f, c in fam.items() if c}}


def tree(project: str, device: str, root: Path | None = None) -> dict:
    root = root or sit_root()
    if not (root / "Tests").is_dir():
        return {"available": False, "reason": f"No sit checkout found at {root} (set TESTOPS_SIT_ROOT)."}
    folder = _folder_for(root, project, device)
    if folder is None:
        return {"available": False, "reason": f"sit has no Tests folder for {project}/{device} yet."}
    nodes: dict[str, dict] = {}
    live, backlog = [], []
    for f in sorted(folder.rglob("*.robot")):
        rel = f.relative_to(folder)
        if any(p.startswith("__") for p in rel.parts):
            continue
        tests = parse_file(f)
        if not tests:
            continue
        is_backlog = rel.parts[0].startswith("_")
        (backlog if is_backlog else live).extend(tests)
        if is_backlog:
            continue
        parts = rel.parent.parts or (".",)
        for i in range(1, len(parts) + 1):
            key = "/".join(parts[:i])
            n = nodes.setdefault(key, {"path": key, "name": parts[i - 1], "depth": i - 1, "tests": []})
            n["tests"].extend(tests)
    out_nodes = []
    for key in sorted(nodes):
        n = nodes[key]
        s = _summarise(n["tests"])
        out_nodes.append({"path": n["path"], "name": n["name"], "depth": n["depth"], "total": s["total"], "flags": s["flags"],
                          "impl": s["families"].get("impl", {}), "modes": s["families"].get("mode", {})})
    return {
        "available": True, "project": project, "device": device,
        "folder": str(folder.relative_to(root)).replace("\\", "/"),
        "git": {"branch": _git(root, "branch", "--show-current"), "sha": _git(root, "rev-parse", "--short", "HEAD"),
                "date": _git(root, "log", "-1", "--format=%cI"), "subject": _git(root, "log", "-1", "--format=%s")},
        "summary": _summarise(live), "backlog": len(backlog), "nodes": out_nodes,
    }
