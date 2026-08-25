# Flow: Translink POS — Card Payment

- Source: `knowledge/flows/translink-pos-full-transcription-v4.0.3.md`, board "6. 5.0 Card Payment"
  (Board Index item "5.0 Card Payment"). Transcribed verbatim via the Claude Chrome extension,
  originally captured 2026-08-04; restructured into this flow-map 2026-08-05.
- Project: translink   Device: POS   Feature: card payment (Chip & PIN / contactless / swipe, via
  Miura M020 payment terminal)
- Transcription confidence: **medium** — the screen list, decision list, and annotation list are
  verbatim, but the raw board's Connections/Flow entries carry **no edge condition labels** (no
  "Yes"/"No"/branch-name text on the arrows themselves, unlike some other boards), and several
  decision nodes in the raw export have no text at all — only an opaque Overflow node id (a UUID).
  Every UUID node and every unlabeled edge is called out explicitly below rather than guessed at.

## Diagram
```mermaid
flowchart TD
  MAIN[4.2.3 Main Screen - FLU - Multiple Items - Payment]
  INIT[5.1.1 FLU/Bank Card/Initialising Transaction]
  PRESENT[5.2.1 FLU/Bank Card/Present]
  PRESENTPIN[5.2.1.1 FLU/Bank Card/Present Card PIN]
  CONFIRM[5.3.1 FLU/Bank Card/Customer Confirmation]
  USERCONF[5.3.2 FLU/Bank Card/User Confirming Amount]
  DECLINED[5.4.1 FLU/Bank Card/Transaction Declined]
  APPROVED[5.4.2 FLU/Transaction Approved]
  APPROVEDCONF[5.4.3 FLU/Transaction Approved-Confirmation]
  DECLINED2[5.5.1 FLU/Bank Card/Transaction Declined 2]
  SIGNATURE[5.5.2 FLU/Bank Card/Customer Signature]

  AMTLARGE{Amount too large? (Test transactions only)}
  PAYTYPE{Payment type}
  OVER45{Over £45, customer decides Chip & PIN, or payment device asks customer to insert their card?}
  CHIPAVAIL{Chip & PIN card available?}
  TXNOK{Transaction Successful?}
  PINOK{Correct PIN Entered?}

  %% unlabeled Overflow decision nodes — no text captured in the raw export, only an id
  U1{{unlabeled decision — Overflow id 46190e4d}}
  U2{{unlabeled decision — Overflow id a533483e}}
  U3{{unlabeled decision — Overflow id 3fc532ce}}
  U4{{unlabeled decision — Overflow id 55798a1f}}
  U5{{unlabeled decision — Overflow id 8fd0b3e2}}
  U6{{unlabeled decision — Overflow id ea99a1eb}}
  U7{{unlabeled decision — Overflow id edd9f3ff}}
  U8{{unlabeled decision — Overflow id 048b82fc}}
  U9{{unlabeled decision — Overflow id 71a331ad}}
  U10{{unlabeled decision — Overflow id 91898426}}
  U11{{unlabeled decision — Overflow id 9c2a019e}}
  U12{{unlabeled decision — Overflow id c276d0ff}}
  U13{{unlabeled decision — Overflow id cf709527}}
  U14{{unlabeled decision — Overflow id 9bb3e5bb}}
  PRINTNOTE{{"When the Print Receipt button is pressed a payment card receipt will be printed and the POS will return to the FLU screen."}}
  DECLINEDNOTE{{"A declined card payment receipt will be printed when this screen is displayed."}}

  MAIN --> INIT
  INIT --> PRESENT
  PRESENT --> AMTLARGE
  PRESENT --> MAIN
  PRESENT -->|Customer cancels the transaction using the Cancel button on the Miura M020| DECLINED2

  AMTLARGE --> DECLINED
  AMTLARGE --> PAYTYPE

  PAYTYPE --> U2
  PAYTYPE --> U4
  PAYTYPE --> U6

  U2 --> OVER45
  U4 --> CHIPAVAIL
  U6 --> USERCONF

  OVER45 --> CONFIRM
  OVER45 --> PRESENTPIN
  PRESENTPIN --> U6

  CHIPAVAIL --> USERCONF
  CHIPAVAIL --> U6

  USERCONF --> PINOK
  USERCONF --> CONFIRM
  USERCONF --> DECLINED2

  PINOK --> CONFIRM
  PINOK --> DECLINED

  CONFIRM --> TXNOK
  TXNOK --> APPROVEDCONF
  TXNOK --> APPROVED
  TXNOK --> DECLINED

  APPROVED --> U7
  U7 --> SIGNATURE
  SIGNATURE --> APPROVEDCONF
  SIGNATURE --> DECLINED

  APPROVEDCONF --> U1
  APPROVEDCONF --> U12
  APPROVEDCONF --> U13
  APPROVEDCONF --> PRINTNOTE

  DECLINED --> MAIN
  DECLINED --> U5
  DECLINED --> U9
  DECLINED --> U10
  DECLINED --> U11
  DECLINED --> DECLINEDNOTE

  DECLINED2 --> MAIN
  DECLINED2 --> U3
  DECLINED2 --> U8
  DECLINED2 --> U14
```

