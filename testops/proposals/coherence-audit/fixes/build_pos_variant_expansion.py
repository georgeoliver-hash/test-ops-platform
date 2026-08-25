"""Build the POS Data-variations expansion for suite 30253 (project 42), 2026-07-24.

For each of the 23 cases carrying a 'Data variations:' line, expand into one case per named
variant: the FIRST/primary variant retitles+rewrites the existing case id (via rewrite.json,
applied by tools/apply_rewrite.py), the REMAINING variants become new cases in the SAME section
(via new-cases.json, applied by push_pos_variant_expansion.py - mirrors
proposals/coherence-audit/fixes/push_abt_portal_split.py's pattern).

Only the worked-example clause (preface + preconds, and occasionally one step line) changes per
variant; the rest of the When/Then stays generic/declarative (per gherkin-standard.md) so it
doesn't need per-variant rewriting. The trailing 'Data variations: ...' sentence is dropped from
custom_expected on every output case.

Grounding for values not explicitly enumerated in a case's own Data-variations line (documented
in full in pos-variant-expansion.changelog.md):
  - "payment" (vague) -> cash / card / warrant: the ONLY payment-method set used anywhere else in
    this suite for POS ticket sales (Single/NIR Single/Ulsterbus Single/Cross-Border/Top-Up all
    enumerate it explicitly) - suite-internal consistency, not invention.
  - "passenger type" (vague) -> Adult / Child: FBD-100293 ("only Passenger Type is currently
    used ... drives Adult/Child") - the spec-grounded baseline pair. Where a case's OWN
    Data-variations line explicitly names a 3rd value (concession), that explicit list is used
    instead and takes precedence over the FBD-100293 default.
  - "iLink zone" (vague) -> Zone 1 / Zone 2 / Zone 3 / Zone 4 / NW Zone: cited to FBD-100250
    ("iLink zones 1-4 + NW") and FBD-100690 ("iLink Zones 1/2/3/4/NW (nested)").
"""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).parent

rewrite_rows: list[dict] = []    # -> pos-variant-expansion.rewrite.json
new_case_rows: list[dict] = []   # -> pos-variant-expansion.new-cases.json
family_log: list[dict] = []      # -> feeds the changelog


def _fmt(text: str, v: dict) -> str:
    try:
        return text.format(**v)
    except (KeyError, IndexError):
        return text


def add_family(
    case_id: int,
    section_path: list[str],
    title_base: str,
    preface_tpl: str,
    preconds_tpl: str,
    steps_tpl: list[dict],
    expected_base: str,
    refs: str | None,
    variants: list[dict],
    devtypes: list[int] | None = None,
    note: str = "",
):
    primary = next((v for v in variants if v.get("_primary")), None)
    assert primary is not None, f"C{case_id}: no primary variant marked"
    rest = [v for v in variants if not v.get("_primary")]

    def render(v):
        title = f"{title_base} ({v['_label']})"
        preface = _fmt(preface_tpl, v)
        preconds = _fmt(preconds_tpl, v)
        steps = [{"content": _fmt(s["content"], v), "expected": _fmt(s["expected"], v)} for s in steps_tpl]
        return title, preface, preconds, steps

    title, preface, preconds, steps = render(primary)
    rewrite_rows.append({
        "id": case_id, "title": title, "preface": preface, "preconds": preconds,
        "steps": steps, "expected": expected_base, "refs": refs,
    })

    for v in rest:
        title, preface, preconds, steps = render(v)
        new_case_rows.append({
            "section_path": section_path, "title": title, "preface": preface, "preconds": preconds,
            "steps": steps, "expected": expected_base, "refs": refs,
            "custom_devtypes": devtypes or [5],
        })

    family_log.append({
        "case_id": case_id, "title_base": title_base, "section_path": section_path,
        "variants": [v["_label"] for v in variants], "new_count": len(rest), "note": note,
    })


CF_STEP = {"content": "**WHEN** the CloudFare activity log is checked",
           "expected": "**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log"}
MERIT_STEP = {"content": "**WHEN** the data is reviewed in MERIT", "expected": "**THEN** the transaction appears in MERIT"}
SMARTTRACK_STEP = {"content": "**WHEN** the smartcard record is reviewed in SmartTrack",
                    "expected": "**THEN** the updated smartcard record appears in SmartTrack"}

