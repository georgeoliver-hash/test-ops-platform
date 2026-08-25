"""Build the follow-up TVM Data-variations expansion — Payments - Cash (887777/887778/887843)."""
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


def write_family(stem, header, section_path, cases):
    doc = {
        "suite": "**NEW** TVM Test Suite",
        "suite_id": 30284,
        "defaults": DEFAULTS,
        "sections": [{"path": section_path, "cases": cases}],
    }
    out = HERE / f"{stem}.cases.yaml"
    out.write_text(header + "\n" + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")
    print(f"{stem}: {len(cases)} cases -> {out}")


cash_cases = []
REF_339 = ["REQ-0339.12"]

# C4103637: coin denomination (old round £1 / 2p / 1p) — 3-way. Primary = old round £1 (first named,
# and the case's title already foregrounds it as "out-of-circulation").
COINS = [
    ("old round £1", "an out-of-circulation round £1 coin"),
    ("2p", "an out-of-circulation 2p coin below the accepted denominations"),
    ("1p", "an out-of-circulation 1p coin below the accepted denominations"),
]
orig_637 = "Coins — out-of-circulation and sub-value coins are rejected"
for i, (label, precond_action) in enumerate(COINS):
    cash_cases.append(case(
        orig_637 if i == 0 else None,
        f"Coins — out-of-circulation and sub-value coins are rejected ({label})",
        ["REQ-0339.12 (TFTS Requirements Matrix, Signed-Off; Q34 resolved)"],
        f"This test is to confirm the TVM rejects a {label} coin as out of circulation or below the accepted denominations.",
        (
            "**GIVEN** a TVM is at the payment screen for a cash transaction\n"
            f"**WHEN** the customer inserts {precond_action}\n"
            "**THEN** the coin is rejected\n"
            "**AND** the coin is returned to the tray\n"
            "**AND** the amount paid is unchanged"
        ),
        f"A {label} coin is rejected and returned; the amount paid is unchanged.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
    ))

# C4103638: foreign-currency class (Euro / other) — 2-way.
orig_638 = "Coins — foreign coins are rejected"
FOREIGN = [("Euro", "a Euro coin"), ("other non-sterling", "a non-Euro foreign coin")]
for i, (label, precond_action) in enumerate(FOREIGN):
    cash_cases.append(case(
        orig_638 if i == 0 else None,
        f"Coins — foreign coins are rejected ({label})",
        ["REQ-0339.12 (TFTS Requirements Matrix, Signed-Off; Q34 resolved)"],
        f"This test is to confirm the TVM rejects a {label} coin as not sterling currency.",
        (
            "**GIVEN** a TVM is at the payment screen for a cash transaction\n"
            f"**WHEN** the customer inserts {precond_action}\n"
            "**THEN** the coin is rejected\n"
            "**AND** the coin is returned to the tray\n"
            "**AND** the amount paid is unchanged"
        ),
        f"A {label} coin is rejected and returned; the amount paid is unchanged.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
    ))

# C4103639: issuing bank (BoE / BoI / Ulster / Danske / First Trust) — 5-way. Primary = BoE (matches
# original's £5 polymer example).
BANKS = ["Bank of England", "Bank of Ireland", "Ulster Bank", "Danske Bank (Northern Bank)", "First Trust Bank"]
orig_639 = "Banknotes — a valid banknote in any orientation pays for a transaction"
for i, bank in enumerate(BANKS):
    cash_cases.append(case(
        orig_639 if i == 0 else None,
        f"Banknotes — a valid banknote in any orientation pays for a transaction ({bank})",
        ["REQ-0339.4 (TFTS Requirements Matrix, Signed-Off; Q34 resolved)"],
        f"This test is to confirm the TVM accepts a valid {bank} banknote in all four insertion orientations.",
        (
            "**GIVEN** a TVM is at the payment screen for a cash transaction\n"
            f"**AND** a valid {bank} £5 banknote is to be used\n"
            "**WHEN** the customer inserts the banknote\n"
            "**THEN** the banknote is accepted in any of the four orientations\n"
            "**AND** the amount paid increases by £5.00"
        ),
        f"A valid {bank} banknote is accepted in all four orientations.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
    ))

# C4103640: withdrawn-note denomination (£5/£10/£20) — 3-way. Primary matches original (£10).
WITHDRAWN = ["£5", "£10", "£20"]
orig_640 = "Banknotes — withdrawn paper notes are rejected"
for i, denom in enumerate(WITHDRAWN):
    is_primary = denom == "£10"
    cash_cases.append(case(
        orig_640 if is_primary else None,
        f"Banknotes — withdrawn paper notes are rejected ({denom})",
        ["REQ-0339.14 (TFTS Requirements Matrix, Signed-Off; Q34 resolved)"],
        f"This test is to confirm the TVM rejects an old paper {denom} note that has been withdrawn from circulation.",
        (
            "**GIVEN** a TVM is at the payment screen for a cash transaction\n"
            f"**WHEN** the customer inserts an old paper {denom} note that has been withdrawn\n"
            "**THEN** the note is rejected\n"
            "**AND** the note is returned to the customer\n"
            "**AND** the customer can complete payment with valid currency"
        ),
        f"A withdrawn paper {denom} note is rejected while valid currency still completes the sale.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
    ))
# reorder so £10 (the primary/match) comes first, matching the pattern used elsewhere
cash_cases_640 = [c for c in cash_cases if "withdrawn paper notes are rejected" in c["title"]]

# C4103641: keep AS-IS (Scottish accepted) + 1 new (non-sterling banknote rejected)
cash_cases.append(case(
    None,
    "Banknotes — a Scottish banknote is accepted as valid sterling",
    ["REQ-0339.0", "REQ-1491.0 (TFTS Requirements Matrix, Signed-Off; Q34 resolved, Q15 already fixed expected outcome)"],
    "This test is to confirm the TVM accepts a Scottish-issued banknote as valid sterling currency, the same as a Bank of England note.",
    (
        "**GIVEN** a TVM is at the payment screen for a cash transaction\n"
        "**AND** a valid Scottish-issued banknote (e.g. Bank of Scotland / RBS / Clydesdale Bank) is to be used\n"
        "**WHEN** the customer inserts the Scottish banknote\n"
        "**THEN** the note is accepted\n"
        "**AND** the amount paid increases by the note's value"
    ),
    "The Scottish banknote is accepted as valid sterling.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
))
cash_cases.append(case(
    None,
    "Banknotes — a non-sterling banknote is rejected",
    ["REQ-0339.0", "REQ-1491.0 (TFTS Requirements Matrix, Signed-Off; Q34 resolved, Q15 already fixed expected outcome)"],
    "This test is to confirm the TVM rejects a non-sterling (e.g. Euro) banknote, in contrast to its acceptance of a Scottish-issued sterling note.",
    (
        "**GIVEN** a TVM is at the payment screen for a cash transaction\n"
        "**AND** a Euro banknote is to be used\n"
        "**WHEN** the customer inserts the Euro banknote\n"
        "**THEN** the note is rejected\n"
        "**AND** the note is returned to the customer"
    ),
    "A non-sterling banknote is rejected and returned, unlike a Scottish-issued sterling note (see the Scottish-banknote sibling case).\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
))

# C4104116 / C4104117: jam location (coin-during-payment / note-during-payment / coin-during-change) — 3-way each.
JAM_LOCATIONS = [
    ("coin jam during payment", "a coin becomes jammed while the customer is inserting coins for payment"),
    ("note jam during payment", "a note becomes jammed while the customer is inserting a note for payment"),
    ("coin jam during change", "a coin becomes jammed while the TVM is dispensing change"),
]
orig_4116 = "Cash — a coin or note jam is cleared successfully during payment or change"
for i, (label, action) in enumerate(JAM_LOCATIONS):
    cash_cases.append(case(
        orig_4116 if i == 0 else None,
        f"Cash — a coin or note jam is cleared successfully during payment or change ({label})",
        ["old-suite C1831511", "old-suite C1831513", "old-suite C1831515"],
        f"This test is to confirm the TVM successfully clears a {label} and the transaction continues.",
        (
            "**GIVEN** a customer has commenced inserting coins or notes, or is receiving change, for a product purchase\n"
            f"**WHEN** {action} and the TVM successfully clears the jam\n"
            "**THEN** the insertion slot reopens\n"
            "**AND** the transaction continues normally"
        ),
        f"A successfully-cleared {label} does not abort the transaction.\n\n[Automatable: Partial — Cross-check: CloudFare / MERIT]",
    ))

orig_4117 = "Cash — a coin or note jam that cannot be cleared fails the transaction cleanly"
for i, (label, action) in enumerate(JAM_LOCATIONS):
    cash_cases.append(case(
        orig_4117 if i == 0 else None,
        f"Cash — a coin or note jam that cannot be cleared fails the transaction cleanly ({label})",
        ["old-suite C1831512", "old-suite C1831514", "old-suite C1831516"],
        f"This test is to confirm the TVM fails a transaction cleanly (no ticket issued, no fare charged) when a {label} cannot be cleared.",
        (
            "**GIVEN** a customer has commenced inserting coins or notes, or is receiving change, for a product purchase\n"
            f"**WHEN** {action} and the TVM cannot clear the jam\n"
            "**THEN** the transaction fails without issuing a ticket\n"
            "**AND** any inserted tender is returned or accounted for per the current cash-handling config"
        ),
        f"An unrecoverable {label} fails the transaction cleanly, with no ticket issued.\n\n[Automatable: Partial — Cross-check: CloudFare / MERIT]",
    ))

# C4103650 (Astreo-only, section 887778) and C4104113 (Kiosk-only, section 887843): Cancel/Back
# dismiss path — 2-way each. These live in DIFFERENT sections, so handled as separate section blocks
# below rather than in the main Payments - Cash list.

astreo_cases = []
DISMISS = ["Cancel", "Back"]
orig_3650 = "BNR — a note left in the exit beak leaves the recycler non-functional"
for i, dismiss in enumerate(DISMISS):
    astreo_cases.append(case(
        orig_3650 if i == 0 else None,
        f"BNR — a note left in the exit beak leaves the recycler non-functional ({dismiss})",
        [],
        f"This test is to confirm the Astreo BNR is reported non-functional when a dispensed note is left in the exit beak after the customer selects {dismiss}.",
        (
            "**GIVEN** an Astreo TVM has a note presented at the BNR exit beak during a cash transaction\n"
            f"**WHEN** the customer selects {dismiss} and leaves the note in the exit beak\n"
            "**THEN** the BNR is reported as non-functional\n"
            "**AND** note payment becomes unavailable until the note is cleared"
        ),
        f"A note left in the exit beak after {dismiss} leaves the BNR non-functional and note payment unavailable.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
    ))

kiosk_cases = []
orig_4113 = "BNR — a note left in the exit beak remains functional on Kiosk"
for i, dismiss in enumerate(DISMISS):
    kiosk_cases.append(case(
        orig_4113 if i == 0 else None,
        f"BNR — a note left in the exit beak remains functional on Kiosk ({dismiss})",
        ["old-suite C1831504"],
        f"This test is to confirm the Kiosk BNR remains functional when a dispensed note is left in the exit beak after the customer selects {dismiss}, unlike the Astreo BNR which is reported non-functional in the same scenario (see the Astreo-only sibling case).",
        (
            "**GIVEN** a Kiosk TVM has a note presented at the BNR exit beak during a cash transaction\n"
            f"**WHEN** the customer selects {dismiss} and leaves the note in the exit beak\n"
            "**THEN** the BNR remains functional\n"
            "**AND** note payment stays available"
        ),
        f"A note left in the exit beak after {dismiss} does not disable the Kiosk BNR.\n\n[Automatable: Partial — Cross-check: CloudFare / MERIT]",
    ))

write_family(
    "tvm-variant-expansion-2-cash",
    "# TVM variant expansion, follow-up batch 2026-07-24 — Payments - Cash (887777), incl.\n"
    "# Note Recycler & Change (Astreo only, 887778) and (Kiosk only, 887843) as separate section\n"
    "# blocks below. See tvm-variant-expansion-2.changelog.md for the full rationale.",
    ["Functional", "Payments - Cash"],
    cash_cases,
)

# Append the two sub-section blocks by hand-editing the produced YAML (separate section paths).
import yaml as _yaml
doc = _yaml.safe_load((HERE / "tvm-variant-expansion-2-cash.cases.yaml").read_text(encoding="utf-8").split("\n", 3)[-1])
doc["sections"].append({"path": ["Functional", "Payments - Cash", "Note Recycler & Change (Astreo only)"], "cases": astreo_cases})
doc["sections"].append({"path": ["Functional", "Payments - Cash", "Note Recycler & Change (Kiosk only)"], "cases": kiosk_cases})
header = (
    "# TVM variant expansion, follow-up batch 2026-07-24 — Payments - Cash (887777), incl.\n"
    "# Note Recycler & Change (Astreo only, 887778) and (Kiosk only, 887843) as separate section\n"
    "# blocks below. See tvm-variant-expansion-2.changelog.md for the full rationale.\n"
)
(HERE / "tvm-variant-expansion-2-cash.cases.yaml").write_text(
    header + _yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8"
)
print("cash total (all 3 sections):", len(cash_cases) + len(astreo_cases) + len(kiosk_cases))
