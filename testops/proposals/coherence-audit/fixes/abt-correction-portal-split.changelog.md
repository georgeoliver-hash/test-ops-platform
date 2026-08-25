# ABT alighting-stop correction — Operator/Passenger portal split (suite 30279), 2026-07-23

## Why

The 2026-07-23 "confirmed live on both portals" tidy-up (`abt-name-tidy.changelog.md`) merged 56
cases onto one generic "works on both portals" line. George flagged that as hiding a real,
spec-documented UX difference (FBD-100662 §5.6): the Operator Portal shows the recalculated fare
**before** confirm (para 693); the Passenger Portal does not, but carries a 1/month·3/year
correction limit instead (para 692) that is explicitly a passenger-abuse-mitigation mechanism, not
an Operator-side control. First plan drafted here treated the capping-math cases as genuinely
portal-agnostic (one case, worded to allow either portal) — George corrected this mid-task: even
where the underlying math is *believed* identical, a portal-specific implementation defect could
exist on one portal and not the other, so both need their own explicit test, same principle as the
card-scheme duplication done earlier. Revised rule applied: **every case in the affected family gets
an Operator Portal version and a Passenger Portal version**, each grounded on that portal's own real
mechanics — never inventing the other portal's mechanic on the wrong version. The only exception is
Correction Limits, which is inherently passenger-only per the spec's own wording.

## Scope confirmed live before starting

Queried suite 30279 for the exact precondition text `confirmed live on both the ABT Operator Portal
and Passenger Portal` (`TestRailClient.get_cases(42, 30279)`) — **56 cases**, matching the prior
tidy-up pass exactly:
- **34 capping/settlement cases** (C4102757–C4102790): Metro Daily Cap, Zonal Cap, Reference Fare
  Cap, Uncapped & Single Taps, Town Service Cap — includes C4102766 (declined-journey case).
- **22 Journey History / Alighting-Stop-Correction cases** (C4102825–C4102849, excluding
  C4102829/4102830/4102832, which are ETM-annulment cases unrelated to the CR122 portal question and
  were left untouched).

