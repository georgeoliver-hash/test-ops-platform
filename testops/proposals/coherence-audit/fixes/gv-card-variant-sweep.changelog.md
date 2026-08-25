# GV suite (30286) — card/credential-variant completeness sweep, 2026-07-23

**Question asked:** a narrower, targeted re-check, modeled on a real miss just found in the PV suite
(13 old-suite card-SCHEME cases — Visa Debit/Credit, Mastercard Debit/Credit, Maestro — folded into
one new case that only named "Visa, Mastercard, mobile wallet" generically, silently dropping the
Debit/Credit distinction and Maestro entirely). George's directive: anywhere the device does
smartcard/EMV tapping, every card type/variant historically tested must still be named explicitly
somewhere in the new suite — "gospel to any device." This pass checks whether GV's consolidation made
the same mistake. It is narrower than today's earlier `gv-consolidation-completeness.changelog.md`
pass, which covered the whole suite's completeness; this one re-opens specifically the card/barcode/
EMV dimension with the PV finding as the search template.

## Method

1. Pulled old suite 14973 fresh in full (`python -m system_test_ops cases --suite 14973 --project 42`
   → 1,184 cases) and new suite 30286 fresh in full (98 cases).
2. Searched the old suite for every card/credential dimension the GV validates: bank-card scheme
   (Visa/Mastercard/Maestro, Debit/Credit), multi-use barcode products, EMV/cEMV decline reasons,
   mobile wallet. Confirmed via title grep across all 1,184 titles — no Amex/Diners/Apple Pay/Google
   Pay/mobile-wallet case exists anywhere in the GV old suite (unlike the PV suite, GV's old suite
   never tested those).
3. For each family found, pulled the **full raw case body** (`TestRailClient.get_case`, not the CLI's
   `cases.md`/`cases.json` — see tooling note below) for the corresponding live case(s) and checked
   whether every distinct old-suite variant is named explicitly in the new case's Expected result as
   a `Data variations` line.

## Tooling note (methodology-affecting, found this session)

`system_test_ops/coverage/normalise.py`'s `_extract_steps()` looks for a `custom_steps_separated` key,
but this TestRail template's real field is `custom_steps_seperated` (TestRail's own field-name typo).
Because of the mismatch, `cases.md`/`cases.json` for this suite/template silently fall through to a
worse fallback (the first `custom_` field containing "given/when/then" — usually just
`custom_preconds`) and **never surface `custom_expected`**, where this suite's Data-variations lines
actually live. A grep over `cases.md` for "Visa/Mastercard/Maestro" therefore initially looked like a
gap (only 1 of the expected hits showed up) until the case bodies were re-pulled directly via
`TestRailClient.get_case`, which returns every `custom_*` field including `custom_expected`. This is a
CLI-extraction gap, not a suite-content gap — flagging it here since it would produce the same false
"looks empty" signal for any future audit of this suite that trusts `cases.md` alone for this
template. Not fixed this session (out of scope for a content-only sweep); worth a follow-up ticket
against `system_test_ops/coverage/normalise.py`.

## Finding: the GV bank-card-scheme family — checked, NOT the same miss as PV

**Old suite:** exactly one card-scheme family, cloned across the 4 gate-mode sections (Entry / Exit /
Entry-Exit A→B / Entry-Exit B→A) — `Employee Smartcards / ABT / Visa` and `/ Mastercard`:
`C3272431` Visa Debit, `C3272432` Visa Credit, `C3272433` Mastercard Debit, `C3272434` Mastercard
Credit, `C3272435` Maestro Debit (×4 modes = 20 cases total). All 5 have mechanically identical bodies
— "present the card → Validation Success screen, gate opens" — differing only by card sample, exactly
the PV pattern's shape.

