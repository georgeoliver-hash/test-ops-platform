# FS002 6.3 — Fare Pay Card (Stored Value & Ticket Product) (distilled)

**Source:** `NJT_FRFRP_FS002 - Fare Register Functional Specification.pdf`, section 6.3 "Fare
Pay card" (§6.3.1 Stored Value Process, §6.3.2 Ticket Product Processing), pp.60–76.
Distilled testable facts only — full spec held locally (see `REQS_DIR` / `tools/extract_req.py`),
not committed. Related sections owned by other notes: §6.1/6.2 (card acceptance, barcode
products/6.1.2), §6.4+ (Emergency Mode onward), §4.1.3 (rider class/transaction validity matrix) —
not covered here.

## Scope — how the Fare Register (FR) picks the flow
- The NJT Card Transaction (`$F4`) message carries a **'Ticket Type Pass'** field. `000000` →
  **Stored Value (SV)** transaction; any other value → **Ticket** (product/pass) transaction.
  (p.60)
- Both flows are further branched by the **'Transaction Approval Mode'** byte in `$F4`:
  - SV: `Waiting for Driver` / `Automatic` / `Waiting for NJT Card Validation Information` (p.60).
  - Ticket: `Waiting for Driver` / `Automatic` / `Waiting for zones` / `Waiting for Rider
    Classification and Zones` (p.68).

## §6.3.1 Stored Value Process

### 6.3.1.1 Waiting for Driver
- **Card accepted, online** (`$F4` NJT Card validation result = `0000`): FR shows a driver-confirm
  screen — Tx Result message, Product Type (hardcoded `"SV Transaction"`), Rider Class, TxType,
  Zone Information, SV Balance — plus a prompt that zones need not be entered. (pp.60–61)
  - Tx Result message = the 20-char ASCII string from `$F4`, unless the override flag is set →
    shows `"Override Required"`.
  - Rider Class from the `$F4` 'Rider Classification' byte; value `01` defaults to **Adult**.
  - Zone Information from 'OBV Start/End Zone'; if both zero, uses the FR's current
    boarding/alighting zones.
  - TxType is **One Way / Cont. Trip / Transfer** only, and is *derived*, not driver-set here:
    if `$F4` discount type = `14` **and** boarding zone == alighting zone → Transfer selected,
    else One Way. (p.61)
  - SV Balance shows the `$F4` card balance (online) or `"Offline"` (offline); negative shown as
    `-$x.xx`.
- Driver presses **Issue** (accept) or **C** (cancel). On accept, FR checks
  **`SV balance − fare ≥ Threshold`** (threshold from `$F4`, can be positive or negative).
  Insufficient funds → error shown, SV screen stays up for the driver to cancel (no retry-with-
  different-params in this mode — contrast §6.3.1.3). (p.61)
- **Sufficient funds** → FR sends `$E7` (ack type `00`, rider classification = value received from
  OBV, Boarding/Destination zones = `0000`, CT fare ticket flag = `00`); prints receipt + sends txn
  to CloudFare (GR-3, FRT-1, GR-12); passenger count on end-of-trip/run receipts updates, **fare
  value does not** (not driver-collected revenue); returns to ticket-issue screen. (p.62)
  - Fare value (receipt, only on OW, and audit) = OW fare for OBV Start/End Zone in `$F4`; if
    those are zero, OW fare for the zones shown on the SV screen. Transfer txns use the O/R
    transfer fare for the selected rider class.
  - Zone audited = 'OBV End Zone'; if zero, the alighting zone shown on the SV screen.
- **Cancelled** → no receipt/audit; `$E7` sent with ack `01`, rider classification `01`, zones
  `0000`, CT flag `00`; returns to ticket-issue screen.
- **Card accepted, offline**: same as online except SV Balance line shows `"Offline"`; **no
  sufficient-funds check performed**; no fare printed on any receipt; receipt gets 2 extra lines
  `"offline, please see | account for details"`. Offline scenario expects OBV Rider Classification
  = `01` (→ defaults Adult); no card balance available. (p.63)
- **Card rejected**: OBV validation result non-zero → FR shows details to the driver (for customer
  advisement only, no accept/reject choice). FR **also self-rejects** if 'Ticket Type' is unknown
  (not `029999`), regardless of OBV result. Denied screen shows the 20-char ASCII reason from
  `$F4`, or `"Unknown Product"` if the rejection was due to unknown Ticket Type; cleared by **C**.
  No receipt. `$E7` sent with ack `01`, rider classification `01`, zones `0000`, CT flag `00`.
  (p.63)

