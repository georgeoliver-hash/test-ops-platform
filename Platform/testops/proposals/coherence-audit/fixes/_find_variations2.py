"""Broader sweep for POS suite 30253: catch variant-list patterns NOT already caught by the
'Data variations' phrase - e.g. a parenthetical enumeration of passenger/card/product/entitlement
types embedded directly in preface/preconds/expected without that exact label.
"""
from __future__ import annotations
import json, re
from pathlib import Path

HERE = Path(__file__).parent
cases = json.loads((HERE / "pos-suite-30253-raw.json").read_text(encoding="utf-8"))

ALREADY = re.compile(r"(?i)data variations?\s*[:—-]|variation\s*—")
# candidate signal words followed by a parenthetical slash-list
CANDIDATE = re.compile(r"(?i)(passenger type|payment|card|scheme|entitlement|product|sub-type|category|categories|concession|currency|zone)\s*\(([^)]*/[^)]*)\)")

def full_fields(c):
    out = [("title", c.get("title") or ""), ("preface", c.get("custom_preface") or ""),
           ("preconds", c.get("custom_preconds") or ""), ("expected", c.get("custom_expected") or "")]
    for i, s in enumerate(c.get("custom_steps_seperated") or []):
        out.append((f"step{i}.content", s.get("content") or ""))
        out.append((f"step{i}.expected", s.get("expected") or ""))
    return out

lines = []
seen_ids = set()
for c in cases:
    title = c.get("title") or ""
    if title.upper().startswith("ZZ_DELETE"):
        continue
    already_hit = False
    matches = []
    for label, text in full_fields(c):
        if ALREADY.search(text):
            already_hit = True
        for m in CANDIDATE.finditer(text):
            matches.append((label, m.group(0)))
    if matches and not already_hit:
        seen_ids.add(c.get("id"))
        lines.append(f"\n=== C{c.get('id')} :: {title}  [section_id={c.get('section_id')}]")
        for label, snippet in matches:
            lines.append(f"  [{label}] {snippet}")

lines.insert(0, f"total cases: {len(cases)}  new hits (not already caught by 'Data variations'): {len(seen_ids)}")
out_text = "\n".join(lines)
(HERE / "_variations_report2.txt").write_text(out_text, encoding="utf-8")
print(f"done: {len(seen_ids)} new candidate hits")
