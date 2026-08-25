# FBD-100335 — Rail Substitution Services (distilled)

**Source:** `FBD-100335 Rail Substitution Services Specification v3.00` (26 Jul 2021, S. James).
Distilled testable facts only — raw spec held locally, not committed. Related documents: None cited.
(Foundational spec; the device/back-office detail is refined by the later Tap-On specs FBD-100662/FBD-100690.)

## What a rail substitution service is
Bus services run when the rail network is disrupted; they visit the **same stations** as the train, configured to follow the rail-line order. ~6–7 routes, one per NI rail line (e.g. Larne, Bangor, Portadown, Londonderry, Portrush, Dublin). **NI Railways smartcard products no longer exist** — those rail business rules now live in ABT; existing rail-valid smartcards (iLink, Free/Half-fare Concession Smartpasses, yLink, 24+, Staff/Spouse/Dependant Passes) are still honoured.

## CloudFare topology config
- New routes per rail line, each direction (IN/OUT), **not** in TransXChange — defined manually as a "Rail Subs" service with the line's stations. **Each station is its own fare stage** (no non-fare intermediate stops).
- Created at the hierarchy level of the operating ETM (Metro rail-sub ⇒ Metro Bus level).
- **`Transport Mode` route attribute = "Rail Sub"** (new mode) — how ETM/ABT recognise a rail-sub route.
- **Default Product Group** attribute set to the paper rail-sub products to populate the FLU menu.
- **GPS tolerances** around each station may need **widening** (bus may not stop exactly at the rail station) so the ETM auto-updates the boarding stop as the bus progresses.

## Product / rule config
Existing bus products reused; rules/areas differentiate the fares. Rail-sub-specific rules assigned to normal bus products in a **"Rail Substitution" area** within Metro Bus / Ulsterbus hierarchy levels ⇒ rail-sub fare triangles carry the "Rail Substitution" area. Optionally, service/route-variant rule assignments can **disable bus smartcard products** on rail-sub services.

## ETM / BV device behaviour
- Same experience as a normal route (paper tickets, smartcard validation) **except no schedule adherence** and a different product set.
- Boarding stop still auto-updates from GPS (given tolerances configured).
- Sign-on: driver uses **"Manual Override"** to select an ad-hoc route not in timetable data — type the rail-sub route variant name/number and sign on (REQ-2867.0 also covers running boards, light running, assist buses, special events, school services).
- Device recognises the route as rail-sub via the Transport Mode attribute and sends **ABT taps with transport mode "Rail Sub"**. NI-Railways-specific smartcard business logic is **not** on the ETM/BV (it's in ABT); ETM/BV still validate cross-mode smartcards (iLink, 24+, half-fare, free concession staff/spouse/dependant).
- REQ-2578.0 (BV/ETM All; BV+NI-Railways smartcard support from Release 2.2b): valid smartcard on a rail-sub bus ⇒ validate against product rules + audio-visual message; invalid ⇒ audio-visual error.

## ABT back-office behaviour
- **Programmed Journey Time is IGNORED** for any journey with a rail-sub leg (train PJT would mis-fit a bus). ABT detects this from **transport mode "Rail Sub"** ⇒ apply rail business rules **but skip PJT**. **Maximum Journey Time still applies.**
- Fares/caps otherwise follow the already-defined **rail ABT business rules**; the rail-sub nature is **visible to customers/operators** in the Passenger/Operator portals.

## Suite implications (ABT/BOS suite 30279 + ETM/BV)
- **This is the root definition of the "Rail Sub" transport-mode path** that FBD-100662 (ETM splits one TOO tap into two TOTO taps) and FBD-100690 (synthetic tap-on/off, PJT ignored, MJT applied) build on. Cases should assert the **"Rail Sub" transport mode on the audit** and the **PJT-ignored / MJT-applied** back-office rule as one coherent chain across the three specs.
- **ETM/BV device cases:** Manual Override sign-on to an ad-hoc rail-sub route; boarding-stop auto-update via widened GPS tolerances; cross-mode smartcard validation still works while NI-Railways-specific logic is absent.
- **Config preconditions** tests must establish: rail-sub routes with Transport Mode "Rail Sub", each station a fare stage, "Rail Substitution" fare area.
- Cover that rail-sub fares/caps **match normal rail** (same fare + same capping group) — a cross-check against the rail-sub fares triangle vs reference table (called out in FBD-100690).
- Confirms the shift **away from NI-Railways smartcard products** into ABT — flag any legacy cases still asserting NIR-smartcard-specific device logic as **stale**.
