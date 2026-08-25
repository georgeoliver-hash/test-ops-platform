# FBD-100306 — Merit Web Reports Viewer (distilled)

**Source:** `Merit Web Specification (FBD-100306) V3.00` (18 Aug 2021, A. Di Re / S. James).
Distilled testable facts only — raw spec held locally, not committed.
Related: Translink Merit 3 FRS, CONOPS §N19.

## What it is
- A **browser front-end onto the existing Merit reporting system** (evolution of Merit 5), giving depots daily reports **without loading CloudFare**. Reuses existing Merit DBs + stored procedures — **report content is unchanged**, only exposed via web.
- Accessed from the **CloudFare launch page → Business Intelligence button**; requires the **Translink corporate network** to load the GUI.

## Access / hosting rules (testable)
- **Auth is mandatory** — username/password + the report data must not be reachable by URL alone. Users added manually by Translink via an **Active Directory security group**.
- **Location Restrictions Editor** controls per-depot data access; existing permissions carry over.
- Under CloudFare SaaS, **Merit Web is NOT migrated to cloud** — stays as originally provided. No extra licensing; unlimited authorised users. Admins still use the **Merit client** for settings/editors.
- **"Saved Selector" functionality is OUT of scope**; everything else in the existing Merit reports is included.

## Viewer behaviour worth asserting
- Left panel = parameter selection; right = display; header = run/view/print.
- Parameter controls: single + multi-select (Shift/Ctrl), **Add All / Remove All**, expand/collapse sections, **Reset** (returns to initial parameter page), **Run**, and **exclude-zero-values** toggle.
- After run: export as **PDF, CSV, Excel 97-2003, RTF, TIFF, Web Archive**; Print View; magnify; page scroll; in-report search.
- **Day Type**: some reports filter by it; others are pre-configured to **Traffic** or **Operational** (where both apply it's selectable).
- **Report Type** summary/detailed drill: Head Office+Detailed → breakdown by company; Company+Detailed → by depot; Depot+Detailed → no further breakdown.
- Class/Route Breakdown reports add radio buttons to switch classes↔class-groups (and routes↔route-groups), then Summary vs Detailed grouping.
- Parameters list (Buses, Date, Devices, Location, Payments, Product Class, Report Type, Routes, Staff, Timebands) are **shared across all Web-Merit reports, not just Translink bespoke ones**. Timebands: configurable start/end, savable as Groups, reusable.

## Report set provided
Pay-In Reconciliation (Summary/Detailed), Class Breakdown (=Class Audit), Route Breakdown (=Route Audit), Sales Breakdown by Driver, by Route/Class (Summary+Detailed), by Class, Sales Analysis by Class, Daily Audit / Daily Audit by Trip / by Module, Daily Summary, Driver Activity (incl. **alighting stage names for concession smartpasses**), Driver Shift, Duty Comparison, Annulled Tickets, Inspector's Report.
- Note: **Pay-In Reconciliation location filter is present but not useful** (no pay-in location in the new system).

## Suite implications (BOS/Merit reporting)
- Assert **auth gate** (no data via bare URL) and **depot location restriction** — security-relevant, likely coverage-worthy.
- Assert viewer mechanics that change results, not cosmetics: **exclude-zero-values**, **Add All/Remove All**, **Reset**, Summary↔Detailed drill (Head Office→company→depot), and the class/route-group toggles.
- Assert **Day Type = Traffic vs Operational** pre-config per report where it drives figures.
- These are existing Merit reports — coverage here should focus on **web-viewer wiring + access control**, not re-testing report maths (owned by Merit FRS).
