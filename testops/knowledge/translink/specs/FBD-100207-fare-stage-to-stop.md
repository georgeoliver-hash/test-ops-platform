# FBD-100207 — TFTS Fare Stage to Stop Migration Solution (distilled)

**Source:** `FBD-100207 TFTS Fare Stage to Stop Solution V4.00` (26 Feb 2021, J. Harley / S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Related: FBD-100296 (TransXChange Data Usage Specification).

## What changed and why
- Legacy Translink system was **entirely Fare-Stage based** (a Fare Stage = a group of bus stops sharing a common fare; stop membership can vary by route context). **ABT requires stop-based fares**, so the system migrates to a **primarily stop-based** model.
- Migration is a **one-off Flowbird activity** on a snapshot of Translink data (TransXChange stops/routes/services + existing Fare-Stage triangles + Rules). Translink's fares rely heavily on **lookup tables**, so **Rules translate lookup values into actual fares**. After migration Translink maintain fares per-stop.

## Fare-triangle population rules (back office)
- Stop-based triangles are seeded only at **mapped Key Stops**; all other stop/stop cells start **zero**. A zero fare passed to a device means **the driver/operator cannot issue a ticket to/from that stop** — so triangles must be **fully populated** first.
- **Cascade algorithm** (two passes, order-independent but each pass completed fully before the next): **cascade the fare UP until the next populated fare; cascade RIGHT until the next populated fare.**
- **Legitimate zero fares** (invalid stop-stop combinations in the source triangle) must be **cascaded as zero** — i.e. some zeros are intentional and must be preserved.
- Stops associated with a Fare Stage are flagged **Key Stops** in CloudFare. Calculated triangles go back to Translink for validation/confirmation.

## Device behaviour (selection + display)
- **ETM:** software restricted so the driver can only select **Key Stops, Favourite Stops, and Fare Stage Breaks** (NOT every stop). Key/Favourite stops defined in CloudFare; **Fare Breaks auto-calculated by the ETM**. For **alighting**, the ETM shows and prints the **Fare Stage name, not the stop name**. **GPS failure fallback:** driver manually selects by scrolling Key Stops (arrows) or entering the **Fare Stage ID** (keypad). When scheduling data is absent, routes are populated with a **superset of all Key Stops/Fare Stages** across route/service variants.
- **POS:** operator selects boarding + alighting by scrolling Key Stops (arrows) or entering the **Fare Stage ID** (numeric keypad). POS **displays and prints the Fare Stage name, not the stop name**.
- **TVM:** customer picks **any Key Stop for any boarding/alighting combination network-wide** (provided a valid fare exists) — **no route selection required**, only Bus vs Rail. Fare Stage name shown on screen + ticket.

## Reporting (CloudFare → MERIT)
- Translink report transactions at **Fare-Stage level, not stop level**. Boarding/alighting stops are translated to their **unique Fare Stage** before being sent to MERIT.
- **Gap-fill rule (R2.1+):** if a transaction contains a stop **not associated to any Fare Stage**, CloudFare looks back to the **previous stop on that route that IS associated to a Fare Stage** and sends that instead (avoids the legacy "Fare Stage 0 / blank" behaviour). Not needed at R2.0 (route config guarantees fare-stage-associated stops); required **R2.1 onward**.
- **Schedule adherence / Headway reports** (R2.1) need stop-level granularity, so they run via the **Data Warehouse** (fed by CloudFare), **not MERIT**.

## Exclusions (do NOT assume stop-based behaviour here)
- **Glider and NIR are excluded** — not in the TransXChange data; they use **Reference Tables** in CloudFare instead.
- Also excluded: Transfer-Stop application to routes/tables (later design review), Rail Substitution, Day Tours, Shuttle, "Special", Assist Bus, and **POS "truncated" fareslists**.

## Suite implications (POS suite 30253)
- **POS stop-selection cases:** assert operator can only reach fares via **Key Stops (arrow scroll) or Fare Stage ID (keypad)**, and that **Fare Stage name — not stop name — is shown on screen and printed** on the ticket. Likely a gap if existing cases assert stop names.
- Assert that a **zero-fare stop/stop combination blocks ticket issue** on POS (and ETM) — negative-path coverage.
- Cover **Fare Stage ID manual entry** as an alternate selection path (parity with the ETM GPS-fail fallback).
- Flag **Glider/NIR (Reference Table) fares** as a separate coverage area — they do NOT follow the stop-based selection model; POS truncated fareslists are explicitly excluded.
- ABT-BOS suite: assert the **MERIT gap-fill** (unassociated stop → previous fare-stage stop) for R2.1+, and that transactions are exported at **Fare Stage** granularity.