# ===========================================================================================
# 1. C4100427 - Validation - entitlement smartcard sets the ticket type (section 886958)
# ===========================================================================================
add_family(
    case_id=4100427, section_path=["Functional", "Top Up & Validation", "Validation"],
    title_base="Validation — entitlement smartcard sets the ticket type",
    preface_tpl=("This test is to confirm that presenting {CARD} sets the matching ticket type, "
                 "validates per transaction, and cannot be basketed."),
    preconds_tpl=("**GIVEN** the POS is signed on and selling a fare in NIR or Ulsterbus mode\n"
                  "**AND** {CARD} is available"),
    steps_tpl=[
        {"content": "**WHEN** the operator presents the entitlement smartcard",
         "expected": "**THEN** the matching ticket type is set (e.g. {TICKET})"},
        {"content": "**WHEN** the sale is on Rail",
         "expected": "**THEN** cross-border variants are selectable via the L4/R4 keys"},
        CF_STEP, MERIT_STEP, SMARTTRACK_STEP,
    ],
    expected_base=("An entitlement smartcard sets its ticket type, requires per-transaction validation "
                   "(no basketing), allows boarding/alighting change, and offers cross-border variants "
                   "on Rail. NIR + Ulsterbus only.\n\n"
                   "[Automatable: Partial – Cross-check: CloudFare / MERIT / SmartTrack]"),
    refs="FBD-100250",
    variants=[
        {"_primary": True, "_label": "Concession — Senior", "CARD": "a Concession Senior SmartPass", "TICKET": '"Senior Single"'},
        {"_label": "Concession — 60+", "CARD": "a Concession 60+ SmartPass", "TICKET": '"60+ Single"'},
        {"_label": "Concession — ROI Senior", "CARD": "a Concession ROI Senior SmartPass", "TICKET": '"ROI Senior Single"'},
        {"_label": "Concession — Blind", "CARD": "a Concession Blind SmartPass", "TICKET": '"Blind Single"'},
        {"_label": "Concession — War Pensioner", "CARD": "a Concession War Pensioner SmartPass", "TICKET": '"War Pensioner Single"'},
        {"_label": "yLink", "CARD": "a yLink smartcard", "TICKET": '"yLink Single"'},
        {"_label": "24+", "CARD": "a 24+ smartcard", "TICKET": '"24+ Single"'},
        {"_label": "Half-Fare — Partially Sighted", "CARD": "a Half-Fare Partially Sighted smartcard", "TICKET": '"Half Fare Single"'},
        {"_label": "Half-Fare — Learning Disability", "CARD": "a Half-Fare Learning Disability smartcard", "TICKET": '"Half Fare Single"'},
        {"_label": "Half-Fare — No Driving Licence", "CARD": "a Half-Fare No Driving Licence smartcard", "TICKET": '"Half Fare Single"'},
        {"_label": "Half-Fare — PIPS", "CARD": "a Half-Fare PIPS smartcard", "TICKET": '"Half Fare Single"'},
        {"_label": "Half-Fare — DLA", "CARD": "a Half-Fare DLA smartcard", "TICKET": '"Half Fare Single"'},
        {"_label": "Dependants", "CARD": "a Dependants smartcard", "TICKET": '"Dependants Single"'},
    ],
    note=("Flattened all 3 lists in the original body (7-item preface list, 5-item 'Half-Fare "
          "sub-types:' list, 5-item trailing 'Data variations: Concession -...' line) into one "
          "set of 13 distinct entitlement smartcard variants - each sets a different ticket type "
          "and can fail independently per FBD-100250."),
)

# ===========================================================================================
# 2. C4100413 - Smartcard - Half Fare (section 887002)
# ===========================================================================================
add_family(
    case_id=4100413, section_path=["Functional", "Smartcards"],
    title_base="Smartcard — Half Fare",
    preface_tpl="This test is to confirm a Half Fare {SUBTYPE} smartcard is recognised at the point of sale and applies the half-fare entitlement to the fare.",
    preconds_tpl=("**GIVEN** the POS is signed on and selling a fare in NIR or Ulsterbus mode\n"
                  "**AND** a Half Fare {SUBTYPE} entitlement smartcard is available\n"
                  "**AND** example: selling an Ulsterbus Adult Single, the half-fare rate is applied on presenting the card"),
    steps_tpl=[
        {"content": "**WHEN** the operator presents the Half Fare smartcard",
         "expected": "**THEN** the card is recognised\n**AND** the half-fare entitlement is applied to the fare"},
        CF_STEP, MERIT_STEP, SMARTTRACK_STEP,
    ],
    expected_base=("A Half Fare smartcard is recognised and applies the half-fare price at sale. NIR + Ulsterbus only.\n\n"
                   "[Automatable: Partial · Cross-check: CloudFare / MERIT / SmartTrack]"),
    refs="TIBU-24795",
    variants=[
        {"_primary": True, "_label": "NDL", "SUBTYPE": "No Driving Licence (NDL)"},
        {"_label": "LD", "SUBTYPE": "Learning Disability (LD)"},
        {"_label": "PIPS", "SUBTYPE": "PIPS"},
        {"_label": "Partially Sighted", "SUBTYPE": "Partially Sighted"},
        {"_label": "DLA", "SUBTYPE": "DLA"},
    ],
)

# ===========================================================================================
# 3. C4100419 - Single ticket (section 887003) - passenger type x payment
# ===========================================================================================
add_family(
    case_id=4100419, section_path=["Functional", "Tickets"],
    title_base="Single ticket",
    preface_tpl=("This test is to confirm the POS can sell and issue a Single ticket in either operating mode "
                 "(NIR or Ulsterbus) — built via that mode's fare look-up, priced correctly for the passenger "
                 "type, printed, and confirmed with the green success banner. Worked example: NIR {PASSENGER} "
                 "Single, Belfast Lanyon Place → Portadown, paid by {PAYMENT}."),
    preconds_tpl=("**GIVEN** an operator is signed on (NIR or Ulsterbus mode)\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: NIR {PASSENGER} Single, Belfast Lanyon Place → Portadown, paid by {PAYMENT}"),
    steps_tpl=[
        {"content": "**WHEN** the operator builds a Single ticket via the mode's fare look-up",
         "expected": "**THEN** the Single ticket is issued at the correct price"},
        {"content": "**WHEN** the operator takes payment for the passenger type",
         "expected": "**THEN** a receipt is printed\n**AND** a green success banner is displayed"},
    ],
    expected_base=("A Single ticket issues at the correct price in NIR and Ulsterbus, prints a receipt, and shows "
                   "the green success banner.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT / SmartTrack]"),
    refs=None,
    variants=[
        {"_primary": True, "_label": "Adult, cash", "PASSENGER": "Adult", "PAYMENT": "cash"},
        {"_label": "Child, cash", "PASSENGER": "Child", "PAYMENT": "cash"},
        {"_label": "concession, cash", "PASSENGER": "concession", "PAYMENT": "cash"},
        {"_label": "Adult, card", "PASSENGER": "Adult", "PAYMENT": "card"},
        {"_label": "Adult, warrant", "PASSENGER": "Adult", "PAYMENT": "warrant"},
    ],
)

