# ABT / CloudFare Configuration — spec-grounding changelog

Re-grounds the CloudFare *configuration* cases in `suite_ABT.json` against the real Flowbird TFTS
specs. No behaviour was invented; every screen/field name is either cited to a spec paragraph or
marked `GAP` / `UNCONFIRMED`.

**Status (2026-07-21): this file already used the correct `{"content","expected"}` step schema (not
the buggy `{"when","then"}` shorthand found in `admin.rewrite.json`), so its cases were never among
the 51 blank-step cases found in the 2026-07-17 partial push. Verified directly against the live
suite: 0 blank-step cases from this file at any point. Properly (re-)pushed 2026-07-21 alongside the
admin/backoffice/correction batch via the same, now-hardened `tools/apply_rewrite.py` (which now
also refuses to push any blank step outright). See
`proposals/coherence-audit/fixes/abt-blank-steps-fix.changelog.md` for the full writeup.**

## Scope
Sections worked (49 cases): Products (15), Route Management (6), Setup & Import (5), Rules (3),
Asset Manager (3), Device Dataset Deployment (3), Station Manager (3), Configuration & Setup (3),
Card Data (3), Stored Procedures (3), Import & Export (2).

## Governing specs consulted (newest non-Archive)
- **FBD-100268** CloudFare Product Configuration – Translink V2.00 (product data dictionary + product types)
- **FBD-100698** ABT and CloudFare Topology Usage v0.04 (ABT/fares-engine usage, capping base products)
- **FBD-100296** Stop, Route & Service Management in CloudFare V6.00 (module/screen names, route mgmt)
- **FBD-100229** CloudFare Zone Configuration V3.00 (zones, overlap, Zone Settings)
- **FBD-100385** CloudFare Configuration Data Exports V2.00 (export functions, Reports module)
- **FBD-100293** Product Group Usage V3.01 (Products menu, Product Groups, FLU/Menu/Toggle/Numeric)
- **FBD-100263** CloudFare Asset Tracking Reports V4.00 (Asset Manager, Device Details page)
- **FBD-100260** Product Name Usage V2.00, **FBD-100320/100353** TID Management — consulted; not load-bearing for these cases.

## Outcome by action
- **grounded-edit: 16** — screen/field names corrected to spec and cited; behaviour verified.
- **unconfirmed: 18** — behaviour partially specified or on an unverified surface; kept and marked `**UNCONFIRMED**`.
- **gap: 15** — no governing spec covers the feature; kept and marked `**GAP**`.

Grounded vs unconfirmed (of the 34 in-scope CloudFare cases): **16 grounded / 18 unconfirmed**.
The 15 gaps are almost entirely out-of-scope surfaces (Smartrack, Merit DWH, Station Manager,
Device Dataset Deployment) that have no spec in the library at all.

## Cross-cutting corrections applied
1. **Screen label normalised.** The invented variant **"CloudFare Topology Management page"**
   (cases 4102994–4102999, 4103003) → **"Topology & Fares Management module"**, the spec's real name
   (FBD-100296 §138, §161).
2. **"Device Information page" → "Device Details page"** (FBD-100263 §418) for Asset Manager cases.
3. **"passback period" → "Passback Time"** (the actual field, in minutes — FBD-100268 §50).
4. **Product types reconciled to FBD-100268's columns**: ABT Create/TopUp, BarcodeUse, Change, FLU,
   Open, Pass, Preset, ReferenceProduct, WTS SmartCreate/Recharge/Transfer/Use. "Excess" and
   "Preset Reverse FLU" are **not** columns → re-grounded / marked UNCONFIRMED.
5. **Route controls named exactly**: Create New Route / Add Route, Copy Route ("-copy", same service),
   Edit Route Attributes, Delete Route (3-dot menu) — FBD-100296 §230–287.
6. **Import Map Point File** success fields named: **Stops Added / Stops Updated** (FBD-100296 §167,189,201).
7. **Titles** rewritten to `<Feature> — <observable behaviour>`; `preconds`/`steps` moved to
   GIVEN state-only / WHEN action / THEN observable, one clause per line, per `docs/gherkin-standard.md`.

## Per-case notes
See each case's `change_note` and `gaps` fields in `cloudfare-config.rewrite.json`. Gap questions are
collated in `cloudfare-config.gaps.md` for the engineer Q&A loop.
