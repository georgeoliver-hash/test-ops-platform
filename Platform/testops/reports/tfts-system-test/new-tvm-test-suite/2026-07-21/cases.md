# Cases — TFTS - System Test / **NEW** TVM Test Suite

- Generated: 2026-07-21T15:37:34.757353+00:00
- Total cases: 201

| Case | Title | Section | Linked refs | Has steps |
|---|---|---|---|---|
| C4103599 | ZZ_DELETE_REVIEW - Buy a Smartcard — issuing a new journey-based card writes the product and prints a receipt | Functional / Smartcards & ABT | FBD-100250, FBD-100261 | yes |
| C4103600 | ZZ_DELETE_REVIEW - Smartcard Top-up — adding journeys to a Multi-Journey card updates the balance and prints a receipt | Functional / Smartcards & ABT | FBD-100260, FBD-100261 | yes |
| C4103601 | ZZ_DELETE_REVIEW - Smartcard Top-up — a Travelcard or Period Pass top-up adds a period and prints a receipt | Functional / Smartcards & ABT | FBD-100260, FBD-100277 | yes |
| C4103602 | ZZ_DELETE_REVIEW - Smartcard Top-up — top-up amount labels come from the recharge product Display Descriptions | Functional / Smartcards & ABT | FBD-100260 | yes |
| C4103603 | ZZ_DELETE_REVIEW - Smartcard Details — presenting a card displays its details screen | Functional / Smartcards & ABT | FBD-100277 | yes |
| C4103604 | ZZ_DELETE_REVIEW - Mini Statement — a mini-statement prints the card balance after a top-up | Functional / Smartcards & ABT | FBD-100260 | yes |
| C4103605 | ZZ_DELETE_REVIEW - Concession — a yLink smartcard prices a ticket at the yLink concessionary fare | Functional / Smartcards & ABT | FBD-100260, FBD-100293 | yes |
| C4103606 | ZZ_DELETE_REVIEW - Concession — a 24+ smartcard prices a ticket at the 24+ discounted fare | Functional / Smartcards & ABT | FBD-100236, FBD-100260 | yes |
| C4103607 | ZZ_DELETE_REVIEW - Concession — a half-fare Smartpass prices a single at half fare | Functional / Smartcards & ABT | FBD-100250 | yes |
| C4103608 | ZZ_DELETE_REVIEW - Concession — a free-concession Smartpass issues a free pass ticket | Functional / Smartcards & ABT | FBD-100250 | yes |
| C4103609 | ZZ_DELETE_REVIEW - Concession — funded-disability Smartpasses are accepted for concessionary travel | Functional / Smartcards & ABT | FBD-100250 | yes |
| C4103610 | ZZ_DELETE_REVIEW - Staff Pass — a staff smartcard issues a staff free-travel ticket | Functional / Smartcards & ABT | FBD-100250 | yes |
| C4103611 | ZZ_DELETE_REVIEW - Invalid Smartcard — a faulty or unreadable card is rejected | Functional / Smartcards & ABT | FBD-100250 | yes |
| C4103612 | ZZ_DELETE_REVIEW - Invalid Smartcard — an expired card cannot be topped up | Functional / Smartcards & ABT | FBD-100250 | yes |
| C4103613 | ZZ_DELETE_REVIEW - Invalid Smartcard — presenting two cards simultaneously is rejected | Functional / Smartcards & ABT | FBD-100250 | yes |
| C4103614 | ZZ_DELETE_REVIEW - Invalid Smartcard — re-presenting a card within the passback period is rejected | Functional / Smartcards & ABT | FBD-100250 | yes |
| C4103615 | ZZ_DELETE_REVIEW - Smartcard Top-up — presenting a different card mid top-up aborts the top-up | Functional / Smartcards & ABT | FBD-100250 | yes |
| C4103616 | ZZ_DELETE_REVIEW - Smartcard removed early — removing the card during payment cancels the transaction | Functional / Smartcards & ABT | FBD-100250 | yes |
| C4103617 | ZZ_DELETE_REVIEW - ABT — issuing an ABT smartcard registers a personalised card | Functional / Smartcards & ABT | FBD-100236 | yes |
| C4103618 | ZZ_DELETE_REVIEW - ABT — a card with the ABT application but no ABT Tracking application is rejected | Functional / Smartcards & ABT | FBD-100236 | yes |
| C4103619 | ZZ_DELETE_REVIEW - ABT — an ABT product top-up posts a transaction to the back office | Functional / Smartcards & ABT | FBD-100236, FBD-100260 | yes |
| C4103620 | Ticket Collection — a valid booking reference collects and prints the pre-paid ticket | Functional / Barcode Redemption | FBD-100317, FBD-100483 | yes |
| C4103621 | Ticket Collection — the booking reference is validated against the back office | Functional / Barcode Redemption | FBD-100483 | yes |
| C4103622 | Ticket Collection — a successful redemption emits a Barcode Redemption event | Functional / Barcode Redemption | FBD-100483 | yes |
| C4103623 | Ticket Collection — an offline redemption still prints and queues an offline event | Functional / Barcode Redemption | FBD-100483 | yes |
| C4103624 | Ticket Collection — a redemption above the barcode ceiling limit cannot validate offline | Functional / Barcode Redemption | FBD-100317, FBD-100483 | yes |
| C4103625 | Booking Reference — an invalid booking reference is rejected | Functional / Barcode Redemption | FBD-100483 | yes |
| C4103626 | Booking Reference — a malformed reference entry is rejected before submission | Functional / Barcode Redemption | FBD-100483 | yes |
| C4103627 | Ticket Collection — a collection against a legacy stage resolves the legacy stage name | Functional / Barcode Redemption | FBD-100483 | yes |
| C4103628 | Single-Use only — a multi-use ticket's Collect Ticket Code is rejected | Functional / Barcode Redemption | FBD-100167, FBD-100317 | yes |
| C4103629 | Single-Use only — collection accepts a booking reference and not a scanned barcode | Functional / Barcode Redemption | FBD-100317, FBD-100483 | yes |
| C4103630 | Ticket Collection — a business error shows an error screen and returns to Home after the timeout | Functional / Barcode Redemption | FBD-100483 | yes |
| C4103631 | Ticket Collection — repeated server errors retry and then fall back | Functional / Barcode Redemption | FBD-100483 | yes |
| C4103632 | Ticket Collection — an already-redeemed booking reference is rejected as used | Functional / Barcode Redemption | FBD-100483 | yes |
| C4103633 | Barcode Ticket Format — a collected ticket prints in the barcode ticket layout | Functional / Barcode Redemption | FBD-100167, FBD-100318 | yes |
| C4103634 | Coins — valid coins pay for a transaction and change is returned | Functional / Payments - Cash | — | yes |
| C4103635 | Coins — a valid coin is accepted after an invalid coin is inserted | Functional / Payments - Cash | — | yes |
| C4103636 | Coins — coins inserted during the "More Time Required" screen complete the payment | Functional / Payments - Cash | — | yes |
| C4103637 | Coins — out-of-circulation and sub-value coins are rejected | Functional / Payments - Cash | — | yes |
| C4103638 | Coins — foreign coins are rejected | Functional / Payments - Cash | — | yes |
| C4103639 | Banknotes — a valid banknote in any orientation pays for a transaction | Functional / Payments - Cash | — | yes |
| C4103640 | Banknotes — withdrawn paper notes are rejected | Functional / Payments - Cash | — | yes |
| C4103641 | Banknotes — a Scottish banknote is accepted as valid sterling | Functional / Payments - Cash | — | yes |
| C4103642 | Cash — mixed coins and banknotes pay for a transaction | Functional / Payments - Cash | — | yes |
| C4103643 | Cash — overpayment returns the correct change | Functional / Payments - Cash | — | yes |
| C4103644 | Cash — pressing Back returns the inserted cash before the escrow limit | Functional / Payments - Cash | — | yes |
| C4103645 | Cash — pressing Cancel returns the inserted cash after the escrow limit | Functional / Payments - Cash | — | yes |
| C4103646 | Cash — the coin escrow limit stops further coins being accepted | Functional / Payments - Cash | — | yes |
| C4103647 | Cash — the banknote escrow limit stops further notes being accepted | Functional / Payments - Cash | — | yes |
| C4103648 | Cash — a print failure returns the inserted cash | Functional / Payments - Cash | — | yes |
| C4103649 | Cash — a completed cash sale posts audit data to CloudFare | Functional / Payments - Cash | FBD-100341 | yes |
| C4103650 | BNR — a note left in the exit beak leaves the recycler non-functional | Functional / Payments - Cash / Note Recycler & Change (Astreo only) | — | yes |
| C4103651 | BNR — a rejected invalid note left hanging from the exit beak leaves the recycler non-functional | Functional / Payments - Cash / Note Recycler & Change (Astreo only) | — | yes |
| C4103652 | BNA — a note-acceptor error makes note payment unavailable | Functional / Payments - Cash / Note Recycler & Change (Astreo only) | — | yes |
| C4103653 | Change — insufficient change prints a Refuse Change Voucher for the balance | Functional / Payments - Cash / Note Recycler & Change (Astreo only) | FBD-100341 | yes |
| C4103654 | Change — a Refuse Change Voucher is printed when cash is inserted during the "More Time Required" screen | Functional / Payments - Cash / Note Recycler & Change (Astreo only) | — | yes |
| C4103655 | Coin recycler — a Cash Content Report is produced after a hopper is replaced | Functional / Payments - Cash / Coin Recycler Hopper (Kiosk only) | — | yes |
| C4103656 | Coin recycler — replenishing a hopper restores change-giving from a low-change state | Functional / Payments - Cash / Coin Recycler Hopper (Kiosk only) | — | yes |
| C4103657 | Chip & PIN — a valid card completes payment and prints the ticket | Functional / Payments - EMV & Contactless | FBD-100320 | yes |
| C4103658 | Chip & PIN — a payment with no PIN entered does not complete | Functional / Payments - EMV & Contactless | FBD-100320 | yes |
| C4103659 | Chip & PIN — American Express and Diners cards are accepted | Functional / Payments - EMV & Contactless | FBD-100320 | yes |
| C4103660 | Chip & PIN — transaction value limits are enforced | Functional / Payments - EMV & Contactless | FBD-100320 | yes |
| C4103661 | Contactless — a tap at or below the contactless limit is approved | Functional / Payments - EMV & Contactless | FBD-100320 | yes |
| C4103662 | Contactless — a tap above the contactless limit falls back to Chip & PIN | Functional / Payments - EMV & Contactless | FBD-100320 | yes |
| C4103663 | Contactless — a mobile wallet payment is approved | Functional / Payments - EMV & Contactless | FBD-100320 | yes |
| C4103664 | EMV — a declined card offers retry or cancel | Functional / Payments - EMV & Contactless | FBD-100320 | yes |
| C4103665 | EMV — cancelling at the pinpad ends the payment without a ticket | Functional / Payments - EMV & Contactless | FBD-100320 | yes |
| C4103666 | EMV — a payment that times out is not completed | Functional / Payments - EMV & Contactless | FBD-100320 | yes |
| C4103667 | EMV — a print failure voids the card payment | Functional / Payments - EMV & Contactless | FBD-100320 | yes |
| C4103668 | EMV — an expired or blocked card is rejected | Functional / Payments - EMV & Contactless | FBD-100320 | yes |
| C4103669 | EMV — the PAN is masked on the receipt and back-office systems | Functional / Payments - EMV & Contactless | FBD-100320 | yes |
| C4103670 | EMV — selecting card after a cash transaction returns any inserted cash and pays by card | Functional / Payments - EMV & Contactless | FBD-100320 | yes |
| C4103671 | EMV — a completed card sale posts audit data to CloudFare under the TVM terminal ID | Functional / Payments - EMV & Contactless | FBD-100320, FBD-100341 | yes |
| C4103672 | EMV — a card payment receipt is printed when selected | Functional / Payments - EMV & Contactless | FBD-100320 | yes |
| C4103680 | Ticket Issue — a selected product is issued and printed | Functional / Sales - Tickets / Ticket Issue | FBD-100207, FBD-100336 | yes |
| C4103681 | Ticket Issue — Adult single ticket | Functional / Sales - Tickets / Ticket Issue | FBD-100207, FBD-100336 | yes |
| C4103682 | Ticket Issue — Child single ticket | Functional / Sales - Tickets / Ticket Issue | FBD-100207, FBD-100336 | yes |
| C4103683 | Ticket Issue — Family and Friends day ticket | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4103684 | Ticket Issue — Family and Friends additional child | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4103685 | Ticket Issue — Popular tickets shortcut | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4103686 | Ticket Issue — Evening ticket | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4103687 | Ticket Issue — Day and Day Return tickets | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4103688 | Ticket Issue — Summer Bus Rambler ticket | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4103689 | Ticket Issue — concessionary half-fare single | Functional / Sales - Tickets / Ticket Issue | FBD-100207, FBD-100336 | yes |
| C4103690 | Ticket Issue — buy a product in a different language | Functional / Sales - Tickets / Ticket Issue | FBD-100336 | yes |
| C4103691 | Ticket Issue — issued ticket carries a single-use barcode | Functional / Sales - Tickets / Ticket Issue | FBD-100167, FBD-100317 | yes |
| C4103692 | Ticket Issue — a single ticket for multiple passengers carries no barcode | Functional / Sales - Tickets / Ticket Issue | FBD-100167 | yes |
| C4103693 | Ticket Issue — the sale posts an audit record to the back office | Functional / Sales - Tickets / Ticket Issue | FBD-100341 | yes |
| C4103694 | 3-Day — a 3-day ticket is issued | Functional / Sales - Tickets / Advance & 3-Day | FBD-100336 | yes |
| C4103695 | 3-Day — the ticket is valid across three consecutive days | Functional / Sales - Tickets / Advance & 3-Day | FBD-100336 | yes |
| C4103696 | NI Rail — Adult single between two stations | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100207, FBD-100450 | yes |
| C4103697 | NI Rail — Day Return, Weekly and Monthly products | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4103698 | NI Rail — 3-Day Select ticket | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100167, FBD-100450 | yes |
| C4103699 | Cross-Border — Adult single | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100207, FBD-100450 | yes |
| C4103700 | Cross-Border — Return, Monthly and 1-Month-Return products | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4103701 | Cross-Border — 1st Class ticket | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4103702 | NI Rail — concessionary single | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450 | yes |
| C4103703 | NI Rail — grouped-station area name prints on a cross-border ticket | Functional / Sales - Tickets / Rail & Cross-Border (Kiosk) | FBD-100450, FBD-100515 | yes |
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
| C4103733 | ZZ_DELETE_REVIEW - Mini Statement — Multi-Journey smartcard after a top-up | Functional / Sales - Tickets / Mini Statement | FBD-100261 | yes |
| C4103734 | ZZ_DELETE_REVIEW - Mini Statement — Multi-Journey smartcard after a validation | Functional / Sales - Tickets / Mini Statement | FBD-100261 | yes |
| C4103735 | ZZ_DELETE_REVIEW - Mini Statement — Period Pass smartcard after a top-up | Functional / Sales - Tickets / Mini Statement | FBD-100261 | yes |
| C4103736 | ZZ_DELETE_REVIEW - Mini Statement — DayLink smartcard after a top-up | Functional / Sales - Tickets / Mini Statement | FBD-100261 | yes |
| C4103737 | ZZ_DELETE_REVIEW - Mini Statement — the printed layout matches the HMI | Functional / Sales - Tickets / Mini Statement | FBD-100261 | yes |
| C4103738 | Commissioning — a TVM downloads its config and credentials by serial | Functional / Commissioning & Deployment | FBD-100320 | yes |
| C4103739 | Commissioning — credentials stay within the TVM Terminal Group | Functional / Commissioning & Deployment | FBD-100320 | yes |
| C4103740 | Commissioning — topology makes home-location products sellable | Functional / Commissioning & Deployment | FBD-100296 | yes |
| C4103741 | Software Deployment — immediate dataset installs and updates versions | Functional / Commissioning & Deployment | FBD-100385 | yes |
| C4103742 | Software Deployment — future dataset downloads but waits to activate | Functional / Commissioning & Deployment | FBD-100385 | yes |
| C4103743 | Software Deployment — report separates downloaded from installed | Functional / Commissioning & Deployment | FBD-100385 | yes |
| C4103744 | Failed Deployment — partial update reports both success and failure | Functional / Commissioning & Deployment | FBD-100385 | yes |
| C4103745 | Topology Deployment — new fares deploy for future activation | Functional / Commissioning & Deployment | FBD-100296, FBD-100385 | yes |
| C4103746 | Topology Deployment — changing location changes sellable products | Functional / Commissioning & Deployment | FBD-100296 | yes |
| C4103747 | Configuration Deployment — coin vault threshold set in TMS applies | Functional / Commissioning & Deployment | FBD-100385 | yes |
| C4103748 | Configuration Deployment — EMV-only mode disables cash | Functional / Commissioning & Deployment | FBD-100385 | yes |
| C4103749 | BOS Interface — CloudFare forces communication with the TVM | Functional / Commissioning & Deployment | FBD-100266 | yes |
| C4103750 | BOS Interface — a secure connection is required for uVNC | Functional / Commissioning & Deployment | FBD-100359 | yes |
| C4103673 | Power-On — a cold boot reaches the Sales home screen | Smoke | REQ-0326 | yes |
| C4103674 | Screensaver Wake — touching the idle screen returns to the Sales home screen | Smoke | REQ-0270, REQ-0277 | yes |
| C4103675 | Ticket Sale — a basic single ticket is issued and printed when paid by cash | Smoke | REQ-0782, REQ-1877 | yes |
| C4103676 | Ticket Sale — a basic single ticket is issued and printed when paid by contactless card | Smoke | FBD-100320, FBD-100353, REQ-0095, REQ-0097 | yes |
| C4103677 | Ticket Collection — a pre-paid ticket is collected and printed | Smoke | FBD-100317, REQ-1576 | yes |
| C4103678 | EMS Access — an engineer opens the EMS/TMS screen and returns to Sales | Smoke | — | yes |
| C4103679 | Comms — the TVM reports to CloudFare and updates Last Communication | Smoke | FBD-100266, FBD-100341 | yes |
| C4103751 | EMS Access — a Technician signs in with a staff-list ID | Non-Functional / EMS & TMS Maintenance | FBD-100266 | yes |
| C4103752 | EMS Access — only authorised roles can sign into EMS | Non-Functional / EMS & TMS Maintenance | FBD-100266 | yes |
| C4103753 | Remote Control — remote Out of Service persists across reboot | Non-Functional / EMS & TMS Maintenance | FBD-100266 | yes |
| C4103754 | Remote Control — CloudFare returns the TVM to In Service | Non-Functional / EMS & TMS Maintenance | FBD-100266 | yes |
| C4103755 | Remote Control — remote reboot, de-activate and re-activate | Non-Functional / EMS & TMS Maintenance | FBD-100266 | yes |
| C4103756 | Cash Collection — an Engineer prints a Cash Content Report | Non-Functional / EMS & TMS Maintenance | — | yes |
| C4103757 | Cash Collection — prints collection and reload reports | Non-Functional / EMS & TMS Maintenance | — | yes |
| C4103758 | Configuration Topology — home location sets the selling operator | Non-Functional / EMS & TMS Maintenance | FBD-100296 | yes |
| C4103759 | Configuration Topology — destination outside triangle unavailable | Non-Functional / EMS & TMS Maintenance | FBD-100296 | yes |
| C4103760 | Location Settings — amend home location to another valid location | Non-Functional / EMS & TMS Maintenance | FBD-100296 | yes |
| C4103761 | Location Settings — an invalid location ID is rejected | Non-Functional / EMS & TMS Maintenance | FBD-100296 | yes |
| C4103762 | Sub Location — a sub-location must be a valid 3-digit ID | Non-Functional / EMS & TMS Maintenance | FBD-100296 | yes |
| C4103763 | Ticket Roll Length — an Engineer corrects the roll length | Non-Functional / EMS & TMS Maintenance | — | yes |
| C4103764 | Transaction Report — prints after multiple transactions | Non-Functional / EMS & TMS Maintenance | — | yes |
| C4103765 | Volume Control — volume adjusts within limits and persists | Non-Functional / EMS & TMS Maintenance | — | yes |
| C4103766 | Screen Brightness — backlight change persists into the Sales App | Non-Functional / EMS & TMS Maintenance | — | yes |
| C4103767 | Config Export — Product List reflects the TVM's configuration | Non-Functional / EMS & TMS Maintenance | FBD-100385 | yes |
| C4103768 | Alarmboard — an Engineer tests the siren | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103769 | Alarmboard — an Engineer tests the status LEDs | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103770 | Alarmboard — an Engineer measures the enclosure temperature | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103771 | Alarmboard — an Engineer reads the UPS status | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103772 | Alarmboard — an Engineer runs the door and sensor tests | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103773 | Alarmboard — an Engineer tests the speaker | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103774 | Alarmboard — an Engineer tests the ticket-chute fan | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103775 | TL80 Printer — an Engineer adjusts the print alignment | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103776 | Touchscreen — an Engineer runs the touchscreen test | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103777 | Comms Configuration — an Engineer kills the on-screen keyboard | Non-Functional / EMS & TMS Maintenance / Alarmboard & Enclosure / Kiosk only | — | yes |
| C4103778 | Coin Recycler Hopper — Cash Content Report after replacement | Non-Functional / EMS & TMS Maintenance / Coin Recycler Hopper / Kiosk only | — | yes |
| C4103779 | Coin Recycler Hopper — reloading updates recorded cash content | Non-Functional / EMS & TMS Maintenance / Coin Recycler Hopper / Kiosk only | — | yes |
| C4103780 | Degraded Service — payment hardware failure transitions to amber | Non-Functional / Resilience | — | yes |
| C4103781 | Degraded Service — low printer stock raises an amber status | Non-Functional / Resilience | — | yes |
| C4103782 | Low Change — change unavailable notifies customer and CloudFare | Non-Functional / Resilience | — | yes |
| C4103783 | Low Change — a change voucher is issued on request | Non-Functional / Resilience | — | yes |
| C4103784 | Print Failure — cash is returned when a ticket fails to print | Non-Functional / Resilience | — | yes |
| C4103785 | Mains Power Failure — runs on battery and keeps vaults secure | Non-Functional / Resilience | — | yes |
| C4103786 | Device Lockout — cash sale at the lockout limit goes Out of Service | Non-Functional / Resilience | — | yes |
| C4103787 | Device Lockout — card sale at the lockout limit stays In Service | Non-Functional / Resilience | — | yes |
| C4103788 | Device Lockout — a cancelled cash sale stays In Service | Non-Functional / Resilience | — | yes |
| C4103789 | Heartbeat — idle TVM updates Last Communication every 15 minutes | Non-Functional / Resilience | FBD-100266 | yes |
| C4103790 | Heartbeat — a StaffList message resets Hours Since Last Comms | Non-Functional / Resilience | FBD-100266 | yes |
| C4103791 | Comms Lock — sustained outage drives the TVM to comms-locked OOS | Non-Functional / Resilience | FBD-100359 | yes |
| C4103792 | Comms Recovery — returns to service and delivers queued sales | Non-Functional / Resilience | FBD-100266, FBD-100359 | yes |
| C4103793 | Comms Reporting — WAN-to-SIM failover reported to CloudFare | Non-Functional / Resilience | FBD-100266 | yes |
| C4103794 | Screensaver Wake-Up — a screen tap wakes to the mode home | Non-Functional / Resilience | — | yes |
| C4103795 | ZZ_DELETE_REVIEW - Screensaver Wake-Up — a smartcard starts the smartcard flow | Non-Functional / Resilience | — | yes |
| C4103796 | Multi-Modal Home — selecting Bus or Rail shows the right home | Non-Functional / Resilience | — | yes |
| C4103797 | Audio Prompts — speech prompts and payment feedback play | Non-Functional / Resilience | — | yes |
| C4103798 | Performance — workflows launch from idle within tolerance | Non-Functional / Resilience | — | yes |
| C4103799 | Performance — the TVM accepts at least 98% of valid cash | Non-Functional / Resilience | — | yes |
