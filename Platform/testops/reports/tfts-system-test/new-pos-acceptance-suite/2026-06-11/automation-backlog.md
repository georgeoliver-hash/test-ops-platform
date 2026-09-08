# Automation backlog — **NEW** POS-Acceptance Suite (POS)

_Generated 2026-06-11T12:01:22+00:00 by system-test-ops. Suite id 30253, project TFTS - System Test._

**51 fully automatable + 118 partial** of 498 cases (5 destructive, 329 manual-only). _Partial = the UI flow is automatable but a step (card tap / print / cash) needs a hardware fixture or human eye._

## How to consume

- Reference `ref` (TestRail case id, e.g. C4099911) in each automated test so a result maps back to its case.
- Mirror device + feature as pytest markers; add @pytest.mark.destructive where destructive is true (deselected by default).
- cross_check lists the back-office systems the case asserts — the test must verify the event landed there (CloudFare / MERIT / SmartTrack).
- automatable/priority are system-test-ops judgements and a starting point; the automation engineer may override with rationale.


## Priority: High

### C4099963 · Administrator — Clear Card  (2m)  — PARTIAL
_Functional / Administrator / Card Management_

**GIVEN** an administrator is signed on
**WHEN** the administrator clears a valid card
**THEN** the card is cleared
**AND** success is reported
**WHEN** the administrator attempts to clear an invalid card
**THEN** the operation is reported as unsuccessful with a card error

### C4099964 · Administrator — Card Dump  (2m)  — PARTIAL
_Functional / Administrator / Card Management_

**GIVEN** an administrator is signed on
**WHEN** the administrator dumps a valid card
**THEN** the card data is read
**AND** success is reported
**WHEN** the administrator attempts to dump an invalid card
**THEN** the operation is reported as unsuccessful

### C4099965 · Administrator — Data Download  (1m)  — PARTIAL
_Functional / Administrator / Card Management_

**GIVEN** an administrator is signed on
**WHEN** the administrator performs a Data Download
**THEN** the data is downloaded
**AND** a 'Data Download Successful' confirmation is shown

### C4099966 · Administrator — Device Settings  (1m)  — refs: TIBU-22632
_Functional / Administrator / Device & Network_

**GIVEN** an administrator is signed on
**WHEN** the administrator changes the Home Location, Boarding Location, Mounting Point and Tray Identifier
**THEN** each setting is updated
**AND** each setting is retained
**AND** the default Boarding Stage and Mounting Point are correct

### C4099967 · Administrator — Network Settings  (1m)  — refs: TIBU-24740
_Functional / Administrator / Device & Network_

**GIVEN** an administrator is signed on
**WHEN** the administrator opens Network Settings and changes a setting
**THEN** the screen responds to the input
**AND** the change is applied

### C4099968 · Administrator — Force Comms  (4m)  — cross-check: CloudFare
_Functional / Administrator / Device & Network_

**GIVEN** an administrator is signed on
**WHEN** the administrator initiates, refreshes and exits Force Comms
**THEN** each action completes
**AND** the administrator returns to the Administrator menu

### C4099969 · Administrator — Versions  (4m)  — PARTIAL; cross-check: CloudFare
_Functional / Administrator / Device & Network_

**GIVEN** an administrator is signed on
**WHEN** the administrator views and prints the serial, software and configuration versions
**THEN** each version set is displayed
**AND** each version set is printed

### C4100439 · Barcode — validate a ticket by barcode  (1m)  — PARTIAL
_Functional / Barcode Scanning_

**GIVEN** the operator accesses Barcode Reference via the Operator Menu
**WHEN** the operator scans a ticket barcode
**THEN** the ticket validation screen shows the information for that barcode type
**AND** any Notes on that barcode type are shown
**AND** pressing any key (or a 3s timeout) returns to the FLU screen

### C4100440 · Barcode — offline validations stored until reconnect  (5m)  — PARTIAL; cross-check: CloudFare
_Functional / Barcode Scanning_

**GIVEN** the POS is offline (no CloudFare/Corethree connection)
**WHEN** the operator validates barcodes
**THEN** the offline validations are stored in a list
**WHEN** connection to CloudFare/Corethree is re-established
**THEN** the stored validations are synced

### C4099996 · Annulment — annul last transaction  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-19352,TIBU-24878
_Functional / Basket & Payment / Annulment_

**GIVEN** the operator has issued a ticket this shift
**WHEN** the operator annuls the last transaction
**THEN** the transaction is annulled
**AND** when there is nothing to annul the 'No ticket to Annul' option is greyed out

### C4099997 · Annulment — newly issued smartcard  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-24334,TIBU-23949,TIBU-26760
_Functional / Basket & Payment / Annulment_

**GIVEN** the operator has just issued a new smartcard
**WHEN** the operator annuls that smartcard issue
**THEN** the issue is annulled successfully
**AND** the annulment is recorded
**AND** its receipt prints

### C4099998 · Annulment — multi-journey top-up  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-25072,TIBU-25100
_Functional / Basket & Payment / Annulment_

**GIVEN** the operator has topped up a multi-journey smartcard
**WHEN** the operator annuls the top-up
**THEN** the top-up is annulled
**AND** the journeys on the card are corrected

### C4099999 · Annulment — receipt content  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-23932,TIBU-25888,TIBU-25889,TIBU-25402,TIBU-25404,TIBU-25800,TIBU-25116
_Functional / Basket & Payment / Annulment_

**GIVEN** the operator has annulled a transaction
**WHEN** the annulment receipt prints
**THEN** it shows the correct title, card type and journey/cancellation information
**AND** the card type text is not cut short
**AND** the Tray ID is present

### C4100000 · Annulment — during paper jam  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-19311,TIBU-20980
_Functional / Basket & Payment / Annulment_

**GIVEN** the printer is in a paper-jam state after a transaction
**WHEN** the operator presses Annul Transaction on the Paper Jam screen
**THEN** the annul control responds
**AND** the transaction is annulled

### C4100386 · Annulment — Belfast Visitor Pass  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-21443
_Functional / Basket & Payment / Annulment_

**GIVEN** the operator has just issued an Adult Belfast Visitors Pass
**WHEN** the operator annuls the issue
**THEN** the Belfast Visitors Pass issue is annulled successfully

### C4100387 · Annulment — re-present different card  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-25073
_Functional / Basket & Payment / Annulment_

**GIVEN** the operator is annulling the last transaction
**WHEN** a different card is presented during the annul flow
**THEN** the mismatch is handled gracefully
**AND** the device is not left stuck

### C4100505 · Annulment — ticket issue  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Basket & Payment / Annulment_

**GIVEN** the operator has just issued a ticket this shift
**WHEN** the operator annuls that ticket issue
**THEN** the ticket issue is annulled
**AND** the annulment is recorded
**AND** an annulment receipt is printed

### C4099989 · Basket — add & review  (3m)  — PARTIAL; refs: TIBU-21777,TIBU-24364
_Functional / Basket & Payment / Basket_

**GIVEN** an operator is signed on and has built one or more fares
**WHEN** the operator adds them to the basket and opens the basket
**THEN** the basket lists the items with the correct total
**AND** the expected basket buttons are present

### C4099990 · Basket — clear basket  (3m)  — PARTIAL; refs: TIBU-24368
_Functional / Basket & Payment / Basket_

