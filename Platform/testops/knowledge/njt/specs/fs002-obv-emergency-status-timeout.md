# FS002 — OBV Emergency Mode, OBV Status, Communication Loss, Transaction Timeout (distilled)

**Source:** `NJT_FRFRP_FS002 - Fare Register Functional Specification.pdf` — sections 6.4 Emergency
Mode, 6.5 OBV Status, 6.6 Communication loss, 6.7 Transaction Timeout (extracted text lines
13258–13905). Raw spec held locally in `njt-requirements/`, not committed.
Distilled testable facts only — every fact below is cited to a page (`NJT_FRFRP_FS002 p.N`).

## 6.4 Emergency Mode — entry/exit messaging to Driver
- **Entry:** when the Fare Register (FR) **first** sees the OBV status bit for Emergency Mode set,
  it displays a message to the Driver stating that products from **other Operators should be
  accepted** because a defined emergency scenario exists. (`NJT_FRFRP_FS002 p.77`)
- **Clear/ack:** that entry message is cleared only by the **Driver pressing the C key**. No further
  Driver action beyond the standard emergency-mode handling procedure is expected once acknowledged.
  (`NJT_FRFRP_FS002 p.77`)
- **Exit:** once Emergency Mode is no longer active on the OBV (status bit cleared), a **second**
  message is displayed telling the Driver the system has reverted to normal operational mode; this
  is also cleared by pressing **C**. (`NJT_FRFRP_FS002 p.77`)
- **GAP** — the spec does not state in this section whether a *second, later* Emergency Mode entry
  (bit set again after having been cleared) re-triggers the entry message, or only the very first
  transition per session/trip is described ("first sees this status bit set" — ambiguous whether
  "first" means first-ever or first-per-occurrence). Confirm on the live system / with the engineer.

## 6.5 OBV Status — status bar indicator table
The FR displays a status-bar indicator derived from an 8-bit "OBV Status Part 1" byte plus an
"OBV Status Part 2" (bit 7 + bits 6–0) value, per a scenario table. The scenario descriptions are
legible in the extracted text; the bit-level column values are not reliably recoverable (see gap
below). Legible scenarios (`NJT_FRFRP_FS002 p.78`–`p.79`):
- OBV is **not communicating** with the FR → status bar shows **N/A**. (p.78)
- OBV is communicating, **no issues**, FR is on a trip → status bar shows **N/A**. (p.78)
- OBV is communicating and indicating it **has a fault** → status bar shows **N/A**. (p.78)
- OBV is communicating and indicating it is **not in service** while FR is on a trip → status bar
  shows **N/A**. (p.78)
- OBV is communicating and indicating it is **not in validation mode** while FR is on a trip →
  status bar shows **N/A**. (p.78)
- OBV is communicating and indicating it is operating in **Emergency Validation mode** → status bar
  shows **N/A**. (p.78)
- OBV is communicating and indicating it is operating but has **no GPS** → status bar shows **N/A**.
  (p.79)
- OBV is communicating and indicating it is operating but has **no screen display** (spec notes: no
  documented feature lets the FR specifically turn this on/off) → status bar shows **N/A**. (p.79)
- OBV is communicating, **not in service**, no fault, but **in maintenance mode** → status bar shows
  **N/A**. (p.79)
- OBV is communicating, **not in service**, no fault, and **FR is not in service** → status bar shows
  **N/A**. (p.79)
- Explicit closing rule: statuses relating to **Emergency Mode, lack of GPS, and lack of screen
  display are ignored from the top-line status indicator** (i.e. excluded from whatever summary/top
  status the FR otherwise shows, distinct from the per-scenario status-bar column above).
  (`NJT_FRFRP_FS002 p.79`)
- **GAP** — the per-scenario bit patterns (which of Bit 7…Bit 0 of Part 1, and Bit 7 / Bits 6-0 of
  Part 2, must be set/clear/"any"/N/A for each scenario) are present in the source PDF as a table,
  but the PDF-to-text extraction has interleaved the column headers and cell values into a single
  run-on line per row, making the bit-to-scenario mapping unreliable to transcribe faithfully. Do
  **not** treat any bit-pattern claim for this table as sourced — re-extract from the original PDF
  table (not the .txt) or ask the engineer for the authoritative bit table before writing any case
  that asserts a specific bit combination.
- **GAP** — it is not clear from the legible text whether "status bar shows N/A" for every listed
  scenario means the status bar genuinely displays nothing for all of them, or whether the "N/A"
  values are an artifact of the same table-extraction corruption noted above. Needs engineer
  confirmation before writing a test that asserts "no status bar text" as an expected outcome.

