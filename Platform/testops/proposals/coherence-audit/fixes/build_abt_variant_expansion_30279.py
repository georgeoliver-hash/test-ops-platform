"""Build the "Data variations:" -> one-case-per-variant expansion for suite 30279 (ABT-only),
per George's 2026-07-24 hard rule: "no test should tell someone to test multiple variants...
we should have a test for each." Every case found carrying a trailing `Data variations:` line
gets expanded so each named variant is its own separate, individually-executable case. The
first/primary variant reuses the original case id (retitled + reworded); the remaining variants
become new cases in the same section.

9 families found in suite 30279 (full-suite grep for "data variation"/"variations:", case body
incl. title/preface/preconds/steps/expected, excluding ZZ_DELETE_*):
  - C4102852 Debt Recovery cadence            -> Visa / Mastercard / Maestro      (3)
  - C4102857 Access — portal claims           -> Account Mgmt / Admin / Capping / Reports (4)
  - C4102871 Transfers — Metro/Glider £0.00   -> Scenario 1 / 3 / 2+4 / 11        (4)
  - C4102894 EMV Summary Report               -> Visa / MasterCard / Maestro      (3)
  - C4102908 Retail Debt Report                -> Visa / Mastercard / Maestro      (3)
  - C4102937 Issuer Liability Threshold        -> Visa / Mastercard / Maestro      (3)
  - C4102939 Pre-auth, first daily use         -> Mastercard / Maestro             (2)
  - C4102940 Pre-auth, after Deny List removal -> Mastercard / Maestro             (2)
  - C4102954 Declined Taps Report reasons      -> 6 DeclinedReason codes           (6)

Writes:
  - abt-variant-expansion-30279.rewrite.json    (9 primary-case updates, for apply_rewrite.py)
  - abt-variant-expansion-30279.new-cases.json  (21 new-case rows, for the push script)
"""
from __future__ import annotations
import json
from pathlib import Path

OUT = Path(__file__).parent

TAG = "\n\n[Automatable: {auto} · Cross-check: {check}]"

rewrite_rows = []   # primary-case updates (id, title, preface, preconds, steps, expected, refs)
new_rows = []        # new cases (section_id, title, preface, preconds, steps, expected, refs, devtypes, priority)


def add_primary(cid, title, preface, preconds, steps, expected, refs):
    rewrite_rows.append({
        "id": cid, "title": title, "preface": preface, "preconds": preconds,
        "steps": steps, "expected": expected, "refs": refs,
    })


def add_new(section_id, title, preface, preconds, steps, expected, refs, priority_id=1, devtypes=None):
    new_rows.append({
        "section_id": section_id, "title": title, "preface": preface, "preconds": preconds,
        "steps": steps, "expected": expected, "refs": refs, "priority_id": priority_id,
        "custom_devtypes": devtypes or [200],
    })


# ------------------------------------------------------------------ #
# 1. C4102852 — Debt Recovery cadence: Visa / Mastercard / Maestro
# ------------------------------------------------------------------ #
SEC_852 = 887585
CADENCE = {
    "Visa": "Visa: six attempts within 14 days, UK/IntraEU/International",
    "Mastercard": "Mastercard: one attempt per day for a month, retried at 4/14/28 days, UK/International",
    "Maestro": "Maestro: same schedule as Mastercard — one attempt per day for a month, retried at 4/14/28 days",
}
for scheme in ("Visa", "Mastercard", "Maestro"):
    title = f"Debt Recovery — automated {scheme} recovery clears a recoverable issuer-liability debt"
    preface = (f"This test is to confirm that scheduled automated {scheme} recovery clears a "
               f"recoverable issuer-liability debt and removes the token from the deny list.")
    preconds = (
        f"**GIVEN** the seeded test account has an EndOfDay authorisation failure and a recoverable "
        f"debt within the issuer-liability threshold, on a {scheme} card\n"
        "**AND** the account is currently blocked and its token is on the ABT Deny List\n"
        "**AND** you are signed in to the ABT Operator Portal on the Customers page"
    )
    steps = [{
        "content": (f"**WHEN** the scheduled automated re-authorisation cycles run "
                    f"({CADENCE[scheme]}) and re-collect the debt\n"
                    "**AND** you refresh the account in the Operator Portal"),
        "expected": ("**THEN** the account is no longer blocked in the Operator Portal\n"
                     "**AND** the account's token no longer appears on the Deny List"),
    }]
    expected = (f"Scheduled {scheme} recovery re-collects the issuer-liability debt; the account is "
                "unblocked and removed from the Deny List." + TAG.format(auto="Yes", check="CloudFare / MERIT"))
    refs = "PSPEC-0015 (Automatic Debt Recovery cadence, para ~11493-11504),TODEV-24990"
    if scheme == "Visa":
        add_primary(4102852, title, preface, preconds, steps, expected, refs)
    else:
        add_new(SEC_852, title, preface, preconds, steps, expected, refs)


