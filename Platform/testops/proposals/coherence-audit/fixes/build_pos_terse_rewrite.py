"""One-shot generator for pos-terse-rewrite.rewrite.json.

Reads the raw case bodies for the 22 cases identified as needing citation
relocation / prose compression (2026-07-21 terse-not-bloated pass on suite
30253), applies the specific, hand-verified text transforms below, and
writes proposals/coherence-audit/fixes/pos-terse-rewrite.rewrite.json in the
{id,title,preface,preconds,steps,action,citations,change_note,refs} shape
used by tools/apply_rewrite.py.

This is NOT a generic bloat-remover — every substitution here was checked
by hand against the actual case text (see the citation-review*.txt files in
reports/tfts-system-test/new-pos-acceptance-suite/2026-07-21/). No fact is
re-derived; only inline citation/provenance text is relocated to `refs` and
verbose citation clauses are shortened to a terse parenthetical.
"""
import json
import re
from pathlib import Path

RAW = Path(r"C:\Users\GeorgeOliver\Documents\GitHub\system-test-ops\reports\tfts-system-test\new-pos-acceptance-suite\2026-07-21\case-bodies-raw.json")
OUT = Path(r"C:\Users\GeorgeOliver\Documents\GitHub\system-test-ops\proposals\coherence-audit\fixes\pos-terse-rewrite.rewrite.json")

cases = json.loads(RAW.read_text(encoding="utf-8"))
byid = {c["id"]: c for c in cases}


def merge_refs(existing, add):
    cur = [r.strip() for r in (existing or "").split(",") if r.strip()]
    for a in add:
        if a not in cur:
            cur.append(a)
    return ",".join(cur)


rows = []

# ---- Rail FLU / cross-border family: "... confirm against the NIR fares
# reference table, FBD-100450)" -> "... confirm against NIR fares reference
# table)" + FBD-100450 relocated to refs. One shared substitution across a
# family of near-identical precond clauses; hand-checked each source string
# above (citation-review-2.txt) before writing the regex.
RAIL_PAT = re.compile(
    r"\(([^()]*?)confirm(?:ed)? against the NIR fares reference table,\s*FBD-100450\)"
)


def rail_sub(text):
    def repl(m):
        prefix = m.group(1).strip()
        prefix = (prefix + " ") if prefix else ""
        return f"({prefix}confirm against NIR fares reference table)"
    return RAIL_PAT.sub(repl, text)


RAIL_IDS = [4099970, 4099971, 4099972, 4099976, 4100429, 4100501, 4100502,
            4099977, 4099978, 4099979, 4099980]

for cid in RAIL_IDS:
    c = byid[cid]
    preconds = c["custom_preconds"]
    new_preconds = rail_sub(preconds)
    assert new_preconds != preconds, f"no substitution matched for {cid}"
    assert "FBD-100450" not in new_preconds
    rows.append({
        "id": cid,
        "title": c["title"],
        "preconds": new_preconds,
        "action": "reword",
        "change_note": "Relocated inline 'FBD-100450' citation out of the worked-example precondition into Refs; shortened the surrounding clause to a terse parenthetical ('confirm against NIR fares reference table').",
        "refs": merge_refs(c.get("refs"), ["FBD-100450"]),
    })

# ---- 4100374 Bus FLU — sell a ticket: "(fares confirm against the fares
# export; Fare Stage names per FBD-100207)" -> "(confirm against fares
# export; Fare Stage names per current config)" + FBD-100207 to refs.
c = byid[4100374]
old = c["custom_preconds"]
new = old.replace(
    "(fares confirm against the fares export; Fare Stage names per FBD-100207)",
    "(confirm against fares export; Fare Stage names per current config)",
)
assert new != old and "FBD-100207" not in new
rows.append({
    "id": 4100374,
    "title": c["title"],
    "preconds": new,
    "action": "reword",
    "change_note": "Relocated inline 'FBD-100207' citation into Refs; shortened the clause.",
    "refs": merge_refs(c.get("refs"), ["FBD-100207"]),
})

