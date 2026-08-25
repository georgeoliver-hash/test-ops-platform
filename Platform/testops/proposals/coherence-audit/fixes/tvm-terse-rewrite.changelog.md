# TVM terse-rewrite (compression + citation relocation) — changelog

**Suite:** `**NEW** TVM Test Suite` (30284), project 42, TFTS - System Test. **Mandate:**
`docs/gherkin-standard.md` § "Terse, not bloated — trust the tester (George, 2026-07-21 — a hard
rule)" — a compression pass, not a re-authoring pass: shorten prose to tags, relocate every
citation/date/confirmation-attribution/spec-paragraph-reference out of the Given/When/Then body and
into the case's **Refs** field. No fact re-derived, no test behaviour changed.

**Pulled fresh:** `python -m system_test_ops cases --project 42 --suite 30284` (201 total cases) plus
raw bodies via `TestRailClient.get_cases(42, 30284)` (custom_preface / custom_preconds /
custom_steps_seperated / custom_expected / refs — the `cases` CLI export flattens these into one
`custom_steps` field, which is too lossy for a targeted body-text edit, so the raw client call was
used per the task instruction).

**Active (non-`ZZ_DELETE_REVIEW`) case count: 174** — matches the task's ~174 estimate (201 total −
27 condemned earlier today in `tvm.rewrite.json`).

## Coverage

**All 174 active cases were read in full** (preface + preconditions + every step + expected-result,
not just titles) — the raw JSON was read case-by-case across the whole file, not sampled. Two
independent programmatic scans were also run over the same data as a second pass to catch anything
missed by eye:

1. A citation/provenance regex over every field (`George`, date `2026-07-\d\d`, `confirmed (by|live)`,
   `live-system confirmation`, `per FBD-\d+`, `(FBD-\d+ ...)`, `FBD-\d+ para/§`, `CORRECTED`,
   `gap-register`).
2. A line-length heuristic for full-sentence bloat (>25 words on one Given/Then line).

