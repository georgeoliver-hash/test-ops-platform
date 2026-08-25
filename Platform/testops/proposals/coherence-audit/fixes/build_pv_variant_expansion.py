"""Build the PV (suite 30255) variant-expansion rewrite + new-cases files.

George's 2026-07-24 rule: every case with a `Data variations:`/`Variation —` line naming multiple
distinct products/schemes/entitlements must be EXPANDED into one separate case per named variant —
no more bundling siblings behind one line. First/primary variant reuses the original case id
(retitled + body trimmed to that one variant); the rest become new cases in the same section.

Scope (documented, not everything with two named things):
  - Expanded: every explicit product/entitlement/scheme enumeration (Concession SmartPass
    sub-types, Half-Fare sub-types, Metro Multi-Journey zones, iLink zones+Belfast Visitor,
    yLink/24+, Translink Employee sub-types, EA Smartpass Pupil/FE, NIR-transfer product list,
    ABT card schemes, Barcode product types, cEMV decline reasons).
  - NOT expanded (documented judgment call, see changelog): the Adult/Child axis and the
    Glider/Rail axis. Glider/Rail is explicitly out of scope per the task (TestRail
    Configurations already cover it). Adult/Child is left as the existing secondary dimension
    (age-tier of the same product, not a distinct product/entitlement code) — flagged in the
    changelog as a scope decision, not silently dropped.

Output:
  pv-variant-expansion.rewrite.json    -- edits to the 11 "primary" cases (by id)
  pv-variant-expansion.new-cases.json  -- new cases to create (section_path + full body)
"""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).parent

SC_PATH = ["Functional", "Smartcard Validation"]
RAIL_PATH = ["Functional", "Rail-specific"]
ABT_PATH = ["Functional", "ABT (Glider)"]
BARCODE_PATH = ["Functional", "Barcodes"]

rewrite = []       # edits to existing cases, by id
new_cases = []      # new cases to create


def sc_case(product_label: str, precond_valid: str, precond_invalid: str,
            invalid_reason_screen: str, refs: str, extra_then_valid: str | None = None,
            title_suffix: str | None = None):
    """Build a standard 'validate a <product>' body (the pattern shared by the 11-family cases)."""
    title = f"Validate a {title_suffix or product_label} smartcard" if not title_suffix else title_suffix
    then_valid = "**THEN** the PV shows the Tag successful screen\n**AND** the success audio tone is played"
    if extra_then_valid:
        then_valid = extra_then_valid
    steps = [
        {"content": f"**WHEN** you present the valid {precond_valid}", "expected": then_valid},
        {"content": f"**WHEN** you present the {precond_invalid}",
         "expected": f"**THEN** the PV shows the {invalid_reason_screen} reject screen"},
        {"content": "**WHEN** you check the back office for the accepted presentation",
         "expected": "**THEN** the validation appears in the CloudFare activity log\n**AND** the transaction appears in MERIT\n**AND** the updated smartcard record appears in SmartTrack"},
    ]
    return steps


# ---------------------------------------------------------------------------
# GROUP A — 11-case Smartcard Validation family
# ---------------------------------------------------------------------------

# --- 1. Concession SmartPass: 60+ (primary, C4100981), Blind, Senior, ROI Senior, War Pensioner ---
CONCESSION_REFS = "FBD-100250, FBD-100335"
rewrite.append({
    "id": 4100981,
    "title": "Validate a 60+ Concession SmartPass",
    "expected": "60+ Concession SmartPasses validate (Tag successful) when valid and reject with the specific reason when invalid, recorded in CloudFare/MERIT/SmartTrack. Run under Glider and Rail.\n\n[Automatable: No · Cross-check: CloudFare / MERIT / SmartTrack]",
    "change_note": "Variant-expansion (George, 2026-07-24): was 'Validate a Concession SmartPass' carrying a 'Variation — 60+, Blind, Senior, ROI Senior, War Pensioner' line. Retitled to the specific sub-type already tested in the body (60+); the other 4 sub-types are now their own cases (C4101109-4101112) in this same section.",
})
for sub in ["Blind", "Senior", "ROI Senior", "War Pensioner"]:
    new_cases.append({
        "section_path": SC_PATH,
        "title": f"Validate a {sub} Concession SmartPass",
        "refs": CONCESSION_REFS,
        "preface": f"This test is to confirm a {sub} Concession SmartPass validates when valid and is rejected with the correct reason when invalid.",
        "preconds": f"**GIVEN** the axio4-PMV Platform Validator is in service showing the Present SmartCard or Barcode screen\n**AND** you have the seeded {sub} Concession SmartPass test cards to hand — a valid one and an expired one\n**AND** you can verify back-office records in the CloudFare activity log, MERIT and SmartTrack",
        "steps": sc_case(sub, f"{sub} SmartPass to the reader", f"expired {sub} Concession SmartPass", "Product Expired", CONCESSION_REFS),
        "expected": f"{sub} Concession SmartPasses validate (Tag successful) when valid and reject with the specific reason when invalid, recorded in CloudFare/MERIT/SmartTrack. Run under Glider and Rail.\n\n[Automatable: No · Cross-check: CloudFare / MERIT / SmartTrack]",
        "priority_id": 1,
    })

