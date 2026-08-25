# POS card/credential-variant sweep — suite 30253, 2026-07-23

**Question this pass answers:** does suite 30253 silently drop a distinct card scheme, smartcard
product/entitlement sub-type, or credential-variant dimension the same way the PV suite dropped
Visa/Mastercard Debit/Credit and Maestro into one generic "Visa, Mastercard, mobile wallet" line?
This is a narrower, targeted follow-up to `pos-consolidation-completeness.changelog.md` (2026-07-23),
specifically hunting the "mechanically-identical old cases differing only by card/product name in the
title" signature.

**Method.** Pulled old suite 9317 (2193 cases) and new suite 30253 (628 cases) live via
`TestRailClient.get_cases`/`get_case`, raw full-body. Searched every card/credential dimension named
in the brief: payment card schemes (Visa/Mastercard/Maestro/Amex/Diners, debit vs credit), smartcard
product/entitlement types, ITSO, mobile wallet, plus a systematic near-duplicate-title sweep across
every `<X> Smartcard`/`<X> Smartpass`/`<X> Pass` old-suite title to catch families not already named
in the brief. Cross-checked candidate families against `FBD-100250` (Smart Card Format for Translink
Preprinted Cards) and `Translink Smartcard Classification.xlsx` (an authoritative product/config
sheet) to confirm distinctness before treating anything as a gap.

## Families checked

### 1. Payment card schemes (Visa/Mastercard/Maestro, debit vs credit) — confirmed NOT a POS gap
Searched old suite 9317 full body (title + preface + preconditions + steps) for `visa`, `mastercard`,
`maestro`, `amex`, `diners`, `debit`, `credit card`, `mobile wallet`, `apple pay`, `google pay`. The
**only** hit across all four scheme names is **C4073808** "Card is from an invalid scheme" — and that
case's own `custom_devtypes: [10]` (PV, not POS/`5`) and preface ("To Ensure the PV rejects a non
valid cEMV Card") show it is a **Glider PV cEMV case that lives in the same TestRail project as
suite 9317, not a POS case** — it belongs to the PV cEMV validation area (the same FBD-100651 §201
family the PV audit already fixed), not to POS scope at all.

Every POS "Card Payment" case (285 old-suite titles checked, e.g. C2754927 `UB Adult Single - Issue -
Card payment`) uses generic `"Bank Card"` / `"Contactless card"` steps with **no scheme differentiation
anywhere** — old suite included. Checked the POS-relevant spec library (`FBD-100183 POS Hardware
Specification`, `FBD-100320 TID Management — Embedded & Non-Embedded Payment Devices`) for
Visa/Mastercard/Maestro/debit/credit/scheme terms: **zero matches in either document.** POS bank-card
payment is processed through a payment terminal (PED/acquirer) that abstracts the scheme from the
device's own test surface — unlike PV, which validates the BIN/scheme itself on-device per
FBD-100651. This is a genuine architectural difference, not an oversight: **there is no POS-suite
gap to fix here** because the old suite itself never tested scheme as a POS dimension. (New suite's
`Card Payment — declined, cancelled or error` family, already reviewed in the prior pass, correctly
enumerates the 5 decline/error *reasons* it does test.)

### 2. ITSO — not applicable
Zero hits for `itso` anywhere in old suite 9317 (title, preface, preconditions, or steps). Translink
uses its own DESFire/ABT smartcard scheme, not ITSO. Nothing to check.

### 3. Mobile wallet (Apple Pay / Google Pay) — not applicable
Zero hits for `wallet`, `apple pay`, `google pay`, or `phone` in any old-suite title. Never a tested
POS dimension in the old suite; nothing dropped.

