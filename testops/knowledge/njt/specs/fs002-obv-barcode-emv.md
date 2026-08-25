# FS002 §6.1–6.2 — OBV Barcode & EMV Transactions (distilled)

**Source:** `NJT_FRFRP_FS002 - Fare Register Functional Specification.pdf` — Section 6 "OBV
functionality" intro, §6.1 Barcode (Overview, Barcode products, Transaction Process, Transaction
Auditing, Receipts/Fare Media, Spotter Display), §6.2 EMV Transactions (Overview, Transaction
Process, Transaction Auditing, Receipt, Spotter Display). Raw text extracted lines 6357–8776 of
`njt-requirements/_text/NJT_FRFRP_FS002 ....pdf.txt`. Page citations below are the nearest PDF page
footer (`Page N`) in the extracted text; some page boundaries are inferred (footer = end of that
page's content) since exact PDF pagination markers don't align 1:1 with heading breaks.
Related sections referenced but **out of scope** here (covered elsewhere): §4.1.3 (rider
class/transaction-type valid combinations, referenced by the CT toggle rule below), doc [3] (RS485
Fare Register–OBV interface spec), §6.3 Fare Pay card onward (another agent's scope).

## Interface overview
- Infigo 4 Fare Register interfaces to the Conduent OBV to validate **barcode**, **NJ Fare Pay smart
  card**, and **contactless bank (cEMV) cards** (NJT_FRFRP_FS002 p.46, GR-10).
- For all three media types: OBV validates the media first, then sends details to the Fare Register
  for the driver to amend or validate the transaction (p.46).
- Fare Register–OBV transport is RS485, detailed in a separate referenced doc [3] (p.46) — not
  expanded in this excerpt.

## 6.1 Barcode

### Overview (p.46)
- OBV scans barcodes present on all NJ Transit paper tickets/passes **and** barcodes available
  through the NJT mobile app.
- On scan, OBV validates the ticket details and sends the result to the Fare Register.
- Fare Register displays a screen for the driver to view the result, finalize the transaction, and
  issue any required fare media.

### Barcode products / ticket-type mapping (p.46–49)
- The barcode product is derived from the **Ticket Type** field provided by the OBV in the
  Transaction (`$F1`) record, via a lookup table.
- Each table row maps: **OBV Ticket Type code(s)** → descriptive Ticket/Rider Class label → **Paper
  product code** → **MyTix (mobile) product code** (`n/a` where no mobile equivalent exists).
- The table is organized by fare category: Bus tickets/passes, City Subway tickets/passes,
  RiverLine, Rail Passes, HBLR — plus a second supplemental table of ticket types added since the
  2019 initial delivery (p.48–49).
- **Not transcribed verbatim** — it is a large lookup table spanning p.46–49 of the spec
  ("Barcode products" table, §6.1.2). Reference the source spec directly for the authoritative
  code-to-product mapping when building/validating specific test data.
- **GAP:** in the supplemental (post-2019) table, a large number of OBV Ticket Type codes are
  labeled **"Unknown"** as their own Ticket/Rider Class description in the spec itself (e.g. codes
  315, 12010, 21201, 23201, 31001, 32001, etc., p.48–49). This is not an extraction artifact — the
  spec provides no descriptive name for these codes, only their paper/MyTix product-code mapping.
  Needs engineer confirmation: are these codes actually sent by the OBV in production, and if so
  what product/rider-class should a test assert is recorded?

### Transaction Process — Waiting for Driver (p.50–53)
**Barcode Accepted:**
- If OBV validates the barcode as acceptable for travel, Fare Register displays details for the
  driver to acknowledge/complete the transaction.
- Displayed fields: **Transaction Result**, **Passenger 1 of n**, **Ticket Type**, **Rider Class**,
  **Zone Information**; plus a prompt for driver input if a continue-trip, transfer, or override is
  required (p.50).
- `[Transaction Result]` = "Transaction OK" or "Override Required", per the override flag in the
  OBV message (p.50).
- `[Ticket Type]`, `[Rider Class]`, `[Zone Information]` populated from OBV-supplied data (p.50).
- **Zone display vs. zone audit split (p.50–51):** the zone info shown to the driver is derived from
  the **"barcode start zone"/"barcode end zone"** fields in the `$F1` message; the zone info that is
  **audited** uses the **"OBV start zone"/"OBV end zone"** fields in the *same* `$F1` message — i.e.
  displayed and audited zones are sourced from two different field pairs and are not guaranteed
  identical. **GAP:** the spec doesn't state when/why these two pairs would diverge or which is
  authoritative for fare purposes — flag for engineer confirmation.
- Driver presses **Issue** to accept or **C** to cancel (p.51).
- If accepted: Fare Register sends a transaction acknowledgement to the OBV; prints receipt/fare
  media (GR-12); records the transaction to CloudFare (GR-3, FRT-1, p.51). **Multi-passenger:** driver
  must press Issue for **each** passenger; Fare Register prints media and sends a **separate** audit
  record per passenger (GR-3, FRT-1, GR-12, p.51–52).
- If **C** pressed (needs modifying): Fare Register sends ack to OBV; returns to ticket issue screen;
  driver sets the required product parameter (Continued Trip / Transfer / Override); driver presses
  Issue to finalize; multi-passenger requires issuing individually per passenger (p.51–52).
- Configurable **auto-accept-after-timeout** option exists (p.52).

**Barcode Rejected (p.53):**
- If OBV determines the barcode invalid, Fare Register displays a rejection message with the
  **denied reason** = the 20-character ASCII string in the `$F1` message from the OBV.
- Closed by pressing **C**. **No receipt printed** for a failed transaction. An acknowledgement is
  sent to the OBV when C is pressed.

### Automatic acknowledgment (p.53)
- If the transaction-approval byte in the `$F1` message is `'01'`, Fare Register displays the same
  details for driver awareness, then **automatically accepts** the transaction, performing the same
  actions as the accepted-transaction flow above.
- For multiple-passenger transactions, each transaction is auto-approved in turn.
- **GAP (ambiguous cross-reference):** the source text says this performs "the actions as per
  section 6.1.2.1" — but no subsection 6.1.2.1 exists in the read structure (6.1.2 is "Barcode
  products", not further subdivided). This almost certainly means the Barcode-Accepted flow under
  §6.1.3.1, but the spec's own cross-reference is wrong/stale. Confirm intended target with the
  spec owner before relying on it for exact behaviour.

### Transaction Auditing (p.53)
- Transactions recorded as the product type looked up from the §6.1.2 table (GR-1, GR-2, GR-3).
- If the transaction record indicates the barcode came from a mobile device, the **MyTix**
  equivalent product is used; otherwise the **paper-based** product is used.
- Payment type recorded as **"barcode usage"**.

### Receipts/Fare Media (p.53) — GR-12
- Receipt/fare media printed per the equivalent paper product when a barcode transaction is
  accepted:
  - Receipt gets a **`*` prefix** before the product information, indicating OBV validation.
  - Zones printed = boarding/alighting zones **received in the `$F1` message from the OBV**.
  - Tickets issued directly by the Fare Register (non-barcode) instead use the **default zone
    information set on the Fare Register**.

### Spotter Display (p.54)
- Barcode transactions corresponding to **MyTix** products show on the spotter display with a
  **`*` prefix** before the transaction type (e.g. `*XTKT`).
- **Paper-based** barcode transactions show **without** the asterisk.

## 6.2 EMV Transactions

### Overview (p.54)
- OBV supports validation of cEMV (contactless bank) cards. If OBV decides a card is valid for
  travel, Fare Register displays a screen for the driver to set the alighting zone (if required) and
  acknowledge or cancel.

### Transaction Process (p.54)
- Processing depends on the **'Transaction Approval Mode'** byte in the EMV Transaction (`$F3`)
  message: **Waiting for Driver**, **Automatic**, or **Waiting for EMV Validation Information**.

**Waiting for Driver — Card accepted (p.54–56):**
- Triggered when `$F3` 'Card acceptance result' = `0000`.
- Screen shows: **Tx Result message**, **Product Type**, **Rider Class**, **TxType**, **Zone
  Information**; plus a prompt that zones are not required for this transaction.
  - `[Tx Result message]` = 20-char ASCII string from `$F3`.
  - `[Product Type]` hardcoded to **"EMV Transaction"**.
  - `[Rider Class]` assumed **Adult (default)** — not sent in `$F3`.
  - `[TxType]` can only be "One Way" or "Cont. Trip"; One Way is always the default displayed.
  - Zones not supplied by OBV for EMV — screen uses the **current boarding/alighting zones set on
    the Fare Register**.
- Driver presses **Issue** (accept) or **C** (cancel).
- **If accepted:** Fare Register sends EMV Transaction Approval (`$E6`) to OBV — ack type `00`,
  Boarding/Destination zones `0000`, CT fare ticket flag `00`, Rider Classification `01`. Prints
  receipt + sends txn record to CloudFare (GR-3, FRT-1, GR-12). **Receipt does NOT include a fare
  value.** Fare value recorded in audit data = the **Adult OW fare for the current boarding/alighting
  zones set on the Fare Register**. Adult passenger count on end-of-trip/run receipts is updated, but
  fare value is **not** (not revenue paid in by the driver). Returns to ticket issue screen.
- **If cancelled:** `$E6` ack type `01`, zones `0000`, CT flag `00`, Rider Class `01`. **No receipt,
  no audit record.** Returns to ticket issue screen.

**Waiting for Driver — Card rejected (p.55–56):**
- Triggered when `$F3` 'Card acceptance result' is non-zero, **or** when the 'Ticket Type' field is
  unknown (not `029899`) **regardless of Card acceptance result** — this second condition is a
  Fare-Register-side rejection independent of the OBV's own decision.
- Denied reason = 20-char ASCII string from `$F3`, **except** overridden to **"Unknown Product"**
  when the Ticket Type sent is unknown.
- Closed via **C**. No receipt printed, only a message shown. `$E6` sent: ack type `01`, zones
  `0000`, CT flag `00`, Rider Class `01`.

**Automatic (p.56–57):**
- Same accept/reject triggers as Waiting-for-Driver; screen shown for driver awareness only (no
  Issue press needed) — Fare Register automatically performs the accepted/rejected actions above and
  auto-returns to the ticket issue screen.
- Multi-passenger: n/a to this mode's description (EMV is single-card-tap; no multi-passenger note
  given in this section).

**Waiting for EMV Validation Information (p.57–58):**
- Triggered when `$F3` 'Card acceptance result' = `0000`; driver additionally confirms **zones,
  rider type, and Continue-Trip requirement** before accept/reject.
- Screen shows same field set (Tx Result, Product Type, Rider Class, TxType, Zone Information) plus
  a confirm prompt.
  - `[Rider Class]` field is limited to **10 characters**.
  - Zones default to current Fare Register boarding/alighting zones as the **initial selected**
    values — driver can change via standard zone-change keys (up/down arrows set boarding; zone
    number + zone key sets alighting). Screen updates live. **The zone set on the ticket-issue screen
    itself is unaffected** — the EMV screen's zone selection is local to this transaction.
  - Rider Classification selectable: **Adult, Child, Senior, Student** (Student unavailable if
    disabled on the current route).
  - OW/CT toggle available **only** on services with "Enable ISSCTT" set in service options, **and**
    only if CT is a valid rider-class/transaction-type combination per §4.1.3 (out of this excerpt's
    scope — external dependency).
- Driver presses Issue (accept) or C (cancel).
- **If accepted:** `$E6` — ack type `00`, Boarding/Destination zones = values entered on the EMV
  screen, CT fare ticket flag `00` if One Way / `01` if Cont. Trip, Rider Classification `01` Adult /
  `02` Child / `03` Senior / `05` Student. Receipt + CloudFare record sent (GR-3, FRT-1, GR-12); **fare
  value only printed on OW receipts**. Fare value on receipt (if applicable) and in audit data = fare
  for the **rider class, transaction type, and zones entered on the EMV screen**. Passenger count for
  the selected rider class is updated on end-of-trip/run receipts; fare value is not (not revenue
  paid in by the driver). Returns to ticket issue screen.
- **If cancelled:** no receipt, no audit record. `$E6` ack type `01`, zones `0000`, CT flag `00`,
  Rider Class `01`. Returns to ticket issue screen.
- **Card rejected:** same process as Waiting-for-Driver rejection above.

### Transaction Auditing (p.59)
- EMV transactions audited as the **paper-based equivalent product**, but payment type recorded as
  **"Credit Card"** (GR-1, GR-2, GR-3).
- Fare value audited = value for the **rider class and transaction type selected**, for the **zones
  that were displayed on the EMV transaction screen** (whether driver-entered, in the Waiting-for-
  EMV-Validation-Information flow, or defaulted to current Fare Register zones for zones-not-required
  transactions).

### Receipt (p.60) — GR-12
- Receipt uses the ticket template of the paper-based equivalent product:
  - Product text set to **`*<rider class>`**.
  - **Fare value only printed on OW receipts**; for "driver approval" (Waiting for Driver) and
    "Automatic" transactions the fare value is **not printed at all** (these are zones-not-required
    modes). For "Waiting for Zones" (i.e. Waiting for EMV Validation Information) transactions, the
    printed OW fare value = the fare for the rider class and zones displayed on the EMV screen.
  - Zones printed = the zones displayed on the EMV transaction screen (driver-entered, or default
    Fare Register zones if a zones-not-required transaction).

### Spotter Display (p.60)
- EMV transactions show as **`<rider class>*CARD`** on the spotter display.

## Gaps flagged (need engineer/BA confirmation before writing/asserting cases)
1. **Ambiguous cross-reference** in §6.1.3.2 Automatic acknowledgment — points to "section 6.1.2.1"
   which does not exist in this structure; almost certainly means the Barcode-Accepted flow under
   §6.1.3.1, but not stated explicitly (p.53).
2. **Undocumented "Unknown" ticket-type codes** in the post-2019 supplemental barcode-product table
   (p.48–49) — dozens of OBV codes have no descriptive rider-class/ticket label in the spec, only a
   product-code mapping. Cannot assert expected on-screen "Ticket Type"/"Rider Class" text for these
   without a real definition.
3. **Barcode zone display vs. zone audit source fields differ** ("barcode start/end zone" shown to
   driver vs. "OBV start/end zone" audited) with no stated rule for when/why they'd diverge (p.50–51).
4. **OW/CT toggle validity** in the EMV "Waiting for EMV Validation Information" flow depends on
   §4.1.3 rider-class/transaction-type combination rules, which are outside this excerpt — treat as
   an external dependency to pull in before writing that specific case.

## Suite implications
- **Barcode — Waiting for Driver, accepted:** assert display fields (Transaction Result, Passenger
  n of n, Ticket Type, Rider Class, Zone Info); "Transaction OK" vs "Override Required" per OBV
  override flag; Issue→ack+receipt+CloudFare record; C→return to issue screen + product-parameter
  entry (Continue Trip/Transfer/Override) + per-passenger re-issue.
- **Barcode — multi-passenger:** dedicated case for per-passenger Issue press, separate media print
  and separate audit record for each passenger, both in direct-accept and C-then-modify paths.
- **Barcode — automatic acknowledgment ($F1 approval byte = 01):** auto-accept without driver Issue
  press; multi-passenger auto-approved in turn — likely under-covered vs. the driver-confirm path.
- **Barcode — rejected:** denied-reason string display (20-char ASCII from `$F1`), C to close, no
  receipt printed, ack still sent to OBV.
- **Barcode — zone display vs audit source:** a case that specifically distinguishes the
  driver-visible zone (barcode start/end zone) from the audited zone (OBV start/end zone) — flag as
  a probable coverage gap given the spec's own ambiguity here (see Gap 3).
- **Barcode — auditing:** product = table lookup (MyTix if mobile-sourced, else paper); payment type
  = "barcode usage".
- **Barcode — receipts:** `*` prefix present; zones = `$F1` OBV zones, vs. FR-default zones for
  non-barcode tickets.
- **Barcode — spotter display:** `*` prefix for MyTix-derived transactions (e.g. `*XTKT`) vs. no
  prefix for paper-based.
- **Barcode product mapping:** spot-check representative codes across each category (Bus, City
  Subway, RiverLine, Rail Pass, HBLR, plus a couple of post-2019 additions) rather than exhaustively
  testing every table row; explicitly flag the "Unknown"-labeled codes (Gap 2) as needing a defined
  expected result before they can be tested meaningfully.
- **EMV — Waiting for Driver, accept/cancel/reject:** assert exact `$E6` response field values (ack
  type, Boarding/Destination zones, CT fare flag, Rider Classification) for each of the three
  outcomes; receipt has no fare value; audited fare = Adult OW fare at current FR zones; passenger
  count updates without fare value on cancel/no-count-on-reject.
- **EMV — reject via unknown Ticket Type:** a dedicated case for the Fare-Register-side rejection
  (Ticket Type ≠ 029899) independent of the OBV's Card acceptance result, asserting the
  "Unknown Product" override text.
- **EMV — Automatic mode:** confirm accept/reject actions match Waiting-for-Driver but without a
  driver Issue press, and auto-return to ticket issue screen.
- **EMV — Waiting for EMV Validation Information:** driver zone adjustment (independent of the
  ticket-issue screen's own zone), Rider Classification selection incl. Student-disabled-by-route
  exclusion, OW/CT toggle gated by ISSCTT + §4.1.3 combination validity (Gap 4), `$E6` field mapping
  per rider class code (01/02/03/05) and CT flag (00/01), fare printed only on OW receipts.
- **EMV — auditing:** payment type = "Credit Card"; fare = rider class/type/zones as shown on the
  EMV screen (not necessarily the FR's current zones, if driver-adjusted).
- **EMV — receipt:** product text `*<rider class>`; fare value printed only for OW under the
  "Waiting for Zones" mode — not for driver-approval/automatic modes at all.
- **EMV — spotter display:** `<rider class>*CARD` format.