### 6.3.1.2 Automatic
- Same display as 6.3.1.1 (informational only — driver does not choose accept/reject).
- Card accepted (online **and** offline) → FR auto-accepts and performs 6.3.1.1's accepted actions,
  **except the insufficient-funds check is skipped** (FR is instructed to auto-accept regardless
  of balance). (p.63)
- Card rejected → same rejection process as 6.3.1.1, but FR auto-closes the rejection window
  (no driver action needed).

### 6.3.1.3 Waiting for NJT Card Validation Information
- **Card accepted, online**: same screen fields as 6.3.1.1, but here the **driver actively sets**
  zones, rider class and transaction type before accept/reject — this mode is the interactive one.
  (pp.64–65)
  - Boarding/alighting zone: up/down arrow keys (boarding) + zone-number entry + zone key
    (alighting) — screen updates live.
  - Rider Classification: 'class' soft keys, limited to **Adult / Child / Senior / Student**
    (Student unavailable if disabled in Service options).
  - Transaction type toggle via **'R4'** soft key between OW / CT / O-R Transfer:
    - **CT** selectable only if 'Enable ISSCTT' is set in service options **and** CT is a valid
      rider-class/transaction combination per §4.1.3 (out of this note's range — cite as pointer,
      **GAP**: the actual valid-combination matrix is not reproduced here).
    - **Transfer** selectable only if `$F4` discount type = `14` **and** the SV screen's current
      boarding/alighting zones are the same zone.
- Accept → same threshold check as 6.3.1.1. Insufficient funds → error shown, screen stays up, and
  **unlike 6.3.1.1 the driver may either cancel or change zone/rider-class/type and retry.** (p.65)
- Sufficient funds → `$E7` ack `00`, rider classification = value **shown on the SV screen**
  (driver-selected, not necessarily what OBV sent), Boarding/Destination zones = values entered on
  screen, **CT fare ticket flag = `01` if CT selected, else `00`**. (pp.65–66)
  - Fare value: OW = OW fare for rider class + the zones entered on-screen; Transfer = O/R
    transfer fare for selected rider class; **CT = Continue-Trip fare** for rider class + zones
    entered on-screen (a third fare basis not present in 6.3.1.1, since CT/Transfer toggle only
    exists in this mode).
  - Alighting zone audited = the zone entered on the SV screen.
- Cancelled → same pattern as 6.3.1.1 (ack `01`, rider class `01`, zones `0000`, CT flag `00`).
- Offline: same overrides as 6.3.1.1 (SV/Offline shows "Offline", no funds check, no fare printed,
  extra offline receipt lines, rider classification defaults Adult, no balance).
- Card rejected: same process as 6.3.1.1.

### 6.3.1.4 Rider Classification (OBV ↔ FR mapping)
**Incoming (OBV → FR)** (p.67, "Table – Incoming OBV to FR mapping"): Adult `01`→`1` Adult;
Child `02`→`2` Child; Senior `03`→`3` Senior; Disabled `04`→`3` Senior; Student `05`→`4` Student;
Senior/Disabled `10`→`3` Senior. (Multiple OBV codes collapse onto FR "Senior".)

**Outgoing (FR → OBV)** (p.68, "Table – Outgoing FR to OBV mapping") — **only used when approval
mode = `03` Waiting for NJT Card Validation Information; every other approval mode returns the
rider classification exactly as received from the OBV** (p.67): `1` Adult→`01`; `2` Child→`02`;
`3` Senior→`03`; `4` Student→`05`; `5` Employee — **N/A, not selectable** (no outgoing mapping,
by design); `6` Family and `7` Foreign — **GAP**: no outgoing OBV code is listed for these two FR
classifications; not stated whether they are simply never selectable/sendable in this flow or the
mapping was omitted. Confirm before asserting any FR→OBV behaviour for Family/Foreign.

### 6.3.1.5 Transaction Auditing (GR-1, GR-2, GR-3)
SV transactions audit as the paper-based equivalent product, with payment type **"Stored Value"**.
Fare value and alighting zone audited follow the description in the applicable approval-mode
section above (i.e., audit basis differs by mode — see 6.3.1.1/.2/.3). (p.67)

