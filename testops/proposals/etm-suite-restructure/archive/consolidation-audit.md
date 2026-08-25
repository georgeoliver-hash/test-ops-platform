# ETM suite — consolidation audit (suite-wide, 2026-06-08)

Applying the sign-on lens to EVERY functional area: fold **sequential steps of one flow** and
**variations of one behaviour** into a single flow test (with extra steps / a variation line); keep
**genuinely distinct risks/scenarios** and **mode-specific** behaviour separable. HMI Screen
Validation (280) stays per-screen by design. Non-Functional reviewed but largely distinct.

Goal: same coverage, fewer individual tests, each test = one risk/flow walked end-to-end.

## Fare Look-Up — Navigation (6 → 2)
- FOLD → **FLU — navigate and select products** : product pages/toggle groups + preset/menu-type + journey-type toggle + selection 60s timeout (one screen's navigation, walked).
- FOLD → **FLU — set boarding and alighting stages** : manual boarding-stage change (GPS/speed gated) + alighting selection & paging.

## Fare Look-Up — Sales (11 → 7)
- FOLD → **FLU — ticket type selection, change and default reversion** (3 cases: select + change + default-reversion).
- FOLD → **FLU — numeric entry, change and last transaction** (numeric/change + last-transaction display).
- REMOVE duplicate **FLU — Easibus** (Ticket Issue already covers Easibus issue).
- KEEP: group ticket, currency switch, Travel Mode, passenger count, favourite stages, start-new-journey.

## Ticket Issue + Promo + Basket (17 → 10)
- FOLD → **Ticket Issue — annulment** (annul last + timeout + refused-non-annullable = one flow, 3→1).
- FOLD change-receipt into **issue a single ticket** as a variation (2→1).
- KEEP: issue single, open-tickets, printer/power interrupt.
- Promo (4→2): FOLD add-additional-child into **issue a promo product** (variation); KEEP not-available; MOVE basket-tracker into Basket.
- Basket (5→3): **build & pay** (incl mandatory receipt), **limits & quantity** (9-max + Basket Full + +/- quantity), **clear / add-more / annul + basket tracker**.

## Smartcards & ABT (28 → 20)
- Validation (5→4): FOLD validation-and-passback + direction/transfer-rules → **validation and passback rules**; KEEP invalid-card, concessionary, faulty.
- Top-up (7→4): FOLD successful + max-50 + expired-removed → **top-up (successful, max, expired removed)**; KEEP cancelled/back, annulment, mini-statement, inter-device → (mini-statement + inter-device kept; 7→4 means folding 3 into 1 and keeping cancelled+annulment+inter-device+mini = 5; net 7→5).
- ABT (10→7): FOLD success + passback + mobile-wallet → **ABT tap (success, passback, wallet)**; FOLD declined + EMV-failure → **ABT tap failures**; KEEP availability, Metro-zone, Ulsterbus-zone, revert-fixed-fare, back-office.
- KEEP: MJ Metro-zone + MJ Ulsterbus-stage (2), hotlist (1), capping (3).

## Driver / Supervisor / Technician menus (27 → 17)
- Driver (14→9): FOLD **Driver options — view information** (totals + messages + Word&Colour + paper-status + ticket-history/last-ticket = one walk); FOLD **Driver options — device actions** (soft reboot + reboot card reader + report faulty reader); KEEP menu access/nav, Driver Break, Inspector, Other Devices, Display Settings, change currency.
- Supervisor (5→3): FOLD versions + GPS-info into a **view-info** test; KEEP force-comms, waybills, soft-reboot → (versions+GPS→1; force-comms; waybills+soft-reboot kept = 3).
- Technician (8→5): FOLD versions + device-status → **view device status & versions**; KEEP device-settings, display-settings, network-settings, force-comms, soft-reboot, decommissioning (decommissioning distinct) — trim to 5 by folding soft-reboot mention into device-status note.

## Barcode (7 → 5)
- FOLD online-successful + online-failures → **barcode online validation (pass and fail reasons)**; KEEP offline, multiple-use, mLink, reference-entry, printed/print-error → fold printed/print-error into reference or multiple. (7→5)

## Location (4 → 2)
- FOLD GPS lock + new-location + arrival + departure + look-ahead → **GPS notifications and tracking**; KEEP Travel-Mode brightness.

## Revenue Limit (2 → 2) — keep (approaching + reached are distinct outcomes).

## Non-Functional (23 → ~20) — light trim
- Power: keep (minor/major, recovery, charging, power-saving, scheduled-maintenance are distinct). Possibly fold power-saving + scheduled-maintenance.
- Displays/LEDs/Audio/PID: keep. Comms: keep (distinct BOS interactions). Time/cellular/auto-signoff/MIFARE/timings/third-party: keep.

## Projected totals
Functional **120 → ~78**; Barcode/Location/NF trims a further ~8. **Suite ~436 → ~385** active
(HMI 280 unchanged). Same coverage; ~50 fewer individual tests; every functional test = one
walked flow/behaviour. Absorbed cases retired as `ZZ_DELETE_REVIEW` into the `ZZ - To Delete` section.
