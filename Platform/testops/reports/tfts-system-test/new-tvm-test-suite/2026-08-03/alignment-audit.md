# Alignment audit - suite 30284

- Cases audited: **317**
- Blocking findings: **0**
- Advisory (reviewed-intentional) findings: **100**

## Residual mojibake in any field - 0
_none_

## Title missing the ' - ' feature separator _(advisory)_ - 0
_none_

## Title over 72 chars _(advisory)_ - 100
- C4103620 | Ticket Collection — a valid booking reference collects and prints the pre-paid ticket (barcode Type B) - 102 chars
- C4103621 | Ticket Collection — the booking reference is validated against the back office - 78 chars
- C4103622 | Ticket Collection — a successful redemption emits a Barcode Redemption event - 76 chars
- C4103623 | Ticket Collection — an offline redemption still prints and queues an offline event - 82 chars
- C4103624 | Ticket Collection — a redemption above the barcode ceiling limit cannot validate offline - 88 chars
- C4103625 | Booking Reference — an invalid booking reference is rejected (invalid To Station) - 81 chars
- C4103626 | Booking Reference — a malformed reference entry is rejected before submission (incomplete entry) - 96 chars
- C4103627 | Ticket Collection — a collection against a legacy stage resolves the legacy stage name (Type B) - 95 chars
- C4103629 | Single-Use only — collection accepts a booking reference and not a scanned barcode - 82 chars
- C4103630 | Ticket Collection — a business error shows an error screen and returns to Home after the timeout - 96 chars
- C4103632 | Ticket Collection — an already-redeemed booking reference is rejected as used - 77 chars
- C4103633 | Barcode Ticket Format — a collected ticket prints in the barcode ticket layout (Single) - 87 chars
- C4104806 | Ticket Collection — a valid booking reference collects and prints the pre-paid ticket (barcode Type D) - 102 chars
- C4104807 | Ticket Collection — a valid booking reference collects and prints the pre-paid ticket (barcode Type E) - 102 chars
- C4104808 | Ticket Collection — a valid booking reference collects and prints the pre-paid ticket (barcode Type H) - 102 chars
- C4104809 | Ticket Collection — a valid booking reference collects and prints the pre-paid ticket (barcode Type S) - 102 chars
- C4104810 | Ticket Collection — a valid booking reference collects and prints the pre-paid ticket (barcode Type U) - 102 chars
- C4104811 | Ticket Collection — a redemption below the barcode ceiling limit validates offline - 82 chars
- C4104812 | Booking Reference — an invalid booking reference is rejected (invalid From Station) - 83 chars
- C4104813 | Booking Reference — an invalid booking reference is rejected (invalid Product Type) - 83 chars
- C4104814 | Booking Reference — an invalid booking reference is rejected (invalid dates) - 76 chars
- C4104815 | Booking Reference — a malformed reference entry is rejected before submission (no characters) - 93 chars
- C4104816 | Booking Reference — a malformed reference entry is rejected before submission (over-maximum length) - 99 chars
- C4104817 | Booking Reference — a malformed reference entry is rejected before submission (invalid character) - 97 chars
- C4104818 | Ticket Collection — a collection against a legacy stage resolves the legacy stage name (Type E) - 95 chars
- C4104819 | Ticket Collection — a collection against a legacy stage resolves the legacy stage name (Type U) - 95 chars
- C4104820 | Barcode Ticket Format — a collected ticket prints in the barcode ticket layout (Day Return) - 91 chars
- C4104821 | Barcode Ticket Format — a collected ticket prints in the barcode ticket layout (3 Day Select) - 93 chars
- C4104822 | Barcode Ticket Format — a collected ticket prints in the barcode ticket layout (Cross Border) - 93 chars
- C4104823 | Barcode Ticket Format — a collected ticket prints in the barcode ticket layout (Half-fare) - 90 chars
- C4104824 | Barcode Ticket Format — a collected ticket prints in the barcode ticket layout (yLink) - 86 chars
- C4104825 | Barcode Ticket Format — a collected ticket prints in the barcode ticket layout (24+) - 84 chars
- C4104826 | Barcode Ticket Format — a collected ticket prints in the barcode ticket layout (Family) - 87 chars
- C4103636 | Coins — coins inserted during the "More Time Required" screen complete the payment - 82 chars
- C4103637 | Coins — out-of-circulation and sub-value coins are rejected (old round £1) - 74 chars
- C4103639 | Banknotes — a valid banknote in any orientation pays for a transaction (Bank of England) - 88 chars
- C4104116 | Cash — a coin or note jam is cleared successfully during payment or change (coin jam during payment) - 100 chars
- C4104117 | Cash — a coin or note jam that cannot be cleared fails the transaction cleanly (coin jam during payment) - 104 chars
- C4104834 | Banknotes — a valid banknote in any orientation pays for a transaction (Bank of Ireland) - 88 chars
- C4104835 | Banknotes — a valid banknote in any orientation pays for a transaction (Ulster Bank) - 84 chars
- C4104836 | Banknotes — a valid banknote in any orientation pays for a transaction (Danske Bank (Northern Bank)) - 100 chars
- C4104837 | Banknotes — a valid banknote in any orientation pays for a transaction (First Trust Bank) - 89 chars
- C4104841 | Cash — a coin or note jam is cleared successfully during payment or change (note jam during payment) - 100 chars
- C4104842 | Cash — a coin or note jam is cleared successfully during payment or change (coin jam during change) - 99 chars
- C4104843 | Cash — a coin or note jam that cannot be cleared fails the transaction cleanly (note jam during payment) - 104 chars
- C4104844 | Cash — a coin or note jam that cannot be cleared fails the transaction cleanly (coin jam during change) - 103 chars
- C4103650 | BNR — a note left in the exit beak leaves the recycler non-functional (Cancel) - 78 chars
- C4103651 | BNR — a rejected invalid note left hanging from the exit beak leaves the recycler non-functional - 96 chars
- C4103653 | Change — insufficient change prints a Refuse Change Voucher for the balance - 75 chars
- C4103654 | Change — a Refuse Change Voucher is printed when cash is inserted during the "More Time Required" screen - 104 chars
- C4104845 | BNR — a note left in the exit beak leaves the recycler non-functional (Back) - 76 chars
- C4103655 | Coin recycler — a Cash Content Report is produced after a hopper is replaced - 76 chars
- C4103656 | Coin recycler — replenishing a hopper restores change-giving from a low-change state - 84 chars
- C4104114 | BNR — a rejected note left hanging from the exit beak remains functional on Kiosk - 81 chars
- C4103657 | Chip & PIN — a valid card completes payment and prints the ticket (Visa Debit) - 78 chars
- C4103658 | Chip & PIN — a payment with no PIN entered does not complete (Visa Debit) - 73 chars
- C4103659 | Chip & PIN — American Express and Diners cards are accepted (Amex Credit) - 73 chars
- C4103661 | Contactless — a tap at or below the contactless limit is approved (Visa Credit) - 79 chars
- C4103662 | Contactless — a tap above the contactless limit falls back to Chip & PIN (Visa Credit) - 86 chars
- C4103665 | EMV — cancelling at the pinpad ends the payment without a ticket (Chip & PIN) - 77 chars
- C4103671 | EMV — a completed card sale posts audit data to CloudFare under the TVM terminal ID - 83 chars
- C4104115 | EMV — a card removed before the transaction completes is handled safely (Chip & PIN) - 84 chars
- C4104129 | Magnetic Stripe — a valid card completes payment and prints the ticket (Visa Credit) - 84 chars
- C4104561 | Chip & PIN — a valid card completes payment and prints the ticket (Visa Credit) - 79 chars
- C4104562 | Chip & PIN — a valid card completes payment and prints the ticket (Mastercard Debit) - 84 chars
- C4104563 | Chip & PIN — a valid card completes payment and prints the ticket (Mastercard Credit) - 85 chars
- C4104564 | Chip & PIN — a valid card completes payment and prints the ticket (non-GBP issued card) - 87 chars
- C4104565 | Chip & PIN — a payment with no PIN entered does not complete (Mastercard Debit) - 79 chars
- C4104567 | Chip & PIN — American Express and Diners cards are accepted (Diners Club) - 73 chars
- C4104568 | Contactless — a tap at or below the contactless limit is approved (Visa Debit) - 78 chars
- C4104569 | Contactless — a tap at or below the contactless limit is approved (Mastercard Credit) - 85 chars
- C4104570 | Contactless — a tap at or below the contactless limit is approved (Mastercard Debit) - 84 chars
- C4104572 | Contactless — a tap above the contactless limit falls back to Chip & PIN (Visa Debit) - 85 chars
- C4104573 | Contactless — a tap above the contactless limit falls back to Chip & PIN (Mastercard Credit) - 92 chars
- C4104574 | Contactless — a tap above the contactless limit falls back to Chip & PIN (Mastercard Debit) - 91 chars
- C4104577 | EMV — a declined card offers retry or cancel (unsupported card issuer/scheme) - 77 chars
- C4104578 | EMV — cancelling at the pinpad ends the payment without a ticket (Contactless) - 78 chars
- C4104579 | EMV — cancelling at the pinpad ends the payment without a ticket (Magnetic Stripe) - 82 chars
- C4104585 | EMV — switching to card after cash is inserted returns the cash and pays by card - 80 chars
- C4104586 | EMV — a card removed before the transaction completes is handled safely (Contactless) - 85 chars
- C4104587 | Magnetic Stripe — a valid card completes payment and prints the ticket (Visa Debit) - 83 chars
- C4104588 | Magnetic Stripe — a valid card completes payment and prints the ticket (Mastercard Credit) - 90 chars
- C4104589 | Magnetic Stripe — a valid card completes payment and prints the ticket (Mastercard Debit) - 89 chars
- C4103692 | Ticket Issue — a single ticket for multiple passengers carries no barcode - 73 chars
- C4104847 | Ticket Issue — a selected product is issued and printed (card (Chip & PIN)) - 75 chars
- C4104867 | Ticket Issue — Cross Border, Family & Friends and concession rail products print a multi-use barcode - 100 chars
- C4103729 | Ticket Collection — collect a pre-paid ticket using a booking reference (Collect Ticket Code) - 93 chars
- C4104123 | Commissioning — the ticket-collection server address is configured via TMS - 74 chars
- C4103674 | Screensaver Wake — touching the idle screen returns to the Sales home screen - 76 chars
- C4103675 | Ticket Sale — a basic single ticket is issued and printed when paid by cash - 75 chars
- C4103676 | Ticket Sale — a basic single ticket is issued and printed when paid by contactless card - 87 chars
- C4104118 | Security — hopper door opened without authorisation raises a burglary event - 75 chars
- C4104120 | Cash vault — swapping coin and note vaults on power-up raises no panic event - 76 chars
- C4104897 | Security — TVM door opened after 3 failed EMS logins raises a burglary event - 76 chars
- C4104898 | Security — TVM door opened without any EMS login attempt raises a burglary event - 80 chars
- C4103779 | Coin Recycler Hopper — reloading updates recorded cash content (set to full cassette) - 85 chars
- C4104903 | Coin Recycler Hopper — reloading updates recorded cash content (set to empty then manually corrected) - 101 chars
- C4103786 | Device Lockout — a paper ticket cash sale at the lockout limit goes Out of Service - 82 chars
- C4104906 | Device Lockout — a discounted ticket cash sale at the lockout limit goes Out of Service - 87 chars
- C4104909 | Audio Prompts — speech prompts play and contactless input gets audible feedback - 79 chars

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
