# Automation backlog — **NEW** POS-Acceptance Suite (POS)

_Generated 2026-08-06T08:49:20+00:00 by system-test-ops. Suite id 30253, project TFTS - System Test._

**52 fully automatable + 204 partial** of 600 cases (5 destructive, 329 manual-only). _Partial = the UI flow is automatable but a step (card tap / print / cash) needs a hardware fixture or human eye._

## How to consume

- Reference `ref` (TestRail case id, e.g. C4099911) in each automated test so a result maps back to its case.
- Mirror device + feature as pytest markers; add @pytest.mark.destructive where destructive is true (deselected by default).
- cross_check lists the back-office systems the case asserts — the test must verify the event landed there (CloudFare / MERIT / SmartTrack).
- automatable/priority are system-test-ops judgements and a starting point; the automation engineer may override with rationale.


## Priority: High

### C4099963 · Administrator — Clear Card  (2m)  — PARTIAL; refs: MODE-PRIMARY-ONLY
_Functional / Administrator / Card Management_

**GIVEN** an administrator is signed on to the POS in Card Management
**AND** a valid smartcard and an unreadable/invalid card are available to present
**AND** example: clearing a valid staff test card, then presenting a damaged card
**WHEN** the administrator clears a valid card
**THEN** the card is cleared
**AND** success is reported
**WHEN** the administrator attempts to clear an invalid card
**THEN** the operation is reported as unsuccessful with a card error

### C4099964 · Administrator — Card Dump  (2m)  — PARTIAL; refs: MODE-PRIMARY-ONLY
_Functional / Administrator / Card Management_

**GIVEN** an administrator is signed on to the POS in Card Management
**AND** a valid smartcard and an unreadable/invalid card are available to present
**AND** example: dumping a valid staff test card, then presenting a damaged card
**WHEN** the administrator dumps a valid card
**THEN** the card data is read
**AND** success is reported
**WHEN** the administrator attempts to dump an invalid card
**THEN** the operation is reported as unsuccessful

### C4099966 · Administrator — Device Settings  (1m)  — refs: TIBU-22632,MODE-PRIMARY-ONLY
_Functional / Administrator / Device & Network_

**GIVEN** an administrator is signed on to the POS in Device Settings
**AND** example: setting Home Location OM, a boarding location, mounting point and Tray Identifier "AT01"
**WHEN** the administrator changes the Home Location, Boarding Location, Mounting Point and Tray Identifier
**THEN** each setting is updated
**WHEN** the administrator leaves and reopens Device Settings
**THEN** each setting is retained

### C4099967 · Administrator — Network Settings  (1m)  — refs: TIBU-24740,FBD-100183,MODE-PRIMARY-ONLY
_Functional / Administrator / Device & Network_

**GIVEN** an administrator is signed on to the POS
**AND** example: the administrator opens Network Settings and changes a network value
**WHEN** the administrator opens Network Settings and changes a setting
**THEN** the screen responds to the input
**AND** the change is applied

### C4099968 · Administrator — Force Comms  (5m)  — cross-check: CloudFare; refs: MODE-PRIMARY-ONLY
_Functional / Administrator / Device & Network_

**GIVEN** an administrator is signed on to the POS
**AND** the POS is communicating with CloudFare
**AND** example: the administrator forces a call-in to pull the latest data, refreshes it, then exits
**WHEN** the administrator initiates, refreshes and exits Force Comms
**THEN** each action completes
**AND** the administrator returns to the Administrator menu
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100034 · Barcode — print barcode  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-13180,MODE-NIR-ONLY
_Functional / Barcode Scanning_

**GIVEN** an operator is signed on to the POS
**AND** a ticket type configured to carry a barcode is available to issue
**AND** the POS is communicating with CloudFare
**AND** example: a Rail Adult Single whose ticket type has 'print barcode' enabled, paid by cash
**WHEN** the operator issues the ticket
**THEN** a scannable barcode is printed on the ticket
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100035 · Barcode — scan barcode  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY
_Functional / Barcode Scanning_

**GIVEN** an operator is signed on to the POS on a screen that accepts a barcode scan
**AND** a valid single-use barcode that the POS accepts is available to scan
**AND** the POS is communicating with CloudFare
**AND** example: a Rail single-use barcode (type B) scanned at the barcode-scan screen
**WHEN** the operator scans the valid barcode
**THEN** the barcode is read
**AND** the corresponding action or product is recognised
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100440 · Barcode — offline validations stored until reconnect  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100317,MODE-NIR-ONLY
_Functional / Barcode Scanning_

**GIVEN** the POS is offline with no connection to CloudFare/Corethree
**AND** single-use barcodes at or below the offline Ceiling Limit are available to validate
**AND** example: two Rail single-use barcodes validated while offline, then the POS reconnects
**WHEN** the operator validates the barcodes offline
**THEN** the offline validations are stored in a list on the device
**WHEN** the connection to CloudFare/Corethree is re-established
**THEN** the stored validations are synced
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4103570 · Barcode — a single-use barcode is validated online and shows a green tick  (1m)  — PARTIAL; refs: FBD-100317,FBD-100167,MODE-NIR-ONLY
_Functional / Barcode Validation_

**GIVEN** a POS is signed on in rail mode with a live connection to Corethree
**AND** single-use rail barcode types B, U, E, S, D and H are accepted on a POS (Translink scheme id 5720)
**AND** example: a type B (no-date) single-use barcode for product 640 Cross Border Standard Adult Single, presented within its validity window
**WHEN** the operator scans the single-use barcode
**THEN** the barcode is validated online against Corethree
**AND** a green tick is shown
**AND** a success tone is played
**WHEN** the result screen is shown
**THEN** the ticket type Display Description is shown on the result screen

### C4103571 · Barcode — a multiple-use barcode is rejected as not accepted on the POS  (1m)  — PARTIAL; refs: FBD-100167,FBD-100317,MODE-NIR-ONLY
_Functional / Barcode Validation_

**GIVEN** a POS is signed on and able to scan barcodes
**AND** the POS validates single-use barcodes only and never multiple-use barcodes
**AND** example: a multiple-use mLink barcode for the "Barc - Adult Single" barcode-use product
**WHEN** the operator scans the multiple-use barcode
**THEN** the message "This Barcode Type is not accepted on this device" is displayed
**AND** the barcode is not validated

### C4103572 · Barcode — a Manifest (type F) barcode is rejected as not accepted on the POS  (1m)  — PARTIAL; refs: FBD-100317,FBD-100167,MODE-NIR-ONLY
_Functional / Barcode Validation_

**GIVEN** a POS is signed on and able to scan barcodes
**AND** single-use type F (Manifest) is accepted only on an ETM, never on a POS
**AND** example: a type F Manifest barcode intended for ETM validation
**WHEN** the operator scans the type F Manifest barcode
**THEN** the message "This Barcode Type is not accepted on this device" is displayed
**AND** the barcode is not validated

### C4103573 · Barcode — offline single-use validation is allowed only at or below the Ceiling Limit  (1m)  — PARTIAL; refs: FBD-100317,MODE-NIR-ONLY
_Functional / Barcode Validation_

**GIVEN** a POS is signed on but offline from Corethree
**AND** offline single-use validation is permitted only when the ticket value is at or below the BOS-configured Ceiling Limit
**AND** example: a Ceiling Limit of £10.00, a type B barcode worth £8.00, and a second worth £12.00
**WHEN** the operator scans the £8.00 barcode while offline
**THEN** the £8.00 barcode is validated offline
**WHEN** the operator then scans the £12.00 barcode while offline
**THEN** the £12.00 barcode is rejected as above the Ceiling Limit

### C4103574 · Barcode — an offline single-use redemption syncs back to Corethree on reconnect  (1m)  — PARTIAL; refs: FBD-100317,MODE-NIR-ONLY
_Functional / Barcode Validation_

**GIVEN** a POS validated a single-use barcode offline while disconnected from Corethree
**AND** example: a type B barcode for product 640 redeemed offline at £8.00, under the £10.00 Ceiling Limit
**WHEN** the POS reconnects to Corethree
**THEN** the offline redemption is synced back to Corethree
**AND** a later attempt to reuse the same barcode is rejected as already redeemed

### C4103575 · Barcode — a successful single-use validation is audited as an event, not a MERIT transaction  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100317,FBD-100318,MODE-NIR-ONLY
_Functional / Barcode Validation_

**GIVEN** a POS validated a single-use barcode successfully
**AND** single-use validations are audited as events, whereas multiple-use validations (not accepted on the POS) would be BarcodeUsage zero-fare transactions
**AND** example: a redeemed type B barcode for product 640 carrying its Unique ID
**WHEN** the validation record reaches CloudFare
**THEN** the record is posted as an event in the Activity Log
**AND** the barcode Unique ID is searchable in the event Message field
**AND** the event is not synced to MERIT

### C4103576 · Barcode — a failed validation is audited as an event carrying the Unique ID and reason  (4m)  — PARTIAL; cross-check: CloudFare; refs: FBD-100167,FBD-100318,MODE-NIR-ONLY
_Functional / Barcode Validation_

**GIVEN** a POS attempted to validate a single-use barcode that failed validation
**AND** example: a type B barcode presented after its expiry, rejected on screen with a red cross
**WHEN** the failed-validation record reaches CloudFare
**THEN** the record is posted as an event
**AND** the event carries the barcode Unique ID
**AND** the event carries the failure reason

### C4103577 · Barcode — a damaged barcode is validated by keying its 12-digit BRID  (1m)  — PARTIAL; refs: FBD-100317,MODE-NIR-ONLY
_Functional / Barcode Validation_

**GIVEN** a POS is signed on with a live connection to Corethree
**AND** a BRID is a 12-digit fallback whose first two digits give the source (12 = Being, 13 = MMT, 99 = Test)
**AND** example: a damaged type B ticket with BRID 120428500786 (source 12, Being)
**WHEN** the operator keys the 12-digit BRID instead of scanning
**THEN** the ticket is validated online by its BRID
**AND** a green tick is shown
**AND** a success tone is played

### C4099996 · Annulment — annul last transaction  (9m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-19352,TIBU-24878,MODE-ALL
_Functional / Basket & Payment / Annulment_

**GIVEN** the POS is signed on as an Operator
**AND** the operator has issued a ticket this shift, e.g. an Adult Single £2.30 on route 10A
**WHEN** the operator annuls the last transaction
**THEN** the last transaction is annulled
**WHEN** there is no transaction available to annul
**THEN** the 'No ticket to Annul' option is greyed out
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4099997 · Annulment — newly issued smartcard  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-24334,TIBU-23949,TIBU-26760,MODE-ALL
_Functional / Basket & Payment / Annulment_

