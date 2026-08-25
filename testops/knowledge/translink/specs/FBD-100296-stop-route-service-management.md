# FBD-100296 — Stop, Route & Service Management in CloudFare (distilled)

**Source:** `Stop, Route & Service Management in CloudFare Specification (FBD-100296) V6.00` (26 Oct 2021, S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Scope excludes fares management and schedule adherence. Related: FBD-100307 (ABT topology publish), FBD-100698 (topology consumed by ABT), Map Point Import File Example.

## TransXChange → abstracted routes
- Source data is **TransXChange** (from Omnibus). Current phase uses it only to generate **'abstracted routes'** (key stops only, analogous to stages). Schedule adherence out of scope.
- CloudFare **Service** dropdown = TransXChange `LineName`; **Route** dropdown = `PrivateCode`. Route dropdown shows **abstracted routes only** (TransXChange route variants omitted).
- Omnibus PrivateCode format ≈ `TMAO<4-digit service>-X[-Y]`. **Abstracted-route naming = service name + direction**, e.g. `1A In`, `2B Out`. This is what the ETM matches.

## ETM sign-on & GPS boarding-stop adjustment (device-testable)
- Driver types the route number on the **Manual Route Number Entry** screen; ETM lists routes whose `PrivateCode` **starts with** the typed string. Blank entry → whole abstracted-route list alphabetically.
- Route Selection screen columns: **left = service name, middle = blank, right = direction ("In"/"Out")**.
- After sign-on, ETM uses GPS + TransXChange stop coordinates to **auto-advance the boarding stop** when within a **configured tolerance (metres)** of a stop. Change is only visible **after leaving the 'travel' screen**. Boarding stop does **not** update at intermediate (non-key) stops.
- **GPS Lookahead** route attribute: number of stops ahead the ETM checks for a GPS match; **0 (default) = look at all stops ahead**.

## Stop (map point) management
- **Map Point Import File** = CSV, header row (no spaces), columns: `UniqueID, ReferenceID, CommonName, ShortName, StopType, Direction, Latitude, Longitude, StageID, StageName, CompassPoint`.
  - `StopType`: **"BCT"** = bus, **"RPL"** = rail. `Direction`: **"Inward" / "Outward" / "Both"**. `CompassPoint` unused → each row ends with a trailing comma.
- Import success box reports **Stops Added** / **Stops Updated** counts. `UniqueID`/`ReferenceID` are the identity keys — changing them = a **new** stop, not an edit.
- Stops can also be added via Drawing Tools (Drag & Drop / Use Current Location) and exported via **Export Map Points** (same CSV format).
- **Delete stop** only enabled if the stop is **not part of any route**. Creating a new **stage** for a stop requires the file-import route (not the map UI).

## Service / route management (assertable rules)
- Create service requires **both** name + description (description not used by CloudFare but synced to MERIT). **Deleting a service also deletes its assigned routes** (with confirmation).
- Create route: from scratch (map stop selection, added in click order) or **Copy Route** (same service, name + `-copy`).
- **Delete route** requires confirmation. **Reset Route Path** restores shortest path between stops.

## Route attributes (config surface consumed elsewhere)
- **Public Route Code** = code printed on tickets. **Direction** feeds Route Selection screen.
- **Vehicle Type** (bus/train/...) — used by **ABT to decide which business rules run**.
- **ABT Type** dropdown: **disabled / TOO / TOTO** (plus an unused driver-initiated-TOO option — *not for Translink*).
- **Transfer Time** (Multi-Journey transfer minutes), **Directional Transfer** flag, **Product Group** / **Easibus Product Group** (FLU menu overrides), **Enable Multiple Currency**, **Service Groups** (fare export grouping), **Tour Route**, **Easibus Route**.

## Suite implications
- ETM sign-on cases: prefix-match route filtering, blank-entry full list, Route Selection column layout, and **GPS auto boarding-stop advance** incl. Lookahead=0 (all-ahead) — device-side, likely thin.
- Map Point Import: assert CSV header/format, `StopType` BCT/RPL, `Direction` enum, trailing-comma, and Added/Updated counts; assert **UniqueID change = new stop**.
- Assert **delete-service cascades to routes** and **delete-stop blocked while on a route** — data-integrity cases.
- **ABT dependency:** `Vehicle Type` and `ABT Type` (TOO vs TOTO) on the route drive ABT business-rule selection — cross-link to FBD-100307/FBD-100698 capping/fare coverage.
