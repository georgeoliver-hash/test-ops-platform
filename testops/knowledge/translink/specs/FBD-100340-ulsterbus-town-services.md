# FBD-100340 — Ulsterbus Town Services (distilled)

**Source:** `FBD-100340 Ulsterbus Town Services Specification v3.00` (10 Aug 2021, S. James).
Distilled testable facts only — raw spec held locally, not committed. Related documents: None cited.
Covers **both** the legacy Ulsterbus Town Service Travelcard **smartcard** validation and the newer **ABT (cEMV) capping** approach.

## Problem being solved
Town Services run in provincial towns (Bangor, Newtownards, Lisburn, Newry, Larne, Ballymena, Antrim, …; Belfast = Metro). Some routes are **dedicated town-service routes**, some are **long-distance routes** that start/end in towns with town services. The limit of travel for a town-service card must stay **within the same town as the boarding stop**. Legacy did this by duplicating stops; CloudFare can't (stops are geographic entities, zones drawn geographically).

## CloudFare topology model
- One overarching **"Ulsterbus Town Services" zone**, subdivided into **Zone Areas per town** (e.g. Ballymena Zone Area, Antrim Zone Area). UBTS zone number = **16 (decimal)**, matching the smartcard encoding.
- Routes (dedicated or long-distance) configured **normally, no special flags**. Products gain only a new "Rapid Issue Sequence Id" for UBTS Smartcard-Use products.
- **For ABT capping, additionally** draw a **separate per-town zone** (e.g. "Ballymena Town Service Zone", "Antrim Town Service Zone") with its own distinct zone number (need not match smartcard zone). So each town has **two overlapping zones**: the UBTS zone (zone-area named after town) for smartcards + a town-named zone for ABT.

## Smartcard validation (ETM) — testable rules
- Card carries zone 16 ⇒ ETM maps to the UBTS zone; card valid for travel only if the **boarding stop is in the UBTS zone**.
- **Limit of travel** = the **furthest stop on the current route that is in the same Zone Area as the boarding stop**; that stop is audited as the alighting stage.
- A boarding stop is valid **iff** it is in the UBTS zone **and is not the last stop on the route within its own Zone Area** (i.e. there must be a furthest-alighting stop ahead of it in that area).
- REQ-0910.0 / REQ-0911.0: Child / Adult UBTS Travelcard — valid when not hotlisted, on all UB services in the operating area, within start/expiry dates inclusive, any time of day, within encoded logical zone; auto-selects the corresponding ticket class, picks furthest alighting stage in the encoded zone on the route, indicates valid, audits with product ref, prints receipt. Adult additionally requires a validatable journey with a retrievable fare.

### Smartcard use cases (oracle behaviour)
- **Dedicated route, tap Harryville Shops** ⇒ Ballymena Zone Area ⇒ furthest = Ballee Park & Ride ⇒ that is the audited alighting. **Valid.**
- **Long route to Antrim, tap Harryville Shops (near start)** ⇒ same as above (Ballymena area, alight Ballee P&R). **Valid.**
- **Long route, tap Pipe Road (outside UBTS zone)** ⇒ **invalid** (not in UBTS zone).
- **Long route, tap Meadowlands (near end)** ⇒ Antrim Zone Area ⇒ furthest = Donegore Drive ⇒ audited alighting. **Valid.**
- **Long route, tap Ballee Park & Ride (last stop in its zone area on the route)** ⇒ **invalid** (no furthest stop ahead in the Ballymena area).

## ABT (cEMV) capping — testable rules
No native "cap by zone area" in the standard ABT product, so use the **per-town ABT zones**: create a cap per town (Daily/Weekly/Monthly) keyed to that town's zone. A journey is **capped only when both boarding and alighting stops are within the same configured town-service zone**.

### ABT use cases (assume Ballymena & Antrim daily caps £1.00; example uncapped fares)
- **Both stops in Ballymena zone** (Harryville→Ballee P&R, fare £1.50) ⇒ **capped to £1.00**.
- **Board in zone, alight outside** (Harryville→Pipe Road, £1.90) ⇒ **not capped**, £1.90 stands.
- **Board outside, alight in zone** (Pipe Road→Donegore Drive, £1.70) ⇒ **not capped**, £1.70 stands.
- **Board in one town zone, alight in a different town zone** (Harryville(Ballymena)→Donegore Drive(Antrim), £2.20) ⇒ **neither** cap applies, £2.20 stands.
- Journey formed **after max journey time** from the tap-on (ETM) + tap-off (BV) taps.

## Suite implications (ABT/BOS suite 30279 + ETM/PV/BV)
- **Confirms** the ABT capping model relied on by the Tap-On specs, and supplies the **"both stops in the same zone"** cap-eligibility rule — the exact condition the ABT Ulsterbus TOO capping-group work (FBD-100662) capitalises on. Good boundary cases for the capping suite.
- **Cap-boundary matrix** (both-in / board-in-alight-out / board-out-alight-in / two-different-town-zones) is a compact, high-value set of cap-eligibility assertions likely missing from suite 30279.
- **Smartcard limit-of-travel** cases (ETM): furthest-stop-in-zone-area as audited alighting, and the two **invalid** edges (outside zone; last-stop-in-area). These belong to the ETM/BV device suite, distinct from cEMV TOO.
- Note the **two-zone overlap** design (smartcard UBTS zone-16 + separate ABT town zone) — a config precondition tests must set up; don't assume a single zone.
- Watch for **stale** cases assuming legacy duplicated-stop behaviour — that mechanism is gone in CloudFare.