**GIVEN** the basket contains one or more items
**WHEN** the operator presses Clear Basket
**THEN** the basket is emptied

### C4099991 · Basket — checkout total  (3m)  — PARTIAL; refs: TIBU-24098,TIBU-24860
_Functional / Basket & Payment / Basket_

**GIVEN** the basket contains multiple items
**WHEN** the operator proceeds to checkout
**THEN** the checkout total equals the sum of the items
**AND** 'add more to basket' is unavailable when the basket cannot accept more

### C4100432 · Basket — maximum of 9 tickets  (4m)  — PARTIAL; **DESTRUCTIVE**
_Functional / Basket & Payment / Basket_

**GIVEN** the operator is adding tickets to the basket
**WHEN** the basket reaches 9 tickets
**THEN** the Add More button becomes unavailable
**WHEN** the operator deletes a ticket from the basket
**THEN** the Add More button becomes available again

### C4100433 · Basket — entitlement passes cannot be basketed  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Basket & Payment / Basket_

**GIVEN** the operator has built a fare using a smartcard entitlement pass
**WHEN** the operator attempts to add it to the basket
**THEN** the fare cannot be basketed
**AND** it must be validated and paid as an individual transaction

### C4100434 · Basket — bus basket is single-route  (4m)  — PARTIAL
_Functional / Basket & Payment / Basket_

**GIVEN** an operator is building a bus basket on a route
**WHEN** the operator tries to add a ticket from a different route
**THEN** it is not allowed
**WHEN** the operator adds tickets with two different boarding stages on the same route
**THEN** both are accepted

### C4099994 · Card Payment — pay by card  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-24777,TIBU-24834
_Functional / Basket & Payment / Card Payment_

**GIVEN** a payment card device (PCD) is attached and the POS is in NIR or Ulsterbus mode
**AND** the basket/fare is ready for payment
**WHEN** the operator selects Bank Card and the customer pays by contactless, chip & PIN, or swipe
**THEN** the payment terminal authorises the transaction
**AND** the ticket is printed as soon as the transaction succeeds
**AND** the customer is offered an optional payment receipt
**AND** the POS returns to the Bus/Rail FLU screen

### C4099995 · Card Payment — back from payment  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-24876
_Functional / Basket & Payment / Card Payment_

**GIVEN** the operator is on the payment screen for a single ticket
**WHEN** the operator presses Back
**THEN** the operator is returned to the basket/fare with its state intact

### C4100424 · Card Payment — declined, cancelled or error  (8m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Basket & Payment / Card Payment_

**GIVEN** the customer is paying by bank card
**WHEN** the card is declined
**THEN** a declined message is shown
**AND** a declined receipt is printed
**WHEN** the customer cancels on the PIN pad before entering the PIN
**THEN** the transaction is cancelled with no cancelled-payment receipt
**WHEN** the PIN is entered incorrectly too many times, or the amount is too big for a card, or the signature does not match
**THEN** the matching error message (driven by the M020/PCD) is shown
**AND** the POS returns to the payment screen

### C4099992 · Cash — pay a basket  (7m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-19336,TIBU-7379
_Functional / Basket & Payment / Cash Payment_

**GIVEN** the basket has one or more items
**WHEN** the operator takes cash payment and completes the transaction
**THEN** the transaction completes
**AND** the basket is issued
**WHEN** the operator builds and cash-pays a further basket on a different route
**THEN** that transaction also completes without the device freezing

### C4099993 · Cash — EOS total net  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-29484,TIBU-30634
_Functional / Basket & Payment / Cash Payment_

**GIVEN** an operator has taken cash sales and at least one annulment during the shift
**WHEN** the End of Shift cash total is produced
**THEN** the total is the net amount, accounting for annulments

### C4100001 · Receipts — printed per transaction  (3m)  — PARTIAL; refs: TIBU-21135,TIBU-21176,TIBU-23016,TIBU-21266
_Functional / Basket & Payment / Receipts & Printing_

**GIVEN** an operator completes an issuing transaction (ticket, card issue or top-up)
**WHEN** the transaction completes
**THEN** a receipt is printed

### C4100002 · Receipts — no duplicates  (3m)  — PARTIAL; refs: TIBU-22548,TIBU-22557
_Functional / Basket & Payment / Receipts & Printing_

**GIVEN** an operator completes a transaction that prints a receipt
**WHEN** the receipt prints
**THEN** exactly one receipt is produced

### C4100003 · Receipts — template & fonts  (3m)  — PARTIAL; refs: TIBU-23835,TIBU-24890,TIBU-23096,TIBU-16109,TIBU-24848
_Functional / Basket & Payment / Receipts & Printing_

**GIVEN** an operator prints a ticket/receipt
**WHEN** the printout is produced
**THEN** it uses the correct template, fonts and current Translink logo
**AND** rail ticket templates follow the revised naming
**AND** a missing template is handled gracefully with no crash

### C4100004 · Receipts — mini statement  (3m)  — PARTIAL; refs: TIBU-20759,TIBU-21581,TIBU-23989,TIBU-21178,TIBU-21463
_Functional / Basket & Payment / Receipts & Printing_

**GIVEN** the operator prints a mini statement for a smartcard
**WHEN** the mini statement prints
**THEN** it shows the correct information including the actual expiry date
**AND** the printout is long enough to contain all content
**AND** an expired multi-journey card still prints its receipt

### C4100005 · Receipts — day summary  (3m)  — PARTIAL; refs: TIBU-24800
_Functional / Basket & Payment / Receipts & Printing_

**GIVEN** card transactions have occurred during the day
**WHEN** the operator prints the day summary
**THEN** the printout includes the card transaction details

### C4100033 · Customer Display — passenger display  (3m)  — PARTIAL; refs: TIBU-24845
_Functional / Customer Displays_

**GIVEN** an operator is building and paying for a fare
**WHEN** the operator adds items and takes payment
**THEN** the passenger display shows the fare and running total
**AND** the passenger display updates as the transaction progresses

### C4100499 · Customer Display — Rail passenger display  (3m)  — PARTIAL
_Functional / Customer Displays_

**GIVEN** an operator is signed on in Rail (NIR) mode and building a fare
**WHEN** the operator adds items and takes payment
**THEN** the passenger display shows the rail fare and running total
**AND** the passenger display updates as the transaction progresses

### C4100500 · Customer Display — Ulsterbus passenger display  (3m)  — PARTIAL
_Functional / Customer Displays_

**GIVEN** an operator is signed on in Ulsterbus mode and building a fare
**WHEN** the operator adds items and takes payment
**THEN** the passenger display shows the Ulsterbus fare and running total
**AND** the passenger display updates as the transaction progresses

### C4099987 · FLU — passenger type  (1m)
_Functional / Fare Look-Up / Common_

**GIVEN** the operator is building a fare
**WHEN** the operator selects a passenger type
**THEN** the passenger type is applied
**AND** the price updates

### C4099988 · FLU — cash limit  (4m)  — PARTIAL; **DESTRUCTIVE**; cross-check: CloudFare / MERIT
_Functional / Fare Look-Up / Common_

**GIVEN** the operator is building a fare
**WHEN** the basket total exceeds the configured cash limit
**THEN** the Cash Limit error is shown

### C4100024 · Issue Card — issue from blank  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-26845,TIBU-21266,TIBU-26760,TIBU-21208,TIBU-24715,TIBU-25890
_Functional / Issue Card / Issue from Blank_