# --- 2. Half-Fare SmartPass: DLA (primary, C4100982), Learning Disability, No Driving Licence, PIPS, Partially Sighted ---
HALFFARE_REFS = "FBD-100250, gap-register Q12"
rewrite.append({
    "id": 4100982,
    "title": "Validate a DLA Half-Fare SmartPass",
    "expected": "DLA Half-Fare SmartPasses validate when valid and reject with the specific reason when invalid. Run under Glider and Rail.\n\n[Automatable: No · Cross-check: CloudFare / MERIT / SmartTrack]",
    "change_note": "Variant-expansion (George, 2026-07-24): was 'Validate a Half-Fare SmartPass' carrying 'Variation — DLA, Learning Disability, No Driving Licence, PIPS, Partially Sighted'. Retitled to the sub-type already tested (DLA); the other 4 are now their own cases in this section.",
})
for sub in ["Learning Disability", "No Driving Licence", "PIPS", "Partially Sighted"]:
    new_cases.append({
        "section_path": SC_PATH,
        "title": f"Validate a {sub} Half-Fare SmartPass",
        "refs": HALFFARE_REFS,
        "preface": f"This test is to confirm a {sub} Half-Fare SmartPass validates when valid and is rejected when invalid.",
        "preconds": f"**GIVEN** the PV is in service showing the Present SmartCard or Barcode screen\n**AND** you have a valid {sub} Half-Fare SmartPass and a Half-Fare SmartPass that is not valid at this location\n**AND** you can verify records in the CloudFare activity log, MERIT and SmartTrack",
        "steps": sc_case(sub, f"{sub} Half-Fare SmartPass", "Half-Fare SmartPass that is not valid here", "Not Valid At This Location", HALFFARE_REFS),
        "expected": f"{sub} Half-Fare SmartPasses validate when valid and reject with the specific reason when invalid. Run under Glider and Rail.\n\n[Automatable: No · Cross-check: CloudFare / MERIT / SmartTrack]",
        "priority_id": 1,
    })

# --- 3. Metro Multi-Journey zones: City (primary, C4100984), Inner, Extended (Adult/Child axis left as-is) ---
MJ_REFS = "FBD-100261, FBD-100277, FBD-100271"
rewrite.append({
    "id": 4100984,
    "title": "Validate a City-zone Metro Multi-Journey smartcard",
    "expected": "Metro Multi-Journey (City zone) validates within its zone (one journey deducted, passback applied) and rejects out-of-zone/invalid. Run for Adult and Child, under Glider and Rail.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT / SmartTrack]",
    "change_note": "Variant-expansion (George, 2026-07-24): was 'Validate a Metro Multi-Journey smartcard' carrying 'Variation — City, Inner, Extended zones'. Retitled to the zone already tested (City); Inner and Extended zones are now their own cases. Adult/Child left as the existing secondary age-tier axis (scope decision, see changelog) — not a distinct product/entitlement code.",
})
for zone, oz in [("Inner", "City"), ("Extended", "City")]:
    new_cases.append({
        "section_path": SC_PATH,
        "title": f"Validate a {zone}-zone Metro Multi-Journey smartcard",
        "refs": MJ_REFS,
        "preface": f"This test is to confirm a {zone}-zone Metro Multi-Journey smartcard validates in its zone (deducting a journey) and is rejected out of zone or when invalid.",
        "preconds": f"**GIVEN** the PV is in service showing the Present SmartCard or Barcode screen, configured for the Metro {zone} zone\n**AND** you have a {zone}-zone Adult Metro Multi-Journey card with journeys remaining, and the same product configured for the {oz} zone (out of zone here)\n**AND** you can verify records in the CloudFare activity log, MERIT and SmartTrack",
        "steps": [
            {"content": f"**WHEN** you present the {zone}-zone Multi-Journey card within its zone",
             "expected": "**THEN** the PV shows the Tag successful screen\n**AND** one journey is deducted with the passback rules applied"},
            {"content": f"**WHEN** you present the out-of-zone ({oz}) Multi-Journey card",
             "expected": "**THEN** the PV shows the Not Valid At This Location reject screen"},
            {"content": "**WHEN** you check the back office for the accepted presentation",
             "expected": "**THEN** the validation and journey deduction appear in the CloudFare activity log\n**AND** the transaction appears in MERIT\n**AND** the updated smartcard record appears in SmartTrack"},
        ],
        "expected": f"Metro Multi-Journey ({zone} zone) validates within its zone (one journey deducted, passback applied) and rejects out-of-zone/invalid. Run for Adult and Child, under Glider and Rail.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT / SmartTrack]",
        "priority_id": 1,
    })

