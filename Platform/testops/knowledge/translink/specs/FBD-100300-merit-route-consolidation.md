# FBD-100300 — MERIT In & Out Route Consolidation Methodology (distilled)

**Source:** `MERIT In and Out Route Consolidation Methodology (FBD-100300) V3.00` (12 Mar 2021, S. James).
Distilled testable facts only — raw spec held locally, not committed.
Related: FBD-100296 (TransXChange Data Usage).

## Purpose
- Defines how **CloudFare synchronises route/stage data to MERIT** so that inbound and outbound variants of a service are **consolidated into one ordered stage list** (MERIT requires ordered stages to function).
- Pre-reqs: TransXChange/route data + Stage-to-Stop mapping imported into CloudFare. Runs **per service** on every CloudFare→MERIT sync.

## The 8-step consolidation algorithm (assert the transform)
1. Get **all route variants** for the service — **including "abstracted" routes** (created for manual route selection on device), not just TransXChange routes.
2. Get all stops per variant, **filter to key stops (stages) only** (drop intermediate stops).
3. **Reverse inbound routes** so all variants point the same direction (outbound). (V3.00 changed the reference direction to **outbound**.)
4. Combine all variants into one list.
5. **Remove duplicate stage numbers** — one entry per stage number.
6. Reorder by order number.
7. Make order numbers **unique**.
8. **Add 1000 to every order number.**

## Rules worth asserting
- Columns handled: Order Number, PTI Stop Reference, Stage Name, Stage Number.
- **Sent to MERIT: Order Number, Stage Name, Stage Number only. PTI Stop Reference is NOT sent.**
- **De-dup is by Stage Number** (not stop reference / not name).
- The **+1000 offset** is deliberate: legacy MERIT order numbers are ≤3 digits, so offsetting new-system orders to ≥1000 lets new and **legacy data coexist** and historic reports keep working unchanged.

## Suite implications (BOS/Merit reporting)
- Assert consolidation determinism on a known multi-variant service (like the doc's 1A example): inbound reversed, variants merged, **duplicate stage numbers collapsed to one**, orders unique and **all ≥1000**.
- Assert **PTI Stop Reference is dropped** from the MERIT payload and abstracted routes ARE included.
- Assert legacy coexistence: a service with pre-existing <1000 order numbers must not collide with newly synced ≥1000 orders (historic MERIT reports unaffected).
- Gap: this is a back-office data-transform test (CloudFare→MERIT), not a device test — likely absent from device-centric suites; good candidate for a Merit-integration coverage row.
