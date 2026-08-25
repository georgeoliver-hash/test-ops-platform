"""Find every POS case (suite 30253) with a 'Data variations' style list, excluding ZZ_DELETE_*.

Searches title/preface/preconds/steps(content+expected)/expected for the pattern and prints a
compact report: case id, title, section path, and the matching text snippet(s).
"""
from __future__ import annotations
import json, re
from pathlib import Path

HERE = Path(__file__).parent
cases = json.loads((HERE / "pos-suite-30253-raw.json").read_text(encoding="utf-8"))

PAT = re.compile(r"(?i)data variations?\s*[:—-]|variation\s*—")

def full_text(c):
    parts = [c.get("title") or "", c.get("custom_preface") or "", c.get("custom_preconds") or "",
              c.get("custom_expected") or ""]
    for s in (c.get("custom_steps_seperated") or []):
        parts.append(s.get("content") or "")
        parts.append(s.get("expected") or "")
    return "\n".join(parts)

hits = []
for c in cases:
    title = c.get("title") or ""
    if title.upper().startswith("ZZ_DELETE"):
        continue
    txt = full_text(c)
    if PAT.search(txt):
        hits.append(c)

lines = []
lines.append(f"total cases: {len(cases)}  hits: {len(hits)}")
for c in hits:
    lines.append(f"\n=== C{c.get('id')} :: {c.get('title')}  [section_id={c.get('section_id')}]")
    for label, field in [("preface", c.get("custom_preface")), ("preconds", c.get("custom_preconds")),
                          ("expected", c.get("custom_expected"))]:
        if field and PAT.search(field):
            lines.append(f"  [{label}] {field}")
    for i, s in enumerate(c.get("custom_steps_seperated") or []):
        for label, field in [(f"step{i}.content", s.get("content")), (f"step{i}.expected", s.get("expected"))]:
            if field and PAT.search(field):
                lines.append(f"  [{label}] {field}")

out_text = "\n".join(lines)
print(out_text)
(HERE / "_variations_report.txt").write_text(out_text, encoding="utf-8")