# --- 4. iLink: Zone 4/Botanic (primary, C4100987), Zone 1, Zone 2, Zone 3, NW, Belfast Visitor Pass ---
ILINK_REFS = "FBD-100250, FBD-100271"
rewrite.append({
    "id": 4100987,
    "title": "Validate an iLink Zone 4 smartcard",
    "expected": "iLink (Zone 4) validates within its zone and rejects out-of-zone/invalid. Run for Adult and Child, under Glider and Rail.\n\n[Automatable: No · Cross-check: CloudFare / MERIT / SmartTrack]",
    "change_note": "Variant-expansion (George, 2026-07-24): was 'Validate an iLink smartcard' carrying 'Variation — Zones 1-4 and NW, plus Belfast Visitor Pass'. Retitled to the zone already tested (Zone 4, Botanic worked example kept). Zones 1-3, NW and Belfast Visitor Pass are now their own cases, using the same generic zone-level phrasing as the existing 'Rail — zone validation' case (C4100997) since no specific station is cited in FBD-100271 for those zones — not inventing a station name.",
})
for zone in ["1", "2", "3"]:
    new_cases.append({
        "section_path": SC_PATH,
        "title": f"Validate an iLink Zone {zone} smartcard",
        "refs": ILINK_REFS,
        "preface": f"This test is to confirm an iLink Zone {zone} smartcard validates in its zone and is rejected out of zone or when invalid.",
        "preconds": f"**GIVEN** a Rail PV within iLink Zone {zone} is in service showing the Present SmartCard or Barcode screen\n**AND** you have a valid iLink Zone {zone} smartcard and an iLink card whose zone does not cover this station\n**AND** you can verify records in the CloudFare activity log, MERIT and SmartTrack",
        "steps": [
            {"content": "**WHEN** you present the valid in-zone iLink card",
             "expected": "**THEN** the PV shows the Tag successful screen\n**AND** the success audio tone is played"},
            {"content": "**WHEN** you present the out-of-zone iLink card",
             "expected": "**THEN** the PV shows the Not Valid At This Location reject screen"},
            {"content": "**WHEN** you check the back office for the accepted presentation",
             "expected": "**THEN** the validation appears in the CloudFare activity log\n**AND** the transaction appears in MERIT\n**AND** the updated smartcard record appears in SmartTrack"},
        ],
        "expected": f"iLink (Zone {zone}) validates within its zone and rejects out-of-zone/invalid. Run for Adult and Child, under Glider and Rail.\n\n[Automatable: No · Cross-check: CloudFare / MERIT / SmartTrack]",
        "priority_id": 1,
    })
new_cases.append({
    "section_path": SC_PATH,
    "title": "Validate an iLink NW smartcard",
    "refs": ILINK_REFS,
    "preface": "This test is to confirm an iLink NW-zone smartcard validates in its zone and is rejected out of zone or when invalid.",
    "preconds": "**GIVEN** a Rail PV within the iLink NW zone is in service showing the Present SmartCard or Barcode screen\n**AND** you have a valid iLink NW smartcard and an iLink card whose zone does not cover this station\n**AND** you can verify records in the CloudFare activity log, MERIT and SmartTrack",
    "steps": [
        {"content": "**WHEN** you present the valid in-zone iLink NW card",
         "expected": "**THEN** the PV shows the Tag successful screen\n**AND** the success audio tone is played"},
        {"content": "**WHEN** you present the out-of-zone iLink card",
         "expected": "**THEN** the PV shows the Not Valid At This Location reject screen"},
        {"content": "**WHEN** you check the back office for the accepted presentation",
         "expected": "**THEN** the validation appears in the CloudFare activity log\n**AND** the transaction appears in MERIT\n**AND** the updated smartcard record appears in SmartTrack"},
    ],
    "expected": "iLink (NW zone) validates within its zone and rejects out-of-zone/invalid. Run for Adult and Child, under Glider and Rail.\n\n[Automatable: No · Cross-check: CloudFare / MERIT / SmartTrack]",
    "priority_id": 1,
})
new_cases.append({
    "section_path": SC_PATH,
    "title": "Validate a Belfast Visitor Pass",
    "refs": ILINK_REFS,
    "preface": "This test is to confirm a Belfast Visitor Pass validates in its zone and is rejected out of zone or when invalid.",
    "preconds": "**GIVEN** a Rail PV within the Belfast Visitor Pass zone is in service showing the Present SmartCard or Barcode screen\n**AND** you have a valid Belfast Visitor Pass and one whose zone does not cover this station\n**AND** you can verify records in the CloudFare activity log, MERIT and SmartTrack",
    "steps": [
        {"content": "**WHEN** you present the valid in-zone Belfast Visitor Pass",
         "expected": "**THEN** the PV shows the Tag successful screen\n**AND** the success audio tone is played"},
        {"content": "**WHEN** you present the out-of-zone Belfast Visitor Pass",
         "expected": "**THEN** the PV shows the Not Valid At This Location reject screen"},
        {"content": "**WHEN** you check the back office for the accepted presentation",
         "expected": "**THEN** the validation appears in the CloudFare activity log\n**AND** the transaction appears in MERIT\n**AND** the updated smartcard record appears in SmartTrack"},
    ],
    "expected": "Belfast Visitor Pass validates within its zone and rejects out-of-zone/invalid. Run for Adult and Child, under Glider and Rail.\n\n[Automatable: No · Cross-check: CloudFare / MERIT / SmartTrack]",
    "priority_id": 1,
})