# ===========================================================================================
# 4. C4100420 - Day Return ticket (section 887003) - passenger type only
# ===========================================================================================
add_family(
    case_id=4100420, section_path=["Functional", "Tickets"],
    title_base="Day Return ticket",
    preface_tpl=("This test is to confirm the POS can sell and issue a Day Return ticket in either operating mode "
                 "(NIR or Ulsterbus), priced correctly for the passenger type, printed, and confirmed with the "
                 "green success banner. Worked example: NIR {PASSENGER} Day Return, Belfast Lanyon Place → "
                 "Portadown, paid by cash."),
    preconds_tpl=("**GIVEN** an operator is signed on (NIR or Ulsterbus mode)\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: NIR {PASSENGER} Day Return, Belfast Lanyon Place → Portadown, paid by cash"),
    steps_tpl=[
        {"content": "**WHEN** the operator builds a Day Return ticket via the mode's fare look-up",
         "expected": "**THEN** the Day Return ticket is issued at the correct price"},
        {"content": "**WHEN** the operator takes payment for the passenger type",
         "expected": "**THEN** a receipt is printed\n**AND** a green success banner is displayed"},
    ],
    expected_base=("A Day Return issues at the correct price in NIR and Ulsterbus, prints a receipt, and shows "
                   "the green success banner.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]"),
    refs=None,
    variants=[
        {"_primary": True, "_label": "Adult", "PASSENGER": "Adult"},
        {"_label": "Child", "PASSENGER": "Child"},
    ],
)

# ===========================================================================================
# 5. C4100421 - iLink Single (section 887003) - iLink zone x passenger type
# ===========================================================================================
add_family(
    case_id=4100421, section_path=["Functional", "Tickets"],
    title_base="iLink Single",
    preface_tpl=("This test is to confirm the POS can sell an iLink Single fare against a presented iLink "
                 "smartcard in either operating mode (NIR or Ulsterbus), recording it against the card, printing "
                 "a receipt, and confirming with the green success banner. Worked example: {PASSENGER} iLink "
                 "Single, iLink {ZONE}, against a presented iLink smartcard, paid by cash."),
    preconds_tpl=("**GIVEN** an operator is signed on (NIR or Ulsterbus mode)\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: {PASSENGER} iLink Single, iLink {ZONE}, against a presented iLink smartcard, paid by cash"),
    steps_tpl=[
        {"content": "**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard",
         "expected": "**THEN** the iLink Single is issued\n**AND** it is recorded against the presented card"},
        {"content": "**WHEN** the operator takes payment",
         "expected": "**THEN** a receipt is printed\n**AND** a green success banner is displayed"},
    ],
    expected_base=("An iLink Single is sold against the presented iLink smartcard in NIR and Ulsterbus, recorded "
                   "against the card, and printed.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT / SmartTrack]"),
    refs=None,
    variants=[
        {"_primary": True, "_label": "Zone 4, Adult", "ZONE": "Zone 4", "PASSENGER": "Adult"},
        {"_label": "Zone 1, Adult", "ZONE": "Zone 1", "PASSENGER": "Adult"},
        {"_label": "Zone 2, Adult", "ZONE": "Zone 2", "PASSENGER": "Adult"},
        {"_label": "Zone 3, Adult", "ZONE": "Zone 3", "PASSENGER": "Adult"},
        {"_label": "NW Zone, Adult", "ZONE": "NW Zone", "PASSENGER": "Adult"},
        {"_label": "Zone 4, Child", "ZONE": "Zone 4", "PASSENGER": "Child"},
    ],
    note="'iLink zone' was named with no explicit value list; grounded to Zone 1/2/3/4/NW per FBD-100250 + FBD-100690.",
)

# ===========================================================================================
# 6. C4100423 - Family & Friends Day ticket (section 887003) - payment only
# ===========================================================================================
add_family(
    case_id=4100423, section_path=["Functional", "Tickets"],
    title_base="Family & Friends Day ticket",
    preface_tpl=("This test is to confirm the POS can sell and issue a Family & Friends Day ticket in either "
                 "operating mode (NIR or Ulsterbus), printing a receipt and confirming with the green success "
                 "banner. Worked example: Family & Friends Day ticket, paid by {PAYMENT}."),
    preconds_tpl=("**GIVEN** an operator is signed on (NIR or Ulsterbus mode)\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: Family & Friends Day ticket, paid by {PAYMENT}"),
    steps_tpl=[
        {"content": "**WHEN** the operator builds a Family & Friends Day ticket",
         "expected": "**THEN** the Family & Friends Day ticket is issued"},
        {"content": "**WHEN** the operator takes payment",
         "expected": "**THEN** a receipt is printed\n**AND** a green success banner is displayed"},
    ],
    expected_base=("A Family & Friends Day ticket issues in NIR and Ulsterbus, prints a receipt, and shows the "
                   "green success banner.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]"),
    refs=None,
    variants=[
        {"_primary": True, "_label": "cash", "PAYMENT": "cash"},
        {"_label": "card", "PAYMENT": "card"},
        {"_label": "warrant", "PAYMENT": "warrant"},
    ],
)

# ===========================================================================================
# 7. C4100393 - NIR - Single (section 886999) - passenger type x payment
# ===========================================================================================
add_family(
    case_id=4100393, section_path=["NIR (Rail)", "Tickets"],
    title_base="NIR — Single",
    preface_tpl=("This test is to confirm the POS can sell and issue an NIR Single ticket for any passenger type "
                 "and payment method — built from boarding and alighting stations via the rail fare look-up, "
                 "priced correctly, printed, and confirmed with the green success banner. Worked example: NIR "
                 "{PASSENGER} Single, Belfast Lanyon Place → Portadown, paid by {PAYMENT}."),
    preconds_tpl=("**GIVEN** an operator is signed on in rail (NIR) mode\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: NIR {PASSENGER} Single, Belfast Lanyon Place → Portadown, paid by {PAYMENT}"),
    steps_tpl=[
        {"content": "**WHEN** the operator builds a Single ticket from the boarding station, alighting station and passenger type",
         "expected": "**THEN** the Single ticket is issued at the correct price"},
        {"content": "**WHEN** the operator takes payment",
         "expected": "**THEN** a receipt is printed\n**AND** a green success banner is displayed"},
    ],
    expected_base=("An NIR Single issues at the correct price, prints a receipt, and shows the green success "
                   "banner.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT / SmartTrack]"),
    refs="FBD-100450",
    variants=[
        {"_primary": True, "_label": "Adult, cash", "PASSENGER": "Adult", "PAYMENT": "cash"},
        {"_label": "Child, cash", "PASSENGER": "Child", "PAYMENT": "cash"},
        {"_label": "concession, cash", "PASSENGER": "concession", "PAYMENT": "cash"},
        {"_label": "Adult, card", "PASSENGER": "Adult", "PAYMENT": "card"},
        {"_label": "Adult, warrant", "PASSENGER": "Adult", "PAYMENT": "warrant"},
    ],
)

