# FBD-100276 — CloudFare Operator Totals API (distilled)

**Source:** `CloudFare Operator Totals API Specification (FBD-100276) V8.00` (7 May 2021, J. Green / S. James).
Distilled testable facts only — raw spec held locally, not committed.

## What it is
- External **JSON REST GET** endpoint on CloudFare letting an authorised 3rd-party (pay-in machines) pull **per-shift cash totals** so operators pay in the correct "shorts & overs". Replaces the old once-a-day MERIT interface; polled frequently (**~2 min**, tunable). No user interaction.
- Applies to staff using **ETM, HHD, POS**.

## Request (assert validation)
- GET params: **`fromdate`** (mandatory, datetime-offset e.g. `2020-11-30 12:49:00+00:00`), **`todate`** (optional), **`operatorId`** (integer, = staff home location).
- Returns **all shifts that ENDED and were processed** in the window for that operator.
- `operatorId` is an enum of Translink locations (e.g. 1=Translink/TL, 2=Metro/MET, 3=Glider, 4=Ulsterbus/UB, 5=TVM Metro; 10007+ = NIR/UB depot codes). Config data "not finalised" — treat the list as example, assert the plumbing not exact codes.

## Response contract (assert field-by-field)
- Array of shift objects. **Unique record = `ShiftId` + `DeviceSerialNumber`** combination.
- Fields: `StaffId` (usually 6-digit string), `StaffName`, `StaffHomeLocation`, `ShiftLocation`, `ShiftLocationCode` (usually 2-letter), `ShiftId` (**32-bit GUID**), `ShiftSignOnDateTime`, `ShiftSignOffDateTime`, `ShiftSignOffProcessedDateTime` (all date/time-offset strings), `EquipmentTypeGroup`, `DeviceSerialNumber`.
- **`CashTotal` = NET (cash+warrants minus annulments), in PRIMARY currency (Sterling), alt currencies converted in, Int64 minor units** (1105 0 = £110.50). `CashAnnulTotalAmount` similarly net-of-nothing = total annulled in Sterling.
- **`AlternativeCurrencies[]`** array, one entry per currency used in the shift: `PaymentType`, `CurrencyCode` (ISO 4217), `CurrencyTotal` (net), `CurrencyAnnulTotal`, `TransactionCount` (net = total minus annuls), `TransactionAnnulCount`. Dual-currency shift → multiple entries (e.g. GBP + EUR).
- **`EquipmentTypeGroup` alias map:** Ticket Machine=ETM, Ticket Vending Machine=TVM, Point of Sale=POS, Bus Validator=BV, Platform Validator=PV, Gate Validator=GV, Handheld Device=HHD.

## Suite implications (BOS/Merit reporting)
- Assert **net-vs-gross**: `CashTotal` and `CurrencyTotal` are net of annulments; annul totals reported separately — a common off-by-annulment bug.
- Assert **only ended+processed shifts** in `[fromdate,todate)` are returned (open shifts excluded); `todate` omitted → up to now.
- Assert **alt-currency conversion into Sterling** for `CashTotal` while `AlternativeCurrencies[]` keeps native amounts (GBP+EUR dual-currency case).
- Assert **`ShiftId`+`DeviceSerialNumber`** uniqueness and `EquipmentTypeGroup` alias for ETM/HHD/POS.
- Assert `ShiftId` is a GUID and datetimes carry offset; integer money is **minor units**.
- Gap: auth mechanism for the 3rd-party caller is referenced but unspecified here — confirm it's covered by a security/API contract case.
