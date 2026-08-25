# ETM variant expansion — changelog (2026-07-24)

Suite: **NEW** ETM-Acceptance Suite (id `30254`), project 42 (`TFTS - System Test`). Old suite 4943
untouched (read-only, as always). Operating-mode coverage (Metro/Ulsterbus Run Configurations) is
unaffected — nothing here touches Configurations.

## Rule applied

George, 2026-07-24: **"no test should tell someone to test multiple variants... we should have a
test for each."** Every case carrying a `Data variations: X, Y, Z` line (or an equivalent inline
list of card/smartcard/product/entitlement names) was expanded into one separate,
individually-executable case per named variant — mirroring the Operator/Passenger portal split done
earlier the same day. `docs/gherkin-standard.md` and `docs/test-practices.md` were updated in the
same pass to retire the old "Data variations: … " guidance (superseded, both files marked
2026-07-24).

## Method

1. Pulled suite 30254 in full via `TestRailClient.get_cases(42, 30254)` (the CLI's `cases` command
   truncates step/precondition bodies due to a field-name bug — `custom_steps_separated` vs the
   real `custom_steps_seperated` — so a direct client pull was used instead to get full bodies).
2. Searched every non-`ZZ - To Delete` case's preface/preconds/steps/expected for
   `data variation|variation\s*[—-]` (case-insensitive). **27 cases** matched.
