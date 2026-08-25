# FBD-100377 — Service Classification on CloudFare (distilled)

**Source:** `FBD-100377 Service Classification Configuration & Reporting Specification V1.00` (16 Dec 2021, C. Kiraz).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Related: FBD-100356 (Merit DWH Solution).

## What it is
- **Service Classification** = an attribute grouping farelist type of service/routes, stored on the **route** as the **"Service Code"** (GFTS terminology). Single-select attribute.
- Configured via **Topology & Fare Management** module of CloudFare.
- Each service has zero-or-more routes; each route has **one** fares-triangle and **one** service code.

## Rules (testable)
- If no tag is allocated to a route, the route **defaults to `Unclassified`**.
- **All routes on the same service should carry the SAME service classification tag** — required so service data syncs against the correct tag.
- If routes on one service disagree, **the first tag the system reaches** on that service's routes is the one synchronised to the Merit Data Warehouse. (Data-integrity risk — see gaps.)
- Service info (incl. service classification) is **synced to Merit DWH** for reporting. Translink can group **Passenger Journey, Revenue and Schedule Adherence** reports by classification.
- Tag list is **configurable** (admin can add/remove tags); more than one tag can exist in the master list, but only one is selected per route.

## Pre-configured tag list (initial setup)
`Unclassified`, `Airport`, `City Express`, `CityStopper`, `Contracts`, `Easibus`, `Express`, `Ferry`, `Foyle Metro`, `Glider`, `Goldline`, `High Frequency Corridors`, `Misc`, `Nightmovers`, `Park & Ride`, `Rural / District`, `Schools`, `Seasonal`, `Town / City Service`, `Urban`, `X Border`.

## Responsibility boundary
- **Translink** configures the correct Service Code per route (Flowbird is not responsible for classification accuracy).
- **Flowbird** provides reporting data filterable by classification group; report format/content is Translink's.

## Suite implications (BOS/ABT suite 30279 + device config)
- **Config-side (CloudFare/portal)** cases: route with no tag → exported/synced as `Unclassified`; setting a route's Service Code persists and appears in the **Route List Report** (FBD-100385).
- **Data-integrity** case (highest value): a service whose routes carry mixed tags → Merit DWH receives only the **first-reached** tag. This is a silent misclassification risk — worth an explicit negative/consistency check across a service's routes.
- Assert the **full pre-configured tag list** is present after config load (missing/renamed tags break reporting joins).
- Reporting assertions (Passenger Journey / Revenue / Schedule Adherence grouped by classification) are **Merit DWH**, not device — cover as BOS reporting cases, cross-ref FBD-100356 / FBD-100347.
