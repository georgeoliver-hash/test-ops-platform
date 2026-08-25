"""Repair refs that were char-exploded by the old writer bug (",".join on a string).

A mangled ref looks like 'T,I,B,U,-,2,7,4'. Reconstruct: drop the inserted commas, then re-join the
whitespace tokens with ', '. Runs across the three Translink suites; updates by case id via a
per-suite writer (so each suite is the allowed write target).
"""
from __future__ import annotations

from system_test_ops.testrail.client import TestRailClient
from system_test_ops.testrail.writer import TestRailWriter

SUITES = {30253: "POS", 30254: "ETM", 30255: "PV"}


def is_mangled(refs: str) -> bool:
    if not refs or "," not in refs:
        return False
    segs = refs.split(",")
    # char-exploded => lots of single-character segments
    singles = sum(1 for s in segs if len(s.strip()) <= 1)
    return singles >= max(3, len(segs) // 2)


def reconstruct(refs: str) -> str:
    # remove the comma the bug inserted between every character, then re-tokenise on whitespace
    collapsed = "".join(refs.split(","))
    return ", ".join(collapsed.split())


def main() -> int:
    client = TestRailClient()
    total = 0
    for sid, name in SUITES.items():
        writer = TestRailWriter(client, 42, sid, commit=True)
        cases = client.get_cases(42, sid)
        fixed = 0
        for cse in cases:
            refs = cse.get("refs")
            if isinstance(refs, str) and is_mangled(refs):
                good = reconstruct(refs)
                writer.update_case_fields(int(cse["id"]), {"refs": good}, section_id=cse.get("section_id"))
                fixed += 1
                if fixed <= 4:
                    print(f"  {name} C{cse['id']}: {refs[:40]!r} -> {good!r}")
        print(f"{name} (suite {sid}): fixed {fixed} mangled-refs cases of {len(cases)}")
        total += fixed
    print(f"\nTOTAL repaired: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
