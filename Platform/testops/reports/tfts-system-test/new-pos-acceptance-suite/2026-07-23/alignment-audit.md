# Alignment audit - suite 30253

- Cases audited: **528**
- Blocking findings: **0**
- Advisory (reviewed-intentional) findings: **43**

## Residual mojibake in any field - 0
_none_

## Title missing the ' - ' feature separator _(advisory)_ - 6
- C4100419 | Single ticket
- C4100420 | Day Return ticket
- C4100421 | iLink Single
- C4100422 | Warrant Return
- C4100423 | Family & Friends Day ticket
- C4100411 | Rail Substitution Service

## Title over 72 chars _(advisory)_ - 37
- C4103578 | Fare-Stage Selection — the POS shows and prints the Fare Stage name, not the stop name - 86 chars
- C4103580 | Fare-Stage Selection — the operator can reach a fare by keying the Fare Stage ID - 80 chars
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
