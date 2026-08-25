"""Build the follow-up TVM Data-variations expansion (suite 30284, project 42), 2026-07-24.

Continues tvm-variant-expansion.cases.yaml (Payments - EMV & Contactless, done) with the 4
families scoped as a follow-up in tvm-variant-expansion.changelog.md:
  - Barcode Redemption (887776)
  - Payments - Cash incl. BNR (887777 / 887778 / 887843)
  - Sales - Tickets: Ticket Issue / Advance & 3-Day / Rail & Cross-Border (887783 / 887784 / 887785)
  - Non-Functional: EMS & TMS Maintenance / Alarmboard / Resilience (887793-887796)

Same mechanics as the first batch: each source case's PRIMARY variant reuses the case id via
`match:` (retitled, `Data variations:`/trailing variant line removed from the body); the other
named variants become new cases in the same section. Kiosk/Astreo model and route-mode axes are
untouched (Configurations); only in-body data-value variant lists are split. Where a
Data-variations line names BOTH a mode/model axis AND a data-value axis (the Sales - Tickets
family), only the data-value axis (payment method / product / concession) is split — mode/model
stays on the case as a worked-example illustration, per the carve-out.

Produces one YAML file per family under proposals/coherence-audit/fixes/, pushed one at a time.
"""
from __future__ import annotations
from pathlib import Path
import yaml

HERE = Path(__file__).parent

DEFAULTS = {
    "template_id": 1,
    "custom_devtypes": [1],
    "custom_revstatus": 2,
    "custom_autoconfirmation": False,
}


def case(match, title, refs, objective, steps, expected):
    d = {}
    if match:
        d["match"] = match
    d["title"] = title
    d["refs"] = refs
    d["objective"] = objective
    d["steps"] = steps
    d["expected"] = expected
    return d


def write_family(filename_stem, header_comment, section_path, section_id, cases):
    doc = {
        "suite": "**NEW** TVM Test Suite",
        "suite_id": 30284,
        "defaults": DEFAULTS,
        "sections": [{"path": section_path, "cases": cases}],
    }
    out_path = HERE / f"{filename_stem}.cases.yaml"
    body = yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100)
    out_path.write_text(header_comment + "\n" + body, encoding="utf-8")
    print(f"{filename_stem}: {len(cases)} cases -> {out_path}")


# ---------------------------------------------------------------------------
# Family 1: Barcode Redemption (887776) — 6 source cases
# ---------------------------------------------------------------------------
barcode_cases = []

# C4103620: barcode type B/D/E/H/S/U (6-way). Primary keeps Type B (matches original content).
BARCODE_TYPES = ["B", "D", "E", "H", "S", "U"]
orig_title_620 = "Ticket Collection — a valid booking reference collects and prints the pre-paid ticket"
for i, bt in enumerate(BARCODE_TYPES):
    barcode_cases.append(case(
        match=orig_title_620 if i == 0 else None,
        title=f"Ticket Collection — a valid booking reference collects and prints the pre-paid ticket (barcode Type {bt})",
        refs=["FBD-100483", "FBD-100317"],
        objective=f"This test is to confirm a customer can collect a pre-paid single-use ticket on the TVM using a Type {bt} booking reference.",
        steps=(
            "**GIVEN** a customer is at the TVM Collect Tickets screen\n"
            f"**AND** a valid Type {bt} single-use booking reference for a Rail Adult Single\n"
            "**WHEN** the customer keys the booking reference and confirms collection\n"
            "**THEN** the pre-paid ticket is printed\n"
            "**AND** the \"Take Your Tickets\" prompt is displayed"
        ),
        expected=f"A valid Type {bt} booking reference collects the pre-paid single-use ticket, prints it, and prompts the customer to take it.\n\n[Automatable: Partial]",
    ))

# C4103624: keep AS-IS (above limit) + 1 new (below limit validated offline)
barcode_cases.append(case(
    match=None,
    title="Ticket Collection — a redemption above the barcode ceiling limit cannot validate offline",
    refs=["FBD-100483", "FBD-100317"],
    objective="This test is to confirm a collection whose value exceeds the offline ceiling limit is not validated offline.",
    steps=(
        "**GIVEN** a customer is at the TVM Collect Tickets screen with no back-office connection\n"
        "**AND** a booking reference whose ticket value exceeds the configured barcode ceiling limit\n"
        "**WHEN** the customer submits the booking reference\n"
        "**THEN** the collection is refused offline\n"
        "**AND** a value-exceeds-offline-limit message is displayed"
    ),
    expected="A collection above the offline ceiling limit is refused offline with a value-exceeds-limit message.\n\n[Automatable: Partial]",
))
barcode_cases.append(case(
    match=None,
    title="Ticket Collection — a redemption below the barcode ceiling limit validates offline",
    refs=["FBD-100483", "FBD-100317"],
    objective="This test is to confirm a collection whose value is within the offline ceiling limit validates and completes offline.",
    steps=(
        "**GIVEN** a customer is at the TVM Collect Tickets screen with no back-office connection\n"
        "**AND** a booking reference whose ticket value is below the configured barcode ceiling limit\n"
        "**WHEN** the customer submits the booking reference\n"
        "**THEN** the collection is validated offline\n"
        "**AND** the pre-paid ticket is printed"
    ),
    expected="A collection below the offline ceiling limit validates offline and the ticket prints.\n\n[Automatable: Partial]",
))