**GIVEN** the POS is signed on as an Operator
**AND** the operator has just issued a new smartcard, e.g. an iLink Zone 1 Adult card
**WHEN** the operator annuls that smartcard issue
**THEN** the smartcard issue is annulled successfully
**AND** the annulment is recorded
**AND** the annulment receipt prints
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4099998 · Annulment — multi-journey top-up  (11m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-25072,TIBU-25100,MODE-ALL
_Functional / Basket & Payment / Annulment_

**GIVEN** the POS is signed on as an Operator
**AND** the operator has just topped up a multi-journey smartcard, e.g. a 10-journey Ulsterbus Multi-Journey top-up (£20)
**WHEN** the operator annuls the top-up
**THEN** the top-up is annulled
**AND** the journey count on the card is corrected
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4099999 · Annulment — receipt content  (7m)  — PARTIAL; cross-check: CloudFare; refs: TIBU-23932,TIBU-25888,TIBU-25889,TIBU-25402,TIBU-25404,TIBU-25800,TIBU-25116,MODE-ALL
_Functional / Basket & Payment / Annulment_

**GIVEN** the POS is signed on as an Operator
**AND** the operator has annulled a transaction, e.g. an Ulsterbus Multi-Journey top-up
**WHEN** the annulment receipt prints
**THEN** the receipt shows the correct title, card type and journey/cancellation information
**AND** the card type text is not cut short
**AND** the Tray ID is present
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100000 · Annulment — during paper jam  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-19311,TIBU-20980,MODE-ALL
_Functional / Basket & Payment / Annulment_

**GIVEN** the POS is signed on as an Operator
**AND** the printer is in a paper-jam state after a transaction, e.g. an Adult Single £2.30 issue
**WHEN** the operator presses Annul Transaction on the Paper Jam screen
**THEN** the annul control responds
**AND** the transaction is annulled

### C4100386 · Annulment — Belfast Visitor Pass  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-21443,MODE-ALL
_Functional / Basket & Payment / Annulment_

**GIVEN** the POS is signed on as an Operator
**AND** the operator has just issued an Adult Belfast Visitors Pass
**WHEN** the operator annuls the issue
**THEN** the Belfast Visitors Pass issue is annulled successfully
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100387 · Annulment — re-present different card  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-25073,MODE-ALL
_Functional / Basket & Payment / Annulment_

**GIVEN** the POS is signed on as an Operator
**AND** the operator is annulling the last transaction, e.g. a multi-journey top-up made moments earlier
**WHEN** a different card from the original is presented during the annul flow
**THEN** the card mismatch is handled gracefully
**AND** the device is not left stuck
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100505 · Annulment — ticket issue  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-ALL
_Functional / Basket & Payment / Annulment_

**GIVEN** the POS is signed on as an Operator
**AND** the operator has just issued a ticket this shift, e.g. an Adult Single £2.30 on route 10A
**WHEN** the operator annuls that ticket issue
**THEN** the ticket issue is annulled
**AND** the annulment is recorded
**AND** an annulment receipt is printed
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4099989 · Basket — add & review  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-21777,TIBU-24364,MODE-ALL
_Functional / Basket & Payment / Basket_

**GIVEN** the POS is signed on as an Operator on the Fare-Look-Up (FLU) screen
**AND** the operator has built one or more fares, e.g. Adult Single £2.30 + Child Single £1.15 on a valid route (Casement Park → City Hall)
**WHEN** the operator adds the fares to the basket and opens the basket
**THEN** the basket lists each added item
**AND** the basket total is correct (£3.45 for the example)
**AND** the expected basket controls are present (Add More, Clear Basket)
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4099990 · Basket — clear basket  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-24368,MODE-ALL
_Functional / Basket & Payment / Basket_

**GIVEN** the POS is signed on as an Operator
**AND** the basket contains two or more items, e.g. Adult Single £2.30 + Child Single £1.15 on a valid route
**WHEN** the operator presses Clear Basket
**THEN** the basket is emptied of all items
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4099991 · Basket — checkout total  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-24098,TIBU-24860,MODE-ALL
_Functional / Basket & Payment / Basket_

**GIVEN** the POS is signed on as an Operator
**AND** the basket contains multiple items, e.g. 2 × Adult Single £2.30 + Child Single £1.15 on a valid route
**WHEN** the operator proceeds to payment
**THEN** the payment total equals the sum of the basketed items (£5.75 for the example)
**AND** Add More is unavailable when the basket cannot accept another ticket
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100432 · Basket — maximum of 9 tickets  (9m)  — PARTIAL; **DESTRUCTIVE**; cross-check: CloudFare / MERIT; refs: MODE-ALL
_Functional / Basket & Payment / Basket_

**GIVEN** the POS is signed on as an Operator on the FLU screen
**AND** the operator is adding Adult Single £2.30 tickets on a valid route to the basket
**WHEN** the basket reaches 9 tickets
**THEN** the Add More control becomes unavailable
**WHEN** the operator deletes a ticket from the basket
**THEN** the Add More control becomes available again
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100433 · Basket — entitlement passes cannot be basketed  (11m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-ALL
_Functional / Basket & Payment / Basket_

**GIVEN** the POS is signed on as an Operator
**AND** the operator has built a fare using a smartcard entitlement pass, e.g. a Senior SmartPass on a valid route
**WHEN** the operator attempts to add the entitlement-pass fare to the basket
**THEN** the fare cannot be added to the basket
**AND** the fare must be validated and paid as an individual transaction
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100434 · Basket — bus basket is single-route  (9m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-ULSTERBUS-ONLY,MODE-METRO-ONLY
_Functional / Basket & Payment / Basket_

**GIVEN** the POS is signed on as an Operator in Ulsterbus mode
**AND** the operator is building a bus basket on route 10A with an Adult Single £2.30 already added
**WHEN** the operator tries to add a ticket from a different route (e.g. route 12B)
**THEN** the second-route ticket is not allowed into the basket
**WHEN** the operator adds tickets with two different boarding stages on route 10A
**THEN** both same-route tickets are accepted
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4099994 · Card Payment — pay by card  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-24777,TIBU-24834,MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Basket & Payment / Card Payment_

**GIVEN** the POS is signed on as an Operator in NIR or Ulsterbus mode with a payment card device (PCD) attached
**AND** the basket is ready for payment, e.g. Adult Single £2.30 on route 10A
**WHEN** the operator selects Bank Card and the customer pays by contactless, chip & PIN, or swipe
**THEN** the payment terminal authorises the transaction
**AND** the ticket is printed as soon as the transaction succeeds
**AND** the customer is offered an optional payment receipt
**AND** the POS returns to the Bus/Rail FLU screen
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4099995 · Card Payment — back from payment  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-24876,MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Basket & Payment / Card Payment_

**GIVEN** the POS is signed on as an Operator in NIR or Ulsterbus mode with a PCD attached
**AND** the operator is on the payment screen for a single Adult Single £2.30 ticket
**WHEN** the operator presses Back
**THEN** the operator is returned to the basket/fare
**AND** the basket/fare state is intact
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100424 · Card Payment — declined, cancelled or error  (9m)  — PARTIAL; cross-check: CloudFare; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Basket & Payment / Card Payment_

**GIVEN** the POS is signed on as an Operator in NIR or Ulsterbus mode with a PCD attached
**AND** the customer is paying an Adult Single £2.30 by bank card
**WHEN** the card is declined
**THEN** a declined message is shown
**AND** a declined receipt is printed
**WHEN** the customer cancels on the PIN pad before entering the PIN
**THEN** the transaction is cancelled
**AND** no cancelled-payment receipt is printed
**WHEN** the PIN is entered incorrectly too many times, or the signature does not match
**THEN** the matching error message (driven by the M020/PCD) is shown
**AND** choosing Print Receipt or Back to Main returns to the FLU screen (a 3-second timeout or any key instead returns to the payment screen)
**WHEN** the transaction amount is too large for the card (test transactions only)
**THEN** the Amount Too Large error is shown
**AND** choosing Print Receipt or Back to Main returns to the FLU screen (a 3-second timeout or any key instead returns to the payment screen)
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4099992 · Cash — pay a basket  (9m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-19336,TIBU-7379,MODE-ALL
_Functional / Basket & Payment / Cash Payment_

**GIVEN** the POS is signed on as an Operator in Ulsterbus mode
**AND** the basket has one or more items, e.g. Adult Single £2.30 + Child Single £1.15 on route 10A
**WHEN** the operator takes cash payment and completes the transaction
**THEN** the transaction completes
**AND** the basket tickets are issued
**WHEN** the operator builds and cash-pays a further basket on a different route (e.g. route 12B)
**THEN** the second transaction also completes
**AND** the device does not freeze
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4099993 · Cash — EOS total net  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-29484,TIBU-30634,MODE-ALL
_Functional / Basket & Payment / Cash Payment_

**GIVEN** the POS is signed on as an Operator in Ulsterbus mode
**AND** the operator has taken cash sales (e.g. 3 × Adult Single £2.30) and made at least one annulment during the shift
**WHEN** the End of Shift cash total is produced
**THEN** the cash total is the net amount, with annulments deducted
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100001 · Receipts — printed per transaction  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-21135,TIBU-21176,TIBU-23016,TIBU-21266,MODE-ALL
_Functional / Basket & Payment / Receipts & Printing_

**GIVEN** the POS is signed on as an Operator
**AND** the operator completes an issuing transaction, e.g. an Adult Single £2.30 ticket, a card issue or a top-up
**WHEN** the transaction completes
**THEN** a receipt is printed
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100002 · Receipts — no duplicates  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-22548,TIBU-22557,MODE-ALL
_Functional / Basket & Payment / Receipts & Printing_

**GIVEN** the POS is signed on as an Operator
**AND** the operator completes a transaction that prints a receipt, e.g. an Adult Single £2.30 ticket
**WHEN** the receipt prints
**THEN** exactly one receipt is produced
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100003 · Receipts — template & fonts  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-23835,TIBU-24890,TIBU-23096,TIBU-16109,TIBU-24848,MODE-ALL
_Functional / Basket & Payment / Receipts & Printing_

**GIVEN** the POS is signed on as an Operator
**AND** the operator prints a ticket/receipt, e.g. an Adult Single £2.30 rail ticket
**WHEN** the printout is produced
**THEN** it uses the correct template, fonts and current Translink logo
**AND** rail ticket templates follow the revised naming
**AND** a missing template is handled gracefully with no crash
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100004 · Receipts — mini statement  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-20759,TIBU-21581,TIBU-23989,TIBU-21178,TIBU-21463,MODE-ALL
_Functional / Basket & Payment / Receipts & Printing_

**GIVEN** the POS is signed on as an Operator
**AND** the operator prints a mini statement for a smartcard, e.g. an Ulsterbus Multi-Journey card
**WHEN** the mini statement prints
**THEN** it shows the correct information including the actual expiry date
**AND** the printout is long enough to contain all content
**AND** an expired multi-journey card still prints its mini statement
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100005 · Receipts — day summary  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-24800,MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Basket & Payment / Receipts & Printing_

**GIVEN** the POS is signed on as an Operator in NIR or Ulsterbus mode
**AND** card transactions have occurred during the day, e.g. an Adult Single £2.30 paid by contactless
**WHEN** the operator prints the day summary
**THEN** the printout includes the card transaction details
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4103581 · Heartbeat — a signed-off POS refreshes Last Communication every 15 minutes via the Staff List check  (4m)  — cross-check: CloudFare; refs: FBD-100266 para 148,165-168,174-175; REQ-0602.4,MODE-PRIMARY-ONLY
_Functional / Comms & Status_

**GIVEN** a POS is signed off with no ticket transactions
**AND** every device performs a Staff List Refresh check every 15 minutes regardless of state (FBD-100266 para 148)
**AND** example: a POS at the Ulsterbus Omagh depot (device home OM) left signed off
**WHEN** the 15-minute Staff List check calls in to CloudFare
**THEN** a StaffList message updates the device Last Communication time
**AND** Hours Since Last Communication is reset to zero
**AND** the update flows into Asset Manager

### C4100033 · Customer Display — passenger display  (3m)  — PARTIAL; refs: TIBU-24845,MODE-ALL
_Functional / Customer Displays_

**GIVEN** the POS is signed on as an Operator building and paying for a fare, e.g. Adult Single £2.30 + Child Single £1.15 on route 10A
**WHEN** the operator adds items and takes payment
**THEN** the passenger display shows the item name (or "Multiple Items" for more than one)
**AND** the passenger display updates as the transaction progresses

### C4100499 · Customer Display — Rail passenger display  (3m)  — PARTIAL; refs: MODE-NIR-ONLY
_Functional / Customer Displays_

**GIVEN** the POS is signed on as an Operator in Rail (NIR) mode building a fare, e.g. an Adult Single rail ticket
**WHEN** the operator adds items and takes payment
**THEN** the passenger display shows the item name (or "Multiple Items" for more than one)
**AND** the passenger display updates as the transaction progresses

### C4100500 · Customer Display — Ulsterbus passenger display  (3m)  — PARTIAL; refs: MODE-ULSTERBUS-ONLY
_Functional / Customer Displays_

**GIVEN** the POS is signed on as an Operator in Ulsterbus mode building a fare, e.g. an Adult Single £2.30 on route 10A
**WHEN** the operator adds items and takes payment
**THEN** the passenger display shows the item name (or "Multiple Items" for more than one)
**AND** the passenger display updates as the transaction progresses

### C4103578 · Fare-Stage Selection — the POS shows and prints the Fare Stage name, not the stop name  (3m)  — PARTIAL; refs: FBD-100207,MODE-ULSTERBUS-ONLY,MODE-METRO-ONLY
_Functional / Fare Look-Up_

**GIVEN** an operator is signed on to a POS building a bus fare
**AND** the POS presents fares by Fare Stage, not by individual stop
**AND** example: on route 72b the boarding stop Moygashel Busby Shop belongs to a Fare Stage (Fare Stage name taken from the fare triangle — confirm against the fares export)
**WHEN** the operator selects the boarding and alighting stages and issues the ticket
**THEN** the result screen shows the Fare Stage name, not the stop name
**AND** the printed ticket shows the Fare Stage name, not the stop name

### C4103579 · Fare-Stage Selection — a zero-fare stage combination blocks ticket issue  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100207,MODE-ULSTERBUS-ONLY,MODE-METRO-ONLY
_Functional / Fare Look-Up_

**GIVEN** an operator is signed on to a POS building a bus fare
**AND** a zero fare for a stage combination means no ticket can be issued for it
**AND** example: on route 72b a boarding/alighting stage combination whose fare-triangle cell is a legitimate zero
**WHEN** the operator selects that zero-fare stage combination
**THEN** the POS does not issue a ticket for the combination
**AND** the operator is prevented from completing the sale

### C4103580 · Fare-Stage Selection — the operator can reach a fare by keying the Fare Stage ID  (1m)  — refs: FBD-100207,MODE-ULSTERBUS-ONLY,MODE-METRO-ONLY
_Functional / Fare Look-Up_

**GIVEN** an operator is signed on to a POS building a bus fare
**AND** a stage can be selected either by scrolling Key Stops with the arrows or by keying the Fare Stage ID on the numeric keypad
**AND** example: on route 72b keying the boarding Fare Stage ID on the numeric keypad instead of scrolling
**WHEN** the operator keys the Fare Stage ID
**THEN** the corresponding Fare Stage is selected
**AND** its fare is displayed for the ticket

### C4099987 · FLU — passenger type  (1m)  — refs: MODE-ALL
_Functional / Fare Look-Up / Common_

**GIVEN** an operator is signed on and building a fare on the POS
**AND** the fare's passenger type can be changed from the passenger-type list
**AND** example: on route 72b, Moygashel Busby Shop → Armagh Bus Centre, changing the passenger type from Adult to Child (fares confirm against the fares export)
**WHEN** the operator selects a passenger type from the list
**THEN** the selected passenger type is applied to the fare
**AND** the displayed price updates to the price for that passenger type

### C4099988 · FLU — cash limit  (5m)  — PARTIAL; **DESTRUCTIVE**; cross-check: CloudFare; refs: MODE-ALL
_Functional / Fare Look-Up / Common_

**GIVEN** an operator is signed on and building a fare on the POS
**AND** a cash limit is configured above which a cash sale cannot complete
**AND** example: on route 72b, adding Adult Single fares (Moygashel Busby Shop → Armagh Bus Centre) until the basket total passes the configured cash limit
**WHEN** a completed cash sale pushes the day's running total over the configured cash limit
**THEN** the Cash Limit notification is shown
**AND** the POS locks, requiring a Supervisor or Technician to be notified
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100024 · Issue Card — issue from blank  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-26845,TIBU-21266,TIBU-26760,TIBU-21208,TIBU-24715,TIBU-25890,MODE-ALL
_Functional / Issue Card / Issue from Blank_

**GIVEN** an operator is signed on to the POS
**AND** a blank smartcard is presented
**AND** the POS is communicating with CloudFare
**AND** example: issue a Metro Multi-Journey onto a blank Smartlink, Metro Inner zone, 10 journeys, paid by cash
**WHEN** the operator selects the product, takes payment and issues it to the card
**THEN** the product is written to the card at the correct price
**AND** a receipt is printed
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100031 · Issue Card — recognised by other devices  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-21446,TIBU-22603,TIBU-23996,TIBU-26721,TIBU-26722,MODE-ALL
_Functional / Issue Card / Issue from Blank_

**GIVEN** an operator has created a new smartcard from blank on the POS
**AND** the POS is communicating with CloudFare
**AND** example: a Multi-Journey card issued on the POS, presented to an ETM, then returned to the POS for top-up
**WHEN** the card is presented to another device (ETM/TVM) and then back to the POS for top-up
**THEN** the card is recognised as valid
**AND** it can be topped up
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100390 · Issue Card — blank card options  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-23963,MODE-ALL
_Functional / Issue Card / Issue from Blank_

**GIVEN** an operator is signed on to the POS
**AND** an Adult BVP or iLink Zone 1 blank card is placed on the POS
**AND** the POS is communicating with CloudFare
**AND** example: an Adult BVP blank card, selecting the Adult Belfast Visitors option
**WHEN** the operator selects the Adult Belfast Visitors option
**THEN** the correct Belfast Visitors options are offered
**AND** the iLink Zone card options are not shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100430 · Numerical Input — group ticket  (9m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: knowledge/flows/flow-annotations.md (Overflow POS flow notes — Numerical Input / Group Ticket,lines ~321-331),MODE-ALL
_Functional / Numerical Input_

**GIVEN** the POS is signed on as an Operator
**AND** the operator has selected a group-eligible product with boarding/alighting set, e.g. Adult Single £2.30 on route 10A (group eligibility configured in CloudFare)
**WHEN** the operator enters a passenger count (or uses + / -) up to 100 and confirms, e.g. 4 passengers
**THEN** a single group ticket is printed
**AND** one back-office transaction is recorded with a sub-element per passenger
**WHEN** the operator selects a non-group-eligible product
**THEN** the "Group Ticket Unavailable" error is shown
**WHEN** the operator enters an invalid count for a group-eligible product
**THEN** the "No Group Ticket" error is shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100431 · Numerical Input — calculate change  (7m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-PRIMARY-ONLY
_Functional / Numerical Input_

**GIVEN** the POS is signed on as an Operator taking a cash payment, e.g. an Adult Single £2.30
**WHEN** the operator enters the amount tendered (e.g. £5.00) and selects Calculate Change
**THEN** the change is calculated
**AND** the change is shown (£2.70 for the example)
**WHEN** too many digits are entered, or the amount is less than the ticket value, or the previous transaction had no value
**THEN** the Calculate Change option is unavailable

### C4099939 · Operator Break — enter Break  (6m)  — cross-check: CloudFare; refs: TIBU-24335,TIBU-24879,TIBU-30633,MODE-PRIMARY-ONLY
_Functional / Operator / Break Mode_

**GIVEN** an operator is signed on to the POS and in service
**AND** the POS is a Way6 Android POS in a live operating mode
**AND** example: the operator takes a break mid-shift and selects Operator Break
**WHEN** the operator selects Operator Break
**THEN** a Break confirmation screen is shown
**WHEN** the operator confirms
**THEN** the POS enters Break mode showing the Break screen
**AND** the Break screen does not show a Bus number
**AND** all on-screen text is spelled correctly
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4099940 · Operator Break — leave Break  (5m)  — cross-check: CloudFare; refs: MODE-PRIMARY-ONLY
_Functional / Operator / Break Mode_

**GIVEN** the POS is in Operator Break mode with an operator signed on
**AND** example: the operator ends the break and selects to leave Break
**WHEN** the operator leaves Break manually and signs back in
**THEN** the POS returns to the Main Screen (Rail selected)
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4099936 · Operator Options — correct options listed  (3m)  — PARTIAL; refs: TIBU-22640,MODE-PRIMARY-ONLY
_Functional / Operator / Options_

**GIVEN** an operator is signed on to the POS at the main Operator menu
**AND** the POS is a Way6 Android POS in a live operating mode (NIR, Ulsterbus or Metro)
**AND** example: the operator opens Operator Options to review the listed entries
**WHEN** the operator opens Operator Options
**THEN** the expected operator options are listed
**AND** no 'Report Faulty Payment Device' option is shown

### C4099937 · Operator Options — cancel Soft Reboot  (5m)  — **DESTRUCTIVE**; cross-check: CloudFare; refs: TIBU-24727,MODE-PRIMARY-ONLY
_Functional / Operator / Options_

**GIVEN** an operator is signed on to the POS
**AND** the operator has opened Operator Options and selected Soft Reboot so the Soft Reboot confirmation is displayed
**AND** example: the operator decides not to reboot and presses Cancel on the confirmation
**WHEN** the operator presses Cancel on the Soft Reboot confirmation
**THEN** the POS returns to Operator Options
**AND** no soft reboot is performed
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4099945 · Totals — view & print  (2m)  — PARTIAL; refs: TIBU-20914,MODE-PRIMARY-ONLY
_Functional / Operator / Totals_

**GIVEN** an operator is signed on to the POS with sales recorded this shift
**AND** the POS has paper loaded ready to print
**AND** example: the operator selects Totals to review the shift, then prints the totals slip
**WHEN** the operator selects Totals
**THEN** the operator's shift totals are displayed
**WHEN** the operator prints the totals
**THEN** the totals print without a fatal error

### C4103533 · Cash Refund — valid URN and amount refunds and prints a receipt  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100373,MODE-PRIMARY-ONLY
_Functional / Refund_

**GIVEN** an Operator is signed on to the POS
**AND** a paper ticket was sold for £13.00 with URN 01122400428500078601300 (23 chars)
**WHEN** the Operator selects Operator Menu, Issue Refund, Cash Refund
**AND** keys the URN and a refund amount of £13.00
**THEN** the refund is accepted
**AND** a success message shows the amount refunded
**WHEN** the refund completes
**THEN** a refund receipt is printed with a customer and operator copy

### C4103534 · Cash Refund — a URN that is not 23 characters is rejected  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100373,MODE-PRIMARY-ONLY
_Functional / Refund_

**GIVEN** an Operator is on the Cash Refund screen
**AND** an example short URN of 011224004285 (12 chars) is to be entered
**WHEN** the Operator keys the short URN and presses Enter
**THEN** an error message and error tone are given
**AND** both the URN and amount fields are cleared for re-entry

### C4103535 · Cash Refund — an amount above the original sale value is rejected  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100373,MODE-PRIMARY-ONLY
_Functional / Refund_

**GIVEN** an Operator is on the Cash Refund screen
**AND** the ticket URN 01122400428500078601300 carries an original sale value of £13.00
**WHEN** the Operator keys the URN and a refund amount of £15.00
**THEN** an error message and error tone are given
**AND** the fields are cleared for re-entry

### C4103536 · Cash Refund — a refund that would make shift totals negative is blocked  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100373,MODE-PRIMARY-ONLY
_Functional / Refund_

**GIVEN** an Operator whose shift cash total is lower than the requested refund
**AND** a valid ticket URN with an original sale value above the shift cash total
**WHEN** the Operator submits the cash refund
**THEN** the message "Cash refund cannot be performed" is displayed
**AND** no refund is issued

### C4103537 · Card Refund — valid PRN refunds via the payment provider and prints a receipt  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100373,MODE-PRIMARY-ONLY
_Functional / Refund_

**GIVEN** an Operator is signed on with a live network to the payment provider
**AND** a card sale printed the PRN P0428500778601300YG on its ticket
**WHEN** the Operator selects Issue Refund, Card Refund, keys the PRN and the refund amount
**AND** confirms the refund
**THEN** the POS calls the payment provider with the amount and PRN
**WHEN** the payment provider returns the refund
**THEN** the provider-returned refunded amount is printed on a refund receipt

### C4103538 · Card Refund — no connection to the payment provider blocks the refund  (3m)  — PARTIAL; refs: FBD-100373,MODE-PRIMARY-ONLY
_Functional / Refund_

**GIVEN** an Operator is on the Card Refund screen with no network to the payment provider
**AND** a valid card-sale PRN P0428500778601300YG
**WHEN** the Operator submits the card refund and the provider call times out
**THEN** an error message and error tone are given
**AND** no refund is issued

### C4103539 · Card Refund — an amount above the original sale value is capped to the original  (6m)  — PARTIAL; cross-check: CloudFare; refs: FBD-100373,MODE-PRIMARY-ONLY
_Functional / Refund_

**GIVEN** an Operator is on the Card Refund screen with a live provider connection
**AND** a card sale of £13.00 with PRN P0428500778601300YG
**WHEN** the Operator keys the PRN and a refund amount of £20.00
**THEN** the provider caps the refund at the £13.00 original sale value
**AND** the £13.00 capped amount is receipted and audited

### C4103540 · Refund — only the Operator role can issue a refund  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100373,MODE-PRIMARY-ONLY
_Functional / Refund_

**GIVEN** the POS is signed on as a Supervisor, Technician or Administrator
**WHEN** the user opens the Operator Menu
**THEN** the Issue Refund option is not available to that role

### C4103541 · Refund — the audit record posts a positive fare with the correct payment method and reference  (6m)  — PARTIAL; cross-check: CloudFare; refs: FBD-100373,MODE-ALL
_Functional / Refund_

**GIVEN** an Operator has completed a £13.00 cash refund on an Ulsterbus POS
**WHEN** the refund transaction is sent to CloudFare
**THEN** the record shows the fare as a positive £13.00
**AND** the Payment Method is 1 for cash (3 for card)
**AND** the Payment Reference is the URN for cash (the PRN for card)
**WHEN** the operator opens the refund record in CloudFare
**THEN** the product is the "Refund" Open product with Allow Refund set
**AND** the Ulsterbus Route Variant Id is populated (the NIR Route Reference Id is used on NIR instead)

### C4103542 · Refund — a completed refund is final and cannot be annulled  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100373,MODE-PRIMARY-ONLY
_Functional / Refund_

**GIVEN** an Operator has completed a refund
**WHEN** the Operator attempts to annul that refund
**THEN** the refund cannot be annulled

### C4103543 · Basket Refund — each ticket URN carries its own value while the card PRN is shared  (1m)  — PARTIAL; refs: FBD-100373,MODE-PRIMARY-ONLY
_Functional / Refund_

**GIVEN** a basket sale of an Adult ticket at £10.00 and a Child ticket at £5.00
**WHEN** the Operator inspects the URN and PRN printed on each ticket
**THEN** each ticket's URN carries its own sale value (£10.00 and £5.00)
**AND** the same PRN is printed on both tickets

### C4103544 · Cross-device Refund — a POS refunds a sale made on another device (CR115)  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100373,CR115,MODE-ALL
_Functional / Refund_

**GIVEN** an Operator on a Bus POS and a paper-ticket sale originally made on a Rail TVM
**AND** cross-device refunds are enabled (CR115)
**WHEN** the Operator issues a refund against that sale's reference
**THEN** the refund is accepted on the POS
**AND** an ETM sale is refundable only when it was originally paid by cash

### C4103582 · Revenue Allocation — a rail ticket sold on an Ulsterbus POS carries the rail route for NIR allocation  (4m)  — cross-check: CloudFare; refs: FBD-100341 para 149-151,MODE-ULSTERBUS-ONLY
_Functional / Revenue Allocation_

**GIVEN** an operator is signed on to a POS whose device home is the Ulsterbus Omagh depot (OM)
**AND** MERIT revenue location is derived from the transaction route mode/company, not the device home location
**AND** example: selling an NIR rail single on this Ulsterbus POS
**WHEN** the rail ticket is sold
**THEN** the transaction carries the rail route reference for its NIR sale
**WHEN** the transaction reaches CloudFare
**THEN** CloudFare maps the POS rail sale to the PR (NIR) revenue location
**AND** the revenue is not allocated to the Ulsterbus device home location

### C4099935 · Sign On — audit events  (8m)  — cross-check: CloudFare; refs: MODE-PRIMARY-ONLY
_Functional / Sign On & Session / Audit_

**GIVEN** a valid operator with the seeded ID and PIN
**AND** the POS is communicating with CloudFare
**AND** example: Operator → sign on, sign off, then a forced sign-off
**WHEN** the operator signs on
**THEN** a Sign On event is recorded to CloudFare
**WHEN** the operator signs off
**THEN** a Sign Off event is recorded to CloudFare
**WHEN** a forced sign-off occurs
**THEN** a Forced Sign Off event is recorded to CloudFare

### C4099924 · Sign On — Communication Locked  (7m)  — cross-check: CloudFare; refs: TIBU-28530,TIBU-21278,MODE-PRIMARY-ONLY
_Functional / Sign On & Session / Communication Locked_

**GIVEN** the POS has lost communication with CloudFare for longer than the configured period
**AND** the seeded Operator ID and PIN are available to attempt sign-on
**AND** example: Operator → sign-on is blocked at the Communication Locked screen
**WHEN** you view the idle screen with communications already down
**THEN** the "Communication Locked" screen is shown
**AND** it states the device was automatically locked due to lost communication
**AND** it instructs the operator to "Notify a Supervisor or Technician"
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4099921 · Sign On — incorrect credentials  (7m)  — cross-check: CloudFare; refs: TIBU-22671,TIBU-24379,MODE-PRIMARY-ONLY
_Functional / Sign On & Session / Failures & Lockout_

**GIVEN** the POS is signed off and showing the Sign On screen
**AND** the POS is communicating with CloudFare
**AND** an unrecognised ID or PIN is to be entered (the seeded Operator credentials are the valid reference)
**AND** example: Operator → the Operator menu
**WHEN** the operator enters an unrecognised ID or PIN and presses Enter
**THEN** the "Sign On Failed" screen is shown with "The ID or PIN is incorrect"
**AND** the attempt counter is shown (e.g. "1 of 3")
**AND** the operator is returned to the Sign On screen to retry
**AND** the ID must be entered before the PIN
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4099922 · Sign On — device locks after the configured failed attempts  (7m)  — **DESTRUCTIVE**; cross-check: CloudFare; refs: TIBU-22672,TIBU-22003,MODE-PRIMARY-ONLY
_Functional / Sign On & Session / Failures & Lockout_

**GIVEN** the POS is signed off and showing the Sign On screen
**AND** the failed-attempt lockout threshold is configured via TMS (use the configured value, e.g. 3)
**AND** the POS is communicating with CloudFare
**AND** example: Operator → repeated failed attempts at the Operator sign-on
**WHEN** the operator enters incorrect credentials up to the configured number of times
**THEN** the POS locks on the configured attempt
**AND** a Device Locked screen is shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4099923 · Sign On — unlock with Supervisor card  (7m)  — PARTIAL; cross-check: CloudFare; refs: TIBU-21384,MODE-PRIMARY-ONLY
_Functional / Sign On & Session / Failures & Lockout_

**GIVEN** the POS is displaying the Device Locked screen
**AND** the POS is communicating with CloudFare
**AND** a valid Supervisor card is available
**AND** example: Supervisor → the Supervisor card unlocks to the Sign On screen
**WHEN** a supervisor presents a valid Supervisor card
**THEN** the POS is unlocked
**AND** the POS returns to the Sign On screen
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4099912 · Sign On — screen, field entry and the 'C' key  (10m)  — PARTIAL; cross-check: CloudFare; refs: REQ-0050,MODE-PRIMARY-ONLY
_Functional / Sign On & Session / Idle & Screen_

**GIVEN** the POS is signed off and idle at the Sign On screen
**AND** the seeded Operator ID and PIN are available for the field-entry checks
**AND** example: Operator → the Operator menu
**WHEN** the Sign On screen is displayed
**THEN** the ID field is shown
**AND** the PIN field is shown
**WHEN** the operator keys digits into a field
**THEN** the field updates to show the entered digits
**WHEN** the operator presses the 'C' key
**THEN** one character is cleared per key press
**WHEN** no entry is made
**THEN** the POS remains on or returns to the idle Sign On screen
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4099929 · Sign Off — by role  (7m)  — cross-check: CloudFare; refs: TIBU-21440,TIBU-26846,MODE-PRIMARY-ONLY
_Functional / Sign On & Session / Sign Off_

**GIVEN** an operator is signed on to the POS
**AND** the POS is communicating with CloudFare
**AND** example: Operator → the Operator menu, then Sign Off
**WHEN** the operator signs off
**THEN** the POS returns to the idle screen
**AND** the sign-off is audited
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4099933 · Sign Off — automatic (inactivity)  (7m)  — cross-check: CloudFare; refs: MODE-PRIMARY-ONLY
_Functional / Sign On & Session / Sign Off_

**GIVEN** an operator is signed on to the POS
**AND** the Auto Sign Off inactivity period is configured (use the configured value)
**AND** the POS is communicating with CloudFare
**AND** example: Operator → signed on, then left with no interaction
**WHEN** the configured Auto Sign Off period elapses with no interaction
**THEN** the POS goes to the Operator Break screen
**AND** no waybill is printed
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4099934 · Sign Off — forced by power cycle  (6m)  — cross-check: CloudFare; refs: TIBU-24790,MODE-PRIMARY-ONLY
_Functional / Sign On & Session / Sign Off_

**GIVEN** an operator is signed on to the POS during a shift
**AND** the Auto Sign Off period is configured (use the configured value)
**AND** the POS is communicating with CloudFare
**AND** example: Operator → signed on, then the POS is powered off for longer than the configured Auto Sign Off time and back on
**WHEN** the POS is power-cycled for longer than the configured Auto Sign Off time
**THEN** on restart the POS returns to the Idle screen with no waybill printed
**AND** exactly one Forced Sign-off event is recorded to CloudFare

### C4099913 · Sign On — by role (manual and smartcard)  (8m)  — PARTIAL; cross-check: CloudFare; refs: REQ-0050,REQ-0056,REQ-0276,REQ-2821,REQ-3013,TIBU-19559,MODE-PRIMARY-ONLY
_Functional / Sign On & Session / Sign On_

**GIVEN** the POS is signed off at the idle Sign On screen
**AND** the POS is communicating with CloudFare
**AND** the seeded ID and PIN, and a valid staff smartcard, are available for the role under test
**AND** example: Operator → the Operator menu
**WHEN** the operator enters a valid ID and PIN and confirms
**THEN** the operator is authenticated
**AND** the menu for their role is displayed (Metro Operator: the Please Present Smartcard screen, not a menu)
**WHEN** the operator instead presents a valid staff smartcard
**THEN** the ID is pre-populated from the card
**AND** after a valid PIN the menu for their role is displayed (Metro Operator: the Please Present Smartcard screen, not a menu)
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4099925 · Sign On — Message and Word & Colour of the Day  (10m)  — PARTIAL; cross-check: CloudFare; refs: MODE-PRIMARY-ONLY
_Functional / Sign On & Session / Sign-on Messages_

**GIVEN** the POS is signed off at the Sign On screen
**AND** the seeded Operator ID and PIN are available to sign on
**AND** the POS is communicating with CloudFare
**AND** example: Operator → the Operator menu
**WHEN** the Message of the Day is available during sign-on
**THEN** it is presented for the operator to confirm
**WHEN** the Message of the Day cannot be retrieved
**THEN** the Message of the Day Unavailable state is shown
**AND** sign-on continues
**WHEN** the Word & Colour of the Day is available
**THEN** it is presented for the operator to confirm
**WHEN** the Word & Colour of the Day cannot be retrieved
**THEN** the Word & Colour Unavailable state is shown
**AND** sign-on continues
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100413 · Smartcard — Half Fare (NDL)  (9m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-24795,MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Smartcards_

**GIVEN** the POS is signed on and selling a fare in NIR or Ulsterbus mode
**AND** a Half Fare No Driving Licence (NDL) entitlement smartcard is available
**AND** example: selling an Ulsterbus Adult Single, the half-fare rate is applied on presenting the card
**WHEN** the operator presents the Half Fare smartcard
**THEN** the card is recognised
**AND** the half-fare entitlement is applied to the fare
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100415 · Smartcard — yLink  (9m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: FBD-100250,MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Smartcards_

**GIVEN** the POS is signed on and selling a fare in NIR or Ulsterbus mode
**AND** a yLink entitlement smartcard is available (a personalised Funded card)
**AND** example: selling a NIR Adult Single, the yLink entitlement is applied on presenting the card
**WHEN** the operator presents the yLink smartcard
**THEN** the card is recognised
**AND** the yLink entitlement is applied to the fare
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100416 · Smartcard — 24+  (9m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: FBD-100250,MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Smartcards_

**GIVEN** the POS is signed on and selling a fare in NIR or Ulsterbus mode
**AND** a 24+ entitlement smartcard is available (a personalised Funded card)
**AND** example: selling a NIR Adult Single, the 24+ entitlement is applied on presenting the card
**WHEN** the operator presents the 24+ smartcard
**THEN** the card is recognised
**AND** the 24+ entitlement is applied to the fare
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100418 · Smartcard — Dependants Pass  (9m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: FBD-100250 (Corporate card taxonomy),MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Smartcards_

**GIVEN** the POS is signed on and selling a fare in NIR or Ulsterbus mode
**AND** a Dependants Pass entitlement smartcard is available (a Corporate card — FBD-100250)
**AND** example: selling a NIR Adult Single, the dependants-pass entitlement is applied on presenting the card
**WHEN** the operator presents the Dependants Pass smartcard
**THEN** the card is recognised
**AND** the dependants-pass entitlement is applied to the fare
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4104604 · Smartcard — Half Fare (LD)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-24795,MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Smartcards_

**GIVEN** the POS is signed on and selling a fare in NIR or Ulsterbus mode
**AND** a Half Fare Learning Disability (LD) entitlement smartcard is available
**AND** example: selling an Ulsterbus Adult Single, the half-fare rate is applied on presenting the card
**WHEN** the operator presents the Half Fare smartcard
**THEN** the card is recognised
**AND** the half-fare entitlement is applied to the fare
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4104605 · Smartcard — Half Fare (PIPS)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-24795,MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Smartcards_

**GIVEN** the POS is signed on and selling a fare in NIR or Ulsterbus mode
**AND** a Half Fare PIPS entitlement smartcard is available
**AND** example: selling an Ulsterbus Adult Single, the half-fare rate is applied on presenting the card
**WHEN** the operator presents the Half Fare smartcard
**THEN** the card is recognised
**AND** the half-fare entitlement is applied to the fare
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4104606 · Smartcard — Half Fare (Partially Sighted)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-24795,MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Smartcards_

**GIVEN** the POS is signed on and selling a fare in NIR or Ulsterbus mode
**AND** a Half Fare Partially Sighted entitlement smartcard is available
**AND** example: selling an Ulsterbus Adult Single, the half-fare rate is applied on presenting the card
**WHEN** the operator presents the Half Fare smartcard
**THEN** the card is recognised
**AND** the half-fare entitlement is applied to the fare
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4104607 · Smartcard — Half Fare (DLA)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-24795,MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Smartcards_

**GIVEN** the POS is signed on and selling a fare in NIR or Ulsterbus mode
**AND** a Half Fare DLA entitlement smartcard is available
**AND** example: selling an Ulsterbus Adult Single, the half-fare rate is applied on presenting the card
**WHEN** the operator presents the Half Fare smartcard
**THEN** the card is recognised
**AND** the half-fare entitlement is applied to the fare
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4099950 · Supervisor — Print & Zero  (8m)  — PARTIAL; cross-check: CloudFare; refs: TIBU-24786,MODE-PRIMARY-ONLY
_Functional / Supervisor / Reports & Information_

**GIVEN** a supervisor is signed on to the POS
**AND** the POS has paper loaded and totals accumulated from the shift
**AND** example: the supervisor runs Print and Zero Current at end of shift and confirms Yes
**WHEN** the supervisor selects Print and Zero (Current or Accumulated)
**THEN** a confirmation prompt asks whether to zero the totals after printing
**WHEN** the supervisor confirms Yes
**THEN** the report is printed
**AND** the totals are reset to zero
**AND** the printout includes operator no., POS no., sign-on/off times, tickets sold, revenue, misc revenue, smartcard validations, annulled tickets, first/last ticket numbers and per-ticket detail

### C4099951 · Supervisor — Versions  (4m)  — PARTIAL; cross-check: CloudFare; refs: TIBU-15782,MODE-PRIMARY-ONLY
_Functional / Supervisor / Versions & Comms_

**GIVEN** a supervisor is signed on to the POS
**AND** the POS has paper loaded ready to print
**AND** example: the supervisor opens Versions to record the current software and config versions
**WHEN** the supervisor opens Versions and views the serial, software and configuration versions
**THEN** each version set is displayed with the real version numbers
**AND** each version set can be printed

### C4099952 · Supervisor — Force Comms  (6m)  — cross-check: CloudFare; refs: MODE-PRIMARY-ONLY
_Functional / Supervisor / Versions & Comms_

**GIVEN** a supervisor is signed on to the POS
**AND** the POS is communicating with CloudFare
**AND** example: the supervisor forces a call-in to pull the latest data, refreshes it, then exits
**WHEN** the supervisor initiates a POS-initiated Force Comms
**THEN** the communication is performed
**WHEN** the supervisor refreshes and then exits Force Comms
**THEN** the supervisor returns to the Supervisor menu
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4099953 · Technician — Device Settings  (1m)  — refs: TIBU-16044,TIBU-16228,TIBU-20967,TIBU-24866,MODE-PRIMARY-ONLY
_Functional / Technician / Device Settings_

**GIVEN** a technician is signed on to the POS in Device Settings
**AND** example: setting Home Location OM, a boarding location, a mounting point, and Tray Identifier "AT01"
**WHEN** the technician changes the Home Location, Boarding Location, Mounting Point and Tray Identifier
**THEN** each setting is updated
**AND** the Tray Identifier is stored with its "AT" prefix
**WHEN** the technician leaves and reopens Device Settings
**THEN** each setting is retained

### C4099954 · Technician — Display Settings  (1m)  — refs: TIBU-21129,MODE-PRIMARY-ONLY
_Functional / Technician / Device Settings_

**GIVEN** a technician is signed on to the POS
**AND** example: the technician opens Display Settings and steps the brightness level up and down
**WHEN** the technician opens Display Settings and adjusts the level
**THEN** the screen indicates the current level

### C4100507 · Technician — set Default Boarding Stage  (1m)  — refs: MODE-ULSTERBUS-ONLY
_Functional / Technician / Device Settings_

**GIVEN** a technician is signed on to the POS in Device Settings
**AND** the POS is in a bus operating mode (Ulsterbus) that performs fare look-ups
**AND** example: setting the default boarding stage for the OM (Omagh) home location
**WHEN** the technician sets the Default Boarding Stage
**THEN** the Default Boarding Stage is saved
**AND** subsequent bus fare look-ups use the new default boarding stage

### C4100373 · Display — clock shows correct 24-hour time  (1m)  — refs: TIBU-19560,TIBU-21411,MODE-PRIMARY-ONLY
_Functional / Technician / Display_

**GIVEN** the POS is powered on and time-synced
**AND** example: viewing the clock at a known wall-clock time to confirm it matches local time
**WHEN** the operator views the on-screen clock
**THEN** the time is shown in 24-hour format
**AND** the time is correct for the local time zone (not an hour out)

### C4099955 · Technician — Force Comms  (5m)  — cross-check: CloudFare; refs: TIBU-21096,MODE-PRIMARY-ONLY
_Functional / Technician / Maintenance_

**GIVEN** a technician is signed on to the POS
**AND** the POS is communicating with CloudFare
**AND** example: the technician forces a call-in to verify comms, refreshes it, then exits
**WHEN** the technician initiates, refreshes and exits Force Comms
**THEN** each action completes successfully
**AND** no fatal error occurs
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4099957 · Technician — Network Settings  (1m)  — refs: TIBU-24740,TIBU-26905,FBD-100183,MODE-PRIMARY-ONLY
_Functional / Technician / Maintenance_

**GIVEN** a technician is signed on to the POS and on the Network Settings page
**AND** example: switching the Ethernet setting and reopening the page to confirm it stuck
**WHEN** the technician changes the Ethernet setting
**THEN** the Ethernet setting is updated
**AND** the change is applied and retained after the page is reopened

### C4099959 · Technician — Status panels  (2m)  — PARTIAL; refs: FBD-100183,MODE-PRIMARY-ONLY
_Functional / Technician / Maintenance_

**GIVEN** a technician is signed on to the POS
**AND** example: the technician reviews Device Status, then Other Devices, Card Reader and Paper Status while diagnosing the POS
**WHEN** the technician opens the Device Status panel
**THEN** the Device Status panel displays its status information
**WHEN** the technician opens the Other Devices, Card Reader and Paper Status panels
**THEN** each panel displays its relevant status information

### C4099960 · Technician — card reader test  (9m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-24792,FBD-100183,MODE-PRIMARY-ONLY
_Functional / Technician / Maintenance_

**GIVEN** a technician is signed on to the POS on the card-reader test screen
**AND** a valid test smartcard is available to present
**AND** example: the technician presents the test smartcard to confirm the reader is healthy
**WHEN** the technician presents a smartcard to the test screen
**THEN** the test screen reports the card-read result correctly
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4099962 · Technician — change operating mode  (1m)  — refs: TIBU-24868,MODE-PRIMARY-ONLY
_Functional / Technician / Maintenance_

**GIVEN** a technician is signed on to the POS
**AND** the POS supports the NIR, Ulsterbus and Metro operating modes
**AND** example: switching the POS from Ulsterbus to NIR (rail) mode
**WHEN** the technician changes the operating mode from the Technician menu
**THEN** the POS switches to the selected operating mode

### C4100384 · Technician — Paper Status back key  (1m)  — PARTIAL; refs: TIBU-23928,MODE-PRIMARY-ONLY
_Functional / Technician / Maintenance_

**GIVEN** a technician is signed on to the POS on the Paper Status screen
**AND** example: the technician checks Paper Status then presses Back to return to the status panels
**WHEN** the technician presses Back
**THEN** the technician returns to the previous screen
**AND** no fatal error occurs

### C4100508 · TMS — application update  (4m)  — cross-check: CloudFare; refs: MODE-PRIMARY-ONLY
_Functional / Technician / TMS Updates_

**GIVEN** an application update has been published to the POS via TMS
**AND** the POS has queued transactions or unsent data that must survive the update
**AND** example: a new POS application build pushed from TMS to this device
**WHEN** the POS downloads and applies the update
**THEN** the update is applied successfully
**AND** the new application version is shown in Technician → Versions
**WHEN** the update completes
**THEN** no queued transactions or unsent data are lost
**AND** an update audit event is recorded

### C4100509 · TMS — topology update  (5m)  — cross-check: CloudFare; refs: MODE-PRIMARY-ONLY
_Functional / Technician / TMS Updates_

**GIVEN** a topology/configuration update has been published to the POS via TMS
**AND** the POS has queued transactions or unsent data that must survive the update
**AND** example: an updated fares/topology configuration pushed from TMS to this device
**WHEN** the POS downloads and applies the update
**THEN** the update is applied successfully
**AND** the new configuration/topology version is shown in Technician → Versions
**AND** no queued transactions or unsent data are lost
**AND** an update audit event is recorded
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100419 · Single ticket (Adult, cash)  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Tickets_

**GIVEN** an operator is signed on (NIR or Ulsterbus mode)
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult Single, Belfast Lanyon Place → Portadown, paid by cash
**WHEN** the operator builds a Single ticket via the mode's fare look-up
**THEN** the Single ticket is issued at the correct price
**WHEN** the operator takes payment for the passenger type
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100420 · Day Return ticket (Adult)  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Tickets_

**GIVEN** an operator is signed on (NIR or Ulsterbus mode)
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult Day Return, Belfast Lanyon Place → Portadown, paid by cash
**WHEN** the operator builds a Day Return ticket via the mode's fare look-up
**THEN** the Day Return ticket is issued at the correct price
**WHEN** the operator takes payment for the passenger type
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100421 · iLink Single (Zone 4, Adult)  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Tickets_

**GIVEN** an operator is signed on (NIR or Ulsterbus mode)
**AND** the POS is communicating with CloudFare
**AND** example: Adult iLink Single, iLink Zone 4, against a presented iLink smartcard, paid by cash
**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard
**THEN** the iLink Single is issued
**AND** it is recorded against the presented card
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100422 · Warrant Return  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Tickets_

**GIVEN** an operator is signed on (NIR or Ulsterbus mode)
**AND** the POS is communicating with CloudFare
**AND** example: Adult Warrant Return, Belfast Lanyon Place → Portadown, paid by warrant
**WHEN** the operator builds a Warrant Return
**THEN** the Warrant Return ticket is issued
**WHEN** the operator completes the warrant payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100423 · Family & Friends Day ticket (cash)  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Tickets_

**GIVEN** an operator is signed on (NIR or Ulsterbus mode)
**AND** the POS is communicating with CloudFare
**AND** example: Family & Friends Day ticket, paid by cash
**WHEN** the operator builds a Family & Friends Day ticket
**THEN** the Family & Friends Day ticket is issued
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104608 · Single ticket (Child, cash)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Tickets_

**GIVEN** an operator is signed on (NIR or Ulsterbus mode)
**AND** the POS is communicating with CloudFare
**AND** example: NIR Child Single, Belfast Lanyon Place → Portadown, paid by cash
**WHEN** the operator builds a Single ticket via the mode's fare look-up
**THEN** the Single ticket is issued at the correct price
**WHEN** the operator takes payment for the passenger type
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104609 · Single ticket (concession, cash)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Tickets_

**GIVEN** an operator is signed on (NIR or Ulsterbus mode)
**AND** the POS is communicating with CloudFare
**AND** example: NIR concession Single, Belfast Lanyon Place → Portadown, paid by cash
**WHEN** the operator builds a Single ticket via the mode's fare look-up
**THEN** the Single ticket is issued at the correct price
**WHEN** the operator takes payment for the passenger type
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104610 · Single ticket (Adult, card)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Tickets_

**GIVEN** an operator is signed on (NIR or Ulsterbus mode)
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult Single, Belfast Lanyon Place → Portadown, paid by card
**WHEN** the operator builds a Single ticket via the mode's fare look-up
**THEN** the Single ticket is issued at the correct price
**WHEN** the operator takes payment for the passenger type
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104611 · Single ticket (Adult, warrant)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Tickets_

**GIVEN** an operator is signed on (NIR or Ulsterbus mode)
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult Single, Belfast Lanyon Place → Portadown, paid by warrant
**WHEN** the operator builds a Single ticket via the mode's fare look-up
**THEN** the Single ticket is issued at the correct price
**WHEN** the operator takes payment for the passenger type
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104612 · Day Return ticket (Child)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Tickets_

**GIVEN** an operator is signed on (NIR or Ulsterbus mode)
**AND** the POS is communicating with CloudFare
**AND** example: NIR Child Day Return, Belfast Lanyon Place → Portadown, paid by cash
**WHEN** the operator builds a Day Return ticket via the mode's fare look-up
**THEN** the Day Return ticket is issued at the correct price
**WHEN** the operator takes payment for the passenger type
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104613 · iLink Single (Zone 1, Adult)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Tickets_

**GIVEN** an operator is signed on (NIR or Ulsterbus mode)
**AND** the POS is communicating with CloudFare
**AND** example: Adult iLink Single, iLink Zone 1, against a presented iLink smartcard, paid by cash
**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard
**THEN** the iLink Single is issued
**AND** it is recorded against the presented card
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104614 · iLink Single (Zone 2, Adult)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Tickets_

**GIVEN** an operator is signed on (NIR or Ulsterbus mode)
**AND** the POS is communicating with CloudFare
**AND** example: Adult iLink Single, iLink Zone 2, against a presented iLink smartcard, paid by cash
**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard
**THEN** the iLink Single is issued
**AND** it is recorded against the presented card
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104615 · iLink Single (Zone 3, Adult)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Tickets_

**GIVEN** an operator is signed on (NIR or Ulsterbus mode)
**AND** the POS is communicating with CloudFare
**AND** example: Adult iLink Single, iLink Zone 3, against a presented iLink smartcard, paid by cash
**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard
**THEN** the iLink Single is issued
**AND** it is recorded against the presented card
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104616 · iLink Single (NW Zone, Adult)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Tickets_

**GIVEN** an operator is signed on (NIR or Ulsterbus mode)
**AND** the POS is communicating with CloudFare
**AND** example: Adult iLink Single, iLink NW Zone, against a presented iLink smartcard, paid by cash
**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard
**THEN** the iLink Single is issued
**AND** it is recorded against the presented card
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104617 · iLink Single (Zone 4, Child)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Tickets_

**GIVEN** an operator is signed on (NIR or Ulsterbus mode)
**AND** the POS is communicating with CloudFare
**AND** example: Child iLink Single, iLink Zone 4, against a presented iLink smartcard, paid by cash
**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard
**THEN** the iLink Single is issued
**AND** it is recorded against the presented card
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104618 · Family & Friends Day ticket (card)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Tickets_

**GIVEN** an operator is signed on (NIR or Ulsterbus mode)
**AND** the POS is communicating with CloudFare
**AND** example: Family & Friends Day ticket, paid by card
**WHEN** the operator builds a Family & Friends Day ticket
**THEN** the Family & Friends Day ticket is issued
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104619 · Family & Friends Day ticket (warrant)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Tickets_

**GIVEN** an operator is signed on (NIR or Ulsterbus mode)
**AND** the POS is communicating with CloudFare
**AND** example: Family & Friends Day ticket, paid by warrant
**WHEN** the operator builds a Family & Friends Day ticket
**THEN** the Family & Friends Day ticket is issued
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100022 · Faulty Card — options  (8m)  — PARTIAL; cross-check: CloudFare; refs: TIBU-25818,TIBU-21256,MODE-ALL
_Functional / Top Up & Validation / Faulty Card_

**GIVEN** the POS is signed on and selling a fare
**AND** a faulty (unreadable) smartcard is presented — example: a faulty Metro Multi-Journey card
**WHEN** the faulty smartcard screen is shown
**THEN** Charge Full Fare is offered
**AND** Issue Ticket is offered
**AND** Select Card Type is offered
**AND** a Cancel option is available
**WHEN** the operator chooses Issue Ticket then Issue Receipt
**THEN** a ticket is produced
**AND** its receipt is produced
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100023 · Faulty Card — invalid card removal  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-20851,MODE-ALL
_Functional / Top Up & Validation / Faulty Card_

**GIVEN** the POS is signed on
**AND** an invalid top-up card is resting on the reader
**WHEN** the card is removed from the reader
**THEN** the POS detects that the card has been removed
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4102563 · Faulty — Fare-Paying Smartcard  (12m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-ALL
_Functional / Top Up & Validation / Faulty Card_

**GIVEN** the POS is signed on and selling a fare
**AND** a faulty (unreadable) fare-paying smartcard is presented
**WHEN** the card cannot be read correctly
**THEN** the faulty-card options are offered (Charge Full Fare, Select Card Type, Issue Ticket)
**WHEN** the operator selects the appropriate option and completes the transaction
**THEN** a faulty fare-paying smartcard receipt is produced
**WHEN** the CloudFare activity log is checked
**THEN** the faulty-card event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** any fare charged appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the faulty fare-paying smartcard is recorded in SmartTrack

### C4102564 · Faulty — Smartpass Receipt  (11m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: FBD-100250,MODE-ALL
_Functional / Top Up & Validation / Faulty Card_

**GIVEN** the POS is signed on and selling a fare
**AND** a faulty concessionary Smartpass is presented — example: a Senior SmartPass (Fare Foregone)
**WHEN** the operator handles the faulty Smartpass and issues the receipt
**THEN** a faulty Smartpass receipt is produced with the correct content
**WHEN** the CloudFare activity log is checked
**THEN** the faulty-card event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the faulty Smartpass is recorded in SmartTrack
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4102565 · Faulty — Dependants Pass Receipt  (11m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: FBD-100250,MODE-ALL
_Functional / Top Up & Validation / Faulty Card_

**GIVEN** the POS is signed on and selling a fare
**AND** a faulty Dependants Pass is presented (a Corporate card)
**WHEN** the operator handles the faulty Dependants Pass and issues the receipt
**THEN** a faulty Dependants Pass receipt is produced with the correct content
**WHEN** the CloudFare activity log is checked
**THEN** the faulty-card event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the faulty Dependants Pass is recorded in SmartTrack
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100007 · Top Up — top up a smartcard  (10m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-23016,TIBU-21280,TIBU-21119,TIBU-21184,TIBU-22985,FBD-100260,MODE-ALL
_Functional / Top Up & Validation / Top Up_

**GIVEN** the POS is signed on and idle
**AND** a toppable smartcard is presented — example: an Adult iLink Zone 4 travelcard, top up 1 Week, paid by cash (Metro is cash-only, bank card / warrant available on NIR + Ulsterbus)
**WHEN** the operator selects Top Up and the amount
**THEN** the top-up amount and price are shown
**WHEN** the operator takes payment and confirms
**THEN** the card is topped up
**AND** a top-up receipt is printed
**WHEN** the card requires validation for the current journey
**THEN** the card is auto-validated where applicable
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100008 · Top Up — cancel a top-up  (7m)  — PARTIAL; cross-check: CloudFare; refs: TIBU-24858,TIBU-25885,TIBU-21786,MODE-ALL
_Functional / Top Up & Validation / Top Up_

**GIVEN** the POS is signed on
**AND** the operator has started a smartcard top-up — example: a part-completed iLink top-up
**WHEN** the operator cancels or presses Back
**THEN** the operator is returned to the previous screen
**AND** the screen remains responsive
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100009 · Top Up — Multi-Journey limit  (12m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-21133,TIBU-21992,TIBU-24051,TIBU-25886,FBD-100261,MODE-ALL
_Functional / Top Up & Validation / Top Up_

**GIVEN** the POS is signed on
**AND** a Multi-Journey smartcard is presented — example: an Adult Metro Multi-Journey (City zone) card, topping up 10 journeys
**WHEN** the operator tops up journeys
**THEN** the journeys are added
**AND** the added journeys are shown
**WHEN** the operator tries to top up beyond the maximum permitted journeys
**THEN** the card cannot exceed its maximum permitted journeys
**WHEN** a card with expired journeys is topped up
**THEN** the card can still be topped up
**AND** the device does not crash
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100017 · Top Up — mini statement  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-21450,TIBU-22398,TIBU-25098,TIBU-23989,TIBU-22558,MODE-ALL
_Functional / Top Up & Validation / Top Up_

**GIVEN** the POS is signed on
**AND** a topped-up smartcard is presented — example: an Adult iLink Zone 4 travelcard topped up on both the POS and an ETM
**WHEN** the mini statement is shown
**THEN** it shows the correct card type
**AND** it shows the correct card number
**AND** it shows the correct balance/journeys
**AND** it shows the correct start date
**AND** it shows the correct expiry
**AND** it reflects top-ups made on this and other devices
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100389 · Top Up — non-toppable card handled  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-21219,MODE-ALL
_Functional / Top Up & Validation / Top Up_

**GIVEN** the POS is signed on
**AND** a card that cannot be topped up is presented — example: an expired or non-toppable product card
**WHEN** the card is read
**THEN** the POS reports that the card cannot be topped up
**AND** the device does not crash
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100435 · Top Up — expired Multi-Journey clears existing journeys  (11m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-ALL
_Functional / Top Up & Validation / Top Up_

**GIVEN** the POS is signed on
**AND** an expired Multi-Journey card is presented — example: an Adult Metro Multi-Journey (City zone) card past its expiry
**WHEN** the operator adds journeys (tops it up) and the top-up succeeds
**THEN** all existing journeys are removed
**AND** a journey-removal receipt is printed
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102561 · Fare-Paying Smartcard — top-up  (11m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-ALL
_Functional / Top Up & Validation / Top Up_

**GIVEN** the POS is signed on
**AND** a fare-paying (stored-value) smartcard is presented — example: top up £10.00 by cash
**WHEN** the operator tops up the card with value and takes payment
**THEN** the value is added to the card balance
**AND** the new balance is shown
**AND** a receipt is printed
**WHEN** the CloudFare activity log is checked
**THEN** the top-up event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the top-up transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard balance appears in SmartTrack

### C4102562 · Top Up — on expiry  (11m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-ALL
_Functional / Top Up & Validation / Top Up_

**GIVEN** the POS is signed on
**AND** a smartcard is presented on its product expiry date — example: an Adult iLink Zone 4 travelcard topped up 1 Week on its expiry date
**WHEN** the operator tops up the card
**THEN** the top-up is applied
**AND** the product validity is recalculated from the top-up
**WHEN** the CloudFare activity log is checked
**THEN** the top-up event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the top-up transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100018 · Validation — validate a smartcard  (11m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Top Up & Validation / Validation_

**GIVEN** the POS is on the main screen in NIR or Ulsterbus mode (Metro has no smartcard validation)
**AND** a valid smartcard is available — example: an Adult iLink Zone 4 travelcard in date
**WHEN** the valid smartcard is presented for validation
**THEN** the validation confirmation screen is shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100019 · Validation — already validated  (11m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Top Up & Validation / Validation_

**GIVEN** the POS is on the main screen in NIR or Ulsterbus mode
**AND** a smartcard has already been validated — example: an Adult Metro Multi-Journey card validated moments earlier
**WHEN** the card is presented again
**THEN** the 'Smartcard Already Validated' message is shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100020 · Validation — hotlisted card  (11m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Top Up & Validation / Validation_

**GIVEN** the POS is on the main screen in NIR or Ulsterbus mode
**AND** a smartcard that is on the hotlist is available
**WHEN** the hotlisted card is presented
**THEN** the Hotlisted Error is shown
**AND** the card is not accepted
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100021 · Validation — outside time band  (11m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Top Up & Validation / Validation_

**GIVEN** the POS is on the main screen in NIR or Ulsterbus mode
**AND** a smartcard is presented outside its valid time band — example: a time-banded travelcard presented before its start time
**WHEN** the card is read
**THEN** the Outside Time Band handling is applied
**WHEN** the CloudFare activity log is checked
**THEN** the validation outcome is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100428 · Validation — error mid-transaction voids the payment  (8m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Top Up & Validation / Validation_

**GIVEN** the POS is signed on
**AND** a fare is being validated as part of a paid transaction — example: a card fare part-paid when a validation error occurs
**WHEN** a validation error occurs
**THEN** any cash or warrant payment is not recorded in the POS audit data
**AND** any card transaction is automatically voided by the POS
**AND** a diagnostic event is recorded to audit the error
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100506 · Mini Statement — reflects usage and top-ups  (11m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-ALL
_Functional / Top Up & Validation / Validation_

**GIVEN** the POS is signed on
**AND** a smartcard that has been validated/used and topped up is available — example: an Adult iLink Zone 4 card used on an ETM and topped up on the POS
**WHEN** the operator presents the card to view the mini statement
**THEN** the mini statement shows the correct current balance/journeys
**AND** it reflects recent validations/usage
**AND** it reflects top-ups made on this and other devices
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102559 · Fare-Paying Smartcard — validation  (12m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Top Up & Validation / Validation_

**GIVEN** the POS is signed on in NIR or Ulsterbus mode
**AND** a fare-paying smartcard with sufficient balance is presented — example: a stored-value card with £10.00 balance against a £2.30 fare
**WHEN** the operator validates a fare against the card
**THEN** the fare is deducted from the card balance
**AND** the remaining balance is shown
**WHEN** a fare-paying smartcard with insufficient balance is presented
**THEN** the shortfall is handled per the rules
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the fare transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard balance appears in SmartTrack

### C4102560 · Validation — passback  (12m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: FBD-100271,MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY
_Functional / Top Up & Validation / Validation_

**GIVEN** the POS is signed on in NIR or Ulsterbus mode
**AND** a smartcard has just been validated on the POS (passback always applies and takes priority over transfer)
**WHEN** the same smartcard is presented again within the passback period
**THEN** the passback rule is applied
**AND** no second deduction is taken within the period
**WHEN** the same smartcard is presented again after the passback period
**THEN** a new validation is allowed
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100425 · Metro — payment is cash only  (7m)  — PARTIAL; cross-check: CloudFare; refs: MODE-METRO-ONLY
_Metro / Payment & Validation_

**GIVEN** an operator is signed on to the POS in Metro mode
**AND** a Metro fare is ready for payment
**AND** the POS is communicating with CloudFare
**AND** example: a Metro Multi-Journey top-up reaching the payment options
**WHEN** the operator reaches the payment options
**THEN** only the Cash option is offered
**AND** Bank Card is not offered
**AND** Warrant is not offered
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100426 · Metro — no smartcard validation  (11m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-METRO-ONLY
_Metro / Payment & Validation_

**GIVEN** an operator is signed on to the POS in Metro mode
**AND** a smartcard is available to present
**AND** the POS is communicating with CloudFare
**AND** example: a Metro Multi-Journey smartcard presented in Metro mode
**WHEN** a smartcard is presented
**THEN** no validation is performed
**AND** the Metro top-up / smartcard menu behaviour applies instead
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100391 · Top Up — Metro Multi-Journey  (7m)  — PARTIAL; cross-check: CloudFare; refs: TIBU-21133,TIBU-21992,TIBU-25081,MODE-METRO-ONLY
_Metro / Top Up_

**GIVEN** an operator is signed on to the POS in Metro mode
**AND** a pre-encoded Metro Multi-Journey (Smartlink) smartcard is presented
**AND** the POS is communicating with CloudFare
**AND** example: Metro Multi-Journey, Metro Inner zone, add 10 journeys, paid by cash
**WHEN** the operator selects the zone and journeys and takes payment
**THEN** the journeys are added to the card
**AND** the added journeys are shown
**AND** the card cannot exceed its maximum permitted journeys
**AND** the mini-statement expiry text is correct
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4099970 · Rail FLU — sell a ticket  (7m)  — cross-check: CloudFare / MERIT; refs: TIBU-19374,TIBU-24862,TIBU-24853,FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Fare Look-Up_

**GIVEN** an operator is signed on with the POS in rail (NIR) mode on the Main Rail screen
**AND** the POS is communicating with CloudFare
**AND** example: Lisburn → Belfast Lanyon Place, Adult, Single
**WHEN** the operator selects a boarding station, an alighting station, a passenger type and a ticket type
**THEN** the selected fare is displayed
**AND** the correct price is shown, including for Cross-Border tickets
**AND** the field layout is correct
**WHEN** the operator adds the fare to the basket
**THEN** the fare is added to the basket
**AND** the correct boarding and alighting stations are audited
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4099971 · Rail FLU — boarding = alighting rejected  (7m)  — PARTIAL; cross-check: CloudFare; refs: TIBU-19292,FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Fare Look-Up_

**GIVEN** an operator is signed on and building a rail fare with the POS in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: setting both boarding and alighting to Belfast Lanyon Place
**WHEN** the operator sets the boarding and alighting stations to the same station
**THEN** the fare is not accepted
**AND** no issue buttons are offered for it
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4099972 · Rail FLU — station lists & numeric select  (2m)  — refs: TIBU-22953,TIBU-21771,FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Fare Look-Up_

**GIVEN** an operator is signed on and building a rail fare with the POS in rail (NIR) mode
**AND** example: opening the boarding station list and keying the station number for Lisburn
**WHEN** the operator opens the station list
**THEN** the station list is displayed
**WHEN** the operator enters the station number
**THEN** the matching station is selected from the list

### C4099973 · Rail FLU — function keys  (1m)  — refs: TIBU-24774,TIBU-24775,TIBU-21779,TIBU-24827,TIBU-24828,TIBU-21770,MODE-NIR-ONLY
_NIR (Rail) / Fare Look-Up_

**GIVEN** an operator is signed on with the POS on the Rail FLU screen (rail/NIR mode)
**AND** example: pressing R3 for passenger types and R4 for ticket types while building a Lisburn → Belfast Lanyon Place fare
**WHEN** the operator presses a function key (e.g. R3 passengers, R4 ticket types)
**THEN** the corresponding list is displayed with real labels, not placeholder "example" text
**AND** the device does not crash
**AND** buttons that should be unavailable cannot be pressed

### C4099974 · Rail FLU — C returns  (1m)  — refs: TIBU-24810,MODE-NIR-ONLY
_NIR (Rail) / Fare Look-Up_

**GIVEN** an operator is signed on with the POS on a Rail FLU sub-screen (rail/NIR mode)
**AND** example: on the passenger-type list reached while building a Lisburn → Belfast Lanyon Place fare
**WHEN** the operator presses the 'C' button
**THEN** the operator is returned to the previous Rail FLU screen

### C4099975 · Rail FLU — Main screen rail-only  (1m)  — PARTIAL; refs: TIBU-24864,MODE-NIR-ONLY
_NIR (Rail) / Fare Look-Up_

**GIVEN** an operator is signed on with the POS in rail (NIR) mode on the Main Rail screen
**AND** example: viewing the Main Rail screen before building any fare
**WHEN** the operator views the Main Rail screen
**THEN** no 'Bus' button is shown
**AND** no 'Day Tours' button is shown

### C4099976 · Rail FLU — non-Adult-Single keeps state  (3m)  — refs: TIBU-24865,FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Fare Look-Up_

**GIVEN** an operator is signed on and has built a non-Adult-Single rail fare (rail/NIR mode)
**AND** example: a Child Single, Lisburn → Belfast Lanyon Place
**WHEN** the operator issues the ticket
**THEN** the Rail FLU screen retains the correct state
**AND** the screen does not unexpectedly revert

### C4100385 · Rail FLU — present smartcard  (9m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-21933,TIBU-21786,MODE-NIR-ONLY
_NIR (Rail) / Fare Look-Up_

**GIVEN** an operator is signed on with the POS on the Rail FLU screen (rail/NIR mode)
**AND** the POS is communicating with CloudFare
**AND** example: presenting a valid smartcard while building a Lisburn → Belfast Lanyon Place fare
**WHEN** the operator presents a smartcard
**THEN** the smartcard is handled without a fatal error
**AND** the operator can return to the Rail FLU screen
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100429 · Rail FLU — cross-border ticket & currency toggle  (3m)  — refs: TIBU-19374,FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Fare Look-Up_

**GIVEN** an operator is signed on and building a rail fare with a cross-border boarding or alighting station (rail/NIR mode)
**AND** example: Belfast Lanyon Place → Dublin Connolly, Adult (Enterprise cross-border)
**WHEN** the operator views the ticket types
**THEN** cross-border ticket types are shown at the correct price
**WHEN** the operator presses the price button
**THEN** the currency toggles to euro
**WHEN** the operator presses the price button again
**THEN** the currency toggles back to GBP

### C4100501 · Rail FLU — change boarding & alighting stations  (2m)  — refs: FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Fare Look-Up_

**GIVEN** an operator is signed on and has selected a rail fare with boarding and alighting stations (rail/NIR mode)
**AND** example: an Adult Single starting Lisburn → Belfast Lanyon Place, then re-pointed to Portadown → Belfast Lanyon Place
**WHEN** the operator changes the boarding station
**THEN** the fare updates for the new boarding station
**WHEN** the operator changes the alighting station
**THEN** the fare updates for the new alighting station

### C4100502 · Cross-Border — enable Euro currency  (3m)  — PARTIAL; refs: FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Fare Look-Up_

**GIVEN** an operator is signed on and has selected a Cross-Border product on the POS in rail (NIR) mode
**AND** example: Belfast Lanyon Place → Dublin Connolly, Adult (Enterprise cross-border)
**WHEN** Euro currency is enabled and the price is toggled to Euro
**THEN** the Cross-Border fare is shown in Euros
**AND** payment can be taken in the selected currency

### C4099979 · Rail FLU — Advance Ticket  (8m)  — cross-check: CloudFare / MERIT; refs: TIBU-21792,TIBU-22824,TIBU-24826,FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Fare Look-Up — Advance & Multi-day_

**GIVEN** an operator is signed on and has selected Advance Ticket on the Rail FLU (rail/NIR mode)
**AND** the POS is communicating with CloudFare
**AND** example: an Adult Advance, Lisburn → Belfast Lanyon Place, for a valid future date within the advance window
**WHEN** the operator enters a valid future date within the advance range
**THEN** the advance ticket is added
**AND** the basket shows 'Ticket Date DD/MM/YY'
**WHEN** the operator enters an invalid date or one outside the valid advance range
**THEN** an error is shown
**AND** the device does not crash
**WHEN** the operator tries to add an advance ticket alongside other products
**THEN** the advance ticket cannot be combined with other basket items (one at a time)
**WHEN** the advance ticket is left for 1 minute with no interaction
**THEN** the advance date, passenger and ticket type reset
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4099980 · Rail FLU — 3 Day Select  (1m)  — refs: TIBU-24829,TIBU-24837,FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Fare Look-Up — Advance & Multi-day_

**GIVEN** an operator is signed on and has selected a 3 Day Select ticket on the Rail FLU (rail/NIR mode)
**AND** example: choosing three available travel days for an Adult 3 Day Select
**WHEN** the operator chooses the available days from the day list and adjusts them with the + / - buttons
**THEN** the selected days are applied to the ticket

### C4099981 · Rail FLU — Misc button  (1m)  — refs: TIBU-19454,MODE-NIR-ONLY
_NIR (Rail) / Fare Look-Up — Advance & Multi-day_

**GIVEN** an operator is signed on with the POS on the Main Rail FLU screen (rail/NIR mode)
**AND** example: pressing Misc from the Main Rail FLU screen before building a fare
**WHEN** the operator presses the Misc button
**THEN** the Misc option opens
**AND** no fatal error occurs

### C4099977 · Rail FLU — favourites: save & issue  (9m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-19371,TIBU-24783,TIBU-24781,TIBU-19456,FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Fare Look-Up — Favourites_

**GIVEN** an operator is signed on with the POS on the Rail FLU screen (rail/NIR mode)
**AND** the POS is communicating with CloudFare
**AND** example: saving an Adult Single, Lisburn → Belfast Lanyon Place, as a favourite, then selecting it from the list
**WHEN** the operator saves a fare as a favourite and opens the favourites list
**THEN** the favourites list is shown with paging
**AND** the list entries are correctly aligned
**WHEN** the operator selects a favourite
**THEN** the favourite's ticket details are shown
**AND** the flow proceeds to the payment screen
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4099978 · Rail FLU — favourites: overwrite  (6m)  — cross-check: CloudFare; refs: TIBU-24095,TIBU-24776,TIBU-24886,FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Fare Look-Up — Favourites_

**GIVEN** an operator is signed on and is overwriting an existing favourite on the Rail FLU (rail/NIR mode)
**AND** the POS is communicating with CloudFare
**AND** example: overwriting the favourite in slot 1 with an Adult Single, Lisburn → Belfast Lanyon Place
**WHEN** the operator confirms the overwrite
**THEN** the favourite is stored in the correct slot
**AND** no fatal error occurs
**WHEN** the operator instead cancels an overwrite
**THEN** the overwrite is aborted
**AND** no change is made to the favourite
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4099946 · Excess Ticket — available (rail)  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-24804,MODE-NIR-ONLY
_NIR (Rail) / Operator (rail-only)_

**GIVEN** an operator is signed on with the POS in rail (NIR) mode
**WHEN** the operator opens the Operator menu
**THEN** the Excess Ticket feature is available
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100393 · NIR — Single (Adult, cash)  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult Single, Belfast Lanyon Place → Portadown, paid by cash
**WHEN** the operator builds a Single ticket from the boarding station, alighting station and passenger type
**THEN** the Single ticket is issued at the correct price
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100394 · NIR — Day Return (Adult)  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult Day Return, Belfast Lanyon Place → Portadown, paid by cash
**WHEN** the operator builds a Day Return ticket
**THEN** the Day Return ticket is issued at the correct price
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100395 · NIR — 1/3 Off Day Return (Adult)  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult 1/3 Off Day Return, Belfast Lanyon Place → Portadown, paid by cash
**WHEN** the operator builds a 1/3 Off Day Return ticket
**THEN** the ticket is issued with the 1/3 discount applied
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100396 · NIR — Weekly Season (Adult, cash)  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult Weekly Season, Belfast Lanyon Place → Portadown, paid by cash
**WHEN** the operator builds a Weekly Season ticket
**THEN** the Weekly Season ticket is issued with the correct From/To dates
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100397 · NIR — Monthly Season (Adult, cash)  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-19299,FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult Monthly Season, Belfast Lanyon Place → Portadown, paid by cash
**WHEN** the operator builds a Monthly Season ticket
**THEN** the Monthly Season ticket is issued with the correct From/To dates
**AND** the expiry (To) date is one calendar month from the start date
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100398 · NIR — Warrant Return  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult Warrant Return, Belfast Lanyon Place → Portadown, paid by warrant
**WHEN** the operator builds a Warrant Return
**THEN** the Warrant Return ticket is issued
**WHEN** the operator completes the warrant payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100399 · NIR — 3 Day Select (Adult, cash)  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: knowledge/projects/translink.md (Audit-confirmed POS facts — NIR-only ticket list),MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult 3 Day Select, Belfast Lanyon Place → Portadown, paid by cash
**WHEN** the operator builds a 3 Day Select ticket
**AND** chooses the days
**THEN** the 3 Day Select ticket is issued for the chosen days
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100400 · NIR — Family & Friends Day (cash)  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Family & Friends Day, paid by cash
**WHEN** the operator builds a Family & Friends Day ticket
**THEN** the Family & Friends Day ticket is issued
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100401 · NIR — iLink Single (Zone 4, Adult)  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult iLink Single, iLink Zone 4, against a presented iLink smartcard, paid by cash
**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard
**THEN** the iLink Single is issued
**AND** it is recorded against the presented card
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100402 · NIR — Dependants Pass  (6m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: FBD-100335 para 119,MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Dependents Pass smartcard, single journey Belfast Lanyon Place → Botanic
**WHEN** the operator processes a Dependents Pass smartcard fare
**THEN** the Dependents Pass fare is applied
**AND** a receipt is printed
**AND** a green success banner is displayed

### C4100503 · NIR — Cross-Border Single (GBP, cash)  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: Adult Cross-Border Single, Belfast Lanyon Place → Dublin Connolly, priced in GBP, paid by cash
**WHEN** the operator selects a Cross-Border Single
**THEN** the Cross-Border Single ticket is issued
**WHEN** the operator takes payment
**THEN** a green success banner is displayed

### C4100504 · NIR — Cross-Border Day Return (GBP, cash)  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: Adult Cross-Border Day Return, Belfast Lanyon Place → Dublin Connolly, priced in GBP, paid by cash
**WHEN** the operator selects a Cross-Border Day Return
**THEN** the Cross-Border Day Return ticket is issued
**WHEN** the operator takes payment
**THEN** a green success banner is displayed

### C4104620 · NIR — Single (Child, cash)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Child Single, Belfast Lanyon Place → Portadown, paid by cash
**WHEN** the operator builds a Single ticket from the boarding station, alighting station and passenger type
**THEN** the Single ticket is issued at the correct price
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104621 · NIR — Single (concession, cash)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR concession Single, Belfast Lanyon Place → Portadown, paid by cash
**WHEN** the operator builds a Single ticket from the boarding station, alighting station and passenger type
**THEN** the Single ticket is issued at the correct price
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104622 · NIR — Single (Adult, card)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult Single, Belfast Lanyon Place → Portadown, paid by card
**WHEN** the operator builds a Single ticket from the boarding station, alighting station and passenger type
**THEN** the Single ticket is issued at the correct price
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104623 · NIR — Single (Adult, warrant)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult Single, Belfast Lanyon Place → Portadown, paid by warrant
**WHEN** the operator builds a Single ticket from the boarding station, alighting station and passenger type
**THEN** the Single ticket is issued at the correct price
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104624 · NIR — Day Return (Child)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Child Day Return, Belfast Lanyon Place → Portadown, paid by cash
**WHEN** the operator builds a Day Return ticket
**THEN** the Day Return ticket is issued at the correct price
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104625 · NIR — 1/3 Off Day Return (Child)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Child 1/3 Off Day Return, Belfast Lanyon Place → Portadown, paid by cash
**WHEN** the operator builds a 1/3 Off Day Return ticket
**THEN** the ticket is issued with the 1/3 discount applied
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104626 · NIR — Weekly Season (Child, cash)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Child Weekly Season, Belfast Lanyon Place → Portadown, paid by cash
**WHEN** the operator builds a Weekly Season ticket
**THEN** the Weekly Season ticket is issued with the correct From/To dates
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104627 · NIR — Weekly Season (Adult, card)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult Weekly Season, Belfast Lanyon Place → Portadown, paid by card
**WHEN** the operator builds a Weekly Season ticket
**THEN** the Weekly Season ticket is issued with the correct From/To dates
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104628 · NIR — Weekly Season (Adult, warrant)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult Weekly Season, Belfast Lanyon Place → Portadown, paid by warrant
**WHEN** the operator builds a Weekly Season ticket
**THEN** the Weekly Season ticket is issued with the correct From/To dates
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104629 · NIR — Monthly Season (Child, cash)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-19299,FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Child Monthly Season, Belfast Lanyon Place → Portadown, paid by cash
**WHEN** the operator builds a Monthly Season ticket
**THEN** the Monthly Season ticket is issued with the correct From/To dates
**AND** the expiry (To) date is one calendar month from the start date
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104630 · NIR — Monthly Season (Adult, card)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-19299,FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult Monthly Season, Belfast Lanyon Place → Portadown, paid by card
**WHEN** the operator builds a Monthly Season ticket
**THEN** the Monthly Season ticket is issued with the correct From/To dates
**AND** the expiry (To) date is one calendar month from the start date
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104631 · NIR — Monthly Season (Adult, warrant)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-19299,FBD-100450,MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult Monthly Season, Belfast Lanyon Place → Portadown, paid by warrant
**WHEN** the operator builds a Monthly Season ticket
**THEN** the Monthly Season ticket is issued with the correct From/To dates
**AND** the expiry (To) date is one calendar month from the start date
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104632 · NIR — 3 Day Select (Child, cash)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: knowledge/projects/translink.md (Audit-confirmed POS facts — NIR-only ticket list),MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Child 3 Day Select, Belfast Lanyon Place → Portadown, paid by cash
**WHEN** the operator builds a 3 Day Select ticket
**AND** chooses the days
**THEN** the 3 Day Select ticket is issued for the chosen days
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104633 · NIR — 3 Day Select (Adult, card)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: knowledge/projects/translink.md (Audit-confirmed POS facts — NIR-only ticket list),MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult 3 Day Select, Belfast Lanyon Place → Portadown, paid by card
**WHEN** the operator builds a 3 Day Select ticket
**AND** chooses the days
**THEN** the 3 Day Select ticket is issued for the chosen days
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104634 · NIR — 3 Day Select (Adult, warrant)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: knowledge/projects/translink.md (Audit-confirmed POS facts — NIR-only ticket list),MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult 3 Day Select, Belfast Lanyon Place → Portadown, paid by warrant
**WHEN** the operator builds a 3 Day Select ticket
**AND** chooses the days
**THEN** the 3 Day Select ticket is issued for the chosen days
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104635 · NIR — Family & Friends Day (card)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Family & Friends Day, paid by card
**WHEN** the operator builds a Family & Friends Day ticket
**THEN** the Family & Friends Day ticket is issued
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104636 · NIR — Family & Friends Day (warrant)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Family & Friends Day, paid by warrant
**WHEN** the operator builds a Family & Friends Day ticket
**THEN** the Family & Friends Day ticket is issued
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104637 · NIR — iLink Single (Zone 1, Adult)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult iLink Single, iLink Zone 1, against a presented iLink smartcard, paid by cash
**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard
**THEN** the iLink Single is issued
**AND** it is recorded against the presented card
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104638 · NIR — iLink Single (Zone 2, Adult)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult iLink Single, iLink Zone 2, against a presented iLink smartcard, paid by cash
**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard
**THEN** the iLink Single is issued
**AND** it is recorded against the presented card
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104639 · NIR — iLink Single (Zone 3, Adult)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult iLink Single, iLink Zone 3, against a presented iLink smartcard, paid by cash
**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard
**THEN** the iLink Single is issued
**AND** it is recorded against the presented card
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104640 · NIR — iLink Single (NW Zone, Adult)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Adult iLink Single, iLink NW Zone, against a presented iLink smartcard, paid by cash
**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard
**THEN** the iLink Single is issued
**AND** it is recorded against the presented card
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104641 · NIR — iLink Single (Zone 4, Child)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: NIR Child iLink Single, iLink Zone 4, against a presented iLink smartcard, paid by cash
**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard
**THEN** the iLink Single is issued
**AND** it is recorded against the presented card
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104642 · NIR — Cross-Border Single (EUR, cash)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: Adult Cross-Border Single, Belfast Lanyon Place → Dublin Connolly, priced in EUR, paid by cash
**WHEN** the operator selects a Cross-Border Single
**THEN** the Cross-Border Single ticket is issued
**WHEN** the operator takes payment
**THEN** a green success banner is displayed

### C4104643 · NIR — Cross-Border Single (GBP, warrant)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: Adult Cross-Border Single, Belfast Lanyon Place → Dublin Connolly, priced in GBP, paid by warrant
**WHEN** the operator selects a Cross-Border Single
**THEN** the Cross-Border Single ticket is issued
**WHEN** the operator takes payment
**THEN** a green success banner is displayed

### C4104644 · NIR — Cross-Border Single (GBP, card)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: Adult Cross-Border Single, Belfast Lanyon Place → Dublin Connolly, priced in GBP, paid by card
**WHEN** the operator selects a Cross-Border Single
**THEN** the Cross-Border Single ticket is issued
**WHEN** the operator takes payment
**THEN** a green success banner is displayed

### C4104645 · NIR — Cross-Border Day Return (EUR, cash)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: Adult Cross-Border Day Return, Belfast Lanyon Place → Dublin Connolly, priced in EUR, paid by cash
**WHEN** the operator selects a Cross-Border Day Return
**THEN** the Cross-Border Day Return ticket is issued
**WHEN** the operator takes payment
**THEN** a green success banner is displayed

### C4104646 · NIR — Cross-Border Day Return (GBP, warrant)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: Adult Cross-Border Day Return, Belfast Lanyon Place → Dublin Connolly, priced in GBP, paid by warrant
**WHEN** the operator selects a Cross-Border Day Return
**THEN** the Cross-Border Day Return ticket is issued
**WHEN** the operator takes payment
**THEN** a green success banner is displayed

### C4104647 · NIR — Cross-Border Day Return (GBP, card)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-NIR-ONLY
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**AND** the POS is communicating with CloudFare
**AND** example: Adult Cross-Border Day Return, Belfast Lanyon Place → Dublin Connolly, priced in GBP, paid by card
**WHEN** the operator selects a Cross-Border Day Return
**THEN** the Cross-Border Day Return ticket is issued
**WHEN** the operator takes payment
**THEN** a green success banner is displayed

### C4100362 · Comms — loss enters Communication Locked  (4m)  — cross-check: CloudFare; refs: TIBU-28530,TIBU-27664,MODE-PRIMARY-ONLY
_Non-Functional / Comms (CloudFare)_

**GIVEN** the device is operating normally
**WHEN** CloudFare communication is lost beyond the configured period
**THEN** the device enters Communication Locked
**AND** it does not enter Communication Locked while comms are healthy

### C4100363 · Comms — recovery reconnects and syncs  (4m)  — cross-check: CloudFare; refs: REQ-2589.0,MODE-PRIMARY-ONLY
_Non-Functional / Comms (CloudFare)_

**GIVEN** the device has lost CloudFare communication
**WHEN** communication is restored
**THEN** the device reconnects to CloudFare
**AND** outstanding transactions are synced

### C4100364 · Comms — token loss does not force Out Of Service  (4m)  — **DESTRUCTIVE**; cross-check: CloudFare; refs: TIBU-21277,MODE-PRIMARY-ONLY
_Non-Functional / Comms (CloudFare)_

**GIVEN** the device is signed on and communicating
**WHEN** the authentication token is lost
**THEN** the device re-authenticates
**AND** the device does not go Out Of Service unexpectedly
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100365 · Comms — card-reader failures do not flood CloudFare  (4m)  — PARTIAL; cross-check: CloudFare; refs: TIBU-16106,MODE-PRIMARY-ONLY
_Non-Functional / Comms (CloudFare)_

**GIVEN** the card reader is experiencing failures
**WHEN** the failures occur repeatedly
**THEN** the failures are reported to CloudFare at a sensible rate
**AND** CloudFare is not flooded with duplicate messages

### C4100366 · Comms — device status and Tray ID reported correctly  (4m)  — cross-check: CloudFare; refs: TIBU-24888,TIBU-24889,TIBU-25071,MODE-PRIMARY-ONLY
_Non-Functional / Comms (CloudFare)_

**GIVEN** the device is communicating with CloudFare
**WHEN** the device reports its status
**THEN** the device status is accurate
**AND** the Tray ID is reported correctly
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100358 · Printer — paper jam detected and recoverable  (5m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-19311,TIBU-20980,TIBU-26723,MODE-PRIMARY-ONLY
_Non-Functional / Printer_

**GIVEN** the operator completes a transaction that prints
**WHEN** the printer experiences a paper jam
**THEN** the Paper Jam screen is shown
**AND** the Annul Transaction control responds
**WHEN** the jam is cleared
**THEN** the device returns to normal operation

### C4100359 · Printer — out of paper is handled  (2m)  — PARTIAL; refs: knowledge/flows/flow-annotations.md §15.0 Printer Errors,MODE-PRIMARY-ONLY
_Non-Functional / Printer_

**GIVEN** the operator attempts to print
**WHEN** the printer is out of paper
**THEN** the device reports the out-of-paper condition
**WHEN** paper is replaced
**THEN** printing resumes normally

### C4100367 · Smoke — operator sign on  (6m)  — cross-check: CloudFare; refs: MODE-ALL
_Smoke_

**GIVEN** the device is at the Idle screen and communicating with CloudFare
**WHEN** the operator signs on with valid credentials
**THEN** the operator reaches the Main Screen

### C4100368 · Smoke — sell a ticket (cash)  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-ALL
_Smoke_

**GIVEN** an operator is signed on
**WHEN** the operator builds a fare, adds it to the basket and takes cash payment
**THEN** the ticket is issued
**AND** a receipt is printed

### C4100369 · Smoke — top up a smartcard  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-ALL
_Smoke_

**GIVEN** an operator is signed on
**WHEN** the operator presents a smartcard, tops it up and takes payment
**THEN** the top up is applied to the card
**AND** a receipt is printed

### C4100370 · Smoke — sign off  (4m)  — cross-check: CloudFare; refs: MODE-ALL
_Smoke_

**GIVEN** an operator is signed on
**WHEN** the operator signs off
**THEN** the device returns to the Idle screen

### C4100374 · Bus FLU — sell a ticket  (7m)  — cross-check: CloudFare / MERIT; refs: TIBU-19459,TIBU-19460,FBD-100207,MODE-ULSTERBUS-ONLY
_Ulsterbus / Fare Look-Up_

**GIVEN** an operator is signed on with the POS in Ulsterbus mode on the Main Screen
**AND** the POS is communicating with CloudFare
**AND** example: route 72b, Moygashel Busby Shop → Armagh Bus Centre, Adult Single
**WHEN** the operator enters a route number, sets the boarding and alighting stages and selects a fare type
**THEN** the fare and price are shown
**AND** the Fare Stage name is shown rather than the stop name
**WHEN** the operator adds the product to the basket and purchases it
**THEN** the product is added to the basket
**AND** the product can be purchased
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100375 · Bus FLU — route number letters via the '*' key  (1m)  — refs: TIBU-19458,MODE-ULSTERBUS-ONLY
_Ulsterbus / Fare Look-Up_

**GIVEN** an operator is signed on and is entering a route number on the Main Screen (Ulsterbus mode)
**AND** example: entering route 72 then pressing '*' to reach the 'b' of route 72b
**WHEN** the operator presses the '*' key during route-number entry
**THEN** the route-number letter options are shown

### C4100376 · Bus FLU — change boarding stage, alighting stage and fare type  (3m)  — refs: MODE-ULSTERBUS-ONLY
_Ulsterbus / Fare Look-Up_

**GIVEN** an operator is signed on and building a bus fare (Ulsterbus mode)
**AND** example: route 72b starting Moygashel Busby Shop → Armagh Bus Centre, Adult Single, then re-pointed to a different boarding/alighting stage and Child fare (fares confirm against the fares export)
**WHEN** the operator changes the boarding stage
**THEN** the fare updates for the new boarding stage
**WHEN** the operator changes the alighting stage
**THEN** the fare updates for the new alighting stage
**WHEN** the operator changes the fare type
**THEN** the fare updates for the new fare type

### C4100377 · Bus FLU — Misc open fare  (7m)  — cross-check: CloudFare / MERIT; refs: MODE-ULSTERBUS-ONLY
_Ulsterbus / Fare Look-Up_

**GIVEN** an operator is signed on and has selected a Misc product (open fare) (Ulsterbus mode)
**AND** the POS is communicating with CloudFare
**AND** example: entering a valid open-fare amount on route 72b, then an invalid amount
**WHEN** the operator enters a valid open-fare amount
**THEN** the open fare is accepted
**AND** the open fare is added to the basket
**WHEN** the operator enters an invalid amount
**THEN** the amount is rejected with an error
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100378 · Bus FLU — Default Boarding Stage '*' key  (1m)  — refs: TIBU-24026,MODE-ULSTERBUS-ONLY
_Ulsterbus / Fare Look-Up_

**GIVEN** an operator is signed on and is on the Default Boarding Stage entry (Ulsterbus mode)
**AND** example: pressing '*' on the Default Boarding Stage entry for route 72b
**WHEN** the operator presses the '*' button
**THEN** no dead key or error occurs
**AND** **GAP** — the specific resulting behaviour is not documented in any sourced FBD, only known as 'not a dead key' via TIBU-24026; confirm the actual on-screen effect before running

### C4100403 · Ulsterbus — Single (Adult, cash)  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Adult Single, 72b (IN) Moygashel Busby Shop → Armagh Bus Centre, paid by cash
**WHEN** the operator builds a Single ticket from the route, boarding and alighting stages and passenger type
**THEN** the Single ticket is issued at the correct price
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100404 · Ulsterbus — Day Return (Adult)  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Adult Day Return, 72b (IN) Moygashel Busby Shop → Armagh Bus Centre, paid by cash
**WHEN** the operator builds a Day Return ticket
**THEN** the Day Return ticket is issued at the correct price
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100405 · Ulsterbus — Month Return (Adult)  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: knowledge/projects/translink.md (Audit-confirmed POS facts — Ulsterbus-only ticket list),MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Adult Month Return, 72b (IN) Moygashel Busby Shop → Armagh Bus Centre, paid by cash
**WHEN** the operator builds a Month Return ticket
**THEN** the Month Return ticket is issued with the correct validity dates
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100406 · Ulsterbus — Warrant Return  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Adult Warrant Return, 72b (IN) Moygashel Busby Shop → Armagh Bus Centre, paid by warrant
**WHEN** the operator builds a Warrant Return
**THEN** the Warrant Return ticket is issued
**WHEN** the operator completes the warrant payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100407 · Ulsterbus — Bus Rambler (Adult, cash)  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: knowledge/projects/translink.md (Audit-confirmed POS facts — Ulsterbus-only ticket list),MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Adult Bus Rambler, paid by cash
**WHEN** the operator builds a Bus Rambler ticket
**THEN** the Bus Rambler ticket is issued
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100408 · Ulsterbus — Family & Friends Day (cash)  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Family & Friends Day, paid by cash
**WHEN** the operator builds a Family & Friends Day ticket
**THEN** the Family & Friends Day ticket is issued
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100409 · Ulsterbus — Jobseeker Single  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: knowledge/projects/translink.md (Audit-confirmed POS facts — Ulsterbus-only ticket list),MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Jobseeker Single, 72b (IN) Moygashel Busby Shop → Armagh Bus Centre, paid by cash
**WHEN** the operator builds a Jobseeker Single ticket
**THEN** the Jobseeker Single ticket is issued at the correct concession price
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100410 · Ulsterbus — iLink Single (Zone 4, Adult)  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Adult iLink Single, iLink Zone 4, against a presented iLink smartcard, paid by cash
**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard
**THEN** the iLink Single is issued
**AND** it is recorded against the presented card
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100411 · Rail Substitution Service  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: FBD-100335 para 126,FBD-100335 para 149,MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode running a rail substitution service
**AND** the POS is communicating with CloudFare
**AND** example: Larne Line rail-substitution route, Adult single, paid by cash
**WHEN** the operator processes a Rail Substitution Service fare
**THEN** the fare is issued under the rail substitution service
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104650 · Ulsterbus — Single (Child, cash)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Child Single, 72b (IN) Moygashel Busby Shop → Armagh Bus Centre, paid by cash
**WHEN** the operator builds a Single ticket from the route, boarding and alighting stages and passenger type
**THEN** the Single ticket is issued at the correct price
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104651 · Ulsterbus — Single (Adult, card)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Adult Single, 72b (IN) Moygashel Busby Shop → Armagh Bus Centre, paid by card
**WHEN** the operator builds a Single ticket from the route, boarding and alighting stages and passenger type
**THEN** the Single ticket is issued at the correct price
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104652 · Ulsterbus — Single (Adult, warrant)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Adult Single, 72b (IN) Moygashel Busby Shop → Armagh Bus Centre, paid by warrant
**WHEN** the operator builds a Single ticket from the route, boarding and alighting stages and passenger type
**THEN** the Single ticket is issued at the correct price
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104653 · Ulsterbus — Day Return (Child)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Child Day Return, 72b (IN) Moygashel Busby Shop → Armagh Bus Centre, paid by cash
**WHEN** the operator builds a Day Return ticket
**THEN** the Day Return ticket is issued at the correct price
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104654 · Ulsterbus — Month Return (Child)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: knowledge/projects/translink.md (Audit-confirmed POS facts — Ulsterbus-only ticket list),MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Child Month Return, 72b (IN) Moygashel Busby Shop → Armagh Bus Centre, paid by cash
**WHEN** the operator builds a Month Return ticket
**THEN** the Month Return ticket is issued with the correct validity dates
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104655 · Ulsterbus — Bus Rambler (Child, cash)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: knowledge/projects/translink.md (Audit-confirmed POS facts — Ulsterbus-only ticket list),MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Child Bus Rambler, paid by cash
**WHEN** the operator builds a Bus Rambler ticket
**THEN** the Bus Rambler ticket is issued
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104656 · Ulsterbus — Bus Rambler (Adult, card)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: knowledge/projects/translink.md (Audit-confirmed POS facts — Ulsterbus-only ticket list),MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Adult Bus Rambler, paid by card
**WHEN** the operator builds a Bus Rambler ticket
**THEN** the Bus Rambler ticket is issued
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104657 · Ulsterbus — Bus Rambler (Adult, warrant)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: knowledge/projects/translink.md (Audit-confirmed POS facts — Ulsterbus-only ticket list),MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Adult Bus Rambler, paid by warrant
**WHEN** the operator builds a Bus Rambler ticket
**THEN** the Bus Rambler ticket is issued
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104658 · Ulsterbus — Family & Friends Day (card)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Family & Friends Day, paid by card
**WHEN** the operator builds a Family & Friends Day ticket
**THEN** the Family & Friends Day ticket is issued
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104659 · Ulsterbus — Family & Friends Day (warrant)  (?)  — PARTIAL; cross-check: CloudFare / MERIT; refs: MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Family & Friends Day, paid by warrant
**WHEN** the operator builds a Family & Friends Day ticket
**THEN** the Family & Friends Day ticket is issued
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104660 · Ulsterbus — iLink Single (Zone 1, Adult)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Adult iLink Single, iLink Zone 1, against a presented iLink smartcard, paid by cash
**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard
**THEN** the iLink Single is issued
**AND** it is recorded against the presented card
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104661 · Ulsterbus — iLink Single (Zone 2, Adult)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Adult iLink Single, iLink Zone 2, against a presented iLink smartcard, paid by cash
**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard
**THEN** the iLink Single is issued
**AND** it is recorded against the presented card
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104662 · Ulsterbus — iLink Single (Zone 3, Adult)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Adult iLink Single, iLink Zone 3, against a presented iLink smartcard, paid by cash
**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard
**THEN** the iLink Single is issued
**AND** it is recorded against the presented card
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104664 · Ulsterbus — iLink Single (NW Zone, Adult)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Adult iLink Single, iLink NW Zone, against a presented iLink smartcard, paid by cash
**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard
**THEN** the iLink Single is issued
**AND** it is recorded against the presented card
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4104666 · Ulsterbus — iLink Single (Zone 4, Child)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: MODE-ULSTERBUS-ONLY
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Child iLink Single, iLink Zone 4, against a presented iLink smartcard, paid by cash
**WHEN** the operator sells an iLink Single fare against the presented iLink smartcard
**THEN** the iLink Single is issued
**AND** it is recorded against the presented card
**WHEN** the operator takes payment
**THEN** a receipt is printed
**AND** a green success banner is displayed

### C4100392 · Top Up — Ulsterbus Multi-Journey (Cash)  (11m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-26861,TIBU-21133,MODE-ULSTERBUS-ONLY
_Ulsterbus / Top Up_

**GIVEN** an operator is signed on to the POS in Ulsterbus mode
**AND** an Ulsterbus Multi-Journey smartcard is presented
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Multi-Journey, select the card's reference number, add 10 journeys, paid by Cash
**WHEN** the operator selects the card reference and journeys and takes payment
**THEN** the journeys are added to the card
**AND** the added journeys are shown
**AND** the card cannot exceed its maximum permitted journeys
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4104648 · Top Up — Ulsterbus Multi-Journey (Warrant)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-26861,TIBU-21133,MODE-ULSTERBUS-ONLY
_Ulsterbus / Top Up_

**GIVEN** an operator is signed on to the POS in Ulsterbus mode
**AND** an Ulsterbus Multi-Journey smartcard is presented
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Multi-Journey, select the card's reference number, add 10 journeys, paid by Warrant
**WHEN** the operator selects the card reference and journeys and takes payment
**THEN** the journeys are added to the card
**AND** the added journeys are shown
**AND** the card cannot exceed its maximum permitted journeys
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4104649 · Top Up — Ulsterbus Multi-Journey (Card)  (?)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-26861,TIBU-21133,MODE-ULSTERBUS-ONLY
_Ulsterbus / Top Up_

**GIVEN** an operator is signed on to the POS in Ulsterbus mode
**AND** an Ulsterbus Multi-Journey smartcard is presented
**AND** the POS is communicating with CloudFare
**AND** example: Ulsterbus Multi-Journey, select the card's reference number, add 10 journeys, paid by Card
**WHEN** the operator selects the card reference and journeys and takes payment
**THEN** the journeys are added to the card
**AND** the added journeys are shown
**AND** the card cannot exceed its maximum permitted journeys
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack


## Priority: Normal

### C4100006 · Numerical Input — keypad entry  (2m)  — refs: TIBU-21771,MODE-PRIMARY-ONLY
_Functional / Numerical Input_

**GIVEN** the POS is signed on as an Operator on a screen requiring numeric entry, e.g. the rail station-number field
**WHEN** the operator keys in digits
**THEN** the entered value reflects the key presses
**WHEN** the operator presses the C key
**THEN** one character is cleared per key press

### C4099948 · Supervisor — Day Information  (2m)  — PARTIAL; refs: TIBU-24785,TIBU-22647,MODE-PRIMARY-ONLY
_Functional / Supervisor / Reports & Information_

**GIVEN** a supervisor is signed on to the POS
**AND** the POS has paper loaded ready to print
**AND** example: a day with two operator shifts on this POS, viewed then printed
**WHEN** the supervisor opens Day Information
**THEN** the Day Information is displayed
**AND** the chevron-key instructions are shown
**WHEN** the supervisor prints it
**THEN** the printout shows the correct number of shifts

### C4099949 · Supervisor — Sales Breakdown  (2m)  — PARTIAL; refs: TIBU-19682,TIBU-23936,MODE-PRIMARY-ONLY
_Functional / Supervisor / Reports & Information_

**GIVEN** a supervisor is signed on to the POS
**AND** the POS has paper loaded and sales recorded this shift
**AND** example: the supervisor opens Sales Breakdown and prints it to check the day's figures
**WHEN** the supervisor opens Sales Breakdown
**THEN** the Sales Breakdown is displayed
**WHEN** the supervisor prints the Sales Breakdown
**THEN** the Sales Breakdown is printed
**AND** the printout shows the correct sales information
**AND** the printout does not include stray 'Paper' content

### C4099961 · Technician — menu options  (1m)  — refs: TIBU-22649,MODE-PRIMARY-ONLY
_Functional / Technician / Maintenance_

**GIVEN** a technician is signed on to the POS
**AND** example: the technician views the Technician menu to confirm the listed entries
**WHEN** the technician views the Technician menu
**THEN** only the intended options are listed

### C4100437 · Printer — paper low notification  (1m)  — PARTIAL; refs: TIBU-26995,knowledge/flows/flow-annotations.md §15.0 Printer Errors,MODE-PRIMARY-ONLY
_Non-Functional / Printer_

**GIVEN** the printer paper level is low
**WHEN** the operator is using the POS
**THEN** a temporary paper-low notification is shown (about 3 seconds)

### C4100438 · Printer — print-failure events are sent  (1m)  — PARTIAL; refs: knowledge/flows/flow-annotations.md §15.0 Printer Errors,MODE-PRIMARY-ONLY
_Non-Functional / Printer_

**GIVEN** the printer encounters a fault (no paper, hardware/software error, or power loss mid-print)
**WHEN** a print fails, partially prints due to power loss, or resumes after power loss
**THEN** the POS sends the corresponding event
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log


## Priority: Low

### C4099969 · Administrator — Versions  (4m)  — PARTIAL; cross-check: CloudFare; refs: MODE-PRIMARY-ONLY
_Functional / Administrator / Device & Network_

**GIVEN** an administrator is signed on to the POS
**AND** the POS has paper loaded ready to print
**AND** example: the administrator opens Versions to confirm the deployed software and config versions
**WHEN** the administrator views and prints the serial, software and configuration versions
**THEN** each version set is displayed
**AND** each version set is printed

### C4099947 · Supervisor — Duty Information  (2m)  — refs: TIBU-21110,TIBU-21138,TIBU-21323,TIBU-21325,TIBU-27443,TIBU-21367,TIBU-22643,MODE-PRIMARY-ONLY
_Functional / Supervisor / Reports & Information_

**GIVEN** a supervisor is signed on to the POS
**AND** there are recorded duties for the day to display
**AND** example: the supervisor opens Duty Information and uses the chevron keys to step through each duty
**WHEN** the supervisor opens Duty Information
**THEN** the Duty Information is displayed
**AND** the headings, text and chevron-key instructions are correct
**AND** the POS does not reset
**WHEN** the supervisor selects a duty and scrolls with the chevron keys
**THEN** each individual duty's details can be viewed

### C4099958 · Technician — Versions  (4m)  — PARTIAL; cross-check: CloudFare; refs: TIBU-15782,MODE-PRIMARY-ONLY
_Functional / Technician / Maintenance_

**GIVEN** a technician is signed on to the POS
**AND** the POS has paper loaded ready to print
**AND** example: the technician opens Versions to confirm the deployed software version
**WHEN** the technician views and prints the serial, software and configuration versions
**THEN** each version set is displayed with the real version numbers
**AND** each version set can be printed

