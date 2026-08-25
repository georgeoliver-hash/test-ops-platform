# TVM suite restructure — cross-tab (the evidence)

Read-only audit. Purpose: **prove** what is shared across the two TVM models (Kiosk / Astreo) and the
four operating modes (NIR-Rail / Ulsterbus / Metro / Glider) before authoring, so the new suite
authors shared behaviour **once** and only splits by model/mode where the steps genuinely diverge.

Evidence base = section trees + case titles pulled from the old suites (project 42). Counts are cases
per section. Source dumps in scratchpad; method per `docs/test-practices.md` (audit-first cross-tab).

## Source suites in scope (raw case counts)
| Suite | id | Cases | Role |
|---|---|---|---|
| AA-TVM-Acceptance Test-V03 | 5602 | 195 | Acceptance baseline (house Gherkin reference) |
| R:2 - MAN - FNC - TVM | 6160 | 1115 | R2 functional (both models; the richest source) |
| TVM Kiosk — EMS & TMS | 22270 | 148 | Kiosk back-office / maintenance |
| TVM Kiosk — Rail | 22272 | 440 | Kiosk NIR-Rail sales |
| TVM Kiosk — Bus | 22273 | 389 | Kiosk bus sales (Metro / Ulsterbus / Glider) |
| TVM Kiosk — Fixes/Changes | 22274 | 345 | Kiosk regression (fold by feature via Refs) |
| TVM Astreo — EMS & TMS | 22275 | 135 | Astreo back-office / maintenance |
| TVM Astreo — Cash & EMV | 22276 | 146 | Astreo payments |
| TVM Astreo — Glider | 22278 | 159 | Astreo bus/street sales |
| TVM Astreo — Fixes/Changes | 22279 | 296 | Astreo regression (fold by feature via Refs) |
| R1.0-TVM-Acceptance | 5382 | 102 | Older acceptance — mine only for non-superseded |
| TVM Project 3 | 18835/18846/19117 | 3988/1795/1333 | Exhaustive per-fare permutation matrices — mine only |
| **Main consolidation scope (5602+6160+Kiosk+Astreo)** | | **≈3,368** | (Project-3 + R1.0 excluded from the total) |

---

## 1. Feature-area cross-tab (Shared / Kiosk-only / Astreo-only / mode-specific)

