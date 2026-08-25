# FBD-100358 — Activity Log & Shift Viewer (distilled)

**Source:** `FBD-100358 Activity Log and Shift Viewer Specification V4.00` (7 Feb 2023, S. James).
Distilled testable facts only — raw spec held locally, not committed.

## What it is
- Two CloudFare sub-modules for viewing device-generated **audit data** (REQ-0665, REQ-1744). **Activity Log** = broad multi-filter search; **Shift Viewer** = all activity within one driver's shift/duty.
- Results scoped by selected operating company: a device is included if its **home location is beneath the selected operator** in the hierarchy.

## Activity Log search rules (testable)
- Two primary filters, **at least one mandatory**: **Activity** (mandatory if Device Type not set) and **Device Type** (mandatory if Activity not set). **Date & Time range always mandatory.**
- **Date range max = 7 continuous days** (default = current day). >7 days → warning, **no results shown**.
- Selecting a device type not in the estate → **no results** (not an error).
- Optional per-device-type string filters: Device ID, Vehicle ID, Staff Member, Product, Service, Stage, Stop, **Barcode ID** (Flowbird multi-use + mLink multi-use w/ defined barcode ID only). Empty field = no filter on that item. Filter-applicability matrix matters, e.g. **Product filter only applies to Transaction/Annulment**; Barcode ID only to Transaction/Annulment; Service applies to journeys/stops/inspection/defect/break.
- Results are chronological, toggle newest↔oldest; standard summary fields always shown: **Device Type, Device ID, Operating Company, Activity, Date/Time, Fleet ID** (where applicable). Rows expand for detail.

## Activity types + sources (assert the taxonomy)
- **Transaction** (all devices): ticket sale, smartcard issue/topup/validate, Flowbird/mLink **multi-use** barcode validate, payment-card tap.
- **Event** (all devices, device-initiated): operational/error events **and transactions NOT recorded in MERIT** — explicitly incl. **Corethree single-use barcode redemptions**. (Key: single-use barcode ≠ MERIT transaction.)
- Transaction Annulment, Start/End of Shift, Start/End of Journey (attended / ETM+Glider HHD), Stop Arrival, Stop Departure, Operator Event, Device Status, Device Registration, Inspection (ETM), Defect (ETM), Driver Break, Peripheral Device, Software Version.
- **Annulment display:** annulled transaction shows **summary total changed to £0.00** but the **expanded Fare keeps the original value**; annulment row shows cancellation ticket number + **negative fare**.
- **Stop Arrival/Departure:** GPS vs manual — "(Manual)" appended to activity; if manual OR no schedule-adherence, **Scheduled/Early fields = N/A**.
- **End of Shift / End of Journey** expanded view carries the money detail: net (minus annulments) **Shift/Journey Cash Total in Sterling** (alt currencies converted), plus per **PaymentType+CurrencyCode** breakdown (Currency Total/Annul, Transaction Count/Annul), **Sign Off Mode** (manual vs inactivity timeout), ticket/pass totals, **Device Cash Total** (since commissioning).
- **Device Status messages are purged after 24 months** — not viewable in Activity Log/Shift Viewer beyond that.

## Shift Viewer + export
- Shift Viewer: pick Staff (from operator hierarchy) + Date → lists shifts for that date/driver (alert if none); **one shift at a time**; Search shows all in-shift activity, expandable as per Activity Log.
- **Export (.xlsx)**: both modules export summary or expanded view. **Activity Log download only enabled when: ≤1 day selected AND at least one of Device ID / Staff ID / Vehicle ID is non-empty.** Expanded export puts summary line bold + each datum on its own row.

## Suite implications (BOS/Merit reporting)
- Assert **7-day cap** + **at-least-one-of-Activity/Device-Type** validation and the **out-of-estate device → empty (not error)** case.
- Assert the **Corethree single-use barcode → "Event" (not MERIT transaction)** rule vs multi-use → "Transaction" — ties to FBD-100167 device matrix.
- Assert **annulment display** (summary £0.00, expanded original fare retained, negative annul row) and **net-of-annulment shift/journey cash totals** with alt-currency conversion — mirrors Operator Totals API (FBD-100276), good cross-check.
- Assert **Stop Arrival/Departure manual→N/A** and GPS-vs-manual "(Manual)" tag.
- Assert **export enable conditions** and the **24-month Device Status purge** boundary.
- Gap: filter-applicability matrix (which filter works on which activity) is broad and likely under-covered.
