# UB TOO tracker → ABT suite coverage cross-check (2026-07-14)

**Source:** `UB_TOO_Test_Tracker_FILLED.xlsx` (the July FILLED workbook — 5 sheets).
**Target:** live ABT suite **30279** (`TFTS - System Test`), 365 active ABT/BOS cases.
**Method:** parsed every tracker sheet to its test index and matched each against the live
`cases.json` pulled today. No TestRail writes.

## Headline

| Tracker sheet | Tests | Our coverage | Verdict |
|---|---|---|---|
| CR122 Test Tracker | 18 | 18 live cases under `Tap Correction/*` | **COVERED 18/18** |
| TODEV Test Tracker | 81 (9 defects) | 1:1 across Tap Correction / Annulment / Duplicate / Journey History / Update Stop List / Debt Recovery | **COVERED** |
| UBTOO Test Tracker | 36 runs / 50 scripts (Groups A–G) | Partial — see gaps | **GAPS** |
| Coverage Matrix | (run→script map) | n/a (index only) | — |

The suite was hand-authored in June from the **CR122 + TODEV** sheets, so those map cleanly.
The **UBTOO Test Tracker sheet is newer than the build** — that is where the gaps are.

## CR122 — 18/18 covered

Every CR122 tap maps to a live case:
- Metro Daily Cap M1–M3 → `Tap Correction/Metro Daily Cap` (same-fare holds / outside removes+charges / into-zone applies+refunds).
- Zonal Cap Z1–Z5 → `Tap Correction/Zonal Cap` (higher-in holds / higher-out removes / lower-in holds / lower drops-below refunds / Zone-4 highest-band holds).
- Reference Fare Cap R1–R3 → `Tap Correction/Reference Fare Cap`.
- Uncapped U1–U4 → `Tap Correction/Uncapped & Single Taps`.
- Town Service T1–T3 → `Tap Correction/Town Service Cap`.

> Note: tracker **TC-T3 is marked BLOCKED** — no route geometry where an outside-TS-zone stop is
> cheaper than an inside one. Our case exists but is practically unexecutable; flag it as
> known-blocked rather than a live gap.

## TODEV — covered (built from this sheet)

The 81 TODEV TCs map 1:1 to our sections: 23967 → Annulment & Re-tap; 24061 & 24397 → Journey
History; 24096 → Tap Correction/Metro Daily Cap (settled-cap guard, 8 cases); 24258 → Duplicate
Detection; 24259 → Annulment & Re-tap (retained-valid-tap); 24300 → Update Stop List; 24348 →
Tap Correction/Zonal Cap (8 cases); 24990 → Debt Recovery.

## UBTOO Test Tracker — the gaps (Groups A–G)

These are **UB ETM Tap-On-Only** execution scenarios; the tap-making is on the ETM, the cap maths
is verified at back-office EndOfDay settlement. Our suite tests **corrections and defect
regressions around** caps — but not the **base cap-calculation** scenarios these groups exercise.

| Group | Runs | What it exercises | Our coverage | Gap? |
|---|---|---|---|---|
| **A** — Combined UB ref cap + Metro cap | A01–A10 | Both caps hit same card-day (ref.60 2/3-tap, multi-route, 4 ref-bands, annul+re-apply) | Corrections assume "cap already reached"; base combined-cap runs not present | **GAP (base capping)** |
| **B** — Metro + UB cap standalone/interleaved | B01–B06 | Metro cap; UB ref cap; both; interleaved; ref.60 **and** ref.61 independently; lone-tap negatives | Not present as execution cases | **GAP (base capping)** |
| **C** — UB annulments | C01–C04 | Annul 1st of 2 → no cap; cap-tap annulled → no free £0 tap; wrong audit-order refused | Covered behaviourally by `Annulment & Re-tap` (25 cases) | Covered |
| **D** — Metro/UB in-zone annulments | D01–D04 | Cap removed then re-applied by annulment; free-then-annulled tap | Covered behaviourally by `Annulment & Re-tap` | Covered |
| **E** — Metro/Zone cross-cap | E01–E03 | Lone Metro + outside-zone UB → UB cap only; per-band lone taps → no cap; Metro cap **and** ref.35 cap | Not present | **GAP (base capping)** |
| **F** — Late taps combined | F01–F04 | Taps held on **blocked ETM**; intraday late (live+held); cross-settlement reconcile; late + annulment | `Processing Taps/Late Taps` (4 cases) covers the principle (within/beyond late window, retrospective capping, duplicate late taps) but **not** the blocked-ETM / cross-settlement / late-with-annulment combinations | **PARTIAL** |
| **G** — Alighting-stop correction limits | G01–G05 | CR122 limit enforcement: **1 correction/calendar month, 3/year**; boundary at 3rd-of-year | No case tests the *limit*; we test correction *behaviour* only | **GAP (not covered)** |

### Recommended additions (to ABT suite 30279)

1. **`ABT / Functional / Daily Capping`** (new section) — base cap execution, folding Groups A/B/E as
   variation-lined cases (house style, not 36 separate runs):
   - Metro daily cap reached and applied (£4.00).
   - UB reference-fare cap reached, per ref band (ref.10/.20/.35/.45/.55/.60/.61) — variation line.
   - Metro cap **and** UB ref cap both hit in one day; taps interleaved; order-independent.
   - Two ref bands cap independently (ref.60 £7.20 **and** ref.61 £8.20).
   - Cross-cap negatives: lone Metro tap / lone per-band UB tap → no cap applied.
2. **`ABT / Functional / Correction Limits`** (new, from Group G + CR122 Legend) —
   1st correction/month accepted; 2nd in month refused; 1st in new month accepted; 4th in year
   refused; boundary (3rd-of-year accepted, immediate 4th refused). Refs: CR122.
3. **Extend `Processing Taps / Late Taps`** with the Group F combinations: taps held on a blocked
   ETM released on unblock; intraday late (live + held); cross-settlement reconciliation; late tap
   accompanied by an annulment.

## Open question for George (ownership)

The UBTOO groups are **ETM Tap-On-Only** device scenarios. Per our test-ownership split (device
suites keep the light "event reached back-office" step; the BOS/ABT suite owns deep capping/
settlement maths), the **base capping calculation** belongs in ABT 30279 — but the **tap-execution**
side may duplicate ETM-suite coverage. Decide: author the base-capping + limit + late-tap cases in
**ABT 30279** (recommended — it owns the cap maths), and cross-reference from the ETM suite rather
than duplicate.

## Housekeeping (unrelated to gaps)

- Live suite currently shows **99 `ZZ_DELETE_REVIEW`** cases (the first-cut ABT set) still awaiting
  your bin in the TestRail UI — that is why the pull returned 464 rows vs 365 active.
- Tracker data-quality notes to raise with the tracker author: route "100a (IN)" in A10/Script 26
  should be **100c** (Castlederg→Killeen Road, ref.35); "Agricultural College" stop in E03 not found
  in the reference CSV — confirm.
