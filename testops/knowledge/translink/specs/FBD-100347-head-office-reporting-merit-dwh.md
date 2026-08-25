# FBD-100347 — Head Office Reporting through Merit DWH (distilled)

**Source:** `FBD-100347 Head Office Reporting through Merit Data Warehouse Specification v1.00` (6 Dec 2021, C. Kiraz).
Distilled testable facts only — raw spec held locally, not committed.
Related: FBD-100356 (DWH Solution), FBD-100306 (Merit Web), FBD-100387 (ABT Reporting).

## Scope
- Defines the **schedule-adherence report set** Head Office users build in **Power BI** off the DWH. All values come from **`FactScheduleAdherence`** joined to schedule/date/time/route/journey/geo/staff dimensions. **Report file format is Power BI's responsibility, not Flowbird's** (constraint) — do not assert on file type.
- Head Office sees **all** data; regional/depot users see only their own (access set in DWH admin + Power BI). Report calc scripts are **Translink's** responsibility; Flowbird assists.

## The reports (each = candidate coverage item)
Two families, both fed from `FactScheduleAdherence`:
- **Headway (REQ-2838.x):** Change (stages with most headway delay), Monitor (all stages, trips >x min behind vehicle in front), Waiting Time (avg wait mins/secs per stage + weekly avg).
- **Schedule (REQ-2848.x):** Company Reliability Graphical, Company Reliability Detailed, Missing Data, Depot Summary, Route Analysis, Driver Summary, Timing Point Analysis, Variation Against Time Point, Journey-by-Timing-Point Graphical, Route-by-Timing-Point Graphical.

## Rules worth asserting
- **Fixed parameter:** all headway/schedule reports use **Date Type = Operational Date** (not traffic/calendar).
- **Selectable filters** (common set): Date range, Days of week, Timeband, Company/Location, Route(s), Journey(s), Direction, plus **Early** and **Late** thresholds in minutes vs schedule; headway reports add **Headway Greater-than-x**.
- **Early/late % is computed per individual timing point visited** (arrived early/late at each), not per journey — a recurring constraint across reports.
- **Missing Data Report** must surface both directions of inconsistency: **scheduled journey with no GPS actual**, and **actual journey with no schedule**; each row gives Operating Date, Route, Journey, Direction, and a **missing-description** (e.g. "Stage 6 missing", "All stage data missing", "Schedule missing").
- **Depot Summary / Route Analysis** bucket timing points into fixed bands: **>5 early, 3–5 early, 1–3 early, on-time, 1–3 late, 3–5 late, >5 late**.
- **Driver Summary / Timing Point Analysis** use **>1 min early** and **>5 min late** as the early/late cut points; sortable best-to-worst.
- **Company Reliability Detailed** row per location: total scheduled timing points, % early, % late, **% with no GPS actual**, % outside criteria, % inside criteria, + company average.
- Key DWH mapping: filters map to `FactScheduleAdherence` date/time/route/journey/geo keys; early/late derived from the **8 Arrival/Departure vs Expected Arrival/Departure Date+Time keys**; **counts/percentages are calculated at query time from row counts** (not stored).

## Constraints (don't over-assert)
- Report file formats and dashboard build are Power BI-side (out of Flowbird scope). Latency depends on DWH sync (see FBD-100356). Schema shifts if Schedule Adherence data model changes.
- Dashboard (REQ-3585/3586): default configurable per-user KPI dashboard, saved per login, must be performant for non-power-users — "subject to detailed design", so treat as advisory not testable-yet.

## Suite implications (BOS/Merit reporting)
- Treat each report as a **coverage row**: given a fixture of schedule-adherence data, assert the report's derived fields (early/late bucket %, missing-data descriptions, driver/timing-point rankings) match expected — these are pre-calculated in TFTS so they are a genuine regression surface.
- Assert **Operational-Date** basis and the **>1 early / >5 late** thresholds explicitly (easy to get wrong).
- Assert **Missing Data Report both-way detection** (no-GPS and no-schedule).
- Do **not** write cases asserting export file type — out of scope.
- Gap: end-to-end (device GPS/stop event → `FactScheduleAdherence` → report value) is the high-value, likely-missing flow.