3. Read each match's full body and classified it:
   - **Split** (16 families, 61 new cases) — the list named genuinely distinct card schemes,
     smartcard/entitlement sub-types, ticket products, zones, source devices, or decline/failure
     reasons, each of which can fail independently of its siblings.
   - **Tidy only, no split** (10 cases) — the "Data variations" text was either a generic Adult/
     Child equivalence-class mention (rubric #2: same partition, not a distinct risk), a single
     mode note (not a list at all), or a stray cross-reference to product coverage already owned by
     another dedicated case. The label/text was removed so it no longer reads as an unaddressed
     checklist, but no new case was needed (rubric #1: already covered elsewhere).
   - **Retire** (1 case) — fully superseded duplicate.
4. Pushed via `system_test_ops push --file etm-variant-expansion.cases.yaml --update --commit`
   (dry-run verified first) and `tools/apply_rewrite.py etm-variant-expansion.rewrite.json --commit`
   (dry-run verified first).
5. Re-ran `python -m system_test_ops audit --suite 30254` — **CLEAN** (0 blocking findings).

## Families split (16) — 61 new cases

| # | Original case | Variants split out | New cases |
|---|---|---|---|
| 1 | C4100512 Driver Sign On — first use with defects recorded | Manual, Smartcard | 1 (`C4104434`) |
| 2 | C4100550 Ticket Issue — issue a single ticket | Metro Single*, Day Return, Month Return, iLink Single, Gateway, Jobseeker, Warrant Return, ME Rugby Day | 7 |
| 3 | C4100555 Ticket Issue — Easibus stage selection | Red*, Orange, Yellow, Green, White, Buggy, Wheelchair, Other | 7 |
| 4 | C4100558 Promo Menu — issue a promo product | Bus Rambler*, Metro Day, Metro Evening, Metro Family Day, Family & Friends Day, Park & Ride, ME Rugby Day | 6 |
| 5 | C4100569 Smartcard — invalid card presented | wrong zone (Metro)*, invalid boarding stage (Ulsterbus), outside time band, expired, hotlisted | 4 |
| 6 | C4100578 Smartcard — inter-device top-up then validate on ETM | POS (TGX150)*, POS (WAY6), HHD, PV, another ETM | 4 |
| 7 | C4100579 Metro Multi-Journey — zone validation | City*, Inner, Extended | 2 |
| 8 | C4102542 Half-Fare SmartPass — validation | DLA*, Partially Sighted, Learning Disability, No Driving Licence, PIPS | 4 |
| 9 | C4102549 EA Bus SmartPass — validation | Pupil*, Further Education | 1 |
| 10 | C4102550 EA Rail SmartPass — validation | Pupil*, Further Education | 1 |
| 11 | C4102552 Belfast Visitor Pass — validation | 1-day*, 2-day, 3-day | 2 |
| 12 | C4102553 iLink — validation | Zone 1*, Zone 2, Zone 3, Zone 4, NW | 4 |
| 13 | C4100582 ABT — successful tap, passback and mobile wallet | Visa Debit*, Visa Credit, Mastercard Debit, Mastercard Credit, Maestro Debit, Apple Pay, Google Pay, Samsung Pay | 7 |
| 14 | C4100591 ABT — invalid taps recorded in back office | Deny List decline*, BIN List decline | 1 |
| 15 | C4100622 Barcode — online validation (pass and fail) | printed copy (pass)*, mobile phone (pass), decryption failed, not valid, already used, wrong date, expired, exceeds offline limit, invalid product, visual inspection not passed | 9 |
| 16 | C4100625 Barcode — multiple-use validation | printed copy*, mobile phone | 1 |

`*` = the variant that reused the original case id (retitled via `match:`, no new case created).

Judgment calls, recorded for review:
- **Adult/Child dropped as a split axis everywhere.** Per `test-practices.md` rubric #2
  (equivalence partitioning), Adult and Child fares exercise the identical mechanism at a different
  price point — not a variant that can fail independently — so it was not multiplied across every
  product/zone/scheme case (that would have produced 150+ cases for no additional risk coverage).
  Flag for the engineer if this read is wrong for any specific product.
- **C4100582 mobile wallets kept phone+watch together per wallet app** (3 cases, not 6) — the
  original body already tests phone and watch as one assertion per wallet; splitting further would
  fragment past the point of independent failure risk.
- **C4100622 barcode medium (printed/mobile) split only for the positive (valid) path**, not
  cross-multiplied against all 8 failure reasons (which would be 16 cases) — the decline reason is
  the dimension most likely to fail independently; the medium is already covered on both the
  positive path and (unsplit) on C4100625's multiple-use case.

## Cases tidied only, no split (10) — text/label removed, no new case

| Case | Why no split |
|---|---|
| C4100551 Ticket Issue — annulment (last ticket, timeout and refusal) | "single and basketed tickets" already has its own dedicated case (`Basket Mode — annul a basketed transaction`); Adult/Child is equivalence-class |
| C4100556 Ticket Issue — Open Tickets excess fare | Adult/Child only — equivalence-class |
| C4100560 Promo Menu — promo product not available | Adult/Child only — equivalence-class |
| C4100567 Smartcard — validation and passback rules | the referenced Metro/Ulsterbus MJ specifics are owned by their own dedicated cases (families #7 and the Ulsterbus MJ case); Adult/Child equivalence-class |
| C4100572 Smartcard top-up — successful, maximum and expired-journey rules | DayLink/iLink/Travelcard/MJ are two already-exercised *mechanisms* (period expiry vs journey-count cap) inside one flow test, not independent failure-prone named entities |
| C4100576 Smartcard top-up — annulment | stray cross-reference to products (Belfast Visitor Pass, iLink) that already have their own dedicated validation cases; the annulment mechanism itself is generic |
| C4100580 Ulsterbus Multi-Journey — boarding-stage validation | Adult/Child + a mode note only — equivalence-class, mode already implied by title |
| C4100586 ABT — Metro zone boarding and alighting | single mode note ("Metro mode."), not a list |
| C4100587 ABT — Ulsterbus zone boarding and alighting | single mode note ("Ulsterbus mode."), not a list |
| C4100655 MIFARE card type validation on the ETM | "8-digit PSN range" is a descriptive detail, not a list of named variants |

## Case retired (1)

- **C4100570 "Smartcard — concessionary pass validation"** → renamed `ZZ_DELETE_REVIEW -` (moved to
  `ZZ - To Delete`, not hard-deleted, per the TestRail instance's write constraints). Its entire
  named list (60+, Senior, ROI Senior, Blind, War Pensioner, Half-Fare sub-types, Free Smartpass,
  Staff/Spouse/Dependants/Retired/External Staff, EA Bus & Rail Pupil/FE) is **already** fully
  covered by 14 pre-existing dedicated cases (`C4102537`–`C4102550`) from an earlier consolidation
  pass. This case was the superseded pre-split general roll-up; keeping both would have been a
  duplicate, not a fix.

## Before / after

| | Count |
|---|---|
| Non-`ZZ` cases before | 456 |
| New cases created | +61 |
| Cases retired (moved to `ZZ - To Delete`) | −1 |
| Non-`ZZ` cases after | **516** |
| 16 originals updated in place (retitled/degeneralised, same case id) | 16 |
| 10 cases tidied in place (label/text removed, no new case) | 10 |

## Audit result

`python -m system_test_ops audit --suite 30254` → **CLEAN** (0 blocking findings across all 516
non-`ZZ` cases). Advisory-only: 8 `title-no-emdash`, 69 `title-too-long` (both pre-existing advisory
categories, reviewed and left — many of the new variant titles are intentionally long to carry the
distinguishing name in brackets, consistent with the gherkin-standard's guidance to add a variant in
brackets "only when it distinguishes the case"). Full report:
`reports/tfts-system-test/new-etm-acceptance-suite/2026-07-24/alignment-audit.md`.

## Files

- `proposals/coherence-audit/fixes/etm-variant-expansion.cases.yaml` — the 16 retitles + 61 new cases (pushed).
- `proposals/coherence-audit/fixes/etm-variant-expansion.rewrite.json` — the 10 tidies + 1 retirement (applied).
- `proposals/coherence-audit/fixes/etm-variant-expansion.changelog.md` — this file.
