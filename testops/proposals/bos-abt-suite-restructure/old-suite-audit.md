# BOS & ABT — old-suite audit (evidence base)

Audit-first foundation for rebuilding into **`**NEW** BOS & ABT Suite` (suite 30279)**.
Recorded 2026-06-23. Read-only against all sources; no TestRail writes yet.

## Sources

| Suite | id | Role | Size |
|---|---|---|---|
| `2.1-Backoffice Systems - Acceptance Suite` | **14441** | OLD SOURCE (mine + consolidate) | **1,766 cases / 257 sections** |
| `2.1-Backoffice Systems - ABT DO NOT USE for Testing` | **16275** | ABT reference (read for coverage; not a run target) | 169 cases / 19 sections |
| `**NEW** BOS & ABT Suite` | **30279** | TARGET (build here) | 0 cases (fresh) |

Plus the **colleague's spreadsheet** (regression + reporting focus, simulated taps → ABT process →
capping) → to be dropped in `knowledge/ABT/`. Awaited; it defines the priority/scope slice.

## What this suite IS (and how it differs from the device suites)

This is **back-office / web-portal** testing, not device-driven. Six systems live in the old source:

| Top section (14441) | Cases | What it is |
|---|---|---|
| **Cloudfare** | 848 | The BOS platform: sign-on, Topology & Fares, Estate Management, Reports, Settings, Ticket Editor, Dashboard, Events & Alerts, API, Roles. Incl. **`Fixes/New Features` 526** = regression organised by release (V142→V220, TMS). |
| **ABT** | 515 | Account-Based Ticketing: Operator Web Portal (Reports Mgmt 81, Customers 35, **Capping Rules 11 + Capping Groups 7**), Passenger Web Portal, Processing Taps (Card Verification, Late Taps), Debt Recovery, End-to-End. Incl. `Fixes/New Features` 317 = release regression. |
| **Merit** | 178 | Reporting engine: Analysis/Translink/NIR Revenue/Concessionary/Daily/Ticketing reports, Synchronisation, Stored Procedures. |
| **Merit Web Reporter** | 77 | Web report viewer (per-report cases). |
| **Smartrack** | 40 | Card-data system: reports, display card data, imports/exports. |
| **Delete** | 108 | A bin (SAAS migration, exploratory, Power BI, dupes). **OUT of scope** — do not carry over. |

### devtype evidence (proves it's its own capability suite — not POS/ETM/PV)
Mirrored from real cases (trust stored values, NOT the field-definition option ordinals — known gotcha):
- `[100]` = 713 → **BOS / CloudFare**
- `[200]` = 516 → **ABT**
- `[151]` = 183, `[152]` = 27 → **Merit / Smartrack family**
- `[]` = 266 → untyped (assign on rebuild)
- mixed (`[25,100]`, `[5,100]`, `[1,100]`…) = genuinely cross-device (device + BOS) — candidate **E2E**.

### Push schema (confirmed live via discover-fields on C2679063)
- `template_id: 1`, `custom_autoconfirmation: false`, `custom_revstatus: 3` (Approved).
- `custom_devtypes`: **per-area** — BOS=`[100]`, ABT=`[200]`, Merit=`[151]`, Smartrack=`[152]` (confirm
  per section from cases.json before each push; mirror real values).
- discover-fields flags `custom_automation_script` / `custom_qualproc` / `custom_bdcreqdocs` as
  REQUIRED, but real cases leave them empty → **do not set** (same lesson as POS/ETM/PV).
- **House style of the old cases:** Gherkin lives in a single `custom_steps` Text field as
  `**GIVEN**/**AND**` (no separated steps, no preface). The **new** suite adopts our standard
  (preface "This test is to confirm", `custom_preconds` GIVEN, `custom_steps_seperated` WHEN/THEN,
  `custom_expected` prose) so it matches POS/ETM/PV and passes the conformance audit.

## Big consolidation opportunities (the POS/ETM/PV playbook applies)

1. **Regression-by-version → fold by feature.** CloudFare `Fixes/New Features` 526 + ABT 317 = **843
   cases organised by release** (V142…V220, V1.2.x, TMS). Same pattern as the POS "Confirmation Tests"
   / ETM "Regression Defects": fold each into the functional case that owns the behaviour, linked via
   **Refs** (defect/version id); a dedicated `@regression` case only where nothing covers it. Expect a
   large shrink here.
2. **Reporting is first-class and spread across 4 systems** (CloudFare Reports 30, Merit 178, Merit
   Web Reporter 77, ABT Reports Mgmt 81). George flagged **reporting** as a priority. Consolidate into
   a clear Reporting area per system; per-report cases stay distinct (each report = a distinct
   function, like HMI per-screen — NOT over-folded).
3. **Capping** (ABT Capping Rules 11 + Groups 7) is a core ABT behaviour set — keep as an explicit
   ABT/Capping feature; the spreadsheet's tap→cap scenarios extend it.
4. **Delete section (108) + "Non-relevant tests" (14) = exclude.**
5. **ABT reference suite 16275** has structured Operator/Passenger Web Portal + Card Verification +
   Debt Recovery + Late Taps + Regression cases — read for COVERAGE (its "Spreadsheet Tests" 24 +
   "Product Specification Document" 24 hint at the spreadsheet's origin) but it's `DO NOT USE` as a run
   target. Mine it to make sure the new ABT area is complete.

## Test-ownership principle (recorded per George's question, 2026-06-23)

Device suites (POS/ETM/PV) keep a **light** audit step ("event recorded in CloudFare activity log /
MERIT") — that verifies the device→BOS *pipe*. This BOS & ABT suite owns the **deep** back-office
verification (capping maths, report contents/totals, reconciliation, debt recovery, account/portal
behaviour). They are complementary layers, **not duplication**. End-to-end "device action → back-office
outcome" cases live **once here**, cross-referenced to the device case via Refs — never copied into both.

## Open decisions (need George / the spreadsheet before authoring)

1. **Scope:** all 5 live systems (CloudFare, ABT, Merit, Merit Web Reporter, Smartrack) in this one
   suite, or a subset? (Name "BOS & ABT" suggests all back-office + ABT; Delete bin out.)
2. **Spreadsheet role:** is it the *priority slice* (the regression + reporting tests to build first),
   or the full intended scope? Where do its rows map (ABT capping/taps? Reporting?)
3. **Structure sign-off** (see `structure.md`).
4. **Run Configurations / modes** — any (e.g. Glider vs NIR for ABT reports), or single-config?
