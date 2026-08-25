# ABT gap-register resolution pass — suite 30279, 2026-07-22/23

Follow-up to `abt-deep-audit.changelog.md`. Task: exhaust old suite (14441) + a broader spec re-search
+ Jira (Atlassian Rovo MCP) before escalating any open BOS/ABT gap-register question to George. Also
folded in three ad-hoc spot-checks raised mid-task: (1) capping-case tap-visibility-vs-charge-timing
wording, (2) a `TFTS Requirements Matrix.xlsx` liveness cross-check, (3) the Q1 CR122
Operator-Portal→Passenger-Portal reversal (a live, in-flight correction from George, prioritised over
the rest of this task per his instruction).

## Scope of questions tackled

- ABT deep-audit session (suite 30279): Q25, Q26, Q28 (batch), Q29 (batch), Q30, Q32, Q33, Q34, Q35,
  Q36, Q37 (batch).
- Older still-open ABT questions: Q1/Q2 (CR122 portal), Q21 part-b (Update Stop list UI specifics).
- Not in scope / left open: Q31 (CloudFare screens live-check batch) — not part of the brief's named
  priority list; not independently re-verified this pass.

## Resolved (from old suite 14441 / broader spec re-search / Jira, not escalated)

| Q | Case(s) | Resolution | Source |
|---|---|---|---|
| Q26 | C4102927/C4102928 | "journeys in previous 7 days" IS a real sign-on gate (not a conflation with the view-window limit) | Old suite C2665782/C2665784/C2665785, REQ-3561 |
| Q28 (batch) | ~18 of ~24 Merit report cases | Real, REQ-traceable, CloudFare-Deployed legacy-generation reports; ~6 remain genuinely unmatched | Old suite Merit sections (REQ-1212/1993/2012/... family); `TFTS Requirements Matrix.xlsx` (REQ-1212 "Deployed") |
| Q29 (batch) | 7 Smartrack report cases + Access/Card Data/Import cases | Confirmed real via old suite `Smartrack` section, REQ-2375/0535/3516/1895 | Old suite C2665878-2665902, C2724075-2724104 |
| Q30 | C4103099 | Rail/BRT mileage+journey allocation are real, distinct Route Revenue Editor sub-functions | Old suite C2665863/864, C2841019/020, REQ-2066/3285 |
| Q32 | C4102996 | Not a conflict — "Preset" and "reverse FLU" are the same product ("Preset Reverse Fares Lookup (Up) Product") | Old suite C2717262, REQ-0516/1592/1862 |
| Q33 | C4102987 | Case's "service code" wording confirmed correct/grounded, not a paraphrase drift | Old suite C2840946, REQ-3291 |
| Q34 | C4102882 | "Minimum fare" is real, distinct, signed-off (REQ-3192.1) — not a mislabel of "Minimum ePurse balance" | Old suite C2925128/C2925129, REQ-3192.1 (Signed-Off) |
| Q35 | C4102881 | "Online" debt recovery correctly distinguished from tap-initiated (REQ-3399 vs REQ-3400, Deployed) | Old suite C2665809/C2665810; `TFTS Requirements Matrix.xlsx` REQ-3399.0 Deployed |
| Q36 | C4102880 | "Maximum journey duration" real, distinct, signed-off (REQ-3414) — not the NIR MJT or a duplicate | Old suite C2665807/C2665808; `TFTS Requirements Matrix.xlsx` REQ-3414.0 |
| Q37 (batch) | 35 Operator Web Portal Reports cases | All 35 have a matching, historically-executed old-suite case — confirmed portal-native, not DWH-only | Old suite `ABT / Operator Web Portal / Reports Management` (35 matches) |
| Q21b (partial) | 22 Journey History / Alighting-Stop-Correction cases | "Update stop" dialog + dropdown + "No options" empty state confirmed real and live (fixed/tested ABT 1.2.228.4) | TODEV-23500 (full ticket, Rovo MCP) |
| Q25 (partial) | C4102766 | Strong analogous evidence (cancelled/annulled journeys explicitly lose the correction option) but not identical-state proof for *declined* journeys — stays `**UNCONFIRMED**` | TODEV-24096, TODEV-24061 (full tickets, Rovo MCP) |

## Genuinely unresolved — stays queued for George

- Q21b granular filter rules (fare>0 filter, zero/negative/transfer exclusion, operator-match rule,
  exact stop counts) — not in any spec, ticket, or old-suite case found.
- Q25 — whether a correction can be *attempted at all* on a declined (not cancelled) journey — the
  cancelled-journey analogy is strong but declined ≠ cancelled; no direct source found.
- Q28 residual — BRT, Glider, Concessionary Class Summary (non-ENTCS), Fare Foregone, Ticketing
  timebands, Route Distance Analysis: no old-suite or REQ match found for these specific report names.
