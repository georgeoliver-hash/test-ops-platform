# PV Acceptance Suite (30255) — card/product variant enumeration sweep

Date: 2026-07-23. Mandate (George): "anywhere with smartcard, EMV tapping on any device... we
should stick with all the validations we do with different cards, types etc... each variant being
tested to ensure we cover all scenarios of card types... this should be gospel to any device." A
prior session today fixed two specific cases (`C4100998` ABT contactless tap, `C4101088` cEMV
decline reasons) for missing card-scheme enumeration. This session sweeps **everything else** for
the same pattern: smartcard product/entitlement families, barcode product types, and any other
credential dimension (mobile wallet, ITSO).

## Method

1. Verified the prior fix is still live and the suite is still clean before starting (below).
2. Pulled old suite `10047` fresh in full (1,144 cases) and new suite `30255` fresh in full (136
   cases), plus raw case bodies for both via `TestRailClient.get_cases` (title, refs,
   `custom_preface`, `custom_preconds`, `custom_steps_seperated`, `custom_expected`).
3. **Smartcard product families**: cross-tabbed every `Glider/Smartcard Validation/...` and
   `Rail/Smartcard Validation/...` old-suite section title (the ~800-case product × Adult/Child ×
   Valid/Invalid × Glider/Rail matrix) against the 11 consolidated `Functional / Smartcard
   Validation` cases' live `custom_expected` "Variation —" lines in the new suite.
4. **Barcode types**: cross-tabbed the old suite's `Functional / Multi-Use Barcodes / TVM Produced`
   and `/ HHD Produced` sections (9-10 per-product-type cases each) against the new suite's
   consolidated `Barcode — multi-use validation` case, and confirmed single-use vs multi-use is
   still correctly split (per the 2026-07-17 finding already resolved — `C4103559`
   rejects single-use, `C4101005` is `ZZ_DELETE_REVIEW`).
