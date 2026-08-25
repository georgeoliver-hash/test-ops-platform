# HHD variant expansion — 2026-07-24

Suite **30285** (`**NEW** HHD Test Suite`, project 42). Applies George's 2026-07-24 rule
(`docs/gherkin-standard.md`, `docs/test-practices.md`, both search "2026-07-24"): **"no test should
tell someone to test multiple variants... we should have a test for each."** Every case carrying a
`Data variations:` line is expanded into one separate, individually-executable case per named
variant — retiring the "Data variations line" pattern used by yesterday's (2026-07-23) card-variant
sweep and consolidation-completeness passes, which this session's rule change now supersedes.
Genuine **operating-mode** coverage (NIR-Rail / Glider) is unaffected — that stays on TestRail
**Configurations**, not split into cases.

## Method

1. Pulled suite 30285 fully via `TestRailClient.get_cases(42, 30285)` (full body: preface, preconds,
   steps, expected) — 213 live cases (216 total incl. 3 pre-existing `ZZ_DELETE_REVIEW`).
2. Swept every case's full body (preface + preconds + steps + expected) for `Data variation`
   case-insensitively — **43 cases matched** (not the ~14 named in the task brief; the brief's
   6+8 cases were a subset of a larger set built up across three earlier sessions: 2026-07-22
   consolidation-completeness [8 cases], 2026-07-23 card-variant sweep [6 cases], plus 29 more
   cases from the original suite build that already carried a `Data variations:` line for
   passenger type / payment method / ticket format, never previously flagged for splitting because
   the rule didn't exist yet).
3. For each of the 43, read the full case body and enumerated every named variant across every
   listed dimension (card scheme, smartcard/entitlement/product type, payment method, passenger
   type, ticket format/layout number) — **excluding** the `mode {NIR-Rail, Glider}` dimension, which
   stays a Configuration per the rule's explicit carve-out.
4. **Expansion model: one new case per named item, not a Cartesian product across dimensions**
   (e.g. a case with `product {A,B,C}; passenger {Adult,Child}` gets one case per product and one
   per passenger — not 6 combinations). This mirrors the shape of the existing 2026-07-23
   card-variant-sweep cases (each new case swaps one variable) and keeps growth linear rather than
   combinatorial, while still giving every named variant its own trackable pass/fail.
5. **Deduped across sibling cases already testing part of a variant set** — e.g. the Chip-and-PIN
   family already had two live primaries (C4103804 Visa Credit, C4103805 Mastercard Debit); only
   the 3 remaining schemes (Visa Debit, Mastercard Credit, Maestro) needed new cases, not 5.
   Same logic applied to the Metro/Ulsterbus product families (C4103875/C4103876).
6. **First/primary variant reuses the original case id, retitled/re-worded** to name the specific
   variant it actually tests (e.g. C4103980 renamed to name Visa Debit; C4103856 clarified as
   Student Monthly/Adult); remaining variants became new cases in the same section, grounded in the
   primary case's own Given/When/Then shape with only the variant name substituted (no invented
   mechanics — every new case reuses the existing, already-cited Refs and worked-example pattern).
7. Pushed the 125 new cases via `system_test_ops push --file
   proposals/coherence-audit/fixes/hhd-variant-expansion.cases.yaml` (dry-run, then `--commit`).
8. Applied the 43 primary-case edits (retitle/reword, strip the retired `Data variations:` text) via
   `tools/apply_rewrite.py proposals/coherence-audit/fixes/hhd-variant-expansion.rewrite.json`
   (dry-run, then `--commit`). A first commit pass missed the fact that on 15 cases the
   `Data variations:` line lived inside the step's `expected` text (not `custom_expected`) — caught
   by a full re-sweep after the first commit, fixed with a second, targeted rewrite file
   (`hhd-variant-expansion-steps-fix.rewrite.json`, dry-run then `--commit`).
9. Re-swept the whole suite for `Data variation` — **0 hits remain**.
10. Re-ran `python -m system_test_ops audit --suite 30285` — **CLEAN**.

## Families expanded (43 source cases -> 125 new cases)