**Result: 9 of 174 cases needed a change. 165 were already clean** (terse tags/fragments, no inline
citations — the suite's baseline style, outside today's touched cluster, was already conformant).
Two line-length hits (C4103639, C4103681) were checked and are **false positives** — their length
comes from legitimate concrete worked examples (the "concrete grounding" rule), not bloat; left
untouched. Two name-collision false positives on the provenance regex (C4103760 "George Best City
Airport", C4103763 "corrected roll length") were also checked and are benign; left untouched.

**Not reached:** none — every active case in the suite was inspected. 0 cases outstanding.

## The 9 cases changed

### A. The 4 cases carrying the literal "George (live-system confirmation), 2026-07-21" clause
(today's barcode/Scottish-note fixes — exactly the task's named prime targets)

| Case | Before (preface excerpt) | After |
|---|---|---|
| **C4103628** — Single-Use only, multi-use CTC rejected | "...there is no barcode scanner (FBD-100317; confirmed by George (live-system confirmation), 2026-07-21)." | "...no barcode scanner." Citation → Refs: `FBD-100167,FBD-100317,confirmed George (live-system) 2026-07-21` |
| **C4103641** — Banknotes, Scottish note accepted | "...**CORRECTED 2026-07-21** — this case previously asserted the note was rejected... George confirms it should be accepted... (gap-register Q15)." | "...the same as a Bank of England note." (one plain sentence). Citation → Refs: `confirmed George (live-system) 2026-07-21; gap-register Q15` (refs was previously empty) |
| **C4103677** — Ticket Collection, pre-paid ticket collected | "...the TVM has no barcode scanner (FBD-100317; confirmed by George (live-system confirmation), 2026-07-21)." | "...the TVM has no barcode scanner." Citation → Refs: added `FBD-100317,confirmed George (live-system) 2026-07-21` (FBD-100317 wasn't in Refs before) |
| **C4103729** — Ticket Collection, collect via booking reference | "...does not accept a BRID scan — booking-reference/Collect Ticket Code entry only (FBD-100317; confirmed by George (live-system confirmation), 2026-07-21)." | "...does not accept a BRID scan." Citation → Refs: added `FBD-100317,confirmed George (live-system) 2026-07-21` |

**Bonus finds while verifying coherence (not new fact-finding — just consistency):** the earlier
same-day fixes to C4103641 and C4103729 had corrected the preface/steps but left the
**`custom_expected`** field stale, so each case's summary line directly contradicted its own body:

- **C4103641** `expected` still read *"Non-sterling notes are rejected and returned. Data
  variations —Scottish notes, Euros..."* — the exact opposite of the corrected "Scottish notes are
  accepted" behaviour. Fixed to: *"The Scottish banknote is accepted as valid sterling. Data
  variations — Scottish (accepted); Euro / other non-sterling currency (still rejected)."*
- **C4103729** `expected` still read *"A valid **BRID** collects and prints the pre-paid ticket."* —
  using the exact term ("BRID") the same fix had explicitly said was wrong for this device (no
  scanner, no BRID). Fixed to: *"A valid booking reference (Collect Ticket Code) collects and prints
  the pre-paid ticket."*

These two field fixes don't re-derive anything or change what's tested — they apply the correction
George already gave today to a field the first pass missed, per the "one scenario, aligned" rule
(title/preface/steps/expected must describe the same behaviour).

### B. 5 further cases found by the broader sweep — redundant inline FBD citations
(not part of today's touched cluster, but the same violation: a spec paragraph reference sitting in
body text that's already carried in Refs)

| Case | Before | After |
|---|---|---|
| **C4103620** | precond: "...for a Rail Adult Single **per FBD-100483**" | "...for a Rail Adult Single" (Refs already has FBD-100483) |
| **C4103625** | precond: "...does not match the product **per FBD-100483**" | "...does not match the product" (Refs already has FBD-100483) |
| **C4103696** | precond: "...priced per the NIR fares export **(FBD-100450)**" | "...priced per the NIR fares export" (Refs already has FBD-100450) |
| **C4103693** | expected: "...carried to MERIT **(FBD-100341 apportionment)**." | "...carried to MERIT (apportionment)." (Refs already has FBD-100341; kept the "apportionment" fact, dropped the redundant cite) |
| **C4103703** | expected: "...printed on the ticket **(FBD-100515, rail-only group)**." | "...printed on the ticket (rail-only group)." (Refs already has FBD-100515; kept the "rail-only group" fact) |

No Refs changes needed for this group — the citation was already present in Refs, only the
redundant in-body duplicate was removed.

## Push

```
$env:TESTRAIL_WRITE_SUITE_ID="30284"
python tools/apply_rewrite.py proposals/coherence-audit/fixes/tvm-terse-rewrite.rewrite.json --commit
```
Dry-run and commit both reported: `updated: 9  removed(ZZ): 0  fare-reframed: 0  skipped: 0  missing: 0`.

`tools/apply_rewrite.py` already supported `refs` pass-through (added by an earlier sibling pass
today — confirmed present at lines 129-131 before this task started); no code change was needed.

## Audit

```
python -m system_test_ops audit --suite 30284
```
**CLEAN** — 174 cases audited, 0 blocking findings, 24 advisory `title-too-long` (pre-existing,
identical count to before this change — unrelated to this pass).

## Totals

| Category | Count |
|---|---:|
| Total active cases reviewed | 174 |
| Needed citation relocation + compression (today's touched cluster) | 4 |
| Needed citation relocation only (broader sweep, redundant inline FBD refs) | 5 |
| Already clean (no change) | 165 |
| Cases not reached | 0 |
| **Total rewrite entries pushed** | **9** |

**Not touched:** every other TestRail suite; all 27 previously condemned (`ZZ_DELETE_REVIEW`) cases
from `tvm.rewrite.json` (untouched by this pass — out of scope, already handled).