# --- 5. yLink or 24+ (C4100989) -> split yLink (primary) + 24+ (new) ---
YLINK_REFS = "FBD-100236,FBD-100250"
YLINK_NOTE = ("resolved 2026-07-22: expiry is date-based only (end of the concessionary period), per "
              "FBD-100236 para 328 (\"the expiry date is expected to be set to the end of the "
              "concessionary period\"); no intraday time-of-day band exists for this product, confirmed "
              "by the total absence of any such case across the old suite's (10047) otherwise exhaustive "
              "coverage (hotlist/passback/days-left/zone), unlike the genuinely time-banded EA Pupil "
              "Smartpass / EA Bus Further Education products (old-suite cases confirm Mon-Fri/weekend/"
              "school-holiday time restrictions for those, a different product family).")
rewrite.append({
    "id": 4100989,
    "title": "Validate a yLink smartcard",
    "preface": "This test is to confirm a yLink smartcard validates while within its concessionary period and is rejected once expired (a date-based expiry, not an intraday time-of-day band).",
    "preconds": "**GIVEN** the PV is in service showing the Present SmartCard or Barcode screen\n**AND** you have a valid yLink smartcard within its concessionary period, and one whose concessionary-period expiry date has passed\n**AND** you can verify records in the CloudFare activity log, MERIT and SmartTrack",
    "steps": [
        {"content": "**WHEN** you present the yLink card after its concessionary-period expiry date",
         "expected": f"**THEN** the PV rejects it as an expired product (Product Expired) — {YLINK_NOTE}"},
    ],
    "expected": "yLink smartcards validate while within their concessionary period and are rejected (Product Expired) once the concessionary-period expiry date has passed — a date-based expiry, not a time-of-day band (gap Q25 resolved 2026-07-22: FBD-100236 para 328; old-suite 10047 absence of any yLink time-of-day case). Run under Glider and Rail.\n\n[Automatable: No · Cross-check: CloudFare / MERIT / SmartTrack]",
    "change_note": "Variant-expansion (George, 2026-07-24): was 'Validate a yLink or 24+ smartcard' bundling both products behind an 'or'. Retitled/rebodied to yLink only; 24+ is now its own case in this section.",
})
new_cases.append({
    "section_path": SC_PATH,
    "title": "Validate a 24+ smartcard",
    "refs": YLINK_REFS,
    "preface": "This test is to confirm a 24+ smartcard validates while within its concessionary period and is rejected once expired (a date-based expiry, not an intraday time-of-day band).",
    "preconds": "**GIVEN** the PV is in service showing the Present SmartCard or Barcode screen\n**AND** you have a valid 24+ smartcard within its concessionary period, and one whose concessionary-period expiry date has passed\n**AND** you can verify records in the CloudFare activity log, MERIT and SmartTrack",
    "steps": [
        {"content": "**WHEN** you present the 24+ card after its concessionary-period expiry date",
         "expected": f"**THEN** the PV rejects it as an expired product (Product Expired) — {YLINK_NOTE}"},
    ],
    "expected": "24+ smartcards validate while within their concessionary period and are rejected (Product Expired) once the concessionary-period expiry date has passed — a date-based expiry, not a time-of-day band (gap Q25 resolved 2026-07-22: FBD-100236 para 328; old-suite 10047 absence of any 24+ time-of-day case). Run under Glider and Rail.\n\n[Automatable: No · Cross-check: CloudFare / MERIT / SmartTrack]",
    "priority_id": 1,
})

