# Flow: Translink HHD — Sales Mode: Printing (Ticket, Receipt, Waybill, Mini Statement, Barcode)

- Source: Overflow project "TFTS HHD V17.3.7" (https://overflow.io/s/XP0NLVZZ/), board "4. Sales
  Mode". Transcribed verbatim via the Claude Chrome extension, 2026-08-05. Raw source:
  `knowledge/flows/translink-hhd-full-transcription-v17.3.7.md`.
- Project: translink   Device: HHD   Feature: sales mode — printing outcomes shared across
  cash/card/smartcard/waybill/mini-statement/barcode ticket flows.
- Transcription confidence: **medium-low for exact wiring, high for text content**. The raw board
  reuses generic decision labels ("Print success?" / "Print Success?") at many distinct points
  without a unique id per instance, the same way ETM's shared printer-error decision does — but here
  there are several genuinely different failure screens (not one shared one), and the source text
  does not always make clear which "Print success?" instance's Yes/No pairs with which entry screen.
  Pairings below are reconstructed from the most contiguous/plausible reading of the raw connections
  list; anything not explicitly stated is flagged `TODO: confirm` rather than assumed. See
  `translink-hhd-sales-mode-navigation.md` for the sibling-file split rationale.

## Diagram
```mermaid
flowchart TD
  %% -- Ticket printing (basic / cash) --
  TICKETPRINT[2.4.3 Printing Ticket] --> PQ1{"Print Success?"}
  PQ1 -->|No| PF1[2.4.3.2 Print Failed]
  PQ1 -->|Yes| TXCOMP1[2.4.3.1 Transaction complete]
  PF1 -->|tap 'Annul Transaction'| ANNUL1(("Go to Annulment flow seen in 'Driver Menu Functionality'."))
  TXCOMP1 -->|3s timeout or tap Tick| BACKSALES1(("Back to 'Sales' screen."))

  %% -- Ticket printing, No Header variant --
  NOHEADER[2.4.3.1 Printing Ticket - No Header] --> PQ2{"Print success?"}
  PQ2 -->|No| PFSHARED[8.5.2.1 Printing Failed - Card]
  PFSHARED -->|tap 'Retry'| NOHEADER
  PFSHARED -->|tap 'Cancel'| BACKSALES2(("Go back to Sales screen."))

  %% -- Ticket printing, Card variant --
  TICKETCARD[2.4.3.3 Printing Ticket - Card] --> PQ3{"Print success?"}
  PQ3 -->|No| PFCARD[2.4.3.2.1 Print Failed - Card]
  PQ3 -->|Yes| TXCOMPCARD[2.4.3.4 Transaction complete - Card]
  PFCARD --> ANNUL2(("Go to Annulment flow seen in 'Driver Menu Functionality'."))
  TXCOMPCARD --> TICKETCARD
  TXCOMPCARD -->|3s timeout or tap Tick| BACKSALES3(("Back to 'Sales' screen or previous flow if applicable."))

  %% -- Card payment receipt --
  RECEIPTQ{"8.5.1 Print Receipt?"} -->|Yes - Print| RECEIPTCARD[8.5.1.1 Printing Receipt - Card]
  RECEIPTQ -->|No| BACKSALES4(("Back to 'Sales' screen or previous flow if applicable."))
  RECEIPTCARD --> PQ4{"Print success?"}
  PQ4 -->|No| PFSHARED
  PQ4 -->|Yes| TXCOMPTOPUP[4.8 Transaction complete]
  PFSHARED -->|tap 'Retry' (mini-statement context)| MINISTMTRETRY(("Print Mini Statement"))
  PFSHARED -->|tap 'Cancel'| BACKSALES5(("Go back to Sales screen."))

  %% -- Waybill printing --
  ACCESSWAYBILLQ{"Accessed Waybill when Signing Off or in a menu?"}
  ACCESSWAYBILLQ -->|Signing Off| WAYBILL1[7. Printing Waybill]
  ACCESSWAYBILLQ -->|From a Menu| WAYBILL2[11.3 Printing Waybill]
  WAYBILL1 --> PQ5{"Print Success?"}
  WAYBILL2 --> PQ6{"Print Success?"}
  PQ5 -->|Yes| TXCOMPMENU[7.1 Transaction complete]
  PQ5 -->|No| PF72[7.2 Print Failed]
  PQ6 -->|No| PF114[11.4 Printing Failed]
  TXCOMPMENU -->|tap green tick or 2s timeout| BACKSUPERVISOR(("Back to Supervisor menu."))
  TXCOMPMENU --> BACKMENU(("Back to relevant menu."))
  TXCOMPMENU --> BACKSALES6(("Back to 'Sales' screen."))
  TXCOMPMENU --> LOGINFLOW1(("Go to 'Login' flow."))
  PF72 -->|tap 'Retry'| WAYBILL1
  PF72 -->|tap 'Continue Without Printing'| LOGINFLOW2(("Go to 'Login' flow."))
  PF72 -->|tap 'Retry'| BACKRECEIPT1(("Back to 'Printing Receipt' screen."))
  PF72 -->|tap 'Continue Without Printing'| BACKSALES7(("Go back to Sales screen."))

  %% -- Card payment print failed --
  PQCARDPAY{"Print success?"} -->|No| PF721[7.2.1 Print Failed Card Payment]
  PF721 -->|tap 'Retry'| BACKRECEIPT2(("Back to 'Printing Receipt' screen."))
  PF721 -->|tap 'Continue Without Printing'| BACKSALES8(("Go back to Sales screen."))

  %% -- Mini statement --
  MINISTMT[26.2 Print Mini Statement] --> PQ7{"Print success?"}
  PQ7 -->|No| PFSHARED
  PFSHARED -->|tap 'Cancel' (mini-statement context)| BACKMINISTMT(("Go back to 'Mini Statement' screen."))

  %% -- Generic receipt printing --
  PRINTRECEIPT[12.2 Printing Receipt] --> PQ8{"Print Success?"}
  PQ8 -->|No| PFSHARED

  %% -- Barcode ticket --
  PQBARCODE{"Print Success?"} -->|Yes| BARCODEQ{"27 Barcode Ticket - Printed?"}
  BARCODEQ -->|Yes| TXCOMPMENU
  BARCODEQ -->|No| GOTOTICKETPRINT(("Go to 'Printing Ticket' screen."))
```

## Paths (each path = one candidate scenario)
| # | Path | Feature | Tags | Covered by |
|---|------|---------|------|------------|
| 1 | Printing Ticket → Print Success? Yes → Transaction complete → back to Sales | printing | — | 4104006, 4103847, 4103848, 4103849 |
| 2 | Printing Ticket → Print Success? No → Print Failed → Annul Transaction → Driver Menu annulment flow | printing | @destructive | 4105258 |
| 3 | Printing Ticket - No Header → Print success? No → Printing Failed - Card → Retry → back to No Header | printing | @destructive | 4105259 |
| 4 | Printing Ticket - No Header → Print success? No → Printing Failed - Card → Cancel → back to Sales | printing | @destructive | 4105260 |
| 5 | Printing Ticket - Card → Print success? Yes → Transaction complete - Card → (reprint loop back to Printing Ticket - Card) | printing-card | — | 4103804, 4103805, 4103806, 4104663 |
| 6 | Printing Ticket - Card → Print success? No → Print Failed - Card → Annulment flow | printing-card | @destructive | 4105261 |
| 7 | Print Receipt? Yes-Print → Printing Receipt - Card → Print success? Yes → Transaction complete (top-up) | printing-card | — | 4103829, 4103830, 4103879 |
| 8 | Print Receipt? No → back to Sales/previous flow | printing-card | — | 4105262 |
| 9 | Accessed Waybill while Signing Off → Printing Waybill (7.) → Print Success? Yes → Transaction complete → back to Supervisor menu/relevant menu/Sales/Login flow | printing-waybill | — | 4104010 |
| 10 | Accessed Waybill via a Menu → Printing Waybill (11.3) → Print Success? No → Printing Failed (11.4) | printing-waybill | @destructive | 4105264 |
| 11 | Printing Waybill → Print Success? No → Print Failed (7.2) → Retry → back to Printing Waybill | printing-waybill | @destructive | 4105265 |
| 12 | Print Failed (7.2) → Continue Without Printing → Login flow / back to Sales | printing-waybill | @destructive | 4105266 |
| 13 | Card payment print → Print success? No → Print Failed Card Payment (7.2.1) → Retry → back to Printing Receipt | printing-card | @destructive | 4103889 |
| 14 | Print Failed Card Payment (7.2.1) → Continue Without Printing → back to Sales | printing-card | @destructive | 4105263 |
| 15 | Print Mini Statement → Print success? No → Printing Failed - Card → Retry → back to Print Mini Statement | printing-mini-statement | @destructive | 4105267 |
| 16 | Print Mini Statement → Print success? No → Printing Failed - Card → Cancel → back to Mini Statement screen | printing-mini-statement | @destructive | 4105268 |
| 17 | Print Success? Yes → Barcode Ticket - Printed? Yes → Transaction complete | printing-barcode | — | 4105269 |
| 18 | Barcode Ticket - Printed? No → go to Printing Ticket screen (reprint) | printing-barcode | @destructive | 4105270 |

## Screen states (Given/Then anchors)
- **8.5.2.1 Printing Failed - Card** — appears to be a **shared** print-failure screen reached from
  several distinct print contexts (No-Header ticket print, card receipt print, mini statement print,
  generic receipt print), the same pattern as ETM's shared FLU printer-error screen: its Retry target
  depends on which flow entered it (back to the originating print screen), and Cancel generally
  returns to Sales — except the mini-statement context, whose Cancel returns to the 'Mini Statement'
  screen specifically.
- **If the user cannot print, they must annul the transaction** — stated explicitly for card ticket
  printing and card payment printing; the annulment itself is the "Annulment flow seen in 'Driver
  Menu Functionality'" (out of scope for this board — cross-reference only).
- **Barcode validation** — barcodes are only validated once the operator confirms a ticket has
  successfully printed; only one reprint attempt is allowed if a print fails.
- **Merchant receipt** — if printed, shows "printing 1 of 2"; if the operator answers 'No' to a
  merchant-receipt prompt but the back office is configured to print one anyway, it still prints (in
  which case both print and it's "printing 1 of 2"); if 'Yes' both print. This follows the Payment
  Card Receipt Print Flow.

## Notes / unknowns
- **Named print sub-flows referenced but not expanded on this board**: "Payment Card Receipt Print
  Flow", "Top Up Receipt Flow", "Concessionary Print Flow", "Penalty Fare Warning Print Flow",
  "Versioning Print Flow", "Barcode Travel Ticket Print Flow", "Mini Statement Print Flow", "Waybill
  Print Flow", "Cash Print Flow", "Payment Card Print Flow" — these are annotation labels naming
  destinations (`Go to relevant 'Cash / Payment Card Print Flow' flow.` etc.) rather than screens
  transcribed on this board. TODO: confirm whether these are detailed on board "8. Additional
  Features" (not yet transcribed into this repo) — do not assume their content.
- TODO: confirm the Yes-branch target for `PQ2` (`2.4.3.1 Printing Ticket - No Header` print success)
  and for `PQ6` (`11.3 Printing Waybill` print success) and for `PQ7` (Mini Statement print success)
  and for `PQ8` (`12.2 Printing Receipt` print success) — the raw transcription gives the No-branch
  (failure screen) for each but no explicit Yes-branch edge was captured.
- TODO: confirm the entry screen for the barcode print-success gate (`PQBARCODE`) — the transcription
  captures `Print Success? → 27 Barcode Ticket - Printed? [Yes]` but not which printing screen
  precedes that particular `Print Success?` instance.
- TODO: confirm whether `PF72` (`7.2 Print Failed`) reached from the Waybill chain is genuinely the
  same screen as the `PF72` whose Retry/Cancel routes to "Printing Receipt"/"Sales" in a
  receipt-printing context, or whether these are two visually distinct board nodes sharing a title —
  the raw transcription does not disambiguate.
- **GAP**: no annotation captures what happens if the operator repeatedly fails to print and there is
  no visible retry-count cap for the ticket/receipt print contexts (unlike the card-reader-reconnect
  flow in `translink-hhd-sales-mode-payment.md`, which explicitly caps retries at 3). Flag for
  engineer confirmation before writing a destructive "print keeps failing" case.