# ------------------------------------------------------------------ #
# 2. C4102857 — Access claims: Account Management / Admin / Capping / Reports
# ------------------------------------------------------------------ #
SEC_857 = 887588
CLAIM_GROUPS = {
    "Account Management": "ReadOnly / CreateReadUpdate / Full, DebtRecovery, EPurseBalanceAdjustmentApproval, "
                            "RefundApproval, RefundAuthorisation, UpdateMediaStatus, TransactionsReadAccess, "
                            "JourneyHistoryColumns",
    "Admin": "AdminReadAccess / AdminFullAccess, EPurseReadAccess, ReceiptConfiguration, AdminRouteGroups",
    "Capping": "BusinessRulesReadAccess / CreateEdit / FullAccess",
    "Reports": "AccountStatus, ActionList, Audit, DeclinedCardTap, EPurseBalance, LateTap, RevenueByMid, "
               "RevenueInspection (each *ReadAccess)",
}
for group in ("Account Management", "Admin", "Capping", "Reports"):
    title = f"Access — portal tasks match the operator's assigned {group} claims"
    preface = (f"This test is to confirm that the {group} functions available in the ABT Operator "
               f"Portal are limited to the {group} claims assigned to the signed-in user's KeyCloak "
               "user group.")
    preconds = (
        f"**GIVEN** two operators exist in the Translink realm, each assigned to a different KeyCloak "
        f"user group whose {group} composite claims differ ({CLAIM_GROUPS[group]})\n"
        "**AND** the ABT Operator Portal (operator-react-client) sign-on page is displayed"
    )
    steps = [{
        "content": "**WHEN** each operator signs on with their Active Directory credentials",
        "expected": (f"**THEN** each operator sees only the {group} portal functions granted by their "
                     "group's composite claims\n**AND** functions not granted by their claims are not "
                     "available to them"),
    }]
    expected = (f"Each user's {group} tasks match their configured access rights." +
                TAG.format(auto="Yes", check="CloudFare / MERIT"))
    refs = "FBD-100342"
    if group == "Account Management":
        add_primary(4102857, title, preface, preconds, steps, expected, refs)
    else:
        add_new(SEC_857, title, preface, preconds, steps, expected, refs)


# ------------------------------------------------------------------ #
# 3. C4102871 — Transfers: Scenario 1 / 3 / 2+4 / 11 (FBD-100651 §7.4)
# ------------------------------------------------------------------ #
SEC_871 = 887591