# --- 6. Translink Employee: Staff (primary, C4100990), Staff Partner, Retired Staff, External Staff, Dependents Pass ---
EMP_REFS = "FBD-100250"
rewrite.append({
    "id": 4100990,
    "title": "Validate a Staff Translink Employee smartcard",
    "expected": "Staff employee smartcards validate when valid and reject when invalid. Run under Glider and Rail.\n\n[Automatable: No · Cross-check: CloudFare / MERIT / SmartTrack]",
    "change_note": "Variant-expansion (George, 2026-07-24): was 'Validate a Translink Employee smartcard' carrying 'Variation — Staff, Staff Partner, Retired Staff, External Staff, Dependents Pass'. Retitled to the sub-type already tested (Staff); the other 4 are now their own cases.",
})
for sub in ["Staff Partner", "Retired Staff", "External Staff", "Dependents Pass"]:
    new_cases.append({
        "section_path": SC_PATH,
        "title": f"Validate a {sub} Translink Employee smartcard",
        "refs": EMP_REFS,
        "preface": f"This test is to confirm a Translink {sub} employee smartcard validates when valid and is rejected when invalid.",
        "preconds": f"**GIVEN** the PV is in service showing the Present SmartCard or Barcode screen\n**AND** you have a valid {sub} employee smartcard and an expired/withdrawn {sub} employee smartcard\n**AND** you can verify records in the CloudFare activity log, MERIT and SmartTrack",
        "steps": sc_case(sub, f"{sub} smartcard", f"expired/withdrawn {sub} employee smartcard", "Product Expired", EMP_REFS),
        "expected": f"{sub} employee smartcards validate when valid and reject when invalid. Run under Glider and Rail.\n\n[Automatable: No · Cross-check: CloudFare / MERIT / SmartTrack]",
        "priority_id": 1,
    })

# --- 7. EA Smartpass: Pupil (primary, C4100991), Further Education ---
EA_REFS = "FBD-100250, coherence-audit/pv.findings.md"
rewrite.append({
    "id": 4100991,
    "title": "Validate an EA Pupil Smartpass",
    "expected": "EA Pupil Smartpasses validate within valid times and reject outside them (before start, after expiry, outside time, weekend, school holiday). Run for EA Bus (Glider) and EA Rail.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT / SmartTrack]",
    "change_note": "Variant-expansion (George, 2026-07-24): was 'Validate an EA Smartpass (Pupil and Further Education)' — both sub-types bundled directly in the title. Retitled to the sub-type already tested (Pupil); Further Education is now its own case. EA Bus (Glider)/EA Rail left as the existing Glider/Rail Configuration axis, out of scope per the task.",
})
new_cases.append({
    "section_path": SC_PATH,
    "title": "Validate an EA Further Education Smartpass",
    "refs": EA_REFS,
    "preface": "This test is to confirm an EA Further Education Smartpass validates within its valid times and is rejected outside them.",
    "preconds": "**GIVEN** the PV is in service showing the Present SmartCard or Barcode screen\n**AND** you have a valid EA Further Education Smartpass presented on a school-term weekday within its valid time\n**AND** you have the same pass to present at a weekend or during a school holiday\n**AND** you can verify records in the CloudFare activity log, MERIT and SmartTrack",
    "steps": [
        {"content": "**WHEN** you present the EA Further Education Smartpass within its valid time on a school day",
         "expected": "**THEN** the PV shows the Tag successful screen"},
        {"content": "**WHEN** you present it at a weekend or during a school holiday",
         "expected": "**THEN** the PV shows the Invalid Time Of Day reject screen"},
        {"content": "**WHEN** you check the back office for the accepted presentation",
         "expected": "**THEN** the validation appears in the CloudFare activity log\n**AND** the transaction appears in MERIT\n**AND** the updated smartcard record appears in SmartTrack"},
    ],
    "expected": "EA Further Education Smartpasses validate within valid times and reject outside them (before start, after expiry, outside time, weekend, school holiday). Run for EA Bus (Glider) and EA Rail.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT / SmartTrack]",
    "priority_id": 1,
})