Excluded by design (per George's exception):
- **5 Correction Limits cases** (C4103480–C4103484) — stay Passenger-only. FBD-100662 para 692
  states the limit exists "to mitigate abuse of this system via the passenger portal" — there is no
  Operator-side equivalent to duplicate, since the limit doesn't apply to operator-initiated
  corrections. Verified unchanged post-push.

## What changed

### Section structure

New sections created (via `TestRailWriter.find_or_create_section_path`, add-only — no existing
section moved or deleted, per this TestRail instance's API constraints):

```
ABT / Operator Web Portal / Tap Correction / Metro Daily Cap
ABT / Operator Web Portal / Tap Correction / Zonal Cap
ABT / Operator Web Portal / Tap Correction / Reference Fare Cap
ABT / Operator Web Portal / Tap Correction / Uncapped & Single Taps
ABT / Operator Web Portal / Tap Correction / Town Service Cap
ABT / Operator Web Portal / Tap Correction / Journey History
ABT / Operator Web Portal / Tap Correction / Update Stop List

ABT / Passenger Web Portal / Tap Correction / Metro Daily Cap
ABT / Passenger Web Portal / Tap Correction / Zonal Cap
ABT / Passenger Web Portal / Tap Correction / Reference Fare Cap
ABT / Passenger Web Portal / Tap Correction / Uncapped & Single Taps
ABT / Passenger Web Portal / Tap Correction / Town Service Cap
ABT / Passenger Web Portal / Tap Correction / Journey History
ABT / Passenger Web Portal / Tap Correction / Update Stop List
```

(14 new leaf sections, mirroring the existing subsection names under the old top-level `ABT / Tap
Correction` (887575), `ABT / Journey History` (887583), and `ABT / Update Stop List` (887584).)

**Old sections**: left in place, not deleted (API cannot delete/re-parent). `ABT / Tap Correction`
(887575) and its 5 subsections, plus the CR122-related cases in `ABT / Journey History` (887583) and
`ABT / Update Stop List` (887584), now hold only `ZZ_DELETE_REVIEW`-prefixed retired cases (887583
also still holds its 3 legitimate, untouched ETM-annulment cases — C4102829/4102830/4102832 — so
that section is not fully retired). Per repo convention, a human bins the emptied old sections via
the TestRail UI; the API does not support deleting/re-parenting sections.

### Cases: 56 pairs created (112 new cases), 56 sources retired

Every one of the 56 in-scope cases now has an **Operator Portal** version and a **Passenger Portal**
version (new case ids **C4104131–C4104242**). The 56 original cases were retired
(`ZZ_DELETE_REVIEW` title prefix, not hard-deleted).

**How the two versions differ, case by case:**

- **51 of the 56 pairs** (all 34 capping/settlement cases + 17 of the 22 Journey-History/Update-
  Stop-List cases): the underlying mechanism (capping/settlement math, or which onward stops are
  offered) is not documented as differing between portals anywhere in FBD-100662 — para 691 says the
  mechanism applies "via the passenger and operator portals" as one recalculation/cap/refund
  behaviour, and para 693's stop-selection rule ("after boarding, same route") is stated once, not
  per-portal. So these 51 pairs are **near-identical test procedures, repeated per portal on
  purpose** — only the portal name in the precondition/steps changes (e.g. "you are signed in to the
  ABT Operator Portal" vs "...Passenger Portal", "in the Operator Portal you correct..." vs "in the
  Passenger Portal you correct..."). This is intentional duplication, not redundancy: a portal-specific
  implementation bug in the capping/settlement path could exist on one portal's correction flow and
  not the other, so each portal needs its own explicit pass/fail. Refs updated
  (`George-2026-07-23-CR122-operator-portal-split` / `...-passenger-portal-split`) in place of the
  now-stale `George-2026-07-22-CR122-passenger-portal-only` pointer.
- **1 pair genuinely bespoke, not a find/replace** — **C4102842** ("selecting a stop updates the
  alighting stage and recalculates the fare"), split into:
  - **C4104227** (Operator, `.../Tap Correction/Update Stop List`) — *"Operator Portal previews the
    recalculated fare before confirming"*: WHEN you select an onward stop, the Operator Portal
    displays the recalculated fare **before** you confirm (FBD-100662 para 693); THEN the previewed
    fare matches the selected stop's fare, confirming updates the alighting stage and recalculates
    caps.
  - **C4104228** (Passenger, same section) — *"Passenger Portal updates the alighting stage without
    a fare preview"*: WHEN you select an onward stop and confirm with **no fare preview shown**
    beforehand; THEN the alighting stage updates and the fare recalculates post-confirm. Neither
    version asserts the other portal's mechanic (no invented fare-preview step on the Passenger case,
    no invented monthly-limit check on the Operator case).
  Both still cite FBD-100662 para 691/693 and TODEV-24300; both carry the correct single-portal
  `confirmed live on the ABT <Portal> Portal` precondition (replacing the merged "both" line) plus the
  portal's own real mechanic as a background fact.
- All other capping/Journey-History/Update-Stop-List `**UNCONFIRMED**`/`**GAP**` markers (stop counts,
  "No options" wording, fare>0/zero/negative-fare filters, operator-match rule, transfer-icon/
  retention behaviour — gap Q21b) were **carried over unchanged** into both portal versions — the
  audit found no spec basis to assert these filter rules differ by portal either, so duplicating them
  unresolved (not inventing an answer) is correct per the no-gap-filling rule.

**Correction Limits (C4103480–C4103484)**: left completely untouched, still in `ABT / Passenger Web
Portal / Correction Limits` (887750) — already correctly nested, no Operator equivalent authored.

**Untouched, out of scope**: C4102829, C4102830, C4102832 (ETM-annulment Journey History cases, no
CR122/portal dependency).

## Grounding

- FBD-100662 §5.6 para 691: CR122 "propose[s] to add a mechanism to change the alighting stop of TOO
  journeys via the passenger and operator portals… ABT recalculates the fare… a transaction will
  automatically refund/charge" — the shared mechanism both portal versions of the 51 near-identical
  pairs assert.
- FBD-100662 para 693: "operator portal (not passenger) shows the new fare before confirm" — the one
  genuine per-portal UX difference, grounding the C4102842 Operator/Passenger split.
- FBD-100662 para 692: passenger correction limited "to mitigate abuse... via a passenger" (1/month,
  3/year) — grounds keeping Correction Limits Passenger-only, no Operator duplicate.
- `gap-register.md` Q1/Q2 (session 2026-07-23, third reversal): both portals confirmed live by
  George — the precondition this whole family now cites per-portal instead of merged.

## Verification

- Dry-run (`push_abt_portal_split.py`, no `--commit`): 112/112 new cases would create (0 skipped, 0
  errors), 56/56 sources would retire (0 missing).
- `--commit`: 112 cases created (C4104131–C4104242), 56 sources retired to `ZZ_DELETE_REVIEW`.
  Post-commit suite total: 608 cases (496 + 112 new; the 56 retired cases are still counted, just
  renamed).
- `python -m system_test_ops audit --suite 30279 --no-gate`: **89 blocking findings — unchanged**
  from the pre-pass baseline (`preface-bad-preamble` ×82, `then-compound-genuine` ×7, all pre-existing
  and unrelated — none of the new C4104131–C4104242 ids or the retired ids appear in either blocking
  list). The 112 new cases appear only in the two **advisory** title checks (title-too-long,
  title-no-emdash) — expected, since portal-suffixed titles on already-detailed capping-case titles
  run long; advisory, not blocking, consistent with the standard's advisory carve-out for cases where
  precision matters more than brevity.

## Counts summary

- **56 pairs created** (112 new cases: C4104131–C4104242) — every in-scope case now has an Operator
  Portal version and a Passenger Portal version.
- **51 pairs** are near-identical, intentionally-repeated procedures (portal name substitution only)
  covering the capping/settlement math and the stop-list/retention mechanics, which no spec source
  distinguishes by portal.
- **1 pair bespoke** (C4102842 → C4104227 Operator / C4104228 Passenger) — the one case where the
  mechanics genuinely differ (fare-preview-before-confirm, para 693).
- **5 cases kept Passenger-only, no duplication** (Correction Limits, C4103480–C4103484) — the limit
  is a passenger-only mechanism per para 692.
- **56 cases retired** (`ZZ_DELETE_REVIEW`), superseded by the 112 new portal-specific cases.
- **3 cases untouched** (ETM-annulment Journey History cases, out of scope).
- **14 new sections created**, old sections left in place holding only retired cases (pending human
  UI bin-cleanup) or their remaining non-CR122 content.
- **0 new blocking audit findings** (89 → 89, all pre-existing and unrelated).

## Files

- `proposals/coherence-audit/fixes/build_abt_portal_split.py` — generator (source cases → 112
  portal-specific variants + 56 retirements), reusable if re-run is needed.
- `proposals/coherence-audit/fixes/abt-portal-split.new-cases.json` — the 112 generated case rows.
- `proposals/coherence-audit/fixes/abt-portal-split.retire.rewrite.json` — the 56 retirement rows.
- `proposals/coherence-audit/fixes/push_abt_portal_split.py` — the writer (dry-run verified, then
  `--commit`, both logged this session).
- `proposals/coherence-audit/fixes/abt-correction-portal-split.changelog.md` — this file.