| Feature area | Verdict | Evidence (suite / section) |
|---|---|---|
| **Commissioning & deployment** (commission, deploy SW/config/topology, failed deployment, scheduled pre-deploy) | **Shared** | R2 `TVM > Commissioning Process` (5), `Deploy the Software, Configurations & Topology` (6) incl. `Failed Deployment`, `Scheduled - Pre-Deployment`, `Topology`; Kiosk-EMS `Device Dataset Deployment` (4) + `Software Versions > Failed/Scheduled`; Astreo-EMS `Device Dataset Deployment` (4) + `Software Versions > Scheduled`. Same sections both models. |
| **BOS interfaces** (remote commands, VNC, software distribution) | **Shared** | Kiosk-EMS + Astreo-EMS both `BOS Interfaces > Remote Commands and VNC Access` (3) + `Software Distribution and Commissioning` (4); mirrors 5602 baseline. |
| **EMS / TMS maintenance core** (Asset Manager, Remote Control of TVM status, Cash Collection reports, Configuration Topology, Home/Location/Sub-Location, Software Versions, Technician Functions, Ticket Roll Length, Transaction Report, Volume Control, screen brightness, Staff Mgmt/HMI login) | **Shared** | Kiosk-EMS (22270) and Astreo-EMS (22275) section sets are near-identical. Set-diff: only Kiosk carries `TVM Initial Set up`, `Events & Alerts`, `TVM goes Out of Service`; Astreo folds equivalents under a single `TVM` (16) section. No functional divergence in the maintenance primitives. |
| **EMS — Alarmboard / enclosure security** (siren, LED, ticket-tray LED, temperature, UPS status, door state, sensor test, payment LED, speaker, ticket-chute fan; TL80 printer alignment; touchscreen maintenance; on-screen keyboard kill) | **Kiosk-only** | R2 section literally named **`EMS Maintenance (Kiosk only)`** (15) — every case is `Maintenance of Alarmboard - …`. Astreo has no Alarmboard section. The Kiosk is a standalone secured cabinet (alarmboard + burglary sensors); Astreo is not. |
| **Burglary / intrusion** (screen slider & scroller, door tamper) | **Shared surface, Kiosk-deeper** | Both have `Burglary` + `Screen Scroll & Slider Operation` (Kiosk 12/7, Astreo 12/8). Burglary status monitoring is shared; the Alarmboard maintenance underneath it is Kiosk-only (above). |
| **Cash — coins & banknotes acceptance** (valid/invalid coins & notes, bank-specific notes: Bank of Ireland/Danske/Ulster, old/incorrect currency, return payment) | **Shared** | Kiosk-Rail + Kiosk-Bus `Correct/Incorrect/Old Currency`; Astreo-Cash-EMV identical `Correct/Incorrect/Old Currency`, `Valid Coins`, `Return Payment` (10). Same denomination/bank matrix both models. |
| **Cash — note recycler + change-giving** (BNR functional/non-functional, BNA error management, insufficient-change → change voucher) | **Astreo-only (behaviour)** | Astreo-Cash-EMV has dedicated `BNR Functionality` (3), `BNA Errors` (2), `Payment Reached - Insufficient Change Available` (2, "Refuse Change Voucher"). Kiosk has **coin recycler hoppers** (Kiosk-EMS "Cash Content Report after Replacement of **Coin Recycler** Hopper") and only a passing `Maintenance of BNR - View Status Screen`. So: both have a BNR unit, but the note-recycler exit-beak error flows and change-voucher-on-low-change behaviour are authored only for Astreo → **genuine payment-hardware divergence**. |
| **EMV / contactless payments** (Chip&PIN Mastercard/VISA/Amex/Diners; Contactless + Apple/Google/Samsung Pay Mastercard & VISA; cancel-cash-then-EMV; payment-does-not-complete; PAN edge cases) | **Shared** | Kiosk-Rail `EMV` and Astreo-Cash-EMV `EMV` are the **same matrix** (Apple/Google/Samsung Pay × MC/VISA, Chip&PIN MC/VISA, Amex/Diners, cancel-cash-and-pay-EMV, payment-does-not-complete). R2 `EMV PAYMENTS` is the union. **No Kiosk-vs-Astreo EMV divergence found** — the EMV/contactless stack is common. Ground on FBD-100320/100353 (TID/EMV). |
| **Smartcards & ABT** (ABT tap/issue/top-up, journey-based, time-based iLink/Daylink/Metro Travelcard, concessionary, half-fare, staff free pass, yLink, 24+, Smartpass validation, invalid cards, error management) | **Shared** | Kiosk-Rail `Smartcards` (24+, concessionary, half-fare, staff, journey/time-based, yLink, error mgmt); Kiosk-Bus `Valid/Invalid Smartcards`; Astreo-Glider `Smartcard` + `invalid Cards` (Concession/Half-Fare/Staff). Same structure. R2 `CUSTOMER SMARTCARDS` + `MULTI-MODAL > Smartcards` is the union. yLink appears in both (Kiosk 30/31, Astreo 16). |
| **Barcode redemption — single-use** (Glider/Metro/Rail/Ulsterbus product validation, legacy stages, failed validation, barcode ticket format) | **Shared** | Kiosk-Bus `Barcode Redemption` and Astreo-Glider `Barcode Redemption` are the **same section** (Glider/Metro/Rail/Ulsterbus product validation, legacy stage, failed validation). Ground on FBD-100167/100317 (TVM validates **single-use only**). |
| **Barcode — multi-use** | **Kiosk-Rail only (anomaly — verify vs spec)** | Kiosk-Rail `Multi-Use Barcodes` (12) + `New Barcode Redemption`. FBD-100167/100317 say **TVM is single-use only**, so this section is a candidate for review/deprecation, not a proven model divergence. Flag for George. |
| **Sales — generic/adult/child/family tickets, basket, popular, evening, Summer Bus Rambler, ticket collection** | **Shared** | R2 `BASKET`, `CUSTOMER TICKETS - Generic`; Kiosk-Bus `Basket`, `Metro/Ulsterbus Tickets`, `Popular Tickets`; Astreo-Glider `Valid Tickets` (Adult/Child/Family/Popular/yLink), `Basket`. Rambler in both (Kiosk-Bus 29, Astreo 7). Ticket Collection in both. |
| **Glider / Metro tickets** | **Shared (NOT Astreo-only)** | "Glider" appears in Kiosk-Bus (73), R2 (99) **and** Astreo (25). Kiosk-Bus `Basket > Adding Glider / Metro Day tickets`, `Metro Tickets > Metro Adult/Child/Family/yLink`. **The hypothesis "Glider is Astreo-only" is refuted** — Glider/Metro is a shared Belfast-city product sold on both models. See §2. |
| **NIR-Rail / Cross-Border tickets** (Adult/Child NI rail, Cross-Border Adult/Child, 3-Day, Cairnshill P&R, Europa, City Airport) | **Kiosk-only (mode NIR-Rail)** | "Cross Border" = Kiosk-Rail (63), Kiosk-Bus (38); Astreo suites **0** (Astreo-Fixes 1 incidental). Kiosk-Rail `Cross Border Tickets > Adult(21)/Child(21)`, `Northern Ireland Tickets`. Astreo has no Rail sales suite. **Rail ticketing is the real model split — Kiosk-only.** See §2. |
| **Ulsterbus tickets & validation** (NI Adult/Child/Family, Cross-Border bus, town services, Ulsterbus basket) | **Shared, mode Ulsterbus** | Kiosk-Bus `Ulsterbus Tickets`; Astreo-Glider `Barcode > Ulsterbus Validation/Failed`. Ground FBD-100340 (Ulsterbus town services), FBD-100662 (Ulsterbus tap-on-only). |
| **Ticket formats & receipts** | **Shared (per-format lists differ)** | 5602 `Ticket Formats and Receipts` (18); R2 `Ticket Format` (formats 1-14); Kiosk `Ticket Formats and Receipts > Rail` + `Formats > Cash/Card`; Astreo-Glider `Ticket Formats` (14). Same behaviour, model-specific product lists (Rail formats Kiosk-only). |
| **Mini statement** | **Shared** | Kiosk-Rail `Mini Statement` (4), Kiosk-Bus `Mini Statement` (4). (Astreo folds into TVM/Glider flows.) |
| **Multi-modal home / mode-of-transport selection, language, screensaver wake-up** | **Shared** | R2 `MULTI-MODAL > Home Workflow` (Mode of Transport - Bus/Rail), `Language`, `TVM INTERFACE SCREEN ON WAKE UP`. |
| **Degraded states & error management** (amber status transitions, print failure, Teltonika modem events) | **Shared** | 5602 + R2 `Degraded States and Error Management`; Kiosk-EMS (10) + Astreo-EMS (12) identical section. |
| **Device lockout / out-of-service / comms-related states** | **Shared** | R2 `DEVICE LOCKOUT` (out-of-service / in-service / comms). Kiosk-EMS `TVM goes Out of Service`. Ground FBD-100266 (heartbeat), FBD-100359 (SaaS comms). |
| **Events & alerts, burglary status, audit data to Cloudfare** | **Shared** | R2 `EVENTS & ALERTS`, `OTHER > Audit Data sent to Cloudfare` (5). Ground FBD-100341 (revenue apportionment TVM & POS). |
| **Audio speech prompts, HMI screens, usability/performance** | **Shared (non-functional)** | R2 `AUDIO SPEECH PROMPT` (29), `HMI`, `PLACEHOLDER > Usability and Performance` (11). |
| **Grouped stops (cheapest-fare boarding-stop)** | **Shared** | Ground FBD-100515 (grouped stops on TVM) — behaviour spans fare look-up; not a model split. |

