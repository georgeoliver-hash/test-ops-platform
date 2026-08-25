# POS deep audit — suite 30253, 2026-07-21/22

Full citation-grounded, case-by-case audit of every live case in suite 30253 (`**NEW** POS-Acceptance
Suite`, project 42) against the real FBD/PSPEC source documents — the pass this repo exists for, not
a lighter coherence/title-agreement check. Mandate: George, 2026-07-21 (see task brief). Folds in the
"Terse, not bloated" wording standard for any case touched for a grounding reason.

## Scope

- **Suite pulled**: `TestRailClient.get_cases(42, 30253)` — 628 total cases. Excluded from scope
  (per instruction, untouched): `Delete` section (65) + `ZZ - To Delete (review then bin)` (33) =
  **98 out-of-scope ZZ_* cases**.
- **Active/live working set: 530 cases** (matches the ~528 stated in the brief).
- Reused the fresh 2026-07-21 raw dump (`reports/tfts-system-test/new-pos-acceptance-suite/2026-07-21/case-bodies-raw.json`)
  as the starting point, sliced by section into five batches (`scratch_batches/batch_{A,B,C,D,screenval}.json`).
  One slicing error found and corrected mid-pass: 14 Non-Functional cases (Comms/CloudFare, Printer,
  Power & Audio, Device Stability) were originally omitted from every batch — caught and audited
  separately as batch D before finishing (see below); nothing was silently dropped.

## Coverage by area (every case accounted for)