### 6.3.1.6 Receipt (GR-12)
Printed only when the SV transaction is accepted. Uses the paper-based product's ticket template;
product text = `*<Rider Class>`. Fare value printed follows the applicable approval-mode
description. **Fare is only printed on OW tickets**, and only when: online & mode = "Waiting for
NJT Card Validation Information"; OR online & mode = "Waiting for Driver" **and** OBV provided the
zones; OR online & mode = "Automatic" **and** OBV provided the zones. Zones printed = the zones
that were displayed on the SV screen. Offline transactions get the extra 2-line offline notice.
(pp.67–68)

### 6.3.1.7 Spotter Display
SV transactions show as **`<Class>*CARD`** on the spotter display. (p.68)

## §6.3.2 Ticket Product Processing
Invoked when `$F4` 'Ticket Type Pass' is non-zero. Same three-way approval-mode branch shape as
SV, but with two extra modes (**Waiting for zones**, **Waiting for Rider Classification and
Zones**) instead of SV's single interactive mode — reflecting that ticket products carry no
SV-balance/threshold concept and no OW/CT/Transfer toggle (see below).

### 6.3.2.1 Waiting for Driver
- Screen: Tx Result message, **Product Type**, **Rider Classification**, Zone Information,
  Offline Indicator (blank online / "Offline" offline) — **no SV Balance field** (tickets have no
  balance). Product Type + Rider Classification are looked up from the 'Ticket Type Pass' field
  (see §6.3.2.5). (pp.68–69)
- Accept → `$E7` ack `00`, rider classification = value received from OBV, zones = `0000`; print
  receipt + audit to CloudFare (GR-3, FRT-1, GR-12); **no fare value is ever printed or audited
  for a Ticket transaction** (key distinction vs SV, which prints/audits fare on OW). Zone audited
  = 'OBV End Zone', or the on-screen alighting zone if that is zero. Passenger count updates.
  (pp.69–70)
- Cancelled → no receipt/audit; `$E7` ack `01`, rider class `01`, zones `0000`.
- **Offline is not expected for Ticket transactions** ("it is considered that this will be for SV
  transactions only") — but if the offline flag is set anyway: Offline Indicator shows "Offline",
  **Product Type + Rider Classification are forced to Adult Monthly Pass regardless of the actual
  Ticket Type Pass value** (since an offline scenario is not expected to carry a valid value), and
  the receipt gets the offline notice lines. (p.70)
- Card rejected: as SV, **plus** FR also rejects if the 'Ticket Type Pass' is unknown **and** the
  transaction is online (the offline-unknown case is absorbed by the Adult-Monthly-Pass override
  above, not rejected). Denied reason shows "Unknown Product" for either unknown-Ticket-Type or
  unknown-Ticket-Type-Pass. (p.70)

### 6.3.2.2 Automatic
Same display; auto-accept/auto-close per 6.3.2.1's logic (no funds check applies to tickets in
either mode, since tickets carry no fare/balance concept). (p.71)

### 6.3.2.3 Waiting for zones
Same screen fields as 6.3.2.1 (no rider-class confirm — only zones are interactive here). Driver
sets boarding/alighting zone via the same arrow-key + zone-key entry (spec calls this widget the
"pop-up window" rather than "the SV/ticket transaction screen" in this mode — verify this is not
just inconsistent spec wording for the same UI before treating it as a distinct screen). Rider
classification on accept = value received from OBV (not driver-editable here). Zone audited = zone
entered on the pop-up. Offline-not-expected and card-rejected behaviour as 6.3.2.1. (pp.71–73)

### 6.3.2.4 Waiting for Rider Classification and Zones
Same screen fields; here the driver edits **both** zones **and** rider classification (same
Adult/Child/Senior/Student soft-key limits as SV's interactive mode). **No OW/CT/Transfer toggle
exists for ticket products** — the transaction type is implicit in the product itself, unlike SV's
§6.3.1.3. On accept: rider classification = value shown on-screen (driver-selected); zones =
values entered on-screen; alighting zone audited = the on-screen zone. Cancel / offline-not-
expected / card-rejected as 6.3.2.1. (pp.73–75)

### 6.3.2.5 Product Mapping
"The Ticket Type Pass to product mapping will be the same as per the barcode products. See
Barcode products in section 6.1.2." **GAP**: the actual product-code lookup table (what a Ticket
Type Pass value encodes — product/rider-class combination) lives in §6.1.2, outside this note's
line range/owner — do not fabricate specific code values here; cite §6.1.2's note for the table.
One stated rule that IS in-range: **Fare Pay card transactions use the 'paper' classes only** (as
opposed to whatever other class families §6.1.2 may define for barcode products). (p.75)

