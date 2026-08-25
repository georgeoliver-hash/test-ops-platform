from __future__ import annotations
from system_test_ops.testrail.client import TestRailClient

client = TestRailClient()
sections = client.get_sections(42, 30253)
by_id = {int(s["id"]): s for s in sections}

def path(sid):
    s = by_id[sid]
    parent = s.get("parent_id")
    prefix = path(int(parent)) if parent else []
    return prefix + [s.get("name")]

for sid in [886958, 887002, 887003, 886999, 886996, 887000]:
    print(sid, "->", " / ".join(path(sid)))
