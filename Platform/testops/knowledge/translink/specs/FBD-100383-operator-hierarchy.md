# FBD-100383 — TFTS Operator Hierarchy (distilled)

**Source:** `FBD-100383 TFTS Operator Hierarchy v4.00` (22 Feb 2022, S. James).
Distilled testable facts only — raw spec (diagram-heavy) held locally in `dev/translink-requirements/`, not committed.
Note: "a view of the *intended initial* configuration… subject to change." Treat structure as authoritative, membership as a snapshot.

## Top-level structure
`Translink` is the root operator. Under it the tree branches by mode/company:
- **Metro** → `Glider`, `Metro Bus`, `Falls (Metro)`, `Milewater Service Centre (Metro)`, `Newtownabbey (Metro)`, `Short Strand (Metro)`, `Metro Central (Metro)`, `TVM Metro (Metro)`, `Metro Agents (Metro)`, `mLink Metro (Metro)`, `Collect Tickets (Metro)`.
- **Ulsterbus** → depot operators: `Antrim (UB)`, `Armagh (UB)`, `Ballymena (UB)`, `Bangor (UB)`, `Coleraine (UB)`, `Craigavon (UB)`, `Downpatrick (UB)`, `Dungannon (UB)`, `Enniskillen (UB)`, `Europa (UB)`, `Larne (UB)`, `Lisburn (UB)`, `Londonderry (UB)`, `Magherafelt (UB)`, `Newcastle (UB)`, `Newry (UB)`, `Newtownabbey (UB)`, `Newtownards (UB)`, `Omagh (UB)`, plus `TVM Ulsterbus (UB)`, `Ulsterbus Agents (UB)`, `Ulsterbus Contractors (UB)`, `Goldline Barcode (UB)`, `Collect Tickets (UB)`, `mLink Ulsterbus (UB)`.
- **NIR** (rail) → station operators: `Antrim (NIR)`, `Ballymena (NIR)`, `Ballymoney (NIR)`, `Bangor (NIR)`, `Botanic (NIR)`, `Carrickfergus (NIR)`, `Coleraine (NIR)`, `Gt Vic St (NIR)`, `Lanyon Place (NIR)`, `Larne (NIR)`, `Larne Harbour (NIR)`, `Lisburn (NIR)`, `Londonderry (NIR)`, `Lurgan (NIR)`, `Newry (NIR)`, `Portadown (NIR)`, `Portrush (NIR)`, `Whitehead (NIR)`, `Yorkgate (NIR)`, plus `NIR Validators (NIR)`, `TVM Railway (NIR)`, `Rail Barcode (NIR)`, `mLink Railway (NIR)`, `Collect Tickets (NIR)`.
- **PayPoint Agents** exists at Translink level.

## Configuration inheritance (what is defined per level)
Each level owns/inherits: **Route & Reference Table config** (services/routes common to ETM/POS/TVM, or specific per mode), **Product config**, **Rule config**, **Ticket Template config**, **Product Group config**, **Area config**, **Zone config** (`All Zones` at top). Explicit tiers exist for:
- Products/Rules/Templates/Groups **common to more than one operator**, **common to Glider + Metro Bus only**, then **specific to** Glider / Metro Bus / Ulsterbus / NIR.
- Areas **specific to** Metro Bus / Ulsterbus / NIR.
- Device-type variants of templates/groups (e.g. Ulsterbus ETM/POS/TVM; NIR HHD/POS/TVM; Glider HHD/TVM).

## Device & staff home locations (per operator)
- Each operator has a **Device Home Location** (e.g. `Falls BV/ETM Devices`, `Glider HHD/PV/TVM Devices`, `Antrim GV/HHD/PV Devices`, `Metro TVM Devices`) and a **Staff Home Location** (e.g. `Falls Staff`, `Antrim Bus Staff`).
- Device types by mode: **Metro/Ulsterbus depots = BV/ETM** (+ Agents = POS, + TVM); **Glider = HHD/PV/TVM**; **NIR stations = GV/HHD/PV** (+ TVM); some NIR halts (`Ballymoney`, `Larne`, `Larne Harbour`, `Portrush`, `Whitehead`) = **HHD only**; `Yorkgate` = HHD.
- **Staff Working Locations** roll up: e.g. all Metro depot staff also belong to **All Metro Staff**; all UB depot staff → **All Ulsterbus Staff**; all NIR station staff → **All NIR Staff**. TVM/Agents staff roll into **Cash Collection / Maintenance Staff**.

## Suite implications (BOS/ABT suite 30279 + device config)
- The hierarchy is the **visibility/scoping backbone** for the config-export reports (FBD-100385) and for **user claims** (FBD-100342): a `CF-Operator-<X>` claim sees that operator and its sub-operators only. Coverage should assert **an operator sees its own + descendant data but NOT parent/sibling data** (e.g. `Antrim (UB)` user cannot see `Bangor (UB)`; a `Metro` user sees Glider + Metro Bus + Falls…).
- **Config inheritance** cases: a product/rule defined at `Translink` or `Metro` level is visible/usable at child depots; one defined `specific to NIR` is NOT visible to Ulsterbus.
- **Device/staff home-location** cases: a device signed on at a depot reports under the correct operator, and staff belong to the right rollup (drives operator-totals and cash-collection reporting).
- Membership lists here are a **snapshot** — verify against live CloudFare before hard-asserting specific depots (v4 already added/removed several: Goldline Express removed, Metro Central re-added without staff home).