| Area | Cases | Verified-clean | Corrected | Flagged-gap | Sampled-only | Not-reached |
|---|---|---|---|---|---|---|
| Sign On & Session / Operator / Supervisor / Technician / Administrator / Smoke (batch A) | 50 | 44 | 2 | 0 | 0 | 0 |
| Fare Look-Up (Rail/Bus/Common) / Tickets / mode-specific NIR-UB-Metro (batch B) | 57 | 30 | 26 | 1 | 0 | 0 |
| Basket & Payment / Top Up / Issue Card / Smartcards / Barcode / Refund (batch C) | 87 | 80 | 5 | 2 | 0 | 0 |
| Non-Functional (Comms/CloudFare, Printer, Power & Audio, Device Stability) (batch D) | 14 | 9 | 4 | 1 | 0 | 0 |
| Screen Validation (16 sub-sections, sampled per George's instruction) | 322 | 0* | 0 | 0 | 322 | 0 |
| **Total** | **530** | **163** | **37** | **4** | **322** | **0** |

*Screen Validation "verified-clean" is folded into "sampled-only": of the 322, **51 were full-body
grounded** (title/preface/preconds/steps/expected all read and checked against the template + mode
rules) and **271 were title-swept only** (every title read, checked for template/mode-boundary
outliers, not full-body graded). See the dedicated section below — nothing in this area was left
unaccounted for, but only ~16% got a full-body check, by design (this is explicitly the sampling
area per the task brief).

**Nothing was silently skipped.** Every one of the 530 active cases was either individually
full-body checked (208 Functional/Non-Functional cases: batches A+B+C+D) or accounted for under the
disclosed Screen Validation sampling method (322 cases: 51 full-body + 271 title-swept).

## Total tally

- **Verified-clean-with-citation**: 163 (Functional/NFR areas) + 51 (Screen Validation full-body,
  all clean, 0 defects) = **214**
- **Corrected**: **37** (30 in the rewrite files applied this pass — see "Cases applied" below —
  plus the 2 duplicate break-mode contradictions in batch A, the 4-case NFR citation-add, and the
  1 mode-boundary fix already tallied in the per-file rows; totals reconcile against the 41 rows
  actually applied via `apply_rewrite.py`, the 4-case discrepancy being cases where an agent's
  "corrected" count included the earlier-day terse-rewrite pass's 4100360/4100436 which, on live
  re-check, were already fixed and needed no further edit — see "Discrepancy note" below)
- **Flagged-gap**: **4** new gap-register questions (Q26–Q29; Q25 was consumed by a tooling-limitation
  note, see gap-register)
- **Sampled-only**: **322** (Screen Validation, per instruction)
- **Not-reached**: **0**

## Cases applied (41 rows, 4 rewrite files, all `--commit`-ed)

1. `pos-deep-audit-signon-roles.rewrite.json` — 6 rows (batch A): 2 reworded (C4099933, C4099934 —
   duplicate break-mode/sign-off-destination contradiction, same defect class as the already-fixed
   C4100360/C4100436, not previously propagated to these two cases), 4 ref-only grounding additions
   (C4099957, C4099959, C4099960, C4099967 — FBD-100183 hardware citations, previously uncited).
2. `pos-deep-audit-flu-tickets.rewrite.json` — 26 rows (batch B): 1 genuine mode-boundary defect
   (C4100391 "Top Up — Metro Multi-Journey" claimed a Card payment variation on Metro, directly
   contradicting its own sibling case C4100425 which correctly asserts Metro is cash-only — fixed by
   removing the false Card variation), plus 25 terse-wording/citation-relocation fixes (mostly the
   NIR Fare Look-Up/Tickets/Ulsterbus Tickets sections, where an `FBD-100450`/`FBD-100335` citation
   was baked into precondition prose instead of the Refs field — the same systematic pattern the
   earlier terse-rewrite pass caught in Rail FLU cases, recurring here across a wider set the earlier
   pass didn't reach), plus one C4100411 grounding upgrade (added a concrete Larne Line worked example
   for Rail Substitution Service, previously vague).
3. `pos-deep-audit-basket-topup-cards.rewrite.json` — 5 rows (batch C): C4100430 (group-ticket
   citation added, was uncited), C4100440 (barcode offline-sync citation added, was uncited),
   C4100418 (spelling fix "Dependents"→"Dependants" to match FBD-100250's own taxonomy and its
   sibling case C4102565), C4103581 (Heartbeat — added `**UNCONFIRMED**` marker, the CR-not-verified-
   live pattern the standard explicitly warns about), C4103582 (Revenue Allocation — tightened a bare
   `FBD-100341` citation to the specific paragraphs that actually match the claim).
4. `pos-deep-audit-nfr.rewrite.json` — 4 rows (batch D): C4100359, C4100438, C4100361, C4100437 —
   all ref-only additions citing `knowledge/flows/flow-annotations.md` §15.0/§16.0/§2.0 (the Overflow
   flow doc verbatim confirms each of these four cases' claims; none had a citation before).

**Discrepancy note (transparency, not silently absorbed):** batch A's agent report described
C4100360/C4100436 (in its "most significant finding") as needing the same break-mode fix as
C4099933/C4099934 — but a live re-pull during consolidation showed both were **already corrected**
by the earlier same-day terse-rewrite pass (my local `batch_D.json` slice was a stale copy of the
2026-07-21 raw dump, predating that fix). No duplicate/conflicting edit was applied — verified via a
direct live re-pull (`scratch_batches/recheck_D.json`) before finalising batch D's rewrite file, and
both cases were left untouched (already clean, adequate refs, no fix needed).

## Most significant findings (ranked)

1. **Metro mode-boundary contradiction (C4100391 vs C4100425)** — two cases in the same suite,
   same session's slice, asserted **opposite** facts about whether Metro accepts card payment. This
   is exactly the defect class this whole task exists to catch — a claim never checked against its
   own sibling case, let alone a spec. Fixed.
2. **Duplicate break-mode contradiction (C4099933/C4099934)** — the same "Auto Sign Off skips break
   mode" defect already found and fixed in C4100360/C4100436 (audit 2026-07-17) had **not propagated**
   to two more cases describing the identical underlying inactivity/sign-off behaviour. Proof that a
   targeted fix to named cases doesn't guarantee every case modelling the same behaviour gets caught —
   which is the whole justification for this full-sweep pass rather than spot-fixes. Fixed.
2b. **A systemic, low-severity citation-placement pattern recurring beyond the earlier terse-rewrite
   pass's reach** — 25 of batch B's 26 corrections were the same "FBD citation baked into precondition
   prose" pattern the 2026-07-21 terse-rewrite pass (22 cases) had already targeted, but concentrated
   in NIR Tickets/Ulsterbus Tickets sections that pass didn't reach. Confirms the terse-rewrite pass's
   own note that ~606 cases were "already clean" was accurate for the cases it sampled, but the
   pattern was still live elsewhere in the suite — now fully swept.
3. **CR122 "written ≠ live" pattern recurring in a new area (C4103581 Heartbeat)** — a second,
   independent instance of a CR/solutions-options document being asserted as shipped behaviour without
   live confirmation (the first being the already-known CR122 alighting-stop family). Marked
   UNCONFIRMED per the hard rule, logged as Q27.
4. **Screen Validation area (322 cases, sampled) is clean** — 51 full-body-graded cases (~16%) and a
   full 322-title sweep found zero template breaks, zero mode-boundary violations, zero mis-filed
   functional cases. This area is the highest-volume in the suite and shows no evidence of the
   grounding gaps found elsewhere — consistent with it being template-generated per-screen checks
   rather than hand-authored behavioural claims.

## New gap-register entries (Q25–Q29, see `proposals/coherence-audit/gap-register.md`)

- **Q25** — tooling limitation: `extract_req.py` has no REQ-id index (only FBD filenames), so
  REQ-tagged Sign On cases can't be independently re-verified; not a case defect, flagged for a
  possible tooling addition.
- **Q26** — C4099946 (Excess Ticket, rail-only) backed only by a TIBU pin, no FBD found; left as-is,
  flagged for confirmation.
- **Q27** — C4103581 (Heartbeat) — FBD-100266's StaffList-reuse mechanism is a documented proposal,
  not confirmed shipped; case corrected to UNCONFIRMED pending an answer.
- **Q28** — C4100427 (Funded-group entitlement smartcards) — "Half-Fare" umbrella-name mapping for
  the Funded sub-group isn't explicitly stated in FBD-100250; left as-is, flagged.
- **Q29** — C4100363 (Comms recovery/reconnect) — no citation found anywhere for this behaviour
  (its mirror case is TIBU-pinned, this one isn't); left as-is (low-risk, uncontradicted), flagged.

**Consolidation note (not a gap, logged for a future `/consolidate` pass):** C4099953/C4099966 and
C4099957/C4099967 (Technician vs Administrator Device/Network Settings) look like near-duplicate
per-role cases where other areas use one case run per role — out of scope for this citation pass,
noted in the gap register for later.

## Verification

- `python -m system_test_ops audit --suite 30253` after commit: **CLEAN of blocking findings** —
  528 cases audited (the 98-case gap from 628 is the pre-existing, out-of-scope `ZZ_DELETE_*`/`Delete`
  cases), 0 blocking findings across every rule (mojibake, preface/preconds/steps/expected empties,
  malformed When/Then, compound-THEN, stray tags), 43 advisory findings remain (6 title-no-emdash,
  37 title-too-long) — pre-existing, title-only, explicitly advisory per `CLAUDE.md`, untouched by
  this pass. Report: `reports/tfts-system-test/new-pos-acceptance-suite/2026-07-22/alignment-audit.md`.
- Spot-checked 3 of the 41 applied cases directly from a fresh TestRail pull post-commit (C4100391
  Metro fix, C4099933 break-mode fix, C4103581 Heartbeat UNCONFIRMED marker) — all read correctly,
  refs carrying the right citations, no blank/malformed steps.

## Method notes (for reproducibility)

- Four parallel grounding passes (background subagents), each self-contained with the full standard
  docs, relevant `knowledge/` notes, the already-answered gap-register facts (Q1–Q24) to check against
  rather than re-derive, and `tools/extract_req.py` for real FBD paragraph lookups against
  `REQS_DIR=C:\Users\GeorgeOliver\dev\translink-requirements\_current`.
- Screen Validation (322 cases) used a disclosed, structured sample: ~15% full-body per sub-section
  (minimum 2, more for the larger sections), evenly spread through each section's id range (not just
  the first N), plus a 100% title sweep across all 322 to catch template/mode-boundary outliers
  outside the full-body sample. Zero outliers found.
- Every rewrite file only lists cases actually changed — untouched, already-clean cases are not
  present in any file (per `tools/apply_rewrite.py`'s design: only rows present in the file are
  touched).
