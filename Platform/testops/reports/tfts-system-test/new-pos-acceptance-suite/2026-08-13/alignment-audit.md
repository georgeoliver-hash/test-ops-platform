# Alignment audit - suite 30253

- Cases audited: **697**
- Blocking findings: **0**
- Advisory (reviewed-intentional) findings: **86**

## Residual mojibake in any field - 0
_none_

## Title missing the ' - ' feature separator _(advisory)_ - 18
- C4100419 | Single ticket (Adult, cash)
- C4100420 | Day Return ticket (Adult)
- C4100421 | iLink Single (Zone 4, Adult)
- C4100422 | Warrant Return
- C4100423 | Family & Friends Day ticket (cash)
- C4104608 | Single ticket (Child, cash)
- C4104609 | Single ticket (concession, cash)
- C4104610 | Single ticket (Adult, card)
- C4104611 | Single ticket (Adult, warrant)
- C4104612 | Day Return ticket (Child)
- C4104613 | iLink Single (Zone 1, Adult)
- C4104614 | iLink Single (Zone 2, Adult)
- C4104615 | iLink Single (Zone 3, Adult)
- C4104616 | iLink Single (NW Zone, Adult)
- C4104617 | iLink Single (Zone 4, Child)
- C4104618 | Family & Friends Day ticket (card)
- C4104619 | Family & Friends Day ticket (warrant)
- C4100411 | Rail Substitution Service