# Primary: Scenario 1 (kept as the original real worked example; malformed EXPECTED text
# — the misplaced "Data variations" paragraph — is removed, leaving only the true expected result).
add_primary(
    4102871,
    "Transfers — a qualifying Directional feeder-to-Glider transfer is charged £0.00 (Scenario 1)",
    "This test is to confirm that a qualifying Directional feeder-to-Glider transfer is charged "
    "£0.00 rather than a normal fare, per the Glider transfer logic (CR123).",
    "**GIVEN** the seeded ABT test card makes two consecutive taps within the configured transfer "
    "time (e.g. 90 minutes) — a Directional feeder tap that is charged, then a Glider tap in the "
    "same direction whose TransferRouteType flag is not \"None\"\n"
    "**AND** example (Scenario 1, \"Dir Fdr to GL\"): an Inbound tap on Ulsterbus feeder route G10D, "
    "followed by an Inbound tap on Glider East within the transfer window\n"
    "**AND** you are signed in to the ABT Operator Portal to verify the card's Journey History",
    [{
        "content": ("**WHEN** the two taps are matched as a transfer and the EndOfDay settlement runs\n"
                    "**AND** you open the card's Journey History"),
        "expected": ("**THEN** the first (feeder) tap is charged its normal fare\n"
                     "**AND** the second (Glider) tap is charged £0.00 and shown with the transfer icon\n"
                     "**AND** the transfer tap is sent to MERIT under the transfer product, not the "
                     "standard ABT product"),
    }],
    "A qualifying Metro/Glider transfer tap is charged £0.00 and recorded as a transfer, while the "
    "originating tap is charged normally.",
    "FBD-100651 §7.4 (Scenario 1)",
)

add_new(
    SEC_871,
    "Transfers — a qualifying Non-Directional feeder-to-Glider transfer is charged £0.00 (Scenario 3)",
    "This test is to confirm that a qualifying Non-Directional feeder-to-Glider transfer is charged "
    "£0.00 rather than a normal fare, per the Glider transfer logic (CR123).",
    "**GIVEN** the seeded ABT test card makes two consecutive taps within the configured transfer "
    "time (e.g. 90 minutes) — a Non-Directional feeder tap that is charged, then a Glider tap whose "
    "TransferRouteType flag is not \"None\" (no RouteDirection match required for a Non-Directional tap)\n"
    "**AND** **GAP** — no worked route example cited for Scenario 3; confirm a live Non-Directional "
    "feeder route before running\n"
    "**AND** you are signed in to the ABT Operator Portal to verify the card's Journey History",
    [{
        "content": ("**WHEN** the two taps are matched as a transfer and the EndOfDay settlement runs\n"
                    "**AND** you open the card's Journey History"),
        "expected": ("**THEN** the first (feeder) tap is charged its normal fare\n"
                     "**AND** the second (Glider) tap is charged £0.00 and shown with the transfer icon\n"
                     "**AND** the transfer tap is sent to MERIT under the transfer product, not the "
                     "standard ABT product"),
    }],
    "A qualifying Metro/Glider transfer tap is charged £0.00 and recorded as a transfer, while the "
    "originating tap is charged normally.",
    "FBD-100651 §7.4 (Scenario 3)",
)

add_new(
    SEC_871,
    "Transfers — a qualifying Glider-to-feeder transfer is charged £0.00 (Scenarios 2/4)",
    "This test is to confirm that a qualifying Glider-to-feeder transfer is charged £0.00 rather "
    "than a normal fare, per the Glider transfer logic (CR123).",
    "**GIVEN** the seeded ABT test card makes two consecutive taps within the configured transfer "
    "time (e.g. 90 minutes) — a Glider tap that is charged, then a feeder tap whose TransferRouteType "
    "flag is not \"None\"\n"
    "**AND** **GAP** — no worked route example cited for Scenarios 2/4; confirm a live Glider-to-feeder "
    "pairing before running\n"
    "**AND** you are signed in to the ABT Operator Portal to verify the card's Journey History",
    [{
        "content": ("**WHEN** the two taps are matched as a transfer and the EndOfDay settlement runs\n"
                    "**AND** you open the card's Journey History"),
        "expected": ("**THEN** the first (Glider) tap is charged its normal fare\n"
                     "**AND** the second (feeder) tap is charged £0.00 and shown with the transfer icon\n"
                     "**AND** the transfer tap is sent to MERIT under the transfer product, not the "
                     "standard ABT product"),
    }],
    "A qualifying Metro/Glider transfer tap is charged £0.00 and recorded as a transfer, while the "
    "originating tap is charged normally.",
    "FBD-100651 §7.4 (Scenarios 2,4)",
)