---

## 2. Direct answers to the audit's open questions

### What genuinely differs between Kiosk and Astreo?

**Kiosk-only (proven):**
- **Alarmboard / secured-enclosure maintenance** — the whole R2 `EMS Maintenance (Kiosk only)` block:
  siren, LEDs (ticket-tray, payment), temperature, UPS status, door state, sensor test, speaker,
  ticket-chute fan, TL80-printer alignment, touchscreen maintenance, on-screen-keyboard kill. Astreo
  has no alarmboard. This is the Kiosk being a standalone locked cabinet.
- **NIR-Rail & Cross-Border ticketing** — Cross-Border Adult/Child, NI rail tickets, 3-Day rail, rail
  ticket formats. Astreo has zero Rail/Cross-Border cases. Astreo is a bus/street TVM; Kiosk is the
  rail-station TVM (plus bus). This is the single biggest sales divergence.
- **Coin-recycler-hopper maintenance** (Kiosk cash unit) — Cash Content Report after replacing a coin
  recycler hopper.
- **Multi-Use Barcodes** (Kiosk-Rail) — present, but conflicts with FBD-100167/100317 (TVM = single-use
  only); treat as a **verify/deprecate** item, not a confirmed capability split.

**Astreo-only (proven):**
- **Bank Note Recycler (BNR) error flows + change-giving** — `BNR Functionality` (exit-beak non-functional
  states), `BNA Errors`, and `Insufficient Change Available → Refuse Change Voucher`. Astreo's note unit
  recycles notes and issues change vouchers; these flows exist only in the Astreo suite. This is the
  main **payment-hardware** divergence.

