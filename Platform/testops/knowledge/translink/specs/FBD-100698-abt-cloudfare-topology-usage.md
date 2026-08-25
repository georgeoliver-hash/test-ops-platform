# FBD-100698 — ABT and CloudFare Topology / Fares-Engine Usage (distilled)

**Source:** `FBD-100698 ABT and CloudFare Topology Usage v0.04` (23 Jan 2025, S. James), plus the
superseded companion `FBD-100698 ABT and CloudFare Fares Engine Usage v0.01` (19 Nov 2024).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Defines how the ABT back office calls the **fares engine** to build capping-rule lists and to price taps. Related: FBD-100658 (audit fields consumed here), FBD-100334 (capping), FBD-100229 (zones).

## Capping-rule service list (topology → ABT)
- ABT's capping-rule service list must be built **automatically from the fares engine**, not hand-maintained in the ABT DB.
- v0.04 mechanism: CloudFare **publishes topology to an exchange** (same one MERIT subscribes to); **ABT subscribes to the same exchange**. Key field consumed is **`ServiceName`** (contains all route service names + all reference-table names).
- Benefit: the customer controls timing — publishing new services synchronises them to **ABT and MERIT simultaneously**.
- (Earlier v0.01 mechanism used `RouteSummaries` API + a new reference-table call and de-duplicated `MasterServiceName` — **case-sensitive**, so `10a` ≠ `10A`. Superseded, but note the case-sensitivity trap.)

## Base (capping) products
- Capping groups need a **"Base Product"** = the cap limit. ABT populates the base-product list from products of type **"ABT Product"** via `ProductsWithPropertiesByProductType` (OperatorId always **"1"**, ProductType always **"ABT Product"**). ABT keeps each product's **Description** (display) and **Id** (for later fares calls).

## Fare-request routing (driven by the audit `RouteType`)
- **`RouteType = 0` → Route Reference Fare** via `/FaresService/{v}/AreaFare` — used for **NIR TOTO** fare requests and **missing-stop additions**. Boarding/alighting from the tap's `Location` element, location type **"Stage"**; filter carries `OperatorId` + `RouteReferenceId` from the audit data.
- **`RouteType = 1` → Fare Triangle Fare** via `/FaresService/{v}/RoutePointToPointFares` — used for **Rail Substitution** routes (ETM TOO split into TOTO by ABT) and **Ulsterbus alighting-stop changes**. Boarding/alighting location type **"Stop"**; filter carries `RouteId`.
- All fare calls pass **Product Id = the Adult account-type product** configured in the ABT DB, plus the **tap-on timestamp** as Date & Time.

## Capping-group & cap-value lookups
- Capping-group product is configured **by name** in the ABT DB; the fares engine needs a **product id**, so a new call resolves it: `/FareProductsService/1.0/FareProductsByDescription/{Product Name}` (URL-encode spaces as `%20`). Then AreaFare (RouteType 0) or RoutePointToPointFares (RouteType 1) runs with the resolved id.
- **Cap value per group:** `/FaresService/{v}/FareByProductId` with Product Id = base product, **Reference = capping-group name**, Date/Time = tap-on time.
- **Max Fare & Standard Fare:** now resolved by **product id** (was product name) so max/standard-fare transactions can be sent to MERIT. Uses `FareByProductId` with **Reference = 0** (preset, boarding/alighting-independent).

## Location lists (for manual ABT adjustments)
- **UB TOO alighting-stage list:** `/TopologyService/{v}/Modes/{Mode}/Operators/{OperatorId}/Route/{RouteVariantId}/Locations/{MapPointId}/Destinations` — Mode `"BRT"`; returns all stops **after** the boarding stop on the route. Take `Name`, `Id`, `logicalZones`.
- **NIR TOTO alighting-stage list:** `/TopologyService/{v}/Modes/{Mode}/RouteReferences/{RouteReferenceId}/Destinations` — Mode `"BRT"`; returns all reference-table stages except the boarding stage.

## Suite implications
- Add a back-office coverage case per **fare-routing branch**: assert `RouteType=0` → AreaFare and `RouteType=1` → RoutePointToPointFares, and that the priced fare matches the boarding/alighting/route/product combination (ties to FBD-100389 charge amounts).
- Cover **Rail Substitution** (ETM TOO → ABT-synthesised TOTO, RouteType 1) and **UB alighting-stop change** — both fare-triangle paths likely thin in the ABT/BOS suite (30279).
- Assert **capping-rule service list** is populated from published topology (name resolution correct, **case-sensitive** de-dupe) — a topology-config regression surface.
- Assert **Max Fare / Standard Fare** now flow to MERIT (product-id based, Reference=0) — a v0.04 change likely missing from existing coverage.
- Assert cap-value lookup uses **capping-group name as Reference** and the correct **Base Product** — the heart of capping correctness.
