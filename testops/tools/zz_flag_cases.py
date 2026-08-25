"""Flag cases in a suite as ZZ_DELETE_REVIEW so a human can bin them in the UI.

This TestRail instance's API can't delete cases, so superseded cases are renamed
with the ZZ_DELETE prefix (which the conformance audit skips) for a human to
sort-by-title and bulk-delete in the TestRail UI.

    python tools/zz_flag_cases.py --suite 30279 [--contains "ABT / Capping"]

By default flags EVERY non-ZZ case in the suite; pass --contains to restrict to
cases whose section path contains a substring. Writes only to the named suite.
"""
from __future__ import annotations

import argparse
import sys

from system_test_ops.testrail.client import TestRailClient
from system_test_ops.testrail.writer import TestRailWriter

PREFIX = "ZZ_DELETE_REVIEW - "


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--suite", type=int, required=True)
    ap.add_argument("--project", type=int, default=42)
    ap.add_argument("--contains", help="only flag cases whose section path contains this substring")
    ap.add_argument("--commit", action="store_true", help="actually rename (default: dry-run)")
    args = ap.parse_args()

    client = TestRailClient()
    secs = {s["id"]: s for s in client.get_sections(args.project, args.suite)}

    def path(sid):
        parts, cur = [], secs.get(sid)
        while cur:
            parts.append(cur["name"])
            cur = secs.get(cur.get("parent_id"))
        return " / ".join(reversed(parts))

    cases = client.get_cases(args.project, args.suite)
    targets = []
    for c in cases:
        title = c.get("title", "")
        if title.startswith("ZZ_DELETE"):
            continue
        if args.contains and args.contains.lower() not in path(c["section_id"]).lower():
            continue
        targets.append(c)

    print(f"{'COMMIT' if args.commit else 'DRY-RUN'}: {len(targets)} case(s) to flag in suite {args.suite}")
    if not args.commit:
        for c in targets[:5]:
            print(f"  would flag C{c['id']}: {c.get('title','')[:60]}")
        print("  ... (re-run with --commit to apply)")
        return 0

    writer = TestRailWriter(client, args.project, args.suite, commit=True)
    n = 0
    for c in targets:
        title = c.get("title", "")
        writer.update_case(title, new_title=PREFIX + title)
        n += 1
    print(f"Flagged {n} case(s) as {PREFIX!r}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
