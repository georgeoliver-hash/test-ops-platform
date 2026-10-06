"""Quick, narrowed-down reports for the Reports page. Read-only: every number comes from a local report file that a
real tool run already produced (sit judgement, defect register, audit) or from the gap-answers log. Nothing is
computed from a guess, and a report with no source file says so instead of showing a number."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from Platform.webapp import runner, store

VERDICT_ORDER = ["COVERED", "READY", "EASY", "FIXTURE", "HARD", "MANUAL"]


def _slug(name: str | None) -> str | None:
    return re.sub(r"[^a-z0-9]+", "-", (name or "").lower()).strip("-") or None


def _latest(root: Path, slug: str, filename: str) -> Path | None:
    hits = sorted(root.glob(f"*/{slug}/*/{filename}"), key=lambda p: p.parent.name, reverse=True)
    return hits[0] if hits else None


def _json(p: Path | None):
    try:
        return json.loads(p.read_text(encoding="utf-8")) if p else None
    except (OSError, ValueError):
        return None


def insights(project: str, device: str) -> dict:
    root = runner.SYSTEM_TEST_OPS_ROOT / "reports"
    mapping = next((m for m in store.list_suite_mappings() if m["project"] == project and m["device"] == device), None)
    slug = _slug(mapping.get("new_suite")) if mapping else None
    out: dict = {"project": project, "device": device, "suite": mapping.get("new_suite") if mapping else None}

    # 1. automation readiness, from the sit judgement (what sit can automate today)
    jp = _latest(root, slug, "sit-judgement.json") if slug else None
    j = _json(jp)
    if j:
        by_section: dict[str, Counter] = defaultdict(Counter)
        for c in j["cases"].values():
            by_section[(c.get("section") or "?").split(" / ")[0]][c["verdict"]] += 1
        total = Counter(c["verdict"] for c in j["cases"].values())
        st = j.get("state", {})
        out["readiness"] = {
            "generated": st.get("generated_utc"), "sit_branch": st.get("sit_branch"), "sit_sha": (st.get("sit_sha") or "")[:8],
            "totals": {v: total.get(v, 0) for v in VERDICT_ORDER},
            "sections": sorted(({"name": k, **{v: cnt.get(v, 0) for v in VERDICT_ORDER}, "total": sum(cnt.values())} for k, cnt in by_section.items()),
                               key=lambda r: -r["total"]),
        }
    # 2. known defects (a tracked list, not Jira)
    dp = root / project.lower() / "defects" / "pos-defects.json"
    dj = _json(dp if dp.is_file() else None)
    lj = _json(root / project.lower() / "defects" / "defect-case-links.validated.json")
    if dj:
        sev = Counter(d.get("severity") for d in dj["defects"])
        c2d = (lj or {}).get("case_to_defects") or {}
        linked_defects = {d for ds in c2d.values() for d in ds}
        out["defects"] = {"total": len(dj["defects"]), "by_severity": {k: sev.get(k, 0) for k in ("High", "Medium", "Low")},
                          "cases_affected": len(c2d), "defects_with_a_case": len(linked_defects),
                          "no_covering_test": len(dj["defects"]) - len(linked_defects),
                          "needs_device_check": sum(1 for d in dj["defects"] if d.get("device_check_needed"))}
    # 3. gap answers (the answers log), per project
    answers = store.list_gap_answers(project)
    latest: dict[str, dict] = {}
    for a in sorted(answers, key=lambda x: x["created_at"]):
        latest[a["gap_ref"].split()[0]] = a
    kinds = Counter()
    for a in latest.values():
        t = a["answer"]
        kinds["Accepted" if t.startswith("[Accepted") else "Draft" if t.startswith("[DRAFT") and a.get("entry_type") == "answer"
              else "Needs a decision" if a.get("entry_type") == "clarification_request" else "Conflict" if a.get("entry_type") == "conflict" else "Answered"] += 1
    out["gaps"] = {"gaps_with_an_entry": len(latest), "by_status": dict(kinds)}
    # 4. case quality, from the latest audit
    ap = _latest(root, slug, "alignment-audit.md") if slug else None
    if ap:
        txt = ap.read_text(encoding="utf-8", errors="replace")
        g = lambda pat: int(m.group(1)) if (m := re.search(pat, txt)) else None
        rules = [(re.sub(r"\s*_\(advisory\)_", "", h).strip(), int(n)) for h, n in re.findall(r"^## (.+?) - (\d+)\s*$", txt, re.M) if int(n)]
        out["audit"] = {"date": ap.parent.name, "cases": g(r"Cases audited: \*\*(\d+)"), "blocking": g(r"Blocking findings: \*\*(\d+)"),
                        "advisory": g(r"Advisory[^*]*\*\*(\d+)"), "top_findings": sorted(rules, key=lambda r: -r[1])[:6]}
    return out
