"""THROWAWAY read-only diff: current vs enrich-proposed estimate/automatable.
Delete after use. Does NOT write to TestRail."""
from __future__ import annotations

import re
from collections import Counter

from system_test_ops.testrail.client import TestRailClient
from tools.enrich_cases import judge

SUITE = 30253
PROJECT = 42
TAG_RX = re.compile(r"\[Automatable:\s*(Yes|Partial|No)\b", re.I)
PRN = {1: "High", 3: "Normal", 4: "Low"}

client = TestRailClient()
secs = {s["id"]: s for s in client.get_sections(PROJECT, SUITE)}


def path(sid):
    p = []
    cur = secs.get(sid)
    while cur:
        p.append(cur["name"])
        cur = secs.get(cur.get("parent_id"))
    return " / ".join(reversed(p))


cases = [c for c in client.get_cases(PROJECT, SUITE)
         if not str(c.get("title", "")).startswith(("ZZ_DELETE", "ZZ "))]

total = len(cases)
missing_est = []
missing_tag = []
est_changes = []
tier_changes = []
prio_changes = []
cur_tier_counts = Counter()
prop_tier_counts = Counter()

for c in cases:
    cur_est = c.get("estimate")
    expected = c.get("custom_expected") or ""
    m = TAG_RX.search(expected)
    cur_tier = m.group(1).title() if m else None

    if not cur_est:
        missing_est.append(c)
    if cur_tier is None:
        missing_tag.append(c)
    cur_tier_counts[cur_tier or "(none)"] += 1

    j = judge(c, path(c["section_id"]))
    prop_est = j["estimate"]
    prop_tier = j["automation_tier"]
    prop_prio = PRN[j["priority_id"]]
    prop_tier_counts[prop_tier] += 1

    if cur_est and cur_est != prop_est:
        est_changes.append((c, cur_est, prop_est))
    if cur_tier and cur_tier != prop_tier:
        tier_changes.append((c, cur_tier, prop_tier))


def title(c):
    return (c.get("title") or "")[:64]


print(f"Suite {SUITE}: {total} active cases (ZZ_DELETE excluded)\n")
print("=== COMPLETENESS (the goal: every case has both) ===")
print(f"  missing estimate     : {len(missing_est)}")
print(f"  missing Automatable   : {len(missing_tag)}")
print()
print("=== CURRENT Automatable tag distribution ===")
for k, v in sorted(cur_tier_counts.items()):
    print(f"  {k:8}: {v}")
print("=== PROPOSED (what enrich would set) ===")
for k, v in sorted(prop_tier_counts.items()):
    print(f"  {k:8}: {v}")
print()
print(f"=== WOULD CHANGE if --apply re-run ===")
print(f"  estimate changes: {len(est_changes)}")
print(f"  tier changes    : {len(tier_changes)}")

if missing_est:
    print("\n--- cases MISSING estimate (first 20) ---")
    for c in missing_est[:20]:
        print(f"  C{c['id']}  {title(c)}")
if missing_tag:
    print("\n--- cases MISSING Automatable tag (first 20) ---")
    for c in missing_tag[:20]:
        print(f"  C{c['id']}  {title(c)}")
if tier_changes:
    print("\n--- tier changes (first 25) ---")
    for c, old, new in tier_changes[:25]:
        print(f"  C{c['id']}  {old:7}->{new:7}  {title(c)}")
if est_changes:
    print("\n--- estimate changes (first 25) ---")
    for c, old, new in est_changes[:25]:
        print(f"  C{c['id']}  {old:5}->{new:5}  {title(c)}")
