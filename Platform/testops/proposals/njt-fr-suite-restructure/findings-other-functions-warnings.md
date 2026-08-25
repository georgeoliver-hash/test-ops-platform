# Findings — NJT Fare Register (Other Functions / FR Operation Warnings & Errors)

Cross-examined 99 existing cases (legacy "Other Functions" + "FR Operation Warnings and Errors"; HMI
Bus Inspection + Error/Warning Screens + Colour of the Day indicator; TIBU "Shortcut Keys" + "FR
Operation Warnings and Errors" + "Miscellaneous" trees) against
`knowledge/njt/specs/fs002-other-functions-warnings-errors.md` (FS002 §5.5–5.6).

## Classification

14 "Suite implications" checkpoints walked: 8 Covered outright, 4 Partial (Sum Function, Paper
Loading, Colour of the Day, Disable Receipt Printing), 2 Covered-with-defect-flags (GPS, Farebox
Failure/Comms loss).

## New cases drafted (6) — see `other-functions-warnings.cases.yaml`

Sum Function 10-transaction boundary; Paper Loading lid-close-triggers-test-print; Colour of the Day
at sign-on; Disable Receipt Printing split into Transfer/CTT/CRT (each named explicitly per spec
p.41, replacing the coverage gap left by one generic existing case).

## Existing-case defects found (flagged, not fixed — out of scope for drafting missing cases)

- **C4099505** — title says "10 consecutive NAKs" but its own step says "6 consecutive NAKs" trigger
  Standby. Internal contradiction within the same case.
- **C4104995** ("GPS - No GPS Data") has steps identical to **C4104994** — it never actually tests a
  no-fix condition.
- **C4088333**/**C4099514** may already answer the excluded AutoLog-off post-timeout gap via HMI
  §10.1/TIBU-30140 — flagged as a lead, not asserted as closed.

## Gated on the 12 named spec gaps (no case drafted)

Spotter class-code table; sum-function 11th-entry behaviour; failed test-print recovery; bus-
inspection receipt content/non-numeric input; colour/day mapping values; GPS no-fix handling; post-
AutoLogoff screen state; paper-low threshold; "special users" role definition; the 6-vs-10-NAK
relationship (see C4099505 above); Farebox Fault recovery path; Fare Mode attribute detail. See
`gap-register-other-functions-warnings.md` (Q1–Q12).

No writes were made to TestRail; no "To Delete" cases were touched.
