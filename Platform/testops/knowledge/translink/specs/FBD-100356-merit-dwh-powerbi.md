# FBD-100356 — Merit Cube DWH / Power BI Integration (distilled)

**Source:** `FBD-100356 DWH Solution Specification V1.00` (28 Nov 2025, C. Warnes).
Distilled testable facts only — raw spec held locally, not committed.
Related: FBD-100347 (Head Office Reporting), FBD-100387 (ABT Reporting), FBD-100469 (Back Office Data Integrity Validation), FBD-100306 (Merit Web).

## What the DWH is
- Star-schema SQL Server data warehouse; **read-only analytical store** fed from **Merit DB + device services** via **SSIS**. Reporting is done in **Power BI** (Report Server on-prem + Desktop), provided/managed by Translink.
- DWH holds only synchronised, calculation-free source data; **all headway/schedule-adherence and ABT report values are pre-calculated by Arrive TFTS** and loaded into DWH tables — Power BI just slices them.

## Load / latency / consistency (testable)
- SSIS load runs on a schedule, **default every 10 min** (configurable in SSMS). Expect near-real-time but non-zero latency between source write and DWH availability.
- **Only data that has passed Checks & Validation (REQ-3605) is extracted** (REQ-3608). Extract is incremental — **only new, not-previously-extracted data**, even if Translink deleted+re-imported in the source; empty output if nothing new.
- **Data Correction Editor** (REQ-3609): failed-check rows can be (a) corrected, (b) tagged exception → loaded with **"unknown" dimension keys**, or (c) marked invalid → **blocked from DWH**.
- **Consistency check** via Power Query + an Arrive-supplied SQL query returns missing-row count for a date: **0 = fully synced**; non-zero = investigate. (Assertable in a BOS integrity test.)
- Retention: sized for **500,000 txns/day for 10 years** (REQ-2782). A **manual purge utility** removes passenger-journey/revenue data past a configurable age once it has been imported to long-term storage.

## Schema (the shape tests assert against)
- **4 fact tables:** `FactProductSales` (one row per ticket sale), `FactPassengerJourney` (one row per ticket/pass use — also the ABT fact), `FactJourneyPoints` (per fare-stage arrival/departure), `FactScheduleAdherence` (per fare-stage arrival/departure vs schedule).
- **19 baseline dimensions**, incl. `DimDate, DimTime, DimDevice, DimRoute, DimJourney, DimGeographic, DimLocation, DimProduct, DimPaymentType, DimPaymentReference, DimFare, DimStaff, DimDuty, DimFleet, DimExpectedJourney, DimGenerationFactor, DimChangeTypes, DimContract, DimAuthority`.
- Key mappings (fact→dim, used everywhere): fares are integer minor units; `DimFare/FareKey` holds both **Fare** (paid) and **FullFare** (full-fare equivalent for discounts); **Revenue Adjusted = Fare, NonRevenue Adjusted = FullFare**; `DimPaymentType/Merit3Type` + `Description`; `DimProduct/Merit3ClassNumber` + `LongName`; boarding/alighting via `OriginReferenceGeoKey`/`DestinationReferenceGeoKey` → `DimGeographic/LocationKey`+`Description`.
- **Derived measures are NOT stored** (`N/A` mapping) — computed at query time: **Product Count, Journey Count, Journey Factor, Generated Revenue (= (Revenue+NonRevenue) × Generation Factor), Pass Revenue Factor**.
- Field mappings for the 12 revenue stored procs (`Usp_Bus_Revenue_{Ulsterbus|Metro|Citybus}` + `Usp_Rail_Revenue_NIR`, each ×{base, _PaymentType, _Operational_PaymentType}) are **identical** — same field set per company/mode.

## Access control
- SQL Server auth via **Active Directory** groups; SSAS/SSMS grant DB roles. Data visibility restricted by org sub-set (Bus-only, Rail-only, depot, Head Office, super user, admin — REQ-0535). Standard SQL DB roles apply (db_datareader / db_denydatareader etc.).

## Suite implications (BOS/ABT suite 30279 + Merit)
- Assert the **source→DWH sync latency window** (≤ configured interval, default 10 min) end-to-end: create a txn on device → confirm in Merit → confirm in the correct DWH fact within the window.
- Assert **incremental/clean-only extraction**: delete+re-import in source must NOT duplicate DWH rows; only validated rows land; exception-tagged rows arrive with **unknown dimension keys**; invalid rows are absent.
- Assert the **consistency-check query returns 0** for a controlled dataset (candidate integrity smoke test, ties to FBD-100469).
- Assert **derived measures** (Generated Revenue, Product/Journey Count, Pass Revenue) recompute correctly vs a known fixture — these are query-time, not stored, so they are a real regression surface.
- Assert **role-based data scoping** (Bus-only user cannot see Rail rows, depot user cannot see other depots).
- Gaps: purge-utility age cutoff and the "unknown dimension key" exception path are unlikely to be covered today.