### 4. Smartcard entitlement/product types — systematic near-duplicate sweep — **1 genuine gap found and fixed**
Grouped every `<X> Smartcard`/`<X> Smartpass`/`<X> Pass` old-suite title (69 distinct title groups).
Confirmed families already fully enumerated by the prior pass (Half Fare NDL/LD/PIPS/DLA/Partially
Sighted in **C4100413**; the 8-product Issue Card catalogue in **C4100031**/**C4100024**; Faulty
Smartpass/Fare-Paying/Dependants receipts) — no re-work needed there.

**Genuine gap: Concession Smartpass sub-types (Senior / 60+ / ROI Senior / Blind / War Pensioner) —
5 distinct old-suite cases, mechanically identical, folded into a generic case with no enumeration.**
- Old suite: `60 + Concession Smartcard` (C4072931/4056131/4057112), `Blind Concession Smartcard`
  (C4072932/4056143/4057113), `ROI Senior Concession Smartcard` (C4072933/4056144/4057114), `Senior
  Concession Smartcard` (C4072934/4056145/4057115), `War Pensioner Concession Smartcard`
  (C4072935/4056146/4057116) — same preface/preconditions/steps across all 5, differing only in card
  name (exactly the PV-scheme signature).
- Spec confirms distinctness: `FBD-100250` §revision history explicitly separates "Added 60+
  Smartpass" (para 263), "Added ROI Senior Smartpass" (para 280), "Added Blind pass" (para 298), and
  lists `Senior SmartPass / War Pensioner / ROI Senior SmartPass / 60+ Smartpass` as distinct products
  with genuinely different eligibility-date rules (paras 840–846, 9040–9110: Senior = 65th birthday,
  ROI Senior = 66th birthday, 60+ = 60th birthday, War Pensioner/Blind = card-issue date — a real
  behavioural difference, not just a label). `Translink Smartcard Classification.xlsx` sheet "Senior,
  Blind, WP.60+ & ROI" independently confirms the same 5-way product list.
- New suite: the dedicated `Smartcard — Concession` case (**C4100417**) was **`ZZ_DELETE_REVIEW`'d
  and folded** into the mega-consolidated **`Validation — entitlement smartcard sets the ticket type`
  (C4100427)**, whose preface only said `"(Senior/Blind/War Pensioner/yLink/24+/Half-Fare/
  Dependants)"` — 3 of the 5 concession sub-types named generically, **60+ and ROI Senior entirely
  absent**, and no `Data variations:` line at all for the concession family (unlike the sibling
  Half-Fare case, which got one in the earlier fix).
- **Same case also had its own incomplete Half-Fare sub-type list**, independent of the already-fixed
  `C4100413`: `"Half-Fare sub-types: Partially Sighted, Learning Disability, No Driving Licence,
  DLA"` — **missing PIPS**, confirmed a real Funded Pass category by `FBD-100250` para 206 ("Added
  PIPS as a new Funded Passes") and by the Classification sheet's "Half Fare & yLink" tab. This is
  the exact "did the Half-Fare fix miss a second location" check the brief asked for — it had.

**Fix applied** to **C4100427** only (via `pos-card-variant.rewrite.json`, `apply_rewrite.py`,
dry-run then `--commit`):
- Preface: added `PIPS` to the Half-Fare sub-type list (now `Partially Sighted, Learning Disability,
  No Driving Licence, PIPS, DLA`).
- Step "a Half-Fare sub-type or DLA card is presented" list: same PIPS addition, for consistency with
  the preface.
- Expected-result: appended `"Data variations: Concession — Senior / 60+ / ROI Senior / Blind / War
  Pensioner Smartpass categories."` — mirrors the exact phrasing pattern used for the Half-Fare fix
  in `C4100413`.
- Refs unchanged (`FBD-100250` already cited, correctly).

### 5. Faulty smartcard state families (Hotlisted / Expired / Invalid) — out of scope, already covered
These are card-*state* dimensions (not scheme/product-type), already asserted separately:
`Validation — hotlisted card` (C4100020), plus dedicated `Screen Validation — Hotlisted Error` /
several `…Expired` screen-validation cases. Not the pattern this sweep targets; confirmed present,
no action taken.

## Verification

`python -m system_test_ops audit --suite 30253` after commit: **CLEAN of blocking findings** — 528
cases audited, 0 blocking across every rule, 43 advisory (6 title-no-emdash, 37 title-too-long) —
identical to the pre-change baseline, so the fix introduced no new advisory findings either.

## Result

**4 dimensions checked** (payment card schemes, ITSO, mobile wallet, smartcard
entitlement/product-type near-duplicate sweep). **1 genuine gap found and fixed**: Concession
Smartpass sub-types (Senior/60+/ROI Senior/Blind/War Pensioner) named nowhere in the consolidated
entitlement case, plus a second, independent instance of the Half-Fare PIPS omission inside the same
case. **Payment card scheme (Visa/Mastercard/Maestro/debit-credit) confirmed NOT a POS gap** — the
one scheme-naming case found in the old suite belongs to PV (`custom_devtypes: [10]`), and POS's own
card-payment spec/old-suite content never differentiates by scheme (payment-terminal abstraction, a
real architectural difference from PV's on-device cEMV scheme check, not an oversight). ITSO and
mobile wallet are not POS-tested dimensions at all — nothing to drop. Audit result: **CLEAN**, no
regressions introduced.
