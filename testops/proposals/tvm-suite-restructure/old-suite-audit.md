# TVM suite restructure — old-suite audit (foundation)

**Target (build here, write-only):** `**NEW** TVM Test Suite` **id 30284**.
**Push schema:** template_id 1, **custom_devtypes [1]** (TVM), custom_revstatus 2, autoconfirmation false.
**Device:** Translink TVM — **two hardware models with possible functional differences: Kiosk and Astreo.**
Audit-first (per `docs/test-practices.md`): cross-tab the old suites to PROVE shared vs model/mode-
specific before authoring. Consolidation rule (same as POS/ETM/PV): **shared behaviour authored ONCE;
a per-model (Kiosk/Astreo) or per-mode (Metro / Glider / Ulsterbus / NIR-Rail) case only where the
steps genuinely diverge** — no doubling/tripling of cross-functional cases.

## Source suites to consolidate (project 42)
| Suite | id | Cases | Role |
|---|---|---|---|
| AA-TVM-Acceptance Test-V03 | 5602 | 195 | Acceptance baseline (house Gherkin reference) |
| R:2 - MAN - FNC - TVM | 6160 | 1115 | R2 functional — commissioning, EMS, sales, tickets, smartcards, deployment/topology |
| TVM Kiosk — EMS & TMS | 22270 | 148 | **Kiosk** back-office/maintenance |
| TVM Kiosk — Rail | 22272 | 440 | **Kiosk** NIR rail tickets/smartcards/cash/card |
| TVM Kiosk — Bus | 22273 | 389 | **Kiosk** bus tickets/smartcards/cash/card |
| TVM Kiosk — Fixes/Changes | 22274 | — | Kiosk regression (fold by feature via Refs) |
| TVM Astreo — EMS & TMS | 22275 | — | **Astreo** back-office/maintenance |
| TVM Astreo — Cash & EMV Cards | 22276 | — | **Astreo** payments |
| TVM Astreo — Glider | 22278 | 159 | **Astreo** Glider tickets/smartcards |
| TVM Astreo — Fixes/Changes | 22279 | — | Astreo regression (fold by feature via Refs) |
| R1.0-TVM-Acceptance / TVM Project 3 | 5382 / 18835,18846,19117 | — | Older — mine only for anything not superseded |
| `Delete`/`ZZ **TVM ...**` suites | 18847-49, 21861-64, 22271, 22277 | — | Superseded — **ignore** |

## Model / mode landscape (from old-suite sections)
- **Kiosk** organises by **mode**: Rail (NIR) and Bus, each with Generic/Adult/Child/Cross-Border
  tickets, Basket, Family & Friends, Smartcards, Cash + Card/Contactless/EMV, Ticket Collection,
  Mini Statement, Ticket Numbering.
- **Astreo** organises by product/validity: Glider tickets, yLink, concessions, Half-Fare, Staff,
  invalid cards, Ticket Formats, Barcode Redemption, Ulsterbus Validation, Cash + EMV.
- **Common (both models):** commissioning, deploy software/config/topology, EMS/maintenance, sales
  app, tickets, smartcards, ticket collection, barcode redemption, cash & card/EMV payments,
  error management, mini statement.
- **Divergence to PROVE (Kiosk vs Astreo):** payment hardware (EMV/contactless), Glider on Astreo,
  EMS/TMS specifics, ticket formats, any peripheral differences. This is the cross-tab to build.

## Grounding specs (knowledge/translink/specs)
FBD-100515 (Grouped Stops on TVM — cheapest-fare boarding-stop rule), FBD-100341 (Revenue
Apportionment TVM & POS), FBD-100167/100317 (barcode — **TVM validates single-use only**),
FBD-100320/100353 (TID management / EMV devices), FBD-100336/100207 (fares/fare-stage), FBD-100266
(heartbeat), FBD-100359 (SaaS comms). Ground assertions in these + the acceptance baseline (5602).

## Proposed structure (DRAFT — for George's sign-off before building)
Test-type-first, model handled like modes (author shared once; Run Configurations carry Kiosk/Astreo
× operating mode):
- **Smoke** — thin critical path (both models).
- **Functional / Commissioning & Deployment** — commission, software/config/topology deploy, failed
  deployment, EMS/TMS/maintenance. (shared; Kiosk-only or Astreo-only leaves where they differ)
- **Functional / Sales — Tickets** — generic/adult/child, cross-border (Rail), basket, family &
  friends, ticket numbering, ticket collection, ticket formats, advance/3-day, mini statement.
  (shared; mode subsections NIR-Rail / Ulsterbus / Metro / Glider only where divergent)
- **Functional / Smartcards** — validation/issue/top-up, yLink, concessions, half-fare, staff,
  invalid cards.
- **Functional / Payments** — Cash; Card / Contactless / EMV (prove Kiosk vs Astreo hardware split).
- **Functional / Barcode** — single-use validation/redemption (TVM = single-use only).
- **Non-Functional** — power/reboot, comms-lock/SaaS, printer/peripherals, performance.
- **Regression** — fold Kiosk & Astreo Fixes/Changes by feature via Refs.
- **Model-specific leaves** — `... / Astreo only` and `... / Kiosk only` only where functionality
  genuinely differs (e.g. Astreo Glider, model-specific payment/EMS).

## Open questions (register)
- Confirm the definitive **Kiosk vs Astreo functional differences** (drives the model-specific leaves).
- Is **Glider on Astreo only** (Kiosk has no Glider)? Old suites suggest yes — confirm.
- Any TVM behaviours only in R1.0/Project-3 suites still in scope?
