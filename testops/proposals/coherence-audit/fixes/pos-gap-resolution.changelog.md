# POS gap-register resolution pass — suite 30253, 2026-07-22

George's directive: before escalating any open `**GAP**`/`**UNCONFIRMED**` question to him, exhaust
every other source first — the old suite (9317), Overflow/UX flow annotations
(`knowledge/flows/flow-annotations.md`), and a broader/deeper requirements-library re-search than the
first pass tried. Only genuinely unanswerable questions stay open.

## Scope

Swept the whole gap register for POS-tagged open questions (identified by case id, not by
session-scoped Q-number — see the file's own note on numbering). Found exactly **5 open POS
questions**, all under the single session header `## Session 2026-07-21/22 — POS deep-audit pass,
suite 30253` (Q25–Q29). No other POS-tagged question elsewhere in the file was open — Q12, Q13, Q18
(the only other POS-tagged entries, in older sessions) were already answered by George on 2026-07-21.

## Method

For each open question:
1. Pulled the full old suite 9317 (`TestRailClient.get_cases(42, 9317)`, 2,193 cases) and searched by
   keyword/title for a matching old case.
2. Checked `knowledge/flows/flow-annotations.md` (the POS Overflow flow transcription) for a matching
   screen/behaviour note.
3. Re-searched `REQS_DIR` more broadly via `tools/extract_req.py --find` — this pass's key discovery
   was searching for `"matrix"`/`"REQ"` rather than only `FBD-#####` filename patterns, which surfaced
   `TFTS Requirements Matrix.xlsx` (a full local REQ-id index that the original Q25 wrongly assumed
   didn't exist) and its linked design-query tracker log.

## Result: all 5 resolved from existing evidence — 0 escalated to George

| Case | Question | Resolved via | Outcome |
|---|---|---|---|
| C4099912, C4099913 | Q25 — no REQ-id index exists, can't re-verify REQ refs | Broader spec search: `TFTS Requirements Matrix.xlsx` **is** a REQ-id index; found and confirmed all 5 REQ ids | Case already correct, no edit. Tooling-limitation premise itself was wrong. |
| C4099946 | Q26 — Excess Ticket rail-only, only a TIBU pin, no FBD | Old suite: **C4078764** (TIBU-24804 regression case, populated) + C4069393/94/97 (`NIR Operator Menu` section) | Case already correct, no edit. TIBU-24804 is grounded in a real old-suite case, not a bare pin. |
| C4103581 | Q27 — Heartbeat/StaffList mechanism framed as a proposal, not confirmed live | FBD-100266 para 174-175 ("Method 2 ... now been agreed") + `TFTS Requirements Matrix.xlsx` REQ-0602.4 (status "Accepted by customer") + its design-query log ("the function has been designed, developed and delivered") | **UNCONFIRMED marker removed**; Refs tightened. Applied via rewrite. |
| C4100427 | Q28 — is "Half-Fare" really the umbrella name for the Funded sub-group (incl. DLA)? | Old suite: 5 cases titled "X Half Fare Smartcard" (NDL/Partially Sighted/LD/PIPS/DLA) | Preface tightened from equivocal to confirmed wording. Applied via rewrite. |
| C4100363 | Q29 — comms recovery reconnect+sync, uncited | Broader spec search: `TFTS Requirements Matrix.xlsx` **REQ-2589.0** (resume-sending-after-interruption requirement, applies to POS, signed off) | Refs added. Applied via rewrite. |

## Cases applied

`proposals/coherence-audit/fixes/pos-gap-resolution.rewrite.json` — 3 rows, `--commit`-ed to suite
30253:
1. **C4103581** — UNCONFIRMED marker removed from preconditions; Refs tightened to
   `FBD-100266 para 148, 165-168, 174-175; REQ-0602.4`.
2. **C4100427** — preface's last sentence tightened from "DLA is also an entitlement card" to
   "Half-Fare sub-types: Partially Sighted, Learning Disability, No Driving Licence, DLA." (confirmed
   umbrella, not hedged).
3. **C4100363** — Refs added: `REQ-2589.0` (was previously uncited).

C4099912/C4099913 and C4099946 needed **no case edit** — they were already correctly worded/cited;
the gap was in the audit's own confidence, not the case.

## Verification

- `python -m system_test_ops audit --suite 30253` after commit: **CLEAN of blocking findings** — 528
  cases audited, 0 blocking findings, 43 pre-existing advisory findings (6 title-no-emdash, 37
  title-too-long) unchanged from before this pass.

## Genuinely open POS questions remaining for George

**None.** All 5 open POS-tagged gap-register questions were resolved from existing evidence (old
suite, or a broader requirements-matrix search) without needing to ask George.

## Notable finding for future audits

The original Q25 claimed `tools/extract_req.py` has "no local REQ-id→document index" — this was
**wrong**. `REQS_DIR\1_Requirements\TFTS Project Delivery Matrices & VCRMs\TFTS Requirements
Matrix.xlsx` (and its sibling `EXCEL VERSION TFTS Project Delivery Matrix.xlsx`) is exactly that
index: a full REQ-id catalogue with description, device applicability, and delivery/acceptance status
per requirement, readable by the existing `extract_req.py` (it already supports `.xlsx` via
openpyxl). It also contains **design-query tracker logs** (dated update threads per requirement,
e.g. "R1.1 - Device Heartbeat Requirements") that record whether a feature was actually designed,
developed and delivered — a genuinely new evidence source beyond FBD documents, not used by any
earlier pass in this repo. Future REQ-#### grounding and "is this CR actually live" questions should
search this file first via `extract_req.py --entry "TFTS Requirements Matrix" --terms "<REQ-id or
keyword>"` before concluding no index/evidence exists.
