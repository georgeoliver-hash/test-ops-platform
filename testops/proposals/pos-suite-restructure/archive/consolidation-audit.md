# POS suite — consolidation audit (2026-06-08)

Applying the flow/variation lens (`docs/test-practices.md` → "Structure by flow/risk, not by screen")
to the live POS suite (30253, 531 active). POS already has a separate `Screen Validation` per-screen
layer (282 cases) — so there is NO case-per-screen fragmentation. The opportunity is in the
**functional** layer: role/method and per-product cases that should be **data-variation lines**, plus
sign-on flow-steps.

## Sign On & Session (26 → ~11)
- **Sign On — by role × method (8 cases):** Operator/Supervisor/Technician/Administrator × manual/
  smartcard are the **same flow**. → FOLD to one "Sign On — by role (manual & smartcard)" with role +
  method as a variation line.
- **Sign-on Messages (4):** Message of the Day (+unavailable) + Word & Colour (+unavailable) are
  sign-on flow steps. → FOLD to one "Sign On — Message and Word & Colour of the Day" (unavailable as a
  branch step).
- **Idle & Screen + field-entry/'C' (3):** flow-step/screen detail. → FOLD into a single "Sign On —
  screen, field entry and 'C'".
- **Sign Off — by role (4):** Operator/Supervisor/Technician/Administrator. → FOLD to one "Sign Off —
  by role" (variation line). KEEP automatic-inactivity + power-cycle.
- **KEEP (distinct scenarios):** incorrect credentials, lockout-after-configured, unlock-with-
  Supervisor, Communication Locked, audit events.

## Top Up & Validation (23 → ~13)
- **Top Up per-product (8):** Metro Travelcard, Town Service, DayLink, iLink, Belfast Visitor, ABT,
  Monthly Season, half-fare/concession are the **same top-up mechanic** per product. → FOLD into
  "Top Up — top up a smartcard" with a product variation line.
- **KEEP:** cancel, Multi-Journey limit, expired-MJ-clears, mini-statement, non-toppable, all
  Validation (already-validated/hotlisted/time-band/entitlement/error-void), Faulty Card.

## Issue Card (11 → ~4)
- **Per-product issue (8):** Metro MJ, MJ, DayLink, iLink, Metro Travelcard, Belfast Visitor,
  Ulsterbus MJ, Town Service = same issue-from-blank mechanic per product. → FOLD into "Issue Card —
  issue from blank" with a product variation line. KEEP recognised-by-other-devices, blank-card-options.

## Operator (10 → ~8)
- **Ticket History (3):** view / details / scroll = one flow. → FOLD to "Ticket History — view, detail
  and paging". KEEP Break, Options, Totals, Excess (rail).

## Tickets (26) — DECISION NEEDED, default = LEAVE
The Tickets section is the **product catalogue** (Single, Day Return, Seasons, Warrant, Cross-Border,
per-mode variants), each with distinct fares/rules, deliberately built per-product in your POS review.
These are arguably **distinct products, not variations**. Options: (a) **LEAVE** as-is (recommended —
the per-product fare/rule coverage is the point); or (b) fold same-mechanic products into a "Tickets —
issue a ticket" with a product variation line (big reduction but loses per-product visibility).

## Projected
Functional ~250 → ~205 (Sign On −15, Top Up −10, Issue Card −7, Operator −2). Screen Validation (282)
and the mode sections unchanged. Tickets per the decision above. Absorbed cases retired
`ZZ_DELETE_REVIEW` into a `ZZ - To Delete` section; same recovery-safe, file-based push as ETM.
