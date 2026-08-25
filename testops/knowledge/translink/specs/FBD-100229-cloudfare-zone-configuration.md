# FBD-100229 — CloudFare Zone Configuration (distilled)

**Source:** `CloudFare Zone Configuration Specification (FBD-100229) V4.00 DRAFT` (20 Apr 2022, S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Zones underpin smartcard validity **and** ABT geographic capping. Related: FBD-100271 (Multi-Journey Transfer), FBD-100340 (Ulsterbus Town Services), FBD-100658 (zone numbers in audit).

## Zone model
- A zone = a map boundary; any stop/station inside is in the zone. **Boundary line is inclusive** of stops on it. Zones may **overlap** (a stop can be in many zones) — except iLink (below).
- **Zone areas:** one zone can have **two disconnected boundaries** (e.g. main Ulsterbus Town Service zone = one area per town; iLink Zone 1 split into City / Inner / Extended Metro areas).
- Baseline ~**40 zones**: iLink ×5, Cross Border ×1, ABT Capping ×4 (example: Coleraine Triangle, Rail Day Tracker, Metro Network, Bus Rambler), Multi-Journey Transfer ×1, ABT Mini-Transfer ×4, Ulsterbus Town Service ×~25.

## iLink hierarchy (the encoding-critical rule)
- iLink zones are **inclusive outward**: Zone 1 ⊂ 2 ⊂ 3 ⊂ 4; **North West ⊂ Zone 4 only** (NW is NOT in 1/2/3, and 1/2/3 are NOT in NW).
- Validity matrix (smartcard valid in ✓):

  | Card | Z1 | Z2 | Z3 | Z4 | NW |
  |---|---|---|---|---|---|
  | Zone 1 | ✓ | ✗ | ✗ | ✗ | ✗ |
  | Zone 2 | ✓ | ✓ | ✗ | ✗ | ✗ |
  | Zone 3 | ✓ | ✓ | ✓ | ✗ | ✗ |
  | Zone 4 | ✓ | ✓ | ✓ | ✓ | ✓ |
  | Zone NW | ✗ | ✗ | ✗ | ✗ | ✓ |

- Because validity is derived **bitwise from the encoded zone number**, iLink zones **must NOT overlap** in CloudFare (Zone 1 outer boundary = Zone 2 inner boundary, etc.). Example: **iLink Zone 2 card is encoded 192 = 128 (Zone 1) + 64 (Zone 2)**, so valid only in those two.

## Zone numbers (assertable constraints)
- Zone **Number** is bitwise/additive and card-proven; **Zone Id** is auto-generated (different thing — don't confuse).
- New non-iLink zone numbers should be **multiples of 256** to avoid colliding with iLink bits. Max zone number = **2,147,483,647**. Zone numbers/ids are effectively immutable once cards are encoded.
- **Ulsterbus Town Service zones can nest inside iLink zones.**

## Cross Border & transport mode
- **Cross Border Zone** covers the whole Republic of Ireland; used to decide where **alternative currency** applies. Multi-currency needs **both** the route's multi-currency attribute **and** boarding/alighting in the Cross Border Zone.
- **Rail vs bus for ABT capping is NOT done by zone** — it uses the **transport mode** setting in the ABT cap rule (e.g. cap bus-only across NI, exclude rail).

## Requirements
- REQ-0179.7 assign zone(s) to a stop; REQ-2280.0 create zone; REQ-2282.0 amend zone; REQ-2283.0 delete zone; REQ-2286.0 layer/overlap zones for area-specific fares/promotions.

## Suite implications
- Add **iLink validity-matrix** cases on validating devices (ETM/GV/PV/HHD): each card zone × each travel zone → valid/invalid per the table; specifically assert **Zone 4 valid in NW** and **NW invalid in 1/2/3**.
- Assert the **bitwise encoding** (e.g. Zone 2 card = 192) and that audit **Zone arrays carry Zone Numbers** matching the boarding/alighting stop (cross-check FBD-100658).
- Cover **ABT capping by zone** (Metro Network, Coleraine Triangle, etc.) AND **capping by transport mode** (rail excluded) — distinct mechanisms.
- Cover **Cross Border multi-currency** dependency on route attribute **+** boarding/alighting in the zone (neither alone enables it).
- Config/topology regression: assert new capping zone numbers are 256-multiples and don't collide with iLink bits.