## Paths (each path = one candidate scenario)
| # | Path | Feature | Tags | Covered by |
|---|------|---------|------|------------|
| 1 | Main Screen → choose Bank Card → Initialising Transaction → Present card → amount not too large → Payment type → contactless/swipe branch (U6) → User Confirming Amount → Customer Confirmation → Transaction Successful → Approved-Confirmation (ticket printed immediately) | card-payment | — | 4099994 |
| 2 | Present → Payment type → Chip & PIN branch, over £45 (U2→Over £45 decision) → Customer Confirmation → Transaction Successful → Approved-Confirmation | card-payment | — | 4099994 |
| 3 | Over £45 decision → customer presents card for PIN (5.2.1.1 Present Card PIN) → (U6) → User Confirming Amount → PIN entry | card-payment | — | 4105085 |
| 4 | Payment type → Chip & PIN branch (U4) → Chip & PIN card available? → Yes → User Confirming Amount → Correct PIN Entered? → Yes → Customer Confirmation → success | card-payment | — | 4099994 |
| 5 | Chip & PIN card available? → No (U6) → User Confirming Amount (fallback path) | card-payment | @destructive | 4105086 |
| 6 | User Confirming Amount → Correct PIN Entered? → No → Transaction Declined | card-payment | @destructive | 4100424 |
| 7 | Present → Amount too large? (test transactions only) → Yes → Transaction Declined (value too big for a card payment) | card-payment | @destructive | 4100424 |
| 8 | Present → Cancel button pressed on Miura M020 → Transaction Declined 2 → back to Main Screen | card-payment | @destructive | 4105087 |
| 9 | User Confirming Amount → customer cancels on PIN pad → Transaction Declined 2 | card-payment | @destructive | 4100424 |
| 10 | Customer Confirmation → Transaction Successful? → No → Transaction Declined → back to Main Screen | card-payment | @destructive | 4100424 |
| 11 | Customer Confirmation → Transaction Successful? → Yes → Transaction Approved (5.4.2) → Customer Signature required → signature matches → Approved-Confirmation → ticket printed | card-payment | — | 4105088 |
| 12 | Customer Signature → signature does NOT match payment card → Transaction Declined ("Signature doesn't match payment card" error) | card-payment | @destructive | 4100424 |
| 13 | Transaction Declined → incorrect PIN entered too many times → "Incorrect PIN entered too many times" error | card-payment | @destructive | 4100424 |
| 14 | Transaction Declined → declined card payment receipt printed automatically on screen display (no operator action) | card-payment | — | 4100424 |
| 15 | Transaction Declined / Transaction Declined 2 → Print Receipt button → payment/declined receipt printed → returns to FLU screen (2.7.3 Bus FLU or 3.2 Rail FLU) | card-payment | — | 4105089 |
| 16 | Transaction Declined / Transaction Declined 2 → operator chooses Back to Main / No receipt → returns to FLU screen (2.7.3 Bus FLU or 3.2 Rail FLU) without printing | card-payment | — | 4105090 |
| 17 | Any Declined/Declined-2 screen → timeout of 3 seconds, or press any key → returns to Payment Screen | card-payment | — | 4100424 |
| 18 | Approved-Confirmation → Print Receipt button → payment card receipt printed → returns to FLU screen | card-payment | — | 4099994 |

## Screen states (Given/Then anchors)
- **5.1.1 FLU/Bank Card/Initialising Transaction** — customer inserts or swipes the card; if
  contactless, the customer can present the card immediately instead.
- **5.2.1 FLU/Bank Card/Present** — POS status is driven by events from the card reader:
  "Starting transaction → Event (Awaiting card) → Insert card into reader → Events back from card."
  Operator can cancel at any time with the **C** button, returning to the payment screen; a
  cancelled transaction does not print a receipt.
- **5.2.1.1 FLU/Bank Card/Present Card PIN** — reached from the "Over £45..." decision; customer is
  asked to insert their card to pay.
