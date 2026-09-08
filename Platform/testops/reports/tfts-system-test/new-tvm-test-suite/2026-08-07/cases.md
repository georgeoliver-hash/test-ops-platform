# Cases — TFTS - System Test / **NEW** TVM Test Suite

- Generated: 2026-08-07T10:36:40.665433+00:00
- Total cases: 436

| Case | Title | Section | Linked refs | Has steps |
|---|---|---|---|---|
| C4103620 | Ticket Collection — a valid booking reference collects and prints the pre-paid ticket (barcode Type B) | Functional / Barcode Redemption | FBD-100317, FBD-100483 | yes |
| C4103621 | Ticket Collection — the booking reference is validated against the back office | Functional / Barcode Redemption | FBD-100483 | yes |
| C4103622 | Ticket Collection — a successful redemption emits a Barcode Redemption event | Functional / Barcode Redemption | FBD-100483 | yes |
| C4103623 | Ticket Collection — an offline redemption still prints and queues an offline event | Functional / Barcode Redemption | FBD-100483 | yes |
| C4103624 | Ticket Collection — a redemption above the barcode ceiling limit cannot validate offline | Functional / Barcode Redemption | FBD-100317, FBD-100483 | yes |
| C4103625 | Booking Reference — an invalid booking reference is rejected (invalid To Station) | Functional / Barcode Redemption | FBD-100483 | yes |
| C4103626 | Booking Reference — a malformed reference entry is rejected before submission (incomplete entry) | Functional / Barcode Redemption | FBD-100483 | yes |
| C4103627 | Ticket Collection — a collection against a legacy stage resolves the legacy stage name (Type B) | Functional / Barcode Redemption | FBD-100483 | yes |
| C4103628 | Single-Use only — a multi-use ticket's Collect Ticket Code is rejected | Functional / Barcode Redemption | FBD-100167, FBD-100317 | yes |
| C4103629 | Single-Use only — collection accepts a booking reference and not a scanned barcode | Functional / Barcode Redemption | FBD-100317, FBD-100483 | yes |
| C4103630 | Ticket Collection — a business error shows an error screen and returns to Home after the timeout | Functional / Barcode Redemption | FBD-100483 | yes |
| C4103631 | Ticket Collection — repeated server errors retry and then fall back | Functional / Barcode Redemption | FBD-100483 | yes |
| C4103632 | Ticket Collection — an already-redeemed booking reference is rejected as used | Functional / Barcode Redemption | FBD-100483 | yes |
| C4103633 | Barcode Ticket Format — a collected ticket prints in the barcode ticket layout (Single) | Functional / Barcode Redemption | FBD-100167, FBD-100318 | yes |
| C4104806 | Ticket Collection — a valid booking reference collects and prints the pre-paid ticket (barcode Type D) | Functional / Barcode Redemption | FBD-100317, FBD-100483 | yes |
| C4104807 | Ticket Collection — a valid booking reference collects and prints the pre-paid ticket (barcode Type E) | Functional / Barcode Redemption | FBD-100317, FBD-100483 | yes |
| C4104808 | Ticket Collection — a valid booking reference collects and prints the pre-paid ticket (barcode Type H) | Functional / Barcode Redemption | FBD-100317, FBD-100483 | yes |
| C4104809 | Ticket Collection — a valid booking reference collects and prints the pre-paid ticket (barcode Type S) | Functional / Barcode Redemption | FBD-100317, FBD-100483 | yes |
| C4104810 | Ticket Collection — a valid booking reference collects and prints the pre-paid ticket (barcode Type U) | Functional / Barcode Redemption | FBD-100317, FBD-100483 | yes |
| C4104811 | Ticket Collection — a redemption below the barcode ceiling limit validates offline | Functional / Barcode Redemption | FBD-100317, FBD-100483 | yes |
| C4104812 | Booking Reference — an invalid booking reference is rejected (invalid From Station) | Functional / Barcode Redemption | FBD-100483 | yes |
| C4104813 | Booking Reference — an invalid booking reference is rejected (invalid Product Type) | Functional / Barcode Redemption | FBD-100483 | yes |
| C4104814 | Booking Reference — an invalid booking reference is rejected (invalid dates) | Functional / Barcode Redemption | FBD-100483 | yes |
| C4104815 | Booking Reference — a malformed reference entry is rejected before submission (no characters) | Functional / Barcode Redemption | FBD-100483 | yes |
| C4104816 | Booking Reference — a malformed reference entry is rejected before submission (over-maximum length) | Functional / Barcode Redemption | FBD-100483 | yes |
| C4104817 | Booking Reference — a malformed reference entry is rejected before submission (invalid character) | Functional / Barcode Redemption | FBD-100483 | yes |
| C4104818 | Ticket Collection — a collection against a legacy stage resolves the legacy stage name (Type E) | Functional / Barcode Redemption | FBD-100483 | yes |
| C4104819 | Ticket Collection — a collection against a legacy stage resolves the legacy stage name (Type U) | Functional / Barcode Redemption | FBD-100483 | yes |
| C4104820 | Barcode Ticket Format — a collected ticket prints in the barcode ticket layout (Day Return) | Functional / Barcode Redemption | FBD-100167, FBD-100318 | yes |
| C4104821 | Barcode Ticket Format — a collected ticket prints in the barcode ticket layout (3 Day Select) | Functional / Barcode Redemption | FBD-100167, FBD-100318 | yes |
| C4104822 | Barcode Ticket Format — a collected ticket prints in the barcode ticket layout (Cross Border) | Functional / Barcode Redemption | FBD-100167, FBD-100318 | yes |
| C4104823 | Barcode Ticket Format — a collected ticket prints in the barcode ticket layout (Half-fare) | Functional / Barcode Redemption | FBD-100167, FBD-100318 | yes |
| C4104824 | Barcode Ticket Format — a collected ticket prints in the barcode ticket layout (yLink) | Functional / Barcode Redemption | FBD-100167, FBD-100318 | yes |
| C4104825 | Barcode Ticket Format — a collected ticket prints in the barcode ticket layout (24+) | Functional / Barcode Redemption | FBD-100167, FBD-100318 | yes |
| C4104826 | Barcode Ticket Format — a collected ticket prints in the barcode ticket layout (Family) | Functional / Barcode Redemption | FBD-100167, FBD-100318 | yes |
| C4103634 | Coins — valid coins pay for a transaction and change is returned | Functional / Payments - Cash | REQ-0339 | yes |
| C4103635 | Coins — a valid coin is accepted after an invalid coin is inserted | Functional / Payments - Cash | REQ-0339 | yes |
| C4103636 | Coins — coins inserted during the "More Time Required" screen complete the payment | Functional / Payments - Cash | REQ-0339 | yes |
| C4103637 | Coins — out-of-circulation and sub-value coins are rejected (old round £1) | Functional / Payments - Cash | REQ-0339 | yes |
| C4103638 | Coins — foreign coins are rejected (Euro) | Functional / Payments - Cash | REQ-0339 | yes |
| C4103639 | Banknotes — a valid banknote in any orientation pays for a transaction (Bank of England) | Functional / Payments - Cash | REQ-0339 | yes |
| C4103640 | Banknotes — withdrawn paper notes are rejected (£10) | Functional / Payments - Cash | REQ-0339 | yes |
| C4103641 | Banknotes — a Scottish banknote is accepted as valid sterling | Functional / Payments - Cash | REQ-0339, REQ-1491 | yes |
| C4103642 | Cash — mixed coins and banknotes pay for a transaction | Functional / Payments - Cash | REQ-0339 | yes |
| C4103643 | Cash — overpayment returns the correct change | Functional / Payments - Cash | REQ-0339 | yes |
| C4103644 | Cash — pressing Back returns the inserted cash before the escrow limit | Functional / Payments - Cash | REQ-0339 | yes |
| C4103645 | Cash — pressing Cancel returns the inserted cash after the escrow limit | Functional / Payments - Cash | REQ-0339 | yes |
| C4103646 | Cash — the coin escrow limit stops further coins being accepted | Functional / Payments - Cash | REQ-0339 | yes |
| C4103647 | Cash — the banknote escrow limit stops further notes being accepted | Functional / Payments - Cash | REQ-0339 | yes |
| C4103648 | Cash — a print failure returns the inserted cash | Functional / Payments - Cash | — | yes |
| C4103649 | Cash — a completed cash sale posts audit data to CloudFare | Functional / Payments - Cash | FBD-100341 | yes |
| C4104116 | Cash — a coin or note jam is cleared successfully during payment or change (coin jam during payment) | Functional / Payments - Cash | — | yes |
| C4104117 | Cash — a coin or note jam that cannot be cleared fails the transaction cleanly (coin jam during payment) | Functional / Payments - Cash | — | yes |
| C4104831 | Coins — out-of-circulation and sub-value coins are rejected (2p) | Functional / Payments - Cash | REQ-0339 | yes |
| C4104832 | Coins — out-of-circulation and sub-value coins are rejected (1p) | Functional / Payments - Cash | REQ-0339 | yes |
| C4104833 | Coins — foreign coins are rejected (other non-sterling) | Functional / Payments - Cash | REQ-0339 | yes |
| C4104834 | Banknotes — a valid banknote in any orientation pays for a transaction (Bank of Ireland) | Functional / Payments - Cash | REQ-0339 | yes |
| C4104835 | Banknotes — a valid banknote in any orientation pays for a transaction (Ulster Bank) | Functional / Payments - Cash | REQ-0339 | yes |
| C4104836 | Banknotes — a valid banknote in any orientation pays for a transaction (Danske Bank (Northern Bank)) | Functional / Payments - Cash | REQ-0339 | yes |
| C4104837 | Banknotes — a valid banknote in any orientation pays for a transaction (First Trust Bank) | Functional / Payments - Cash | REQ-0339 | yes |
| C4104838 | Banknotes — withdrawn paper notes are rejected (£5) | Functional / Payments - Cash | REQ-0339 | yes |
| C4104839 | Banknotes — withdrawn paper notes are rejected (£20) | Functional / Payments - Cash | REQ-0339 | yes |
| C4104840 | Banknotes — a non-sterling banknote is rejected | Functional / Payments - Cash | REQ-0339, REQ-1491 | yes |
| C4104841 | Cash — a coin or note jam is cleared successfully during payment or change (note jam during payment) | Functional / Payments - Cash | — | yes |
| C4104842 | Cash — a coin or note jam is cleared successfully during payment or change (coin jam during change) | Functional / Payments - Cash | — | yes |
| C4104843 | Cash — a coin or note jam that cannot be cleared fails the transaction cleanly (note jam during payment) | Functional / Payments - Cash | — | yes |
| C4104844 | Cash — a coin or note jam that cannot be cleared fails the transaction cleanly (coin jam during change) | Functional / Payments - Cash | — | yes |
| C4105364 | Cash Payment — no more cash accepted stops the transaction | Functional / Payments - Cash | — | yes |
| C4105365 | Payment Cancelled — Back returns to Select Payment Type | Functional / Payments - Cash | — | yes |
| C4105366 | Payment Cancelled Please Wait — Cancel returns to the Home Screen | Functional / Payments - Cash | — | yes |
| C4105367 | Payment Cancelled Please Wait — Back returns to Select Payment Type | Functional / Payments - Cash | — | yes |
| C4105368 | Change Returned — Try Again or Back returns to Select Payment Type | Functional / Payments - Cash | — | yes |
| C4105369 | Change Returned — Cancel returns to the Home Screen | Functional / Payments - Cash | — | yes |
| C4105370 | Change Returned — change failing to return shows Payment Cancelation Failure | Functional / Payments - Cash | — | yes |
| C4105390 | Change Voucher — voucher print failure shows the error screen | Functional / Payments - Cash | — | yes |
| C4105391 | Timeouts — resuming from More Time Required returns to the timed-out screen | Functional / Payments - Cash | — | yes |
| C4105392 | Timeouts — no cash or payment type selected times out to Home Screen | Functional / Payments - Cash | — | yes |
| C4105393 | Timeouts — cash entered but payment not completed times out to Home Screen | Functional / Payments - Cash | — | yes |
| C4105394 | Timeouts — payment type selected times out to Home Screen | Functional / Payments - Cash | — | yes |
| C4103650 | BNR — a note left in the exit beak leaves the recycler non-functional (Cancel) | Functional / Payments - Cash / Note Recycler & Change (Astreo only) | — | yes |
| C4103651 | BNR — a rejected invalid note left hanging from the exit beak leaves the recycler non-functional | Functional / Payments - Cash / Note Recycler & Change (Astreo only) | — | yes |
| C4103652 | BNA — a note-acceptor error makes note payment unavailable | Functional / Payments - Cash / Note Recycler & Change (Astreo only) | — | yes |
| C4103653 | Change — insufficient change prints a Refuse Change Voucher for the balance | Functional / Payments - Cash / Note Recycler & Change (Astreo only) | FBD-100341, REQ-0339 | yes |
| C4103654 | Change — a Refuse Change Voucher is printed when cash is inserted during the "More Time Required" screen | Functional / Payments - Cash / Note Recycler & Change (Astreo only) | REQ-0339 | yes |
| C4104845 | BNR — a note left in the exit beak leaves the recycler non-functional (Back) | Functional / Payments - Cash / Note Recycler & Change (Astreo only) | — | yes |
| C4103655 | Coin recycler — a Cash Content Report is produced after a hopper is replaced | Functional / Payments - Cash / Coin Recycler Hopper (Kiosk only) | REQ-2720 | yes |
| C4103656 | Coin recycler — replenishing a hopper restores change-giving from a low-change state | Functional / Payments - Cash / Coin Recycler Hopper (Kiosk only) | REQ-0339 | yes |
| C4104113 | BNR — a note left in the exit beak remains functional on Kiosk (Cancel) | Functional / Payments - Cash / Note Recycler & Change (Kiosk only) | — | yes |
| C4104114 | BNR — a rejected note left hanging from the exit beak remains functional on Kiosk | Functional / Payments - Cash / Note Recycler & Change (Kiosk only) | — | yes |
| C4104846 | BNR — a note left in the exit beak remains functional on Kiosk (Back) | Functional / Payments - Cash / Note Recycler & Change (Kiosk only) | — | yes |
| C4103657 | Chip & PIN — a valid card completes payment and prints the ticket (Visa Debit) | Functional / Payments - EMV & Contactless | REQ-0097, REQ-0295, REQ-0340, REQ-1488, REQ-1515, REQ-1722, REQ-2583 | yes |
| C4103658 | Chip & PIN — a payment with no PIN entered does not complete (Visa Debit) | Functional / Payments - EMV & Contactless | — | yes |
| C4103659 | Chip & PIN — American Express and Diners cards are accepted (Amex Credit) | Functional / Payments - EMV & Contactless | REQ-0097, REQ-0295, REQ-0340, REQ-1722 | yes |
| C4103660 | Chip & PIN — transaction value limits are enforced | Functional / Payments - EMV & Contactless | C3546435-438, REQ-1489 | yes |
| C4103661 | Contactless — a tap at or below the contactless limit is approved (Visa Credit) | Functional / Payments - EMV & Contactless | C1831356-396, C3546403-410, REQ-1488, REQ-1489, REQ-1630, REQ-2519 | yes |
| C4103662 | Contactless — a tap above the contactless limit falls back to Chip & PIN (Visa Credit) | Functional / Payments - EMV & Contactless | REQ-1488, REQ-1489, REQ-2519 | yes |
| C4103663 | Contactless — a mobile wallet payment is approved (Apple Pay) | Functional / Payments - EMV & Contactless | C3546411-434, REQ-1488, REQ-1490, REQ-2519 | yes |
| C4103664 | EMV — a declined card offers retry or cancel (acquirer decline) | Functional / Payments - EMV & Contactless | REQ-1409, REQ-1515, REQ-1591 | yes |
| C4103665 | EMV — cancelling at the pinpad ends the payment without a ticket (Chip & PIN) | Functional / Payments - EMV & Contactless | REQ-1515, REQ-1591 | yes |
| C4103666 | EMV — a payment that times out is not completed (Chip & PIN) | Functional / Payments - EMV & Contactless | REQ-1591 | yes |
| C4103667 | EMV — a print failure voids the card payment (Chip & PIN) | Functional / Payments - EMV & Contactless | REQ-0847, REQ-1515, REQ-1591 | yes |
| C4103668 | EMV — an expired card is rejected | Functional / Payments - EMV & Contactless | REQ-1519 | yes |
| C4103669 | EMV — the PAN is masked on the receipt and back-office systems | Functional / Payments - EMV & Contactless | REQ-1630, REQ-1723 | yes |
| C4103670 | EMV — switching to card before cash is inserted pays by card | Functional / Payments - EMV & Contactless | REQ-0097, REQ-0295, REQ-0340, REQ-1489, REQ-1722, REQ-2583 | yes |
| C4103671 | EMV — a completed card sale posts audit data to CloudFare under the TVM terminal ID | Functional / Payments - EMV & Contactless | FBD-100320, FBD-100341 | yes |
| C4103672 | EMV — a card payment receipt is printed when selected | Functional / Payments - EMV & Contactless | REQ-0097, REQ-0295, REQ-0340 | yes |
| C4104115 | EMV — a card removed before the transaction completes is handled safely (Chip & PIN) | Functional / Payments - EMV & Contactless | — | yes |
| C4104129 | Magnetic Stripe — a valid card completes payment and prints the ticket (Visa Credit) | Functional / Payments - EMV & Contactless | REQ-0340, REQ-1515 | yes |
| C4104130 | Magnetic Stripe — American Express cards are declined (Credit) | Functional / Payments - EMV & Contactless | REQ-0340 | yes |
| C4104561 | Chip & PIN — a valid card completes payment and prints the ticket (Visa Credit) | Functional / Payments - EMV & Contactless | REQ-0097, REQ-0295, REQ-0340, REQ-1488, REQ-1515, REQ-1722, REQ-2583 | yes |
| C4104562 | Chip & PIN — a valid card completes payment and prints the ticket (Mastercard Debit) | Functional / Payments - EMV & Contactless | REQ-0097, REQ-0295, REQ-0340, REQ-1488, REQ-1515, REQ-1722, REQ-2583 | yes |
| C4104563 | Chip & PIN — a valid card completes payment and prints the ticket (Mastercard Credit) | Functional / Payments - EMV & Contactless | REQ-0097, REQ-0295, REQ-0340, REQ-1488, REQ-1515, REQ-1722, REQ-2583 | yes |
| C4104564 | Chip & PIN — a valid card completes payment and prints the ticket (non-GBP issued card) | Functional / Payments - EMV & Contactless | REQ-0097, REQ-0295, REQ-0340, REQ-1488, REQ-1515, REQ-1722, REQ-2583 | yes |
| C4104565 | Chip & PIN — a payment with no PIN entered does not complete (Mastercard Debit) | Functional / Payments - EMV & Contactless | — | yes |
| C4104566 | Chip & PIN — American Express and Diners cards are accepted (Amex Debit) | Functional / Payments - EMV & Contactless | REQ-0097, REQ-0295, REQ-0340, REQ-1722 | yes |
| C4104567 | Chip & PIN — American Express and Diners cards are accepted (Diners Club) | Functional / Payments - EMV & Contactless | REQ-0097, REQ-0295, REQ-0340, REQ-1722 | yes |
| C4104568 | Contactless — a tap at or below the contactless limit is approved (Visa Debit) | Functional / Payments - EMV & Contactless | C1831356-396, C3546403-410, REQ-1488, REQ-1489, REQ-1630, REQ-2519 | yes |
| C4104569 | Contactless — a tap at or below the contactless limit is approved (Mastercard Credit) | Functional / Payments - EMV & Contactless | C1831356-396, C3546403-410, REQ-1488, REQ-1489, REQ-1630, REQ-2519 | yes |
| C4104570 | Contactless — a tap at or below the contactless limit is approved (Mastercard Debit) | Functional / Payments - EMV & Contactless | C1831356-396, C3546403-410, REQ-1488, REQ-1489, REQ-1630, REQ-2519 | yes |
| C4104571 | Contactless — a tap at the legacy £30.00 limit is approved | Functional / Payments - EMV & Contactless | C1831356-396, C3546403-410, REQ-1488, REQ-1489, REQ-1630, REQ-2519 | yes |
| C4104572 | Contactless — a tap above the contactless limit falls back to Chip & PIN (Visa Debit) | Functional / Payments - EMV & Contactless | REQ-1488, REQ-1489, REQ-2519 | yes |
| C4104573 | Contactless — a tap above the contactless limit falls back to Chip & PIN (Mastercard Credit) | Functional / Payments - EMV & Contactless | REQ-1488, REQ-1489, REQ-2519 | yes |
| C4104574 | Contactless — a tap above the contactless limit falls back to Chip & PIN (Mastercard Debit) | Functional / Payments - EMV & Contactless | REQ-1488, REQ-1489, REQ-2519 | yes |
| C4104575 | Contactless — a mobile wallet payment is approved (Google Pay) | Functional / Payments - EMV & Contactless | C3546411-434, REQ-1488, REQ-1490, REQ-2519 | yes |
| C4104576 | Contactless — a mobile wallet payment is approved (Samsung Pay) | Functional / Payments - EMV & Contactless | C3546411-434, REQ-1488, REQ-1490, REQ-2519 | yes |
| C4104577 | EMV — a declined card offers retry or cancel (unsupported card issuer/scheme) | Functional / Payments - EMV & Contactless | REQ-1409, REQ-1515, REQ-1591 | yes |
| C4104578 | EMV — cancelling at the pinpad ends the payment without a ticket (Contactless) | Functional / Payments - EMV & Contactless | REQ-1515, REQ-1591 | yes |
| C4104579 | EMV — cancelling at the pinpad ends the payment without a ticket (Magnetic Stripe) | Functional / Payments - EMV & Contactless | REQ-1515, REQ-1591 | yes |
| C4104580 | EMV — a payment that times out is not completed (Contactless) | Functional / Payments - EMV & Contactless | REQ-1591 | yes |
| C4104581 | EMV — a payment that times out is not completed (Magnetic Stripe) | Functional / Payments - EMV & Contactless | REQ-1591 | yes |
| C4104582 | EMV — a print failure voids the card payment (Contactless) | Functional / Payments - EMV & Contactless | REQ-0847, REQ-1515, REQ-1591 | yes |
| C4104583 | EMV — a print failure voids the card payment (Magnetic Stripe) | Functional / Payments - EMV & Contactless | REQ-0847, REQ-1515, REQ-1591 | yes |
| C4104584 | EMV — a blocked card is rejected | Functional / Payments - EMV & Contactless | REQ-1519 | yes |
| C4104585 | EMV — switching to card after cash is inserted returns the cash and pays by card | Functional / Payments - EMV & Contactless | REQ-0097, REQ-0295, REQ-0340, REQ-1489, REQ-1722, REQ-2583 | yes |
| C4104586 | EMV — a card removed before the transaction completes is handled safely (Contactless) | Functional / Payments - EMV & Contactless | — | yes |
| C4104587 | Magnetic Stripe — a valid card completes payment and prints the ticket (Visa Debit) | Functional / Payments - EMV & Contactless | REQ-0340, REQ-1515 | yes |
| C4104588 | Magnetic Stripe — a valid card completes payment and prints the ticket (Mastercard Credit) | Functional / Payments - EMV & Contactless | REQ-0340, REQ-1515 | yes |
| C4104589 | Magnetic Stripe — a valid card completes payment and prints the ticket (Mastercard Debit) | Functional / Payments - EMV & Contactless | REQ-0340, REQ-1515 | yes |
| C4104590 | Magnetic Stripe — American Express cards are declined (Debit) | Functional / Payments - EMV & Contactless | REQ-0340 | yes |
| C4104591 | Magnetic Stripe — Diners Club cards are declined | Functional / Payments - EMV & Contactless | REQ-0340 | yes |
| C4105371 | Card Payment — payment failure prompts card removal | Functional / Payments - EMV & Contactless | — | yes |
| C4103680 | Ticket Issue — a selected product is issued and printed (cash) | Functional / Sales - Tickets / Ticket Issue | FBD-100207, FBD-100336 | yes |
| C4103681 | Ticket Issue — Adult single ticket (cash) | Functional / Sales - Tickets / Ticket Issue | FBD-100207, FBD-100336 | yes |
| C4103682 | Ticket Issue — Child single ticket (cash) | Functional / Sales - Tickets / Ticket Issue | FBD-100207, FBD-100336 | yes |
| C4103683 | Ticket Issue — Family and Friends day ticket (cash) | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4103684 | Ticket Issue — Family and Friends additional child (cash) | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4103685 | Ticket Issue — Popular tickets shortcut (cash) | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4103686 | Ticket Issue — Evening ticket (cash) | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4103687 | Ticket Issue — Day ticket | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4103688 | Ticket Issue — Summer Bus Rambler ticket (cash) | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4103689 | Ticket Issue — concessionary half-fare single (cash) | Functional / Sales - Tickets / Ticket Issue | FBD-100207, FBD-100336 | yes |
| C4103690 | Ticket Issue — buy a product in a different language | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4103691 | Ticket Issue — issued ticket carries a single-use barcode | Functional / Sales - Tickets / Ticket Issue | FBD-100167, FBD-100317 | yes |
| C4103692 | Ticket Issue — a single ticket for multiple passengers carries no barcode | Functional / Sales - Tickets / Ticket Issue | FBD-100167 | yes |
| C4103693 | Ticket Issue — the sale posts an audit record to the back office | Functional / Sales - Tickets / Ticket Issue | FBD-100341 | yes |
| C4104847 | Ticket Issue — a selected product is issued and printed (card (Chip & PIN)) | Functional / Sales - Tickets / Ticket Issue | FBD-100207, FBD-100336 | yes |
| C4104848 | Ticket Issue — a selected product is issued and printed (contactless) | Functional / Sales - Tickets / Ticket Issue | FBD-100207, FBD-100336 | yes |
| C4104849 | Ticket Issue — Adult single ticket (card (Chip & PIN)) | Functional / Sales - Tickets / Ticket Issue | FBD-100207, FBD-100336 | yes |
| C4104850 | Ticket Issue — Adult single ticket (contactless) | Functional / Sales - Tickets / Ticket Issue | FBD-100207, FBD-100336 | yes |
| C4104851 | Ticket Issue — Child single ticket (card (Chip & PIN)) | Functional / Sales - Tickets / Ticket Issue | FBD-100207, FBD-100336 | yes |
| C4104852 | Ticket Issue — Child single ticket (contactless) | Functional / Sales - Tickets / Ticket Issue | FBD-100207, FBD-100336 | yes |
| C4104853 | Ticket Issue — Family and Friends day ticket (card (Chip & PIN)) | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4104854 | Ticket Issue — Family and Friends day ticket (contactless) | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4104855 | Ticket Issue — Family and Friends additional child (card (Chip & PIN)) | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4104856 | Ticket Issue — Family and Friends additional child (contactless) | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4104857 | Ticket Issue — Popular tickets shortcut (card (Chip & PIN)) | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4104858 | Ticket Issue — Popular tickets shortcut (contactless) | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4104859 | Ticket Issue — Evening ticket (card (Chip & PIN)) | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4104860 | Ticket Issue — Evening ticket (contactless) | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4104861 | Ticket Issue — Summer Bus Rambler ticket (card (Chip & PIN)) | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4104862 | Ticket Issue — Summer Bus Rambler ticket (contactless) | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4104863 | Ticket Issue — concessionary half-fare single (card (Chip & PIN)) | Functional / Sales - Tickets / Ticket Issue | FBD-100207, FBD-100336 | yes |
| C4104864 | Ticket Issue — concessionary half-fare single (contactless) | Functional / Sales - Tickets / Ticket Issue | FBD-100207, FBD-100336 | yes |
| C4104865 | Ticket Issue — Day Return ticket | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4104866 | Ticket Issue — 1 Month Return ticket | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4104867 | Ticket Issue — Cross Border, Family & Friends and concession rail products print a multi-use barcode | Functional / Sales - Tickets / Ticket Issue | FBD-100167, FBD-100317 | yes |
| C4105327 | Ticket Issue — quick select reaches ticket-selected screen without a basket step | Functional / Sales - Tickets / Ticket Issue | — | yes |
| C4105328 | Ticket Issue — ticket selection returns to the Home Screen | Functional / Sales - Tickets / Ticket Issue | — | yes |
| C4105336 | Destination Selection — selecting a popular destination reaches the Buy Tickets screen | Functional / Sales - Tickets / Ticket Issue | — | yes |
| C4105337 | Destination Selection — searching and selecting a station greys out unusable keys and reaches Buy Tickets | Functional / Sales - Tickets / Ticket Issue | — | yes |
| C4105338 | Destination Selection — search narrows to one station and selecting it reaches Buy Tickets | Functional / Sales - Tickets / Ticket Issue | — | yes |
| C4105339 | Destination Selection — 'Back' during search returns to the Main Screen and clears typed letters | Functional / Sales - Tickets / Ticket Issue | — | yes |
| C4105340 | Destination Selection — scroll buttons page through 6 or more Alighting Stage results | Functional / Sales - Tickets / Ticket Issue | — | yes |
| C4105341 | Destination Selection — scroll buttons disappear once fewer than 6 Alighting Stages remain | Functional / Sales - Tickets / Ticket Issue | — | yes |
| C4105342 | Destination Selection — changing the Boarding Stage via 'Departing From' opens selection against the new stage | Functional / Sales - Tickets / Ticket Issue | — | yes |
| C4105343 | Destination Selection — 'Back' after changing Boarding Stage does not undo the change | Functional / Sales - Tickets / Ticket Issue | — | yes |
| C4105344 | Destination Selection — a Boarding Stage with no possible Alighting Stages greys out the keyboard | Functional / Sales - Tickets / Ticket Issue | — | yes |
| C4105345 | Home Screen — selecting Choose Ticket Details opens the Choose Ticket Details flow | Functional / Sales - Tickets / Ticket Issue | — | yes |
| C4105353 | Buy Tickets — Destination and Buy Tickets link to each other and to Choose Ticket Details | Functional / Sales - Tickets / Ticket Issue | — | yes |
| C4105361 | Multi-Modal Home (Bus) — picking a quick ticket opens Choose Ticket Details | Functional / Sales - Tickets / Ticket Issue | — | yes |
| C4105362 | Multi-Modal Home (Bus) — Buy Tickets opens the Buy Tickets flow | Functional / Sales - Tickets / Ticket Issue | — | yes |
| C4103694 | 3-Day — a 3-day ticket is issued (cash) | Functional / Sales - Tickets / Advance & 3-Day | FBD-100336 | yes |
| C4103695 | 3-Day — the ticket is valid for any 3 days within one calendar week | Functional / Sales - Tickets / Advance & 3-Day | FBD-100690 | yes |
| C4104868 | 3-Day — a 3-day ticket is issued (card (Chip & PIN)) | Functional / Sales - Tickets / Advance & 3-Day | FBD-100336 | yes |
| C4104869 | 3-Day — a 3-day ticket is issued (contactless) | Functional / Sales - Tickets / Advance & 3-Day | FBD-100336 | yes |
| C4105326 | Three-Day Travel — changing the start date clears the selected day | Functional / Sales - Tickets / Advance & 3-Day | — | yes |
| C4103696 | NI Rail — Adult single between two stations (cash) | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100207, FBD-100450 | yes |
| C4103697 | NI Rail — Day Return ticket | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4103698 | NI Rail — 3-Day Select ticket (cash) | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100167, FBD-100450 | yes |
| C4103699 | Cross-Border — Adult single (cash) | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100207, FBD-100450 | yes |
| C4103700 | Cross-Border — Day Return ticket | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4103701 | Cross-Border — 1st Class Single | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4103702 | NI Rail — Senior concessionary single | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4103703 | NI Rail — grouped-station area name prints on a cross-border ticket | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450, FBD-100515 | yes |
| C4104870 | NI Rail — Adult single between two stations (card (Chip & PIN)) | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100207, FBD-100450 | yes |
| C4104871 | NI Rail — Adult single between two stations (contactless) | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100207, FBD-100450 | yes |
| C4104872 | NI Rail — 3-Day Select ticket (card (Chip & PIN)) | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100167, FBD-100450 | yes |
| C4104873 | NI Rail — 3-Day Select ticket (contactless) | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100167, FBD-100450 | yes |
| C4104874 | Cross-Border — Adult single (card (Chip & PIN)) | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100207, FBD-100450 | yes |
| C4104875 | Cross-Border — Adult single (contactless) | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100207, FBD-100450 | yes |
| C4104876 | NI Rail — Weekly ticket | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4104877 | NI Rail — Monthly ticket | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4104878 | NI Rail — 1/3-off Day Return ticket | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4104879 | NI Rail — Day Tracker ticket | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4104880 | Cross-Border — Weekly ticket | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4104881 | Cross-Border — Monthly ticket | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4104882 | Cross-Border — 1 Month Return ticket | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4104883 | Cross-Border — 1st Class 1 Month Return | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4104884 | NI Rail — ROI Senior concessionary single | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4104885 | NI Rail — Blind concessionary single | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4104886 | NI Rail — War Pensioner concessionary single | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4104887 | NI Rail — 60+ concessionary single | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4105330 | Rail & Cross-Border — insufficient paper shows the low-paper error | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | — | yes |
| C4105331 | Rail & Cross-Border — purchase over £500.00 shows the invalid-amount error, taking priority over low paper | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | — | yes |
| C4103704 | Basket — adding a product increases the basket quantity | Functional / Sales - Tickets / Basket | FBD-100336 | yes |
| C4103705 | Basket — adding more of the same product increases the quantity | Functional / Sales - Tickets / Basket | FBD-100336 | yes |
| C4103706 | Basket — an identical product merges into the existing basket line | Functional / Sales - Tickets / Basket | FBD-100336 | yes |
| C4103707 | Basket — the same product with different stages is a separate line | Functional / Sales - Tickets / Basket | FBD-100207, FBD-100336 | yes |
| C4103708 | Basket — reducing an item quantity lowers the total | Functional / Sales - Tickets / Basket | FBD-100336 | yes |
| C4103709 | Basket — removing a product with the bin icon deletes the line | Functional / Sales - Tickets / Basket | FBD-100336 | yes |
| C4103710 | Basket — removing the final product empties the basket | Functional / Sales - Tickets / Basket | FBD-100336 | yes |
| C4103711 | Basket — remaining ticket numbers are contiguous after a removal | Functional / Sales - Tickets / Basket | FBD-100336 | yes |
| C4103712 | Basket — amending the boarding stage reduces the fare | Functional / Sales - Tickets / Basket | FBD-100207, FBD-100336 | yes |
| C4103713 | Basket — amending the alighting stage increases the fare | Functional / Sales - Tickets / Basket | FBD-100207, FBD-100336 | yes |
| C4103714 | Basket — Family and Friends quantity set to zero removes the line | Functional / Sales - Tickets / Basket | FBD-100336 | yes |
| C4103715 | Basket — increasing the Family and Friends quantity raises the total | Functional / Sales - Tickets / Basket | FBD-100336 | yes |
| C4103716 | Basket — cash overpayment is handled after amending the basket | Functional / Sales - Tickets / Basket | FBD-100336 | yes |
| C4105303 | Basket — editing a Single/Return item opens its edit screen | Functional / Sales - Tickets / Basket | — | yes |
| C4105304 | Basket — editing a Day Ticket item opens its edit screen | Functional / Sales - Tickets / Basket | — | yes |
| C4105305 | Basket — Pay Now reaches the Payment Process after a payment type is selected | Functional / Sales - Tickets / Basket | — | yes |
| C4105306 | Basket — Pay Now (Basket - 2025 variant) continues the payment flow | Functional / Sales - Tickets / Basket | — | yes |
| C4105307 | Select Payment Type (Basket - 2025) — Back returns to Select tickets with tickets selected | Functional / Sales - Tickets / Basket | — | yes |
| C4105308 | Select Payment Type (Basket - 2025) — Back or View Basket returns to the Basket | Functional / Sales - Tickets / Basket | — | yes |
| C4105309 | Basket — Add More Items reaches the destination selection screen | Functional / Sales - Tickets / Basket | — | yes |
| C4105310 | Basket — Add More Items reaches Operator Selection for another ticket | Functional / Sales - Tickets / Basket | — | yes |
| C4105311 | Destination selection (Basket) — selecting a destination reaches Single-Return Ulsterbus | Functional / Sales - Tickets / Basket | — | yes |
| C4105312 | Destination selection (Basket) — Search Bar opens destination search | Functional / Sales - Tickets / Basket | — | yes |
| C4105313 | Destination search (Basket) — selecting a destination reaches Single-Return Ulsterbus | Functional / Sales - Tickets / Basket | — | yes |
| C4105314 | Destination search (Basket) — Back returns to the Main Screen | Functional / Sales - Tickets / Basket | — | yes |
| C4105315 | Destination search (Basket) — View Basket returns to the prior screen | Functional / Sales - Tickets / Basket | — | yes |
| C4105316 | Single-Return - Ulsterbus (Basket) — proceeds to Select Tickets | Functional / Sales - Tickets / Basket | — | yes |
| C4105317 | Single-Return - Ulsterbus (Basket) — Back returns to destination selection | Functional / Sales - Tickets / Basket | — | yes |
| C4105318 | Select Tickets (Basket) — Arrow Buttons select a ticket count and confirm | Functional / Sales - Tickets / Basket | — | yes |
| C4105319 | Select Tickets (Basket) — Back returns to Single-Return Ulsterbus | Functional / Sales - Tickets / Basket | — | yes |
| C4105320 | Select tickets with tickets selected (Basket) — Back returns to Single-Return Ulsterbus | Functional / Sales - Tickets / Basket | — | yes |
| C4105321 | Select tickets with tickets selected (Basket) — reaches the Basket | Functional / Sales - Tickets / Basket | — | yes |
| C4105322 | Select tickets with tickets selected (Basket) — reaches Select Payment Type (Basket - 2025) | Functional / Sales - Tickets / Basket | — | yes |
| C4105323 | Basket — Cancel with items in the basket returns to the Home Screen and empties the basket | Functional / Sales - Tickets / Basket | — | yes |
| C4103717 | Ticket Numbering — identical products in separate transactions | Functional / Sales - Tickets / Ticket Numbering | FBD-100336 | yes |
| C4103718 | Ticket Numbering — different products in separate transactions | Functional / Sales - Tickets / Ticket Numbering | FBD-100336 | yes |
| C4103719 | Ticket Numbering — identical products in a single transaction | Functional / Sales - Tickets / Ticket Numbering | FBD-100336 | yes |
| C4103720 | Ticket Numbering — different products in a single transaction | Functional / Sales - Tickets / Ticket Numbering | FBD-100336 | yes |
| C4103721 | Ticket Numbering — cancelling a selection does not skip a number | Functional / Sales - Tickets / Ticket Numbering | FBD-100336 | yes |
| C4103722 | Grouped Stops — a grouped TVM defaults to the group boarding stage | Functional / Sales - Tickets / Grouped Stops | FBD-100515 | yes |
| C4103723 | Grouped Stops — alighting list spans all stops in the group | Functional / Sales - Tickets / Grouped Stops | FBD-100515 | yes |
| C4103724 | Grouped Stops — the cheapest non-zero fare combination is selected | Functional / Sales - Tickets / Grouped Stops | FBD-100336, FBD-100515 | yes |
| C4103725 | Grouped Stops — a fare tie is broken by the first combination | Functional / Sales - Tickets / Grouped Stops | FBD-100515 | yes |
| C4103726 | Grouped Stops — the printed boarding stop need not be nearest the TVM | Functional / Sales - Tickets / Grouped Stops | FBD-100515 | yes |
| C4103727 | Grouped Stops — the group name shows on screen and prints on the ticket | Functional / Sales - Tickets / Grouped Stops | FBD-100515 | yes |
| C4103728 | Grouped Stops — no valid fare shows an error screen | Functional / Sales - Tickets / Grouped Stops | FBD-100515 | yes |
| C4103729 | Ticket Collection — collect a pre-paid ticket using a booking reference (Collect Ticket Code) | Functional / Sales - Tickets / Ticket Collection | FBD-100317, FBD-100336 | yes |
| C4103730 | Ticket Collection — an incomplete booking reference is rejected | Functional / Sales - Tickets / Ticket Collection | FBD-100336 | yes |
| C4103731 | Ticket Collection — an invalid-character booking reference is rejected | Functional / Sales - Tickets / Ticket Collection | FBD-100336 | yes |
| C4103732 | Ticket Collection — a full-length valid reference is accepted | Functional / Sales - Tickets / Ticket Collection | FBD-100336 | yes |
| C4105332 | Ticket Collection — repeated invalid booking reference reaches attempt limit | Functional / Sales - Tickets / Ticket Collection | — | yes |
| C4105333 | Ticket Collection — Please wait screen returns to the Home Screen | Functional / Sales - Tickets / Ticket Collection | — | yes |
| C4105334 | Ticket Collection — Back returns to the booking reference entry screen | Functional / Sales - Tickets / Ticket Collection | — | yes |
| C4105335 | Ticket Collection — location-restricted reference shows a location error | Functional / Sales - Tickets / Ticket Collection | — | yes |
| C4105352 | Ticket Collection — Multi Modal Home Screen reaches Ticket Printing via Collect Tickets by Reference | Functional / Sales - Tickets / Ticket Collection | — | yes |
| C4105363 | Multi-Modal Home (Bus) — Collect Tickets opens Collect Tickets by Reference | Functional / Sales - Tickets / Ticket Collection | — | yes |
| C4103738 | Commissioning — a TVM downloads its config and credentials by serial | Functional / Commissioning & Deployment | FBD-100320 | yes |
| C4103739 | Commissioning — credentials stay within the TVM Terminal Group | Functional / Commissioning & Deployment | FBD-100320 | yes |
| C4103740 | Commissioning — topology makes home-location products sellable | Functional / Commissioning & Deployment | FBD-100383, PSPEC-0014, REQ-2710 | yes |
| C4103741 | Software Deployment — immediate dataset installs and updates versions | Functional / Commissioning & Deployment | REQ-0551, REQ-0553, REQ-0608, REQ-2727 | yes |
| C4103742 | Software Deployment — future dataset downloads but waits to activate | Functional / Commissioning & Deployment | REQ-0551, REQ-0553, REQ-0608, REQ-0680, REQ-2727 | yes |
| C4103743 | Software Deployment — report separates downloaded from installed | Functional / Commissioning & Deployment | C1831389-392, C3546250-253, REQ-2720 | yes |
| C4103744 | Failed Deployment — partial update reports both success and failure | Functional / Commissioning & Deployment | REQ-2720 | yes |
| C4103745 | Topology Deployment — new fares deploy for future activation | Functional / Commissioning & Deployment | REQ-0063 | yes |
| C4103746 | Topology Deployment — changing location changes sellable products | Functional / Commissioning & Deployment | FBD-100383, PSPEC-0014, REQ-2710 | yes |
| C4103747 | Configuration Deployment — coin vault threshold set in TMS applies | Functional / Commissioning & Deployment | REQ-0847 | yes |
| C4103748 | Configuration Deployment — EMV-only mode disables cash | Functional / Commissioning & Deployment | REQ-3294 | yes |
| C4103749 | BOS Interface — CloudFare forces communication with the TVM | Functional / Commissioning & Deployment | FBD-100266 | yes |
| C4103750 | BOS Interface — a secure connection is required for uVNC | Functional / Commissioning & Deployment | FBD-100359 | yes |
| C4104123 | Commissioning — the ticket-collection server address is configured via TMS | Functional / Commissioning & Deployment | — | yes |
| C4104124 | Topology — a device rejects topology intended for another device type | Functional / Commissioning & Deployment | — | yes |
| C4105324 | Smartcards & ABT — buying an ABT card issues the card and receipts | Functional / Smartcards & ABT | — | yes |
| C4105325 | Smartcards & ABT — a card jam during ABT card issuing returns to Home Screen | Functional / Smartcards & ABT | — | yes |
| C4105329 | Smartcards & ABT — yLink ticket selection shows the yLink select-tickets screen | Functional / Smartcards & ABT | — | yes |
| C4105346 | Home Screen — selecting Smartcards opens the Smartcards flow | Functional / Smartcards & ABT | — | yes |
| C4105347 | Home Screen — selecting Buy ABT Card opens the Buy ABT Card flow | Functional / Smartcards & ABT | — | yes |
| C4105350 | Smartcards — Home Screen navigates to the Smartcards screen | Functional / Smartcards & ABT | — | yes |
| C4105351 | Smartcards — Multi Modal Home Screen navigates to the Smartcards screen | Functional / Smartcards & ABT | — | yes |
| C4105356 | Multi-Modal Home — presenting an ABT or top-up card opens Smartcards | Functional / Smartcards & ABT | — | yes |
| C4105357 | Multi-Modal Home — a Discount Smartcard routes to transport-type selection for Discount | Functional / Smartcards & ABT | — | yes |
| C4105358 | Multi-Modal Home — a Free Smartpass routes to transport-type selection for Free Smartpass | Functional / Smartcards & ABT | — | yes |
| C4105359 | Multi-Modal Home (Bus) — Buy ABT Card opens the Buy ABT Card flow | Functional / Smartcards & ABT | — | yes |
| C4105360 | Multi-Modal Home (Bus) — the Smartcard button or presenting a card opens Smartcards | Functional / Smartcards & ABT | — | yes |
| C4105372 | Smartcards — a fully topped-up card shows No more top up and offers a statement | Functional / Smartcards & ABT | — | yes |
| C4105373 | Smartcards — a printed Smartpass statement can only be taken once | Functional / Smartcards & ABT | — | yes |
| C4105374 | Smartcards — a discount card on a Bus TVM offers DepCh1 and yLink ticket selection | Functional / Smartcards & ABT | — | yes |
| C4105375 | Smartcards — a discount card on a Rail TVM offers Rail ticket selection | Functional / Smartcards & ABT | — | yes |
| C4105376 | Smartcards — a free DepCh1 ticket skips payment and prints directly | Functional / Smartcards & ABT | — | yes |
| C4105377 | Smartcards — DepCh1 Rail and Free Smartpass tickets go straight to Ticket Printing | Functional / Smartcards & ABT | — | yes |
| C4105378 | Smartcards — yLink, yLink Rail, 24 Rail and Half-Fare Smartpass tickets go to Payment Process | Functional / Smartcards & ABT | — | yes |
| C4105379 | Smartcards — a new or from-first-use card shows Use before top up and offers a statement | Functional / Smartcards & ABT | — | yes |
| C4105380 | Smartcards — an ABT deny-list top-up can print a receipt | Functional / Smartcards & ABT | — | yes |
| C4105381 | Smartcards — an ABT top-up can print a receipt | Functional / Smartcards & ABT | — | yes |
| C4105382 | Smartcards — a card offering free or half-fare travel routes to Present to Driver | Functional / Smartcards & ABT | — | yes |
| C4105383 | Smartcards — a card write error can end in Faulty smartcard No Update | Functional / Smartcards & ABT | — | yes |
| C4105384 | Smartcards — a card write error can end in Faulty smartcard No Update - Cash | Functional / Smartcards & ABT | — | yes |
| C4105385 | Smartcards — the faulty-smartcard no-update flow returns to Home Screen if the card is already removed | Functional / Smartcards & ABT | — | yes |
| C4105386 | Smartcards — top-up completes and prompts for the card once re-presented after removal | Functional / Smartcards & ABT | — | yes |
| C4105387 | Smartcards — the TVM re-prompts for a card removed earlier before printing a ticket | Functional / Smartcards & ABT | — | yes |
| C4105388 | Smartcards — the customer can opt to take both a top-up receipt and a card receipt | Functional / Smartcards & ABT | — | yes |
| C4105389 | Smartcards — the customer can decline both the top-up receipt and the card receipt | Functional / Smartcards & ABT | — | yes |
| C4103673 | Power-On — a cold boot reaches the Sales home screen | Smoke | REQ-0326 | yes |
| C4103674 | Screensaver Wake — touching the idle screen returns to the Sales home screen | Smoke | REQ-0270, REQ-0277 | yes |
| C4103675 | Ticket Sale — a basic single ticket is issued and printed when paid by cash | Smoke | REQ-0782, REQ-1877 | yes |
| C4103676 | Ticket Sale — a basic single ticket is issued and printed when paid by contactless card | Smoke | FBD-100320, FBD-100353, REQ-0095, REQ-0097 | yes |
| C4103677 | Ticket Collection — a pre-paid ticket is collected and printed | Smoke | FBD-100317, REQ-1576 | yes |
| C4103678 | EMS Access — an engineer opens the EMS/TMS screen and returns to Sales | Smoke | — | yes |
| C4103679 | Comms — the TVM reports to CloudFare and updates Last Communication | Smoke | FBD-100266, FBD-100341 | yes |
| C4103751 | EMS Access — a Technician signs in with a staff-list ID | Non-Functional / EMS & TMS Maintenance | FBD-100266, REQ-2731 | yes |
| C4103752 | EMS Access — only authorised roles can sign into EMS | Non-Functional / EMS & TMS Maintenance | FBD-100266, REQ-2731 | yes |
| C4103753 | Remote Control — remote Out of Service persists across reboot | Non-Functional / EMS & TMS Maintenance | FBD-100266 | yes |
| C4103754 | Remote Control — CloudFare returns the TVM to In Service | Non-Functional / EMS & TMS Maintenance | FBD-100266 | yes |
| C4103755 | Remote Control — remote reboot | Non-Functional / EMS & TMS Maintenance | FBD-100266 | yes |
| C4103756 | Cash Collection — an Engineer prints a Cash Content Report | Non-Functional / EMS & TMS Maintenance | REQ-2720 | yes |
| C4103757 | Cash Collection — prints the Cash Collection Report | Non-Functional / EMS & TMS Maintenance | REQ-2720 | yes |
| C4103758 | Configuration Topology — home location sets the selling operator | Non-Functional / EMS & TMS Maintenance | FBD-100383, PSPEC-0014, REQ-2710 | yes |
| C4103759 | Configuration Topology — destination outside triangle unavailable | Non-Functional / EMS & TMS Maintenance | FBD-100383, PSPEC-0014, REQ-2710 | yes |
| C4103760 | Location Settings — amend home location to another valid location | Non-Functional / EMS & TMS Maintenance | FBD-100383, REQ-2710 | yes |
| C4103761 | Location Settings — an invalid location ID is rejected | Non-Functional / EMS & TMS Maintenance | FBD-100383, REQ-2710 | yes |
| C4103762 | Sub Location — a sub-location must be a valid 3-digit ID | Non-Functional / EMS & TMS Maintenance | C1831422-425, REQ-2710 | yes |
| C4103763 | Ticket Roll Length — an Engineer corrects the roll length | Non-Functional / EMS & TMS Maintenance | REQ-0847, REQ-0848 | yes |
| C4103764 | Transaction Report — prints after multiple transactions | Non-Functional / EMS & TMS Maintenance | REQ-2720 | yes |
| C4103765 | Volume Control — volume adjusts within limits and persists | Non-Functional / EMS & TMS Maintenance | REQ-0511 | yes |
| C4103766 | Screen Brightness — a backlight increase persists into the Sales App | Non-Functional / EMS & TMS Maintenance | REQ-0511 | yes |
| C4103767 | Config Export — Product List reflects the TVM's configuration | Non-Functional / EMS & TMS Maintenance | FBD-100385 | yes |
| C4104118 | Security — hopper door opened without authorisation raises a burglary event | Non-Functional / EMS & TMS Maintenance | — | yes |
| C4104119 | EMS — Battery Saver Mode is maintained during a mains power failure | Non-Functional / EMS & TMS Maintenance | — | yes |
| C4104120 | Cash vault — swapping coin and note vaults on power-up raises no panic event | Non-Functional / EMS & TMS Maintenance | — | yes |
| C4104121 | EMS — exit returns to Sales without General Reboot | Non-Functional / EMS & TMS Maintenance | — | yes |
| C4104891 | Remote Control — remote de-activate | Non-Functional / EMS & TMS Maintenance | FBD-100266 | yes |
| C4104892 | Remote Control — remote re-activate | Non-Functional / EMS & TMS Maintenance | FBD-100266 | yes |
| C4104893 | Cash Collection — prints the Bank Note Collection Report | Non-Functional / EMS & TMS Maintenance | REQ-2720 | yes |
| C4104894 | Cash Collection — prints the Coins Reload Report | Non-Functional / EMS & TMS Maintenance | REQ-2720 | yes |
| C4104895 | Screen Brightness — a backlight decrease persists into the Sales App | Non-Functional / EMS & TMS Maintenance | REQ-0511 | yes |
| C4104896 | Security — 3 failed EMS login attempts raises a burglary event | Non-Functional / EMS & TMS Maintenance | — | yes |
| C4104897 | Security — TVM door opened after 3 failed EMS logins raises a burglary event | Non-Functional / EMS & TMS Maintenance | — | yes |
| C4104898 | Security — TVM door opened without any EMS login attempt raises a burglary event | Non-Functional / EMS & TMS Maintenance | — | yes |
| C4104899 | EMS — exit returns to Sales with General Reboot | Non-Functional / EMS & TMS Maintenance | — | yes |
| C4103768 | Alarmboard — an Engineer tests the siren | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103769 | Alarmboard — an Engineer tests the ticket-tray LED | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103770 | Alarmboard — an Engineer measures the enclosure temperature | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103771 | Alarmboard — an Engineer reads the UPS status | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103772 | Alarmboard — an Engineer runs the door state test | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103773 | Alarmboard — an Engineer tests the speaker | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103774 | Alarmboard — an Engineer tests the ticket-chute fan | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103775 | Printer — an Engineer adjusts the TL80 print alignment | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103776 | Touchscreen — an Engineer runs the touchscreen test | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103777 | Comms Configuration — an Engineer kills the on-screen keyboard | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4104122 | Alarmboard — an Engineer requests the alarmboard firmware version | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4104900 | Alarmboard — an Engineer tests the payment LED | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4104901 | Alarmboard — an Engineer runs the sensor test | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4104902 | Printer — an Engineer adjusts the IML5 print alignment | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103778 | Coin Recycler Hopper — Cash Content Report after replacement | Non-Functional / EMS & TMS Maintenance / Coin Recycler Hopper / Kiosk only | REQ-2720 | yes |
| C4103779 | Coin Recycler Hopper — reloading updates recorded cash content (set to full cassette) | Non-Functional / EMS & TMS Maintenance / Coin Recycler Hopper / Kiosk only | REQ-2720 | yes |
| C4104903 | Coin Recycler Hopper — reloading updates recorded cash content (set to empty then manually corrected) | Non-Functional / EMS & TMS Maintenance / Coin Recycler Hopper / Kiosk only | REQ-2720 | yes |
| C4103780 | Degraded Service — Ingenico card reader failure transitions to amber | Non-Functional / Resilience | — | yes |
| C4103781 | Degraded Service — low printer stock raises an amber status | Non-Functional / Resilience | — | yes |
| C4103782 | Low Change — change unavailable notifies customer and CloudFare | Non-Functional / Resilience | REQ-0339 | yes |
| C4103783 | Low Change — a change voucher is issued on request | Non-Functional / Resilience | REQ-0339 | yes |
| C4103784 | Print Failure — cash is returned when a ticket fails to print | Non-Functional / Resilience | — | yes |
| C4103785 | Mains Power Failure — runs on battery and keeps vaults secure | Non-Functional / Resilience | — | yes |
| C4103786 | Device Lockout — a paper ticket cash sale at the lockout limit goes Out of Service | Non-Functional / Resilience | REQ-2690 | yes |
| C4103787 | Device Lockout — card sale at the lockout limit stays In Service | Non-Functional / Resilience | REQ-2690 | yes |
| C4103788 | Device Lockout — a cancelled cash sale stays In Service | Non-Functional / Resilience | REQ-2690 | yes |
| C4103789 | Heartbeat — idle TVM updates Last Communication every 15 minutes | Non-Functional / Resilience | FBD-100266 | yes |
| C4103790 | Heartbeat — a StaffList message resets Hours Since Last Comms | Non-Functional / Resilience | FBD-100266 | yes |
| C4103791 | Comms Lock — sustained outage drives the TVM to comms-locked OOS | Non-Functional / Resilience | FBD-100359, REQ-2576 | yes |
| C4103792 | Comms Recovery — returns to service and delivers queued sales | Non-Functional / Resilience | FBD-100266, FBD-100359 | yes |
| C4103793 | Comms Reporting — WAN-to-SIM failover reported to CloudFare | Non-Functional / Resilience | FBD-100266, REQ-2399, REQ-2450, REQ-2589, REQ-2741, REQ-2746, TIBU-13485 | yes |
| C4103794 | Screensaver Wake-Up — a screen tap wakes to the mode home | Non-Functional / Resilience | — | yes |
| C4103796 | Multi-Modal Home — selecting Bus shows the Bus home | Non-Functional / Resilience | — | yes |
| C4103797 | Audio Prompts — speech prompts play and cash input gets audible feedback | Non-Functional / Resilience | REQ-0279, REQ-1687 | yes |
| C4103798 | Performance — Quick Select launches from idle within tolerance | Non-Functional / Resilience | — | yes |
| C4103799 | Performance — the TVM accepts at least 98% of valid cash | Non-Functional / Resilience | REQ-0339 | yes |
| C4104904 | Degraded Service — coin selector failure transitions to amber | Non-Functional / Resilience | — | yes |
| C4104905 | Degraded Service — banknote acceptor failure transitions to amber | Non-Functional / Resilience | — | yes |
| C4104906 | Device Lockout — a discounted ticket cash sale at the lockout limit goes Out of Service | Non-Functional / Resilience | REQ-2690 | yes |
| C4104907 | Multi-Modal Home — selecting Rail shows the Rail home | Non-Functional / Resilience | — | yes |
| C4104908 | Audio Prompts — speech prompts play and card input gets audible feedback | Non-Functional / Resilience | REQ-0279, REQ-1687 | yes |
| C4104909 | Audio Prompts — speech prompts play and contactless input gets audible feedback | Non-Functional / Resilience | REQ-0279, REQ-1687 | yes |
| C4104910 | Performance — Buy Other Tickets launches from idle within tolerance | Non-Functional / Resilience | — | yes |
| C4105348 | Home Screen — a machine fault shows the machine-not-available message then Adverts | Non-Functional / Resilience | — | yes |
| C4105349 | Home Screen — Adverts reached from the machine-not-available message returns to Home Screen on tap | Non-Functional / Resilience | — | yes |
| C4105354 | Multi-Modal Home — a machine fault advances to Adverts after timeout | Non-Functional / Resilience | — | yes |
| C4105355 | Multi-Modal Home — Select transport type times out to Adverts | Non-Functional / Resilience | — | yes |
| C4103795 | ZZ_DELETE_REVIEW - Screensaver Wake-Up — a smartcard starts the smartcard flow | Delete | — | yes |
| C4103599 | ZZ_DELETE_REVIEW - Buy a Smartcard — issuing a new journey-based card writes the product and prints a receipt | Delete / Smartcards & ABT | FBD-100250, FBD-100261 | yes |
| C4103600 | ZZ_DELETE_REVIEW - Smartcard Top-up — adding journeys to a Multi-Journey card updates the balance and prints a receipt | Delete / Smartcards & ABT | FBD-100260, FBD-100261 | yes |
| C4103601 | ZZ_DELETE_REVIEW - Smartcard Top-up — a Travelcard or Period Pass top-up adds a period and prints a receipt | Delete / Smartcards & ABT | FBD-100260, FBD-100277 | yes |
| C4103602 | ZZ_DELETE_REVIEW - Smartcard Top-up — top-up amount labels come from the recharge product Display Descriptions | Delete / Smartcards & ABT | FBD-100260 | yes |
| C4103603 | ZZ_DELETE_REVIEW - Smartcard Details — presenting a card displays its details screen | Delete / Smartcards & ABT | FBD-100277 | yes |
| C4103604 | ZZ_DELETE_REVIEW - Mini Statement — a mini-statement prints the card balance after a top-up | Delete / Smartcards & ABT | FBD-100260 | yes |
| C4103605 | ZZ_DELETE_REVIEW - Concession — a yLink smartcard prices a ticket at the yLink concessionary fare | Delete / Smartcards & ABT | FBD-100260, FBD-100293 | yes |
| C4103606 | ZZ_DELETE_REVIEW - Concession — a 24+ smartcard prices a ticket at the 24+ discounted fare | Delete / Smartcards & ABT | FBD-100236, FBD-100260 | yes |
| C4103607 | ZZ_DELETE_REVIEW - Concession — a half-fare Smartpass prices a single at half fare | Delete / Smartcards & ABT | FBD-100250 | yes |
| C4103608 | ZZ_DELETE_REVIEW - Concession — a free-concession Smartpass issues a free pass ticket | Delete / Smartcards & ABT | FBD-100250 | yes |
| C4103609 | ZZ_DELETE_REVIEW - Concession — funded-disability Smartpasses are accepted for concessionary travel | Delete / Smartcards & ABT | FBD-100250 | yes |
| C4103610 | ZZ_DELETE_REVIEW - Staff Pass — a staff smartcard issues a staff free-travel ticket | Delete / Smartcards & ABT | FBD-100250 | yes |
| C4103611 | ZZ_DELETE_REVIEW - Invalid Smartcard — a faulty or unreadable card is rejected | Delete / Smartcards & ABT | FBD-100250 | yes |
| C4103612 | ZZ_DELETE_REVIEW - Invalid Smartcard — an expired card cannot be topped up | Delete / Smartcards & ABT | FBD-100250 | yes |
| C4103613 | ZZ_DELETE_REVIEW - Invalid Smartcard — presenting two cards simultaneously is rejected | Delete / Smartcards & ABT | FBD-100250 | yes |
| C4103614 | ZZ_DELETE_REVIEW - Invalid Smartcard — re-presenting a card within the passback period is rejected | Delete / Smartcards & ABT | FBD-100250 | yes |
| C4103615 | ZZ_DELETE_REVIEW - Smartcard Top-up — presenting a different card mid top-up aborts the top-up | Delete / Smartcards & ABT | FBD-100250 | yes |
| C4103616 | ZZ_DELETE_REVIEW - Smartcard removed early — removing the card during payment cancels the transaction | Delete / Smartcards & ABT | FBD-100250 | yes |
| C4103617 | ZZ_DELETE_REVIEW - ABT — issuing an ABT smartcard registers a personalised card | Delete / Smartcards & ABT | FBD-100236 | yes |
| C4103618 | ZZ_DELETE_REVIEW - ABT — a card with the ABT application but no ABT Tracking application is rejected | Delete / Smartcards & ABT | FBD-100236 | yes |
| C4103619 | ZZ_DELETE_REVIEW - ABT — an ABT product top-up posts a transaction to the back office | Delete / Smartcards & ABT | FBD-100236, FBD-100260 | yes |
| C4103733 | ZZ_DELETE_REVIEW - Mini Statement — Multi-Journey smartcard after a top-up | Delete / Mini Statement | FBD-100261 | yes |
| C4103734 | ZZ_DELETE_REVIEW - Mini Statement — Multi-Journey smartcard after a validation | Delete / Mini Statement | FBD-100261 | yes |
| C4103735 | ZZ_DELETE_REVIEW - Mini Statement — Period Pass smartcard after a top-up | Delete / Mini Statement | FBD-100261 | yes |
| C4103736 | ZZ_DELETE_REVIEW - Mini Statement — DayLink smartcard after a top-up | Delete / Mini Statement | FBD-100261 | yes |
| C4103737 | ZZ_DELETE_REVIEW - Mini Statement — the printed layout matches the HMI | Delete / Mini Statement | FBD-100261 | yes |