# --- 8. Rail — NIR transfer validation (C4100996): iLink (primary), Belfast Visitor, Staff Smartpass, aLink, EA Pupil, EA Further Education ---
NIR_REFS = "FBD-100271"
rewrite.append({
    "id": 4100996,
    "title": "Rail — NIR transfer validation (iLink)",
    "expected": "NIR transfers validate for an eligible iLink smartcard (recorded as a transfer) and reject otherwise. Run for Adult and Child. (Rail mode.)\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT / SmartTrack]",
    "change_note": "Variant-expansion (George, 2026-07-24): was 'Rail — NIR transfer validation' carrying 'Variation — iLink, Belfast Visitor, Staff Smartpass, aLink, EA Pupil/FE'. Retitled to the product already tested (iLink); Belfast Visitor, Staff Smartpass, aLink, EA Pupil and EA Further Education are now their own cases (EA Pupil/FE further split into 2, matching the EA Smartpass family split above).",
})
for prod in ["Belfast Visitor", "Staff Smartpass", "aLink", "EA Pupil", "EA Further Education"]:
    new_cases.append({
        "section_path": RAIL_PATH,
        "title": f"Rail — NIR transfer validation ({prod})",
        "refs": NIR_REFS,
        "preface": f"This test is to confirm NIR transfer validation on a Rail PV for the {prod} product.",
        "preconds": f"**GIVEN** a Rail (NIR) PV is in service showing the Present SmartCard or Barcode screen\n**AND** you have a transfer-eligible {prod} smartcard that has just made a first NIR journey (inside its transfer window) and a non-eligible smartcard\n**AND** you can verify records in the CloudFare activity log, MERIT and SmartTrack",
        "steps": [
            {"content": f"**WHEN** you present the transfer-eligible {prod} card for the connecting NIR journey inside the transfer window",
             "expected": "**THEN** the PV validates it as a transfer per the transfer rules (no new journey charged)"},
            {"content": "**WHEN** you present the non-eligible card for the transfer",
             "expected": "**THEN** the PV rejects it with the specific reason shown"},
            {"content": "**WHEN** you check the back office for the transfer",
             "expected": "**THEN** the transfer validation is recorded in CloudFare, MERIT and SmartTrack"},
        ],
        "expected": f"NIR transfers validate for an eligible {prod} smartcard (recorded as a transfer) and reject otherwise. Run for Adult and Child. (Rail mode.)\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT / SmartTrack]",
        "priority_id": 1,
    })

# ---------------------------------------------------------------------------
# GROUP B — card scheme / product-type lists outside the smartcard family
# ---------------------------------------------------------------------------

# --- 9. ABT contactless tap (C4100998): Visa Debit (primary), Visa Credit, Mastercard Debit, Mastercard Credit, Maestro, mobile wallet ---
ABT_REFS = "knowledge/flows/pv-flow-annotations.md,FBD-100651 para 201"
rewrite.append({
    "id": 4100998,
    "title": "ABT — Visa Debit contactless tap validation",
    "preconds": "**GIVEN** a Glider PV on a Tap-On-Only route has ABT/cEMV enabled and is showing the Present screen\n**AND** you have a valid Visa Debit contactless payment card\n**AND** you can verify records in the CloudFare activity log and MERIT",
    "expected": "A valid Visa Debit contactless tap is accepted (ABT Tag successful) and recorded in CloudFare/MERIT.\n\n[Automatable: No · Cross-check: CloudFare / MERIT]",
    "change_note": "Variant-expansion (George, 2026-07-24): was 'ABT — contactless tap validation' carrying a 'Data variations: Visa Debit, Visa Credit, Mastercard Debit, Mastercard Credit, Maestro, mobile wallet' line. Retitled to one scheme (Visa Debit); the other 5 are now their own cases in this section.",
})
for scheme in ["Visa Credit", "Mastercard Debit", "Mastercard Credit", "Maestro", "mobile wallet"]:
    new_cases.append({
        "section_path": ABT_PATH,
        "title": f"ABT — {scheme} contactless tap validation",
        "refs": ABT_REFS,
        "preface": f"This test is to confirm a valid {scheme} contactless payment card is accepted for an ABT tap on a Glider PV.",
        "preconds": f"**GIVEN** a Glider PV on a Tap-On-Only route has ABT/cEMV enabled and is showing the Present screen\n**AND** you have a valid {scheme} contactless payment card\n**AND** you can verify records in the CloudFare activity log and MERIT",
        "steps": [
            {"content": f"**WHEN** you tap the valid {scheme} contactless card at the reader",
             "expected": "**THEN** the PV shows the ABT Tag successful screen to the passenger\n**AND** the success audio tone is played"},
            {"content": "**WHEN** you check the back office for the tap",
             "expected": "**THEN** the accepted tap appears in the CloudFare activity log\n**AND** the transaction appears in MERIT"},
        ],
        "expected": f"A valid {scheme} contactless tap is accepted (ABT Tag successful) and recorded in CloudFare/MERIT.\n\n[Automatable: No · Cross-check: CloudFare / MERIT]",
        "priority_id": 1,
    })

