"""Build the Operator/Passenger portal-split duplication for the ABT alighting-stop-correction
family (suite 30279), per George's 2026-07-23 directive: don't merge as "portal-agnostic" — every
case in the capping/settlement + Journey-History/Update-Stop-List family gets an Operator Portal
version AND a Passenger Portal version, each filed in its own folder, grounded on that portal's own
real mechanics (fare-preview-before-confirm is Operator-only per FBD-100662 para 693; no preview +
the 1/month.3/year limit is Passenger-only per para 692/693). Correction Limits (C4103480-4103484)
stay Passenger-only — the limit is a passenger-abuse-mitigation mechanism with no Operator equivalent.

Reads a fresh pull of the 56 source cases (the ones carrying the "confirmed live on both...portals"
precondition line) directly from TestRail, generates two variants of each (Operator / Passenger),
and writes:
  - abt-portal-split.new-cases.json   (112 new-case rows, for direct writer.add_case use)
  - abt-portal-split.retire.rewrite.json (56 ids -> ZZ_DELETE_REVIEW, for apply_rewrite.py)

Run this to (re)generate the JSON; a separate push script actually writes to TestRail.
"""
from __future__ import annotations
import json, re
from pathlib import Path
import os

from system_test_ops.testrail.client import TestRailClient

OUT_DIR = Path(__file__).parent

SECTION_MAP = {
    887576: "Metro Daily Cap",
    887577: "Zonal Cap",
    887578: "Reference Fare Cap",
    887579: "Uncapped & Single Taps",
    887580: "Town Service Cap",
    887583: "Journey History",
    887584: "Update Stop List",
}

TARGET_IDS = {
    4102757, 4102758, 4102759, 4102760, 4102761, 4102762, 4102763, 4102764, 4102765, 4102766,
    4102767, 4102768, 4102769, 4102770, 4102771, 4102772, 4102773, 4102774, 4102775, 4102776,
    4102777, 4102778, 4102779, 4102780, 4102781, 4102782, 4102783, 4102784, 4102785, 4102786,
    4102787, 4102788, 4102789, 4102790,
    4102825, 4102826, 4102827, 4102828, 4102831,
    4102833, 4102834, 4102835, 4102836, 4102837, 4102838,
    4102839, 4102840, 4102841, 4102842, 4102843, 4102844, 4102845, 4102846, 4102847, 4102848, 4102849,
}

BOTH_LINE = "**AND** CR122 alighting-stop correction is confirmed live on both the ABT Operator Portal and Passenger Portal"
BOTH_LINE_FAREPREVIEW = (
    "**AND** CR122 alighting-stop correction is confirmed live on both the ABT Operator Portal and "
    "Passenger Portal; the Operator Portal shows the recalculated fare before confirming, the "
    "Passenger Portal (used here) does not (FBD-100662 para 693)"
)
BOTH_LINE_REFUND_UNCONF = (
    "**AND** CR122 alighting-stop correction is confirmed live on both the ABT Operator Portal and "
    "Passenger Portal; the cancel/refund mechanism for a settled journey remains unconfirmed (see C4102830)"
)

SIGNIN_A = "**AND** you are signed in to the ABT Passenger Portal to view Journey History"
SIGNIN_B = "**AND** you are signed into the ABT Passenger Web Portal (env5) on that card's account"


def portal_line(portal: str) -> str:
    if portal == "Operator":
        return (f"**AND** CR122 alighting-stop correction is confirmed live on the ABT Operator "
                f"Portal; the Operator Portal shows the recalculated fare before confirming "
                f"(FBD-100662 para 693)")
    return (f"**AND** CR122 alighting-stop correction is confirmed live on the ABT Passenger "
            f"Portal; no fare preview is shown before confirm (FBD-100662 para 693)")


def transform_preconds(text: str, portal: str, case_id: int) -> str:
    lines = text.split("\n")
    out = []
    for ln in lines:
        s = ln.strip()
        if s == BOTH_LINE:
            out.append(portal_line(portal))
        elif s == BOTH_LINE_FAREPREVIEW:
            # C4102842 handled bespoke elsewhere; shouldn't reach here, but be safe
            out.append(portal_line(portal))
        elif s == BOTH_LINE_REFUND_UNCONF:
            out.append(portal_line(portal) + " The cancel/refund mechanism for a settled journey "
                       "remains unconfirmed (see C4102830).")
        elif s == SIGNIN_A:
            out.append(f"**AND** you are signed in to the ABT {portal} Portal to view Journey History")
        elif s == SIGNIN_B:
            out.append(f"**AND** you are signed into the ABT {portal} Web Portal (env5) on that card's account")
        else:
            out.append(ln)
    return "\n".join(out)


def transform_steps(steps: list[dict], portal: str) -> list[dict]:
    out = []
    for s in steps:
        content = (s.get("content") or "").replace("in the Passenger Portal you correct",
                                                     f"in the {portal} Portal you correct")
        expected = s.get("expected") or ""
        out.append({"content": content, "expected": expected})
    return out


def transform_refs(refs: str, portal: str) -> str:
    parts = [p.strip() for p in (refs or "").split(",") if p.strip()]
    parts = [p for p in parts if not p.startswith("George-2026-07-2")]
    parts.append(f"George-2026-07-23-CR122-{portal.lower()}-portal-split")
    return ",".join(parts)


def portal_title(title: str, portal: str) -> str:
    if title.rstrip().endswith("(CR122)"):
        return title.rstrip()[: -len("(CR122)")].rstrip() + f" (CR122, {portal} Portal)"
    return title + f" ({portal} Portal)"


