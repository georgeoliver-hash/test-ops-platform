# FBD-100658 — Translink ABT Audit Specification (distilled)

**Source:** `FBD-100658 Translink ABT Audit Specification v1.03` (18 Mar 2026, S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Defines the **audit message structure/content** for ABT taps. Related: FBD-100651 (Glider TOO), FBD-100662 (Ulsterbus TOO), FBD-100716 (Revenue Inspection), FBD-100690 (NIR TOTO).

## Scope — which device emits which record
- **Tap On Only (TOO):** Metro ETM, Ulsterbus ETM, Glider PV, Glider HHD (inspection).
- **Tap On Tap Off (TOTO):** NIR GV, NIR PV, NIR HHD (inspection).
- All ABT taps: `paymentType` = **"ABT"**, `revenue` = **0** (charge is calculated by the ABT back office, never on-device).

## Field rules that are assertable (device-agnostic unless noted)
- **`DeclinedReason`** enum (both tap and journey level): `0`=Success, `1`=Card Expired, `2`=On Deny List, `3`=Declined, `4`=Cancelled, `15`=On BIN List, `20`=Passback.
- **`TapId`** = `DeviceId` + `Terminal ID (TID)` + `UNIX timestamp` concatenated (e.g. `042002201156881725545715`).
- **`transactionId` / `ClientTransactionId`** = GUID; **`SequenceId`** increments by 1 per transaction.
- **`CardType`** always `"emv"`; **`exchangeRate`** always `1.0`; **`currencyCode`** `"GBP"` (ETM only field).
- **`Fare`** in the tap = **pounds** (e.g. `2.3`); **`fareCost`** in `transactionProducts` = **pence** (e.g. `230`). (Unit mismatch is an easy bug — assert both.)
- **`passCount`** always `true`; **`ticketsIssued`** always `false`.
- **`RouteType`**: `0`=Reference Tables (Glider/NIR), `1`=Fare Triangles (Metro/Ulsterbus). Drives which fares-engine call the back office makes (see FBD-100698).
- **`TransferRouteType`**: Metro=`Non-Directional`, Ulsterbus=`None`, PV=`Directional`.
- **`TransportationType`**: `"BUS"` normally; Ulsterbus ETM = **`"Rail Sub"`** on rail-substitution services.
- **Zones** array: one `{"Id": <ZoneNumber>}` per zone the boarding/alighting map point sits in. Zone **Numbers** (not Zone Ids) — bitwise-encoded values like 128/512/768/1280/10240 (see FBD-100229).
- **`IsInspection`: true** on HHD taps (fare `0`, `TID` `"0"`, product id `5001`).

## Product IDs used in audit (assertable per device/scenario)
- **`7000`** — TOO travel product ("ABT Tap On Only"). Fare = rule assignment of the **first "ABT Tap On Only" product on the device's home location** (Translink must create this; current usage is type "ABT Product").
- **`6000`** — NIR TOTO travel product (GV/PV).
- **`5001`** — Inspection product (HHD TOO and TOTO inspection taps).

## Alighting-location calculation (per device — no driver selection on flat-fare/validator devices)
- **Metro ETM:** last stop on the route within the configured **Metro Network Zone**.
- **Ulsterbus ETM:** driver **does** choose alighting stage (audited directly).
- **Glider PV:** uses the **Furthest Alighting Point file**, extended for ABT via a `ProductSearchKey` = **"ABT"** entry; matched on configured BoardingStopID + Direction.
- **Structural differences:** PV/GV taps carry `gpsCoordinates`; HHD taps carry a **`CardDetails`** block (CardBrandLabel, CardHash, CardReference, CardToken, ExpiryDate, MaskedPan, PAR, TransactionReference) instead of raw `CardData`. TOTO taps use a **`TotoTap`**/`Location` structure (renamed from `JourneyTap` in v1.03); TOO taps use **`JourneyTap`** with `BoardingStage`/`AlightingStage`.

## Suite implications
- Build a **per-device audit-schema conformance case** (ETM Metro, ETM Ulsterbus, PV Glider, HHD Glider, GV NIR, PV NIR, HHD NIR) asserting the required structures and the constant fields (`paymentType=ABT`, `revenue=0`, `CardType=emv`, `passCount=true`, `ticketsIssued=false`).
- Assert the **fare unit split** (`Fare` pounds vs `fareCost` pence) and correct **product id** (7000 TOO / 6000 TOTO / 5001 inspection).
- Assert **`DeclinedReason` mapping** across the failure taxonomy (expired/deny/BIN/passback/declined/cancelled) — ties to FBD-100307 failure modes.
- Cover **alighting-location derivation** per device, especially PV Furthest-Alighting-Point `ProductSearchKey="ABT"` and Metro-Network-Zone last-stop logic.
- Cover **`TransportationType="Rail Sub"`** on Ulsterbus rail-substitution and **HHD `CardDetails`/`IsInspection`** (v1.02–v1.03 changes) — likely stale/missing after the rename of `JourneyTap`→`TotoTap`.
- Zone arrays must carry **Zone Numbers** not Zone Ids — cross-check against FBD-100229 encoding.