## 6.6 Communication loss — detection and effect on in-flight transactions
- **Detection:** the FR monitors messages from the OBV; if it detects **no messages from the OBV for
  a configured period**, it registers a communication loss with the OBV. Timeout is configurable;
  **initial/default value = 9 seconds**. (`NJT_FRFRP_FS002 p.80`)
- **Effect — EMV or SV (stored value) transaction awaiting driver interaction:** on comms-loss
  detection, the transaction is **immediately automatically cancelled**. (`NJT_FRFRP_FS002 p.80`)
- **Effect — Barcode or Fare card ticket transaction awaiting driver interaction:** on comms-loss
  detection, the FR **remains waiting** for the Driver to accept or cancel the transaction (i.e. no
  automatic cancel for these two transaction types on comms loss). (`NJT_FRFRP_FS002 p.80`)

## 6.7 Transaction Timeout — auto-accept/auto-reject after driver-interaction wait
- **Timeout scope:** applies when a Barcode, EMV, or Fare card transaction is waiting for driver
  interaction; the FR can automatically accept or reject it. Timeout is configurable; **initial/
  default value = 60 seconds**. (`NJT_FRFRP_FS002 p.80`)
- **Trigger condition (OBV-accepted transaction path):** applies after the OBV transaction screen
  has been displayed for an OBV-accepted transaction whose approval state is one of **"waiting for
  driver"**, **"waiting for zones"**, or **"waiting for rider classification and zones"** — if the
  Driver has not confirmed or cancelled before the timeout elapses, the FR auto-resolves as follows
  (`NJT_FRFRP_FS002 p.80`):
  - **Barcode** → FR **automatically accepts** the transaction with the current details shown on the
    barcode transaction screen.
  - **EMV** → FR **automatically cancels** the transaction.
  - **Fare card** → FR **automatically accepts** the transaction with the current details shown on
    the Fare card product transaction screen.
  - For auto-accepted Barcode and Fare card transactions, a **receipt may also print if configured
    to**.
- **Trigger condition (OBV-rejected transaction path):** after the error message has been displayed
  for a rejected OBV transaction, if the Driver has not acknowledged the rejection before the timeout
  elapses, the FR **automatically acknowledges it** on the Driver's behalf. (`NJT_FRFRP_FS002 p.81`)
- **GAP** — the spec (in this excerpt) does not state the timeout behaviour for an SV (stored value)
  transaction under 6.7's auto-accept/reject list, only EMV, Barcode, and Fare card are enumerated,
  even though 6.6 explicitly mentions SV transactions as one of the types affected by comms loss. If
  a case is written asserting "no SV timeout behaviour exists," flag it `UNCONFIRMED` and route to
  the engineer rather than asserting SV has no timeout path.

## Suite implications
- **Emergency Mode:** add/verify cases for (a) entry message display + accept-other-operator-products
  guidance on first Emergency-Mode bit-set, (b) clearing entry message via **C key only**, (c) exit
  message on bit-clear, (d) clearing exit message via **C key only**. Flag the "first sees" repeat-
  entry ambiguity as a gap-register question before asserting repeat-trigger behaviour either way.
- **OBV Status bar:** do NOT write cases asserting specific bit-pattern-to-scenario mappings from this
  note — the source table extraction is corrupted (see GAP above); get the authoritative table from
  the PDF or engineer first. Do cover the **behavioural** facts that are clean: Emergency Mode/no-GPS/
  no-screen-display statuses are excluded from the top-line status indicator.
- **Communication loss:** cover the 9-second default timeout trigger, and specifically the
  **differing behaviour by transaction type** — EMV/SV auto-cancel on comms loss vs. Barcode/Fare
  card remain-waiting on comms loss. This asymmetry is a likely-missed coverage gap; check existing
  suite for a comms-loss case per transaction type (Barcode, EMV, SV, Fare card).
- **Transaction timeout:** cover the 60-second default timeout for each of the three enumerated
  approval-wait states (waiting for driver / waiting for zones / waiting for rider classification and
  zones), crossed with each transaction type's differing outcome (Barcode auto-accept, EMV
  auto-cancel, Fare card auto-accept), plus the optional receipt-print-if-configured for auto-accepted
  Barcode/Fare card. Also cover the separate **OBV-rejected-transaction auto-acknowledge** path
  (p.81) — distinct trigger (error message displayed, not accepted) from the accepted-transaction
  path.
- Raise the **SV-transaction timeout gap** to the engineer via the gap register before assuming SV
  has (or lacks) an auto-accept/reject timeout path; do not write a case implying either without an
  answer.