5. **Other credential dimensions**: swept old-suite titles for `ITSO|MIFARE|DESFire|mobile
   wallet|Apple Pay|Google Pay`, cross-checked against the new suite's `Card technology — MIFARE
   and DESFire` (`C4101008`), `FEIG — card reading` (`C4101081`), `Legacy Smartcard` (`C4101007`),
   and `Smartcard — inter-device top-up then validate on PV` (`C4101090`) cases.
6. Re-ran `python -m system_test_ops audit --suite 30255` after committing.

## Findings

### 1. Smartcard product families — CLEAN, no gap

All 11 old-suite product families (Concession SmartPass: 60+/Blind/Senior/ROI Senior/War Pensioner;
Half-Fare: DLA/Learning Disability/No Driving Licence/PIPS/Partially Sighted; Metro Daylink; Metro
Multi-Journey: City/Inner/Extended zones; Metro Travelcard; Ulsterbus Multi-Journey; iLink: Zones
1-4/NW + Belfast Visitor Pass; aLink; yLink/24+; Translink Employee: Staff/Staff Partner/Retired/
External/Dependents; EA Smartpass: Pupil/FE, EA Bus + EA Rail) are already named verbatim as
Data-variations lines on the live consolidated cases (`C4100981`-`C4100991`) — this was already done
properly, most likely by the 2026-07-21/22 deep-audit and consolidation-completeness passes. No
product family is hidden behind a generic "a smartcard" line. **No fix needed.**

### 2. Barcode product types — GAP FOUND AND FIXED

The old suite tests each multi-use-barcode **product/fare type** as its own case, once per source
device: **Adult, Child, 3 Day Select, 1/3 Off Day Return, 24+, Ylink, Concession, Half Fare, Day
Tracker** — for both **TVM-produced** (`C4040353`-`C4040363`) and **HHD-produced**
(`C4040364`-`C4040375`, plus **Unemployed Day Return** which is HHD-only, `C4040373`) tickets — 19
old cases in total (plus their `Unsure (To Be Organised)` duplicates). Each is the identical
validate-and-decrement mechanic with a different product encoded (confirmed generic per FBD-100167
"Product Key": any product configured against the barcode-use Product ID validates the same way) —
correctly folded into one case, no new test needed (equivalence partitioning,
`docs/test-practices.md` rubric step 2).

**But** the consolidated case (`C4101006` "Barcode — multi-use validation") only carried
`Variation — HHD-produced and TVM-produced` — the actual product/fare-type enumeration was dropped
entirely. A separate beep-pattern step in the same case names a different, TIBU-27324-specific
product list (Student XB, PRV-A, PRV-C, etc., migrated from old-suite `C4091912`) which is a real
but distinct enumeration (audible feedback, not validate/reject) and doesn't substitute for naming
the old suite's own tested product set.

**Fix applied**: added the full product enumeration as its own clause in `custom_expected`:
`product types Adult, Child, 3 Day Select, 1/3 Off Day Return, 24+, Ylink, Concession, Half Fare, Day
Tracker (TVM + HHD), plus Unemployed Day Return (HHD only)`.

### 3. Other credential dimensions — one stale-field bug found and fixed (ITSO)

- **MIFARE/DESFire**: already correctly covered by `C4101008` ("Card technology — MIFARE and
  DESFire"), citing FBD-100250/100236/100690. No gap.
- **Mobile wallet**: already covered on `C4100998` (fixed earlier today, verified still present —
  see below).
- **ITSO**: the old suite has one case, `C4099852` "FEIG - ITSO Smartcard Tap". The 2026-07-21/22
  deep-audit already determined ITSO was a misnomer (Translink's own card-format spec, FBD-100236
  "Translink DESFire ABT Card Format Specification", never mentions ITSO — the real credential is
  DESFire EV3) and rewrote `C4101081`'s title/preface/preconditions/steps accordingly via
  `pv-deep-audit-batch2.rewrite.json`. **However that rewrite never included an `expected` field**,
  so the case's top-level `custom_expected` summary was left stale: it still read *"The FEIG reads
  **ITSO** smartcards..."* after the fix landed — the same stale-Expected-field bug independently
  found and fixed on `C4101085` in that same pass, missed here. Fixed to match the already-corrected
  body: *"The FEIG reads **DESFire** smartcards..."*. No behavioural change — this closes an
  inconsistent/uncorroborated credential name that had survived in the one field a summary view
  would show.

## Verification — the two already-fixed cases

Re-pulled live (not assumed) before and after this session's commit:

- **`C4100998`** "ABT — contactless tap validation": `custom_expected` still reads *"Data
  variations: Visa Debit, Visa Credit, Mastercard Debit, Mastercard Credit, Maestro, mobile wallet —
  test each distinctly, a failure can be scheme/BIN-range specific."* — unchanged, correct, untouched
  this session.
- **`C4101088`** "cEMV — decline reasons and route-type enablement": preconditions still read *"cards
  for each decline condition (card not read, unsupported scheme e.g. AMEX or Diners, expired, ODA
  fail, on BIN list, on Deny list, card clash...)"* — Diners is present, unchanged, correct, untouched
  this session. (Noted in passing, not fixed, as out of this sweep's scope: the case's one-line
  `custom_expected` summary says only "unsupported scheme (AMEX)" without repeating Diners, and
  separately still lists "Technician-Menu-disable" as a disable condition even though the
  2026-07-21/22 deep-audit confirmed no such Technician Menu toggle exists — both look like the same
  class of stale-summary-field drift as the ITSO fix above, but neither is a card/product
  *enumeration* gap, so left for a future coherence pass rather than fixed under this mandate.)

## Result

- **2 cases changed**: `C4101006` (barcode product-type enumeration added), `C4101081` (stale
  "ITSO" wording in `custom_expected` corrected to "DESFire").
- Applied via `tools/apply_rewrite.py proposals/coherence-audit/fixes/pv-card-variant-sweep.rewrite.json`
  (dry-run verified, then `--commit`).
- **Suite 30255 re-audited: CLEAN of blocking findings** (135 cases; 24 pre-existing advisory
  title-length/em-dash notices, unchanged; 0 new).
- **Old suite 10047: untouched** (read-only throughout).

## Files

- `proposals/coherence-audit/fixes/pv-card-variant-sweep.rewrite.json` — the 2-case rewrite applied.
- `proposals/coherence-audit/fixes/pv-card-variant-sweep.changelog.md` — this file.
- `proposals/coherence-audit/fixes/pv-suite-30255-raw.json`, `pv-suite-10047-old-raw.json` — full
  raw case dumps used for this session's cross-tab (superseded scratch dumps; not authoritative
  going forward).
