# POS suite restructure — Wave 2 complete (2026-06-04)

Suite: **`**NEW** POS-Acceptance Suite`** (id 30253), project TFTS - System Test (42).
Built off George's 22-point review (`review-notes-register.md`). Wave 1 (clear edits + adds) and
Wave 2 (bulk variation lines) are now applied and the suite **audits CLEAN** (0 blocking, 35
advisory/intentional). Edits were append-only, idempotent partial `update_case`s via
`tools/wave2_edits.py` — re-runnable safely.

## Wave 2 applied (49 case edits)

| Note | What | Cases |
|---|---|---|
| #18 | Green success banner outcome added to every ticket-issue case | 24 ticket cases |
| #6/#7 | Payment data-variation (Cash/Warrant/Card) on top-up + issue **product** cases. Metro products = Cash/Card only (no Warrant). | 18 cases |
| #9 | Adult/Child passenger-type variation on standard journey tickets | 6 cases |
| #8 | Half-Fare sub-types (Partially Sighted, Learning Disability, No Driving Licence) + DLA enumerated on entitlement case C4100427 (no new case — would duplicate) | 1 case |

### #9 judgement calls (Adult/Child)
Added to: C4100394, C4100395, C4100403, C4100404, C4100405, C4100420 (+ already on C4100393,
C4100419). **Deliberately NOT added** (specific product / passenger type — confirm if any should
get it): Seasons (C4100396/397), Warrant Returns (C4100398/422), Family & Friends
(C4100400/408/423), iLink (C4100401/410/421), Dependents Pass (C4100402), 3 Day Select (C4100399),
Bus Rambler (C4100407), Jobseeker (C4100409), Rail Substitution (C4100411), Cross-Border
(C4100503/504).

## Still needs George in the TestRail UI (API on this instance can't move or delete)

### 1. Bin the staged "Delete" section (65 cases)
- **13 review-driven removes** (`ZZ_DELETE_REVIEW`): C4099941 (pointless Operator Break),
  shared Bus FLU C4099982–986, Metro/FLU C4100379–383, rail Warrant issue-card C4100032,
  Metro sell-ticket C4100412.
- **52 created-in-error duplicates** (`ZZ_DELETE_DUP`): C4100445–496.

### 2. Move 2 cases (drag in UI)
- C4100025 *Issue Card — Metro Multi-Journey* and C4100029 *Issue Card — Metro Travelcard*
  → from `Functional / Issue Card / Issue from Blank` into **`Metro / Issue Card`** (target section
  already exists, empty, waiting).

### 3. Remove empty leaf sections (after the moves/bins)
- `Functional / Fare Look-Up / Bus (Ulsterbus / Metro)`
- `NIR (Rail) / Issue Card`
- `Metro / Fare Look-Up`
- `Metro / Tickets`
- `Delete / Functional` (and the whole `Delete` staging section once emptied)
- **Keep** `Metro / Issue Card` — it's the move target above.

## Optional / low-priority follow-ups
- #4: confirm whether there are >1 Ulsterbus Multi-Journey top-up product variants worth splitting
  out (currently one case, C4100392).

## Definition of done
`audit --suite 30253` → **CLEAN**; 35 advisory (13 bare product-name titles, 22 Screen-Validation
titles mirroring exact UI names) — all reviewed-intentional.
