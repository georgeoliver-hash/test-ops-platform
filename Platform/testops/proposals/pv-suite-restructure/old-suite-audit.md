# PV (Platform Validator) — old-suite audit (evidence base, 2026-06-08)

Audit-first. Source (read-only): `AA-Platform Validator Acceptance Test` **id 10047** — **1,144 cases,
406 sections**. Target (new): `**NEW** PV-Acceptance Test Suite` **id 30255**. Push defaults
(from sample C2681551): `template_id 1`, **`custom_devtypes [10]`** (Validator), `custom_revstatus 2`.

## What the PV is
A **platform validator** — an **unattended** device mounted at Glider stops / Rail platforms (and
Glider vehicles). The passenger **presents a smartcard, barcode or contactless (cEMV/ABT) card** and
the PV **validates** it. **No operator sign-on, no ticket issue, no basket** (unlike POS/ETM). It has
a **Technician Menu** (PIN-protected) for config/maintenance. Comms via CloudFare/BOS.

## Modes / dimension that matters
The validation tree exists almost identically under **Glider** and **Rail** → the dimension is
**Glider vs Rail** (run via TestRail Configurations), most behaviour **shared**:
- **Shared (Glider + Rail) smartcard validation:** Concession SmartPasses (60+, Blind, Senior, ROI
  Senior, War Pensioner), Half Fares (DLA, Learning Disability, No Driving Licence, PIPS, Partially
  Sighted), Metro Daylink, Metro Multi-Journey (City/Inner/Extended zones), Metro Travelcard,
  Ulsterbus Multi-Journey, iLink (Zones 1-4/NW + Belfast Visitor Pass), aLink, yLink/24+, Translink
  Employee Smartcards (Staff/Partner/Retired/External/Dependents) — each × Adult/Child × Valid/Invalid.
- **Rail-only:** NIR Transfers (iLink/Belfast Visitor/Staff/aLink/EA transfers), Zone Validation, EA
  Pupil & Further Education Smartpass **Rail**.
- **Glider-only:** **Glider TOO** (Tap-On-Only / flat-fare): cEMV/ABT card validation, cEMV
  enablement (route-attribute / location / fare checks), Glider transfers, daily taps, pilot mode,
  Deny/BIN list download, FEIG/PV software update; EA Bus Pupil & Further Education Smartpass.

## The duplication (why 1,144)
The suite is **dominated by the smartcard-validation matrix**: every product × Adult/Child ×
Valid/Invalid × Glider/Rail = one case each (~800+ cases). The **validation mechanic is identical**:
present card → if valid, success outcome (+ passback rules); if invalid, the specific reason (Not
Valid At This Location / Invalid Time Of Day / Product Expired / Represent Card / Unable to Validate
/ wrong zone / outside time band / hotlisted). Only the **product/eligibility and fare** differ.

## Run-history (8 runs, 1204 cases)
Only **58 executed**, and (as on ETM) they are **CloudFare/BOS web-admin** cases (Dashboard/ABT/
Schedule/Reports/Settings/BI screen-content, CloudFare sign-on, Rules) that leak into the suite — the
PV validation cases are "orphaned" = simply not in these BOS-focused runs (NOT invalid). 35
always-failing + 25 title-flagged (`Delete`, `Unsure (To Be Organised)`, `Legacy`, `Fixes/Changes`).

## Live regression = the real "what's used" (from the latest plan PV 3.1.2.15214)
PV is regression-tested per release via **test plans** (Glider + NIR + Fixes/Changes runs) — these are
NOT returned by `get_runs` (plan-nested), which is why the first scan looked empty. The **latest**
plan `PV 3.1.2.15214` executed **261 of 1,144 cases (~23%)** — the rest is dead weight:
- **Regression Glider (121):** Glider Smartcard Validation **104** + Technician Menu **16** + 1.
- **Regression NIR (138):** Rail Smartcard Validation **117** + Multi-Use Barcodes **21**.
So the **real, used coverage = Smartcard Validation (221) + Multi-Use Barcodes (21) + Technician Menu
(16)**. The new suite MUST cover these; everything else (ABT/cEMV, Legacy, etc.) is added value (more
coverage than the live regression — find more bugs), not a like-for-like must. This confirms the
Glider/Rail Configuration split and the aggressive consolidation.

## Scope decisions (mirror ETM/POS)
- **PV device only.** EXCLUDE the BOS/CloudFare **web-admin** cases (different system). KEEP PV↔BOS
  interaction that impacts the PV (FEIG/PV software update via CloudFare TMS, Deny/BIN list download,
  BOS comms upload, force comms).
- **Bin the housekeeping** sections (`Delete`, `Unsure (To Be Organised)`) — triage into the new
  structure or leave. `Fixes/Changes / PV vX` = the **regression/defect** history → fold per
  `docs/test-practices.md`.
- **Glider + Rail** = Configurations; shared validation authored once; mode-specific sections for
  NIR Transfers / Zone (Rail) and Glider TOO / cEMV (Glider).

## Consolidation plan (the big win): ~1,144 → ~150
- **Smartcard Validation (~800 → ~30):** one behaviour case per **product family** ("Validate a
  <product> smartcard — valid and invalid"), with **Adult/Child** and the **specific products** as
  variation lines, run under **Glider/Rail** Configurations. Invalid-reason set captured once.
- **ABT / cEMV (Glider TOO):** tap success/declined, BIN/Deny/Pilot lists, cEMV enablement
  (route/location/fare), Glider transfers, daily taps — consolidate to ~12.
- **Barcodes:** single/multi-use, HHD/TVM-produced, validator barcode screens — ~6.
- **Legacy / MIFARE / DESFire / Passback / Invalid Smartcard / Operating Times / DST** — ~10.
- **Technician Menu:** login/PIN, location, brightness/ambient, audio, versions, force comms,
  network, power, operating times — ~10.
- **Non-Functional:** power interrupt, BOS comms, software distribution — ~6.
- **HMI Screen Validation:** per-screen from the UX images (Validation screens + Technician Menu).
- **Smoke** + **Regression** (fold `Fixes/Changes`).

UX assets: `knowledge/flows/pv/` has the **Validation** screens (Present SmartCard/Barcode, Not Valid
At This Location, Invalid Time Of Day, Product Expired, Represent Card, Unable to Validate, Passback
Journeys Left, Machine Not in Service) + **Technician Menu** screens. No Overflow flow-data JSON, so
the **old suite is the behaviour source**; UX images drive the HMI layer.
