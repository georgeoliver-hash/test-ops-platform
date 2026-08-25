# Proposal: restructured Translink HHD suite

Goal: consolidate the old HHD suites (5446 AA-HHD-Acceptance · 13958 HHD Master · 5608 FAT HHD Glider ·
5505 R1.1-HHD) into a cleaner, **test-type-first** new suite **`**NEW** HHD Test Suite` (id 30285)** —
reuse the good old cases, dedupe the NIR×Glider double/triple tree, collapse the smartcard product
explosion, and fold the Fixes/Changes + TIBU regression by feature. **READ-ONLY / propose-first:** this is
the blueprint, not authoring. Evidence: `old-suite-audit.md` (this folder). Governing mindset:
`docs/test-practices.md`. House-style precedents: ETM, POS, TVM `structure.md`.

## Mode decision (the crux)
- **HHD runs in two operating modes: NIR (rail) · Glider (bus / Metro network).** Metro and Ulsterbus are
  **product sets within the bus/Glider mode**, not separate device trees. The task's four-mode taxonomy
  (NIR-Rail / Ulsterbus / Metro / Glider) maps to **Run Configurations**, not sections.
- `old-suite-audit.md` §4 proves the two modes share the large majority of behaviour (sign-on, card
  payment/M020, smartcards, top-ups, annulment/reversal, multi-use barcodes, inspection, penalty, formats,
  power/battery, comms). Divergence is confined to a small set of **proven areas** (below).
- **Decision (follows the ETM/TVM precedent):** structure is **feature/test-type-first**, and **mode
  (NIR/Glider incl. Metro/Ulsterbus product sets) is handled by TestRail Run Configurations** — shared
  behaviour authored **once**, executed against each configuration. Mode-first section trees would recreate
  the old suite's NIR||Glider duplication (the very thing we are collapsing) and split the shared core for
  no benefit (the POS lesson, recorded in `etm-suite-restructure/structure.md`).
- **Mode coverage lives in `mode-coverage.md`** (to build) — the shared / NIR-only / Glider-only map + the
  Run-Configuration spec. Explicit `… / NIR only` and `… / Glider only` leaves appear **only for the proven
  divergences:**
  1. **NIR only — Cross-Border tickets** (rail).
  2. **NIR only — Single-Use Barcodes (CR094)** — Glider HHD does not do single-use (FBD-100483).
  3. **NIR only — Card-payment reference-number station set** (Yorkgate/Antrim/Coleraine/…).
  4. **Glider only — Metro/Ulsterbus product family** (Multi-Journey / Daylink / Travelcard / Town Service).
  5. **Glider only — Old Barcode Redemption (BRS)**.
  6. **Glider only — cEMV Revenue Inspection** (Glider TOO live now; **NIR TOTO inspection is future scope**
     per FBD-100690 — tag `@future`, do not author full NIR inspection yet).

