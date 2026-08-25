# FBD-100277 — Card Reference File Usage (distilled)

**Source:** `Card Reference File Usage (FBD-100277) V2.00` (14 Jan 2021, S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Related: FBD-100261 (CloudFare Multi-Journey Product Configuration).

## What the Card Reference File is
A device-distributed lookup that, combined with the **card reference number** on the smartcard + the current **boarding stop** + the **fares triangle**, determines **how far along the route** a passenger may travel (the alighting point). Used by smartcards that carry a card reference number:
- Metro Multi-Journey (Inner/City/Extended), Metro Travelcard, Ulsterbus Multi-Journey, Ulsterbus Town Service Travelcard, Metro DayLink. (**TaxSmart lookups 17/18/19 are no longer used.**)

## File format (JSON, replacing legacy TXT)
- Translink may keep editing the **legacy .txt**; Flowbird runs a utility to convert to **JSON**, imported into TMS and distributed to devices (same row ordering as the txt).
- Five nodes: **FormatVersion** (schema version — device picks parse structure from it), **ConfigurationVersion** (data version — **MUST be incremented on any content change or devices won't pick it up**), the **reference-table lookup number** (= smartcard **Field ID**), the **card reference number (`ReferenceId`)**, and **`Fare`** (pence, **for info only — not used in issue or validation**).
- Lookup numbers → card type: `01`–`06` Metro MJ, `07/08` Metro Travelcard A/C, `09/10` Ulsterbus MJ A/C, `11/12` Ulsterbus Town Service A/C, `20/21` DayLink A/C (17/18/19 TaxSmart retired).

## Card issue (where the reference number comes from)
- Most types (Metro MJ, Metro Travelcard, UTS Travelcard, DayLink): reference number is **predefined in CloudFare** (WTS SmartCreate product **`Card Reference ID`**), written to the card by POS at issue. **`Card Reference ID Location`** setting picks which card field holds it (usually **"Journeys"** or **"Start Date"**).
- **Ulsterbus Multi-Journey is the exception:** the **operator chooses** the reference number — calculates the Adult Single fare between the two stops, consults a **crib sheet** mapping fares→reference numbers, then selects it + number of journeys on POS.

## Validation lookup algorithm (the testable logic)
1. Read **Field ID** + **card reference number** from the card.
2. Field ID → select the reference table in the file.
3. Find the card's reference number in that table's `ReferenceId` list.
4. Using the **boarding stop** column of the fares triangle, search down that column for the `ReferenceId`. If found → step 7; else step 5.
5/6. Iterate **upward** through the reference table (next-higher `ReferenceId`) and repeat the column search until a match is found or the top is reached (**no match → no alighting stop returned**).
7. Pick the occurrence **furthest down** the boarding column, and audit **that alighting stop + the card reference number** in the **WTS SmartUse** transaction (for Pass Revenue reporting).
- **Circular routes** are explicitly handled (a reference number may recur down the fareslist with different numbers between). New system uses **stops (PTI reference)**, not stages, for the audited alighting point.

## Suite implications
- Cover the **validation lookup end-to-end**: given boarding stop + card reference number, assert the **correct alighting stop** appears in the WTS SmartUse audit (incl. the "furthest down the column" selection and the upward-iteration fallback).
- Cover the **no-match** path (reference not found in column, iteration reaches top → no alighting stop) and a **circular-route** case (recurring reference number resolves to the correct further-down stop).
- Cover the **Ulsterbus MJ operator-chosen** reference-number issue path on POS vs the **predefined CloudFare** path for the other types — different issue behaviours.
- Assert **ConfigurationVersion increment** gating: an edited file with an unchanged version is **not** applied by devices (a real "stale config" trap).
- Assert `Card Reference ID Location` ("Journeys" vs "Start Date") is honoured at issue, and that **`Fare` is ignored** by device logic.
- These are primarily **POS (issue) + ETM/PV (validation)** cases; the alighting-stop audit ties into Pass Revenue / MERIT reporting checks.
