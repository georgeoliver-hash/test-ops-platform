"""POS consolidation — retire the 33 absorbed cases (folded into keepers) and create the bin section.

File-based (clean UTF-8 em-dashes) so title `match` hits — never a PowerShell heredoc. Run AFTER
pushing proposals/pos-suite-restructure/consolidate-keepers.cases.yaml.
"""
from __future__ import annotations

from system_test_ops.testrail.client import TestRailClient
from system_test_ops.testrail.writer import TestRailWriter

RETIRE = [
    # Sign On — role × method (keeper: "Sign On — Operator sign on" -> "Sign On — by role ...")
    "Sign On — Supervisor sign on",
    "Sign On — Technician sign on",
    "Sign On — Administrator sign on",
    "Sign On — Operator sign on (smartcard)",
    "Sign On — Supervisor sign on (smartcard)",
    "Sign On — Technician sign on (smartcard)",
    "Sign On — Administrator sign on (smartcard)",
    # Sign-on messages (keeper: "Sign On — Message of the Day")
    "Sign On — Message of the Day unavailable",
    "Sign On — Word & Colour of the Day",
    "Sign On — Word & Colour of the Day unavailable",
    # Idle & screen / field (keeper: "Sign On — ID and PIN fields shown")
    "Sign On — idle to Sign On screen",
    "Sign On — field entry and the 'C' key",
    # Sign Off by role (keeper: "Sign Off — Operator")
    "Sign Off — Supervisor",
    "Sign Off — Technician",
    "Sign Off — Administrator",
    # Top Up per-product (keeper: "Top Up — top up a smartcard")
    "Top Up — Metro Travelcard",
    "Top Up — Town Service Travelcard",
    "Top Up — DayLink",
    "Top Up — iLink",
    "Top Up — Belfast Visitor Pass",
    "Top Up — ABT smartcard",
    "Top Up — Monthly Season Pass",
    "Top Up — half-fare / concession smartcard",
    # Issue Card per-product (keeper: "Issue Card — issue from blank")
    "Issue Card — Metro Multi-Journey",
    "Issue Card — Multi-Journey",
    "Issue Card — DayLink",
    "Issue Card — iLink",
    "Issue Card — Metro Travelcard",
    "Issue Card — Belfast Visitor Pass",
    "Issue Card — Ulsterbus Multi-Journey",
    "Issue Card — Town Service Travelcard",
    # Ticket History (keeper: "Ticket History — view history")
    "Ticket History — ticket details",
    "Ticket History — scroll pages",
]


def main() -> int:
    client = TestRailClient()
    writer = TestRailWriter(client, 42, 30253, commit=True)
    # Create the bin section as the human's move-target.
    writer.find_or_create_section_path(["ZZ - To Delete (review then bin)"])
    print(f"Retiring {len(RETIRE)} absorbed POS cases as ZZ_DELETE_REVIEW")
    missing = []
    for t in RETIRE:
        res = writer.update_case(t, new_title=f"ZZ_DELETE_REVIEW - {t} (folded)")
        if res.get("missing"):
            missing.append(t)
        else:
            print(f"  retired: {t}")
    if missing:
        print("\nNOT FOUND (check exact title):")
        for t in missing:
            print(f"  - {t}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
