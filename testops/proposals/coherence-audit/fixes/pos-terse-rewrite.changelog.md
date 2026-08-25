# POS terse-rewrite pass — suite 30253, 2026-07-21

Mandate: `docs/gherkin-standard.md` § "Terse, not bloated — trust the tester (George, 2026-07-21)".
Compression + citation-relocation pass only — no behaviour re-derived, nothing invented.

## Coverage

- **Suite pulled**: 628 cases (`system_test_ops cases --project 42 --suite 30253`); the CLI's
  `cases.json` is a normalised summary (no `custom_preconds`/`custom_steps_seperated`/
  `custom_expected`/`refs`), so full raw bodies were pulled directly via
  `TestRailClient.get_cases(42, 30253)` and dumped to
  `reports/tfts-system-test/new-pos-acceptance-suite/2026-07-21/case-bodies-raw.json` for reference.
- **Classified**: all 628 active cases (audit covers 528 — the ~100 gap is `ZZ_DELETE_DUP`/
  `ZZ_DELETE_REVIEW` cases already retired from earlier folds, out of scope, untouched).
- **Method**: targeted every phrase named in the mandate's own failure examples (`— George`,
  `confirmed live`, `per FBD-#####`, `(gap Q##)`, `20XX-XX-XX` dates, `source:`, `CONFIRMED (`,
  `live-system confirmation`, `gap-register`, `audit 20…`, plus generic `FBD-`, `confirm against`,
  `reference table`, `as per`, `Overflow`) across preface/preconds/steps/expected of every case, then
  hand-read every hit to separate real violations from false positives.
- **Result**: **22 cases changed**, **~300 false-positive hits excluded** (Screen Validation cases'
  `Design reference (Overflow): …` block in the Preface is a *different*, already-sanctioned
  convention — CLAUDE.md: "Screen-validation cases carry the Overflow link + image filename in the
  preface instead", not inline provenance in Given/When/Then — left untouched), **remainder of the
  628 (≈606) already clean** — a random 15-case sample and the longest-body outliers were hand-read
  and found already terse/declarative (this suite went through prior terse/executable rewrite passes
  per git history — "ABT executable re-write complete", "major update" — so most of the backlog this
  mandate targets was already retired before today).
- **Not reached**: none. All 628 cases were scanned; all flagged cases were rewritten; no case was
  silently skipped for time.

## What changed (by pattern)

1. **11 Rail FLU / Cross-Border cases** (4099970, 4099971, 4099972, 4099976, 4100429, 4100501,
   4100502, 4099977, 4099978, 4099979, 4099980) — precondition worked-examples carried
   `(… confirm against the NIR fares reference table, FBD-100450)`. `FBD-100450` moved to Refs;
   clause shortened to `(confirm against NIR fares reference table)`.
2. **1 Bus FLU case** (4100374) — `(fares confirm against the fares export; Fare Stage names per
   FBD-100207)` → `FBD-100207` to Refs, clause shortened to `(confirm against fares export; Fare
   Stage names per current config)`.
3. **7 Top Up / Smartcard cases** (4100007, 4100009, 4102560, 4102564, 4102565, 4100415, 4100416,
   4100418) — bare or lightly-wrapped `(… — FBD-100250/60/61/71)` citations in the precondition;
   citation relocated to Refs, operational detail (e.g. "Fare Foregone", "a Corporate card",
   "passback always applies and takes priority over transfer") kept in the body since it's fact the
   tester needs, not provenance.
4. **2 heavy-provenance cases** (4100360, 4100436) — the worst offender pattern, a full
   `**CONFIRMED (George, live-system confirmation, 2026-07-21)** — … Closes gap-register.md Q18 and
   resolves the prior CONFLICT with C#### (audit 2026-07-17) …` paragraph baked into the Preface.
   Attribution/date/gap-register-id/audit-history relocated to Refs; Preface now states only the
   behaviour. While re-aligning 4100436, found its EXPECTED summary was stale from the earlier
   half-applied fix (still said "FLU inactivity → Idle, no break", contradicting its own steps,
   which already route through the Operator Break screen) — corrected the summary to match the
   steps it already has (no new fact introduced, just removed a self-contradiction surfaced by this
   edit).

## Before / after

**4100436 preface** —
Before: `... **CONFIRMED (George, live-system confirmation, 2026-07-21)** — break mode is used, not
skipped, for the Auto Sign Off destination; closes gap-register.md Q18. This case previously
modelled the FLU/Auto-Sign-Off timeout as skipping break mode ('break mode skipped'), in direct
conflict with C4100360 (audit 2026-07-17). Corrected below to route through the Operator Break
screen, matching C4100360's wording.`
After: `This test is to confirm the configurable inactivity behaviour: FLU timeout signs off via
Operator Break; Idle timeout (or continued inactivity on the Operator Break screen) suspends;
suspend duration auto-reboots.`
Refs: `George live-system confirmation 2026-07-21 (resolves gap-register Q18),supersedes conflict
with C4100360, audit 2026-07-17`

**4102560 precond** —
Before: `a smartcard has just been validated on the POS (passback always applies and takes priority
over transfer — FBD-100271)`
After: `a smartcard has just been validated on the POS (passback always applies and takes priority
over transfer)` — Refs: `FBD-100271`

**4099970 precond example** —
Before: `Lisburn → Belfast Lanyon Place, Adult, Single (stations/price confirm against the NIR fares
reference table, FBD-100450)`
After: `Lisburn → Belfast Lanyon Place, Adult, Single (stations/price confirm against NIR fares
reference table)` — Refs gains `FBD-100450`.

## Apply

- Proposal: `proposals/coherence-audit/fixes/pos-terse-rewrite.rewrite.json` (22 rows, generated by
  `proposals/coherence-audit/fixes/build_pos_terse_rewrite.py`, kept alongside for reproducibility —
  every substitution was hand-verified against the source text, listed in that script's comments,
  not a blind regex sweep).
- `tools/apply_rewrite.py` already supported a `refs` merge/set pass-through (added by a prior
  session earlier the same day — checked `git log -- tools/apply_rewrite.py`, confirmed present in
  the committed version, no extension needed).
- Dry-run then `--commit`: `updated: 22  removed(ZZ): 0  fare-reframed: 0  skipped: 0  missing: 0`.
  Spot-checked 5 of the 22 post-apply directly from TestRail (`case-bodies-raw.json` re-pull) —
  reads as clean terse Gherkin, refs correctly carrying the relocated citations.

## Audit

`python -m system_test_ops audit --suite 30253` after commit: **CLEAN** (0 blocking findings across
all rules — mojibake, preface/preconds/steps/expected empties, malformed When/Then, compound-THEN,
stray tags). 528 cases audited (the ~100-case gap from 628 is pre-existing `ZZ_DELETE_*` cases,
excluded from audit scope, not part of this pass). 50 advisory findings remain (13 title-no-emdash,
37 title-too-long) — pre-existing, title-only, explicitly advisory per `CLAUDE.md`, untouched by
this pass.
