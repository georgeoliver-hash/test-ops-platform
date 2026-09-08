# Alignment audit - suite 30284

- Cases audited: **201**
- Blocking findings: **0**
- Advisory (reviewed-intentional) findings: **33**

## Residual mojibake in any field - 0
_none_

## Title missing the ' - ' feature separator _(advisory)_ - 0
_none_

## Title over 72 chars _(advisory)_ - 33
- C4103599 | Buy a Smartcard — issuing a new journey-based card writes the product and prints a receipt - 90 chars
- C4103600 | Smartcard Top-up — adding journeys to a Multi-Journey card updates the balance and prints a receipt - 99 chars
- C4103601 | Smartcard Top-up — a Travelcard or Period Pass top-up adds a period and prints a receipt - 88 chars
- C4103602 | Smartcard Top-up — top-up amount labels come from the recharge product Display Descriptions - 91 chars
- C4103605 | Concession — a yLink smartcard prices a ticket at the yLink concessionary fare - 78 chars
- C4103609 | Concession — funded-disability Smartpasses are accepted for concessionary travel - 80 chars
- C4103614 | Invalid Smartcard — re-presenting a card within the passback period is rejected - 79 chars
- C4103615 | Smartcard Top-up — presenting a different card mid top-up aborts the top-up - 75 chars
- C4103616 | Smartcard removed early — removing the card during payment cancels the transaction - 82 chars
- C4103618 | ABT — a card with the ABT application but no ABT Tracking application is rejected - 81 chars
- C4103620 | Ticket Collection — a valid booking reference collects and prints the pre-paid ticket - 85 chars
- C4103621 | Ticket Collection — the booking reference is validated against the back office - 78 chars
- C4103622 | Ticket Collection — a successful redemption emits a Barcode Redemption event - 76 chars
- C4103623 | Ticket Collection — an offline redemption still prints and queues an offline event - 82 chars
- C4103624 | Ticket Collection — a redemption above the barcode ceiling limit cannot validate offline - 88 chars
- C4103626 | Booking Reference — a malformed reference entry is rejected before submission - 77 chars
- C4103627 | Ticket Collection — a collection against a legacy stage resolves the legacy stage name - 86 chars
- C4103629 | Single-Use only — collection accepts a booking reference and not a scanned barcode - 82 chars
- C4103630 | Ticket Collection — a business error shows an error screen and returns to Home after the timeout - 96 chars
- C4103632 | Ticket Collection — an already-redeemed booking reference is rejected as used - 77 chars
- C4103633 | Barcode Ticket Format — a collected ticket prints in the barcode ticket layout - 78 chars
- C4103636 | Coins — coins inserted during the "More Time Required" screen complete the payment - 82 chars
- C4103651 | BNR — a rejected invalid note left hanging from the exit beak leaves the recycler non-functional - 96 chars
- C4103653 | Change — insufficient change prints a Refuse Change Voucher for the balance - 75 chars
- C4103654 | Change — a Refuse Change Voucher is printed when cash is inserted during the "More Time Required" screen - 104 chars
- C4103655 | Coin recycler — a Cash Content Report is produced after a hopper is replaced - 76 chars
- C4103656 | Coin recycler — replenishing a hopper restores change-giving from a low-change state - 84 chars
- C4103670 | EMV — selecting card after a cash transaction returns any inserted cash and pays by card - 88 chars
- C4103671 | EMV — a completed card sale posts audit data to CloudFare under the TVM terminal ID - 83 chars
- C4103692 | Ticket Issue — a single ticket for multiple passengers carries no barcode - 73 chars
- C4103674 | Screensaver Wake — touching the idle screen returns to the Sales home screen - 76 chars
- C4103675 | Ticket Sale — a basic single ticket is issued and printed when paid by cash - 75 chars
- C4103676 | Ticket Sale — a basic single ticket is issued and printed when paid by contactless card - 87 chars

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