add_new(
    SEC_871,
    "Transfers — a qualifying Ulsterbus-to-Glider transfer is charged £0.00 (Scenario 11)",
    "This test is to confirm that a qualifying Ulsterbus-to-Glider transfer (transfers enabled) is "
    "charged £0.00 rather than a normal fare, per the Glider transfer logic (CR123).",
    "**GIVEN** the seeded ABT test card makes two consecutive taps within the configured transfer "
    "time (e.g. 90 minutes) on an Ulsterbus route with transfers enabled — a feeder tap that is "
    "charged, then a Glider tap whose TransferRouteType flag is not \"None\"\n"
    "**AND** **GAP** — no worked route example cited for Scenario 11; confirm a live Ulsterbus "
    "transfers-enabled route before running\n"
    "**AND** you are signed in to the ABT Operator Portal to verify the card's Journey History",
    [{
        "content": ("**WHEN** the two taps are matched as a transfer and the EndOfDay settlement runs\n"
                    "**AND** you open the card's Journey History"),
        "expected": ("**THEN** the first (feeder) tap is charged its normal fare\n"
                     "**AND** the second (Glider) tap is charged £0.00 and shown with the transfer icon\n"
                     "**AND** the transfer tap is sent to MERIT under the transfer product, not the "
                     "standard ABT product"),
    }],
    "A qualifying Metro/Glider transfer tap is charged £0.00 and recorded as a transfer, while the "
    "originating tap is charged normally.",
    "FBD-100651 §7.4 (Scenario 11)",
)


# ------------------------------------------------------------------ #
# 4. C4102894 — EMV Summary Report: Visa / MasterCard / Maestro
# ------------------------------------------------------------------ #
SEC_894 = 887593
for scheme in ("Visa", "MasterCard", "Maestro"):
    title = f"EMV Summary Report — {scheme}"
    preface = ("**UNCONFIRMED** — not named in the seven governing ABT/BOS reporting specs; confirm "
               "it exists on the live portal before running.")
    preconds = ("**GIVEN** an operator is signed into the Operator Web Portal\n"
                "**AND** the Reports page is displayed")
    steps = [{
        "content": "**WHEN** the operator runs the EMV Summary Report for a date range",
        "expected": (
            "**THEN** the report is generated\n"
            f"**AND** it is displayed with Open Payment totals for {scheme}\n"
            "**AND** it can be exported (PDF / XLS / CSV)\n"
            "**AND** KPI headings shown: Total EMV Payments, Total EMV Revenue, Total EMV Declines, "
            "Total EMV Decline Value, Total Decline Percentage\n"
            "**AND** row detail shown: Decline Reason, BIN range, Issuer, Quantity, Value, Decline Percentage"
        ),
    }]
    expected = (f"The EMV Summary Report generates, displays and can be exported, with Open Payment "
                f"details for {scheme}." + TAG.format(auto="Partial", check="CloudFare / MERIT"))
    refs = "FBD-100387 para 218,REQ-2662.1,REQ-3457,REQ-3491,OldSuite-C2665801,OldSuite-C2817603,OldSuite-C2879324"
    if scheme == "Visa":
        add_primary(4102894, title, preface, preconds, steps, expected, refs)
    else:
        add_new(SEC_894, title, preface, preconds, steps, expected, refs)


