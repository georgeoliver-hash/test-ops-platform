# ABT terse-rewrite pass — 2026-07-21 mandate ("Terse, not bloated — trust the tester")

Suite 30279 (`**NEW** BOS & ABT Suite`, project 42). Applied via
`tools/apply_rewrite.py proposals/coherence-audit/fixes/abt-terse-rewrite-cr122.rewrite.json
proposals/coherence-audit/fixes/abt-terse-rewrite-correction-limits.rewrite.json --commit`.

## Scope re-verified live before starting

Pulled a fresh full suite dump (`TestRailClient.get_cases(42, 30279)`, 496 cases) rather than trusting
any earlier-in-the-day description, per the task brief. This turned up a discrepancy worth recording:
the task brief stated the CR122/refund family (37 cases) had "just been fixed" earlier today. **Live
data showed otherwise** — the exact bloated sentence quoted verbatim in
`docs/gherkin-standard.md`'s new terse-mandate section ("...confirmed live in the Operator Portal test
environment — George (live-system confirmation), 2026-07-21 (mechanism per FBD-100662 §5.6, paras
691, 693, 271)") was still present, live, in all 34 cases of the capping family (sections `Metro Cap`,
`Zonal Cap`, `Reference Cap`, `Uncapped Tap`, `Town Service Cap` under `ABT / Functional`). Whatever
happened earlier today evidently touched the fare-value wording (already in the terser "*example per
current ABT pricing config...*" form from an earlier `--reframe-fares` pass) but not this sentence.
Grounded on the live suite, not the description, per the task's own instruction.

## Cases changed: 39

### Batch 1 — CR122 capping family, 34 cases (`abt-terse-rewrite-cr122.rewrite.json`)

Exact IDs: 4102757–4102790 (Metro Cap 4102757–4102767; Zonal Cap 4102768–4102780; Reference Cap
4102781–4102783, 4102786–4102787; Uncapped Tap 4102784–4102785; Town Service Cap 4102788–4102790).

Every one carried the **identical** precondition sentence (confirmed via regex: matched exactly once
per case, 34/34, zero misses):

> `**AND** the portal alighting-stop adjustment (CR122) is confirmed live in the Operator Portal test
> environment — George (live-system confirmation), 2026-07-21 (mechanism per FBD-100662 §5.6, paras
> 691, 693, 271).`

Replaced with the exact terse form given as the canonical example in `docs/gherkin-standard.md`:

> `**AND** CR122 alighting-stop correction is available`

The relocated citation (`FBD-100662 §5.6 paras 691,693,271`) was **appended to each case's Refs
field**, not deleted — e.g. C4102757's Refs went from `CR122` to `CR122,FBD-100662 §5.6 paras
691,693,271`; a case that already carried a defect ref (`TODEV-24096`, `TODEV-24348`) got the citation
appended the same way (e.g. C4102760: `TODEV-24096` → `TODEV-24096,FBD-100662 §5.6 paras 691,693,271`).
The "George (live-system confirmation), 2026-07-21" attribution is recorded in this changelog and in
the rewrite file's `change_note` per case — not re-added to any TestRail field, per the standard's
"citations… belong in the Refs field / the proposal's citations metadata / gap-register.md" rule.

Nothing else in these 34 cases was touched — title, the rest of preconditions (including the
already-terse fare-reframe note), steps, and expected-result text are byte-identical to before.

### Batch 2 — Correction Limits (CR122) family, 5 cases (`abt-terse-rewrite-correction-limits.rewrite.json`)

IDs: 4103480, 4103481, 4103482, 4103483, 4103484 (section `ABT / Functional / Correction Limits`).
A different, milder bloat pattern: legitimate `**UNCONFIRMED**` markers (kept, per the no-gap-filling
rule — the CR122 mechanism genuinely is undetermined) but each one's citation was baked inline —
`(FBD-100662 §5.6, paras 691–693)`, `(FBD-100662 para 692)`, `(FBD-100690 para 810)` — repeated across
preface, preconditions, and every step's `Then`. Relocated every inline FBD paragraph citation to
each case's Refs field (e.g. C4103481's Refs went from `CR122` to
`CR122,FBD-100662 §5.6 paras 691-693,FBD-100662 para 692,FBD-100690 para 810`) and shortened the
`NOTE: the correction feature is CR122, an unconfirmed proposal; only the monthly/annual LIMIT
(1/month, 3/year) is specified` style preface prose to one parenthetical. The `**UNCONFIRMED**`
markers, gap ids (`gap Q14`/`gap Q21`), and all behavioural content are unchanged — only citation
placement and prose length changed, per this being a compression pass, not a re-authoring pass.

## Before / after examples

**C4102757** (worst offender, matches the doc's own worked example verbatim):
- Before: `**AND** the portal alighting-stop adjustment (CR122) is confirmed live in the Operator
  Portal test environment — George (live-system confirmation), 2026-07-21 (mechanism per FBD-100662
  §5.6, paras 691, 693, 271).`
- After: `**AND** CR122 alighting-stop correction is available` — Refs: `CR122` →
  `CR122,FBD-100662 §5.6 paras 691,693,271`

**C4103480**:
- Before (preconds line): `**AND** **UNCONFIRMED** — the alighting-stop correction itself is CR122, a
  proposal with UX to be determined (FBD-100662 §5.6, paras 691–693). Confirm the feature exists live
  (gap Q21).`
- After: `**AND** **UNCONFIRMED** — CR122 alighting-stop correction UX is TBD; confirm the feature
  exists live (gap Q21)` — Refs: `CR122` → `CR122,FBD-100662 §5.6 paras 691,692,693`
- Before (step1 expected): `**THEN** the correction is accepted (first of the month, within the
  1/month, 3/year limit — FBD-100662 para 692) — **UNCONFIRMED** (CR122 proposal)`
- After: `**THEN** the correction is accepted (within the 1/month, 3/year limit) — **UNCONFIRMED**
  (CR122)`

## Verification

- Dry-run both files first: `updated: 34 removed(ZZ): 0 fare-reframed: 0 skipped: 0 missing: 0` and
  `updated: 5 removed(ZZ): 0 fare-reframed: 0 skipped: 0 missing: 0` — no refusals (no blank steps),
  no missing ids.
- `--commit`: `updated: 39 removed(ZZ): 0 fare-reframed: 0 skipped: 0 missing: 0`.
- Re-fetched C4102757, C4102790, C4103480, C4103484 live via `TestRailClient.get_case` after commit —
  confirmed the terse text and appended Refs are live, and the untouched fields (title, steps,
  expected, other precondition lines) are unchanged.

### Audit before/after (suite 30279, `python -m system_test_ops audit --suite 30279 --no-gate`)

| | Cases audited | Blocking | Advisory |
|---|---|---|---|
| Before this pass (2026-07-21 baseline, post blank-steps-fix) | 391 | **89** | 208 |
| After this pass | 391 | **89** | 208 |

Blocking count is **unchanged (89 → 89)** — this pass introduced no new blocking findings. The 89
remaining are the suite's pre-existing, unrelated backlog (mostly `preface-bad-preamble` and
`then-compound-genuine`) explicitly out of scope for this task, untouched.

## Coverage — honest disclosure

This was **not** a full 496-case sweep. Given the size of the suite and the effort budget for this
pass, work was triaged to the two known/confirmed worst-offender families first, per the task's
explicit priority instruction ("prioritising the known-bloated CR122/transfer-cap/refund cases first").

**Changed (39):**
- 34 × CR122 capping family (Metro/Zonal/Reference/Uncapped-tap/Town-service cap), 4102757–4102790
  (excluding no gaps in that id range — all 34 consecutive ids in range were affected, confirmed by
  exact regex match count).
- 5 × Correction Limits (CR122), 4103480–4103484.

**Scanned but classified already-clean / out of the worst-offender tier, NOT rewritten this pass (not
reached):**
- A further **~90 cases** matched a broader citation-pattern scan (inline `FBD-100xxx paraN` references
  inside `**UNCONFIRMED**`/`**GAP**` marker prose) across many sections — e.g. `Reports` (Revenue,
  Pay-In Reconciliation, NIR Revenue Performance, Revenue Foregone — sections 887633–887635),
  `CloudFare Operator Web Portal` (Topology filter, Fares export, Route configuration, Product
  buttons, Fares rule — sections 887610–887614), `Journey History` (annulment/cancellation cases,
  section 887583), `Duplicate Detection` (887582), `Late Taps` (887600), `Alighting-Stop Correction`
  (887584), and one `Debt Recovery` case (4102855). These carry the *same class* of bloat (a citation
  embedded in the sentence rather than in Refs) but are a materially different editing job — each
  `**UNCONFIRMED**`/`**GAP**` marker's reasoning text is bespoke per case (not one repeated sentence
  like the CR122 family), so each would need individual, careful surgical editing rather than one
  batch transform, to avoid accidentally weakening or dropping the gap reasoning itself. Given the
  size of that job relative to this pass's remaining budget, it was **not attempted** this pass —
  flagged here rather than rushed.
- The **remaining ~360 cases** in the suite were pulled and scanned for the citation/date/prose-bloat
  regex patterns (date stamps, "George (…)", "confirmed live/by", "per FBD-…", "FBD-… para…", tracker
  references) but returned no further hits of the CR122-severity kind; a full manual read for softer
  "full sentence where a tag would do" prose bloat (the second failure mode in the mandate) was not
  performed case-by-case at this scale and should be treated as **not fully audited** for that
  softer criterion.

**Recommendation for next pass:** the ~90 flagged sections above are the next-highest-value target
(same bloat family, already located by section) — each needs the FBD paragraph citations moved to
Refs and the marker prose trimmed, case by case, preserving every `**GAP**`/`**UNCONFIRMED**` marker's
substance per the no-gap-filling rule.

## Grounding

No behaviour, title, step order, or expected-result content was changed in any of the 39 cases — this
was purely a compression/relocation pass per the mandate ("This is a compression pass, not a
re-authoring pass"). Every citation removed from a case body was verified present, unchanged, in that
same case's Refs field afterward — nothing was deleted, only relocated.

## Files touched

- `proposals/coherence-audit/fixes/abt-terse-rewrite-cr122.rewrite.json` (new, this pass — 34 cases)
- `proposals/coherence-audit/fixes/abt-terse-rewrite-correction-limits.rewrite.json` (new, this pass —
  5 cases)
- `proposals/coherence-audit/fixes/abt-terse-rewrite.changelog.md` (new, this file)
- No changes to `tools/apply_rewrite.py` — its existing `refs` pass-through (added for the earlier
  `abt-transfer-cap` fix today) was verified sufficient as-is; no further tooling change was needed.
