# Proposal: restructured Translink TVM suite

Goal: consolidate the old TVM suites (5602, 6160, Kiosk 22270/22272/22273/22274, Astreo
22275/22276/22278/22279) into a cleaner, test-type-first new suite **`**NEW** TVM Test Suite`
(id 30284)** — reuse the good old cases, dedupe the model×mode triplication, and fold the
Fixes/Changes regression by feature. Read-only / propose-first: this is the blueprint, not authoring.
Evidence: `cross-tab.md` (this folder). Governing mindset: `docs/test-practices.md`.

## Model & mode decision (the crux)
- **Two hardware models: Kiosk · Astreo.** Four operating modes: **NIR-Rail · Ulsterbus · Metro · Glider.**
- `cross-tab.md` proves the two models share **~90%** of behaviour (EMV/contactless, cash acceptance,
  smartcards/ABT, single-use barcode, EMS/TMS core, commissioning, sales tickets, formats). Divergence
  is confined to **four proven areas** (see below).
- **Decision (follows the ETM precedent, not POS):** structure is **feature/test-type-first**, and
  **both the model (Kiosk/Astreo) and the mode (NIR-Rail/Ulsterbus/Metro/Glider) are handled by
  TestRail Run Configurations** — shared behaviour authored **once**, executed against each
  model×mode configuration. Mode-first / model-first section trees would create near-empty duplicate
  trees and split the shared 90% for no benefit (the POS lesson, recorded in etm structure.md).
- **Model/mode coverage lives in `model-mode-coverage.md`** (the shared / Kiosk-only / Astreo-only /
  per-mode map + the Run-Configuration spec) — the same visibility POS gets from mode sections,
  without the duplication. Explicit `… / Kiosk only` and `… / Astreo only` **leaves appear only for
  the four proven divergences**:
  1. **Kiosk only — Alarmboard / enclosure maintenance** (R2 `EMS Maintenance (Kiosk only)`).
  2. **Kiosk only — NIR-Rail & Cross-Border ticketing** (Astreo has zero rail sales).
  3. **Astreo only — BNR note-recycler error flows + insufficient-change / change-voucher**.
  4. **Kiosk only — coin-recycler-hopper maintenance** (Kiosk cash unit).
  (Glider is a **shared mode**, not an Astreo leaf — proven in `cross-tab.md` §2.)

## Proposed section tree
```
**NEW** TVM Test Suite (30284)     ← Configurations: Model{Kiosk·Astreo} × Mode{NIR-Rail·Ulsterbus·Metro·Glider}
│
├─ SMOKE                                   @model(all) @mode(all)   thin critical path, both models
│     wake from screensaver → select mode → fare look-up → basket → pay (cash/EMV) → print → collect
│
├─ FUNCTIONAL
│   ├─ Commissioning & Deployment          commission, deploy SW/config/topology, failed deploy,
│   │                                       scheduled pre-deploy, BOS remote commands / VNC
│   ├─ Sales — Tickets                      generic/adult/child/family, evening, Summer Bus Rambler,
│   │   │                                   popular, 3-day, basket (add/amend/remove/identical), qty limits
│   │   ├─ NIR-Rail / Cross-Border …/Kiosk only   Cross-Border Adult/Child, NI rail, rail 3-day
│   │   ├─ Ulsterbus                         @mode(Ulsterbus)   NI Adult/Child/Family, cross-border bus, town services
│   │   ├─ Metro                             @mode(Metro)       Metro Adult/Child/Family/yLink
│   │   └─ Glider                            @mode(Glider)      Glider/Metro day & family tickets
│   ├─ Sales — Ticket Collection & Mini Statement
│   ├─ Smartcards & ABT                      ABT tap/issue/top-up, journey-based, time-based (iLink/
│   │                                        Daylink/Metro Travelcard), concessionary, half-fare, staff,
│   │                                        yLink, 24+, Smartpass validation, invalid cards, error mgmt
│   ├─ Payments — Cash                       coins & banknotes (valid/invalid, bank-specific notes,
│   │   │                                    old/incorrect currency), return payment
│   │   └─ Note Recycler & Change            …/Astreo only   BNR functional/non-functional, BNA errors,
│   │                                                         insufficient-change → change voucher
│   ├─ Payments — EMV / Contactless          @model(all)   Chip&PIN (MC/VISA/Amex/Diners), Contactless +
│   │                                        Apple/Google/Samsung Pay (MC & VISA), cancel-cash-then-EMV,
│   │                                        payment-does-not-complete, PAN edge cases   [FBD-100320/100353]
│   ├─ Barcode Redemption (single-use)       Glider/Metro/Rail/Ulsterbus product validation, legacy
│   │                                        stages, failed validation, barcode ticket format   [FBD-100167/100317]
│   └─ Ticket Formats & Receipts             format catalogue (rail formats land on Kiosk config)
│
├─ NON-FUNCTIONAL / RESILIENCE
│   ├─ EMS / TMS Maintenance                 asset manager, remote control of TVM status, cash-collection
│   │   │                                    reports, config topology, home/location/sub-location,
│   │   │                                    software versions, technician functions, ticket roll length,
│   │   │                                    transaction report, volume, screen brightness, staff/HMI login
│   │   ├─ Alarmboard & Enclosure    …/Kiosk only   siren, LEDs, temperature, UPS, door/sensor, speaker,
│   │   │                                            ticket-chute fan, TL80 alignment, touchscreen, keyboard-kill
│   │   └─ Coin Recycler Hopper       …/Kiosk only   cash content report after hopper replacement
│   ├─ Degraded States & Error Mgmt          amber status transitions, print failure, Teltonika modem events
│   ├─ Device Lockout / Out-of-Service       out-of-service / in-service / comms-related states
│   ├─ Comms / SaaS / Heartbeat              BOS connection loss, audit-data to Cloudfare   [FBD-100266/100359/100341]
│   ├─ Screensaver / Wake-Up & Multi-Modal Home   mode-of-transport (bus/rail), language, screensaver interaction
│   ├─ Audio Speech Prompts
│   └─ Usability & Performance
│
└─ REGRESSION
      NOT a parking lot. Kiosk (22274, 345) & Astreo (22279, 296) Fixes/Changes folded into the
      FUNCTIONAL case that owns the behaviour (linked via Refs, incl. TIBU-#####). Only defects with
      no natural functional home live here. See bug-regression-register.md (to build).
```

