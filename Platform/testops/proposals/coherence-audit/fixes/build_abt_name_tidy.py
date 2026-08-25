"""One-off builder for the ABT name-tidy + stale-UNCONFIRMED-liveness rewrite files.

Reads the fresh suite dump (scratch_abt_suite.json, project root) and produces three
rewrite files:
  - abt-name-tidy-capping.rewrite.json      (34 cases, 4102757-4102790)
  - abt-name-tidy-journeyhistory.rewrite.json (22 cases, Journey History / Alighting-Stop
    Correction family)
  - abt-name-tidy-correctionlimits.rewrite.json (5 cases, 4103480-4103484)

Not meant to be re-run generically — case ids and substitution rules are hard-coded for
this specific pass (2026-07-23 ABT name-tidy task). Safe to delete after the pass lands.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
cases = json.loads((ROOT / "scratch_abt_suite.json").read_text(encoding="utf-8"))
by_id = {c["id"]: c for c in cases}

GEORGE_LIVE_LINE = (
    "**AND** CR122 alighting-stop correction is confirmed live on the ABT Passenger "
    "Portal — the Operator Portal does NOT have this function (George, 2026-07-22, "
    "reversing the 2026-07-21 answer)"
)
TERSE_LIVE_LINE = (
    "**AND** CR122 alighting-stop correction is confirmed live on both the ABT Operator Portal "
    "and Passenger Portal"
)
IS_AVAILABLE_LINE = "**AND** CR122 alighting-stop correction is available"


def steps_out(c):
    return [
        {"content": s.get("content") or "", "expected": s.get("expected") or ""}
        for s in (c.get("custom_steps_seperated") or [])
    ]


# ---------------------------------------------------------------------------
# Batch 1: capping family, 4102757-4102790 (34 cases)
# ---------------------------------------------------------------------------
capping_ids = list(range(4102757, 4102791))
batch1 = []
for cid in capping_ids:
    c = by_id[cid]
    preconds = c["custom_preconds"]
    assert IS_AVAILABLE_LINE in preconds, cid
    assert GEORGE_LIVE_LINE in preconds, cid
    new_preconds = preconds.replace(
        IS_AVAILABLE_LINE + "\n" + GEORGE_LIVE_LINE, TERSE_LIVE_LINE
    )
    steps = steps_out(c)
    if cid == 4102766:
        old_line = (
            "**AND** the card has one Metro journey that was declined at the reader "
            "(e.g. the card in a deny-listed state, Declined Reason 2), shown in "
            "Journey History as declined"
        )
        new_line = (
            "**AND** the card has one Metro journey whose own tap triggered the decline "
            "(e.g. Declined Reason 2, the first tap that applies the deny-list), shown "
            "in Journey History as declined"
        )
        assert old_line in new_preconds, cid
        new_preconds = new_preconds.replace(old_line, new_line)
    assert new_preconds != preconds
    batch1.append({
        "id": cid,
        "preconds": new_preconds,
        "steps": steps,
    })

Path(ROOT / "proposals/coherence-audit/fixes/abt-name-tidy-capping.rewrite.json").write_text(
    json.dumps(batch1, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("batch1 (capping):", len(batch1))

# ---------------------------------------------------------------------------
# Batch 2: Journey History / Alighting-Stop Correction family (22 cases)
# ---------------------------------------------------------------------------
jh_ids = [
    4102825, 4102826, 4102827, 4102828, 4102831,
    4102833, 4102834, 4102835, 4102836, 4102837, 4102838,
    4102839, 4102840, 4102841, 4102842, 4102843, 4102844, 4102845,
    4102846, 4102847, 4102848, 4102849,
]

# extra content preserved from the stale precond line, per case (None = fully dropped)
EXTRA = {
    4102831: "; the cancel/refund mechanism for a settled journey remains unconfirmed (see C4102830)",
    4102842: "; the Operator Portal shows the recalculated fare before confirming, the Passenger Portal (used here) does not (FBD-100662 para 693)",
}

# regex: the stale precond UNCONFIRMED line immediately followed by the george confirmed-live line
STALE_PRECOND_RE = re.compile(
    r"\*\*AND\*\* \*\*UNCONFIRMED\*\* — [^\n]*\n" + re.escape(GEORGE_LIVE_LINE)
)

# explicit old->new preface sentences (the paren clause questioning CR122's existence removed;
# any genuine narrower open item folded into a short parenthetical, or dropped if none)
PREFACE_NEW = {
    4102825: "This test is to confirm the proposed alighting-stop correction leaves a cancelled tap visible and still cancelled.",
    4102826: "This test is to confirm the proposed alighting-stop correction that recalculates a cancelled tap to £0.00 does not hide or duplicate the row.",
    4102827: "This test is to confirm the proposed correction on a normal (non-cancelled) journey recalculates the fare and keeps it active.",
    4102828: "This test is to confirm that a proposed stop correction does not flip a cancelled journey back to active across settlements.",
    4102831: "This test is to confirm that a proposed correction on an already-refunded cancelled tap keeps a single record and raises no further refund.",
    4102833: "This test is to confirm that the proposed alighting-stop correction offers the onward stops for a settled Ulsterbus TOO journey.",
    4102834: "This test is to confirm the proposed alighting-stop correction offers onward stops for a settled TOO journey from a different boarding stage (the exact stop count and \"No options\" wording are unconfirmed).",
    4102835: "This test is to confirm the proposed correction offers onward stops for each of two settled ref.60 taps from the same boarding stage (the \"No options\" wording is unconfirmed).",
    4102836: "This test is to confirm the proposed correction offers onward stops on every open, not intermittently (reads as a defect-fix acceptance test, not a requirement).",
    4102837: "This test is to confirm the proposed correction offers no stops only when there are no onward stops after the boarding stop (\"No options\" wording is unconfirmed).",
    4102838: "This test is to confirm the proposed correction returns onward stops for the journey's correct operator (the operator-match rule is not in the specs).",
    4102839: "This test is to confirm the proposed correction offers only appropriate onward stops (the filter rules are not in the requirement specs).",
    4102840: "This test is to confirm the proposed correction excludes zero-fare transfer stops (the zero-fare exclusion rule is not in the specs).",
    4102841: "This test is to confirm the proposed correction offers valid onward stops (the fare-based framing is not in the specs).",
    4102842: "This test is to confirm the proposed correction updates the alighting stage and recalculates the fare (the recalculation itself is specified).",
    4102843: "This test is to confirm the proposed correction's fare filter (the fare>0 filter is not in the specs).",
    4102844: "This test is to confirm a journey charged £0.00 by the daily cap remains visible and correctable (the fare>0 filter is not in the specs).",
    4102845: "This test is to confirm a cancelled £0.00 journey remains visible and correctable (the fare>0 filter and the \"**\" cancelled-indicator are unconfirmed).",
    4102846: "This test is to confirm a transfer journey charged £0.00 remains displayed and correctable (the fare>0 filter and transfer icon are unconfirmed).",
    4102847: "This test is to confirm the proposed correction excludes negative-fare anomalies (the fare filter and the negative-fare data-anomaly scenario are not in the specs).",
    4102848: "This test is to confirm positive-fare transfer stops still appear (the fare filter is not in the specs).",
    4102849: "This test is to confirm TVM-only positive-fare stops still appear, their exclusion being a separate known limitation (the fare filter and the TVM-only limitation are not in the requirement specs).",
}

batch2 = []
for cid in jh_ids:
    c = by_id[cid]
    preface = c["custom_preface"]
    new_preface = PREFACE_NEW[cid]
    assert new_preface != preface, cid

    preconds = c["custom_preconds"]
    assert GEORGE_LIVE_LINE in preconds, cid
    m = STALE_PRECOND_RE.search(preconds)
    assert m, (cid, preconds[-400:])
    extra = EXTRA.get(cid, "")
    new_preconds = preconds[: m.start()] + TERSE_LIVE_LINE + extra + preconds[m.end():]
    assert new_preconds != preconds

    steps = steps_out(c)

    if cid == 4102825:
        steps[0]["expected"] = steps[0]["expected"].replace(
            "— **UNCONFIRMED** (CR122 proposal)", ""
        ).rstrip()
    elif cid == 4102826:
        steps[0]["expected"] = steps[0]["expected"].replace(
            "— **UNCONFIRMED** (CR122 proposal)", ""
        ).rstrip()
    elif cid == 4102827:
        steps[0]["expected"] = steps[0]["expected"].replace(
            "\n**AND** all of the above is **UNCONFIRMED** (CR122 proposal)", ""
        )
    elif cid == 4102828:
        steps[0]["expected"] = steps[0]["expected"].replace(
            ' "**" indicator / retention behaviour, and CR122 correction precondition (gap Q21)',
            ' "**" indicator / retention behaviour (gap Q21)',
        )
    elif cid == 4102831:
        pass  # step-level markers already genuine, unchanged
    elif cid == 4102833:
        steps[0]["expected"] = steps[0]["expected"].replace(
            "for selection — **UNCONFIRMED** (CR122 proposal)",
            "for selection",
        )
    elif cid == 4102834:
        steps[0]["expected"] = steps[0]["expected"].replace(
            "are offered — **UNCONFIRMED**\n",
            "are offered\n",
        )
    elif cid == 4102835:
        steps[0]["expected"] = steps[0]["expected"].replace(
            "the same route — **UNCONFIRMED**\n",
            "the same route\n",
        )
    elif cid == 4102836:
        steps[0]["expected"] = steps[0]["expected"].replace(
            "on every open — **UNCONFIRMED**\n",
            "on every open\n",
        )
    elif cid == 4102837:
        steps[0]["expected"] = steps[0]["expected"].replace(
            "on the route — **UNCONFIRMED**\n",
            "on the route\n",
        )
    elif cid == 4102838:
        steps[0]["expected"] = steps[0]["expected"].replace(
            "are offered — **UNCONFIRMED**",
            "are offered",
        )
    elif cid == 4102839:
        pass
    elif cid == 4102840:
        pass
    elif cid == 4102841:
        pass
    elif cid == 4102842:
        steps[0]["expected"] = steps[0]["expected"].replace(
            "\n**AND** all of the above is **UNCONFIRMED** (CR122 proposal; gap Q21)", ""
        )
    elif cid == 4102843:
        pass
    elif cid == 4102844:
        steps[0]["expected"] = steps[0]["expected"].replace(
            "**AND** it is correctable — **UNCONFIRMED** (CR122)\n",
            "**AND** it is correctable\n",
        )
    elif cid == 4102845:
        steps[0]["expected"] = steps[0]["expected"].replace(
            "**AND** it is correctable — **UNCONFIRMED** (CR122)\n",
            "**AND** it is correctable\n",
        )
    elif cid == 4102846:
        steps[0]["expected"] = steps[0]["expected"].replace(
            "**AND** it is correctable — **UNCONFIRMED** (CR122)\n",
            "**AND** it is correctable\n",
        )
    elif cid == 4102847:
        pass
    elif cid == 4102848:
        pass
    elif cid == 4102849:
        pass

    batch2.append({
        "id": cid,
        "preface": new_preface,
        "preconds": new_preconds,
        "steps": steps,
    })

Path(ROOT / "proposals/coherence-audit/fixes/abt-name-tidy-journeyhistory.rewrite.json").write_text(
    json.dumps(batch2, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("batch2 (journey history):", len(batch2))

# ---------------------------------------------------------------------------
# Batch 3: Correction Limits, 4103480-4103484 (5 cases)
# ---------------------------------------------------------------------------
cl_ids = [4103480, 4103481, 4103482, 4103483, 4103484]
batch3 = []
for cid in cl_ids:
    c = by_id[cid]
    preconds = c["custom_preconds"]
    new_preconds = preconds.replace(" (George, 2026-07-22)", "")
    assert new_preconds != preconds, cid
    assert "george" not in new_preconds.lower(), cid
    batch3.append({
        "id": cid,
        "preconds": new_preconds,
    })

Path(ROOT / "proposals/coherence-audit/fixes/abt-name-tidy-correctionlimits.rewrite.json").write_text(
    json.dumps(batch3, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("batch3 (correction limits):", len(batch3))
