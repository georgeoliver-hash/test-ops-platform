# ABT/BOS suite (30279) — name-tidy + stale-UNCONFIRMED reconciliation, 2026-07-23

Two specific cleanups George flagged directly, plus a mid-task correction folded in when the
underlying CR122 fact changed again while this pass was in flight.

## Scope re-verified live before starting

Pulled a fresh full dump of suite 30279 (`TestRailClient.get_cases(42, 30279)`, 496 cases) rather than
trusting the task brief's carried-over numbers. A case-insensitive scan of preface/preconditions/
steps/expected across all non-`ZZ_DELETE_REVIEW` cases found:

- **61 cases with "George" inline** — exactly the brief's known set: 4102757–4102790 (34, Metro/Zonal/
  Reference/Uncapped-tap/Town-service cap), 4102825–4102849 minus 4102829/4102830/4102832 (22,
  Journey History / Alighting-Stop Correction), 4103480–4103484 (5, Correction Limits). No cases
  outside this list carried a "George" mention.
- **143 cases carrying an `**UNCONFIRMED**` marker total** — matches the brief's count exactly.

## Fix 1 — strip inline "George" mentions (61 cases)

Every one of the 61 cases' Refs field already carried the provenance pointer
(`George-2026-07-22-CR122-passenger-portal-only`) before this pass — verified programmatically
(0 missing) — so no Refs addition was needed, only relocating the inline text out of the body.

Two body patterns, both stripped of the name/date attribution and merged into one terse line:

- 34 capping-family cases had a redundant pair of precondition lines (`CR122 alighting-stop correction
  is available` + `... confirmed live on the ABT Passenger Portal — the Operator Portal does NOT have
  this function (George, 2026-07-22, reversing the 2026-07-21 answer)`) — merged into one line (see
  Fix 3 below for the final wording, corrected mid-pass).
- 22 Journey History / Alighting-Stop-Correction cases had the same "confirmed live... (George, ...)"
  line paired with a stale `**UNCONFIRMED**` precondition line (see Fix 2).
- 5 Correction Limits cases just had `(George, 2026-07-22)` appended to an otherwise-correct, already-
  terse confirmed-live sentence — the parenthetical was dropped, nothing else touched.

Result: 0 "George" mentions remain anywhere in the live suite (re-scanned post-commit).

## Fix 2 — reconcile stale UNCONFIRMED-liveness markers (22 cases)

The 22 Journey History / Alighting-Stop-Correction cases each carried a precondition pair like:

```
**AND** **UNCONFIRMED** — CR122 alighting-stop correction, UX TBD; "Update Stop list" screen name
  not in spec; confirm live (gap Q21)
**AND** CR122 alighting-stop correction is confirmed live on the ABT Passenger Portal — the Operator
  Portal does NOT have this function (George, 2026-07-22, reversing the 2026-07-21 answer)
```

The first line questions CR122's very existence/liveness — stale, since the second line (and the
gap register) already confirms it. Removed the stale liveness-questioning line in all 22 and merged
into a single confirmed-live precondition (final wording per Fix 3). Genuinely open **narrower**
Q21b questions (exact stop count, "No options" wording, fare>0/zero/negative/transfer-stop filter
rules, operator-match rule, the "**" cancelled-indicator, transfer icon) were **not** removed — where
they were duplicated between the stale precondition line and an already-correct step-level marker,
only the redundant precondition copy was dropped; the step-level marker (already correctly scoped and
not naming George) was left as the single home for that genuine gap. Two cases needed a preserved
fragment moved rather than dropped outright:
- **C4102831** — kept "the cancel/refund mechanism for a settled journey remains unconfirmed (see
  C4102830)" (a real, still-open, different question, not a CR122-liveness question).
- **C4102842** — kept the Operator-vs-Passenger fare-preview distinction (now phrased as a two-portal
  contrast per Fix 3, cited FBD-100662 para 693 — this is a genuine, spec-grounded UX difference, not
  an unconfirmed claim).