# --- 10. Barcode multi-use validation (C4101006): Adult (primary), Child, 3 Day Select, 1/3 Off Day Return,
#         24+, Ylink, Concession, Half Fare, Day Tracker (TVM+HHD), Unemployed Day Return (HHD only) ---
BARCODE_REFS = "TIBU-27324, FBD-100167"
BEEP = {
    "Adult": "single", "Child": "double", "3 Day Select": "double", "1/3 Off Day Return": "double",
    "24+": "double", "Ylink": "double", "Concession": "double", "Half Fare": "double",
    "Day Tracker": "double", "Unemployed Day Return": "single",
}


def barcode_case(product: str, device_note: str) -> dict:
    return {
        "section_path": BARCODE_PATH,
        "title": f"Barcode — multi-use validation ({product})",
        "refs": BARCODE_REFS,
        "preface": f"This test is to confirm a {product} multi-use barcode validates and tracks its remaining uses, {device_note}, with the correct audible beep pattern.",
        "preconds": f"**GIVEN** the PV is in service showing the Present SmartCard or Barcode screen with its barcode reader armed\n**AND** you have a valid {product} multi-use barcode with uses remaining and one presented beyond its allowed uses\n**AND** you can verify records in the CloudFare activity log and MERIT",
        "steps": [
            {"content": f"**WHEN** you present the valid {product} multi-use barcode",
             "expected": "**THEN** the PV validates it\n**AND** the PV shows the success result\n**AND** one use is recorded (remaining uses decremented)"},
            {"content": f"**WHEN** you present the {product} barcode beyond its allowed uses or an invalid one",
             "expected": "**THEN** the PV rejects it with the specific reason shown"},
            {"content": "**WHEN** you check the back office for the validation",
             "expected": "**THEN** the validation is recorded in the CloudFare activity log and MERIT"},
            {"content": f"**WHEN** a valid {product} multi-use barcode is presented",
             "expected": f"**THEN** the audible validation beep pattern is correct for {product} — {BEEP[product]} (pins TIBU-27324; migrated from old-suite C4091912)"},
        ],
        "expected": f"{product} multi-use barcodes validate and decrement remaining uses; reject when exhausted/invalid; recorded in CloudFare/MERIT, {device_note}. (In the live NIR regression.)\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
        "priority_id": 1,
    }


rewrite.append({
    "id": 4101006,
    "title": "Barcode — multi-use validation (Adult)",
    "preface": "This test is to confirm an Adult multi-use barcode validates and tracks its remaining uses, HHD- and TVM-produced, with the correct audible beep pattern.",
    "preconds": "**GIVEN** the PV is in service showing the Present SmartCard or Barcode screen with its barcode reader armed\n**AND** you have a valid Adult multi-use barcode with uses remaining and one presented beyond its allowed uses\n**AND** you can verify records in the CloudFare activity log and MERIT",
    "steps": [
        {"content": "**WHEN** you present the valid Adult multi-use barcode",
         "expected": "**THEN** the PV validates it\n**AND** the PV shows the success result\n**AND** one use is recorded (remaining uses decremented)"},
        {"content": "**WHEN** you present the Adult barcode beyond its allowed uses or an invalid one",
         "expected": "**THEN** the PV rejects it with the specific reason shown"},
        {"content": "**WHEN** you check the back office for the validation",
         "expected": "**THEN** the validation is recorded in the CloudFare activity log and MERIT"},
        {"content": "**WHEN** a valid Adult multi-use barcode is presented",
         "expected": "**THEN** the audible validation beep pattern is correct for Adult — single (pins TIBU-27324; migrated from old-suite C4091912)"},
    ],
    "expected": "Adult multi-use barcodes validate and decrement remaining uses; reject when exhausted/invalid; recorded in CloudFare/MERIT, HHD- and TVM-produced. (In the live NIR regression.)\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
    "change_note": "Variant-expansion (George, 2026-07-24): was 'Barcode — multi-use validation' carrying 'Variation — HHD-produced and TVM-produced; product types Adult, Child, 3 Day Select, 1/3 Off Day Return, 24+, Ylink, Concession, Half Fare, Day Tracker (TVM + HHD), plus Unemployed Day Return (HHD only)'. Retitled to Adult; the other 8 TVM+HHD product types and the HHD-only Unemployed Day Return are now their own cases, each carrying its own already-cited audible beep-pattern fact (TIBU-27324) instead of a shared enumeration line. HHD/TVM device-produced axis kept inside each case (both are already tested per product in the old suite; not treated as a distinct entitlement axis for this expansion).",
})
for product in ["Child", "3 Day Select", "1/3 Off Day Return", "24+", "Ylink", "Concession", "Half Fare", "Day Tracker"]:
    new_cases.append(barcode_case(product, "HHD- and TVM-produced"))