**Given** an operator is signed on and a blank smartcard is presented
**WHEN** the operator selects the product, takes payment and issues it to the card
**THEN** the product is written to the card at the correct price
**AND** a receipt is printed

### C4100031 · Issue Card — recognised by other devices  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-21446,TIBU-22603,TIBU-23996,TIBU-26721,TIBU-26722
_Functional / Issue Card / Issue from Blank_

**GIVEN** the operator has created a new card from blank on the POS
**WHEN** the card is presented to another device (ETM/TVM) and back to the POS for top-up
**THEN** the card is recognised as valid
**AND** it can be topped up

### C4100390 · Issue Card — blank card options  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-23963
_Functional / Issue Card / Issue from Blank_

**GIVEN** the operator places an Adult BVP or iLink Zone 1 'blank' card on the POS
**WHEN** the operator selects the Adult Belfast Visitors option
**THEN** the correct Belfast Visitors options are offered
**AND** the iLink Zone card options are not shown

### C4100430 · Numerical Input — group ticket  (7m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Numerical Input_

**GIVEN** the operator has selected a group-eligible product with boarding/alighting set
**WHEN** the operator enters a passenger count (or uses + / -) up to 100 and confirms
**THEN** a single group ticket is printed
**AND** one back-office transaction is recorded with a sub-element per passenger
**WHEN** the operator selects a non-group-eligible product or an invalid count
**THEN** an error banner is shown

### C4100431 · Numerical Input — calculate change  (7m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Numerical Input_

**GIVEN** the operator is taking a cash payment
**WHEN** the operator enters the amount tendered and selects Calculate Change
**THEN** the change is calculated
**AND** the change is shown
**WHEN** too many digits are entered, or the amount is less than the ticket value, or the previous transaction had no value
**THEN** the Calculate Change option is unavailable

### C4099936 · Operator Options — correct options listed  (3m)  — PARTIAL; refs: TIBU-22640
_Functional / Operator / Options_

**GIVEN** an operator is signed on
**WHEN** the operator opens Operator Options
**THEN** the expected operator options are listed
**AND** no 'Report Faulty Payment Device' option is shown

### C4099945 · Totals — view & print  (2m)  — PARTIAL; refs: TIBU-20914
_Functional / Operator / Totals_

**GIVEN** an operator is signed on
**WHEN** the operator selects Totals
**THEN** the operator's totals are displayed
**WHEN** the operator prints the totals
**THEN** the totals print without a fatal error

### C4099935 · Sign On — audit events  (6m)  — cross-check: CloudFare
_Functional / Sign On & Session / Audit_

**GIVEN** a valid operator
**WHEN** the operator signs on, then signs off, and separately a forced sign-off occurs
**THEN** a Sign On event is recorded to CloudFare
**AND** a Sign Off event is recorded to CloudFare
**AND** a Forced Sign Off event is recorded to CloudFare

### C4099924 · Sign On — Communication Locked  (6m)  — cross-check: CloudFare; refs: TIBU-28530,TIBU-21278
_Functional / Sign On & Session / Communication Locked_

**GIVEN** the POS has lost communication with CloudFare for longer than the configured period
**WHEN** the operator attempts to sign on
**THEN** the "Communication Locked" screen is shown
**AND** it states the device was automatically locked due to lost communication
**AND** it instructs the operator to "Notify a Supervisor or Technician"

### C4099921 · Sign On — incorrect credentials  (6m)  — cross-check: CloudFare; refs: REQ-0050,REQ-0056,REQ-0276,REQ-2821,TIBU-22671,TIBU-24379
_Functional / Sign On & Session / Failures & Lockout_

**GIVEN** the POS is showing the Sign On screen
**WHEN** the operator enters an unrecognised ID or PIN and presses Enter
**THEN** the "Sign On Failed" screen is shown with "The ID or PIN is incorrect"
**AND** the attempt counter is shown (e.g. "1 of 3")
**AND** the operator is returned to the Sign On screen to retry

### C4099922 · Sign On — device locks after the configured failed attempts  (6m)  — **DESTRUCTIVE**; cross-check: CloudFare; refs: REQ-0050,REQ-0099,REQ-2821,TIBU-22672,TIBU-22003
_Functional / Sign On & Session / Failures & Lockout_

**GIVEN** the configured failed-attempt lockout threshold (set via TMS)
**WHEN** the operator enters incorrect credentials up to the configured number of times
**THEN** the device locks after the configured number of attempts
**AND** a Device Locked screen is shown

### C4099923 · Sign On — unlock with Supervisor card  (6m)  — PARTIAL; cross-check: CloudFare; refs: REQ-0050,REQ-1137,REQ-2821,TIBU-21384
_Functional / Sign On & Session / Failures & Lockout_

**GIVEN** the POS is displaying the Device Locked screen
**AND** the POS is communicating with CloudFare
**WHEN** a supervisor presents a valid Supervisor card
**THEN** the device is unlocked
**AND** the POS returns to the Sign On screen

### C4099912 · Sign On — screen, field entry and the 'C' key  (8m)  — PARTIAL; cross-check: CloudFare; refs: REQ-0050
_Functional / Sign On & Session / Idle & Screen_

**Given** the ETM is idle
**WHEN** the Sign On screen is displayed
**THEN** the ID and PIN fields are shown
**WHEN** the operator enters digits into a field
**THEN** the field updates
**AND** the 'C' key clears one character at a time
**WHEN** no entry is made
**THEN** the ETM remains on or returns to the idle Sign On screen

### C4099929 · Sign Off — by role  (6m)  — cross-check: CloudFare; refs: TIBU-21440,TIBU-26846
_Functional / Sign On & Session / Sign Off_

**Given** an operator is signed on
**WHEN** the operator signs off
**THEN** the ETM returns to the idle screen
**AND** the sign-off is audited

### C4099933 · Sign Off — automatic (inactivity)  (6m)  — cross-check: CloudFare
_Functional / Sign On & Session / Sign Off_

**GIVEN** an operator is signed on
**WHEN** the configured inactivity period elapses with no interaction
**THEN** the operator is automatically signed off
**AND** the POS returns to the Idle screen

### C4099934 · Sign Off — forced by power cycle  (6m)  — cross-check: CloudFare; refs: TIBU-24790
_Functional / Sign On & Session / Sign Off_

**GIVEN** an operator is signed on
**WHEN** the POS is power-cycled during the shift
**THEN** on restart the POS returns to the Idle screen
**AND** exactly one Forced Sign-off event is recorded to CloudFare

### C4099913 · Sign On — by role (manual and smartcard)  (9m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: REQ-0050,REQ-0056,REQ-0276,REQ-2821,REQ-3013
_Functional / Sign On & Session / Sign On_

**Given** the ETM is at the idle Sign On screen and communicating with CloudFare
**WHEN** the operator enters a valid ID and PIN and confirms
**THEN** the operator is authenticated and reaches the menu for their role
**WHEN** the operator presents a valid staff smartcard instead
**THEN** the ID is pre-populated and, after a valid PIN, the operator reaches their role menu

### C4099925 · Sign On — Message and Word & Colour of the Day  (9m)  — PARTIAL; cross-check: CloudFare
_Functional / Sign On & Session / Sign-on Messages_