- **5.3.1 FLU/Bank Card/Customer Confirmation** — payment terminal is in the process of authorising
  the transaction.
- **5.3.2 FLU/Bank Card/User Confirming Amount** — customer confirms the transaction amount and
  inputs their PIN; POS waits for the customer to press the green button on the M020 to confirm the
  amount.
- **5.4.1 FLU/Bank Card/Transaction Declined** — a declined card payment receipt is printed
  automatically when this screen is displayed; error messages shown depend on the message received
  from the M020. Exceptions cited: **no** cancelled-payment receipt if the customer presses the red
  X on the M020 before entering the PIN; possible errors include "Incorrect PIN entered too many
  times" and "Signature doesn't match payment card."
- **5.4.2 FLU/Transaction Approved** — leads into the signature step.
- **5.4.3 FLU/Transaction Approved-Confirmation** — as soon as this screen appears, the ticket is
  immediately printed; only after the ticket prints does the operator get the option to print a
  payment card receipt or skip it (Back to Main Screen / No receipt).
- **5.5.1 FLU/Bank Card/Transaction Declined 2** — reached from a mid-transaction cancel (Present
  screen: Cancel button on the M020) or from a customer cancelling on the PIN pad during User
  Confirming Amount.
- **5.5.2 FLU/Bank Card/Customer Signature** — a receipt for the customer to sign is printed; once
  the customer presses Yes on this screen, the ticket prints and the POS reverts to screen 2.7.3
  (Bus FLU) or 3.2 (Rail FLU).
- **Shared exit behaviour** — regardless of whether the operator chooses "Print receipt" or "Back to
  Main / No receipt" from either Declined screen, the POS reverts to screen 2.7.3 (Bus FLU) or 3.2
  (Rail FLU). A timeout of 3 seconds, or pressing any key, returns from a Declined screen to the
  Payment Screen.

## Notes / unknowns
- **TODO: confirm the "Payment type" three-way split.** The raw annotation list immediately
  following the "Payment type" decision contains the bare words "Chip & PIN", "Contactless", and
  "Swipe Card" — strongly suggesting these are the three branch labels off "Payment type" — but the
  raw Connections/Flow section carries **no edge labels**, so which of the three unlabeled decision
  nodes (U2 → "Over £45..."; U4 → "Chip & PIN card available?"; U6 → straight to "User Confirming
  Amount") corresponds to which payment method could not be determined from the transcription alone.
  Verify against the live Overflow board before writing Gherkin for this split.
- **TODO: confirm U1 / U12 / U13 (unlabeled decisions off 5.4.3 Approved-Confirmation)** and
  **U5 / U9 / U10 / U11 (unlabeled decisions off 5.4.1 Transaction Declined)** and
  **U3 / U8 / U14 (unlabeled decisions off 5.5.1 Transaction Declined 2)**. The raw transcription
  captured these as edge targets (arrow from the screen to an Overflow node id) but did not capture
  any onward edge, label, or resolved text for the node itself. Given the "Print Receipt" and
  "declined receipt auto-prints" annotations attached to these same screens, these are very likely
  the Print-Receipt-button / Back-to-Main-No-receipt / timeout branches described in the Screen
  states section above — but that is inference, not a transcribed fact, so it is not asserted in the
  diagram or paths table. Re-check the live board to resolve.
- **TODO: confirm which "Transaction Successful?" occurrence maps to which outcome pairing.** The
  decision appears three times in the raw Decision Points list and the same "Yes"/"No" text repeats
  in the Annotations list without an explicit 1:1 index-to-decision mapping; the diagram merges all
  occurrences into one `TXNOK` node per the connections actually listed (→ Approved-Confirmation, →
  Approved, → Declined), which is what the raw Connections/Flow section supports.
- The "Amount too large? (Test transactions only)" decision is explicitly scoped to **test
  transactions only** per its own label — flag any case built on it as testing a test-mode-only
  behaviour, not a live-transaction path.
- 5.4.1 "Transaction Declined" and 5.5.1 "Transaction Declined 2" are **distinct screens** in the raw
  export (different node numbers, both present in the Screens list) — do not collapse them into one
  screen when authoring cases; keep the transaction-authorisation-declined path (5.4.1) separate from
  the mid-transaction-cancel path (5.5.1).
- Board scope note: screen "4.2.3 Main Screen - FLU - Multiple Items - Payment" is the shared FLU
  Basket & Payment screen (see the "4.0 Basket & Payment" board) that this Card Payment board both
  enters from and returns to — it is included here only as an entry/exit anchor, not as this board's
  own screen.
