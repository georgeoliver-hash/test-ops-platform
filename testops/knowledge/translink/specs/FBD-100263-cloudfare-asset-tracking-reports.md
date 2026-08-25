# FBD-100263 — CloudFare Asset Tracking Reports (distilled)

**Source:** `CloudFare - Asset Tracking Reports (FBD-100263) V4.00` (8 Mar 2021, Flowbird) + Depot Location / Devices Last Seen / Operator report examples.
Distilled testable facts only — raw spec held locally, not committed.

## Common rules (all reports)
- Accessed via CloudFare **Reports page → "Assets" sub-menu**. Data is scoped to the **currently selected operator in the hierarchy** and filtered by **user claims** (hierarchical: child operators/depots included; only devices "owned" by that company).
- Device-type filter = multi-tick over **HHD, ETM, POS, BV, GV, PV, TVM**; **nil selection = all types**. Output is **.xlsx** download. Date ranges cap at **31 consecutive days** (single continuous period: from-time on day 1, to-time on last day). Fulfils REQ-2499.x.
- **Device location convention** (recurring across reports): for **PV/TVM/GV** = programmed physical station/stop; for **ETM/BV** = **bus/fleet number**; for **HHD/POS** = programmed home location.

## The three reports (current = v3.0 in each case)
- **Depot Location Report** (REQ-2499.1): assets seen at a location in a date range. One entry per home location → per-day-per-device sub-entries. **A device that moves home location on the same day appears under BOTH.** v3.0 adds Device Status (in service / degraded / out of service / locked / blocked), Category, last-known staff, and sub-component IDs (Bank Note Recycler/Coin Vault/EMV Pin Pad→TVM; Barcode Reader→ETM/GV/POS; HHD Printer + Miura M020→HHD; SIM→HHD/ETM/TVM/PV/POS; Terminal ID all; Tray ID for ETM/BV/POS/GV, Pedestal ID for PV).
- **Staff Activity Report** (v3.0, was "Operator Report", REQ-2499.2): staff↔device interactions. Filters cascade: **Company → Staff Home Location → Staff ID**. Activity enum: operator/supervisor/technician/administrator/cash-collector/stock-manager **sign on & sign off**, plus **Inspection event**. Rows ranked by least-recent comms.
- **Devices Last Seen Report** (REQ-2499.3): per-device comms summary. **Single date/time, NOT a range.** Fields incl. Device Status, Category, Operator, **Last Communication** (last successful comms of any type) and **Last Transaction** (last successful txn submission — **annulments count as transactions**), Installation Point ID, Software Version, sub-component IDs. **Sub-component data reflects most-recent status only** — stale for long-silent devices.

## Blacklist & exceptions (not reports)
- **Blacklist (REQ-2499.0/.5):** two new Estate-Manager status categories **Lost/Stolen** and **Decommissioned**, assignable from Device Details, filterable, CSV-exportable from Asset Manager / Comms Monitor / Command Viewer.
- **Exceptions:** (1) enhanced **"Hours since last communication" dashboard tile** — adds a **Company** filter (name always visible), **Location/Fleet ID** column (ETM/BV show Fleet ID), and a **Depot** column; the device list acts as a count. (2) enhanced **Staff Activity Report** flags **concurrent ShiftStart/JourneyStart for the same driver on different devices** (fraud signal).

## Suite implications (asset/BOS side)
- Assert the **device-location convention** (fleet number for ETM/BV vs physical stop for PV/TVM/GV vs home location for HHD/POS) — easy to regress and used everywhere.
- Assert **31-day cap** enforcement and **user-claims scoping** (device not owned / outside hierarchy is excluded).
- Assert **Last Transaction includes annulments** and **Last Communication = any comms**; Devices Last Seen is single-instant not range.
- Assert **same-day home-location move → device in both** (Depot Location Report) and **concurrent shift/journey fraud flag** (Staff Activity).
- Assert **Lost/Stolen & Decommissioned** categories flow to the Estate-Manager filters + CSV export.
- Gap: sub-component staleness caveat (long-silent devices show old sub-component associations) is a subtle correctness note unlikely to be tested.