**Given** an operator is signing on
**WHEN** the Message of the Day is available
**THEN** it is presented for the operator to confirm
**WHEN** the Message of the Day cannot be retrieved
**THEN** the Message of the Day Unavailable state is shown and sign-on continues
**WHEN** the Word & Colour of the Day is available
**THEN** it is presented for the operator to confirm
**WHEN** the Word & Colour of the Day cannot be retrieved
**THEN** the Word & Colour Unavailable state is shown and sign-on continues

### C4100413 · Smartcard — Half Fare  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-24795
_Functional / Smartcards_

**GIVEN** an operator is selling a fare
**WHEN** the operator presents a Half Fare smartcard
**THEN** the card is recognised
**AND** the half-fare entitlement is applied to the fare

### C4100414 · Smartcard — Youth  (6m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards_

**GIVEN** an operator is selling a fare
**WHEN** the operator presents a Youth smartcard
**THEN** the card is recognised
**AND** the youth entitlement is applied

### C4100415 · Smartcard — yLink  (6m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards_

**GIVEN** an operator is selling a fare
**WHEN** the operator presents a yLink smartcard
**THEN** the card is recognised
**AND** the yLink entitlement is applied

### C4100416 · Smartcard — 24+  (6m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards_

**GIVEN** an operator is selling a fare
**WHEN** the operator presents a 24+ smartcard
**THEN** the card is recognised
**AND** the 24+ entitlement is applied

### C4100417 · Smartcard — Concession  (6m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards_

**GIVEN** an operator is selling a fare
**WHEN** the operator presents a Concession smartcard
**THEN** the card is recognised
**AND** the concession entitlement is applied

### C4100418 · Smartcard — Dependents Pass  (6m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards_

**GIVEN** an operator is selling a fare
**WHEN** the operator presents a Dependents Pass smartcard
**THEN** the card is recognised
**AND** the dependents-pass entitlement is applied

### C4099950 · Supervisor — Print & Zero  (9m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-24786
_Functional / Supervisor / Reports & Information_

**GIVEN** a supervisor is signed on
**WHEN** the supervisor selects Print and Zero (Current or Accumulated)
**THEN** a confirmation prompt asks whether to zero the totals after printing
**WHEN** the supervisor confirms Yes
**THEN** the report is printed
**AND** the totals are reset to zero
**AND** the printout includes operator no., POS no., sign-on/off times, tickets sold, revenue, misc revenue, smartcard validations, annulled tickets, first/last ticket numbers and per-ticket detail

### C4099951 · Supervisor — Versions  (4m)  — PARTIAL; cross-check: CloudFare; refs: TIBU-15782
_Functional / Supervisor / Versions & Comms_

**GIVEN** a supervisor is signed on
**WHEN** the supervisor opens Versions and views the serial, software and configuration versions
**THEN** each version set is displayed with the real version numbers
**AND** each version set can be printed

### C4099952 · Supervisor — Force Comms  (5m)  — cross-check: CloudFare
_Functional / Supervisor / Versions & Comms_

**GIVEN** a supervisor is signed on
**WHEN** the supervisor initiates a POS-initiated Force Comms
**THEN** the communication is performed
**WHEN** the supervisor refreshes and then exits Force Comms
**THEN** the supervisor returns to the Supervisor menu

### C4099953 · Technician — Device Settings  (1m)  — refs: TIBU-16044,TIBU-16228,TIBU-20967,TIBU-24866
_Functional / Technician / Device Settings_

**GIVEN** a technician is signed on
**WHEN** the technician changes the Home Location, Boarding Location, Mounting Point and Tray Identifier
**THEN** each setting is updated
**AND** each setting is retained
**AND** the Tray Identifier is stored correctly (prefixed "AT")

### C4100507 · Technician — set Default Boarding Stage  (1m)
_Functional / Technician / Device Settings_

**GIVEN** a Technician is signed on in Device Settings
**WHEN** the Technician sets the Default Boarding Stage
**THEN** the Default Boarding Stage is saved
**AND** subsequent bus fare look-ups use the new default boarding stage

### C4100373 · Display — clock shows correct 24-hour time  (1m)  — refs: TIBU-19560,TIBU-21411
_Functional / Technician / Display_

**GIVEN** the device is powered on and time-synced
**WHEN** the operator views the on-screen clock
**THEN** the time is shown in 24-hour format
**AND** the time is correct for the local time zone (not an hour out)

### C4099955 · Technician — Force Comms  (4m)  — cross-check: CloudFare; refs: TIBU-21096
_Functional / Technician / Maintenance_

**GIVEN** a technician is signed on
**WHEN** the technician initiates, refreshes and exits Force Comms
**THEN** each action completes successfully
**AND** no fatal error occurs

### C4099957 · Technician — Network Settings  (1m)  — refs: TIBU-24740,TIBU-26905
_Functional / Technician / Maintenance_

**GIVEN** a Technician is signed on and on the Network Settings page
**WHEN** the Technician changes the Ethernet setting
**THEN** the Ethernet setting is updated
**AND** the change is applied and retained after the page is reopened

### C4099958 · Technician — Versions  (4m)  — PARTIAL; cross-check: CloudFare; refs: TIBU-15782
_Functional / Technician / Maintenance_

**GIVEN** a technician is signed on
**WHEN** the technician views and prints the serial, software and configuration versions
**THEN** each version set is displayed with real version numbers
**AND** each can be printed

### C4099959 · Technician — Status panels  (1m)  — PARTIAL
_Functional / Technician / Maintenance_

**GIVEN** a technician is signed on
**WHEN** the technician opens the Device Status, Other Devices, Card Reader and Paper Status panels
**THEN** each panel displays the relevant status information

### C4099960 · Technician — card reader test  (6m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-24792
_Functional / Technician / Maintenance_

**GIVEN** a technician is on the card-reader test
**WHEN** the technician presents a smartcard to the test screen
**THEN** the test screen reports the card-read result correctly

### C4099962 · Technician — change operating mode  (1m)  — refs: TIBU-24868
_Functional / Technician / Maintenance_

**GIVEN** a technician is signed on
**WHEN** the technician changes the operating mode from the Technician menu
**THEN** the device switches to the selected operating mode

### C4100384 · Technician — Paper Status back key  (1m)  — PARTIAL; refs: TIBU-23928
_Functional / Technician / Maintenance_

**GIVEN** a technician is on the Paper Status screen
**WHEN** the technician presses Back
**THEN** the technician returns to the previous screen
**AND** no fatal error occurs

### C4100508 · TMS — application update  (4m)  — cross-check: CloudFare
_Functional / Technician / TMS Updates_

**GIVEN** an application update is published to the device via TMS
**WHEN** the device downloads and applies the update
**THEN** the update is applied successfully
**AND** the new application version is shown in Technician → Versions
**AND** no queued transactions or unsent data are lost
**AND** an update audit event is recorded

### C4100509 · TMS — topology update  (4m)  — cross-check: CloudFare
_Functional / Technician / TMS Updates_

**GIVEN** a topology/configuration update is published to the device via TMS
**WHEN** the device downloads and applies the update
**THEN** the update is applied successfully
**AND** the new configuration/topology version is shown in Technician → Versions
**AND** no queued transactions or unsent data are lost
**AND** an update audit event is recorded

### C4100419 · Single ticket  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Tickets_

