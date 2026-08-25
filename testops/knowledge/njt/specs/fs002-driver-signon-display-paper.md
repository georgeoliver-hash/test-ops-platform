# FS002 — Driver Sign-on, Default Display & Paper Ticket Transactions (distilled)

**Source:** `NJT_FRFRP_FS002 - Fare Register Functional Specification.pdf` — Section 5 "Driver
Functionality" intro, 5.1 Sign on, 5.2 Default Display, 5.3 Paper Ticket Transactions (5.3.1–5.3.6).
Distilled testable facts only — raw spec held locally in `njt-requirements/`, not committed.
Covers lines 1425–3361 of the extracted text (pp.26–33). A parallel note covers 5.4 Operator Menu
onward — not duplicated here.

## Scope note — Full Service vs Exact Fare mode
- Two operating modes, set **per-route in configuration**: **Full Service** (FR used in isolation,
  driver handles cash) and **Exact Fare** (FR used with a Farebox, all money into the Farebox). p.26
- **Fallback rule:** on an Exact Fare route, if an operational Farebox is **not detected**, the FR
  **reverts to Full Service mode**. p.26 — candidate coverage: Farebox-absent boot/runtime behaviour.
- Function-availability table (mode-gated — worth asserting the gating, not just the happy path):

| Function | Full Service | Exact Fare |
|---|---|---|
| Sign on | Y | Y |
| Sum | Y | — |
| OBV Validation | Y | Y |
| Product Issue | Y | Y |
| Cancel Ticket | Y | — |
| Hold | — | Y |
| Pay Leave | Y | Y |
| Passenger Count | Y | Y |
| Driver Totals | Y | Y |
| Dump | — | Y |
| End Trip / End Run | Y | Y |
| Relief | Y | Y |
| Device settings | Y | Y |
| Paper Status | Y | Y |
| Driver Break | Y | Y |
| Supervisor/Audit reports | Y | Y |
| Accept Next bill | — | Y |
| Bus Inspection | Y | Y |
| Spotter Display | Y | Y |
| Colour of the day | Y | Y |
| Clear Bill Jam | — | Y |
| Wheelchair count | Y | Y |
| Non Payment Count | Y | Y |