### 6.3.2.6 Transaction Auditing (GR-1, GR-2, GR-3)
Ticket transactions audit as the paper-based equivalent product, with payment type **"magnetic or
smart card pass"**. **GAP**: no rule in this range states how FR distinguishes "magnetic" vs
"smart card" for the payment-type value — confirm whether this is card-type-driven (unconfirmed
in-range) before writing an audit assertion that picks one. Alighting zone audited follows the
applicable approval-mode section. (p.76)

### 6.3.2.7 Receipt (GR-12)
Product text = `*<Rider Classification><transaction type>`, e.g. `"Adult Ticket Rx"`. **No fare
values are ever printed** for ticket products. Zones printed = the zones displayed on-screen.
Offline notice lines as elsewhere. (p.76)

### 6.3.2.8 Spotter Display
Ticket transactions **also** show as `<Class>*CARD` — **identical format string to SV** (§6.3.1.7).
The spotter display does not visibly distinguish an SV purse transaction from a Ticket product
transaction; flag as a coverage note, not a defect (spec states it plainly for both).

## Suite implications
- **SV vs Ticket at the top-level split**: assert `$F4` Ticket Type Pass `000000` → SV path, any
  other value → Ticket path — one case per branch, since downstream behaviour (fare printed?
  audited? balance shown?) diverges completely.
- **One case per approval mode per product family**: SV × {Waiting for Driver, Automatic, Waiting
  for NJT Card Validation Info} and Ticket × {Waiting for Driver, Automatic, Waiting for zones,
  Waiting for Rider Classification and Zones} — 7 flow-state cases minimum, each with accept +
  cancel + card-rejected sub-paths. Note that "Waiting for Driver" and "Automatic" reach the
  same result — retry-after-insufficient-funds only exists in the interactive SV mode
  (§6.3.1.3); confirm the suite does not assume it applies to §6.3.1.1/.2 too.
- **Insufficient-funds check** exists only for SV (threshold formula `SV balance − fare ≥
  Threshold`, threshold may be signed) — cover a case with a negative threshold and one where the
  check is skipped under Automatic mode.
- **Online vs Offline** per mode: Offline is explicitly expected for SV, explicitly **not**
  expected for Ticket (but must still be exercised defensively, since the spec defines forced
  fallback-to-Adult-Monthly-Pass behaviour for that unexpected case).
- **Rider classification mapping**: one case per incoming OBV code (01/02/03/04/05/10) → FR class,
  and one per outgoing FR→OBV code (1/2/3/4) exercised only under approval mode 03; explicitly
  assert Employee (5) is never sent to OBV; flag Family (6) / Foreign (7) as a gap-register item
  pending clarification (no outgoing mapping documented).
- **Zone-selection paths**: one case for "OBV supplies zones" (Start/End Zone non-zero) vs one for
  "OBV supplies zero, FR falls back to current boarding/alighting zones" — applies to every mode
  with a Zone Information field.
- **Transaction-type derivation vs selection**: SV §6.3.1.1/.2 *derive* OW/Transfer from discount
  type 14 + same-zone check (no driver choice); SV §6.3.1.3 lets the driver *toggle* OW/CT/Transfer
  with the CT-eligibility and Transfer-eligibility gating rules — cover both the derived and the
  driver-toggled path, plus the CT-disabled-by-service-options and Student-disabled-by-service-
  options negative cases.
- **Fare print/audit rules differ sharply between SV and Ticket** — Ticket products never print or
  audit a fare value under any mode; SV prints/audits fare only on OW (and only under specific
  online+mode combinations) — assert both the "fare shown" and "fare withheld" paths for SV OW,
  and assert Ticket product receipts never carry a fare line.
- **Spotter-display ambiguity** (`<Class>*CARD` for both SV and Ticket): treat as intentional per
  spec, not a defect — but flag if any existing case asserts spotter output implies product type.
- **Product-code mapping (§6.1.2) and CT-validity matrix (§4.1.3)** are out of this note's range —
  do not let this note's coverage checkpoints stand in for those; cross-reference the sibling notes
  covering those sections before calling Product Mapping coverage complete.
- **Payment-type "magnetic vs smart card" for Ticket audit** is an open gap (see §6.3.2.6) — log to
  the gap register before writing an assertion that picks one value.