## Proposed section tree
```
**NEW** HHD Test Suite (30285)         ← Configurations: Mode{NIR-Rail · Glider(Metro/Ulsterbus)}
│
├─ SMOKE                                    @mode(all)   thin critical path (basis: FAT suite 5608)
│     sign on → sell paper ticket (cash + M020 card) → print → annul → sign off → waybill
│
├─ FUNCTIONAL
│   ├─ Sign On & Session                    Operator/Supervisor/Technician (ID+pwd, smartcard, duty no.),
│   │                                       Message/Word-&-Colour of the Day, topology, device-locked,
│   │                                       break-mode sign-on (CR78)
│   ├─ Sales — Paper Tickets                cash / warrant / cEMV card, basket, group, Bus Rambler,
│   │   │                                   visual paper-ticket inspection
│   │   ├─ Cross-Border Tickets  …/NIR only
│   │   └─ Metro/Ulsterbus products …/Glider only   Multi-Journey/Daylink/Travelcard/Town Service
│   ├─ Card Payment (Miura M020)            Bluetooth pairing, PRN (H+IMEI+ticks+op), TID/TK after pairing,
│   │   │                                   payment-does-not-complete, on-charge   [FBD-100320/100373]
│   │   └─ Reference-Number Stations …/NIR only
│   ├─ Smartcards & ABT                     validate representative products (iLink adult/child/NW, BVP,
│   │                                       aLink, yLink, 24+, EA pupil/further-ed bus&rail, concessionary
│   │                                       families, staff+dependants); expired / hotlisted / faulty
│   │                                       [FBD-100236/100250/100271]
│   ├─ Smartcard Top-Ups                    Multi-Journey/Period/Daylink/iLink/Travelcard/BVP; annul top-up
│   ├─ Smartcard Inspection                 visual/colour-change period-pass inspection (adult/child colour,
│   │                                       concession/half-fare/staff/EA/youth, invalid), CR78 break-mode
│   │                                       inspection + passback   [FBD-100651]
│   ├─ Single-Use Barcodes (CR094) …/NIR only   encryption-key lifecycle, AES/TripleDES, 17-comma decrypt,
│   │                                       200/400/500 + /logfailure, offline validation + 15-min sweep,
│   │                                       manual ref→ShortID, legacy stages, events 1412/1416
│   │                                       [FBD-100483 / 100317 / 100167]
│   ├─ Multi-Use Barcodes                   validate offline → Merit transaction; check order, zone/location,
│   │   │                                   partial validation, success/failure/partial screens, formats
│   │   └─ Old Barcode Redemption (BRS) …/Glider only
│   ├─ Revenue Inspection (cEMV / RID) …/Glider only   Inspector Mode → M020 tap → integrity (scheme/ODA/
│   │                                       expired → "Card Declined") → online validation → RID deny
│   │                                       ("Card on RID List") → success; events 5008-5013 + audio tones;
│   │                                       RID-list lifecycle (full/15-min delta/full-after-EoD/comms defer);
│   │                                       30-s timeout; cannot-annul   [FBD-100716; NIR TOTO @future 100690]
│   ├─ Annulment & Reversal                 annul ticket/top-up/discount (cash&card), reversal (EMV),
│   │                                       annul-unique-reference (PRN), nothing-to-annul; **NO refund
│   │                                       (assert negative)**   [FBD-100373 REQ-1630.0]
│   ├─ Penalty Warning & Fares              issue penalty warning + penalty fare
│   ├─ Ticket Formats & Receipts / Waybill  format catalogue incl. Format 16 annul/cancel; waybill w/ annuls
│   └─ Operator / Supervisor / Technician   operator menu (totals/mini-statement/favourites/break),
│                                           printer pairing, supervisor start-duty, technician TID/TK+pair+
│                                           version ticket + home location
│
├─ NON-FUNCTIONAL / RESILIENCE              @mode(all)
│   ├─ Power & Battery                      power recovery, power save, replace battery mid-shift, low-battery
│   ├─ Printer                              NIR/Glider printer, printer pairing / NFC, roll/errors
│   ├─ Comms / SaaS / Heartbeat             CloudFare connection loss, offline behaviour, 15-min staff-list
│   │                                       heartbeat   [FBD-100266 / 100359]
│   ├─ Network Settings                     device network config
│   ├─ Device Security / OS                 device lock, OS 8 upgrade
│   └─ Timings / Performance                validation/inspection/print timings
│
└─ REGRESSION
      NOT a parking lot. Fixes/Changes (71) + Fixes (35) + Barcodes TIBU (162) + Glider Multi-Use TIBU (50)
      + CR78 Regression (21) folded into the FUNCTIONAL case that owns the behaviour (linked via Refs, incl.
      TIBU-#####). Only defects with no natural functional home live here. See bug-regression-register.md
      (to build).
```

## Governing mindset
All add/edit/merge/fold/leave decisions follow `docs/test-practices.md` — risk-based, minimal sufficient
coverage, no duplication, one behaviour per case, traceability via Refs (REQ + TIBU). The NIR×Glider
shared-vs-mode cross-tab (`old-suite-audit.md` §4) is the mandatory precondition: the old suite already
proves the cost of guessing — it authored the whole tree twice (NIR||Glider) and a third time (HHD Master).
Author shared once; split only the six proven leaves.

## Suites
- **Source (old, read-only):** 5446 (primary), 13958 (dedup), 5608 (FAT — smoke template), 5505 (R1.1 —
  non-superseded detail only). Never modified or deleted from.
- **Target (new):** `**NEW** HHD Test Suite` (30285) — everything below is built here.

