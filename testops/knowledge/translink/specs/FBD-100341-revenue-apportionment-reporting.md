# FBD-100341 — Revenue Apportionment & Reporting (TVM & POS) (distilled)

**Source:** `FBD-100341 Revenue Apportionment & Reporting (TVM & POS) Specification V1.00` (13 Dec 2021, S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Requirements: REQ-2121.0–.6. Note: several drivers were "discussed but not-yet-approved" and may become a scope change.

## Core distinction — two separate location concepts
- **Cash/card reconciliation** uses the **device home (physical/geographical) location** (e.g. POS in Ulsterbus Omagh = OM, POS in NIR Botanic = BT). Treasury reconciles TVMs by **individual serial number**.
- **Management-information (MERIT) reporting** uses the **location derived from the transaction's route mode/company**, NOT the device home location. (A rail ticket sold on an Ulsterbus TVM → allocated to NIR; an Ulsterbus ticket sold on a Rail POS → allocated to Ulsterbus.) Bus sales are then further split to an individual bus/Metro depot by route.

## Device-based reallocation — TVM presets
- A **preset ticket on a TVM has no route**, so revenue location is ambiguous. To avoid disadvantaging an operator, the TVM assigns a route by:
  1. Use the **route of the previous transaction** — **unless** there is no rule assignment for that route's operator + the selected preset product.
  2. If (1) doesn't populate, use the **first available route assigned at the operator level** of the preset's rule assignment.
- **Example 1:** prev sale = Ulsterbus route 652; next = bus Family & Friends Day Ticket (has Ulsterbus rule assignment) → preset audited with **route 652**.
- **Example 2:** prev sale = Ulsterbus route 652; next = **rail** Family & Friends preset (no Ulsterbus rule assignment, rule sits at NIR level) → preset audited with route reference **'Rail'**.

## CloudFare MERIT-location mapping (route operating unit + equipment type)
CloudFare adjusts data before it reaches MERIT, keyed on the route's operating unit and the sending equipment type:
- **POS:** Metro Bus → `PM`; NIR → `PR`; Ulsterbus → `PU`.
- **TVM:** Metro Bus → `TM`; NIR → `TR`; Ulsterbus → `TU`.
(Route/Depot Allocation Editor code table also lists: CT/CU Collect Tickets, GB Goldline Barcode, MM/MU mLink.)

## Pay-In Reconciliation
- Transactions are **auto-assigned to the device home location** for cash/card reconciliation. The **CloudFare Reporting → Pay-In Reconciliation** report gives cash/card value **by device home location** (used by local depot + head-office staff, since the MERIT report no longer serves this purpose once the route-based mechanism above is live).
- An **extra "device home location" field** is added to the data sent to MERIT — **not used in MERIT** but **synchronised to the Data Warehouse** for additional Translink reports.

## MERIT editors / behaviour
- Existing MERIT reports keep working, but **POS/TVM transactions are associated to the route's depot, not the device's depot**.
- **Pass Revenue Editor** (existing): reallocates revenue to £0.00 smartcard validations by class + card-reference; pass-revenue report fields use it.
- **New "Route Allocation" editor** (under Route Revenue Editor): columns **Route, Location, Generation Factor** (dropdown-selected). Synced to a **new Data Warehouse fact table** so cash reconciliation (original data) and revenue allocation (computed) can both be reported.
- **New "Top Up / Issue Revenue" editor**: columns **Class, Location, Generation Factor**; Class dropdown limited to **card top-up / card-issue classes**. Also synced to a DW fact table.

## Data Warehouse
- Device-home-location field enables a **DW Pay-In Reconciliation** report and a report to **reallocate concessionary fare recovery by device home location**.
- Revenue can be split between depots by **route and/or class** (smartcard top-ups/issues); existing MERIT reports/stored procedures may be re-generated in the DW using the new allocation.

## Smartcard nuance (needs care in allocation)
- Metro Multi-Journey / Travelcards → always allocated to **Metro** in Agresso regardless of selling device.
- Ulsterbus Multi-Journey / Town Service Travelcards → always allocated to **Ulsterbus**.
- **iLink / BVP** cards are integrated (bus + rail) → allocated by **device/company/location** — the tricky case for TVM/POS sales.

## Suite implications (POS suite 30253 + TVM / ABT-BOS)
- This spec is mostly **back-office/reporting**, but drives assertions on the **audit data a POS/TVM emits** — the route/operating-unit that ends up on the transaction is what CloudFare maps to PM/PR/PU (POS) or TM/TR/TU (TVM). Assert the **MERIT-location mapping** end-to-end (sell a rail ticket on an Ulsterbus POS → expect NIR/PR allocation, not device-home).
- **TVM preset route-inheritance** is a concrete device-behaviour test: preset inherits previous transaction's route when a matching operator rule exists, else falls back to operator-level route / 'Rail'. Cover both the inherit and the cross-mode fallback (Examples 1 & 2). Likely a coverage gap.
- Assert the **device-home-location field** is present in the data sent to MERIT/DW (reconciliation path) distinct from the route-based MI allocation.
- Cover **iLink/BVP** integrated-card allocation-by-device vs Metro/Ulsterbus fixed allocation.
- Editors (Route Allocation, Top Up/Issue) are BOS-config, not device tests — note as out-of-POS-suite but relevant for ABT-BOS reconciliation coverage.