# ===========================================================================================
# 8. C4100394 - NIR - Day Return (section 886999) - passenger type only
# ===========================================================================================
add_family(
    case_id=4100394, section_path=["NIR (Rail)", "Tickets"],
    title_base="NIR — Day Return",
    preface_tpl=("This test is to confirm the POS can sell and issue an NIR Day Return ticket, priced correctly "
                 "for the passenger type, printed, and confirmed with the green success banner. Worked example: "
                 "NIR {PASSENGER} Day Return, Belfast Lanyon Place → Portadown, paid by cash."),
    preconds_tpl=("**GIVEN** an operator is signed on in rail (NIR) mode\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: NIR {PASSENGER} Day Return, Belfast Lanyon Place → Portadown, paid by cash"),
    steps_tpl=[
        {"content": "**WHEN** the operator builds a Day Return ticket",
         "expected": "**THEN** the Day Return ticket is issued at the correct price"},
        {"content": "**WHEN** the operator takes payment",
         "expected": "**THEN** a receipt is printed\n**AND** a green success banner is displayed"},
    ],
    expected_base=("An NIR Day Return issues at the correct price, prints a receipt, and shows the green success "
                   "banner.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]"),
    refs="FBD-100450",
    variants=[
        {"_primary": True, "_label": "Adult", "PASSENGER": "Adult"},
        {"_label": "Child", "PASSENGER": "Child"},
    ],
)

# ===========================================================================================
# 9. C4100395 - NIR - 1/3 Off Day Return (section 886999) - passenger type only
# ===========================================================================================
add_family(
    case_id=4100395, section_path=["NIR (Rail)", "Tickets"],
    title_base="NIR — 1/3 Off Day Return",
    preface_tpl=("This test is to confirm the POS can sell an NIR 1/3 Off Day Return ticket with the one-third "
                 "discount applied, printed, and confirmed with the green success banner. Worked example: NIR "
                 "{PASSENGER} 1/3 Off Day Return, Belfast Lanyon Place → Portadown, paid by cash."),
    preconds_tpl=("**GIVEN** an operator is signed on in rail (NIR) mode\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: NIR {PASSENGER} 1/3 Off Day Return, Belfast Lanyon Place → Portadown, paid by cash"),
    steps_tpl=[
        {"content": "**WHEN** the operator builds a 1/3 Off Day Return ticket",
         "expected": "**THEN** the ticket is issued with the 1/3 discount applied"},
        {"content": "**WHEN** the operator takes payment",
         "expected": "**THEN** a receipt is printed\n**AND** a green success banner is displayed"},
    ],
    expected_base=("A 1/3 Off Day Return issues with the one-third discount applied, prints a receipt, and shows "
                   "the green success banner.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]"),
    refs="FBD-100450",
    variants=[
        {"_primary": True, "_label": "Adult", "PASSENGER": "Adult"},
        {"_label": "Child", "PASSENGER": "Child"},
    ],
)

# ===========================================================================================
# 10. C4100396 - NIR - Weekly Season (section 886999) - passenger type x payment (both vague)
# ===========================================================================================
add_family(
    case_id=4100396, section_path=["NIR (Rail)", "Tickets"],
    title_base="NIR — Weekly Season",
    preface_tpl=("This test is to confirm the POS can sell an NIR Weekly Season ticket carrying the correct "
                 "From/To validity dates, printed, and confirmed with the green success banner. Worked example: "
                 "NIR {PASSENGER} Weekly Season, Belfast Lanyon Place → Portadown, paid by {PAYMENT}."),
    preconds_tpl=("**GIVEN** an operator is signed on in rail (NIR) mode\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: NIR {PASSENGER} Weekly Season, Belfast Lanyon Place → Portadown, paid by {PAYMENT}"),
    steps_tpl=[
        {"content": "**WHEN** the operator builds a Weekly Season ticket",
         "expected": "**THEN** the Weekly Season ticket is issued with the correct From/To dates"},
        {"content": "**WHEN** the operator takes payment",
         "expected": "**THEN** a receipt is printed\n**AND** a green success banner is displayed"},
    ],
    expected_base=("A Weekly Season issues with the correct From/To validity dates, prints a receipt, and shows "
                   "the green success banner.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]"),
    refs="FBD-100450",
    variants=[
        {"_primary": True, "_label": "Adult, cash", "PASSENGER": "Adult", "PAYMENT": "cash"},
        {"_label": "Child, cash", "PASSENGER": "Child", "PAYMENT": "cash"},
        {"_label": "Adult, card", "PASSENGER": "Adult", "PAYMENT": "card"},
        {"_label": "Adult, warrant", "PASSENGER": "Adult", "PAYMENT": "warrant"},
    ],
    note="'passenger type; payment' were vague (no values listed); passenger type limited to Adult/Child per FBD-100293 (season products never show 'concession' elsewhere in this suite); payment grounded to cash/card/warrant per suite-wide consistency.",
)

