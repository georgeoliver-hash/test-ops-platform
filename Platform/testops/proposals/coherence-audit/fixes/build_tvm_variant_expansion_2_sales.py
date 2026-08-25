"""Build the follow-up TVM Data-variations expansion — Sales - Tickets (887783/887784/887785).

Axis: for cases whose ONLY genuine data-value axis (beyond mode/model, which stay a Configuration
per the carve-out) is payment method, split 3-way {cash, card (Chip & PIN), contactless}. For cases
where the Data-variations line names a product or concession-type list instead, split on THAT named
axis (not also crossed with payment, mirroring the changelog's own scoping). C4103691 is a genuinely
distinct-behaviour case (multi-use barcode exception), not a same-behaviour value list, so it is
kept as-is + one new sibling case, not split by payment.
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


PAYMENTS = ["cash", "card (Chip & PIN)", "contactless"]


def payment_split(orig_title, refs, objective_tpl, precond_tpl, then_line1, then_line2, expected_tpl, primary_payment="cash"):
    """Build a 3-way payment-method split. Primary keeps the original id."""
    out = []
    order = [primary_payment] + [p for p in PAYMENTS if p != primary_payment]
    for i, pay in enumerate(order):
        out.append(case(
            orig_title if i == 0 else None,
            f"{orig_title} ({pay})",
            refs,
            objective_tpl.format(pay=pay),
            (
                f"{precond_tpl}\n"
                f"**WHEN** the customer pays by {pay}\n"
                f"**THEN** {then_line1}\n"
                f"**AND** {then_line2}"
            ),
            expected_tpl.format(pay=pay),
        ))
    return out


ticket_issue_cases = []  # section 887783 (Ticket Issue)

ticket_issue_cases += payment_split(
    "Ticket Issue — a selected product is issued and printed",
    ["FBD-100336", "FBD-100207"],
    "This test is to confirm the customer can select a valid product, pay by {pay}, and receive a printed ticket.",
    (
        "**GIVEN** a TVM at its home stage on the multi-modal home screen\n"
        "**AND** an example product of a Metro Adult Single from 10A (IN) Casement Park to City Hall at £2.30 (fares export FBD-100336)"
    ),
    "a ticket is printed for the selected product",
    "the paid fare on the ticket matches the fares export",
    "The chosen product is issued and a ticket printed at the fares-export price, paying by {pay}.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
)

ticket_issue_cases += payment_split(
    "Ticket Issue — Adult single ticket",
    ["FBD-100336", "FBD-100207"],
    "This test is to confirm the customer can buy an Adult single ticket for the boarding and alighting stages selected, paying by {pay}.",
    (
        "**GIVEN** a TVM showing the Adult product range\n"
        "**AND** an example Metro Adult Single, 10A (IN) Casement Park to City Hall, £2.30"
    ),
    "an Adult single ticket is printed for the selected stages",
    "the fare charged equals the fares-export Adult single fare",
    "An Adult single is issued for the selected stages at the Adult fare, paying by {pay}.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
)

ticket_issue_cases += payment_split(
    "Ticket Issue — Child single ticket",
    ["FBD-100336", "FBD-100207"],
    "This test is to confirm the customer can buy a Child single ticket at the Child fare, paying by {pay}.",
    (
        "**GIVEN** a TVM showing the Child product range\n"
        "**AND** an example Metro Child Single, 10A (IN) Casement Park to City Hall, at the Child fare per the fares export"
    ),
    "a Child single ticket is printed for the selected stages",
    "the fare charged equals the fares-export Child single fare",
    "A Child single is issued at the Child fare, paying by {pay}.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
)

ticket_issue_cases += payment_split(
    "Ticket Issue — Family and Friends day ticket",
    ["FBD-100336"],
    "This test is to confirm the customer can buy a Family and Friends day ticket for the group, paying by {pay}.",
    (
        "**GIVEN** a TVM showing the Family and Friends product\n"
        "**AND** an example Metro Family and Friends Day ticket priced per the fares export"
    ),
    "a Family and Friends day ticket is printed",
    "the fare charged equals the fares-export Family and Friends fare",
    "A Family and Friends day ticket is issued for the group at the fares-export price, paying by {pay}.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
)

ticket_issue_cases += payment_split(
    "Ticket Issue — Family and Friends additional child",
    ["FBD-100336"],
    "This test is to confirm the customer can add an additional child to a Family and Friends ticket at the add-child price, paying by {pay}.",
    (
        "**GIVEN** a TVM with a Family and Friends day ticket selected\n"
        "**AND** the fares export defines a Family and Friends Additional Child price"
    ),
    "an additional-child ticket is printed alongside the Family and Friends ticket",
    "the fare charged includes the add-child price from the fares export",
    "An additional child is added to the Family and Friends ticket and charged the add-child price, paying by {pay}.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
)

ticket_issue_cases += payment_split(
    "Ticket Issue — Popular tickets shortcut",
    ["FBD-100336"],
    "This test is to confirm the customer can buy a product from the Popular Tickets shortcut list, paying by {pay}.",
    (
        "**GIVEN** a TVM showing the Popular Tickets shortcuts\n"
        "**AND** an example Popular shortcut for a Metro Adult Single at £2.30"
    ),
    "the shortcut product is printed as a ticket",
    "the fare charged matches the fares export for that product",
    "A product bought from the Popular Tickets shortcut is issued at its fares-export price, paying by {pay}.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
)

ticket_issue_cases += payment_split(
    "Ticket Issue — Evening ticket",
    ["FBD-100336"],
    "This test is to confirm the customer can buy a Metro Evening ticket during the evening validity window, paying by {pay}.",
    (
        "**GIVEN** a TVM inside the Metro Evening validity window\n"
        "**AND** an example Metro Evening Adult ticket priced per the fares export"
    ),
    "an Evening ticket is printed",
    "the fare charged equals the fares-export Evening fare",
    "A Metro Evening ticket is issued at the Evening fare during its validity window, paying by {pay}.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
)

ticket_issue_cases += payment_split(
    "Ticket Issue — Summer Bus Rambler ticket",
    ["FBD-100336"],
    "This test is to confirm the customer can buy a Summer Bus Rambler ticket at the fares-export price, paying by {pay}.",
    (
        "**GIVEN** a TVM showing the Summer Bus Rambler product within its seasonal availability\n"
        "**AND** an example Summer Bus Rambler Adult ticket priced per the fares export"
    ),
    "a Bus Rambler ticket is printed",
    "the fare charged equals the fares-export Bus Rambler fare",
    "A Summer Bus Rambler ticket is issued at its fares-export price, paying by {pay}.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
)

ticket_issue_cases += payment_split(
    "Ticket Issue — concessionary half-fare single",
    ["FBD-100336", "FBD-100207"],
    "This test is to confirm the customer can buy a half-fare concessionary single at the half-fare price, paying by {pay}.",
    (
        "**GIVEN** a TVM showing the concessionary product range\n"
        "**AND** an example half-fare concessionary single at half the Adult fares-export single fare"
    ),
    "a concessionary single ticket is printed",
    "the fare charged equals the half-fare price from the fares export",
    "A half-fare concessionary single is issued at the half-fare price, paying by {pay}.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT / SmartTrack]",
)

# C4103687: product axis (Day / Day Return / 1 Month Return) — 3-way, NOT crossed with payment.
PRODUCTS_687 = ["Day", "Day Return", "1 Month Return"]
orig_687 = "Ticket Issue — Day and Day Return tickets"
for i, prod in enumerate(PRODUCTS_687):
    ticket_issue_cases.append(case(
        orig_687 if i == 0 else None,
        f"Ticket Issue — {prod} ticket",
        ["FBD-100336"],
        f"This test is to confirm the customer can buy a {prod} ticket at the fares-export price.",
        (
            "**GIVEN** a TVM showing the Day and Day Return products\n"
            f"**AND** an example Metro Adult {prod} ticket priced per the fares export\n"
            f"**WHEN** the customer buys the {prod} ticket and pays\n"
            f"**THEN** the {prod} ticket is printed\n"
            "**AND** the fare charged equals the fares-export price for that product"
        ),
        f"A {prod} ticket is issued at its fares-export price.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
    ))

advance_3day_cases = []  # section 887784
advance_3day_cases += payment_split(
    "3-Day — a 3-day ticket is issued",
    ["FBD-100336"],
    "This test is to confirm the customer can buy a 3-day ticket at the fares-export price, paying by {pay}.",
    (
        "**GIVEN** a TVM showing the 3-day product\n"
        "**AND** an example Adult 3-Day ticket priced per the fares export"
    ),
    "a 3-day ticket is printed",
    "the fare charged equals the fares-export 3-day price",
    "A 3-day ticket is issued at its fares-export price, paying by {pay}.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
)

rail_xborder_cases = []  # section 887785 (Rail & Cross-Border, Kiosk)

rail_xborder_cases += payment_split(
    "NI Rail — Adult single between two stations",
    ["FBD-100450", "FBD-100207"],
    "This test is to confirm a Kiosk in NIR-Rail mode issues an Adult rail single between the selected from and to stations, paying by {pay}.",
    (
        "**GIVEN** a Kiosk in NIR-Rail mode showing the rail from/to station selection\n"
        "**AND** an example Adult single from Belfast Lanyon Place to Portadown priced per the NIR fares export"
    ),
    "an Adult rail single is printed for the selected stations",
    "the fare charged equals the NIR fares-export single fare",
    "A Kiosk issues an Adult NI rail single between the selected stations at the NIR fares-export fare, paying by {pay}.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
)

rail_xborder_cases += payment_split(
    "NI Rail — 3-Day Select ticket",
    ["FBD-100450", "FBD-100167"],
    "This test is to confirm a Kiosk issues a rail 3-Day Select ticket valid on three selected dates, paying by {pay}.",
    (
        "**GIVEN** a Kiosk in NIR-Rail mode showing the 3-Day Select product\n"
        "**AND** an example Adult 3-Day Select between Belfast Lanyon Place and Portadown priced per the NIR fares export"
    ),
    "a 3-Day Select ticket is printed",
    "the printed validity reflects the 3-Day Select date rule",
    "A rail 3-Day Select ticket is issued with its selectable-date validity, paying by {pay}.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
)

rail_xborder_cases += payment_split(
    "Cross-Border — Adult single",
    ["FBD-100450", "FBD-100207"],
    "This test is to confirm a Kiosk issues a Cross-Border Adult single between a NI and a cross-border station, paying by {pay}.",
    (
        "**GIVEN** a Kiosk in NIR-Rail mode showing cross-border stations\n"
        "**AND** an example Cross-Border Adult single from Newry to Dundalk priced per the NIR fares export"
    ),
    "a Cross-Border Adult single is printed for the selected stations",
    "the fare charged equals the NIR fares-export cross-border single fare",
    "A Cross-Border single is issued between the selected NI and cross-border stations at the fares-export fare, paying by {pay}.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
)

# C4103697: product axis (Day Return / Weekly / Monthly / 1/3-off Day Return / Day Tracker) — 5-way.
PRODUCTS_697 = ["Day Return", "Weekly", "Monthly", "1/3-off Day Return", "Day Tracker"]
orig_697 = "NI Rail — Day Return, Weekly and Monthly products"
for i, prod in enumerate(PRODUCTS_697):
    rail_xborder_cases.append(case(
        orig_697 if i == 0 else None,
        f"NI Rail — {prod} ticket",
        ["FBD-100450"],
        f"This test is to confirm a Kiosk issues a NI rail {prod} product at the fares-export price.",
        (
            "**GIVEN** a Kiosk in NIR-Rail mode with stations selected\n"
            f"**AND** an example Adult {prod} from Belfast Lanyon Place to Portadown priced per the NIR fares export\n"
            f"**WHEN** the customer selects the {prod} product and pays\n"
            f"**THEN** the {prod} ticket is printed for the stations\n"
            "**AND** the fare charged equals the NIR fares-export price for that product"
        ),
        f"A NI rail {prod} product is issued at its NIR fares-export price.\n\n[Automatable: Partial]",
    ))

# C4103700: product axis (Day Return / Weekly / Monthly / 1 Month Return) — 4-way.
PRODUCTS_700 = ["Day Return", "Weekly", "Monthly", "1 Month Return"]
orig_700 = "Cross-Border — Return, Monthly and 1-Month-Return products"
for i, prod in enumerate(PRODUCTS_700):
    rail_xborder_cases.append(case(
        orig_700 if i == 0 else None,
        f"Cross-Border — {prod} ticket",
        ["FBD-100450"],
        f"This test is to confirm a Kiosk issues a Cross-Border {prod} product at the fares-export price.",
        (
            "**GIVEN** a Kiosk in NIR-Rail mode with cross-border stations selected\n"
            f"**AND** an example Cross-Border Adult {prod} from Newry to Dundalk priced per the NIR fares export\n"
            f"**WHEN** the customer selects the {prod} product and pays\n"
            f"**THEN** the {prod} cross-border ticket is printed\n"
            "**AND** the fare charged equals the NIR fares-export price for that product"
        ),
        f"A Cross-Border {prod} product is issued at its fares-export price.\n\n[Automatable: Partial]",
    ))

# C4103701: product axis (Single / 1 Month Return) — 2-way.
PRODUCTS_701 = ["Single", "1 Month Return"]
orig_701 = "Cross-Border — 1st Class ticket"
for i, prod in enumerate(PRODUCTS_701):
    rail_xborder_cases.append(case(
        orig_701 if i == 0 else None,
        f"Cross-Border — 1st Class {prod}",
        ["FBD-100450"],
        f"This test is to confirm a Kiosk issues a 1st Class Cross-Border {prod} at the 1st Class fares-export price.",
        (
            "**GIVEN** a Kiosk in NIR-Rail mode showing 1st Class cross-border products\n"
            f"**AND** an example 1st Class Cross-Border Adult {prod} priced per the NIR fares export\n"
            f"**WHEN** the customer buys the 1st Class {prod} and pays\n"
            f"**THEN** a 1st Class Cross-Border {prod} ticket is printed\n"
            "**AND** the fare charged equals the NIR fares-export 1st Class price"
        ),
        f"A 1st Class Cross-Border {prod} is issued at the 1st Class fares-export price.\n\n[Automatable: Partial]",
    ))

# C4103702: concession axis (Senior / ROI Senior / Blind / War Pensioner / 60+) — 5-way.
CONCESSIONS = ["Senior", "ROI Senior", "Blind", "War Pensioner", "60+"]
orig_702 = "NI Rail — concessionary single"
for i, conc in enumerate(CONCESSIONS):
    rail_xborder_cases.append(case(
        orig_702 if i == 0 else None,
        f"NI Rail — {conc} concessionary single",
        ["FBD-100450"],
        f"This test is to confirm a Kiosk issues a rail concessionary single at the {conc} concessionary price.",
        (
            "**GIVEN** a Kiosk in NIR-Rail mode showing rail concessionary products\n"
            f"**AND** an example {conc} concessionary single from Belfast Lanyon Place to Portadown priced per the NIR fares export\n"
            f"**WHEN** the customer buys a {conc} concessionary single and pays\n"
            "**THEN** a concessionary single ticket is printed\n"
            "**AND** the fare charged equals the NIR fares-export concessionary price"
        ),
        f"A rail {conc} concessionary single is issued at its fares-export concessionary price.\n\n[Automatable: Partial]",
    ))

# C4103691: keep AS-IS + 1 new sibling for the multi-use-barcode exception (genuinely distinct
# behaviour, not a same-behaviour value list — per the changelog's own note).
ticket_issue_cases.append(case(
    None,
    "Ticket Issue — issued ticket carries a single-use barcode",
    ["FBD-100167", "FBD-100317 (old suite C3544955-C3544968 Rail multi-use barcode issuance; gap-register Q10; consolidation-completeness audit 2026-07-23)"],
    "This test is to confirm a printed ticket carries a single-use barcode when the ticket type has barcode printing enabled.",
    (
        "**GIVEN** a TVM issuing a product whose ticket type has barcode printing enabled in CloudFare\n"
        "**AND** an example Metro Adult Single from 10A (IN) Casement Park to City Hall\n"
        "**WHEN** the customer completes the purchase\n"
        "**THEN** a single-use barcode is printed at the end of the ticket"
    ),
    "A ticket for a barcode-enabled product prints a single-use barcode at the end of the ticket.\n\n[Automatable: Partial — Cross-check: CloudFare / MERIT]",
))
ticket_issue_cases.append(case(
    None,
    "Ticket Issue — Cross Border, Family & Friends and concession rail products print a multi-use barcode",
    ["FBD-100167", "FBD-100317 (old suite C3544955-C3544968 Rail multi-use barcode issuance; gap-register Q10; consolidation-completeness audit 2026-07-23)"],
    "This test is to confirm a Cross Border, Family & Friends or concession rail product prints a multi-use-type barcode for redemption elsewhere, in contrast to the single-use barcode on the standard product (see the sibling single-use-barcode case).",
    (
        "**GIVEN** a TVM issuing a Cross Border, Family & Friends or concession rail product whose ticket type has barcode printing enabled in CloudFare\n"
        "**AND** an example NI Rail Cross-Border Adult single from Newry to Dundalk\n"
        "**WHEN** the customer completes the purchase\n"
        "**THEN** a multi-use-type barcode is printed at the end of the ticket\n"
        "**AND** the TVM cannot itself validate that multi-use barcode presented back to it (the restriction is on read-back, not on printing)"
    ),
    "A Cross Border / Family & Friends / concession rail product prints a multi-use barcode for redemption elsewhere; the TVM does not read that barcode type back.\n\n[Automatable: Partial — Cross-check: CloudFare / MERIT]",
))


def write_family(stem, header, sections):
    doc = {
        "suite": "**NEW** TVM Test Suite",
        "suite_id": 30284,
        "defaults": DEFAULTS,
        "sections": sections,
    }
    out = HERE / f"{stem}.cases.yaml"
    out.write_text(header + "\n" + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")
    print(f"{stem}: {sum(len(s['cases']) for s in sections)} cases -> {out}")


write_family(
    "tvm-variant-expansion-2-sales",
    "# TVM variant expansion, follow-up batch 2026-07-24 — Sales - Tickets: Ticket Issue (887783),\n"
    "# Advance & 3-Day (887784), Rail & Cross-Border / Kiosk (887785). Payment-method split (3-way)\n"
    "# for cases where payment is the only in-scope data axis; product/concession-type split where\n"
    "# that is the named axis instead (not crossed with payment). Mode/model axes are UNCHANGED\n"
    "# (Configurations). See tvm-variant-expansion-2.changelog.md for the full rationale.",
    [
        {"path": ["Functional", "Sales - Tickets", "Ticket Issue"], "cases": ticket_issue_cases},
        {"path": ["Functional", "Sales - Tickets", "Advance & 3-Day"], "cases": advance_3day_cases},
        {"path": ["Functional", "Sales - Tickets", "Rail & Cross-Border (Kiosk)"], "cases": rail_xborder_cases},
    ],
)

print("ticket_issue:", len(ticket_issue_cases), "advance_3day:", len(advance_3day_cases), "rail_xborder:", len(rail_xborder_cases))
print("TOTAL:", len(ticket_issue_cases) + len(advance_3day_cases) + len(rail_xborder_cases))