**GIVEN** an operator is signed on
**WHEN** the operator builds a Single ticket via the mode's fare look-up and takes payment
**THEN** the Single ticket is issued at the correct price
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100420 · Day Return ticket  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Tickets_

**GIVEN** an operator is signed on
**WHEN** the operator builds a Day Return ticket via the mode's fare look-up and takes payment
**THEN** the Day Return ticket is issued at the correct price
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100421 · iLink Single  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Tickets_

**GIVEN** an operator is signed on
**WHEN** the operator sells an iLink Single fare against a presented iLink smartcard
**THEN** the iLink Single is issued/recorded against the card
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100422 · Warrant Return  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Tickets_

**GIVEN** an operator is signed on
**WHEN** the operator builds a Warrant Return and completes the warrant payment
**THEN** the Warrant Return ticket is issued
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100423 · Family & Friends Day ticket  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Tickets_

**GIVEN** an operator is signed on
**WHEN** the operator builds a Family & Friends Day ticket and takes payment
**THEN** the Family & Friends Day ticket is issued
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100022 · Faulty Card — options  (9m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-25818,TIBU-21256
_Functional / Top Up & Validation / Faulty Card_

**GIVEN** the operator presents a faulty smartcard
**WHEN** the faulty smartcard screen is shown
**THEN** Charge Full Fare, Issue Ticket and Select Card Type are offered
**AND** a Cancel option is available
**WHEN** the operator chooses Issue Ticket then Issue Receipt
**THEN** a ticket is produced
**AND** its receipt is produced

### C4100023 · Faulty Card — invalid card removal  (3m)  — PARTIAL; refs: TIBU-20851
_Functional / Top Up & Validation / Faulty Card_

**GIVEN** an invalid top-up card is on the reader
**WHEN** the card is removed
**THEN** the POS detects that the card has been removed

### C4100007 · Top Up — top up a smartcard  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-23016,TIBU-21280,TIBU-21119,TIBU-21184,TIBU-22985
_Functional / Top Up & Validation / Top Up_

**Given** an operator is signed on and a topp-able smartcard is presented
**WHEN** the operator selects Top Up, takes payment and confirms
**THEN** the card is topped up
**AND** a top-up receipt is printed
**AND** the card is auto-validated for the current journey where applicable

### C4100008 · Top Up — cancel a top-up  (3m)  — PARTIAL; refs: TIBU-24858,TIBU-25885,TIBU-21786
_Functional / Top Up & Validation / Top Up_

**GIVEN** the operator has started a smartcard top-up
**WHEN** the operator cancels or presses Back
**THEN** the operator is returned to the previous screen
**AND** the screen remains responsive

### C4100009 · Top Up — Multi-Journey limit  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-21133,TIBU-21992,TIBU-24051,TIBU-25886
_Functional / Top Up & Validation / Top Up_

**GIVEN** the operator presents a Multi-Journey smartcard
**WHEN** the operator tops up journeys
**THEN** the journeys are added
**AND** the journeys are shown
**AND** the card cannot exceed its maximum permitted journeys
**AND** a card with expired journeys can still be topped up
**AND** the device does not crash

### C4100017 · Top Up — mini statement  (3m)  — PARTIAL; refs: TIBU-21450,TIBU-22398,TIBU-25098,TIBU-23989,TIBU-22558
_Functional / Top Up & Validation / Top Up_

**GIVEN** the operator presents a topped-up smartcard
**WHEN** the mini statement is shown
**THEN** it shows the correct card type, number, balance/journeys, start date and expiry
**AND** it reflects top-ups made on this and other devices

### C4100389 · Top Up — non-toppable card handled  (3m)  — PARTIAL; refs: TIBU-21219
_Functional / Top Up & Validation / Top Up_

**GIVEN** the operator presents a card that cannot be topped up
**WHEN** the card is read
**THEN** the POS reports that the card cannot be topped up
**AND** the device does not crash

### C4100435 · Top Up — expired Multi-Journey clears existing journeys  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Top Up & Validation / Top Up_

**GIVEN** the operator presents an expired Multi-Journey card
**WHEN** the operator adds journeys (tops it up) and the top-up succeeds
**THEN** all existing journeys are removed
**AND** a journey-removal receipt is printed

### C4100018 · Validation — validate a smartcard  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Top Up & Validation / Validation_

**GIVEN** the POS is on the main screen
**WHEN** a valid smartcard is presented for validation
**THEN** the validation confirmation screen is shown

### C4100019 · Validation — already validated  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Top Up & Validation / Validation_

**GIVEN** a smartcard has already been validated
**WHEN** the card is presented again
**THEN** the 'Smartcard Already Validated' message is shown

### C4100020 · Validation — hotlisted card  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Top Up & Validation / Validation_

**GIVEN** a smartcard is on the hotlist
**WHEN** the card is presented
**THEN** the Hotlisted Error is shown
**AND** the card is not accepted

### C4100021 · Validation — outside time band  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Top Up & Validation / Validation_

**GIVEN** a smartcard is presented outside its valid time band
**WHEN** the card is read
**THEN** the Outside Time Band handling is applied
**AND** the validation outcome is recorded in the back office (CloudFare, MERIT and SmartTrack)

### C4100427 · Validation — entitlement smartcard sets the ticket type  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Top Up & Validation / Validation_

**GIVEN** an operator is selling a fare in NIR or Ulsterbus mode
**WHEN** the operator presents an entitlement smartcard (e.g. Senior, Blind, War Pensioner, yLink, 24+, Half-Fare, Dependants)
**THEN** the matching ticket type is set (e.g. "60+ Single", "Half Fare Single")
**AND** the fare must be validated per transaction (it cannot be added to a basket)
**AND** the operator can still change the boarding or alighting station
**AND** on Rail, cross-border variants are selectable via the L4/R4 keys
**AND** Half-Fare sub-types (Partially Sighted, Learning Disability, No Driving Licence) and DLA each set the matching ticket type

### C4100428 · Validation — error mid-transaction voids the payment  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Top Up & Validation / Validation_

**GIVEN** a fare is being validated as part of a paid transaction
**WHEN** a validation error occurs
**THEN** any cash or warrant payment is not recorded in the POS audit data
**AND** any card transaction is automatically voided by the POS
**AND** a diagnostic event is recorded to audit the error

### C4100506 · Mini Statement — reflects usage and top-ups  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Top Up & Validation / Validation_

**GIVEN** a smartcard that has been validated/used and topped up
**WHEN** the operator presents the card to view the mini statement
**THEN** the mini statement shows the correct current balance/journeys
**AND** it reflects recent validations/usage
**AND** it reflects top-ups made on this and other devices

### C4100425 · Metro — payment is cash only  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Metro / Payment & Validation_

**GIVEN** an operator is signed on in Metro mode with a fare ready for payment
**WHEN** the operator reaches the payment options
**THEN** only the Cash option is offered
**AND** Bank Card is not offered
**AND** Warrant is not offered

### C4100426 · Metro — no smartcard validation  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Metro / Payment & Validation_

**GIVEN** an operator is signed on in Metro mode
**WHEN** a smartcard is presented
**THEN** no validation is performed
**AND** the Metro top-up / smartcard menu behaviour applies instead

### C4100391 · Top Up — Metro Multi-Journey  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-21133,TIBU-21992,TIBU-25081
_Metro / Top Up_

**GIVEN** the operator presents a Metro Multi-Journey smartcard
**WHEN** the operator tops up journeys and pays
**THEN** the journeys are added
**AND** the journeys are shown
**AND** the card cannot exceed its maximum permitted journeys
**AND** the mini-statement expiry text is correct

### C4099970 · Rail FLU — sell a ticket  (5m)  — cross-check: CloudFare; refs: TIBU-19374,TIBU-24862,TIBU-24853
_NIR (Rail) / Fare Look-Up_

**GIVEN** an operator is signed on with the POS in rail (NIR) mode on the Main Rail screen
**WHEN** the operator selects a boarding station, an alighting station, a passenger type and a ticket type
**THEN** the selected fare and price are shown with the correct field layout
**AND** the correct price is used (including Cross-Border tickets)
**WHEN** the operator adds the fare to the basket
**THEN** the fare is added
**AND** the correct boarding and alighting stations are audited

### C4099971 · Rail FLU — boarding = alighting rejected  (3m)  — PARTIAL; refs: TIBU-19292
_NIR (Rail) / Fare Look-Up_

**GIVEN** the operator is building a rail fare
**WHEN** the operator sets the boarding and alighting stations to the same station
**THEN** the fare is not accepted
**AND** the screen does not offer issue buttons for it

### C4099972 · Rail FLU — station lists & numeric select  (1m)  — refs: TIBU-22953,TIBU-21771
_NIR (Rail) / Fare Look-Up_

**GIVEN** the operator is building a rail fare
**WHEN** the operator opens the station list and enters the station number
**THEN** the station list is displayed
**AND** the numeric selection chooses the station

### C4099973 · Rail FLU — function keys  (1m)  — **DESTRUCTIVE**; refs: TIBU-24774,TIBU-24775,TIBU-21779,TIBU-24827,TIBU-24828,TIBU-21770
_NIR (Rail) / Fare Look-Up_

**GIVEN** the operator is on the Rail FLU screen
**WHEN** the operator presses the function keys (e.g. R3 passengers, R4 ticket types)
**THEN** the corresponding list is displayed with real labels (not "example")
**AND** the device does not crash
**AND** buttons that should be unavailable cannot be pressed

### C4099974 · Rail FLU — C returns  (1m)  — refs: TIBU-24810
_NIR (Rail) / Fare Look-Up_

**GIVEN** the operator is on a Rail FLU sub-screen
**WHEN** the operator presses the 'C' button
**THEN** the operator is returned to the previous FLU screen

### C4099975 · Rail FLU — Main screen rail-only  (1m)  — refs: TIBU-24864
_NIR (Rail) / Fare Look-Up_

**GIVEN** the POS is in rail (NIR) mode on the Main Rail screen
**WHEN** the operator views the screen
**THEN** no 'Bus' or 'Day Tours' button is shown

### C4099976 · Rail FLU — non-Adult-Single keeps state  (3m)  — refs: TIBU-24865
_NIR (Rail) / Fare Look-Up_

**GIVEN** the operator has built a non-Adult-Single rail fare
**WHEN** the operator issues the ticket
**THEN** the Rail FLU screen retains the correct state and does not revert

### C4100385 · Rail FLU — present smartcard  (6m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-21933,TIBU-21786
_NIR (Rail) / Fare Look-Up_

**GIVEN** the operator is on the Rail FLU screen
**WHEN** the operator presents a smartcard
**THEN** the smartcard is handled without a fatal error
**AND** the operator can return to the Rail FLU screen

### C4100429 · Rail FLU — cross-border ticket & currency toggle  (3m)  — refs: TIBU-19374
_NIR (Rail) / Fare Look-Up_

**GIVEN** an operator is building a rail fare with a cross-border boarding or alighting station
**WHEN** the operator views the ticket types
**THEN** cross-border ticket types are shown with the correct price
**WHEN** the operator presses the price button
**THEN** the currency toggles to euro
**WHEN** the operator presses it again
**THEN** the currency toggles back to GBP

### C4100501 · Rail FLU — change boarding & alighting stations  (2m)
_NIR (Rail) / Fare Look-Up_

**GIVEN** the operator has selected a rail fare with boarding and alighting stations
**WHEN** the operator changes the boarding station
**THEN** the fare updates for the new boarding station
**WHEN** the operator changes the alighting station
**THEN** the fare updates for the new alighting station

### C4100502 · Cross-Border — enable Euro currency  (3m)  — PARTIAL
_NIR (Rail) / Fare Look-Up_

**GIVEN** a Cross-Border product is selected on a Rail (NIR) POS
**WHEN** Euro currency is enabled and the price/currency is toggled to Euro
**THEN** the Cross-Border fare is shown in Euros
**AND** payment can be taken in the selected currency

### C4099979 · Rail FLU — Advance Ticket  (2m)  — refs: TIBU-21792,TIBU-22824,TIBU-24826
_NIR (Rail) / Fare Look-Up — Advance & Multi-day_

**GIVEN** the operator selects Advance Ticket on the Rail FLU
**WHEN** the operator enters a valid future date in range
**THEN** the advance ticket is added (basket shows 'Ticket Date DD/MM/YY')
**WHEN** the operator enters an invalid date or one outside the valid advance range
**THEN** an error is shown (3s timeout, override with any key)
**AND** the device does not crash
**AND** an advance ticket cannot be combined with other products in the basket (one at a time)
**AND** the advance date, passenger and ticket type reset after 1 minute of inactivity

### C4099980 · Rail FLU — 3 Day Select  (1m)  — refs: TIBU-24829,TIBU-24837
_NIR (Rail) / Fare Look-Up — Advance & Multi-day_

**GIVEN** the operator selects a 3 Day Select ticket on the Rail FLU
**WHEN** the operator chooses the available days using the day list and the + / - buttons
**THEN** the selected days are applied to the ticket

### C4099981 · Rail FLU — Misc button  (1m)  — refs: TIBU-19454
_NIR (Rail) / Fare Look-Up — Advance & Multi-day_

**GIVEN** the operator is on the Main Rail FLU screen
**WHEN** the operator presses the Misc button
**THEN** the Misc option opens without a fatal error

### C4099977 · Rail FLU — favourites: save & issue  (4m)  — PARTIAL; refs: TIBU-19371,TIBU-24783,TIBU-24781,TIBU-19456
_NIR (Rail) / Fare Look-Up — Favourites_

**GIVEN** the operator is on the Rail FLU screen
**WHEN** the operator saves a fare as a favourite and opens the favourites list
**THEN** the favourites list is shown with paging and correct alignment
**WHEN** the operator selects a favourite
**THEN** the favourite's ticket details are shown
**AND** the flow proceeds to the payment screen

### C4099978 · Rail FLU — favourites: overwrite  (2m)  — refs: TIBU-24095,TIBU-24776,TIBU-24886
_NIR (Rail) / Fare Look-Up — Favourites_

**GIVEN** the operator is overwriting an existing favourite
**WHEN** the operator confirms the overwrite
**THEN** the favourite is stored in the correct slot with no fatal error
**WHEN** the operator instead cancels an overwrite
**THEN** the overwrite is aborted and no change is made

### C4099946 · Excess Ticket — available (rail)  (4m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-24804
_NIR (Rail) / Operator (rail-only)_

**GIVEN** an operator is signed on with the POS in rail (NIR) mode
**WHEN** the operator opens the Operator menu
**THEN** the Excess Ticket feature is available

### C4100393 · NIR — Single  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**WHEN** the operator builds a Single ticket (boarding, alighting, passenger type) and takes payment
**THEN** the Single ticket is issued at the correct price
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100394 · NIR — Day Return  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**WHEN** the operator builds a Day Return ticket and takes payment
**THEN** the Day Return ticket is issued at the correct price
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100395 · 1/3 Off Day Return  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**WHEN** the operator builds a 1/3 Off Day Return ticket and takes payment
**THEN** the ticket is issued with the 1/3 discount applied
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100396 · Weekly Season  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**WHEN** the operator builds a Weekly Season ticket and takes payment
**THEN** the Weekly Season ticket is issued with the correct From/To dates
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100397 · Monthly Season  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-19299
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**WHEN** the operator builds a Monthly Season ticket and takes payment
**THEN** the Monthly Season ticket is issued with the correct From/To dates
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100398 · NIR — Warrant Return  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**WHEN** the operator builds a Warrant Return and completes the warrant payment
**THEN** the Warrant Return ticket is issued
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100399 · 3 Day Select  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**WHEN** the operator builds a 3 Day Select ticket, chooses the days and takes payment
**THEN** the 3 Day Select ticket is issued for the chosen days
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100400 · NIR — Family & Friends Day  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**WHEN** the operator builds a Family & Friends Day ticket and takes payment
**THEN** the Family & Friends Day ticket is issued
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100401 · NIR — iLink Single  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**WHEN** the operator sells an iLink Single fare against a presented iLink smartcard
**THEN** the iLink Single is issued/recorded against the card
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100402 · NIR — Dependents Pass  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in rail (NIR) mode
**WHEN** the operator processes a Dependents Pass smartcard fare
**THEN** the Dependents Pass fare is applied
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100503 · NIR — Cross-Border Single  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in Rail (NIR) mode
**WHEN** the operator selects a Cross-Border Single and takes payment
**THEN** the Cross-Border Single ticket is issued
**AND** a green success banner is displayed following the successful issue

### C4100504 · NIR — Cross-Border Day Return  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_NIR (Rail) / Tickets_

**GIVEN** an operator is signed on in Rail (NIR) mode
**WHEN** the operator selects a Cross-Border Day Return and takes payment
**THEN** the Cross-Border Day Return ticket is issued
**AND** a green success banner is displayed following the successful issue

### C4100362 · Comms — loss enters Communication Locked  (4m)  — cross-check: CloudFare; refs: TIBU-28530,TIBU-27664
_Non-Functional / Comms (CloudFare)_

**GIVEN** the device is operating normally
**WHEN** CloudFare communication is lost beyond the configured period
**THEN** the device enters Communication Locked
**AND** it does not enter Communication Locked while comms are healthy

### C4100363 · Comms — recovery reconnects and syncs  (4m)  — cross-check: CloudFare
_Non-Functional / Comms (CloudFare)_

**GIVEN** the device has lost CloudFare communication
**WHEN** communication is restored
**THEN** the device reconnects to CloudFare
**AND** outstanding transactions are synced

### C4100364 · Comms — token loss does not force Out Of Service  (4m)  — **DESTRUCTIVE**; cross-check: CloudFare; refs: TIBU-21277
_Non-Functional / Comms (CloudFare)_

**GIVEN** the device is signed on and communicating
**WHEN** the authentication token is lost
**THEN** the device re-authenticates
**AND** the device does not go Out Of Service unexpectedly

### C4100365 · Comms — card-reader failures do not flood CloudFare  (4m)  — PARTIAL; cross-check: CloudFare; refs: TIBU-16106
_Non-Functional / Comms (CloudFare)_

**GIVEN** the card reader is experiencing failures
**WHEN** the failures occur repeatedly
**THEN** the failures are reported to CloudFare at a sensible rate
**AND** CloudFare is not flooded with duplicate messages

### C4100366 · Comms — device status and Tray ID reported correctly  (4m)  — cross-check: CloudFare; refs: TIBU-24888,TIBU-24889,TIBU-25071
_Non-Functional / Comms (CloudFare)_

**GIVEN** the device is communicating with CloudFare
**WHEN** the device reports its status
**THEN** the device status is accurate
**AND** the Tray ID is reported correctly

### C4100358 · Printer — paper jam detected and recoverable  (5m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-19311,TIBU-20980,TIBU-26723
_Non-Functional / Printer_

**GIVEN** the operator completes a transaction that prints
**WHEN** the printer experiences a paper jam
**THEN** the Paper Jam screen is shown
**AND** the Annul Transaction control responds
**WHEN** the jam is cleared
**THEN** the device returns to normal operation

### C4100359 · Printer — out of paper is handled  (2m)  — PARTIAL
_Non-Functional / Printer_

**GIVEN** the operator attempts to print
**WHEN** the printer is out of paper
**THEN** the device reports the out-of-paper condition
**WHEN** paper is replaced
**THEN** printing resumes normally

### C4100367 · Smoke — operator sign on  (6m)  — cross-check: CloudFare
_Smoke_

**GIVEN** the device is at the Idle screen and communicating with CloudFare
**WHEN** the operator signs on with valid credentials
**THEN** the operator reaches the Main Screen

### C4100368 · Smoke — sell a ticket (cash)  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Smoke_

**GIVEN** an operator is signed on
**WHEN** the operator builds a fare, adds it to the basket and takes cash payment
**THEN** the ticket is issued
**AND** a receipt is printed

### C4100369 · Smoke — top up a smartcard  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Smoke_

**GIVEN** an operator is signed on
**WHEN** the operator presents a smartcard, tops it up and takes payment
**THEN** the top up is applied to the card
**AND** a receipt is printed

### C4100370 · Smoke — sign off  (4m)  — cross-check: CloudFare
_Smoke_

**GIVEN** an operator is signed on
**WHEN** the operator signs off
**THEN** the device returns to the Idle screen

### C4100374 · Bus FLU — sell a ticket  (1m)  — refs: TIBU-19459,TIBU-19460
_Ulsterbus / Fare Look-Up_

**GIVEN** an operator is signed on with the POS on the Main Screen
**WHEN** the operator enters a route number, sets the boarding and alighting stages and selects a fare type
**THEN** the fare and price are shown
**AND** the product is added to the basket
**AND** the product can be purchased

### C4100375 · Bus FLU — route number letters via the '*' key  (1m)  — refs: TIBU-19458
_Ulsterbus / Fare Look-Up_

**GIVEN** the operator is entering a route number on the Main Screen
**WHEN** the operator presses the '*' key
**THEN** the route-number letter options are shown

### C4100376 · Bus FLU — change boarding stage, alighting stage and fare type  (2m)
_Ulsterbus / Fare Look-Up_

**GIVEN** the operator is building a bus fare
**WHEN** the operator changes the boarding stage
**THEN** the fare updates
**WHEN** the operator changes the alighting stage and fare type
**THEN** the fare updates to reflect each change

### C4100377 · Bus FLU — Misc open fare  (2m)
_Ulsterbus / Fare Look-Up_

**GIVEN** the operator selects a Misc product (open fare)
**WHEN** the operator enters a valid open-fare amount
**THEN** the open fare is accepted
**AND** the open fare is added to the basket
**WHEN** the operator enters an invalid amount
**THEN** the amount is rejected with an error

### C4100378 · Bus FLU — Default Boarding Stage '*' key  (1m)  — refs: TIBU-24026
_Ulsterbus / Fare Look-Up_

**GIVEN** the operator is on the Default Boarding Stage entry
**WHEN** the operator presses the '*' button
**THEN** the expected behaviour occurs with no dead key or error

### C4100403 · Ulsterbus — Single  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**WHEN** the operator builds a Single ticket (route, stages, passenger type) and takes payment
**THEN** the Single ticket is issued at the correct price
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100404 · Ulsterbus — Day Return  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**WHEN** the operator builds a Day Return ticket and takes payment
**THEN** the Day Return ticket is issued at the correct price
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100405 · Month Return  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**WHEN** the operator builds a Month Return ticket and takes payment
**THEN** the Month Return ticket is issued with the correct validity dates
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100406 · Ulsterbus — Warrant Return  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**WHEN** the operator builds a Warrant Return and completes the warrant payment
**THEN** the Warrant Return ticket is issued
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100407 · Bus Rambler  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**WHEN** the operator builds a Bus Rambler ticket and takes payment
**THEN** the Bus Rambler ticket is issued
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100408 · Ulsterbus — Family & Friends Day  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**WHEN** the operator builds a Family & Friends Day ticket and takes payment
**THEN** the Family & Friends Day ticket is issued
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100409 · Jobseeker Single  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**WHEN** the operator builds a Jobseeker Single ticket and takes payment
**THEN** the Jobseeker Single ticket is issued at the correct concession price
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100410 · Ulsterbus — iLink Single  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode
**WHEN** the operator sells an iLink Single fare against a presented iLink smartcard
**THEN** the iLink Single is issued/recorded against the card
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100411 · Rail Substitution Service  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Ulsterbus / Tickets_

**GIVEN** an operator is signed on in Ulsterbus mode running a rail substitution service
**WHEN** the operator processes a Rail Substitution Service fare and takes payment
**THEN** the fare is issued under the rail substitution service
**AND** a receipt is printed
**AND** a green success banner is displayed following the successful ticket issue

### C4100392 · Top Up — Ulsterbus Multi-Journey  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-26861,TIBU-21133
_Ulsterbus / Top Up_

**GIVEN** the operator presents an Ulsterbus Multi-Journey smartcard
**WHEN** the operator tops up journeys and pays
**THEN** the journeys are added following the correct UX flow
**AND** the journeys are shown
**AND** the card cannot exceed its maximum permitted journeys


## Priority: Normal

### C4100034 · Barcode — print barcode  (1m)  — PARTIAL; refs: TIBU-13180
_Functional / Barcode Scanning_

**GIVEN** an operator issues a ticket configured to carry a barcode
**WHEN** the ticket prints
**THEN** a scannable barcode is printed on the ticket

### C4100035 · Barcode — scan barcode  (1m)  — PARTIAL
_Functional / Barcode Scanning_

**GIVEN** an operator is on a screen that accepts a barcode scan
**WHEN** the operator scans a valid barcode
**THEN** the barcode is read
**AND** the corresponding action/product is recognised

### C4100006 · Numerical Input — keypad entry  (1m)  — refs: TIBU-21771
_Functional / Numerical Input_

**GIVEN** the operator is on a screen requiring numeric entry
**WHEN** the operator enters digits and corrects with the C key
**THEN** the entered value reflects the key presses

### C4099940 · Operator Break — leave Break  (1m)
_Functional / Operator / Break Mode_

**GIVEN** the device is in Operator Break mode
**WHEN** the operator leaves Break manually
**THEN** the device returns to the Operator menu

### C4099937 · Operator Options — cancel Soft Reset  (1m)  — refs: TIBU-24727
_Functional / Operator / Options_

**GIVEN** an operator is in Operator Options on the Soft Reset confirmation
**WHEN** the operator presses Cancel
**THEN** the device returns to Operator Options
**AND** no soft reset is performed

### C4099942 · Ticket History — view, detail and paging  (5m)  — refs: TIBU-23091,TIBU-24332,TIBU-24329
_Functional / Operator / Ticket History_

**Given** an operator is signed on with prior transactions
**WHEN** the operator opens Ticket History
**THEN** the issued tickets are listed
**WHEN** the operator selects a ticket
**THEN** the ticket detail is displayed
**WHEN** the operator pages the list
**THEN** further tickets are shown

### C4099948 · Supervisor — Day Information  (2m)  — PARTIAL; refs: TIBU-24785,TIBU-22647
_Functional / Supervisor / Reports & Information_

**GIVEN** a supervisor is signed on
**WHEN** the supervisor opens Day Information
**THEN** the Day Information is displayed with chevron-key instructions
**WHEN** the supervisor prints it
**THEN** the printout shows the correct number of shifts

### C4099949 · Supervisor — Sales Breakdown  (1m)  — PARTIAL; refs: TIBU-19682,TIBU-23936
_Functional / Supervisor / Reports & Information_

**GIVEN** a supervisor is signed on
**WHEN** the supervisor opens Sales Breakdown and prints it
**THEN** the Sales Breakdown is displayed
**AND** the Sales Breakdown is printed
**AND** the printout shows the correct sales information
**AND** the printout does not include stray 'Paper' content

### C4099961 · Technician — menu options  (1m)  — refs: TIBU-22649
_Functional / Technician / Maintenance_

**GIVEN** a technician is signed on
**WHEN** the technician views the Technician menu
**THEN** only the intended options are listed

### C4100437 · Printer — paper low notification  (1m)  — PARTIAL; refs: TIBU-26995
_Non-Functional / Printer_

**GIVEN** the printer paper level is low
**WHEN** the operator is using the POS
**THEN** a temporary paper-low notification is shown (about 3 seconds)

### C4100438 · Printer — print-failure events are sent  (1m)  — PARTIAL
_Non-Functional / Printer_

**GIVEN** the printer encounters a fault (no paper, hardware/software error, or power loss mid-print)
**WHEN** a print fails, partially prints due to power loss, or resumes after power loss
**THEN** the POS sends the corresponding event


## Priority: Low

### C4099939 · Operator Break — enter Break  (2m)  — refs: TIBU-24335,TIBU-24879,TIBU-30633
_Functional / Operator / Break Mode_

**GIVEN** an operator is signed on
**WHEN** the operator selects Operator Break
**THEN** a confirmation screen is shown
**WHEN** the operator confirms
**THEN** the device enters Break mode showing the Break screen
**AND** the Break screen does not show a Bus number
**AND** all on-screen text is spelled correctly

### C4099947 · Supervisor — Duty Information  (2m)  — refs: TIBU-21110,TIBU-21138,TIBU-21323,TIBU-21325,TIBU-27443,TIBU-21367,TIBU-22643
_Functional / Supervisor / Reports & Information_

**GIVEN** a supervisor is signed on
**WHEN** the supervisor opens Duty Information
**THEN** the duty information is displayed with correct headings, text and chevron-key instructions
**AND** the device does not reset
**WHEN** the supervisor selects a duty and scrolls with the chevron keys
**THEN** each individual duty's details can be viewed

### C4099954 · Technician — Display Settings  (1m)  — refs: TIBU-21129
_Functional / Technician / Device Settings_

**GIVEN** a technician is signed on
**WHEN** the technician opens Display Settings and adjusts the level
**THEN** the screen indicates the current level

