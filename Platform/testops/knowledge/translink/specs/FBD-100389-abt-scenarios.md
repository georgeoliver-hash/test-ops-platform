# FBD-100389 — ABT Scenarios (distilled)

**Source:** `CloudFare - ABT Scenarios (FBD-100389) V5.00` (24 Apr 2023, M. Douglas / S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Related: FBD-100307 (ABT Data Flow), FBD-100658 (ABT Audit), FBD-100334 (Capping), FBD-100698 (Topology usage).
Worked-example spec: shows how taps flow device → CloudFare → CloudFare ABT → MERIT and the money that lands.

## Definitions (assert these are computed correctly, not just present)
- **Fare (Uncapped):** value for a journey before any discount/cap.
- **Revenue Taken / Charge Amount:** what the passenger is actually charged for the transaction.
- **Aggregated Fare:** running total of all journeys in a day before capping.
- **Full Fare Equivalent:** what the journey would have cost with no discount/cap — a **non-revenue** reporting value.
- **Operating day = 04:00:00 → 03:59:59** (the capping window boundary).

## Default rules used by the scenarios
- **Rule 1 – Daily Cap:** within one operating day, passenger charged a **max of £5.00**.
- **Journey 1 – TOO:** tap-on to an ETM = **£2.00 flat fare** (distance-independent).

## General assumptions baked into every scenario (each is a precondition, i.e. a negative test)
- Tap on an in-service ETM; boarding + a subsequent alighting location both permitted (correct zone) per CloudFare topology, on the signed-on route.
- Card/token not on **deny list / BIN blocking list**; product valid.
- Tap is **outside the configured passback period**.
- Card not expired, supported scheme (AID), passed **Offline Data Authentication (ODA)**, pre-auth successful.

## The three scenarios (expected money in MERIT / ABT)
- **S1 — Single cEMV tap, not capped:** charge £2.00. MERIT txn = £2.00 full-fare-equiv, £2.00 revenue taken.
- **S2 — Three cEMV taps, cap applied:** aggregated £2 → £4 → £5; charge amounts £2, £2, **£1** (capped at £5). MERIT: three txns, revenue taken £2/£2/£1; ABT txn total = £5.00.
- **S3 — Three taps, one late:** tap 2 fails to reach CloudFare on Day 1 (comms failure / quarantined). Day 1 settles taps 1 & 3 → charge **£4.00**. Tap 2 arrives Day 5, marked **'Late Tap'** on the ABT Customer & Operator Portal, settled → charge **£1.00** (total still £5).
  - **Key rule:** a late tap is **retrospectively treated as the last tap(s) of its original day** for charging.
  - **Late taps accepted up to a maximum of 14 days**; beyond 14 days = expired (see FBD-100307).
  - MERIT/ABT-journey reports use **Day 1** (the travel date), but the **ABT Transaction** record uses **Day 5** (settlement date).

## Suite implications
- Add end-to-end capping cases keyed to the operating-day boundary (04:00–03:59) — assert **charge amount per tap** and **daily aggregate cap**, not just "a fare was taken". S2 is the canonical cap-applied case.
- Cover the **late-tap** path (S3): comms-failure/quarantine on one tap, arrival within 14 days, `Late Tap` flag on the portal, and the **travel-date vs settlement-date** split in MERIT vs ABT Transaction. Add a boundary case at **>14 days = expired**.
- Assert **Full Fare Equivalent stays at the uncapped value** while Revenue Taken drops on the capped tap — a common reporting bug.
- Each assumption (passback, deny/BIN list, expired card, ODA fail, unsupported scheme) is a distinct negative ABT case for the ABT/BOS suite (30279).