**Shared (proven — author ONCE, do NOT duplicate per model):**
- **EMV / contactless** (Apple/Google/Samsung Pay, Chip&PIN MC/VISA/Amex/Diners) — identical matrix in
  Kiosk-Rail and Astreo-Cash-EMV. **No EMV divergence.**
- **Cash coin/banknote acceptance** (bank-specific notes, old/invalid currency, return payment).
- **Smartcards & ABT** (concessions, half-fare, staff, yLink, journey/time-based, invalid cards).
- **Barcode single-use redemption** (Glider/Metro/Rail/Ulsterbus validation) — same section both models.
- **EMS/TMS maintenance core** (asset manager, remote control, cash-collection reports, config topology,
  locations, software versions, technician functions, roll length, transaction report, volume, brightness).
- **Commissioning/deployment, BOS interfaces, degraded states, device lockout, events/alerts, audio,
  multi-modal home, sales tickets/basket, ticket formats, mini statement.**

### Is Glider Astreo-only?
**No.** Glider/Metro is a **shared** Belfast-city product — it appears in Kiosk-Bus (73 mentions), R2
(99) and Astreo (25). The Astreo suite is *named* "Glider" because Astreo's entire product set is
bus/street (Glider/Metro/Ulsterbus). The real asymmetry is the opposite: **Rail/Cross-Border is
Kiosk-only.** Glider should be a shared **mode** (Run Configuration), not an Astreo-only leaf.

### Anything only in R1.0 / Project-3 (still in scope)?
- **R1.0 (5382):** adds `Kiosk - Airport` and `Legacy Devices` sections. Airport-kiosk content is
  superseded by R2/Kiosk suites (City Airport also appears in R2 `George Best City Airport`);
  `Legacy Devices` is an empty holding. **Nothing uniquely in scope** — mine only if an airport-specific
  ticket format is missing from R2.
- **Project-3 (18835/18846/19117, ~7,100 cases):** exhaustive per-fare permutation matrices (Glider 393,
  Rambler 122, yLink 151 in one suite alone) and the deepest **BNR/BNA** coverage (35 BNR mentions).
  These are the source to mine for **BNR/BNA behaviour detail** and any fare permutation not represented
  elsewhere — but they are permutation explosions, **not** a structural source. Do not carry the matrices
  across wholesale; parametrise.

---

## 3. Consolidation implication (feeds structure.md)
The two models share ~90% of behaviour (payments-EMV, cash, smartcards, barcode, EMS core, sales,
commissioning). Divergence is confined to: **Kiosk** = alarmboard/enclosure + Rail/Cross-Border sales +
coin-recycler; **Astreo** = BNR note-recycler/change-voucher flows. Therefore the new suite should be
**feature/test-type-first with model handled by Run Configuration** (like ETM's 2-mode decision, not
POS's mode-first tree), plus a small number of explicit `… / Kiosk only` and `… / Astreo only` leaves
for the four proven divergences above. Modes NIR-Rail / Ulsterbus / Metro / Glider are also Run
Configurations, with NIR-Rail cases naturally landing on the Kiosk configuration only.
