# FBD-100387 — ABT Reporting through Merit DWH (distilled)

**Source:** `FBD-100387 ABT Reporting Data Warehouse Specification v1.00` (2 Dec 2021, C. Kiraz).
Distilled testable facts only — raw spec held locally, not committed.
Related: FBD-100356 (DWH Solution), FBD-100347 (Head Office Reporting).

## Scope / core rules
- ABT (Account Based Ticketing) master data lives in the **ABT Database**; the **reportable subset — only COMPLETED journeys — is synced to Merit + Merit DWH** for BI reporting. **Incomplete/open journeys are NOT in the DWH** (key filtering rule).
- ABT report data is stored in **`FactPassengerJourney`** joined to `DimDevice, DimRoute, DimLocation, DimJourney, DimDate, DimGeographic, DimPaymentType, DimProduct`.
- DWH stores **original transaction detail only, no extra calculations**. Detailed ABT reports are generated via the **CloudFare ABT Portal**; DWH/Power BI is for the transaction-level extract.
- **Special product `ABT Tap On Only`** is the filter used to isolate ABT data in the DWH.
- Export formats (REQ-3457): **PDF, CSV, XLS** (BI-tool dependent). Naming convention `reportType_date(ddMMyyyy).fileExt` (e.g. `ABTReport_28072021.csv`).

## ABT record fields → DWH mapping (assert against these)
- Device: `DeviceId`/`DeviceType` ← `FactPassengerJourney/SalesDeviceKey` → `DimDevice`.
- Route: `RouteName` ← `RouteKey` → `DimRoute`. Location: `LocationCode`/`LocationDescription` ← `LocationKey` → `DimLocation`.
- Journey: `JourneyId`, `DirectionOfTravel` ← `JourneyKey` → `DimJourney`; `JourneyStartDate`/`JourneyEndDate` ← `JourneyStart/EndDateKey` → `DimDate`.
- Boarding/Alighting: `BoardingStageId`/`Name` ← `OriginReferenceGeoKey`; `AlightingStageId`/`Name` ← `DestinationReferenceGeoKey` → `DimGeographic/LocationKey`+`Description`.
- `Fare` ← `FactPassengerJourney/Fare`. `PaymentMethod`/`PaymentDescription` ← `PaymentTypeKey` → `DimPaymentType/Merit3Type`+`Description`. `ProductClassId`/`ProductClassName` ← `ProductKey` → `DimProduct/ProductKey`+`LongName`.

## Suite implications (BOS/ABT suite 30279 + Merit)
- Assert the **completed-journey-only** rule: an open/tap-on-only-without-tap-off ABT journey must **not** appear in the DWH `FactPassengerJourney` extract; once completed, it must.
- Assert the **`ABT Tap On Only` product filter** correctly scopes ABT rows.
- Assert the field-by-field ABT record mapping (device/route/journey/boarding/alighting/fare/payment/product) round-trips from a controlled ABT transaction into the DWH.
- Do **not** assert export file type (BI-tool dependent, out of scope).
- Gap: the DWH view is transaction-level only — capping/reallocation logic lives elsewhere (see FBD-100334); confirm the boundary is covered by the ABT audit suite, not here.