# ===========================================================================================
# 11. C4100397 - NIR - Monthly Season (section 886999) - passenger type x payment (both vague)
#     Keep the TIBU-19299 regression pin + expiry-date assertion on every variant.
# ===========================================================================================
add_family(
    case_id=4100397, section_path=["NIR (Rail)", "Tickets"],
    title_base="NIR — Monthly Season",
    preface_tpl=("This test is to confirm the POS can sell an NIR Monthly Season ticket carrying the correct "
                 "expiry (To) date, printed, and confirmed with the green success banner. This also pins the "
                 "TIBU-19299 fix (Monthly Season expiry date). Worked example: NIR {PASSENGER} Monthly Season, "
                 "Belfast Lanyon Place → Portadown, paid by {PAYMENT}."),
    preconds_tpl=("**GIVEN** an operator is signed on in rail (NIR) mode\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: NIR {PASSENGER} Monthly Season, Belfast Lanyon Place → Portadown, paid by {PAYMENT}"),
    steps_tpl=[
        {"content": "**WHEN** the operator builds a Monthly Season ticket",
         "expected": "**THEN** the Monthly Season ticket is issued with the correct From/To dates\n**AND** the expiry (To) date is one calendar month from the start date"},
        {"content": "**WHEN** the operator takes payment",
         "expected": "**THEN** a receipt is printed\n**AND** a green success banner is displayed"},
    ],
    expected_base=("A Monthly Season issues with the correct expiry (To) date, prints a receipt, and shows the "
                   "green success banner (regression pin — TIBU-19299).\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]"),
    refs="TIBU-19299,FBD-100450",
    variants=[
        {"_primary": True, "_label": "Adult, cash", "PASSENGER": "Adult", "PAYMENT": "cash"},
        {"_label": "Child, cash", "PASSENGER": "Child", "PAYMENT": "cash"},
        {"_label": "Adult, card", "PASSENGER": "Adult", "PAYMENT": "card"},
        {"_label": "Adult, warrant", "PASSENGER": "Adult", "PAYMENT": "warrant"},
    ],
    note="Regression pin (TIBU-19299) kept on ALL 4 variants - the expiry-date bug could regress independently per passenger/payment path.",
)

# ===========================================================================================
# 12. C4100399 - NIR - 3 Day Select (section 886999) - passenger type x payment (both vague)
# ===========================================================================================
add_family(
    case_id=4100399, section_path=["NIR (Rail)", "Tickets"],
    title_base="NIR — 3 Day Select",
    preface_tpl=("This test is to confirm the POS can sell an NIR 3 Day Select ticket for the days chosen by "
                 "the operator, printed, and confirmed with the green success banner. Worked example: NIR "
                 "{PASSENGER} 3 Day Select, Belfast Lanyon Place → Portadown, paid by {PAYMENT}."),
    preconds_tpl=("**GIVEN** an operator is signed on in rail (NIR) mode\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: NIR {PASSENGER} 3 Day Select, Belfast Lanyon Place → Portadown, paid by {PAYMENT}"),
    steps_tpl=[
        {"content": "**WHEN** the operator builds a 3 Day Select ticket\n**AND** chooses the days",
         "expected": "**THEN** the 3 Day Select ticket is issued for the chosen days"},
        {"content": "**WHEN** the operator takes payment",
         "expected": "**THEN** a receipt is printed\n**AND** a green success banner is displayed"},
    ],
    expected_base=("A 3 Day Select issues for the chosen days, prints a receipt, and shows the green success "
                   "banner.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]"),
    refs="knowledge/projects/translink.md (Audit-confirmed POS facts — NIR-only ticket list)",
    variants=[
        {"_primary": True, "_label": "Adult, cash", "PASSENGER": "Adult", "PAYMENT": "cash"},
        {"_label": "Child, cash", "PASSENGER": "Child", "PAYMENT": "cash"},
        {"_label": "Adult, card", "PASSENGER": "Adult", "PAYMENT": "card"},
        {"_label": "Adult, warrant", "PASSENGER": "Adult", "PAYMENT": "warrant"},
    ],
)

# ===========================================================================================
# 13. C4100400 - NIR - Family & Friends Day (section 886999) - payment only (vague)
# ===========================================================================================
add_family(
    case_id=4100400, section_path=["NIR (Rail)", "Tickets"],
    title_base="NIR — Family & Friends Day",
    preface_tpl=("This test is to confirm the POS can sell and issue an NIR Family & Friends Day ticket, "
                 "printed, and confirmed with the green success banner. Worked example: NIR Family & Friends "
                 "Day, paid by {PAYMENT}."),
    preconds_tpl=("**GIVEN** an operator is signed on in rail (NIR) mode\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: NIR Family & Friends Day, paid by {PAYMENT}"),
    steps_tpl=[
        {"content": "**WHEN** the operator builds a Family & Friends Day ticket",
         "expected": "**THEN** the Family & Friends Day ticket is issued"},
        {"content": "**WHEN** the operator takes payment",
         "expected": "**THEN** a receipt is printed\n**AND** a green success banner is displayed"},
    ],
    expected_base=("An NIR Family & Friends Day ticket issues, prints a receipt, and shows the green success "
                   "banner.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]"),
    refs=None,
    variants=[
        {"_primary": True, "_label": "cash", "PAYMENT": "cash"},
        {"_label": "card", "PAYMENT": "card"},
        {"_label": "warrant", "PAYMENT": "warrant"},
    ],
)

# ===========================================================================================
# 14. C4100401 - NIR - iLink Single (section 886999) - iLink zone x passenger type (both vague)
# ===========================================================================================
add_family(
    case_id=4100401, section_path=["NIR (Rail)", "Tickets"],
    title_base="NIR — iLink Single",
    preface_tpl=("This test is to confirm the POS can sell an NIR iLink Single fare against a presented iLink "
                 "smartcard, recording it against the card, printing a receipt, and confirming with the green "
                 "success banner. Worked example: NIR {PASSENGER} iLink Single, iLink {ZONE}, against a presented "
                 "iLink smartcard, paid by cash."),
    preconds_tpl=("**GIVEN** an operator is signed on in rail (NIR) mode\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: NIR {PASSENGER} iLink Single, iLink {ZONE}, against a presented iLink smartcard, paid by cash"),
    steps_tpl=[
        {"content": "**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard",
         "expected": "**THEN** the iLink Single is issued\n**AND** it is recorded against the presented card"},
        {"content": "**WHEN** the operator takes payment",
         "expected": "**THEN** a receipt is printed\n**AND** a green success banner is displayed"},
    ],
    expected_base=("An NIR iLink Single is sold against the presented iLink smartcard, recorded against the "
                   "card, and printed.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT / SmartTrack]"),
    refs=None,
    variants=[
        {"_primary": True, "_label": "Zone 4, Adult", "ZONE": "Zone 4", "PASSENGER": "Adult"},
        {"_label": "Zone 1, Adult", "ZONE": "Zone 1", "PASSENGER": "Adult"},
        {"_label": "Zone 2, Adult", "ZONE": "Zone 2", "PASSENGER": "Adult"},
        {"_label": "Zone 3, Adult", "ZONE": "Zone 3", "PASSENGER": "Adult"},
        {"_label": "NW Zone, Adult", "ZONE": "NW Zone", "PASSENGER": "Adult"},
        {"_label": "Zone 4, Child", "ZONE": "Zone 4", "PASSENGER": "Child"},
    ],
    note="'iLink zone' grounded to Zone 1/2/3/4/NW per FBD-100250 + FBD-100690 (same as C4100421).",
)