# ------------------------------------------------------------------ #
# 5. C4102908 — Retail Debt Report: Visa / Mastercard / Maestro
# ------------------------------------------------------------------ #
SEC_908 = 887593
DEBT_REFS = {
    "Visa": "FBD-100387 para 218,OldSuite-C2880099,CA-13549",
    "Mastercard": "FBD-100387 para 218,OldSuite-C2880099,CA-13549",
    "Maestro": "FBD-100387 para 218,OldSuite-C2880099,TODEV-15538,TODEV-11567",
}
for scheme in ("Visa", "Mastercard", "Maestro"):
    title = f"Retail Debt Report — {scheme}"
    preface = ("**UNCONFIRMED** — not named in the seven governing ABT/BOS reporting specs; confirm "
               "it exists on the live portal before running.")
    preconds = ("**GIVEN** an operator is signed into the Operator Web Portal\n"
                "**AND** the Reports page is displayed")
    steps = [{
        "content": "**WHEN** the operator runs the Retail Debt Report",
        "expected": (
            "**THEN** the report is generated\n"
            f"**AND** it is displayed with the Retail Debt Summary for {scheme} (value and percentage)\n"
            "**AND** it can be exported (PDF / XLS / CSV)\n"
            "**AND** row detail shown: Date/Time, Automatic Debt Retries, Remaining, Amount, Brand, "
            "Masked PAN, Transaction Reference"
        ),
    }]
    expected = (f"The Retail Debt Report generates, displays and can be exported, with debt shown for "
                f"{scheme} (value and percentage)." + TAG.format(auto="Yes", check="CloudFare / MERIT"))
    refs = DEBT_REFS[scheme]
    if scheme == "Visa":
        add_primary(4102908, title, preface, preconds, steps, expected, refs)
    else:
        add_new(SEC_908, title, preface, preconds, steps, expected, refs)


# ------------------------------------------------------------------ #
# 6. C4102937 — Issuer Liability Threshold: Visa / Mastercard / Maestro
# ------------------------------------------------------------------ #
SEC_937 = 887599
ILT_OLDID = {"Visa": "OldSuite-C2665815", "Mastercard": "OldSuite-C2665816", "Maestro": "OldSuite-C2665817"}
for scheme in ("Visa", "Mastercard", "Maestro"):
    title = f"Card Verification — declined {scheme} payments are guaranteed up to the Issuer Liability Threshold"
    preface = (f"This test is to confirm that a declined {scheme} payment not recovered from the "
               "customer is guaranteed by the card issuer up to the Issuer Liability Threshold (UK "
               "threshold £10.00).")
    preconds = (f"**GIVEN** a seeded ABT test cEMV {scheme} card is available\n"
                "**AND** a transaction was made that failed authorisation for payment\n"
                "**AND** you can verify the outcome in CloudFare env5")
    steps = [{
        "content": "**WHEN** the declined payment is not recovered from the customer",
        "expected": ("**THEN** in CloudFare the card issuer guarantees the payment up to the Issuer "
                     "Liability Threshold (£10.00 in the UK)\n"
                     "**AND** amounts within the threshold are cleared under issuer liability / "
                     "chargeback protection"),
    }]
    expected = (f"Unrecovered declined {scheme} payments are guaranteed by the issuer up to the "
                "liability threshold." + TAG.format(auto="Partial", check="CloudFare"))
    refs = ("PSPEC-0015 §4.7.3 (Issuer Liability/Chargeback Protection, para ~10920-10931, "
            f"13295-13412),REQ-3354,{ILT_OLDID[scheme]}")
    if scheme == "Visa":
        add_primary(4102937, title, preface, preconds, steps, expected, refs)
    else:
        add_new(SEC_937, title, preface, preconds, steps, expected, refs)