Also removed 12 **bare** step-level `**UNCONFIRMED** (CR122)` / `**UNCONFIRMED** (CR122 proposal)`
tags that asserted a whole outcome was unconfirmed purely because CR122 itself was unconfirmed (now
stale) — e.g. C4102825/4102826 ("... shows the corrected stop — **UNCONFIRMED** (CR122 proposal)"),
C4102844/4102845/4102846 ("it is correctable — **UNCONFIRMED** (CR122)"), C4102833–4102838 ("...are
offered — **UNCONFIRMED**" with no further qualifier). Every removal was checked against the
surrounding text first — where a genuine narrower qualifier was attached to the same `**UNCONFIRMED**`
tag (fare filter, stop count, "No options" wording, operator-match, retention/indicator behaviour),
only the bare/redundant part was removed and the qualifier's `**UNCONFIRMED** (gap Q21)` tag was kept
untouched (13 cases: C4102825, 4102828, 4102831, 4102833–4102849's fare-filter/count/wording lines).

Preface text was also cleaned in all 22 cases — each preface's `(CR122 — unconfirmed proposal)` /
`(CR122 unconfirmed; ...)` parenthetical was reworded to drop the stale "CR122 unconfirmed" framing
while keeping any genuine narrower note it carried (e.g. "(the fare>0 filter is not in the specs)",
"(the operator-match rule is not in the specs)"); five prefaces (C4102825–4102828, 4102831) had no
genuine narrower note attached and the parenthetical was dropped entirely.

## Fix 3 — mid-pass correction (Q1/Q2 reversed a third time)

While Fix 1/2 were being built (not yet committed), George checked the live system again and
confirmed: **the alighting-stop correction function exists on BOTH the ABT Operator Portal and the
Passenger Portal** — reversing the 2026-07-22 "Passenger Portal only" answer this pass was originally
built on (gap-register `Q1`/`Q2`, session "REVERSED AGAIN 2026-07-23"). Caught before any commit, so
only the build script needed correcting, not a second live edit:

- The merged confirmed-live line used across all 56 affected cases (34 capping + 22 Journey History)
  now reads: `**AND** CR122 alighting-stop correction is confirmed live on both the ABT Operator
  Portal and Passenger Portal` — no portal-exclusivity claim, no name/date.
- C4102842 (the one case asserting the operator-vs-passenger fare-preview UX difference) was reworded
  to state the real, still-valid distinction as a contrast rather than an exclusivity claim: `the
  Operator Portal shows the recalculated fare before confirming, the Passenger Portal (used here)
  does not (FBD-100662 para 693)` — this UX difference is unaffected by which portal has the base
  correction capability.
- The 5 Correction Limits cases were left as "confirmed live on the Passenger Portal" (unchanged
  besides the George-strip) — they test the Passenger Portal specifically and never claimed Operator-
  Portal exclusivity, so no correction was needed there.
- Re-scanned the full suite post-commit for `does NOT have this function` / `Passenger Portal only` /
  `Operator Portal only` — **0 hits** anywhere.
- `gap-register.md` Q1/Q2 were already updated directly (by the engineer) before this pass finished;
  re-read fresh, not overwritten.

## Fix 4 — C4102766 domain-fact correction (folded in mid-pass)

A separate live clarification arrived for this same case while it was in scope (it's part of the
34-case capping family): the **first** declined tap (the one that triggers a deny-listing) shows in
Journey History as declined, but **subsequent** taps on an already-denied card do not appear in
Journey History at all. C4102766's precondition used an ambiguous "the card in a deny-listed state"
example, which could be read as the latter (contradicting its own premise that the journey "is shown
in Journey History as declined"). Reworded the precondition to an unambiguous first-decline scenario:
`the card has one Metro journey whose own tap triggered the decline (e.g. Declined Reason 2, the
first tap that applies the deny-list), shown in Journey History as declined`. The case's own gap-Q25
`**UNCONFIRMED**` marker (whether a correction can be *attempted* on a declined journey at all) is a
separate, still-genuinely-open question — left untouched. `gap-register.md`'s Q25 entry already
carries this note (added directly by the engineer); not duplicated here.

## Verification

- Dry-run all three rewrite files first (`updated: 61, removed(ZZ): 0, fare-reframed: 0, skipped: 0,
  missing: 0`) before `--commit`.
- `--commit`: `updated: 61 removed(ZZ): 0 fare-reframed: 0 skipped: 0 missing: 0`.
- Post-commit full re-pull (496 cases) confirms: 0 remaining case-insensitive "George" hits outside
  `ZZ_DELETE_REVIEW` titles; 0 remaining `does NOT have this function` / `Passenger Portal only` /
  `Operator Portal only` hits; 56 cases now carry the corrected "both...Operator Portal and Passenger
  Portal" wording.

### Audit before/after (suite 30279, `python -m system_test_ops audit --suite 30279 --no-gate`)

| | Cases audited | Blocking | Advisory |
|---|---|---|---|
| Before this pass | 391 | **89** | 208 |
| After this pass | 391 | **89** | 208 |

**Unchanged (89 → 89).** None of the 61 touched case ids appear in either blocking-finding list
(`preface-bad-preamble` ×82, `then-compound-genuine` ×7) — verified by grep against
`reports/tfts-system-test/new-abt-suite/2026-07-23/alignment-audit.md`. The 89 are the suite's
pre-existing, unrelated backlog, explicitly out of scope for this task.

## Counts summary

- **61** cases had inline "George" mentions stripped (Refs pointer already present in all 61, verified
  before stripping — none needed adding).
- **22** cases had a stale CR122-liveness-questioning `**UNCONFIRMED**` marker removed/merged, plus 12
  bare stale step-level `**UNCONFIRMED** (CR122...)` tags removed; **13** genuinely-open narrower
  Q21b markers (fare filters, stop counts, "No options" wording, operator-match, indicator/retention
  behaviour) were left in place, only tersened where a redundant precondition copy was dropped.
- **1** case (C4102766) had its precondition reworded for an unrelated, separately-flagged domain-fact
  clarification (first-decline vs already-denied-card visibility) folded into this pass because it
  fell inside the same 34-case batch already being edited.
- **0** new blocking audit findings introduced.

## Files touched

- `proposals/coherence-audit/fixes/build_abt_name_tidy.py` (new, one-off builder script — safe to
  delete once this pass is reviewed)
- `proposals/coherence-audit/fixes/abt-name-tidy-capping.rewrite.json` (new, 34 cases, committed)
- `proposals/coherence-audit/fixes/abt-name-tidy-journeyhistory.rewrite.json` (new, 22 cases, committed)
- `proposals/coherence-audit/fixes/abt-name-tidy-correctionlimits.rewrite.json` (new, 5 cases, committed)
- `proposals/coherence-audit/fixes/abt-name-tidy.changelog.md` (new, this file)
- `proposals/coherence-audit/gap-register.md` — not edited by this pass (Q1/Q2/Q25 already updated
  directly by the engineer mid-task; re-read fresh, not overwritten)