# ===========================================================================================
# 15. C4100503 - NIR - Cross-Border Single (section 886999) - currency x payment
# ===========================================================================================
add_family(
    case_id=4100503, section_path=["NIR (Rail)", "Tickets"],
    title_base="NIR — Cross-Border Single",
    preface_tpl=("This test is to confirm the POS can sell and issue a Cross-Border Single ticket on a Rail "
                 "(NIR) POS, confirmed with the green success banner, with the price button toggling GBP and "
                 "EUR. Worked example: Adult Cross-Border Single, Belfast Lanyon Place → Dublin Connolly, priced "
                 "in {CURRENCY}, paid by {PAYMENT}."),
    preconds_tpl=("**GIVEN** an operator is signed on in rail (NIR) mode\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: Adult Cross-Border Single, Belfast Lanyon Place → Dublin Connolly, priced in {CURRENCY}, paid by {PAYMENT}"),
    steps_tpl=[
        {"content": "**WHEN** the operator selects a Cross-Border Single",
         "expected": "**THEN** the Cross-Border Single ticket is issued"},
        {"content": "**WHEN** the operator takes payment",
         "expected": "**THEN** a green success banner is displayed"},
    ],
    expected_base=("A Cross-Border Single issues and shows the green success banner.\n\n"
                   "[Automatable: Partial · Cross-check: CloudFare / MERIT]"),
    refs=None,
    variants=[
        {"_primary": True, "_label": "GBP, cash", "CURRENCY": "GBP", "PAYMENT": "cash"},
        {"_label": "EUR, cash", "CURRENCY": "EUR", "PAYMENT": "cash"},
        {"_label": "GBP, warrant", "CURRENCY": "GBP", "PAYMENT": "warrant"},
        {"_label": "GBP, card", "CURRENCY": "GBP", "PAYMENT": "card"},
    ],
)

# ===========================================================================================
# 16. C4100504 - NIR - Cross-Border Day Return (section 886999) - currency x payment
# ===========================================================================================
add_family(
    case_id=4100504, section_path=["NIR (Rail)", "Tickets"],
    title_base="NIR — Cross-Border Day Return",
    preface_tpl=("This test is to confirm the POS can sell and issue a Cross-Border Day Return ticket on a Rail "
                 "(NIR) POS, confirmed with the green success banner, with the price button toggling GBP and "
                 "EUR. Worked example: Adult Cross-Border Day Return, Belfast Lanyon Place → Dublin Connolly, "
                 "priced in {CURRENCY}, paid by {PAYMENT}."),
    preconds_tpl=("**GIVEN** an operator is signed on in rail (NIR) mode\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: Adult Cross-Border Day Return, Belfast Lanyon Place → Dublin Connolly, priced in {CURRENCY}, paid by {PAYMENT}"),
    steps_tpl=[
        {"content": "**WHEN** the operator selects a Cross-Border Day Return",
         "expected": "**THEN** the Cross-Border Day Return ticket is issued"},
        {"content": "**WHEN** the operator takes payment",
         "expected": "**THEN** a green success banner is displayed"},
    ],
    expected_base=("A Cross-Border Day Return issues and shows the green success banner.\n\n"
                   "[Automatable: Partial · Cross-check: CloudFare / MERIT]"),
    refs=None,
    variants=[
        {"_primary": True, "_label": "GBP, cash", "CURRENCY": "GBP", "PAYMENT": "cash"},
        {"_label": "EUR, cash", "CURRENCY": "EUR", "PAYMENT": "cash"},
        {"_label": "GBP, warrant", "CURRENCY": "GBP", "PAYMENT": "warrant"},
        {"_label": "GBP, card", "CURRENCY": "GBP", "PAYMENT": "card"},
    ],
)

# ===========================================================================================
# 17. C4100392 - Top Up - Ulsterbus Multi-Journey (section 886996) - payment only
# ===========================================================================================
add_family(
    case_id=4100392, section_path=["Ulsterbus", "Top Up"],
    title_base="Top Up — Ulsterbus Multi-Journey",
    preface_tpl=("This test is to confirm an Ulsterbus Multi-Journey smartcard can be topped up through its "
                 "card-reference-then-journeys flow — journeys are added and shown, and the maximum permitted "
                 "journeys is enforced."),
    preconds_tpl=("**GIVEN** an operator is signed on to the POS in Ulsterbus mode\n"
                  "**AND** an Ulsterbus Multi-Journey smartcard is presented\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: Ulsterbus Multi-Journey, select the card's reference number, add 10 journeys, paid by {PAYMENT}"),
    steps_tpl=[
        {"content": "**WHEN** the operator selects the card reference and journeys and takes payment",
         "expected": "**THEN** the journeys are added to the card\n**AND** the added journeys are shown\n**AND** the card cannot exceed its maximum permitted journeys"},
        CF_STEP, MERIT_STEP, SMARTTRACK_STEP,
    ],
    expected_base=("An Ulsterbus Multi-Journey top-up adds and shows journeys via the card-reference-then-"
                   "journeys flow and enforces the maximum (regression: TIBU-26861, TIBU-21133).\n\n"
                   "[Automatable: Partial · Cross-check: CloudFare / MERIT / SmartTrack]"),
    refs="TIBU-26861,TIBU-21133",
    variants=[
        {"_primary": True, "_label": "Cash", "PAYMENT": "Cash"},
        {"_label": "Warrant", "PAYMENT": "Warrant"},
        {"_label": "Card", "PAYMENT": "Card"},
    ],
    note="Regression pins (TIBU-26861, TIBU-21133) kept on ALL 3 variants.",
)