## Title over 72 chars _(advisory)_ - 68
- C4105125 | Operator Information — Word and Colour of the Day Unavailable screen shown when unavailable - 91 chars
- C4105127 | Operator Information — Message of the Day Unavailable screen shown when unavailable - 83 chars
- C4105129 | Report Faulty Device — reporting shows the Faulty Device icon on the Main Screen - 80 chars
- C4105139 | Sign Out — cancelling from Supervisor Menu Sign Out returns to Supervisor Menu - 78 chars
- C4105142 | Device Settings — Go Back from Device Settings Summary returns to Technician Menu - 81 chars
- C4103578 | Fare-Stage Selection — the POS shows and prints the Fare Stage name, not the stop name - 86 chars
- C4103580 | Fare-Stage Selection — the operator can reach a fare by keying the Fare Stage ID - 80 chars
- C4105087 | Card Payment — Cancel on the Miura M020 during Present declines the transaction - 79 chars
- C4105088 | Card Payment — matching signature completes approval and prints the ticket - 74 chars
- C4105090 | Card Payment — declining without a receipt still returns to the FLU screen - 74 chars
- C4105117 | Numerical Input — Change Boarding and Alighting applies to stage selected via L1/L2 - 83 chars
- C4105147 | Top Up — ABT Basket/Expired Warrant card write failure shows Top Up Error - 73 chars
- C4105151 | Top Up — Belfast Visitor Pass card write failure returns to payment screen - 74 chars
- C4100427 | Validation — entitlement smartcard sets the ticket type (Concession — Senior) - 77 chars
- C4104592 | Validation — entitlement smartcard sets the ticket type (Concession — 60+) - 74 chars
- C4104593 | Validation — entitlement smartcard sets the ticket type (Concession — ROI Senior) - 81 chars
- C4104594 | Validation — entitlement smartcard sets the ticket type (Concession — Blind) - 76 chars
- C4104595 | Validation — entitlement smartcard sets the ticket type (Concession — War Pensioner) - 84 chars
- C4104598 | Validation — entitlement smartcard sets the ticket type (Half-Fare — Partially Sighted) - 87 chars
- C4104599 | Validation — entitlement smartcard sets the ticket type (Half-Fare — Learning Disability) - 89 chars
- C4104600 | Validation — entitlement smartcard sets the ticket type (Half-Fare — No Driving Licence) - 88 chars
- C4104601 | Validation — entitlement smartcard sets the ticket type (Half-Fare — PIPS) - 74 chars
- C4104602 | Validation — entitlement smartcard sets the ticket type (Half-Fare — DLA) - 73 chars
- C4105065 | Barcode Scanning — invalid ticket cancellation retries Validating Details - 73 chars
- C4105073 | Barcode Scanning — validation failure routes to manual Barcode Reference entry - 78 chars
- C4103537 | Card Refund — valid PRN refunds via the payment provider and prints a receipt - 77 chars
- C4103539 | Card Refund — an amount above the original sale value is capped to the original - 79 chars
- C4103541 | Refund — the audit record posts a positive fare with the correct payment method and reference - 93 chars
- C4103543 | Basket Refund — each ticket URN carries its own value while the card PRN is shared - 82 chars
- C4103544 | Cross-device Refund — a POS refunds a sale made on another device (CR115) - 73 chars
- C4103570 | Barcode — a single-use barcode is validated online and shows a green tick - 73 chars
- C4103572 | Barcode — a Manifest (type F) barcode is rejected as not accepted on the POS - 76 chars
- C4103573 | Barcode — offline single-use validation is allowed only at or below the Ceiling Limit - 85 chars
- C4103574 | Barcode — an offline single-use redemption syncs back to Corethree on reconnect - 79 chars
- C4103575 | Barcode — a successful single-use validation is audited as an event, not a MERIT transaction - 92 chars
- C4103576 | Barcode — a failed validation is audited as an event carrying the Unique ID and reason - 86 chars
- C4103581 | Heartbeat — a signed-off POS refreshes Last Communication every 15 minutes via the Staff List check - 99 chars
- C4103582 | Revenue Allocation — a rail ticket sold on an Ulsterbus POS carries the rail route for NIR allocation - 101 chars
- C4105081 | Payment — Rail Advance Ticket Bank Card unavailable when no PCD is attached - 75 chars
- C4105082 | Basket — Rail Advance Ticket routing into the Bus Advance Ticket screen (GAP) - 77 chars
- C4105094 | Day Tours — a non-associated route number shows the Day Tours Error screen - 74 chars
- C4105095 | Day Tours — a non-associated lettered route via Letters ETM shows the Letters Error screen - 90 chars
- C4105111 | Issue Card — invalid card reference number shows Reference Numbers/Invalid - 74 chars
- C4105112 | Issue Card — C button on Reference Numbers picks an alternative reference - 73 chars
- C4100085 | Screen Validation — Administrator Mode_Device Settings_Mounting Point_Active - 76 chars
- C4100102 | Screen Validation — Administrator Mode_Device Settings_Mounting Point_Letters - 77 chars
- C4100119 | Screen Validation — Barcode Scan - Ticket Valid inc_ Date and Depart Time - 73 chars
- C4100120 | Screen Validation — Barcode Scan - Ticket Valid inc_ Date with Expiry and Depart Time - 85 chars
- C4100121 | Screen Validation — Barcode Scan - Ticket Valid inc_ Outbound ands Return - Page 2 - 82 chars
- C4100122 | Screen Validation — Barcode Scan - Ticket Valid inc_ Outbound ands Return - 73 chars
- C4100123 | Screen Validation — Barcode Scan - Transaction Cancelled - Ticket Not Passed Visual Inspection - 94 chars
- C4100124 | Screen Validation — Barcode Scan - Transaction Cancelled - Ticket Not Valid - 75 chars
- C4100199 | Screen Validation — Main Screen - FLU - Multiple Items - Basket - Selected - 74 chars
- C4100200 | Screen Validation — Main Screen - FLU - Multiple Items - Basket - Item removed - 78 chars
- C4100202 | Screen Validation — Main Screen - FLU - Multiple Items - Basket - Selected Added - 80 chars
- C4100203 | Screen Validation — Main Screen - FLU - Multiple Items - Basket - 1Item - Bus Advance Ticket - 92 chars
- C4100205 | Screen Validation — Main Screen - FLU - Multiple Items - Payment - Bank Card Unavailable - 88 chars
- C4100208 | Screen Validation — Main Screen - FLU - Payment - Advance Ticket - Card Unavailable - 83 chars
- C4100209 | Screen Validation — Main Screen - FLU - Payment - Popular - Card Unavailable - 76 chars
- C4100231 | Screen Validation — Numeric Entry - 9017 - Change _ Alighting - Unable to calculate change - 90 chars
- C4100339 | Screen Validation — Operator Menu_Tickets _ Totals_Annulment Options - Card Top Up - 82 chars
- C4100342 | Screen Validation — Operator Menu_Tickets _ Totals_Annul Previous Ticket Rail - 77 chars
- C4100343 | Screen Validation — Operator Menu_Tickets _ Totals_Annulment Options - Card Issue - 81 chars
- C4100346 | Screen Validation — Operator Menu_Tickets _ Totals_Annulment Options - Confirmation - 83 chars
- C4100351 | Screen Validation — Operator Menu_Tickets _ Totals_Annulment Options - Error - 76 chars
- C4100352 | Screen Validation — Operator Menu_Tickets _ Totals_Annulment - No Ticket - Error - 80 chars
- C4105135 | Printer Error — successful reprint returns to the screen where print was attempted - 82 chars
- C4105137 | Printer Error / Paper Jam — non-transaction print shows Continue without Printing - 81 chars

## Objective/preface empty - 0
_none_

## Objective not starting 'This test is to confirm' - 0
_none_

## Preconditions empty - 0
_none_

## Preconditions without a GIVEN - 0
_none_

## No When/Then steps at all - 0
_none_

## First step is not a WHEN - 0
_none_

## Step content not WHEN/AND - 0
_none_

## A WHEN with no THEN outcome - 0
_none_

## Genuine compound THEN (two distinct outcomes) - should split - 0
_none_

## Expected (prose) empty - 0
_none_

## Expected starts with THEN (should be prose) - 0
_none_

## Tags (@project/@device/...) written into the case - 0
_none_
