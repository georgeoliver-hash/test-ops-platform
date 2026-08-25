# HHD card/credential-variant sweep — 2026-07-23

Suite **30285** (`**NEW** HHD Test Suite`, project 42). A narrow, targeted follow-up to today's earlier
`hhd-consolidation-completeness.changelog.md` pass, modelled on a real miss just found in the **PV**
suite: `C4100998` folded 13 old-suite card-scheme cases (Visa/Mastercard × Debit/Credit, Maestro) into
one case that only said "Visa, Mastercard, mobile wallet" — silently dropping the Debit/Credit
distinction and Maestro entirely (`pv-consolidation-completeness.changelog.md` signed this off as
"correctly folded", which was wrong). George's directive: **"anywhere with smartcard, EMV tapping on
any device... we should stick with all the validations we do with different cards, types etc... each
variant being tested to ensure we cover all scenarios of card types... this should be gospel to any
device."** This pass hunts the identical pattern on HHD specifically.

## Method

1. Re-checked the 8 cases fixed by the earlier consolidation-completeness pass (C4103820, C4103822,
   C4103826, C4103840, C4103879, C4103875, C4103876, C4103971) against `Smartcard Use Matrix.xlsx` for
   *completeness*, not just presence. **No new discrepancy found with confidence** — see caveat below
   (the flattened `.xlsx.txt` extract used for this pass doesn't reliably preserve the original merged
   column boundaries, so this re-check couldn't independently re-derive the HHD Glider/NIR columns
   without risking a wrong read; no changes made to these 8 cases this session).
2. Pulled all 4 old HHD suites (5446, 13958, 5608, 5505) and the live suite (30285) fresh, full-body,
   via `TestRailClient.get_cases(42, <id>)` — dumped to local JSON for offline title/body search
   (avoided repeated live calls).
3. Regex-swept all 4 old suites' titles for `visa|mastercard|maestro|amex|american express|diners|
   debit|credit` (40 hits in 5446, 8 in 13958, 0 in 5608, 1 in 5505) and grouped by family.
4. For each family, read the live suite's corresponding case body (`custom_preface`/`custom_preconds`/
   `custom_steps_seperated`/`custom_expected`) to check whether the fold carries an explicit
   `Data variations:` line naming every distinct scheme/type the old suite tested, or only the one
   scheme named in its own title.
5. Fixed every under-enumerated case found (6), citing the old cases' own REQ ids as the ground.
6. Pushed via `tools/apply_rewrite.py --commit` (dry-run first).
7. Re-ran `python -m system_test_ops audit --suite 30285` — confirmed still CLEAN.

## Families checked

| Family | Old-suite basis | Verdict |
|---|---|---|
| **M020 Chip-and-PIN card payment** | 5 old cases (`C1692496` Visa Credit, `C1694407` Visa Debit, `C1694409` Mastercard Credit, `C1694408` Mastercard Debit, `C1694410` Maestro), 5446 + 13958 | **Gap found and fixed.** `C4103804`/`C4103805` each named only one scheme, no enumeration of the other 3. |
| **M020 Contactless card payment** | 2 old cases (`C1692498` Visa, `C1694412` Mastercard), 5446 + 13958 | **Gap found and fixed.** `C4103806` named only Visa; Mastercard contactless wasn't named anywhere (only the genuinely-distinct mobile-wallet case, `C4103807`, existed alongside it). |
| **M020 card-payment declines — unsupported scheme** | `C1694411` "Diners Declined" (REQ-0890.0), 5446 + 13958 | **Gap found and fixed.** The generic `Card Declined` family (`C4103808/09/10`) covers provider-declined/expired/blocked but never named the distinct "unsupported scheme, declined before a PIN prompt" reason. |
| **M020 On-Charge card-payment variants** | 7 old cases (5 chip-and-PIN schemes + 2 contactless, all "...- Payment Device On Charge"), 5446 | **No gap** — `C4103817` tests the on-charge *device state*, which is orthogonal to card scheme (equivalence partition per `docs/test-practices.md` rubric step 2); no scheme enumeration needed here, same as the Cancel-EMV/EMV-Unavailable cases. |
| **Revenue Inspection (cEMV/RID) — valid card inspection** | 5 old cases (`C3498105-109`: Visa Debit/Credit, MasterCard Credit/Debit, Maestro), "ABT — Valid Card Inspection", 5446 | **Gap found and fixed.** `C4103980` named no scheme at all ("a valid contactless EMV card"). |
| **Revenue Inspection (cEMV/RID) — unsupported-scheme decline (event 5012)** | 2 old cases (`C3498112` American Express, `C3498113` Diners), "ABT — Invalid Card Inspection", 5446 | **Gap found and fixed.** `C4103984` already said "a scheme other than Visa, Mastercard or Maestro" (correct as a boundary description) but named no worked examples. |
| **cEMV Validation (NIR Rail boarding + Capped Travel)** | 16 old cases across 2 duplicate sections (`C2766456-496`), 5446 | **New behavioural gap, logged not fixed** — see gap-register Q66. This is a distinct scenario (NIR passenger boarding via bank card, with fare-capping on repeat taps), not a scheme-enumeration issue, so out of scope for this targeted pass; the live suite has **zero** cEMV-capping coverage. |
| **8 already-fixed smartcard/product-family cases (C4103820/22/26/40/79/75/76/71)** | earlier session's fix batch | **Re-checked, no new discrepancy found with confidence** — see the Smartcard Use Matrix column-ambiguity caveat above. No changes. |

## Fixes applied

Six cases updated with `Data variations:` lines + Refs (via
`proposals/coherence-audit/fixes/hhd-card-variant-sweep.rewrite.json`,
`tools/apply_rewrite.py --commit`):

- **C4103804** "Chip and PIN — a Visa credit sale completes and prints a ticket" — added
  `Data variations: Visa Debit, Mastercard Credit, Mastercard Debit, Maestro`.
- **C4103805** "Chip and PIN — a Mastercard debit sale completes" — added
  `Data variations: Visa Credit, Visa Debit, Mastercard Credit, Maestro`.
- **C4103806** "Contactless — a Visa contactless sale completes" — added `Data variations: Mastercard`.
- **C4103808** "Card Declined — a declined card does not issue a ticket" — added a `Data variations:`
  line for the unsupported-scheme decline reason (e.g. Diners), citing REQ-0890.0.
- **C4103980** "Revenue Inspection — a valid card inspection succeeds and emits event 5008" — added
  `Data variations: Visa Debit, Visa Credit, Mastercard Credit, Mastercard Debit, Maestro`.
- **C4103984** "Revenue Inspection — an unsupported scheme is declined and emits event 5012" — added
  worked examples (`Data variations: e.g. American Express, Diners`).

**Gap register:** `proposals/coherence-audit/gap-register.md`, new session "Session 2026-07-23 — HHD
card/credential-variant sweep" — Q66 (open: NIR-Rail cEMV boarding + Capped Travel, no live coverage
found).

## Files

- `proposals/coherence-audit/fixes/hhd-card-variant-sweep.rewrite.json` — 6 case updates, applied via
  `tools/apply_rewrite.py --commit`.
- `proposals/coherence-audit/gap-register.md` — Q66 appended.
- Report: `reports/tfts-system-test/new-hhd-test-suite/2026-07-23/alignment-audit.md` (post-commit
  re-audit).

## Audit result

```
audited 210 cases: CLEAN; 43 advisory.
```

0 blocking findings after the commit (same 210-case/43-advisory-title baseline as the earlier
consolidation-completeness pass today — this pass only changed `custom_expected`/`refs` text on 6
existing cases, no titles/counts changed).
