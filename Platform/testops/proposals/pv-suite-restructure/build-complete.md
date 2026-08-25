# PV (Platform Validator) suite — BUILD COMPLETE (2026-06-08)

Target `**NEW** PV-Acceptance Test Suite` (**30255**), project 42, device `custom_devtypes [10]`.
Source (read-only) `AA-Platform Validator Acceptance Test` (10047, 1,144 cases). Audit: **CLEAN —
0 blocking, 21 advisory** (intentional "Validate a …" / screen-name titles).

## Coverage-completeness pass (George): +14 cases from a full title-level sweep
After the initial build, a **case-title-level sweep of all 1,144 old cases** (not just the section
structure + run data) surfaced recently-added / structurally-hidden behaviours that were folded too
hard or missing. Added 14 cases (`pv-additions.cases.yaml` + `pv-additions-2.cases.yaml`): Pilot List
management, Deny/BIN delta+full updates (TIBU-26320/25745), FEIG software/OTA + ITSO/EMV reading,
MERIT heartbeat, scheduled reboot, config/topology distribution, comms resilience + secondary
failover, scheduled maintenance, cEMV decline-reasons + route-types + JourneyTap/alighting-derivation,
inter-device (POS/legacy) top-up→PV validation, performance timings, backup/layout/audible feedback.
Full old→new mapping for both modes in `coverage-map.md`. **Final: 111 active cases.**

## Final shape — 111 active cases (from 1,144)
| Section | Cases |
|---|---|
| HMI Screen Validation (Validation Screens + Technician Menu) | 49 |
| Functional (Smartcard Validation 17 + ABT/Barcode/Legacy 13 + Technician Menu 7) | 37 |
| Smoke | 6 |
| Non-Functional (power, PV↔BOS, DST) | 5 |

## How we got from 1,144 → 97
- **Evidence-led:** the latest live regression plan `PV 3.1.2.15214` ran only **261/1,144 (~23%)** —
  Smartcard Validation 221 + Multi-Use Barcodes 21 + Technician Menu 16. The big run before it was
  named "for deletion". So ~880 cases were dead weight. (See `old-suite-audit.md`.)
- **Consolidation:** the ~800-case Glider/Rail validation matrix (product × Adult/Child ×
  Valid/Invalid × mode) folded into **11 product-family validation flows** (valid+invalid) with the
  products/passenger/zone as variation lines, run under **Glider + Rail Configurations**.
- **Added coverage** beyond the live regression (to find more bugs): ABT/cEMV (deny/BIN/pilot lists,
  enablement checks, transfers), Legacy/MIFARE/DESFire, Operating Times, full Technician Menu, PV↔BOS
  comms, power, DST — none of which the live regression exercised.
- **Excluded:** BOS/CloudFare web-admin cases (different system); `Delete`/`Unsure` housekeeping.

## Scope / model
PV = unattended validator (present smartcard/barcode/cEMV → validate; no sign-on/issue). Modes Glider
+ Rail via Configurations; shared validation once, Rail-only (NIR transfers, zone) and Glider-only
(TOO/cEMV) in their own sections. Regression: `Fixes/Changes` fix-checks fold into the owning
functional case via Refs (`regression-register.md`) — no dedicated section needed.

## George — TestRail UI actions
1. **Set up Run Configurations** on suite 30255: **Glider** and **Rail**. (A Glider run = shared
   validation + Glider-only; a Rail run = shared + Rail-specific.)
2. No `ZZ_DELETE` bin needed — PV was built fresh in the new suite; the old suite 10047 is untouched.
3. *(Optional, cosmetic)* the two UX image folders are still named `Translink Validators 3.1.7 - …`;
   they can be left, or I can tidy them into `pv/<slug>/` on request.

## Optional follow-ups (on request)
- Enrich historical `Fixes/Changes` defect ids onto their owning cases' Refs for full traceability.
- Grab a PV Overflow flow-data JSON (if one exists) to add rich annotation grounding like ETM.

## Files (proposals/pv-suite-restructure/)
old-suite-audit.md, structure.md, regression-register.md, build-complete.md, and the pushed specs:
smartcard-validation, abt-barcode-legacy, technician-nonfunctional, hmi (generated via
tools/gen_pv_hmi.py), smoke.