(pp.26–27, split across two consecutive table pages.) **GAP** — this note only distils Sign on,
Default Display and Paper Ticket Transactions; the mode-exclusive functions (Sum, Cancel Ticket,
Hold, Dump, Accept Next bill, Clear Bill Jam) are named here for the gating table but their own
behaviour is specified later in the document (out of this note's line range) — do not treat as
covered by this note.

## 5.1 Sign on
- Trigger: driver presses **Issue key** while the **idle screen** is displayed → FR prompts for
  **Driver number** and **PIN**. p.27
- Validation: number+PIN checked against the **latest staff list from CloudFare**. Match → proceed
  to sign-on sequence. No match → FR tells the driver the details are incorrect and they must
  **re-enter**. p.27
- **GAP** — no stated limit on re-entry attempts (lockout/retry count not specified in this section);
  confirm on the live system / with the engineer before asserting a retry-limit behaviour.
- After PIN validation, driver enters, **in turn**: **Run, Line, Trip, Board Zone, Alight Zone,
  Class, Transaction**. Any invalid entry in a field → FR shows an **'invalid entry' error**, driver
  must **re-enter that field's data**. p.27
- Per-field validation rules (each is a distinct testable rule — valid, boundary, and invalid-value
  cases per field):
  - **Run** — 1–4 digit number for the assigned running board. p.27
  - **Line** — 1–4 digit number uniquely mapping to a route in the FR's loaded route files; driver
    can **scroll through available routes** with the up/down arrow keys (so entry can be by scroll,
    not only typed digits). p.27
  - **Trip** — 1–3 digit number for the trip being performed. p.27
  - **Board Zone** — 1–2 digit number; **only zone numbers valid for the selected Line (route)** are
    selectable — i.e. Board Zone validity is **conditional on the prior Line entry**. p.27
  - **Alight Zone** — 1–2 digit number; likewise **only valid zone numbers for the selected Line**
    are selectable. p.27
  - **Class** — selected via up/down arrow keys (not typed); **initial value shown = the last class
    set as default** (i.e. sticky from previous sign-on). p.27
  - **Transaction** — the default Transaction Type, selected via up/down arrow keys. **GAP /
    POSSIBLE SPEC INCONSISTENCY** — the spec's sentence describing the Transaction field's initial
    value literally repeats the Class field's wording verbatim ("The initial class displayed is the
    last class that was set as the default") rather than describing a "last transaction type"
    default; this reads as a copy-paste artifact in the source spec, not a confirmed statement that
    Transaction Type has no independent default-memory. Flag to the engineer via the gap register —
    do not assert either behaviour (sticky-default vs fixed-default) as fact until confirmed. p.27–28
- Completion: once Run/Line/Trip/Board Zone/Alight Zone/Class/Transaction are all entered, FR enters
  **ticket issue mode**; a **start-of-run receipt is printed**; FR sends **start-of-shift and
  start-of-trip audit records to CloudFare** (refs GR-3, FRT-1), a **start-trip message to the Clever
  Device** (ref GR-10), and — **if on an Exact Fare route** — an **enter-service command to the
  Farebox** (refs GR-10, FM-1). p.28. **GAP** — GR-3/FRT-1/GR-10/FM-1 are cross-references to other
  interface-spec sections/documents not covered by this note's line range; contents of those audit
  records/messages are not verified here — treat as pointers, not confirmed payload detail.

## 5.2 Default Display (ticket issue screen)
- Once in ticket issue mode, the **default display is the ticket issue screen**, refs FM-6, FM-10
  (cross-reference, not detailed in this range). p.29
- From this screen the driver can issue products and see connected-device state. Screen displays:
  - the current selected product issue details;
  - **if Exact Fare mode**: available funds inserted into the Farebox (refs FM-1, FM-5);
  - status indicators for connected equipment;
  - Colour of the Day information;
  - controls: change rider class (left-hand function keys), change transaction type (right-hand
    driver keys), change boarding zone (Λ/V keys), change alighting zone (type zone number + **Z**
    key). p.29
- **Suite-relevant distinction:** the "available funds" element is **Exact-Fare-mode-only** on this
  screen — a Full Service default-display test should assert its **absence**, not just that Exact
  Fare shows it.

## 5.3.1 Change product parameters
- **Rider class** — select desired class from the left side of the screen. For keys offering **more
  than two** class options, the **second option** is reached via **'A' then the class soft key**
  (a shift-style secondary selection). refs FF-1, FRT-2. p.29
- **Transaction type** — select from the right side of the screen; **P** and **N** keys scroll
  up/down the transaction-type list. **Only transactions allowed for the route are displayed** (see
  section 4.1.4 — out of this note's range; cite as a cross-reference gap if asserting the allowed-set
  logic). p.29
- **Boarding zone** — Λ/V key, or numeric value then Λ/V, sets boarding zone to the entered value.
  On lines where zone values **increment** during the trip, **Λ** advances to the next zone; on lines
  where zone values **decrement**, **V** advances to the next zone. (Direction-dependent key mapping
  — a concrete boundary/negative-path test target: using the "wrong" key for the line's zone
  direction.) p.29–30
- **Alighting zone** — numeric entry then the **'Zone' key**. p.30
- **CLEAR key** — resets **alighting zone, class, and transaction type** back to the values entered
  by the driver during sign-on. Note: **boarding zone is not listed** as reset by CLEAR — worth
  confirming (possible gap) whether that's deliberate or an omission. p.30

## 5.3.2 Product Issue — Full Fare
- Once parameters are set, FR shows the configured price for those parameters on the default display
  (ref FRT-3); driver presses **ISSUE** to issue. p.30
- On issue: audible confirmation sounds; transaction data audited to CloudFare (refs GR-1, GR-2,
  GR-3, FRT-1); receipt printed (ref GR-12); if a Clever Device is connected, a transaction-detail
  message is sent to it (ref GR-10). p.30
- **Invalid zone combination:** a boarding/alighting pair defined as a **zero reference fare** in the
  fare table shows **"Error"** for the fare; **no ticket/receipt can be issued** to these
  destinations, and FR shows an error if issue is attempted. p.30 — concrete negative-path test.

## 5.3.3 Product Issue — Exact Fare
- FR only allows issuance if **sufficient funds** are in the Farebox; FR **polls the Farebox
  continuously** so inserted funds register immediately (refs GR-1, GR-10); available funds are
  shown alongside product details. p.30
- Price is shown on the default display (ref FRT-3) once parameters are set; driver presses **ISSUE**.
  - **Funds ≥ price** → product issued.
  - **Funds < price** → **"not enough money" error** shown + error tone sounded (no issue). p.30–31
- On successful issue: audible confirmation; transaction audited to CloudFare (refs GR-1, GR-2,
  GR-3, FRT-1); receipt printed (ref GR-12); a transaction-detail message is sent to the Farebox which
  **decrements the transaction value from available funds** (refs GR-1, GR-10); if connected, a
  transaction-detail message goes to the Clever Device (ref GR-10). p.31
- Same **invalid zero-fare zone combination** rule as Full Fare applies (Error shown, issue blocked).
  p.31
- **Timing rule:** **60 seconds** after the last money inserted into the Farebox, an **automatic dump
  transaction occurs** — any pending transaction(s) must be **finalised within that window**. p.31
  — a concrete timing/negative-path test (attempt to finalise after the 60s dump).

### 5.3.3.1 Accept
- Purpose: allows the driver to issue a product even with **insufficient Farebox funds**, in certain
  (unspecified-here) circumstances. **GAP** — "certain circumstances" is not enumerated in this
  section; confirm with the engineer what governs when Accept is permitted vs. blocked before writing
  a precondition-gated test.
- Mechanism: press **'A' then Issue** (rather than Issue alone). Product issues **at the value of the
  farebox money actually received**; an **underpayment record** is recorded and **printed on the
  receipt**. p.31
- **Precondition:** the FR must be **registering at least one cent** from the Farebox for Accept to
  work (i.e. $0.00 received → Accept unavailable/fails) — explicit boundary test. p.31
- On Accept issue: audible confirmation; transaction data **including both the full fare and the
  accepted value** audited to CloudFare (refs GR-1, GR-2, GR-3, FRT-1); receipt printed **showing the
  accepted fare value** (ref GR-12); Farebox decrement message sent (refs GR-1, GR-10); if connected,
  **two** Clever Device messages sent — one for the ticket class/full price, a second for the accept
  class and actual money taken (ref GR-10). p.31–32 — note the **dual-message** behaviour is a
  distinct assertion from the single-message Full/Exact Fare issue paths above.

## 5.3.4 Special Transaction Sequences
General rule: selected Transaction Type shows a fare for the trip, or **zero** if a fare-media ticket
is being received; **ISSUE** completes the transaction. Certain transaction types instead allow/require
a **manually entered fare** — six named sequences, each a distinct scenario family:

- **Override** — passenger travelling further than their original transaction covers. Fare entered
  via numeric keys, then **ISSUE**. **Passenger count is NOT incremented.** p.32
- **Special** — passenger paying cash for a special ticket. **Last Special fare issued** is shown
  initially (sticky default); value can be changed via numeric keys; **ISSUE** completes. **Range:
  $0.00 to $650.00.** p.32 — boundary test at both ends plus an out-of-range negative case.
- **Monthly and Rail Pass (override)** — for a pass not valid for all zones travelled, an override
  lets the driver enter the **excess fare** via numeric keys; **ISSUE** prints a receipt including
  the excess fare. **Range: $0.01 to $650.00** (note: lower bound differs from Special — **not**
  $0.00-inclusive here). p.32 — boundary test, and explicitly assert the $0.00 case is invalid for
  this sequence (distinguishing it from Special's $0.00-valid case).
- **Override Transfer** — issued **after** the initial transaction is completed, via the **O/R Tfr**
  key. Display shows the transfer value; driver selects the destination zone to issue. **Passenger
  count is NOT incremented.** p.32–33
- **Override No Charge Transfer** — issued after the initial transaction, via **A key then NC
  Transfer key**. **Passenger count is NOT incremented.** p.33
- **Counterfeit ticket** — driver suspects a counterfeit monthly pass presented for inspection;
  recorded via **A key then Monthly Pass** (shifted option); transaction type displays as **MPass\***
  while flagged. Pressing **ISSUE** completes the Monthly Pass transaction as normal AND sends an
  **event to CloudFare** recording suspected counterfeit usage (refs GR-3, FRT-1); FR then **defaults
  back to standard MPass** transaction type. If a Clever Device is connected, a counterfeit-ticket
  message is sent to it (ref GR-10). p.33 — two assertions worth separating in tests: (1) the
  transaction itself still completes normally, (2) the counterfeit event/flag is a side-channel audit
  signal, not a block.

## 5.3.5 Wheelchair counter
- Driver logs a wheelchair-user boarding via a **shifted number-1 key** (e.g. "A+1"). Sends an
  **"event" message to CloudFare** (refs GR-3, FRT-1) to log the wheelchair user. p.33
- Explicit exclusions — all three are distinct negative assertions:
  - **NOT included in the passenger count.**
  - **NOT included in any end-of-trip/run reports.**
  - **No message sent to the spotter display.** p.33

## 5.3.6 Non Payment counter
- A new **'pass' transaction** accounts for passengers who **refuse to pay** when boarding.
  **Issued/audited as per a normal pass product** (i.e. not a separate audit path). p.33
- Exceptions vs. a normal pass transaction — again distinct negative assertions:
  - **No receipt is printed** for this transaction type.
  - **Spotter display shows only the passenger count** (i.e. **no class or transaction** shown on
    spotter display for this type). p.33

## Suite implications
- **Mode-gating:** add/confirm cases asserting Full-Service-only and Exact-Fare-only functions are
  genuinely unavailable in the other mode (per the table on pp.26–27), and the **Farebox-not-detected
  → revert to Full Service** fallback on an Exact Fare route.
- **Sign-on field validation:** one case family per field (Run, Line, Trip, Board Zone, Alight Zone,
  Class, Transaction) covering valid range, boundary, and invalid-entry re-prompt; explicitly cover
  the **Board/Alight Zone depends on selected Line** conditional-validity rule, and Line-selection by
  **scroll** vs typed entry.
- **GAP to route to engineer (gap register):** the Class/Transaction "last default" wording collision
  at p.27–28 — confirm whether Transaction Type retains its own sticky default or the spec sentence is
  a copy-paste artifact, before writing an assertion either way.
- **GAP to route to engineer:** sign-on PIN retry/lockout behaviour is unspecified in this section —
  confirm whether a retry limit exists.
- **Default display:** assert Exact-Fare-only "available funds" element is present in Exact Fare and
  **absent** in Full Service on the ticket-issue screen.
- **Change-product-parameters:** cover the Λ/V **direction-dependent** zone-advance behaviour (wrong
  key for the line's increment/decrement direction), the 'A'+class-key path for >2-option class keys,
  and confirm/flag whether **CLEAR** resetting boarding zone (not just alight/class/transaction) is a
  gap or intentional.
- **Full Fare & Exact Fare issue:** cover the zero-reference-fare "Error" zone-combination block
  (both modes); Exact Fare "not enough money" error path; the **60-second auto-dump** finalisation
  window as a timing/negative case.
- **Accept:** cover the $0.00-received-blocks-Accept boundary, the underpayment-record-on-receipt
  content, and the **dual Clever Device message** behaviour (distinct from single-message normal
  issue) — and route the "certain circumstances" precondition gap to the engineer before asserting
  when Accept is/isn't allowed.
- **Special Transaction Sequences:** one case family per named sequence (Override, Special, Monthly/
  Rail Pass override, Override Transfer, Override No Charge Transfer, Counterfeit) — explicitly test
  the **differing fare ranges** ($0.00–$650.00 for Special vs $0.01–$650.00 for Monthly/Rail Pass
  override) and the **passenger-count-not-incremented** rule for Override / Override Transfer /
  Override No Charge Transfer. For Counterfeit, assert both the normal-completion and the
  side-channel CloudFare event independently.
- **Wheelchair counter:** assert all three exclusions (passenger count, end-of-trip/run reports,
  spotter display) as separate negative checks, not one combined assertion.
- **Non Payment counter:** assert no-receipt and spotter-display-count-only-no-class/transaction as
  separate negative checks; confirm it otherwise audits identically to a normal pass product (cite
  case ids if an existing "normal pass" case is reused as the baseline to diff against).
- **Cross-reference gaps (not verified in this note — flag if any existing case asserts contents):**
  GR-1/GR-2/GR-3/FRT-1/FRT-2/FRT-3/GR-10/GR-12/FM-1/FM-5/FM-6/FM-10/FF-1 and section 4.1.4
  (route-allowed transaction types) are all pointers into other spec sections/interfaces outside this
  note's line range — their payload/behaviour detail is not confirmed here.