def build_variant(case: dict, portal: str) -> dict:
    cid = case["id"]
    preconds = transform_preconds(case.get("custom_preconds") or "", portal, cid)
    steps = transform_steps(case.get("custom_steps_seperated") or [], portal)
    refs = transform_refs(case.get("refs") or "", portal)
    title = portal_title(case["title"], portal)
    section_name = SECTION_MAP[case["section_id"]]
    return {
        "source_id": cid,
        "portal": portal,
        "section_path": ["ABT", f"{portal} Web Portal", "Tap Correction", section_name],
        "title": title,
        "refs": refs,
        "preface": case.get("custom_preface") or "",
        "preconds": preconds,
        "steps": steps,
        "expected": case.get("custom_expected") or "",
        "priority_id": case.get("priority_id", 1),
        "custom_devtypes": case.get("custom_devtypes") or [200],
    }


def build_c4102842_variant(case: dict, portal: str) -> dict:
    """Bespoke, not a find/replace — the fare-preview mechanic genuinely differs by portal."""
    cid = case["id"]
    section_name = SECTION_MAP[case["section_id"]]
    if portal == "Operator":
        title = "Alighting-Stop Correction — Operator Portal previews the recalculated fare before confirming (CR122, Operator Portal)"
        preface = ("This test is to confirm the Operator Portal shows the recalculated fare before "
                    "confirming an alighting-stop correction, then updates the alighting stage (CR122).")
        preconds = ("**GIVEN** the seeded ABT test cEMV card and its account exist in CloudFare env5\n"
                    "**AND** you are signed into the ABT Operator Web Portal (env5) on that card's account\n"
                    "**AND** a TOO journey exists on route 273 with a settled alighting stage to be corrected\n"
                    "**AND** CR122 alighting-stop correction is confirmed live on the ABT Operator Portal; "
                    "the Operator Portal shows the recalculated fare before confirming (FBD-100662 para 693)")
        steps = [{
            "content": ("**WHEN** you select an onward stop after the boarding stop on the same route\n"
                        "**AND** the Operator Portal displays the recalculated fare for the selected stop "
                        "before you confirm"),
            "expected": ("**THEN** the previewed fare matches the selected stop's fare\n"
                         "**AND** confirming updates the journey's alighting stage to the selected stop\n"
                         "**AND** the fare is recalculated and any affected caps updated"),
        }]
        expected = ("The Operator Portal previews the recalculated fare before confirm; confirming "
                     "updates the alighting stage and recalculates the fare.")
    else:
        title = "Alighting-Stop Correction — Passenger Portal updates the alighting stage without a fare preview (CR122, Passenger Portal)"
        preface = ("This test is to confirm the Passenger Portal updates the alighting stage and "
                    "recalculates the fare with no fare preview shown before confirm (CR122).")
        preconds = ("**GIVEN** the seeded ABT test cEMV card and its account exist in CloudFare env5\n"
                    "**AND** you are signed into the ABT Passenger Web Portal (env5) on that card's account\n"
                    "**AND** a TOO journey exists on route 273 with a settled alighting stage to be corrected\n"
                    "**AND** CR122 alighting-stop correction is confirmed live on the ABT Passenger Portal; "
                    "no fare preview is shown before confirm (FBD-100662 para 693)")
        steps = [{
            "content": ("**WHEN** you select an onward stop after the boarding stop on the same route\n"
                        "**AND** you confirm the change (no fare preview is shown beforehand)"),
            "expected": ("**THEN** the journey's alighting stage is updated to the selected stop\n"
                         "**AND** the fare is recalculated and any affected caps updated"),
        }]
        expected = ("The Passenger Portal updates the alighting stage and recalculates the fare with "
                     "no fare preview shown before confirm.")
    refs = transform_refs(case.get("refs") or "", portal)
    return {
        "source_id": cid,
        "portal": portal,
        "section_path": ["ABT", f"{portal} Web Portal", "Tap Correction", section_name],
        "title": title,
        "refs": refs,
        "preface": preface,
        "preconds": preconds,
        "steps": steps,
        "expected": expected,
        "priority_id": case.get("priority_id", 1),
        "custom_devtypes": case.get("custom_devtypes") or [200],
    }


def main():
    client = TestRailClient()
    cases = client.get_cases(42, 30279)
    by_id = {c["id"]: c for c in cases}
    missing = TARGET_IDS - set(by_id)
    if missing:
        print("MISSING:", missing)

    new_cases = []
    for cid in sorted(TARGET_IDS):
        case = by_id.get(cid)
        if not case:
            continue
        if cid == 4102842:
            new_cases.append(build_c4102842_variant(case, "Operator"))
            new_cases.append(build_c4102842_variant(case, "Passenger"))
        else:
            new_cases.append(build_variant(case, "Operator"))
            new_cases.append(build_variant(case, "Passenger"))

    (OUT_DIR / "abt-portal-split.new-cases.json").write_text(
        json.dumps(new_cases, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    retire = [{"id": cid, "action": "remove"} for cid in sorted(TARGET_IDS)]
    (OUT_DIR / "abt-portal-split.retire.rewrite.json").write_text(
        json.dumps(retire, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"Built {len(new_cases)} new-case rows (from {len(TARGET_IDS)} sources x2) "
          f"+ {len(retire)} retirements.")


if __name__ == "__main__":
    main()