# C4103625: invalid-field reason (To Station / From Station / Product Type / dates) — 4-way.
# Primary matches the original's own content (a station mismatch) -> "invalid To Station".
INVALID_FIELDS = [
    ("To Station", "whose To Station does not match the product"),
    ("From Station", "whose From Station does not match the product"),
    ("Product Type", "whose Product Type does not match the booked product"),
    ("dates", "whose travel dates do not match the booked product"),
]
orig_title_625 = "Booking Reference — an invalid booking reference is rejected"
for i, (label, precond) in enumerate(INVALID_FIELDS):
    barcode_cases.append(case(
        match=orig_title_625 if i == 0 else None,
        title=f"Booking Reference — an invalid booking reference is rejected (invalid {label})",
        refs=["FBD-100483"],
        objective=f"This test is to confirm a booking reference with an invalid {label} is rejected with the standard message.",
        steps=(
            "**GIVEN** a customer is at the TVM Collect Tickets screen\n"
            f"**AND** a booking reference {precond}\n"
            "**WHEN** the customer submits the booking reference\n"
            "**THEN** the message \"Booking reference entered is invalid\" is displayed\n"
            "**AND** a logfailure message is posted to the back office"
        ),
        expected=f"An invalid {label} on a booking reference is rejected with \"Booking reference entered is invalid\" and a logfailure is posted.\n\n[Automatable: Partial · Cross-check: CloudFare]",
    ))

# C4103626: malformed entry (no characters / incomplete / over-maximum length / invalid character).
# Primary matches original content ("incomplete" - shorter than required length).
MALFORMED = [
    ("incomplete entry", "an incomplete booking reference shorter than the required length"),
    ("no characters", "an empty booking reference field with no characters entered"),
    ("over-maximum length", "a booking reference entry longer than the maximum accepted length"),
    ("invalid character", "a booking reference entry containing a character outside the accepted set"),
]
orig_title_626 = "Booking Reference — a malformed reference entry is rejected before submission"
for i, (label, precond) in enumerate(MALFORMED):
    barcode_cases.append(case(
        match=orig_title_626 if i == 0 else None,
        title=f"Booking Reference — a malformed reference entry is rejected before submission ({label})",
        refs=["FBD-100483"],
        objective=f"This test is to confirm the TVM rejects a booking-reference entry that is {label}.",
        steps=(
            "**GIVEN** a customer is at the TVM Collect Tickets entry screen\n"
            f"**AND** {precond}\n"
            "**WHEN** the customer attempts to submit the reference\n"
            "**THEN** the entry is not accepted\n"
            "**AND** the customer is prompted to correct the reference"
        ),
        expected=f"A booking-reference entry that is {label} is not accepted and the customer is prompted to correct it.\n\n[Automatable: Partial]",
    ))

# C4103627: legacy-stage barcode type (B / E / U) — 3-way. Primary matches original (Type B).
LEGACY_TYPES = ["B", "E", "U"]
orig_title_627 = "Ticket Collection — a collection against a legacy stage resolves the legacy stage name"
for i, bt in enumerate(LEGACY_TYPES):
    barcode_cases.append(case(
        match=orig_title_627 if i == 0 else None,
        title=f"Ticket Collection — a collection against a legacy stage resolves the legacy stage name (Type {bt})",
        refs=["FBD-100483"],
        objective=f"This test is to confirm a Type {bt} booking reference using a legacy stage resolves it via the legacy stages file.",
        steps=(
            "**GIVEN** a customer is at the TVM Collect Tickets screen\n"
            f"**AND** a Type {bt} booking reference whose alighting point is the legacy stage \"Any NIR Station\"\n"
            "**WHEN** the customer submits the booking reference\n"
            "**THEN** the legacy stage is resolved to its stage name from the legacy stages file\n"
            "**AND** the ticket is printed for that legacy stage"
        ),
        expected=f"A Type {bt} legacy-stage booking reference resolves the stage name from the legacy stages file and the ticket prints.\n\n[Automatable: Partial]",
    ))

# C4103633: ticket layout (Single / Day Return / 3 Day Select / Cross Border / Half-fare / yLink /
# 24+ / Family) — 8-way. Primary matches original content (Single).
LAYOUTS = ["Single", "Day Return", "3 Day Select", "Cross Border", "Half-fare", "yLink", "24+", "Family"]
orig_title_633 = "Barcode Ticket Format — a collected ticket prints in the barcode ticket layout"
for i, layout in enumerate(LAYOUTS):
    barcode_cases.append(case(
        match=orig_title_633 if i == 0 else None,
        title=f"Barcode Ticket Format — a collected ticket prints in the barcode ticket layout ({layout})",
        refs=["FBD-100167", "FBD-100318"],
        objective=f"This test is to confirm a collected {layout} single-use ticket prints in the correct barcode ticket layout.",
        steps=(
            "**GIVEN** a customer has collected a valid single-use ticket on the TVM\n"
            f"**AND** a Rail {layout} collected via a Type B booking reference\n"
            "**WHEN** the ticket is printed\n"
            "**THEN** the ticket prints in the barcode redemption layout\n"
            "**AND** the printed fields match the collected product"
        ),
        expected=f"The collected {layout} ticket prints in the barcode redemption layout with fields matching the collected product.\n\n[Automatable: Partial]",
    ))

write_family(
    "tvm-variant-expansion-2-barcode",
    "# TVM variant expansion, follow-up batch 2026-07-24 — Barcode Redemption (887776).\n"
    "# See tvm-variant-expansion-2.changelog.md for the full rationale.",
    ["Functional", "Barcode Redemption"],
    887776,
    barcode_cases,
)

print("barcode total:", len(barcode_cases))
