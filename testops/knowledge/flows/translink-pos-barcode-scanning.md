# Flow: Translink POS — Barcode Scanning

- Source: `knowledge/flows/translink-pos-full-transcription-v4.0.3.md`, board "15. 14.0 Barcode
  Scanning" (Board Index entry "15.0 14.0 Barcode Scanning"). Raw transcription captured via the
  Claude Chrome extension, 2026-08-04, all 17 boards. This flow-map structured from it 2026-08-05.
- Project: translink   Device: POS   Feature: barcode scanning (FLU barcode ticket validation +
  Operator Menu manual Barcode Reference entry)
- Transcription confidence: **medium** — the source board's screen/decision/connection lists are
  verbatim, but several connections wrap across lines in the raw export and a small number of
  decision targets did not resolve to a named node (see Notes/unknowns). Treated as one board — it
  is a single coherent scan→validate→print flow (plus its own Operator Menu entry sub-flow), not a
  bundle of distinct feature areas, so it was **not** split.

## Diagram
```mermaid
flowchart TD
  FLU["2.5.2 Main Screen - Ulsterbus selected"]
  RETRIEVEQ{Barcode data successfully retrieved?}
  UNRESOLVED["UNRESOLVED decision target (raw export node id 3b5ae6dc-a37e-4fcb-8bf7-3afda54ad4ef) — see Notes"]
  VALIDATING["Barcode - Validating Details"]
  DECRYPTQ{Decryption and parsing successful?}
  VALFAIL["Barcode Validation Failed"]
  OFFLINEQ{Is the barcode already offline validated?}
  ONLINECHECKQ{Online check available?}
  OFFLINECHECK["Barcode - Offline Check"]
  LIMITQ{"Ticket value <= configurable limit & product is valid?"}
  VALIDQ{Valid barcode?}
  BGCHECKQ{Passed additional background checks?}
  CANCELLED["Barcode Scan - Transaction Cancelled - Ticket Not Valid"]
  VISUALFAIL["Barcode Scan - Transaction Cancelled - Ticket Not Passed Visual Inspection"]
  TICKETVALID["Barcode Scan - Ticket Valid inc. Date and Depart Time"]
  ONLINEQ{Online?}
  PRINTONLINE["POS attempts to print ticket"]
  PRINTOFFLINE["POS attempts to print ticket & stores offline validation in the background"]
  PRINTOKQ{Print successful?}
  PRINTERR["Barcode Ticket - Print Error"]
  PRINTED["Barcode Ticket - Printed?"]
  OPMENU["9.0 Operator Menu"]
  BCREF["Barcode Reference"]
  BCREFENTERED["Barcode Reference Entered"]
  PAGE1["Barcode Scan - Ticket Valid inc. Outbound and Return"]
  PAGE2["Barcode Scan - Ticket Valid inc. Outbound and Return - Page 2"]

  FLU -->|barcode scanned by reader| RETRIEVEQ
  RETRIEVEQ -->|Yes| VALIDATING
  RETRIEVEQ -->|No| UNRESOLVED

  VALIDATING --> DECRYPTQ
  DECRYPTQ -->|No: "Barcode Decryption has failed"| VALFAIL
  DECRYPTQ -->|Yes| OFFLINEQ

  VALFAIL -->|"Back to 'Validating Ticket Details' check"| VALIDATING
  VALFAIL -->|"Back to FLU screen"| FLU
  VALFAIL -->|manual retry: to Barcode Reference screen| BCREF

  OFFLINEQ -->|"Yes: already offline validated — 'ticket has already been offline validated'"| VALFAIL
  OFFLINEQ -->|No| ONLINECHECKQ

  ONLINECHECKQ -->|No| OFFLINECHECK
  ONLINECHECKQ -->|Yes| VALIDQ

  OFFLINECHECK --> LIMITQ
  LIMITQ -->|"Yes: go to 'Valid Barcode?' decision point"| VALIDQ
  LIMITQ -->|"No: value exceeds offline validation limit / ticket not valid"| VALFAIL

  VALIDQ -->|"No: 'ticket not valid' / 'already used' / 'not valid on this date' / 'expired'"| CANCELLED
  CANCELLED -->|"Back to 'Validating Ticket Details' check"| VALIDATING
  CANCELLED -->|"Back to FLU screen"| FLU
  VALIDQ -->|Yes| BGCHECKQ

  BGCHECKQ -->|"No: 'Additional validation failed'"| CANCELLED
  BGCHECKQ -->|Yes| TICKETVALID

  TICKETVALID -->|operator visual inspection fails| VISUALFAIL
  VISUALFAIL --> FLU
  TICKETVALID --> ONLINEQ

  ONLINEQ -->|online| PRINTONLINE
  ONLINEQ -->|offline| PRINTOFFLINE
  PRINTONLINE --> PRINTOKQ
  PRINTOFFLINE --> PRINTOKQ

  PRINTOKQ -->|No| PRINTERR
  PRINTERR -->|"1st press: retry print, audit retry with Corethree/CloudFare, back to Print successful? check"| PRINTOKQ
  PRINTERR -->|"2nd press: back to FLU, barcode no longer valid"| FLU
  PRINTOKQ -->|Yes| PRINTED

  PRINTED -->|"Barcode has been validated — back to the FLU screen"| FLU
  PRINTED -->|"Barcode still valid — back to the print check"| PRINTOKQ

  OPMENU --> BCREF
  BCREF -->|operator enters barcode reference number| BCREFENTERED
  BCREF -->|"unreadable receipt: Cancel key"| FLU
  BCREFENTERED -->|"Go to 'Barcode - Validating Details' check"| VALIDATING

  PAGE1 -->|Next page| PAGE2
  PAGE2 --> PAGE1
```

