import json

CASES_JSON = r"C:\SystemTestOps\system-test-ops\reports\uk-bus-projects\njt-farebox-and-register-replacement\2026-08-13\cases.json"
OUT_DIR = r"C:\SystemTestOps\system-test-ops\reports\uk-bus-projects\njt-farebox-and-register-replacement\2026-08-13\area-cases"

AREAS = {
    "functional-states": [
        "Fare Register / Functional States",
        "TIBU-28853 - NJT ETM / TIBU-28852 - NJT - Idle",
        "TIBU-28853 - NJT ETM / TIBU-29310 - NJT - Non Operational States",
        "Fare Register HMI / Signed Off (Section 6)",
    ],
    "fare-structure": [
        "Fare Register / Fare Structure",
    ],
    "driver-signon-paper": [
        "Fare Register / Driver Functionality / Sign on",
        "Fare Register / Driver Functionality / Default Display",
        "Fare Register / Driver Functionality / Paper Ticket Transactions",
        "Fare Register HMI / Sign On Process (Section 7)",
        "Fare Register HMI / Default Display (Section 8) / Ticket Issue Screen",
        "Fare Register HMI / Default Display (Section 8) / Overview",
        "Fare Register HMI / Default Display (Section 8) / Transaction Rejected (Section 8.6)",
        "TIBU-28853 - NJT ETM / TIBU-28899 -NJT - Sign On",
        "TIBU-28853 - NJT ETM / TIBU-29471 - NJT - Product Issue",
    ],
    "operator-menu": [
        "Fare Register / Driver Functionality / Operator Menu",
        "Fare Register HMI / Driver menu (Section 9)",
        "Fare Register HMI / Ticket Formats (Section 13)",
        "TIBU-28853 - NJT ETM / TIBU-29384 - NJT - Operator Menu",
        # legacy orphan top-level single-word sections (pre-restructure remnants)
        "Accept Next Bill", "Clear Bill Jam", "Device Handling", "Device Settings",
        "Driver Break", "Driver Totals", "Dump", "End of Run", "End of Trip",
        "Operator Menu", "Paper Status", "Relief", "Supervisor / Audit Reports",
    ],
    "other-functions-warnings": [
        "Fare Register / Driver Functionality / Other Functions",
        "Fare Register / Driver Functionality / FR Operation Warnings and Errors",
        "Fare Register HMI / Default Display (Section 8) / Bus Inspection (Section 8.7)",
        "Fare Register HMI / Error and Warning Screens (Section 10)",
        "Fare Register HMI / Status Bar (Section 5) / Status Indicators (Section 5.2) / Colour of the Day Indicator",
        "TIBU-28853 - NJT ETM / TIBU-29313 - NJT - Shortcut Keys",
        "TIBU-28853 - NJT ETM / TIBU-29628 - NJT - FR Operation Warnings and Errors",
        "TIBU-28853 - NJT ETM / TIBU-30121 - NJT - Miscellaneous",
    ],
    "obv-barcode-emv": [
        "Fare Register / OBV Functionality / Barcode",
        "Fare Register / OBV Functionality / EMV Transactions",
        "Fare Register HMI / Default Display (Section 8) / Barcode Validation Screen",
        "Fare Register HMI / Default Display (Section 8) / PayGo Transactions",
        "TIBU-28853 - NJT ETM / TIBU-28947 - NJT - OBV / TIBU-28970 - NJT - OBV - Barcode",
        "TIBU-28853 - NJT ETM / TIBU-28947 - NJT - OBV / TIBU-28979 - NJT - OBV - PayGo EMV",
    ],
    "obv-farepay": [
        "Fare Register / OBV Functionality / Fare Pay card",
        "Fare Register HMI / Default Display (Section 8) / FARE-PAY Transactions",
        "TIBU-28853 - NJT ETM / TIBU-28947 - NJT - OBV / TIBU-29093 - NJT - OBV - FarePay",
    ],
    "obv-emergency-status-timeout": [
        "Fare Register / OBV Functionality / Emergency Mode",
        "Fare Register / OBV Functionality / Communication Loss",
        "Fare Register / OBV Functionality / OBV Status",
        "Fare Register / OBV Functionality / Transaction Timeout",
        "Fare Register HMI / Status Bar (Section 5)",
        "TIBU-28853 - NJT ETM / TIBU-28947 - NJT - OBV / TIBU-28971 - NJT - OBV - Emergency Mode",
        "TIBU-28853 - NJT ETM / TIBU-30296 - NJT - Status Bar",
    ],
    "special-user": [
        "Fare Register / Special User Functionality",
        "Fare Register HMI / Administrator Mode (Section 12)",
        "Fare Register HMI / Supervisor Menu (Section 11)",
        "TIBU-28853 - NJT ETM / TIBU-29330 - NJT - Administrator Mode",
        "TIBU-28853 - NJT ETM / TIBU-30367 - NJT - Supervisor Mode",
    ],
    "cloudfare-comms": [
        "Fare Register / CloudFare Communication",
        "Cloudfare / Cloudfare Product Documentation",
        "Cloudfare / Device Management / Device Communication",
        "TIBU-28853 - NJT ETM / TIBU-29319 - NJT - Cloudfare Comms",
    ],
    "rs485-farebox-messaging": [
        "TIBU-28853 - NJT ETM / TIBU-29116 - NJT - Cubic RS485 Network",
    ],
    "nfr": [
        "Non Functional Requirements",
    ],
}

with open(CASES_JSON, encoding="utf-8") as f:
    data = json.load(f)
cases = data["cases"]

matched_ids = set()
EXACT_ONLY_EXTRA = {
    "driver-signon-paper": ["Fare Register / Driver Functionality"],
}

for area, prefixes in AREAS.items():
    rows = []
    exact_extra = EXACT_ONLY_EXTRA.get(area, [])
    for c in cases:
        sp = c["section_path"]
        if any(sp == p or sp.startswith(p + " /") for p in prefixes) or sp in exact_extra:
            rows.append(c)
            matched_ids.add(c["case_id"])
    rows.sort(key=lambda c: c["section_path"])
    out_path = f"{OUT_DIR}\\{area}.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# NJT cases — area: {area}\n\nTotal: {len(rows)}\n\n")
        for c in rows:
            f.write(f"## C{c['case_id']} — {c['title']}\n")
            f.write(f"Section: {c['section_path']}\n\n")
            steps = c.get("custom_steps") or ""
            f.write("```\n" + steps.strip() + "\n```\n\n")
    print(f"{area}: {len(rows)} cases -> {out_path}")

print("\nTotal distinct matched:", len(matched_ids))
print("Total in-scope target (excl To Delete):", sum(1 for c in cases if not c["section_path"].startswith("To Delete")))
