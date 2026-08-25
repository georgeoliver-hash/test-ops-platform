# BOS & ABT Suite (30279) — build complete

Rebuilt from old suite `2.1-Backoffice Systems - Acceptance Suite` (14441, 1,766 cases) + the
UB-TOO tracker spreadsheet, in house style (feature-first sections, concise titles, intent-level
Gherkin, defects in Refs). **365 active cases, audit CLEAN, all enriched.**

## Final shape (365 active)

| System (devtype) | Cases | Areas |
|---|---|---|
| **ABT** [200] | 190 | Tap Correction (Metro/Zonal/Reference/Uncapped/Town Service), Annulment & Re-tap, Duplicate Detection, Journey History, Update Stop List, Debt Recovery, End to End, Operator Web Portal (Sign On/Customers/Reports/Capping Config/Admin Settings), Passenger Web Portal, Processing Taps, Configuration & Setup |
| **CloudFare** [100] | 110 | Sign On & Access, Roles & Profiles, Settings, API, Topology & Fares (Setup/Drawing Tool/Route Mgmt/Products/Rules/Card Ref File/Labeling), Estate Management (Activity Log/Asset Mgr/Comms Monitor/Dataset Deployment/Staff Mgr/Quarantine/Commands), Reports, Events & Alerts, Dashboard, Ticket Editor, Station Manager |
| **Merit** [151] | 50 | Administration, Analysis Reports, Revenue Performance Reports, Concessionary, Daily, Distance, Stored Procedures, Synchronisation & Tools |
| **Merit Web Reporter** [151] | 2 | Report Viewer |
| **Smartrack** [152] | 13 | Access, Card Data, Import & Export, Reports |

Consolidated ~1,658 old non-Delete cases → 365 (the report catalogues kept one case per distinct
report; Summary/Detailed/Grouping/Direction-of-Travel presentation variants and per-device
duplication folded; out-of-scope and the `Delete` bin dropped).

## George's TestRail UI actions (API can't do these)
1. **Bin the 99 `ZZ_DELETE_REVIEW` cases** (the first-cut ABT cases, superseded by the rebuilt
   `abt-functional.cases.yaml`). Sort by title in 30279, multi-select the ZZ block, delete.
2. **Set up Run Configurations** if the suite is run per operating mode (Metro / Ulsterbus, and
   Glider / NIR where relevant for ABT).

## Known follow-ups (optional, honest gaps)
- **Version-regression fold-Refs not applied.** The old suite's `Fixes/New Features` trees
  (CloudFare 526 + ABT 317 = 843 release-regression cases, e.g. V142–V220) were **excluded** from the
  rebuild — their *behaviours* are covered by the functional cases, but the specific defect IDs are
  not yet linked as Refs on the owning cases. A regression-fold pass (map each defect → owning case,
  add Ref) would complete traceability, as offered on the other suites.
- **Title-level coverage sweep.** The build was area/section-driven; a full case-title sweep of all
  1,766 old cases (as done for PV) would catch any hidden title-level behaviour. Minor items
  knowingly deferred: old `Tickets` (2) and a couple of `Settings/Topology` amend-zone cases folded
  into Topology.
- **BOS login** (read-only, test env) would let coverage be verified against the live CloudFare/Merit
  systems rather than mined from the old suite.

## Automation handoff
`export-automation` backlog at `reports/tfts-system-test/new-bos-abt-suite/<date>/automation-backlog.json`:
**217 fully + 136 partially automatable** (4 destructive). NOTE: these are web-portal/back-office
cases — Playwright-automatable, a different harness from the ADB/Appium device tests in
`automation-tests`.
