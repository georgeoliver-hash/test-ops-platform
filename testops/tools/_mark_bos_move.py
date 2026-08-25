"""One-off: prefix all CloudFare/Merit/Merit Web Reporter/Smartrack cases in suite 30279
with a move-marker so George can bulk 'Move To' them into the new BOS Suite (30287) via the
TestRail UI, since the API cannot move cases between suites. Run once, then after George
confirms the move, run the companion strip script to remove the marker.
"""
import json
from system_test_ops.testrail.client import TestRailClient
from system_test_ops.testrail.writer import TestRailWriter, load_write_suite_id

MARKER = "[MOVE -> **NEW** BOS Suite] "

def main():
    suite = load_write_suite_id()
    if suite != 30279:
        raise SystemExit(f"expected TESTRAIL_WRITE_SUITE_ID=30279, got {suite}")
    client = TestRailClient()
    writer = TestRailWriter(client, 42, suite, commit=True)
    with open("bos_move_ids.json", encoding="utf-8") as f:
        ids = json.load(f)
    updated = 0
    for cid in ids:
        cs = client.get_case(cid)
        title = cs.get("title") or ""
        if title.startswith(MARKER):
            continue
        writer.update_case_fields(cid, {"title": MARKER + title}, section_id=cs.get("section_id"))
        updated += 1
    print(f"marked {updated} cases (of {len(ids)} targeted)")

if __name__ == "__main__":
    main()
