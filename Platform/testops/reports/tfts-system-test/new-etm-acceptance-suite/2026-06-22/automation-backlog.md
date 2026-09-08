# Automation backlog — **NEW** ETM-Acceptance Suite (ETMS)

_Generated 2026-06-22T10:01:26+00:00 by system-test-ops. Suite id 30254, project TFTS - System Test._

**51 fully automatable + 84 partial** of 441 cases (4 destructive, 306 manual-only). _Partial = the UI flow is automatable but a step (card tap / print / cash) needs a hardware fixture or human eye._

## How to consume

- Reference `ref` (TestRail case id, e.g. C4099911) in each automated test so a result maps back to its case.
- Mirror device + feature as pytest markers; add @pytest.mark.destructive where destructive is true (deselected by default).
- cross_check lists the back-office systems the case asserts — the test must verify the event landed there (CloudFare / MERIT / SmartTrack).
- automatable/priority are system-test-ops judgements and a starting point; the automation engineer may override with rationale.


## Priority: High

### C4100582 · ABT — successful tap, passback and mobile wallet  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / ABT_

**Given** ABT taps are enabled and the ETM is at the FLU screen
**WHEN** a customer taps a valid contactless card or device
**THEN** the tap is accepted for the journey
**AND** a success tone is played
**AND** the passenger display shows "Success"
**WHEN** the same card is tapped again
**THEN** the ETM enters passback mode for the additional passenger
**WHEN** the customer taps a mobile wallet
**THEN** the wallet tap is accepted as for a contactless card

### C4100583 · ABT — declined, error and EMV validation failures  (5m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / ABT_

**Given** ABT taps are enabled and the ETM is at the FLU screen
**WHEN** a customer taps a card that is declined, expired, deny/BIN-listed, or that mis-reads
**THEN** the error tone is played
**AND** a declined receipt is printed
**AND** the passenger display shows "See Driver"
**WHEN** an EMV validation fails
**THEN** the matching EMV validation-failure screen is shown for the reason

### C4100585 · ABT — tap availability rules  (7m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / ABT_

**Given** ABT is configured as enabled
**WHEN** the ETM is at the FLU screen ready for taps
**THEN** ABT taps are accepted
**WHEN** the ETM is on a basket screen, in basket mode, Driver Break, a smartcard screen, the annul screen, the Start New Journey flow, or Travel Mode above 5kph
**THEN** ABT taps are not enabled
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100586 · ABT — Metro zone boarding and alighting  (4m)  — cross-check: CloudFare / MERIT
_Functional / ABT_

**Given** ABT is enabled in a Metro ABT zone
**WHEN** the customer taps for boarding only, alighting only, or both within the Metro ABT zone
**THEN** the ABT journey is recorded for the corresponding boarding/alighting points
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100587 · ABT — Ulsterbus zone boarding and alighting  (4m)  — cross-check: CloudFare / MERIT
_Functional / ABT_

**Given** ABT is enabled in an Ulsterbus ABT zone
**WHEN** the customer taps for boarding only, alighting only, or both within Ulsterbus ABT zones
**THEN** the ABT journey is recorded for the corresponding boarding/alighting points
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100588 · ABT — reverts to standard fixed fare on rule change  (4m)  — cross-check: CloudFare / MERIT
_Functional / ABT_

**Given** an ABT journey is in progress
**WHEN** a different service, journey or fare rule is triggered
**THEN** the ABT fare reverts to the standard fixed fare
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100591 · ABT — invalid taps recorded in back office  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / ABT_