# ------------------------------------------------------------------ #
# 7/8. C4102939 / C4102940 — Pre-auth: Mastercard / Maestro
# ------------------------------------------------------------------ #
PREAUTH = {
    4102939: {
        "label": "first daily use",
        "cond": "that has not yet transacted today",
        "when": "**WHEN** you tap the card to make the first transaction of the day on the ETM",
        "req": {"Mastercard": ("REQ-3360", "OldSuite-C2665819"), "Maestro": ("REQ-3361", "OldSuite-C2665821")},
    },
    4102940: {
        "label": "first use after Deny List removal",
        "cond": "that has just been removed from the Deny List",
        "when": "**WHEN** you next tap the card to make a transaction on the ETM",
        "req": {"Mastercard": ("REQ-3360", "OldSuite-C2665820"), "Maestro": ("REQ-3361", "OldSuite-C2665822")},
    },
}
SEC_939 = 887599
for cid, spec in PREAUTH.items():
    for scheme in ("Mastercard", "Maestro"):
        req, oldid = spec["req"][scheme]
        title = f"Card Verification — {spec['label']} of a {scheme} card triggers a pre-authorisation"
        preface = (f"This test is to confirm that a pre-authorisation is performed on the {spec['label']} "
                   f"of a {scheme} card.")
        preconds = (f"**GIVEN** a seeded ABT test cEMV {scheme} card {spec['cond']}\n"
                    "**AND** an in-service ETM signed on to a route\n"
                    "**AND** you can verify the outcome in CloudFare env5")
        steps = [{
            "content": spec["when"],
            "expected": "**THEN** in CloudFare a pre-authorisation is performed",
        }]
        expected = (f"A Pre-Authorisation check is performed on the {spec['label']} of a {scheme} card." +
                    TAG.format(auto="Partial", check="CloudFare"))
        refs = f"PSPEC-0015 §4.6 (para ~10548-10550),{req},{oldid}"
        if scheme == "Mastercard":
            add_primary(cid, title, preface, preconds, steps, expected, refs)
        else:
            add_new(SEC_939, title, preface, preconds, steps, expected, refs)


# ------------------------------------------------------------------ #
# 9. C4102954 — Declined Taps Report: 6 DeclinedReason codes
# ------------------------------------------------------------------ #
SEC_954 = 887602
REASONS = [
    (1, "Card Expired", "an expired card"),
    (2, "On Deny List", "a Deny-listed card"),
    (3, "Declined/ODA", "an ODA/authenticity failure"),
    (4, "Cancelled", "a cancelled tap"),
    (15, "On BIN List", "a BIN-listed card"),
    (20, "Passback/Negative List", "a passback (Negative List)"),
]
for code, label, cause in REASONS:
    title = f"Declined taps — {cause} (DeclinedReason {code}) is recorded on the Declined Taps Report"
    preface = f"This test is to confirm a decline caused by {cause} is recorded with reason {label} on the Declined Taps Report."
    preconds = (f"**GIVEN** a declined card tap has occurred for {cause} (DeclinedReason {code}, {label})\n"
                "**AND** the user is signed into the ABT Operator Portal with the report claim for "
                "declined card taps")
    steps = [{
        "content": "**WHEN** the user opens the Declined Taps Report for the test period",
        "expected": (f"**THEN** the declined tap is listed with decline reason {label} (DeclinedReason "
                     f"{code}, per the FBD-100658 DeclinedReason enum)\n"
                     "**AND** the reason recorded matches the failure that caused the decline\n"
                     "**AND** **UNCONFIRMED** — exact on-screen label string not pinned to a spec; "
                     "confirm against live"),
    }]
    expected = (f"The declined tap for {cause} is listed on the Declined Taps Report with reason "
                f"{label} (DeclinedReason {code})." + TAG.format(auto="Partial", check="CloudFare / MERIT"))
    refs = "FBD-100658,OldSuite-C3211528"
    if code == 1:
        add_primary(4102954, title, preface, preconds, steps, expected, refs)
    else:
        add_new(SEC_954, title, preface, preconds, steps, expected, refs)


# ------------------------------------------------------------------ #
def main():
    (OUT / "abt-variant-expansion-30279.rewrite.json").write_text(
        json.dumps(rewrite_rows, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    (OUT / "abt-variant-expansion-30279.new-cases.json").write_text(
        json.dumps(new_rows, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"Built {len(rewrite_rows)} primary-case updates + {len(new_rows)} new cases.")


if __name__ == "__main__":
    main()