## Paths (each path = one candidate scenario)
| # | Path | Feature | Tags | Covered by |
|---|------|---------|------|------------|
| 1 | Main Screen → barcode scanned → data **not** retrieved → unresolved failure path | barcode-scan | @destructive | 4105062 |
| 2 | Main Screen → barcode scanned → data retrieved → Validating Details → decrypt/parse fails → Validation Failed → retry Validating Details | barcode-scan | @destructive | 4105063 |
| 3 | Validation Failed (decrypt/parse) → back to FLU screen | barcode-scan | @destructive | 4105064 |
| 4 | Validating Details → decrypt/parse OK → already offline validated → Validation Failed ("already offline validated") | barcode-scan | @destructive | 4103574 |
| 5 | decrypt/parse OK → not already offline validated → online check unavailable → Offline Check → ticket value ≤ limit & product valid → Valid Barcode? | barcode-scan | — | 4103573 |
| 6 | Offline Check → ticket value/product check fails → Validation Failed | barcode-scan | @destructive | 4103573 |
| 7 | online check available → Valid Barcode? = No → Transaction Cancelled - Ticket Not Valid → retry Validating Details | barcode-scan | @destructive | 4105065 |
| 8 | Transaction Cancelled - Ticket Not Valid → back to FLU screen | barcode-scan | @destructive | 4105066 |
| 9 | Valid Barcode? = Yes → Passed additional background checks? = No → Transaction Cancelled - Ticket Not Valid | barcode-scan | @destructive | 4105067 |
| 10 | Passed additional background checks? = Yes → Ticket Valid inc. Date and Depart Time shown → operator visual inspection fails → Transaction Cancelled - Ticket Not Passed Visual Inspection → back to FLU | barcode-scan | @destructive | 4105068 |
| 11 | Ticket Valid → visual inspection passes → Online? = online → POS attempts print → Print successful → Barcode Ticket - Printed? → "validated, back to FLU" | barcode-scan | — | 4103570 |
| 12 | Ticket Valid → Online? = offline → POS attempts print & stores offline validation in background → Print successful → Printed? | barcode-scan | — | 4100440 |
| 13 | POS attempts print → Print successful? = No → Barcode Ticket - Print Error → 1st press retries print (audited reprint) → back to Print successful? check | barcode-scan | @destructive | 4105069 |
| 14 | Barcode Ticket - Print Error → 2nd press on same barcode → back to FLU, barcode no longer valid | barcode-scan | @destructive | 4105070 |
| 15 | Barcode Ticket - Printed? → "barcode still valid, back to print check" (reprint loop) | barcode-scan | — | 4105071 |
| 16 | Operator Menu → Barcode Reference → operator enters reference number → Barcode Reference Entered → Go to Barcode - Validating Details check (manual entry route into the same validation flow) | barcode-scan | — | 4103577 |
| 17 | Barcode Reference screen → unreadable barcode → Cancel key → back to FLU screen (and 'C' key clears one digit at a time while entering) | barcode-scan | @destructive | 4105072 |
| 18 | Any "Barcode Validation Failed" failure point → routed to Barcode Reference screen for manual retry entry | barcode-scan | — | 4105073 |
| 19 | Barcode Scan - Ticket Valid inc. Outbound and Return → Next page → Page 2 → back to page 1 | barcode-scan | — | 4105074 |

## Screen states (Given/Then anchors)
- **2.5.2 Main Screen-Ulsterbus selected** — the FLU screen from which a barcode scan is
  initiated; every terminal path in this board ("back to FLU screen") returns here.