- Q31 — not tackled this pass (out of the brief's named priority list).

## Ad-hoc spot-check 1 — capping-case tap-visibility vs. 04:00-settlement-charge timing

George confirmed: a tap becomes visible in Journey History (with running cap status) almost
immediately, but the actual **charge** is deferred to EndOfDay settlement (04:00). Swept the live
capping-correction and Duplicate Detection cases (C4102757-C4102822) for wording that conflates these
two moments.

**Found and fixed**: 7 cases in `ABT / Duplicate Detection` (C4102816-C4102822) asserted a tap was
"charged the full £2.30" (or the day total already reflected a charge) in a step that ran **before**
any EndOfDay settlement action — i.e. asserting the settlement-time charge as an immediate consequence
of tapping. Reworded so the pre-settlement step only asserts the tap "appears in Journey History", and
the charge assertion moves to the step that actually runs the settlement (C4102817/C4102818 already had
a settlement step nearby; the fix there just moved the settlement action earlier so the existing
charge assertion is no longer premature).
**Checked and found correct as-is**: all 34 capping-correction cases (C4102757-C4102790) and all
annulment/re-tap cases (C4102791-C4102815) — every charge/refund/cap assertion in these was already
correctly gated behind a "run the EndOfDay settlement" step; no fix needed.
Applied: `proposals/coherence-audit/fixes/abt-capping-charge-timing.rewrite.json` (7 cases, committed).
Refs on all 7 cases now cite `George-settlement-timing-2026-07-22` alongside the existing TODEV/FBD refs.

## Ad-hoc spot-check 2 — `TFTS Requirements Matrix.xlsx`

A sibling POS gap-resolution pass found this file (`REQS_DIR\1_Requirements\TFTS Project Delivery
Matrices & VCRMs\TFTS Requirements Matrix.xlsx`) — an `openpyxl`-readable REQ-id index with delivery
status. Cross-checked it against this session's REQ ids (REQ-3192.1, REQ-3399/3400, REQ-3414, REQ-3436,
REQ-1212 family, REQ-2375) — all confirmed Signed-Off, several explicitly "Deployed". Folded into the
Q34/Q35/Q36/Q28/Q37 resolutions above; no case was left resting on old-suite evidence alone where the
matrix could independently corroborate delivery status.

## Ad-hoc spot-check 3 (priority interrupt) — Q1 CR122 Operator→Passenger reversal

Full writeup in `gap-register.md`, session header "Session 2026-07-22/23 — ABT gap-resolution
follow-up (Q21b, and the Q1 CR122 Operator→Passenger reversal)". Summary: George's 2026-07-21 "yes,
Operator Portal has CR122" answer was itself wrong and is now reversed — the Operator Portal has NO
alighting/fare correction function; the Passenger Portal does. A full 496-case keyword sweep (not just
the known ~42-case list) found exactly 61 live cases assuming Operator-Portal correction (34
capping-correction + 22 Journey-History/Alighting-Stop-Correction + C4102766, already counted in the
34; the 5 Correction-Limits cases were already correctly Passenger-scoped) and 35 already-condemned
`ZZ_DELETE_REVIEW` duplicates (out of scope) — nothing outside the known correction family. All 61
reworded to the Passenger Portal, with C4102842's operator-only "fare shown before confirming" clause
corrected (not just relabelled) per FBD-100662 para 693. Section-placement checked: no case sits in a
portal-named section, so no wrong-section list to hand to George. The separate, already-applied
`proposals/spec-grounded/abt/correction.rewrite.json` (47 cases) was checked and found clean — it never
asserted Operator-Portal-live behaviour (everything was left `UNCONFIRMED` at that time), so no
retroactive contradiction exists there beyond the C4102842 fix already made.
Applied: `proposals/coherence-audit/fixes/abt-cr122-operator-to-passenger.rewrite.json` (61 cases,
committed).

## Files touched this pass

- `proposals/coherence-audit/fixes/abt-capping-charge-timing.rewrite.json` (7 cases, committed)
- `proposals/coherence-audit/fixes/abt-deep-audit-merit-smartrack-reports-resolved.rewrite.json` (60 cases, committed)
- `proposals/coherence-audit/fixes/abt-deep-audit-single-case-resolutions.rewrite.json` (8 cases, committed)
- `proposals/coherence-audit/fixes/abt-cr122-operator-to-passenger.rewrite.json` (61 cases, committed)
- `proposals/coherence-audit/gap-register.md` (Q25/Q26/Q28/Q29/Q30/Q32/Q33/Q34/Q35/Q36/Q37/Q21b/Q1/Q2 updated)
- `proposals/coherence-audit/fixes/abt-gap-resolution-2026-07-22.changelog.md` (this file)

All four rewrite files were dry-run verified (0 refused, 0 missing) before `--commit`; each commit's
`updated` count matched the dry-run exactly (7, 60, 8, 61 — 136 case-updates total, some cases touched
by more than one file, e.g. C4102766 by both the CR122 batch and its own Q25 note).

## Audit — before/after (this pass's changes specifically)

`python -m system_test_ops audit --suite 30279 --no-gate`:

| | Cases audited | Blocking | Advisory |
|---|---|---|---|
| Before (baseline, carried from the same-day `abt-deep-audit.changelog.md` pass) | 391 | **89** | 208 |
| After this pass (all 4 rewrite files committed) | 391 | **89** | 208 |

**Unchanged (89 → 89).** None of the case ids touched by any of the 4 rewrite files in this pass appear
in the audit report's blocking or advisory finding lists (verified by grep against
`reports/tfts-system-test/new-bos-abt-suite/2026-07-23/alignment-audit.md`). The 89 blocking findings
are the suite's pre-existing, unrelated backlog (`preface-bad-preamble` ×82, `then-compound-genuine` ×7)
— explicitly out of scope for this task, unchanged by this pass.