# ===========================================================================================
# 18. C4100403 - Ulsterbus - Single (section 887000) - passenger type x payment
# ===========================================================================================
add_family(
    case_id=4100403, section_path=["Ulsterbus", "Tickets"],
    title_base="Ulsterbus — Single",
    preface_tpl=("This test is to confirm the POS can sell and issue an Ulsterbus Single ticket for any "
                 "passenger type and payment method — built from route and stages via the bus fare look-up, "
                 "priced correctly, printed, and confirmed with the green success banner. Worked example: "
                 "Ulsterbus {PASSENGER} Single, 72b (IN) Moygashel Busby Shop → Armagh Bus Centre, paid by {PAYMENT}."),
    preconds_tpl=("**GIVEN** an operator is signed on in Ulsterbus mode\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: Ulsterbus {PASSENGER} Single, 72b (IN) Moygashel Busby Shop → Armagh Bus Centre, paid by {PAYMENT}"),
    steps_tpl=[
        {"content": "**WHEN** the operator builds a Single ticket from the route, boarding and alighting stages and passenger type",
         "expected": "**THEN** the Single ticket is issued at the correct price"},
        {"content": "**WHEN** the operator takes payment",
         "expected": "**THEN** a receipt is printed\n**AND** a green success banner is displayed"},
    ],
    expected_base=("An Ulsterbus Single issues at the correct price, prints a receipt, and shows the green "
                   "success banner.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]"),
    refs=None,
    variants=[
        {"_primary": True, "_label": "Adult, cash", "PASSENGER": "Adult", "PAYMENT": "cash"},
        {"_label": "Child, cash", "PASSENGER": "Child", "PAYMENT": "cash"},
        {"_label": "Adult, card", "PASSENGER": "Adult", "PAYMENT": "card"},
        {"_label": "Adult, warrant", "PASSENGER": "Adult", "PAYMENT": "warrant"},
    ],
)

# ===========================================================================================
# 19. C4100404 - Ulsterbus - Day Return (section 887000) - passenger type only
# ===========================================================================================
add_family(
    case_id=4100404, section_path=["Ulsterbus", "Tickets"],
    title_base="Ulsterbus — Day Return",
    preface_tpl=("This test is to confirm the POS can sell and issue an Ulsterbus Day Return ticket, priced "
                 "correctly for the passenger type, printed, and confirmed with the green success banner. "
                 "Worked example: Ulsterbus {PASSENGER} Day Return, 72b (IN) Moygashel Busby Shop → Armagh Bus "
                 "Centre, paid by cash."),
    preconds_tpl=("**GIVEN** an operator is signed on in Ulsterbus mode\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: Ulsterbus {PASSENGER} Day Return, 72b (IN) Moygashel Busby Shop → Armagh Bus Centre, paid by cash"),
    steps_tpl=[
        {"content": "**WHEN** the operator builds a Day Return ticket",
         "expected": "**THEN** the Day Return ticket is issued at the correct price"},
        {"content": "**WHEN** the operator takes payment",
         "expected": "**THEN** a receipt is printed\n**AND** a green success banner is displayed"},
    ],
    expected_base=("An Ulsterbus Day Return issues at the correct price, prints a receipt, and shows the green "
                   "success banner.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]"),
    refs=None,
    variants=[
        {"_primary": True, "_label": "Adult", "PASSENGER": "Adult"},
        {"_label": "Child", "PASSENGER": "Child"},
    ],
)

# ===========================================================================================
# 20. C4100405 - Ulsterbus - Month Return (section 887000) - passenger type only
# ===========================================================================================
add_family(
    case_id=4100405, section_path=["Ulsterbus", "Tickets"],
    title_base="Ulsterbus — Month Return",
    preface_tpl=("This test is to confirm the POS can sell an Ulsterbus Month Return ticket carrying the "
                 "correct validity dates, printed, and confirmed with the green success banner. Worked example: "
                 "Ulsterbus {PASSENGER} Month Return, 72b (IN) Moygashel Busby Shop → Armagh Bus Centre, paid by cash."),
    preconds_tpl=("**GIVEN** an operator is signed on in Ulsterbus mode\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: Ulsterbus {PASSENGER} Month Return, 72b (IN) Moygashel Busby Shop → Armagh Bus Centre, paid by cash"),
    steps_tpl=[
        {"content": "**WHEN** the operator builds a Month Return ticket",
         "expected": "**THEN** the Month Return ticket is issued with the correct validity dates"},
        {"content": "**WHEN** the operator takes payment",
         "expected": "**THEN** a receipt is printed\n**AND** a green success banner is displayed"},
    ],
    expected_base=("A Month Return issues with the correct validity dates, prints a receipt, and shows the "
                   "green success banner.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]"),
    refs="knowledge/projects/translink.md (Audit-confirmed POS facts — Ulsterbus-only ticket list)",
    variants=[
        {"_primary": True, "_label": "Adult", "PASSENGER": "Adult"},
        {"_label": "Child", "PASSENGER": "Child"},
    ],
)