- **Barcode - Validating Details** — intermediate "checking" state; source is explicit that
  several failure branches loop back to this exact check ("Back to 'Validating Ticket Details'
  check").
- **Barcode Validation Failed** — the single shared failure screen reused across at least three
  distinct failure causes: decryption/parsing failure, "already offline validated", and ticket
  value/product check failure (Offline Check limit). Exact displayed message differs per cause
  (see Diagram edge labels) but the screen name in the source is identical each time.
- **Barcode - Offline Check** — reached only when the online check is unavailable; gates on
  "ticket value ≤ the configurable limit & product is valid".
- **Barcode Scan - Transaction Cancelled - Ticket Not Valid** — shown for both the "Valid
  barcode? = No" branch and the "Passed additional background checks? = No" branch; displayed
  message set is one of: 'the ticket has already been used', 'the ticket is not valid on this
  date', 'the ticket has expired', 'the ticket is not valid'.
- **Barcode Scan - Ticket Valid inc. Date and Depart Time** — the ticket-valid confirmation shown
  after passing background checks, subject to operator visual inspection before proceeding to
  print.
- **Barcode Scan - Transaction Cancelled - Ticket Not Passed Visual Inspection** — reached only
  from the ticket-valid screen when the operator's manual visual check fails; goes straight back
  to FLU (no further retry loop shown in the source).
- **Barcode Ticket - Print Error** — the shared print-failure screen; source specifies asymmetric
  behaviour depending on press count on the *same barcode*: 1st press retries the print job
  (audited as a reprint with Corethree/CloudFare) and returns to the Print successful? check;
  2nd press abandons the print, returns to FLU, and invalidates the barcode.
  Contrast with the ETM/FLU shared printer-error screen elsewhere in the suite — this one is
  barcode-specific and has its own retry-count rule, not a generic "retry/cancel" pair.
- **Barcode Ticket - Printed?** — confirms the ticket printed; can loop back to the print check
  ("barcode still valid — back to the print check") or terminate back to FLU ("barcode has been
  validated").
- **Barcode Reference** — manual barcode entry screen, reached both from the Operator Menu
  directly and as the retry destination from multiple Validation Failed states; has a 12-character
  upper limit on the entered reference and supports 'C' to clear one digit at a time; Cancel key
  aborts back to FLU screen.
- **Barcode Reference Entered** — feeds the manually-entered reference into the same "Barcode -
  Validating Details" check used by the scanner path.
- **Barcode Scan - Ticket Valid inc. Outbound and Return** — paginated ticket-valid variant with
  a "Page 2" companion screen (Next page / back).

## Notes / unknowns
- TODO: confirm the "No" (not retrieved) destination of "Barcode data successfully retrieved?" —
  the raw transcription's connection list resolves this edge to an internal node id
  (`3b5ae6dc-a37e-4fcb-8bf7-3afda54ad4ef`) rather than a named screen/decision. This likely maps to
  a "scan failed / rescan" state that exists in Overflow but didn't resolve in the export; do not
  assume it is the "Barcode Validation Failed" screen without confirming against the live board.
- TODO: confirm where **"Barcode Scan - Ticket Valid inc. 3 Use Times"** and **"Barcode Scan -
  Ticket Valid inc. Date with Expiry and Depart Time"** sit in the flow. Both are listed in the
  board's Screens but have no explicit connection in the Connections/Flow list. Given the
  annotation "Ticket Validation Screen Examples" and "On this particular barcode type there can be
  Notes as well", these read as alternate examples of the same ticket-valid confirmation point as
  "Barcode Scan - Ticket Valid inc. Date and Depart Time" (i.e. the screen shown varies by barcode
  product type) — not confirmed as a distinct branch, so not drawn as a separate path above.
- TODO: confirm the exact relationship of "Barcode Scan - Ticket Valid inc. Outbound and Return"
  (+ Page 2) to the main Ticket Valid screen — the source shows its own Next-page/back pairing but
  no connection tying it into the online/offline print branch; likely another per-product-type
  variant of the same ticket-valid confirmation point, unconfirmed.
- The three separate "Barcode Validation Failed → [decision] This will take the user to the
  'Barcode Reference' screen…" connections in the source are transcribed as one edge in the
  diagram (Validation Failed → Barcode Reference) since all three carry identical text; if the
  live board distinguishes which specific failure causes route to manual retry vs. straight back
  to FLU, that distinction is not resolvable from this transcription — TODO: confirm on live board.
- "Barcode - Offline Check" behaviour note from annotations: barcodes validated offline are
  queued/stored until connectivity with CloudFare and Corethree is re-established (annotation is
  itself phrased as a question in the source — "Barcodes that have been validated offline will be
  stored in a list until a connection with Cloudfare and Corethree is re-established?" — kept
  verbatim; TODO: confirm this is settled behaviour, not an open design question).
- "If a barcode fails, it will not mark the barcode as redeemed in CoreThree" appears three times
  in the Decision Points list without a resolvable connection target in this transcription — kept
  as a behavioural note rather than a diagram edge. TODO: confirm which failure branch(es) this
  attaches to.