# ---- Top Up / Smartcard family: bare or light "(... — FBD-#####)" clauses.
SIMPLE = [
    (4100007,
     "example: an Adult iLink Zone 4 travelcard, top up 1 Week, paid by cash (top-up amount labels per FBD-100260; Metro is cash-only, bank card / warrant available on NIR + Ulsterbus)",
     "example: an Adult iLink Zone 4 travelcard, top up 1 Week, paid by cash (Metro is cash-only, bank card / warrant available on NIR + Ulsterbus)",
     ["FBD-100260"]),
    (4100009,
     "example: an Adult Metro Multi-Journey (City zone) card, topping up 10 journeys (FBD-100261)",
     "example: an Adult Metro Multi-Journey (City zone) card, topping up 10 journeys",
     ["FBD-100261"]),
    (4102560,
     "a smartcard has just been validated on the POS (passback always applies and takes priority over transfer — FBD-100271)",
     "a smartcard has just been validated on the POS (passback always applies and takes priority over transfer)",
     ["FBD-100271"]),
    (4102564,
     "a faulty concessionary Smartpass is presented — example: a Senior SmartPass (Fare Foregone — FBD-100250)",
     "a faulty concessionary Smartpass is presented — example: a Senior SmartPass (Fare Foregone)",
     ["FBD-100250"]),
    (4102565,
     "a faulty Dependants Pass is presented (a Corporate card — FBD-100250)",
     "a faulty Dependants Pass is presented (a Corporate card)",
     ["FBD-100250"]),
    (4100415,
     "a yLink entitlement smartcard is available (a personalised Funded card — FBD-100250)",
     "a yLink entitlement smartcard is available (a personalised Funded card)",
     ["FBD-100250"]),
    (4100416,
     "a 24+ entitlement smartcard is available (a personalised Funded card — FBD-100250)",
     "a 24+ entitlement smartcard is available (a personalised Funded card)",
     ["FBD-100250"]),
    (4100418,
     "a Dependents Pass entitlement smartcard is available (a Corporate card — FBD-100250)",
     "a Dependents Pass entitlement smartcard is available (a Corporate card)",
     ["FBD-100250"]),
]

for cid, old_frag, new_frag, cites in SIMPLE:
    c = byid[cid]
    old = c["custom_preconds"]
    assert old_frag in old, f"fragment not found in {cid}"
    new = old.replace(old_frag, new_frag)
    rows.append({
        "id": cid,
        "title": c["title"],
        "preconds": new,
        "action": "reword",
        "change_note": f"Relocated inline citation ({', '.join(cites)}) out of the precondition text into Refs; kept the operational detail, dropped the bare spec reference.",
        "refs": merge_refs(c.get("refs"), cites),
    })

# ---- 4100360 / 4100436: heavy provenance paragraph baked into the preface
# ("**CONFIRMED (George, live-system confirmation, 2026-07-21)**  ...  Closes
# gap-register.md Q18 ... conflict with C#### (audit 2026-07-17) ..."). This
# is the exact failure mode called out in the mandate. Behaviour itself is
# untouched (steps/preconds already state the corrected behaviour); only the
# confirmation/date/audit-history prose moves out of the preface into Refs,
# and — because 4100436's EXPECTED summary was left stale after the earlier
# half-applied correction (contradicts its own steps: "FLU inactivity →
# Idle (no waybill, no break)" vs the steps' "goes to the Operator Break
# screen") — the summary is re-aligned to the steps it already has. No new
# fact invented; this only removes a summary/steps contradiction that was a
# residual of the prior fix.
c = byid[4100360]
rows.append({
    "id": 4100360,
    "title": c["title"],
    "preface": "This test is to confirm the POS resumes to the correct state after a power interruption, depending on how long power was lost relative to the Auto Sign Off time — for an interruption shorter than the Auto Sign Off time, the POS resumes via the Operator Break screen (break mode used, not skipped).",
    "action": "reword",
    "change_note": "Relocated the 'CONFIRMED (George, live-system confirmation, 2026-07-21)' attribution, the gap-register Q18 reference, and the audit/conflict history with C4100436 out of the preface into Refs. Preface now states the behaviour only.",
    "refs": merge_refs(c.get("refs"), [
        "George live-system confirmation 2026-07-21 (resolves gap-register Q18)",
        "supersedes conflict with C4100436, audit 2026-07-17",
    ]),
})

c = byid[4100436]
rows.append({
    "id": 4100436,
    "title": c["title"],
    "preface": "This test is to confirm the configurable inactivity behaviour: FLU timeout signs off via Operator Break; Idle timeout (or continued inactivity on the Operator Break screen) suspends; suspend duration auto-reboots.",
    "expected": "Resume state depends on the configured timers: FLU inactivity for the Auto Sign Off period → Operator Break screen (no waybill); continued inactivity on Operator Break for the Auto Suspend period → suspend; Suspend Duration elapsed or a keypress → reboot to Idle. All periods configurable.",
    "action": "reword",
    "change_note": "Relocated the 'CONFIRMED (George, live-system confirmation, 2026-07-21)' attribution, the gap-register Q18 reference, and the audit/conflict history with C4100360 out of the preface into Refs. Also re-aligned the EXPECTED summary, which had been left stale from the earlier half-applied correction (it still said 'FLU inactivity -> Idle, no break', contradicting this case's own steps which already route through the Operator Break screen) -- summary now matches the steps, no new fact introduced.",
    "refs": merge_refs(c.get("refs"), [
        "George live-system confirmation 2026-07-21 (resolves gap-register Q18)",
        "supersedes conflict with C4100360, audit 2026-07-17",
    ]),
})

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote {len(rows)} rows -> {OUT}")
