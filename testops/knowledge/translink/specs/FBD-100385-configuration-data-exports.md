# FBD-100385 — CloudFare Configuration Data Exports (distilled)

**Source:** `CloudFare Configuration Data Exports Specification (FBD-100385) V2.00` (24 Feb 2022, S. James).
Distilled testable facts only — raw spec + CSV examples held locally in `dev/translink-requirements/`, not committed.
Related: FBD-100296 (Stop/Route/Service Mgmt), FBD-100336 (Fares List File Export).

## Scope — config exports only
Covers **configuration** exports from CloudFare, all under **Reports module → Topology submodule → Report Selection**. Does NOT cover asset-tracking or transactional exports. Each report has download + reset-filter buttons (reset is a no-op where noted).

## Hierarchy & ordering rules (apply to every report)
- Contents are scoped to the **currently selected level of the Operator Hierarchy** (see FBD-100383). Reports include what is visible at that level "or lower".
- Rows sorted **alphabetically** by the report's primary name column.
- **CSV comma-safety:** any field containing a comma is wrapped in double quotes so the CSV stays well-formed.

## Reports and their columns
- **Map Point Export** — stage details, GPS coords, stop direction (detail in FBD-100296).
- **Rules Report** (no parameters) — two sections: (1) Rule Name, Rule Statements; (2) Time Rule Name, Time From/To (`HH:MM`), Date From/To (`DD:MM:YYYY`), Days of Week (`Mon`/`Tue`…). Alphabetical by rule name.
- **Concise Area & Reference Fare Report** (no parameters) — one section per area, each split into 3 subsections: (a) Ref Fare → Used by service/routes (`<Service>/<Route>, <Route>` e.g. `600/600 (IN), 600 (OUT)`) → Reference tables; (b) Product Name → Rule Name (rule assignments per product in area); (c) Used by services. Alphabetical by area name.
- **Fares List Export** — separate spec FBD-100336.
- **Route List Report** (no parameters) — Route Name, Printed Route Name (=`Public Route Code`), Direction, Service Name, Service Description, **Service Classification** (=`Service Code`, one per service — see FBD-100377). Alphabetical by route name.
- **Product List Report** — one filter: **Device Type** (`All` default, or one of BV/ETM/GV/HHD/POS/PV/TVM). Columns: Product Name (=`Product Description`), Product Short Name (=`Short Code`), Product Type, Operator Name (hierarchy level product configured at), Product Categories (Passenger Type, Travel Type, Passenger Class), Product Disabled (one column per device type that any product populates), Product Settings (one column per default setting + device-override columns). **Override columns named `<Setting> [<DeviceType>]`** (e.g. `Annul Allowed [ETM]`); device columns ordered alphabetically (BV before ETM). Settings that reference another product display the referenced product's name. Filtered to a device type → all default settings shown but disabled/override columns limited to that device type, and only present if ≥1 product configures them. Alphabetical by product name.
- **Product to Ticket Assignment Report** (no parameters) — Product Name, Device Type (full name e.g. `Handheld Device`, `Ticket Machine`), Ticket Template, Operator Level, Enabled (`Yes`/`No`). Alphabetical by product name, then by equipment type on ties.

## Device-type abbreviations (fixed)
BV=Bus Validator, ETM=Ticket Machine, GV=Gate Validator, HHD=Handheld Device, POS=Point of Sale, PV=Platform Validator, TVM=Ticket Vending Machine.

## Suite implications (BOS/ABT suite 30279 + device config)
- These are **portal/config-export** cases (not device runtime). Assert each report: correct columns in order, alphabetical sort, hierarchy scoping (data at selected level "or lower" only), and CSV comma-quoting.
- **Product List Report** device-type filter is the highest-value case: `All` vs a single device type must change which Disabled/override columns appear, and override columns must be named `<Setting> [<Device>]` in alphabetical device order.
- Assert **Service Classification** column in Route List traces to the route's Service Code (cross-ref FBD-100377).
- Product-to-ticket **Enabled Yes/No** and Operator Level are testable against known config.
- Export contents are a good **config-drift oracle** — diff export vs expected device config as a regression check.
