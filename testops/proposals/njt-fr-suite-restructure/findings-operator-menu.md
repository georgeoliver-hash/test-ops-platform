# Findings — NJT Fare Register (Operator Menu)

Cross-examined 304 existing cases spanning **four parallel trees**: orphaned top-level sections
(pre-restructure remnants), the legacy "Fare Register / Driver Functionality / Operator Menu" tree,
the JIRA-organized "TIBU-29384 - NJT - Operator Menu" tree, and the HMI "Driver menu (Section 9)"
tree — against `knowledge/njt/specs/fs002-operator-menu.md` (FS002 §5.4, all 14 menu items) and the
relevant HMI01 screens/receipt formats (Section 13).

## Duplication / suite hygiene (flagged, not fixed — human resolves via TestRail UI)

10 of 14 menu items show clear pre-restructure duplication — orphaned top-level cases
(`C4105437`–`C4105454`) duplicate content already held more granularly in the HMI and/or TIBU trees:
Driver Totals, Dump, End of Trip/Run, Relief, Device Settings, Paper Status, Driver Break,
Supervisor/Audit Reports, Accept Next Bill (partial), Clear Bill Jam. Cancel Ticket and End of Trip
show the heaviest 3-way duplication (legacy + HMI + TIBU). `C4105455` (Device Handling — comms loss)
is genuinely unique, not a duplicate.

## Section 13 receipts

All 5 relevant to this area (Cancel Receipts, Relief Report, End of Run Report, End of Trip Report,
Supervisor and Audit Report) have cases — no gaps.

## New cases drafted (3) — see `operator-menu.cases.yaml`

1. Cancel Ticket — exact 10-minute boundary eligibility.
2. Hold — Farebox dump-timeout resets to 60s (spec-explicit, never asserted).
3. Dump — Clever Device disconnected branch (message withheld).

## Gated on the 8 named spec gaps (no case drafted)

Cancel Ticket's Exact-Fare availability; Pay Leave's zone-range wording; Passenger Count's near-
total lack of spec detail; Relief's missing cancel path; Device Settings' missing Farebox restore-
default; Driver Break's unstated force-sign-off authority/audit; Supervisor Reports' unstated invalid-
ID logging; Clear Bill Jam's unstated audit event. See `gap-register-operator-menu.md`.

## New findings routed to the gap register (Q9–Q10)

- Driver Break's "if connected" (spec) vs "if in Exact Fare mode" (TIBU tests) discrepancy.
- Hold missing from the orphaned Exact-Fare restriction-list case.

No writes were made to TestRail; no "To Delete" cases were touched.