**Given** an invalid ABT tap has occurred on the ETM
**WHEN** the back-office ABT records are reviewed
**THEN** the invalid tap is recorded under ABT with its reason
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100622 · Barcode — online validation (pass and fail)  (5m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Barcode Scanning_

**Given** a Driver is signed on and barcode scanning is available
**WHEN** a valid barcode ticket is scanned and validated online
**THEN** the ticket is accepted with the correct validity detail shown
**AND** the validation is recorded in the back office (CloudFare and MERIT)
**WHEN** a barcode fails online validation
**THEN** the transaction is cancelled with the failure reason shown

### C4100624 · Barcode — offline validation  (5m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Barcode Scanning_

**Given** the ETM is validating a barcode offline
**WHEN** a valid barcode is scanned within the offline validation limit
**THEN** the ticket is accepted offline
**AND** the offline validation is recorded for upload to the back office (CloudFare and MERIT)
**WHEN** the barcode is over the offline validation limit or invalid
**THEN** the barcode is rejected with the reason shown

### C4100625 · Barcode — multiple-use validation  (5m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Barcode Scanning_

**Given** a Driver is signed on and barcode scanning is available
**WHEN** a multiple-use barcode is scanned and multiple use is confirmed
**THEN** the multiple-use ticket is validated
**AND** the validation is recorded in the back office (CloudFare and MERIT)
**WHEN** validation fails
**THEN** the failure reason is shown (passback, incorrect zone, wrong start/end date, or wrong travel method)

### C4100626 · Barcode — mLink scan validation  (5m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Barcode Scanning_

**Given** a Driver is signed on and barcode scanning is available
**WHEN** a valid mLink barcode is scanned
**THEN** the mLink barcode is validated
**AND** the validation is recorded in the back office (CloudFare and MERIT)
**WHEN** an expired mLink barcode is scanned
**THEN** the mLink barcode is rejected as expired

### C4100627 · Barcode — reference entry via Driver Menu  (5m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Barcode Scanning_

**Given** a Driver has opened the barcode reference entry from the Driver Menu
**WHEN** the Driver enters a valid single-use or multiple-use barcode reference
**THEN** the reference is accepted and validated
**AND** the validation is recorded in the back office (CloudFare and MERIT)
**WHEN** the Driver enters an invalid reference
**THEN** the reference is rejected as invalid

### C4100628 · Barcode — printed tickets and print error  (5m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Barcode Scanning_

**Given** a Driver issues a ticket that carries a barcode
**WHEN** the ticket is printed
**THEN** the ticket prints with its barcode
**AND** the ticket sale is recorded in the back office (CloudFare and MERIT)
**WHEN** a print error occurs
**THEN** the barcode-ticket print error is handled

### C4100562 · Basket Mode — build a multi-item basket and pay  (7m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Basket Mode_

**Given** a Driver is signed on at the FLU screen
**WHEN** the Driver presses R6 to enter basket mode with a product/alighting stage selected
**THEN** the selected product is added to the basket and basket mode is active
**WHEN** the Driver adds further items, confirms the basket and takes payment
**THEN** all basket items are issued in one transaction
**AND** the sale is recorded in the back office (CloudFare and MERIT)
**AND** a receipt is printed automatically where mandatory

### C4100563 · Basket Mode — limits and line-item quantity  (3m)
_Functional / Basket Mode_

**Given** a Driver has nine items in the basket
**WHEN** the Driver attempts to add another from the FLU or basket screen
**THEN** the Basket Full error is shown and no item is added
**WHEN** the Driver removes an item
**THEN** a new item can be added
**WHEN** the Driver adjusts a line-item quantity with the '+' or '-' keys
**THEN** the quantity changes, or a relevant error is shown for two seconds when it cannot

### C4100565 · Basket Mode — clear, add more and basket tracker  (6m)  — cross-check: CloudFare / MERIT
_Functional / Basket Mode_

**Given** a Driver has items in the basket
**WHEN** the Driver selects Add More to Basket
**THEN** the ETM returns to FLU with the basket retained
**WHEN** the Driver navigates into a Promo Menu sub-menu
**THEN** the basket tracker remains displayed and functional
**WHEN** the Driver selects Clear Basket
**THEN** the ETM returns to FLU
**AND** the basket is emptied and the product reverts to default

### C4100566 · Basket Mode — annul a basketed transaction  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Basket Mode_

**Given** a Driver has issued a basket of tickets
**WHEN** the Driver annuls the basketed transaction
**THEN** the transaction is annulled
**AND** the annulment is recorded against the shift
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100592 · Capping — cap reached  (1m)
_Functional / Capping_

**Given** a customer is tapping journeys within a capping group
**WHEN** the qualifying journeys for the cap are reached
**THEN** the cap is applied and no further fare is charged for the capped period
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100593 · Capping — journeys without reaching the cap  (1m)
_Functional / Capping_

**Given** a customer is tapping journeys within a capping group
**WHEN** the journeys taken are below the cap threshold
**THEN** each journey is charged normally
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100594 · Capping — multiple services and modes  (1m)
_Functional / Capping_

**Given** a daily capping group spans multiple services and transport modes
**WHEN** the customer taps journeys across those services and modes
**THEN** the journeys aggregate toward the same cap
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100596 · Driver Break — enter, leave and override  (7m)  — PARTIAL; cross-check: CloudFare
_Functional / Driver Menu & Options_

**Given** a Driver is signed on
**WHEN** the Driver selects Driver Break to enter break mode
**THEN** the ETM shows the On Break idle screen
**AND** only the operator who started the break may sign back in
**WHEN** the Driver leaves the break by manual sign-in or Staff card, or aborts the leave
**THEN** the Driver resumes the shift, or the abort returns to the On Break screen
**WHEN** a Supervisor signs in during the break
**THEN** the Supervisor overrides the break
**WHEN** the TMS-configured break time elapses
**THEN** the Driver is signed out and others may sign in
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100606 · Driver Menu — change currency  (2m)
_Functional / Driver Menu & Options_

**Given** a Driver has opened the Driver Menu
**WHEN** the Driver changes the currency to Euros
**THEN** the sale currency is set to Euros
**WHEN** the Driver changes the currency back to Pounds
**THEN** the sale currency is set to Pounds

### C4100607 · Inspector — report and smartcard check  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Driver Menu & Options_

**Given** the Inspector option is selected from the Driver Menu
**WHEN** a smartcard is presented for inspection
**THEN** the card's inspection detail is displayed
**WHEN** an invalid smartcard is presented
**THEN** the invalid-smartcard error is shown
**WHEN** the Inspector requests a report
**THEN** the Inspector report is produced

### C4102170 · Driver options — ticket history and last ticket  (7m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Driver Menu & Options_

**Given** a Driver has opened Driver options
**WHEN** the Driver views the ticket history
**THEN** the issued tickets are listed and can be scrolled with the up/down arrows
**AND** annulled transactions are marked with a cross
**WHEN** the Driver selects the last ticket issued
**THEN** the ticket detail is displayed

### C4100533 · FLU — navigate and select products  (4m)
_Functional / Fare Look-Up / Navigation_

**Given** a Driver is signed on at the FLU Home screen
**WHEN** the Driver views a product group with more than one product
**THEN** up to four toggle pips are shown for the first four products
**AND** a '+' icon is shown when the group holds more than four, highlighted when an extended product is chosen
**WHEN** the Driver selects a preset or menu-type product
**THEN** the selected product is applied with the correct toggle-group indication
**WHEN** the Driver toggles the journey type
**THEN** the fare-based, favourite and transfer journeys can each be viewed
**WHEN** an FLU selection is left idle for 60 seconds
**THEN** the ETM clears the selection and returns to the default FLU page

### C4100535 · FLU — set boarding and alighting stages  (4m)  — PARTIAL
_Functional / Fare Look-Up / Navigation_

**Given** a Driver is signed on at the FLU screen for a known route
**WHEN** the Driver changes the boarding stage while outside the GPS footprint and below 20kph
**THEN** the boarding stage is updated
**WHEN** the bus is inside the GPS footprint or above 20kph
**THEN** manual boarding-stage change is unavailable
**WHEN** the Driver views and pages the alighting stages
**THEN** up to five are shown with the fifth always the route's last stage, paging with no timeout
**WHEN** the Driver selects an alighting stage
**THEN** the selected stage is applied to the sale

### C4100539 · FLU — numeric entry, change and last transaction  (4m)
_Functional / Fare Look-Up / Sales_

**Given** a Driver is signed on at the FLU screen
**WHEN** the Driver enters an amount tendered
**THEN** the change due is calculated
**AND** the change due is displayed
**WHEN** the Driver enters a stage ID to set the boarding or alighting stage
**THEN** the matching stage is set
**WHEN** an entry cannot be completed
**THEN** the relevant error-bar message is shown
**AND** the input is cleared, and 'C' clears one character
**WHEN** a sale completes
**THEN** a success confirmation shows for three seconds with the last transaction in the bottom-right of FLU

### C4100540 · FLU — group ticket payment  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Fare Look-Up / Sales_

**Given** a Driver is signed on at the FLU screen
**WHEN** the Driver builds a group ticket and takes payment
**THEN** the group ticket is issued at the correct price
**AND** a ticket is printed

### C4100541 · FLU — ticket type selection, change and default reversion  (3m)
_Functional / Fare Look-Up / Sales_

**Given** a Driver is signed on at the FLU screen
**WHEN** the Driver selects a ticket type
**THEN** the fare for that ticket type is displayed
**WHEN** the Driver changes the ticket type
**THEN** the fare display updates to the new ticket type
**WHEN** a non-default ticket class is left idle for the configured timeout
**THEN** the ticket class reverts to the default

### C4100545 · FLU — currency switch to Euro and back  (2m)
_Functional / Fare Look-Up / Sales_

**Given** a Driver is signed on with an alighting stage selectable
**WHEN** the Driver presses the alighting-stage key a second time
**THEN** the currency switches to Euro (€)
**WHEN** the Driver presses the alighting-stage key a third time
**THEN** the currency switches back to Pounds (£)

### C4100547 · FLU — passenger count  (1m)
_Functional / Fare Look-Up / Sales_

**Given** a Driver is signed on at the FLU screen
**WHEN** the Driver records a passenger count
**THEN** the passenger count is captured against the journey

### C4100548 · FLU — favourite stages  (2m)
_Functional / Fare Look-Up / Sales_

**Given** a Driver is signed on at the FLU screen
**WHEN** the Driver opens the favourite stages
**THEN** the configured favourite stages are listed
**WHEN** the Driver selects a favourite stage
**THEN** the selected stage is applied

### C4100549 · FLU — start a new journey mid-shift  (4m)  — cross-check: CloudFare
_Functional / Fare Look-Up / Sales_

**Given** a Driver is signed on and partway through a shift
**WHEN** the Driver selects Start New Journey and confirms a new route and journey number
**THEN** the ETM updates to the new route and journey
**AND** the change is audited

### C4100629 · GPS — notifications and tracking  (3m)
_Functional / Location_

**Given** a Driver is signed on with GPS active on a route
**WHEN** the ETM acquires a GPS lock or detects a new location
**THEN** the matching notification is shown
**WHEN** the bus arrives at or departs a stop
**THEN** the arrival and departure are detected
**WHEN** the bus approaches the next stop
**THEN** the ETM looks ahead and updates the current stage

### C4100633 · Revenue Limit — approaching notification  (1m)
_Functional / Revenue Limit_

**Given** a Driver is signed on and taking cash fares
**WHEN** the takings approach the pre-configured revenue limit
**THEN** a revenue-limit-approaching notification appears in the header after the Transaction Complete banner
**AND** the notification disappears after three seconds
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100634 · Revenue Limit — reached locks the ETM  (4m)  — PARTIAL; cross-check: CloudFare
_Functional / Revenue Limit_

**Given** a Driver is signed on and the takings reach the maximum revenue limit
**WHEN** the revenue limit is reached
**THEN** the Driver is automatically signed off
**AND** a waybill is printed
**AND** the ETM locks
**AND** a Supervisor or Technician is required to resolve it
**AND** the ETM retrieves its back-office connection in the background
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100510 · Driver Sign On — Manual, first use  (13m)  — PARTIAL; cross-check: CloudFare
_Functional / Sign On & Session / Driver_

**Given** the ETM is displaying the idle screen
**AND** the ETM is communicating with CloudFare
**WHEN** the Enter key is pressed and a valid Staff ID (4–6 digits) and PIN are entered, confirming each with Enter
**THEN** the ETM authenticates the operator against the authorised user list
**AND** each PIN digit is masked with a '*' on entry
**AND** the First Use Safety Check screen is displayed
**WHEN** the Driver confirms the bus has been safety checked and answers the Any Defects prompt
**THEN** the Duty Number entry screen is displayed
**WHEN** an invalid duty number is entered, then a valid duty number is entered and confirmed
**THEN** the invalid duty is rejected before the valid one advances to route selection
**WHEN** the Driver selects a route by letters or number, with inbound and outbound journeys filtered
**THEN** the matching route is selected
**WHEN** the Driver selects the journey, an invalid journey number is rejected, and the Route Summary is confirmed
**THEN** the Message of the Day screen is presented, or its Unavailable fallback after the 5-second timeout
**WHEN** the Driver confirms the Message of the Day
**THEN** the Word and Colours of the Day screen is presented, or its Unavailable fallback after the 5-second timeout
**WHEN** the Driver confirms the Word and Colours of the Day
**THEN** the FLU screen is displayed
**AND** the start of shift is audited
**AND** the running total is recorded
**WHEN** the shift is reviewed in CloudFare
**THEN** the staff activity, shift details and defect record can be identified

### C4100511 · Driver Sign On — Smartcard, first use  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Sign On & Session / Driver_

**Given** the ETM is displaying the idle screen
**AND** the ETM is communicating with CloudFare
**WHEN** the Driver presents a Staff pass carrying a Staff ID
**THEN** the operator sign-on screen is displayed with the Staff ID pre-populated
**AND** the PIN field is highlighted for entry
**WHEN** a valid PIN is entered and confirmed with Enter
**THEN** the ETM authenticates the operator and displays the First Use Safety Check screen
**WHEN** the Staff pass is removed
**THEN** the ETM remains on the First Use Safety Check screen and sign-on continues as normal
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100512 · Driver Sign On — first use with defects recorded  (7m)  — cross-check: CloudFare
_Functional / Sign On & Session / Driver_

**Given** the Driver is at the Any Defects screen during first-use sign-on
**WHEN** the Driver selects Yes to record that the bus has defects and enters the defect detail
**THEN** the defect is recorded against the shift
**AND** sign-on continues to the Duty Number entry screen
**WHEN** the shift is reviewed in CloudFare
**THEN** the defect record can be identified against the Driver and vehicle

### C4100513 · Driver Sign On — subsequent use  (7m)  — PARTIAL; cross-check: CloudFare
_Functional / Sign On & Session / Driver_

**Given** the ETM is displaying the idle screen and a first-use safety check has already been performed for the vehicle today
**WHEN** the Driver signs on with a valid ID and PIN
**THEN** the ETM authenticates the operator
**AND** the First Use Safety Check is skipped when already satisfied on board, or presented/overridden per configuration
**WHEN** the Driver completes duty, route and journey selection
**THEN** the FLU screen is displayed
**AND** the shift is audited
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100514 · Driver Sign On — incorrect PIN locks the device after the configured attempts  (7m)  — **DESTRUCTIVE**; cross-check: CloudFare
_Functional / Sign On & Session / Driver_

**Given** the ETM is in idle mode prompting for sign-on
**AND** a configurable failed-attempt threshold is set in the TMS
**WHEN** an invalid PIN is entered for a valid Staff ID, by manual entry and by Staff pass
**THEN** the Sign On Failed screen is displayed after each attempt
**WHEN** the failed attempts reach the configured threshold
**THEN** the device is locked against further sign-on
**AND** the lock-out is audited
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100515 · Driver Sign On — communications locked / not communicating with CloudFare  (7m)  — cross-check: CloudFare
_Functional / Sign On & Session / Driver_

**Given** the ETM has not communicated with CloudFare for the configured number of hours
**WHEN** the idle screen is shown
**THEN** a bad-comms indicator is displayed and communications are locked
**WHEN** the Driver attempts to sign on
**THEN** sign-on proceeds in the not-communicating state per design
**AND** the not-communicating condition is made clear to the Driver
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100521 · Driver Sign On — abandon  (7m)  — PARTIAL; cross-check: CloudFare
_Functional / Sign On & Session / Driver_

**Given** the Driver is mid sign-on
**WHEN** the 'P' key is pressed to reach the Sign Off prompt before route selection
**THEN** sign-on is abandoned with no shift recorded
**WHEN** sign-on is abandoned after Duty Number entry (Route Selection onwards)
**THEN** an End-of-Shift record is recorded
**AND** a Driver Waybill is printed
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100522 · Driver Sign On — idle timeout returns to idle  (6m)  — cross-check: CloudFare
_Functional / Sign On & Session / Driver_

**Given** the Driver is mid sign-on
**WHEN** no button is pressed for 30 seconds
**THEN** the ETM returns to the Idle screen
**AND** if the Driver was signed in they are signed out
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100523 · Driver Sign On — correct topology and fares data presented for the route  (6m)  — PARTIAL; cross-check: CloudFare
_Functional / Sign On & Session / Driver_

**Given** the Driver signs on to a known route in Metro mode
**WHEN** sign-on completes and the FLU screen is displayed
**THEN** the topology and fares data presented match the configured data for that route and mode
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100524 · Driver Sign Off  (6m)  — cross-check: CloudFare
_Functional / Sign On & Session / Driver_

**Given** the Driver is signed on with the FLU screen displayed
**WHEN** the Driver signs off
**THEN** the ETM returns to the Idle screen
**AND** the operator sign-off is audited
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100525 · Supervisor Sign On — Manual  (6m)  — cross-check: CloudFare
_Functional / Sign On & Session / Supervisor_

**Given** the ETM is displaying the idle screen
**WHEN** a Supervisor signs on with a valid ID and PIN
**THEN** the Supervisor menu is displayed
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100526 · Supervisor Sign On — Smartcard  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Sign On & Session / Supervisor_

**Given** the ETM is displaying the idle screen
**WHEN** a Supervisor presents a valid Staff card and enters a valid PIN
**THEN** the Supervisor menu is displayed
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100527 · Supervisor Sign On — device locks after the configured attempts  (6m)  — **DESTRUCTIVE**; cross-check: CloudFare
_Functional / Sign On & Session / Supervisor_

**Given** the ETM is prompting for sign-on with a configured failed-attempt threshold
**WHEN** a Supervisor enters an invalid PIN up to the configured threshold
**THEN** the device is locked against further sign-on
**AND** the lock-out is audited
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100528 · Supervisor — unlock a PIN-locked device  (7m)  — PARTIAL; cross-check: CloudFare
_Functional / Sign On & Session / Supervisor_

**Given** an operator has PIN-locked the device
**WHEN** the Supervisor signs in with their Staff card
**THEN** the Supervisor menu is displayed
**AND** the device is no longer PIN-locked
**WHEN** the Activity Log for the device is filtered in CloudFare Estate Management
**THEN** an Unlocked entry for the device is shown for the time of the action

### C4100529 · Supervisor Sign Off — manual and idle timeout  (7m)  — cross-check: CloudFare
_Functional / Sign On & Session / Supervisor_

**Given** the ETM is displaying the Supervisor menu
**WHEN** the Supervisor signs off manually
**THEN** the ETM returns to idle
**AND** the sign-off is audited
**WHEN** no buttons are pressed for 60 seconds instead
**THEN** the ETM returns to idle mode
**AND** the operator sign-off is audited
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100530 · Technician Sign On — Manual  (6m)  — cross-check: CloudFare
_Functional / Sign On & Session / Technician_

**Given** the ETM is displaying the idle screen
**WHEN** a Technician signs on with a valid ID and PIN
**THEN** the Technician menu is displayed
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100531 · Technician Sign On — Smartcard  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Sign On & Session / Technician_

**Given** the ETM is displaying the idle screen
**WHEN** a Technician presents a valid Staff card and enters a valid PIN
**THEN** the Technician menu is displayed
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100532 · Technician Sign On — device locks after the configured attempts  (6m)  — **DESTRUCTIVE**; cross-check: CloudFare
_Functional / Sign On & Session / Technician_

**Given** the ETM is prompting for sign-on with a configured failed-attempt threshold
**WHEN** a Technician enters an invalid PIN up to the configured threshold
**THEN** the device is locked against further sign-on
**AND** the lock-out is audited
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4102551 · DayLink — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Commercial_

**Given** the ETM is signed on and in service
**WHEN** a valid DayLink smartcard is presented within its valid day
**THEN** the journey is validated with the success tone
**AND** passback is applied within the configured period
**WHEN** the DayLink is expired, has no days left, or is hotlisted
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102552 · Belfast Visitor Pass — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Commercial_

**Given** the ETM is signed on and in service
**WHEN** a valid Belfast Visitor Pass is presented within its zone and validity
**THEN** the journey is validated with the success tone
**AND** passback is applied within the configured period
**WHEN** the pass is out of zone, expired or hotlisted
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102553 · iLink — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Commercial_

**Given** the ETM is signed on and in service
**WHEN** a valid iLink smartcard is presented within its zone
**THEN** the journey is validated with the success tone
**AND** passback is applied within the configured period
**WHEN** the iLink is presented out of zone, expired or hotlisted
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102554 · aLink — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Commercial_

**Given** the ETM is signed on and in service
**WHEN** a valid aLink smartcard is presented
**THEN** the journey is validated with the success tone
**AND** passback is applied within the configured period
**WHEN** the aLink is expired or hotlisted
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102555 · yLink — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Commercial_

**Given** the ETM is signed on and in service
**WHEN** a valid yLink smartcard is presented
**THEN** the youth-discount journey is validated with the success tone
**AND** passback is applied within the configured period
**WHEN** the yLink is expired or hotlisted
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102556 · 24+ smartcard — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Commercial_

**Given** the ETM is signed on and in service
**WHEN** a valid 24+ smartcard is presented
**THEN** the discount journey is validated with the success tone
**AND** passback is applied within the configured period
**WHEN** the 24+ smartcard is expired or hotlisted
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102537 · 60+ SmartPass — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Concessionary_

**Given** the ETM is signed on and in service
**WHEN** a valid 60+ SmartPass is presented
**THEN** the free-travel journey is validated with the success tone
**AND** passback is applied within the configured period
**WHEN** an expired or hotlisted 60+ SmartPass is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102538 · Senior SmartPass — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Concessionary_

**Given** the ETM is signed on and in service
**WHEN** a valid Senior SmartPass is presented
**THEN** the free-travel journey is validated with the success tone
**AND** passback is applied within the configured period
**WHEN** an expired or hotlisted Senior SmartPass is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102539 · ROI Senior SmartPass — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Concessionary_

**Given** the ETM is signed on and in service
**WHEN** a valid ROI Senior SmartPass is presented on an eligible service
**THEN** the free-travel journey is validated with the success tone
**AND** passback is applied within the configured period
**WHEN** the pass is presented on a non-eligible service, or is expired or hotlisted
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102540 · Blind Person's SmartPass — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Concessionary_

**Given** the ETM is signed on and in service
**WHEN** a valid Blind Person's SmartPass is presented
**THEN** the free-travel journey is validated with the success tone
**AND** a companion is permitted where the pass allows it
**WHEN** an expired or hotlisted Blind Person's SmartPass is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102541 · War Pensioner SmartPass — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Concessionary_

**Given** the ETM is signed on and in service
**WHEN** a valid War Pensioner SmartPass is presented
**THEN** the free-travel journey is validated with the success tone
**AND** passback is applied within the configured period
**WHEN** an expired or hotlisted War Pensioner SmartPass is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102542 · Half-Fare SmartPass — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Concessionary_

**Given** the ETM is signed on and in service
**WHEN** a valid Half-Fare SmartPass is presented
**THEN** a half-fare journey is validated with the success tone
**AND** passback is applied within the configured period
**WHEN** an expired or hotlisted Half-Fare SmartPass is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102543 · Free SmartPass — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Concessionary_

**Given** the ETM is signed on and in service
**WHEN** a valid Free SmartPass is presented
**THEN** the free-travel journey is validated with the success tone
**AND** passback is applied within the configured period
**WHEN** an expired or hotlisted Free SmartPass is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102549 · EA Bus SmartPass — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Education_

**Given** the ETM is signed on and in service
**WHEN** a valid EA Bus SmartPass is presented within its valid time
**THEN** the journey is validated with the success tone
**WHEN** it is presented before the start date, after expiry, outside the valid time, at a weekend or during a school holiday
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102550 · EA Rail SmartPass — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Education_

**Given** the ETM is signed on and in service
**WHEN** a valid EA Rail SmartPass is presented within its valid time
**THEN** the journey is validated with the success tone
**WHEN** it is presented before the start date, after expiry, outside the valid time, at a weekend or during a school holiday
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102568 · Faulty — Fare-Paying Smartcard  (12m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Faulty_

**Given** a faulty fare-paying smartcard is presented on the ETM
**WHEN** the card cannot be read correctly
**THEN** the faulty-card options are offered (Charge Full Fare, Select Card Type, Issue Ticket)
**WHEN** the Driver selects the appropriate option and completes
**THEN** a faulty fare-paying smartcard receipt is produced
**WHEN** the CloudFare activity log is checked
**THEN** the faulty-card event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** any fare charged appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the faulty fare-paying smartcard is recorded in SmartTrack

### C4102569 · Faulty — Smartpass Receipt  (8m)  — PARTIAL; cross-check: CloudFare / SmartTrack
_Functional / Smartcards / Faulty_

**Given** a faulty Smartpass (concessionary) is presented on the ETM
**WHEN** the Driver handles the faulty Smartpass and issues the receipt
**THEN** a faulty Smartpass receipt is produced with the correct content
**WHEN** the CloudFare activity log is checked
**THEN** the faulty-card event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the faulty Smartpass is recorded in SmartTrack

### C4102570 · Faulty — Dependants Pass Receipt  (8m)  — PARTIAL; cross-check: CloudFare / SmartTrack
_Functional / Smartcards / Faulty_

**Given** a faulty Dependants Pass is presented on the ETM
**WHEN** the Driver handles the faulty Dependants Pass and issues the receipt
**THEN** a faulty Dependants Pass receipt is produced with the correct content
**WHEN** the CloudFare activity log is checked
**THEN** the faulty-card event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the faulty Dependants Pass is recorded in SmartTrack

### C4100581 · Hotlisted smartcard — presented and marked  (7m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Hotlist_

**Given** a Driver is signed on at the FLU screen
**WHEN** an already-hotlisted smartcard is presented
**THEN** the card is rejected with a hotlisted error
**WHEN** a smartcard marked for hotlist is presented
**THEN** the card is handled per the hotlist rules
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100579 · Metro Multi-Journey — zone validation  (7m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Multi-Journey_

**Given** a Metro Multi-Journey smartcard for a given zone is presented
**WHEN** the card is validated within its zone
**THEN** the journey is validated against the Multi-Journey balance
**WHEN** the card is presented outside its zone
**THEN** the card is rejected as wrong zone
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100580 · Ulsterbus Multi-Journey — boarding-stage validation  (7m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Multi-Journey_

**Given** an Ulsterbus Multi-Journey smartcard is presented
**WHEN** the card is validated with a valid boarding stage
**THEN** the journey is validated against the Multi-Journey balance
**WHEN** the boarding stage is invalid
**THEN** the card is rejected as an invalid boarding stage
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102557 · Metro Travelcard — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Multi-Journey_

**Given** the ETM is signed on and in service in Metro mode
**WHEN** a valid Metro Travelcard is presented within its period
**THEN** the journey is validated with the success tone
**AND** passback is applied within the configured period
**WHEN** the Metro Travelcard is expired or hotlisted
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102558 · Town Service Travelcard — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Multi-Journey_

**Given** the ETM is signed on and in service in Ulsterbus mode
**WHEN** a valid Town Service Travelcard is presented on its town service within its period
**THEN** the journey is validated with the success tone
**AND** passback is applied within the configured period
**WHEN** the Town Service Travelcard is presented off its town service, is expired or is hotlisted
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102544 · Staff SmartPass — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Staff_

**Given** the ETM is signed on and in service
**WHEN** a valid Staff SmartPass is presented
**THEN** the staff-travel journey is validated with the success tone
**AND** passback is applied within the configured period
**WHEN** an expired or hotlisted Staff SmartPass is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102545 · Staff Spouse / Partner Pass — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Staff_

**Given** the ETM is signed on and in service
**WHEN** a valid Staff Spouse / Partner Pass is presented
**THEN** the journey is validated with the success tone
**AND** passback is applied within the configured period
**WHEN** an expired or hotlisted Staff Spouse / Partner Pass is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102546 · Staff Dependants Pass — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Staff_

**Given** the ETM is signed on and in service
**WHEN** a valid Staff Dependants Pass is presented
**THEN** the journey is validated with the success tone
**AND** passback is applied within the configured period
**WHEN** an expired or hotlisted Staff Dependants Pass is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102547 · Retired Staff Pass — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Staff_

**Given** the ETM is signed on and in service
**WHEN** a valid Retired Staff Pass is presented
**THEN** the journey is validated with the success tone
**AND** passback is applied within the configured period
**WHEN** an expired or hotlisted Retired Staff Pass is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102548 · External Staff Pass — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Staff_

**Given** the ETM is signed on and in service
**WHEN** a valid External Staff Pass is presented
**THEN** the journey is validated with the success tone
**AND** passback is applied within the configured period
**WHEN** an expired or hotlisted External Staff Pass is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the validation transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100572 · Smartcard top-up — successful, maximum and expired-journey rules  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Top-Up_

**Given** a customer presents a topp-able smartcard and the Driver selects Top-Up
**WHEN** the Driver takes payment and confirms the top-up
**THEN** the card is topped up
**AND** a top-up receipt is printed
**AND** the card is auto-validated for the current journey
**WHEN** a Multi-Journey top-up would exceed 50 journeys
**THEN** the top-up is capped at the 50-journey maximum
**WHEN** the card has expired journeys at top-up
**THEN** the expired journeys are removed with a removal receipt where applicable
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100573 · Smartcard top-up — cancelled with Back  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Top-Up_

**Given** the Driver is in the smartcard top-up flow
**WHEN** the Driver selects Back or the card is removed before payment
**THEN** the top-up is cancelled
**AND** the ETM returns to the FLU Home screen
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100576 · Smartcard top-up — annulment  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Top-Up_

**Given** a Driver has just topped up a smartcard
**WHEN** the Driver annuls the top-up transaction
**THEN** the top-up is annulled
**AND** the annulment is recorded
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100577 · Smartcard — mini-statement  (9m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Top-Up_

**Given** a customer presents a smartcard and the Driver opens the smartcard menu
**WHEN** the Driver selects Mini Statement
**THEN** the card's mini-statement is displayed
**WHEN** the card is removed
**THEN** the ETM returns to the FLU Home screen

### C4100578 · Smartcard — inter-device top-up then validate on ETM  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Top-Up_

**Given** a smartcard has been topped up on another device
**WHEN** the card is presented to the ETM for validation
**THEN** the ETM validates the card reflecting the top-up made elsewhere
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102567 · Fare-Paying Smartcard — top-up  (11m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Top-Up_

**Given** the ETM is signed on and a fare-paying smartcard is presented
**WHEN** the Driver tops up the card with value and takes payment
**THEN** the value is added to the card balance
**AND** the new balance is recorded and a receipt is printed
**WHEN** the CloudFare activity log is checked
**THEN** the top-up event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the top-up transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard balance appears in SmartTrack

### C4100567 · Smartcard — validation and passback rules  (9m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Validation_

**Given** a Driver is signed on at the FLU screen
**WHEN** a customer presents a valid smartcard
**THEN** the card is validated for the journey with a success indication
**WHEN** the same card is presented again in the same direction within the transfer period
**THEN** passback applies and no second fare is taken
**WHEN** the card is presented in a different direction within the transfer period
**THEN** the validation is handled per the transfer rules
**WHEN** the card is presented outside the transfer period
**THEN** a new journey is validated and charged
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100569 · Smartcard — invalid card presented  (6m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Validation_

**Given** a Driver is signed on at the FLU screen
**WHEN** an invalid smartcard is presented
**THEN** the card is rejected with the reason displayed

### C4100570 · Smartcard — concessionary pass validation  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Validation_

**Given** a Driver is signed on at the FLU screen
**WHEN** a valid concessionary pass is presented
**THEN** the matching concessionary entitlement is applied and validated
**WHEN** the pass is invalid or presented outside its valid time
**THEN** the pass is rejected with the reason shown
**WHEN** a passback override is permitted and selected
**THEN** a further validation is allowed
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100571 · Smartcard — faulty card handling  (9m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Validation_

**Given** a faulty smartcard is presented
**WHEN** the Driver selects the card type for the faulty card
**THEN** the Driver is offered to charge full fare or issue a ticket
**WHEN** the Driver issues a ticket or charges full fare
**THEN** the transaction completes
**AND** a faulty Smartpass receipt is produced where applicable
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102566 · Fare-Paying Smartcard — validation  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcards / Validation_

**Given** the ETM is signed on and in service
**WHEN** a fare-paying smartcard with sufficient balance is presented
**THEN** the fare is deducted from the card balance with the success tone
**AND** the remaining balance is recorded
**WHEN** a fare-paying smartcard with insufficient balance is presented
**THEN** the shortfall is handled per the rules
**WHEN** the CloudFare activity log is checked
**THEN** the validation event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the fare transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard balance appears in SmartTrack

### C4100611 · Supervisor — force communications  (6m)  — cross-check: CloudFare
_Functional / Supervisor Menu_

**Given** a Supervisor is at the Supervisor Menu
**WHEN** the Supervisor presses Force Comms
**THEN** the ETM communicates with the back office for downloads and uploads
**WHEN** the Supervisor presses Refresh
**THEN** the communication information is updated
**WHEN** the Supervisor exits
**THEN** the ETM returns to the Supervisor Menu

### C4102177 · Supervisor — view and print versions  (5m)  — PARTIAL; cross-check: CloudFare
_Functional / Supervisor Menu_

**Given** a Supervisor is at the Supervisor Menu
**WHEN** the Supervisor opens Versions and views software versions, configuration data versions and serial numbers
**THEN** the version and serial information is displayed and can be scrolled
**WHEN** the Supervisor prints the information
**THEN** the version and serial information is printed

### C4100614 · Technician — device settings  (3m)
_Functional / Technician Menu_

**Given** a Technician is at the Technician Menu
**WHEN** the Technician edits the home location, tray identifier or fleet identifier and presses Enter to confirm
**THEN** the change is saved
**AND** the Technician returns to the Technician Menu
**WHEN** the home location is not available
**THEN** the home-location-not-available state is shown
**WHEN** the Technician cancels instead
**THEN** the change is discarded
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100619 · Technician — force communications  (5m)  — cross-check: CloudFare
_Functional / Technician Menu_

**Given** a Technician is at the Force Communications screen
**WHEN** the Technician forces communications
**THEN** the ETM communicates with the back office while the status is identified
**WHEN** the Technician refreshes
**THEN** the communication information is updated

### C4102180 · Technician — view and print versions  (5m)  — PARTIAL; cross-check: CloudFare
_Functional / Technician Menu_

**Given** a Technician is at the Technician Menu
**WHEN** the Technician opens Versions and views software versions, configuration versions and serial numbers
**THEN** the version and serial information is displayed
**WHEN** the Technician prints the information
**THEN** the version and serial information is printed

### C4100550 · Ticket Issue — issue a single ticket  (9m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Ticket Issue_

**Given** a Driver is signed on at the FLU screen
**WHEN** the Driver selects a product and alighting stage and takes payment
**THEN** the ticket is issued at the correct fare
**AND** a ticket is printed
**AND** a success confirmation is shown and the last transaction is updated
**WHEN** change is due on the sale
**THEN** a change receipt is printed and can itself be annulled
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100551 · Ticket Issue — annulment (last ticket, timeout and refusal)  (10m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Ticket Issue_

**Given** a Driver has just issued a ticket
**WHEN** the Driver annuls the last issued ticket
**THEN** the transaction is annulled
**AND** an annulment is recorded against the shift
**WHEN** the annul prompt is left unconfirmed past its timeout
**THEN** the annulment is abandoned
**AND** the original ticket remains valid
**WHEN** the Driver attempts to annul a non-annullable transaction
**THEN** the annulment is refused with the reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100555 · Ticket Issue — Easibus stage selection  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Ticket Issue_

**Given** a Driver is signed on at the FLU screen
**WHEN** the Driver selects an Easibus stage and issues the ticket
**THEN** the ticket is issued for the selected Easibus stage
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100556 · Ticket Issue — Open Tickets excess fare  (7m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Ticket Issue_

**Given** a Driver is signed on at the FLU screen
**WHEN** the Driver issues an Open excess ticket for a valid amount
**THEN** the excess ticket is issued at the entered amount
**WHEN** the Driver enters an invalid amount
**THEN** the amount is rejected
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100558 · Promo Menu — issue a promo product  (7m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Ticket Issue / Promo Menu_

**Given** a Driver is signed on at the FLU screen
**WHEN** the Driver opens the Promo Menu, selects a product and takes payment
**THEN** the promo product is issued at the correct fare
**AND** a ticket is printed
**WHEN** the product is a Family & Friends or Metro Family Day product and an additional child is added
**THEN** the additional child is included at the correct fare
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100560 · Promo Menu — promo product not available  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Ticket Issue / Promo Menu_

**Given** a promo product is configured as not currently available
**WHEN** the Driver attempts to select it from the Promo Menu
**THEN** the product is shown as not available and cannot be issued
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100646 · Force communications — CloudFare initiated  (4m)  — cross-check: CloudFare
_Non-Functional / Communications_

**Given** the ETM is in service and communicating with the back office
**WHEN** CloudFare initiates a forced communication
**THEN** the ETM communicates with the back office for downloads and uploads

### C4100647 · Communications — comms lock, interruption and restore  (6m)  — cross-check: CloudFare
_Non-Functional / Communications_

**Given** the ETM has not communicated with the back office for the configured period
**WHEN** the comms-lock threshold is reached
**THEN** communications are locked and indicated to the Driver
**WHEN** communications are interrupted mid-exchange
**THEN** the interruption is handled without data loss
**WHEN** communications are restored
**THEN** the comms lock clears and pending data is exchanged
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100648 · ETM continues working when the BOS connection is lost  (4m)  — cross-check: CloudFare
_Non-Functional / Communications_

**Given** a Driver is signed on and the ETM is working
**WHEN** the back-office connection is lost
**THEN** the ETM continues to operate and queues data to send to the back office
**AND** data due to download from the back office is retrieved once the connection returns

### C4100649 · Download configuration files from the back office  (6m)  — cross-check: CloudFare
_Non-Functional / Communications_

**Given** the back office has configuration files for the ETM
**WHEN** the ETM downloads a configuration file for immediate activation
**THEN** the configuration is applied
**WHEN** the configuration has a future activation date
**THEN** the configuration is stored and activated on the future date
**WHEN** a corrupt configuration file is downloaded
**THEN** the corrupt file is rejected
**AND** the current configuration is retained
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100650 · Software distribution and fare-mode transition  (4m)  — cross-check: CloudFare
_Non-Functional / Communications_

**Given** the back office has distributed a future fare mode to the ETM
**WHEN** the activation point is reached
**THEN** the ETM transitions from the current fare mode to the future fare mode
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100651 · Upload audit files and data to the back office  (4m)  — cross-check: CloudFare
_Non-Functional / Communications_

**Given** the ETM has audit files and data to send
**WHEN** the ETM communicates with the back office
**THEN** the audit files are uploaded
**AND** the operational data is uploaded

### C4100636 · Power loss recovery — within and outside the recovery period  (3m)
_Non-Functional / Power_

**Given** a Driver is signed on and in service
**WHEN** power is lost and restored within the recovery period
**THEN** the ETM recovers to the signed-in state
**WHEN** power is lost and restored outside the recovery period
**THEN** the ETM does not recover the signed-in state and returns to idle
**WHEN** the power loss occurs in break mode
**THEN** the ETM recovers to the break state appropriately
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100640 · Paper management — low, jam, out and replacement  (4m)  — PARTIAL
_Non-Functional / Printer and Paper_

**Given** a Driver is signed on
**WHEN** the paper falls below the low threshold after printing a ticket
**THEN** the Paper Low warning is shown for five seconds and returns to FLU Home
**WHEN** the paper jams
**THEN** the jam is reported with a reverse-paper-feed option
**WHEN** the paper runs out
**THEN** the Paper Out condition is shown
**WHEN** the paper roll is replaced
**THEN** printing is restored

### C4100944 · Regression — sequence ID integrity across power loss  (1m)  — refs: 301074
_Regression_

**Given** the ETM has processed transactions and holds the current sequence ID
**WHEN** the ETM loses power and restarts
**THEN** the sequence ID resumes in sync with no gap or duplication
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100946 · Regression — passenger display GDPR compliance  (1m)  — PARTIAL; refs: 300751
_Regression_

**Given** a customer-facing passenger display is connected
**WHEN** transactions and card interactions are shown on the passenger display
**THEN** no personal or card data is displayed beyond what GDPR permits

### C4100947 · Regression — no freeze on quick card removal after top-up  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: 301209
_Regression_

**Given** a smartcard has just been topped up
**WHEN** the customer removes the smartcard very quickly after the top-up completes
**THEN** the ETM returns to the FLU screen without freezing
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100938 · Smoke — sign on, issue a ticket and sign off  (8m)  — PARTIAL; cross-check: CloudFare / MERIT
_Smoke_

**Given** the ETM is at the idle screen and communicating with CloudFare
**WHEN** a Driver signs on and reaches the FLU screen
**THEN** the Driver is signed on at FLU
**WHEN** the Driver issues a single ticket and takes payment
**THEN** the ticket is issued
**AND** the ticket is printed
**WHEN** the Driver signs off
**THEN** the ETM returns to idle
**AND** the sign-off is audited

### C4100939 · Smoke — smartcard validates on tap  (6m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Smoke_

**Given** a Driver is signed on at the FLU screen
**WHEN** a customer presents a valid smartcard
**THEN** the card is validated
**AND** a success is indicated

### C4100940 · Smoke — ABT contactless tap succeeds  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_Smoke_

**Given** ABT taps are enabled and the ETM is at the FLU screen
**WHEN** a customer taps a valid contactless card
**THEN** the tap is accepted with the success tone

### C4100941 · Smoke — smartcard top-up succeeds  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Smoke_

**Given** a Driver is signed on and a topp-able smartcard is presented
**WHEN** the Driver tops up the card and takes payment
**THEN** the card is topped up
**AND** a receipt is printed

### C4100942 · Smoke — basket sale of multiple tickets  (3m)  — PARTIAL
_Smoke_

**Given** a Driver is signed on at the FLU screen
**WHEN** the Driver adds multiple tickets to the basket and takes a single payment
**THEN** all basket items are issued in one transaction

### C4100943 · Smoke — ETM communicates with the back office  (4m)  — cross-check: CloudFare
_Smoke_

**Given** the ETM is in service
**WHEN** communications with the back office are forced
**THEN** the ETM exchanges data with the back office successfully


## Priority: Normal

### C4100595 · Driver Menu — access and navigation  (2m)
_Functional / Driver Menu & Options_

**Given** a Driver is signed on at the FLU screen
**WHEN** the Driver opens the Driver Menu
**THEN** the Driver Menu options are displayed
**WHEN** the Driver presses 'C' or Go Back
**THEN** the ETM returns to the previous screen

### C4102169 · Driver options — duty and journey totals  (1m)
_Functional / Driver Menu & Options_

**Given** a Driver has opened Driver options
**WHEN** the Driver views the totals
**THEN** the duty totals and journey totals are displayed

### C4102171 · Driver options — messages  (2m)
_Functional / Driver Menu & Options_

**Given** a Driver has opened Driver options
**WHEN** the Driver views Messages
**THEN** the available messages are displayed
**WHEN** messages cannot be retrieved
**THEN** the Messages — Unavailable state is shown

### C4102172 · Driver options — Word and Colour of the Day  (2m)
_Functional / Driver Menu & Options_

**Given** a Driver has opened Driver options
**WHEN** the Driver views the Word and Colour of the Day
**THEN** the configured word and colour are displayed
**WHEN** the Word and Colour of the Day cannot be retrieved
**THEN** the Unavailable state is shown

### C4102173 · Driver options — paper status  (1m)  — PARTIAL
_Functional / Driver Menu & Options_

**Given** a Driver has opened Driver options
**WHEN** the Driver views Paper Status
**THEN** the current paper status is displayed

### C4100610 · Supervisor — historic waybills  (1m)
_Functional / Supervisor Menu_

**Given** a Supervisor is at the Supervisor Menu
**WHEN** the Supervisor opens Historic Waybills and selects one
**THEN** the waybill detail is displayed
**AND** the left/right arrows move between waybills

### C4102178 · Supervisor — GPS information  (2m)
_Functional / Supervisor Menu_

**Given** a Supervisor is at the Supervisor Menu
**WHEN** the Supervisor views GPS Information
**THEN** the current GPS information is displayed
**WHEN** GPS information cannot be obtained
**THEN** the GPS information error state is shown

### C4100616 · Technician — network settings  (2m)
_Functional / Technician Menu_

**Given** a Technician is at the Network Settings screen
**WHEN** the Technician edits an IP address and confirms
**THEN** the IP address is updated
**WHEN** the Technician views the cellular modem and the network routing table
**THEN** the cellular modem detail and routing table are displayed and can be refreshed

### C4100621 · Technician — decommissioning  (2m)
_Functional / Technician Menu_

**Given** a Technician is at the Technician Menu
**WHEN** the Technician selects Decommissioning
**THEN** a decommissioning warning is shown before any action
**WHEN** the Technician confirms the warning
**THEN** the ETM is decommissioned
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100638 · Power Saving Mode — entering and leaving  (2m)
_Non-Functional / Power_

**Given** the ETM is idle and configured for power saving
**WHEN** the conditions to enter Power Saving Mode are met
**THEN** the ETM enters Power Saving Mode
**WHEN** the ETM is woken
**THEN** the ETM leaves Power Saving Mode and returns to its prior state

### C4100639 · Scheduled Maintenance — suspend and idle  (2m)
_Non-Functional / Power_

**Given** a scheduled maintenance window applies
**WHEN** the ETM is in idle mode during the window
**THEN** the scheduled maintenance is performed
**WHEN** the ETM comes out of suspend
**THEN** the ETM resumes to idle ready for service

### C4100641 · Printer — out of service error  (1m)  — PARTIAL; **DESTRUCTIVE**
_Non-Functional / Printer and Paper_

**Given** a Driver is signed on
**WHEN** the printer cannot complete a print and is out of service
**THEN** the Out of Service error is displayed

### C4100948 · Regression — no error navigating back from passenger-type menu  (1m)  — refs: 301683
_Regression_

**Given** the Driver is in the Adult/Child/Other passenger-type menu
**WHEN** the Driver navigates back from the menu
**THEN** the ETM returns to the previous screen without an internal error

### C4100950 · Regression — ticket print speed  (1m)  — PARTIAL; refs: 301258
_Regression_

**Given** the ETM printer is loaded and ready
**WHEN** a 110mm ticket is printed
**THEN** the ticket prints within the target print-speed time
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