new_cases.append(barcode_case("Unemployed Day Return", "HHD-produced only"))

# ---------------------------------------------------------------------------
# GROUP C — cEMV decline reasons (C4101088), found via comprehensive sweep
# ---------------------------------------------------------------------------
DECLINE_REFS = "TIBU-22322,FBD-100651,knowledge/flows/pv-flow-annotations.md"
DECLINE_REASONS = [
    ("card not read", "card not read"),
    ("unsupported scheme (AMEX or Diners)", "unsupported scheme"),
    ("expired", "expired card"),
    ("ODA fail", "ODA (offline data authentication) fail"),
    ("on BIN list", "card on the BIN list"),
    ("on Deny list", "card on the Deny list"),
    ("card clash", "card clash"),
]
rewrite.append({
    "id": 4101088,
    "title": "cEMV — route-type enablement and passback distinctness",
    "preface": "This test is to confirm cEMV taps enable per route type, are disabled where they should be, and that a passback re-tap is handled distinctly from a decline.",
    "preconds": "**GIVEN** a Glider PV with cEMV is showing the Present screen\n**AND** a card can be re-presented within the configured ABT Passback window\n**AND** you can verify records in the CloudFare activity log",
    "steps": [
        {"content": "**WHEN** the route is \"Tap On Only (Flat Fare)\" or \"Tap On Tap Off\"",
         "expected": "**THEN** cEMV taps are enabled for that route type"},
        {"content": "**WHEN** no valid fare is found or the boarding location is outside the configured area",
         "expected": "**THEN** cEMV taps are disabled"},
        {"content": "**WHEN** a card is re-presented within the configured ABT Passback window",
         "expected": "**THEN** the PV shows the Passback outcome, not a decline error\n**AND** no second fare is taken for the re-presented card (pins TIBU-22322)"},
    ],
    "expected": "cEMV enables for Tap-On-Only and Tap-On-Tap-Off routes; disables on no-fare / out-of-area; a passback re-tap is distinct from a decline (pins TIBU-22322).\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
    "change_note": "Variant-expansion (George, 2026-07-24), found via comprehensive sweep beyond the known list: the case bundled 7 named decline conditions (card not read, unsupported scheme e.g. AMEX or Diners, expired, ODA fail, on BIN list, on Deny list, card clash) behind ONE generic WHEN/THEN step ('present a card that hits one of those decline conditions') — exactly the anti-pattern (a failure can be reason-specific; only one example ever actually gets executed). Split each decline reason into its own case (C-new below); this case keeps the 3 remaining, genuinely-distinct behaviours (route enablement, route disablement, passback-vs-decline) that were already correctly tested as one flow, retitled to match.",
})
for reason_short, reason_full in DECLINE_REASONS:
    new_cases.append({
        "section_path": ABT_PATH,
        "title": f"cEMV — decline reason: {reason_short}",
        "refs": DECLINE_REFS,
        "preface": f"This test is to confirm a cEMV tap declined for {reason_full} shows Please Try Again with that specific reason.",
        "preconds": f"**GIVEN** a Glider PV with cEMV is showing the Present screen\n**AND** you have a card seeded for the {reason_full} decline condition — restored 2026-07-22 via the Overflow UX design source (`knowledge/flows/pv-flow-annotations.md`, Platform Validator flow annotation for screen `1.3.3 Invalid Card`)\n**AND** you can verify records in the CloudFare activity log",
        "steps": [
            {"content": f"**WHEN** you present the card that hits the {reason_full} condition",
             "expected": "**THEN** the PV shows the Please Try Again outcome with that specific reason"},
            {"content": "**WHEN** you check the back office for the declined tap",
             "expected": "**THEN** the decline is recorded in the CloudFare activity log"},
        ],
        "expected": f"A cEMV tap declined for {reason_full} shows Please Try Again with the specific reason, recorded in CloudFare.\n\n[Automatable: Partial · Cross-check: CloudFare]",
        "priority_id": 1,
    })

# ---------------------------------------------------------------------------
# write outputs
# ---------------------------------------------------------------------------
defaults = {
    "template_id": 1, "type_id": 2, "custom_autoconfirmation": False,
    "custom_revstatus": 2, "custom_devtypes": [10],
}
for row in new_cases:
    row.setdefault("priority_id", 1)
    row["custom_devtypes"] = [10]

(HERE / "pv-variant-expansion.rewrite.json").write_text(
    json.dumps(rewrite, indent=2, ensure_ascii=False), encoding="utf-8")
(HERE / "pv-variant-expansion.new-cases.json").write_text(
    json.dumps(new_cases, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"rewrite (existing-case edits): {len(rewrite)}")
print(f"new cases: {len(new_cases)}")