## Push defaults for this suite
```yaml
suite_id: 30285
defaults:
  template_id: 1
  custom_devtypes: [TBD]        # HHD — run discover-fields before authoring
  custom_revstatus: 2
  custom_autoconfirmation: false
```
(devtype id is a build step — confirm via `python -m system_test_ops discover-fields --project 42
--sample-case <hhd case id>` before the first push.)

## Estimated consolidated case count
Old **main scope ≈ 2,087** cases (5446 1,632 + 13958 455), or **2,280** including FAT (42) and R1.1 (151).
The count is inflated by four multipliers the new suite removes:
**(a)** the same behaviour authored **twice** (NIR || Glider trees) and a **third** time (HHD Master);
**(b)** smartcard **product explosion** (~100 "Validate <Product>" cases + per-product expired/hotlisted/
transfer/top-up/inspection leaves);
**(c)** ~340 **regression/defect** cases (Fixes/Changes 71 + Fixes 35 + Barcodes TIBU 162 + Glider Multi-Use
TIBU 50 + CR78 Regression 21) that fold into functional cases via Refs;
**(d)** ~46 **dead** cases (ABT-Invalid 37 + Delete 9) plus ~32 back-office (Merit/CloudFare) candidates to
exclude to a BOS suite.

| New area | Est. cases | How it collapses the old total |
|---|---:|---|
| Smoke | ~8 | one critical path (basis: FAT 5608) |
| Sign On & Session | ~15 | dedupe NIR/Glider/Master triple copy; + break-mode |
| Sales — Paper Tickets (+ NIR X-border / Glider products) | ~40 | parametrise; modes = Run Configs, not copies |
| Card Payment (M020) (+ NIR ref-number stations) | ~20 | one M020/PRN matrix; NIR station leaf |
| Smartcards & ABT | ~70 | representative products, not one case per Smartpass variant; both modes via config |
| Smartcard Top-Ups | ~25 | one top-up matrix, both modes |
| Smartcard Inspection | ~30 | one visual-inspection matrix (was NIR+Glider+CR78) |
| Single-Use Barcodes (CR094) …/NIR only | ~35 | consolidate CR094 state machine + Barcodes TIBU |
| Multi-Use Barcodes (+ Glider Old-BRS leaf) | ~30 | one section (was NIR + Glider + TIBU copies) |
| Revenue Inspection (cEMV/RID) …/Glider only | ~30 | consolidate RID/inspection + CR78; NIR TOTO @future |
| Annulment & Reversal (no refund) | ~20 | one matrix, both modes |
| Penalty Warning & Fares | ~8 | |
| Ticket Formats & Receipts / Waybill | ~25 | format catalogue, rail formats on NIR config |
| Operator / Supervisor / Technician | ~30 | dedupe NIR/Glider/Master triple copy |
| Non-Functional (power/battery, printer, comms, network, security/OS, timings) | ~40 | shared non-functional |
| Regression (un-homeable only) | ~15 | remainder of ~340 folded into functional via Refs |
| **Total** | **≈ 400–450 (~420)** | **~80% reduction vs the ~2,087 main-scope raw count (~82% vs 2,280 all-in)** |

## Old → new mapping
Per-area `<area>.cases.yaml` built into 30285 via `push` (idempotent, new-suite-only; auto-audit gates each
push). Old suites untouched; "leave" = simply not carried over. UI moves/bins done by George (this
instance's API can't move/re-parent/delete).

## Gated on (before authoring)
1. George's sign-off on this section tree and the **mode = Run Configuration** decision.
2. Confirm the **six proven divergences** are complete (NIR: cross-border, single-use CR094, ref-number
   stations; Glider: Metro/Ulsterbus products, Old BRS, cEMV inspection) — and confirm **NIR TOTO inspection
   is future scope** (FBD-100690) so it is tagged `@future`, not authored now.
3. Decide **EXCLUDE to a BOS/MERIT suite** for Merit (14) + CloudFare back-office (18), keeping only the
   HHD-device-impacting subset (payment device, device functionality) — the ETM precedent.
4. Mine 13958 (HHD Master) + 5505 (R1.1) for any non-superseded detail before dedup.
5. Resolve the **single-use version drift** (author to FBD-100483/CR094, not legacy FBD-100317 online flow).
6. `mode-coverage.md` written (shared / NIR-only / Glider-only map + Run-Config spec) and
   `discover-fields` run to fill the HHD `custom_devtypes` id.
```