| Family | Section | Source cases | New cases |
|---|---|---|---|
| Card Payment (M020) — chip-and-PIN / contactless / declines | Card Payment (M020) | C4103804/05/06/08 | 5 |
| Smartcard Validation — iLink/aLink/yLink/EA/Metro-Ulsterbus products; Senior Smartpass concessions; Staff Pass | Smartcards & ABT | C4103820/22/26 | 24 |
| Annulment — 24+ Discount | Annulment & Reversal | C4103840 | 1 |
| Ticket Issue — payment method, stage-selection method, advance-date passenger, period product, Bus Rambler, 3 Day Select | Sales - Paper Tickets / Ticket Issue | C4103847/48/49/51/55/56/57/58 | 14 |
| Cross-Border — Euro cash/warrant | Sales - Paper Tickets / Cross-Border Tickets | C4103871/72 | 4 |
| Metro & Ulsterbus Products — product + passenger | Sales - Paper Tickets / Metro & Ulsterbus Products | C4103875/76 | 13 |
| Top-Ups — product, passenger, payment, amount-selection, expiry-reactivation, mini-statement | Top-Ups | C4103879/80/82/83/91 | 15 |
| Penalty Fares — invalid-smartcard passenger types, issuing role | Penalty Warning & Fares | C4103896/97 | 6 |
| Sign On & Session — Inspection/Validation Mode break-resume | Sign On & Session | C4103913/19 | 2 |
| Ticket Formats — NIR Layouts, Glider Formats (travel, concession, top-up receipt, annul/cancel) | Ticket Formats & Waybill | C4103939/41/42/43 | 24 |
| Smartcard Inspection — concession/half-fare/staff/EA/yLink families | Smartcard Inspection | C4103971 | 12 |
| Revenue Inspection (cEMV/RID) — card scheme success, unsupported-scheme decline | Revenue Inspection (cEMV/RID) | C4103980/84 | 5 |
| **Total** | | **43 source cases** | **125 new cases** |

Mode-only `Data variations` wording (no case split — Configurations already the correct model, per
the rule's explicit carve-out) was still cleaned of the retired phrase on: C4103893, C4103895,
C4103907, C4103908 (mode-only penalty/sign-on cases).

## Deliberate non-split exception (documented, not silent)

**C4103947, C4103949, C4103950** (Waybill — Operator Waybill / annulment lines / validation-
inspection-barcode activity) carried a `Data variations` list of transaction/activity types but were
**NOT split**. Judgement call: these three cases test the waybill's *reconciliation across a mixed
duty* — the risk they cover (a transaction type silently missing from a combined waybill) is only
exercised by testing several types *together* in one duty; splitting into one-type-per-case tests
would be *weaker* coverage, not stronger, since it would stop testing whether the waybill correctly
aggregates a mix. This is different in kind from a card scheme/product/format, which fails
independently at the point of use. Their `custom_expected` was still reworded to drop the retired
"Data variations" phrasing (now plain prose naming what the one worked example covers). Flagged here
for George's review in case he disagrees with the distinction.

## Files

- `proposals/coherence-audit/fixes/hhd-variant-expansion.cases.yaml` — 125 new cases, applied via
  `system_test_ops push --commit`.
- `proposals/coherence-audit/fixes/hhd-variant-expansion.rewrite.json` — 43 primary-case
  retitles/rewordings, applied via `tools/apply_rewrite.py --commit`.
- `proposals/coherence-audit/fixes/hhd-variant-expansion-steps-fix.rewrite.json` — a 15-case
  follow-up fix for `Data variations` text that lived in a step's `expected` field rather than
  `custom_expected` (missed by the first rewrite pass, caught by the post-commit re-sweep), applied
  via `tools/apply_rewrite.py --commit`.
- Report: `reports/tfts-system-test/new-hhd-test-suite/2026-07-24/alignment-audit.md` (post-commit
  re-audit).

## Before / after

- Before: 213 live cases (216 total incl. 3 `ZZ_DELETE_REVIEW`).
- After: 335 live cases (338 total incl. 3 `ZZ_DELETE_REVIEW`) = 213 + 125 new - 3 pre-existing
  condemned (unchanged, excluded from the live count both times).

## Audit result

```
audited 335 cases: CLEAN; 102 advisory. 0 blocking.
```

The 102 advisory `title-too-long` findings (up from 43 pre-existing) are expected: many new cases
carry a bracketed variant qualifier in the title (e.g. "(Adult)", "(cEMV card payment)", "Glider
Format 13A") for traceability, per the standard's advisory-only title-length rule — reviewed and
intentional, same treatment as the existing Screen Validation titles.

Old HHD suites (5446, 13958, 5608, 5505) were not touched — read-only per the repo's hard rule.
