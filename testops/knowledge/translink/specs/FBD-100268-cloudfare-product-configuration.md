# FBD-100268 — CloudFare Product Configuration - Translink (distilled)

**Source:** `CloudFare Product Configuration - Translink (FBD-100268) V2.00` (10 Feb 2021, S. James) — an
Excel matrix of product properties × device type × product type. Distilled testable facts only — raw
spec held locally in `dev/translink-requirements/`, not committed.

> This is a **configuration reference matrix**, not narrative behaviour. It defines, for every product
> property, which **device types** (TVM/ETM/POS/HHD/PV,BV,GV) and **product types** (ABT Create/TopUp,
> BarcodeUse, Change, FLU, Open, Pass, Preset, ReferenceProduct, WTS SmartCreate/Recharge/Transfer/Use)
> it applies to (Yes / NOT USED / N/A). Use it to check a property is set only where it is meaningful.

## Property groupings
Product Details, Audit, Display, Reference, Rule, Search — each holds many named properties with a
Description, a **Device Override** flag, and a **CF Data Input Format** (String(n) / Boolean / Numeric
(Fare|Product Id|Stage Id|Minutes) / Alphanumeric).

## Testable field semantics worth asserting
- **Description** = main product name; used on device (absent Display Description) and in MERIT with **Short Code** + **Reference ID**. **Reference ID** = the MERIT product id that syncs CloudFare↔MERIT.
- **Values in pence:** `Maximum Value`, `Minimum Value` (open-value tickets, ETM/POS only).
- **Count As Pass** (ETM/HHD/PV) → sets pass-count in txn record + device totals. **Count As Passenger** (**ETM only**) → passenger-boarding count on Route Breakdown Report; **excludes WTS Recharge**.
- **Concession Product** → transaction formatted as concession into MERIT. **Reference Product** → product used for validation + full-fare-equivalent (fare-forgone) calc. **Default Fare Foregone** → fallback fare-forgone value when device can't calculate.
- **Passback Time** (minutes) — all devices; delay before same **card** re-tap accepted. **Barcode Passback** (minutes, ETM/HHD/validators) — same for same **barcode**. **Re-validation Time** — validators only; allows POS/TVM-bought concession card to pass a gate within the window.
- **Alternative Product 1–5** — device offers fallbacks in priority order 1→5, skipping any not valid for current time / boarding-alighting combo.
- **Transfer Time** — **PV only** among validators (ETM/HHD = NOT USED); minutes a card still counts as a transfer.
- **Print Barcode** / **Barcode Use** link the printed barcode to its BarcodeUse product; **Group Issue** = shared multi-passenger ticket.
- **Recharge** family (Recharge Allowed/Amount/Type MD·MJ·Days·Months·Pass / Expiry Data/Type / Max Recharge Amount) — WTS Recharge/top-up behaviour.
- **Search / Barcode Search String** — links a Corethree barcode Product Id to a Flowbird product.
- **NOT USED by TVM/HHD:** Card Ticket Expiry Ticket 1/2/3 date type & value (v2.00 change).

## Suite implications
- Use this matrix as an **oracle for config-driven device tests**: a property asserted on a device where the matrix says **NOT USED / N/A** is a likely mis-config (e.g. Transfer Time on ETM, Count As Passenger on POS).
- ABT-relevant: confirm the **"ABT Tap On Only" product** carries the right Audit/Reference fields feeding FBD-100658 fields (product id 7000, fare source) and FBD-100698 fare calls.
- Assert **pence vs pounds** on Maximum/Minimum Value and fares (recurring unit bug; see FBD-100658).
- Assert **Count As Pass / Count As Passenger** flags drive the correct MERIT pass/passenger counts and that **WTS Recharge is excluded** from passenger counts.
- Assert **Passback Time / Barcode Passback / Re-validation Time** windows behave per device class (validators vs POS/TVM).
- Two spreadsheet copies exist (`...(FBD-100268) V2.00.xlsx` and `Cloudfare Product Configuration.xlsx`) — reconcile before treating either as authoritative.