# ===========================================================================================
# 21. C4100407 - Ulsterbus - Bus Rambler (section 887000) - passenger type x payment (both vague)
# ===========================================================================================
add_family(
    case_id=4100407, section_path=["Ulsterbus", "Tickets"],
    title_base="Ulsterbus — Bus Rambler",
    preface_tpl=("This test is to confirm the POS can sell and issue an Ulsterbus Bus Rambler ticket, printed, "
                 "and confirmed with the green success banner. Worked example: Ulsterbus {PASSENGER} Bus "
                 "Rambler, paid by {PAYMENT}."),
    preconds_tpl=("**GIVEN** an operator is signed on in Ulsterbus mode\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: Ulsterbus {PASSENGER} Bus Rambler, paid by {PAYMENT}"),
    steps_tpl=[
        {"content": "**WHEN** the operator builds a Bus Rambler ticket",
         "expected": "**THEN** the Bus Rambler ticket is issued"},
        {"content": "**WHEN** the operator takes payment",
         "expected": "**THEN** a receipt is printed\n**AND** a green success banner is displayed"},
    ],
    expected_base=("A Bus Rambler issues, prints a receipt, and shows the green success banner.\n\n"
                   "[Automatable: Partial · Cross-check: CloudFare / MERIT]"),
    refs="knowledge/projects/translink.md (Audit-confirmed POS facts — Ulsterbus-only ticket list)",
    variants=[
        {"_primary": True, "_label": "Adult, cash", "PASSENGER": "Adult", "PAYMENT": "cash"},
        {"_label": "Child, cash", "PASSENGER": "Child", "PAYMENT": "cash"},
        {"_label": "Adult, card", "PASSENGER": "Adult", "PAYMENT": "card"},
        {"_label": "Adult, warrant", "PASSENGER": "Adult", "PAYMENT": "warrant"},
    ],
    note="'passenger type; payment' were vague; grounded the same way as C4100396/etc.",
)

# ===========================================================================================
# 22. C4100408 - Ulsterbus - Family & Friends Day (section 887000) - payment only (vague)
# ===========================================================================================
add_family(
    case_id=4100408, section_path=["Ulsterbus", "Tickets"],
    title_base="Ulsterbus — Family & Friends Day",
    preface_tpl=("This test is to confirm the POS can sell and issue an Ulsterbus Family & Friends Day ticket, "
                 "printed, and confirmed with the green success banner. Worked example: Ulsterbus Family & "
                 "Friends Day, paid by {PAYMENT}."),
    preconds_tpl=("**GIVEN** an operator is signed on in Ulsterbus mode\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: Ulsterbus Family & Friends Day, paid by {PAYMENT}"),
    steps_tpl=[
        {"content": "**WHEN** the operator builds a Family & Friends Day ticket",
         "expected": "**THEN** the Family & Friends Day ticket is issued"},
        {"content": "**WHEN** the operator takes payment",
         "expected": "**THEN** a receipt is printed\n**AND** a green success banner is displayed"},
    ],
    expected_base=("An Ulsterbus Family & Friends Day ticket issues, prints a receipt, and shows the green "
                   "success banner.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]"),
    refs=None,
    variants=[
        {"_primary": True, "_label": "cash", "PAYMENT": "cash"},
        {"_label": "card", "PAYMENT": "card"},
        {"_label": "warrant", "PAYMENT": "warrant"},
    ],
)

# ===========================================================================================
# 23. C4100410 - Ulsterbus - iLink Single (section 887000) - iLink zone x passenger type (vague)
# ===========================================================================================
add_family(
    case_id=4100410, section_path=["Ulsterbus", "Tickets"],
    title_base="Ulsterbus — iLink Single",
    preface_tpl=("This test is to confirm the POS can sell an Ulsterbus iLink Single fare against a presented "
                 "iLink smartcard, recording it against the card, printing a receipt, and confirming with the "
                 "green success banner. Worked example: Ulsterbus {PASSENGER} iLink Single, iLink {ZONE}, against "
                 "a presented iLink smartcard, paid by cash."),
    preconds_tpl=("**GIVEN** an operator is signed on in Ulsterbus mode\n"
                  "**AND** the POS is communicating with CloudFare\n"
                  "**AND** example: Ulsterbus {PASSENGER} iLink Single, iLink {ZONE}, against a presented iLink smartcard, paid by cash"),
    steps_tpl=[
        {"content": "**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard",
         "expected": "**THEN** the iLink Single is issued\n**AND** it is recorded against the presented card"},
        {"content": "**WHEN** the operator takes payment",
         "expected": "**THEN** a receipt is printed\n**AND** a green success banner is displayed"},
    ],
    expected_base=("An Ulsterbus iLink Single is sold against the presented iLink smartcard, recorded against "
                   "the card, and printed.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT / SmartTrack]"),
    refs=None,
    variants=[
        {"_primary": True, "_label": "Zone 4, Adult", "ZONE": "Zone 4", "PASSENGER": "Adult"},
        {"_label": "Zone 1, Adult", "ZONE": "Zone 1", "PASSENGER": "Adult"},
        {"_label": "Zone 2, Adult", "ZONE": "Zone 2", "PASSENGER": "Adult"},
        {"_label": "Zone 3, Adult", "ZONE": "Zone 3", "PASSENGER": "Adult"},
        {"_label": "NW Zone, Adult", "ZONE": "NW Zone", "PASSENGER": "Adult"},
        {"_label": "Zone 4, Child", "ZONE": "Zone 4", "PASSENGER": "Child"},
    ],
    note="'iLink zone' grounded to Zone 1/2/3/4/NW per FBD-100250 + FBD-100690 (same as C4100421/C4100401).",
)

# ===========================================================================================
# write outputs
# ===========================================================================================
(HERE / "pos-variant-expansion.rewrite.json").write_text(
    json.dumps(rewrite_rows, indent=2, ensure_ascii=False), encoding="utf-8")
(HERE / "pos-variant-expansion.new-cases.json").write_text(
    json.dumps(new_case_rows, indent=2, ensure_ascii=False), encoding="utf-8")
(HERE / "pos-variant-expansion.family-log.json").write_text(
    json.dumps(family_log, indent=2, ensure_ascii=False), encoding="utf-8")

total_new = len(new_case_rows)
total_families = len(family_log)
print(f"families: {total_families}  primaries rewritten: {len(rewrite_rows)}  new cases: {total_new}")
print(f"total cases after expansion for these families: {len(rewrite_rows) + total_new}")