## Governing mindset
All add/edit/merge/fold/leave decisions follow `docs/test-practices.md` — risk-based, minimal
sufficient coverage, no duplication, one behaviour per case, traceability via Refs (REQ + TIBU). The
model×mode cross-tab (`cross-tab.md`) is the mandatory precondition already met: guessing shared-vs-
model produced wrong duplicates on POS; here we author shared once and split only the four proven leaves.

## Suites
- **Source (old, read-only):** 5602, 6160, Kiosk 22270/22272/22273/22274, Astreo 22275/22276/22278/22279
  (+ mine R1.0 5382 and Project-3 18835/18846/19117 only for non-superseded detail — esp. BNR/BNA).
  Never modified or deleted from.
- **Target (new):** `**NEW** TVM Test Suite` (30284) — everything below is built here.

## Push defaults for this suite
```yaml
suite_id: 30284
defaults:
  template_id: 1
  custom_devtypes: [1]          # TVM
  custom_revstatus: 2
  custom_autoconfirmation: false
```

## Estimated consolidated case count
Old **main scope ≈ 3,368** cases (5602 195 + 6160 1,115 + Kiosk 1,322 + Astreo 736), before Project-3
(~7,100) and R1.0 (102). The count is inflated by three multipliers the new suite removes:
**(a)** the same behaviour authored twice, once per model (EMV, cash, smartcards, barcode, EMS core);
**(b)** fare-permutation explosion (every ticket × adult/child/family × payment × bank note / coin);
**(c)** ~641 Fixes/Changes cases (22274 + 22279) that fold into functional cases via Refs.

| New area | Est. cases | How it collapses the old total |
|---|---:|---|
| Smoke | ~10 | one critical path, both models |
| Commissioning & Deployment | ~25 | dedupe Kiosk/Astreo EMS deploy + BOS |
| Sales — Tickets (+ mode leaves) | ~120 | parametrise adult/child/family; modes = Run Configs, not copies |
| Sales — Collection & Mini Statement | ~10 | |
| Smartcards & ABT | ~70 | one matrix, both models; representative concessions not per-Smartpass-type |
| Payments — Cash (+ Astreo BNR leaf) | ~45 | one bank/denomination matrix; +Astreo BNR/change leaf |
| Payments — EMV / Contactless | ~40 | authored once (was duplicated Kiosk + Astreo) |
| Barcode Redemption | ~20 | one section (was duplicated Kiosk-Bus + Astreo) |
| Ticket Formats & Receipts | ~25 | format catalogue, rail formats on Kiosk config |
| EMS/TMS Maintenance (+ Kiosk leaves) | ~80 | shared core ~60 + Kiosk alarmboard/coin-recycler ~20 |
| Degraded / Lockout / Comms / Wake-up / Audio / Perf | ~55 | shared non-functional |
| Regression (un-homeable only) | ~20 | remaining 620 folded into functional via Refs |
| **Total** | **≈ 480–540 (~500)** | **~85% reduction vs the ~3,368 main-scope raw count** |

## Old → new mapping
Per-area `<area>.cases.yaml` built into 30284 via `push` (idempotent, new-suite-only; auto-audit gates
each push). Old suites untouched; "leave" = simply not carried over. UI moves/bins done by George
(this instance's API can't move/re-parent/delete).

## Gated on (before authoring)
1. George's sign-off on this section tree and the **model+mode = Run Configuration** decision.
2. Confirm the **four proven divergences** are complete (alarmboard, rail/cross-border, coin-recycler,
   Astreo BNR/change) — and resolve the **Kiosk-Rail Multi-Use Barcodes vs FBD-100167/100317
   single-use** conflict (deprecate or justify).
3. Mine Project-3 (18835/18846/19117) for BNR/BNA detail and any fare permutation not represented in R2.
4. `model-mode-coverage.md` written (shared / Kiosk-only / Astreo-only / per-mode map + Run-Config spec).
