"""Finish the ABT->BOS suite split:
1. Strip the [MOVE -> **NEW** BOS Suite] prefix from every case in suite 30287 (the copy landed there).
2. Condemn (ZZ_DELETE_REVIEW) the 175 leftover duplicate originals still sitting in suite 30279,
   since the TestRail copy operation left them behind rather than truly relocating them.
"""
from system_test_ops.testrail.client import TestRailClient
from system_test_ops.testrail.writer import TestRailWriter

MARKER = "[MOVE -> **NEW** BOS Suite] "

def strip_bos():
    client = TestRailClient()
    writer = TestRailWriter(client, 42, 30287, commit=True)
    cases = client.get_cases(42, 30287)
    updated = 0
    for cs in cases:
        title = cs.get("title") or ""
        if title.startswith(MARKER):
            writer.update_case_fields(cs["id"], {"title": title[len(MARKER):]}, section_id=cs.get("section_id"))
            updated += 1
    print(f"stripped marker on {updated} cases in suite 30287")

def condemn_abt_dupes():
    client = TestRailClient()
    writer = TestRailWriter(client, 42, 30279, commit=True)
    cases = client.get_cases(42, 30279)
    updated = 0
    for cs in cases:
        title = cs.get("title") or ""
        if title.startswith(MARKER):
            new_title = "ZZ_DELETE_REVIEW - " + title[len(MARKER):]
            writer.update_case_fields(cs["id"], {"title": new_title}, section_id=cs.get("section_id"))
            updated += 1
    print(f"condemned {updated} leftover duplicate cases in suite 30279")

if __name__ == "__main__":
    strip_bos()
    condemn_abt_dupes()