**Live suite:** `C4104011` ("ABT Tap — a valid contactless card tap succeeds and the gate opens",
section `Functional / ABT cEMV Taps`) already carries the full accepted-scheme enumeration in its
Expected result: *"Data variations, card scheme, Visa Debit / Visa Credit / Mastercard Debit /
Mastercard Credit."* All 4 accepted variants from the old suite are named explicitly, not silently
folded into a vague "Visa, Mastercard" — the direction-clone dimension (Entry/Exit/A→B/B→A) is
correctly handled by TestRail Run Configurations rather than 4 copies, per the standard.

**Maestro — genuinely NOT a silent drop, verified against the spec directly.** `C4104024` ("ABT Tap —
a Maestro card is not accepted at the GV") asserts Maestro is **declined**, which at first read looks
like a contradiction with the old suite's `C3272435` (Maestro Debit **accepted**, Validation Success,
gate opens). Resolved by reading FBD-100690 (NIR Tap On Tap Off Specification v4.00) directly — it
has **two separate paragraphs**, one for each device:
- PV (para ~749): "valid scheme (i.e. Visa/Mastercard **including Maestro**)"
- GV (para ~940): "valid scheme (i.e. Visa/Mastercard)" — Maestro not listed.

So the spec itself draws a **device-specific** line: Maestro is a valid scheme on the PV but not on
the GV. The old suite's `C3272435` (Maestro accepted on GV) was wrong per this spec text; the new
suite's `C4104024` is correctly grounded — its preface even states the device-specific reasoning
explicitly ("Maestro is accepted on the PV, not the GV"), citing FBD-100690. This was already
identified in yesterday's `gv-deep-audit.changelog.md` (para 940-943 citation, matches C4104024).
**No fix needed — the new suite is right, the old suite (or an older spec revision) was wrong, and
this is the correct outcome of consolidation catching an error, not causing one.**

## Fuller sweep — no other card/credential family in scope

- **Multi-use barcode products** (`C4104028`): spot-checked directly, Expected result carries *"Data
  variations, product, Adult / Child / 3-Day Select / 1-3 Off Day Return / 24+ / Ylink / Concession /
  Half Fare / Day Tracker / Unemployed Day Return"* — every old-suite product named. Confirms today's
  earlier consolidation-completeness pass's claim, independently re-verified via raw case body (not
  `cases.md`, per the tooling note above).
- **EMV/cEMV decline reasons** (`C4104014`-`C4104017`, `C4104018` roll-up): Reason 1/2/3/15/20 all
  named, confirmed present in raw `custom_expected` bodies.
- **Smartcard product acceptance** (iLink/Belfast Visitor/Employee-Staff/Rail-EA/etc.): out of scope
  for this sweep — already correctly identified (in `gv-consolidation-completeness.changelog.md`) as
  held-back `pending-integration` scaffolding, not a live consolidation, so "did the fold silently
  drop a variant" doesn't apply — nothing has been folded there yet.
- **Mobile wallet / Amex / Diners**: zero hits anywhere in the GV old suite's 1,184 titles — this
  dimension simply doesn't exist for GV (unlike PV, which does test Apple Pay/Apple Pay Express).
  Nothing to preserve, nothing dropped.

## Result

**No suite changes made this session.** The GV suite does not repeat the PV-suite miss: the bank-card-
scheme family and the barcode-product family both already carry explicit, complete `Data variations`
lines, and the one apparent discrepancy (Maestro) is a correctly-grounded, device-specific spec
distinction rather than a dropped variant.

`python -m system_test_ops audit --suite 30286`: **CLEAN** — 97 live cases, 0 blocking findings, 38
pre-existing title-length advisories (unchanged).

## Files
- This file (new).
- No `.cases.yaml` / rewrite was produced — no push was needed.
- `reports/tfts-system-test/aa-gate-validator-acceptance-test/2026-07-23/cases.json` /`.md` (fresh
  pull, old suite 14973, read-only).
- `reports/tfts-system-test/new-gv-test-suite/2026-07-23/cases.json` / `.md` / `alignment-audit.md`
  (fresh pull + re-audit, new suite 30286).
