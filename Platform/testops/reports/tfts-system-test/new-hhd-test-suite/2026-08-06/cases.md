# Cases — TFTS - System Test / **NEW** HHD Test Suite

- Generated: 2026-08-06T09:52:48.150139+00:00
- Total cases: 482

| Case | Title | Section | Linked refs | Has steps |
|---|---|---|---|---|
| C4104005 | Smoke — the operator signs on and reaches the main menu | Smoke | REQ-0050 | yes |
| C4104006 | Smoke — a paper ticket is sold and paid by cash | Smoke | REQ-0163 | yes |
| C4104007 | Smoke — a paper ticket is sold and paid by card on the M020 | Smoke | FBD-100320, REQ-0163 | yes |
| C4104008 | Smoke — a just-sold ticket is annulled | Smoke | REQ-0300 | yes |
| C4104009 | Smoke — a valid smartcard validates successfully | Smoke | REQ-0871 | yes |
| C4104010 | Smoke — the operator signs off and prints a waybill | Smoke | REQ-0329 | yes |
| C4103800 | M020 Pairing — Bluetooth pairing completes and enables card payment | Functional / Card Payment (M020) | FBD-100320 | yes |
| C4103801 | M020 Commissioning — TID and TK download from TMS by serial after pairing | Functional / Card Payment (M020) | FBD-100320 | yes |
| C4103802 | Terminal Group — the M020 settles under the "HHD Retailing" group | Functional / Card Payment (M020) | FBD-100320 | yes |
| C4103803 | Payment Device Swap — a replacement M020 keeps the existing TID and TK | Functional / Card Payment (M020) | FBD-100320 | yes |
| C4103804 | Chip and PIN — a Visa credit sale completes and prints a ticket | Functional / Card Payment (M020) | FBD-100183, FBD-100320, REQ-0163, REQ-1384, REQ-1488, REQ-1489, REQ-1491, REQ-1514, REQ-1516, REQ-1630, REQ-1722, REQ-1723 | yes |
| C4103805 | Chip and PIN — a Mastercard debit sale completes | Functional / Card Payment (M020) | FBD-100183, FBD-100320, REQ-0163, REQ-1384, REQ-1488, REQ-1489, REQ-1491, REQ-1514, REQ-1630, REQ-1722 | yes |
| C4103806 | Contactless — a Visa contactless sale completes | Functional / Card Payment (M020) | FBD-100183, FBD-100320, REQ-0163, REQ-1384, REQ-1488, REQ-1489, REQ-1491, REQ-1514, REQ-1516, REQ-1630, REQ-1722, REQ-1723, REQ-1854, REQ-2519 | yes |
| C4103807 | Contactless — a mobile wallet sale completes | Functional / Card Payment (M020) | FBD-100183, FBD-100320 | yes |
| C4103808 | Card Declined — a declined card does not issue a ticket | Functional / Card Payment (M020) | FBD-100183, FBD-100320, REQ-0163, REQ-0890, REQ-1384, REQ-1488, REQ-1489, REQ-1491, REQ-1514, REQ-1630, REQ-1722 | yes |
| C4103809 | Card Declined — an expired card is rejected | Functional / Card Payment (M020) | FBD-100183, FBD-100320 | yes |
| C4103810 | Card Declined — a blocked card is rejected | Functional / Card Payment (M020) | FBD-100183, FBD-100320 | yes |
| C4103811 | EMV Timeout — no card presented within the timeout ends the sale | Functional / Card Payment (M020) | FBD-100183, FBD-100320 | yes |
| C4103812 | Cancel EMV — the Operator cancels before the card is presented | Functional / Card Payment (M020) | FBD-100183, FBD-100320 | yes |
| C4103813 | Cancel EMV — the sale cannot be cancelled after the card is presented | Functional / Card Payment (M020) | FBD-100183, FBD-100320 | yes |
| C4103814 | EMV Unavailable — payment resumes after communications re-establish | Functional / Card Payment (M020) | FBD-100320 | yes |
| C4103815 | PAN Masking — the printed ticket shows only a masked PAN | Functional / Card Payment (M020) | FBD-100658, REQ-1722, REQ-1723 | yes |
| C4103816 | PRN — a card sale prints a PRN in the H + IMEI + ticks + operator format | Functional / Card Payment (M020) | FBD-100373 | yes |
| C4103817 | Payment Device On Charge — a card sale completes while the M020 is on charge | Functional / Card Payment (M020) | FBD-100183, FBD-100320 | yes |
| C4104663 | Chip and PIN — a Visa debit sale completes and prints a ticket | Functional / Card Payment (M020) | FBD-100183, FBD-100320, REQ-0163, REQ-1384, REQ-1488, REQ-1489, REQ-1491, REQ-1514, REQ-1516, REQ-1630, REQ-1722, REQ-1723 | yes |
| C4104665 | Chip and PIN — a Mastercard credit sale completes and prints a ticket | Functional / Card Payment (M020) | FBD-100183, FBD-100320, REQ-0163, REQ-1384, REQ-1488, REQ-1489, REQ-1491, REQ-1514, REQ-1516, REQ-1630, REQ-1722, REQ-1723 | yes |
| C4104667 | Chip and PIN — a Maestro sale completes and prints a ticket | Functional / Card Payment (M020) | FBD-100183, FBD-100320, REQ-0163, REQ-1384, REQ-1488, REQ-1489, REQ-1491, REQ-1514, REQ-1516, REQ-1630, REQ-1722, REQ-1723 | yes |
| C4104668 | Contactless — a Mastercard contactless sale completes | Functional / Card Payment (M020) | FBD-100183, FBD-100320, REQ-0163, REQ-1384, REQ-1488, REQ-1489, REQ-1491, REQ-1514, REQ-1516, REQ-1630, REQ-1722, REQ-1723, REQ-1854, REQ-2519 | yes |
| C4104669 | Card Declined — an unsupported-scheme card is declined without a PIN prompt | Functional / Card Payment (M020) | FBD-100183, FBD-100320, REQ-0163, REQ-0890, REQ-1384, REQ-1488, REQ-1489, REQ-1491, REQ-1514, REQ-1630, REQ-1722 | yes |
| C4105249 | Card Payment — contactless over £45 redirects to Chip & PIN | Functional / Card Payment (M020) | — | yes |
| C4105250 | Card Payment — a swiped Chip & PIN-capable card is redirected to Chip & PIN | Functional / Card Payment (M020) | — | yes |
| C4105251 | Card Payment — a swiped card without Chip & PIN goes to Confirm Amount | Functional / Card Payment (M020) | — | yes |
| C4105252 | Card Payment — customer cancels the transaction before payment | Functional / Card Payment (M020) | — | yes |
| C4105253 | Card Payment — repeated PIN entry failures decline the transaction | Functional / Card Payment (M020) | — | yes |
| C4105254 | Card Payment — a signature mismatch voids the transaction | Functional / Card Payment (M020) | — | yes |
| C4105255 | Card Reader — a successful reconnect proceeds to the Card Payment flow | Functional / Card Payment (M020) | — | yes |
| C4105256 | Card Reader — a failed reconnect with tries remaining retries Connecting | Functional / Card Payment (M020) | — | yes |
| C4105257 | Card Reader — exhausted reconnect retries prompts Contact Supervisor | Functional / Card Payment (M020) | — | yes |
| C4105262 | Card Payment Receipt — declining the receipt returns to Sales | Functional / Card Payment (M020) | — | yes |
| C4105263 | Card Payment Print Failure — continuing without printing returns to Sales | Functional / Card Payment (M020) | — | yes |
| C4105301 | Payment Device Status — reporting a faulty device notifies the back office and removes card payment | Functional / Card Payment (M020) | — | yes |
| C4103818 | Reference-Number Station — a card sale is keyed to the station reference number (NIR only) | Functional / Card Payment (M020) / Reference-Number Stations | FBD-100383 | yes |
| C4103819 | Reference-Number Station — the sale settles while the payment device is on charge (NIR only) | Functional / Card Payment (M020) / Reference-Number Stations | FBD-100383 | yes |
| C4103820 | Validate — an Adult iLink is accepted for a boarding within its zone | Functional / Smartcards & ABT | FBD-100250, FBD-100389, REQ-0862, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0879, REQ-0885, REQ-0912, REQ-0913, REQ-0914, REQ-0915, REQ-0919, REQ-0927, REQ-3473, REQ-3478 | yes |
| C4103821 | Validate — an Adult iLink is rejected for a boarding outside its zone | Functional / Smartcards & ABT | FBD-100250, FBD-100389 | yes |
| C4103822 | Validate — a Senior Smartpass concession is accepted | Functional / Smartcards & ABT | FBD-100250, REQ-0840, REQ-0841, REQ-0842, REQ-0843, REQ-0844, REQ-0845, REQ-0851, REQ-0852, REQ-0853 | yes |
| C4103823 | Validate — an expired Smartpass is rejected | Functional / Smartcards & ABT | FBD-100250, FBD-100658 | yes |
| C4103824 | Validate — a hotlisted Smartpass is rejected | Functional / Smartcards & ABT | FBD-100250, FBD-100658 | yes |
| C4103825 | Validate — an unreadable smartcard is rejected | Functional / Smartcards & ABT | FBD-100250 | yes |
| C4103826 | Validate — a Staff Pass is accepted | Functional / Smartcards & ABT | FBD-100250, REQ-0855, REQ-0856, REQ-2025, REQ-2026 | yes |
| C4103827 | Validate — a passback re-tap within the window is rejected | Functional / Smartcards & ABT | FBD-100271, FBD-100658 | yes |
| C4103828 | Validate — a successful validation posts an ABT audit record | Functional / Smartcards & ABT | FBD-100307, FBD-100658 | yes |
| C4103829 | Top-Up — a cash top-up adds value to an Adult iLink and prints a receipt | Functional / Smartcards & ABT | FBD-100261 | yes |
| C4103830 | Top-Up — a card top-up adds value to a Child iLink | Functional / Smartcards & ABT | FBD-100261 | yes |
| C4103831 | ZZ_DELETE_REVIEW - Top-Up — a top-up on an expired card is rejected | Functional / Smartcards & ABT | FBD-100261 | yes |
| C4103832 | Issue — issuing a new smartcard is not available on the HHD | Functional / Smartcards & ABT | FBD-100261 | yes |
| C4103833 | ABT Tap — a Glider inspection tap audits as an inspection with product 5001 | Functional / Smartcards & ABT | FBD-100658 | yes |
| C4103834 | ABT Tap — an HHD tap carries a CardDetails block with a masked PAN | Functional / Smartcards & ABT | FBD-100658 | yes |
| C4103835 | ABT Tap — a card-expired inspection maps DeclinedReason to 1 | Functional / Smartcards & ABT | FBD-100658 | yes |
| C4104670 | Validate — a Child iLink is accepted for a boarding within its zone | Functional / Smartcards & ABT | FBD-100250, FBD-100389, REQ-0862, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0879, REQ-0885, REQ-0912, REQ-0913, REQ-0914, REQ-0915, REQ-0919, REQ-0927, REQ-3473, REQ-3478 | yes |
| C4104671 | Validate — an aLink is accepted for a boarding within its zone | Functional / Smartcards & ABT | FBD-100250, FBD-100389, REQ-0862, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0879, REQ-0885, REQ-0912, REQ-0913, REQ-0914, REQ-0915, REQ-0919, REQ-0927, REQ-3473, REQ-3478 | yes |
| C4104672 | Validate — a yLink Discount is accepted for a boarding within its zone | Functional / Smartcards & ABT | FBD-100250, FBD-100389, REQ-0862, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0879, REQ-0885, REQ-0912, REQ-0913, REQ-0914, REQ-0915, REQ-0919, REQ-0927, REQ-3473, REQ-3478 | yes |
| C4104673 | Validate — an EA Pupil/Further-Education is accepted for a boarding within its zone | Functional / Smartcards & ABT | FBD-100250, FBD-100389, REQ-0862, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0879, REQ-0885, REQ-0912, REQ-0913, REQ-0914, REQ-0915, REQ-0919, REQ-0927, REQ-3473, REQ-3478 | yes |
| C4104674 | Validate — a Metro DayLink (Glider) is accepted for a boarding within its zone | Functional / Smartcards & ABT | FBD-100250, FBD-100389, REQ-0862, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0879, REQ-0885, REQ-0912, REQ-0913, REQ-0914, REQ-0915, REQ-0919, REQ-0927, REQ-3473, REQ-3478 | yes |
| C4104675 | Validate — a Metro Multi-Journey Adult (Glider) is accepted for a boarding within its zone | Functional / Smartcards & ABT | FBD-100250, FBD-100389, REQ-0862, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0879, REQ-0885, REQ-0912, REQ-0913, REQ-0914, REQ-0915, REQ-0919, REQ-0927, REQ-3473, REQ-3478 | yes |
| C4104676 | Validate — a Metro Multi-Journey Child (Glider) is accepted for a boarding within its zone | Functional / Smartcards & ABT | FBD-100250, FBD-100389, REQ-0862, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0879, REQ-0885, REQ-0912, REQ-0913, REQ-0914, REQ-0915, REQ-0919, REQ-0927, REQ-3473, REQ-3478 | yes |
| C4104677 | Validate — a Belfast Visitor Pass Adult (Glider) is accepted for a boarding within its zone | Functional / Smartcards & ABT | FBD-100250, FBD-100389, REQ-0862, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0879, REQ-0885, REQ-0912, REQ-0913, REQ-0914, REQ-0915, REQ-0919, REQ-0927, REQ-3473, REQ-3478 | yes |
| C4104678 | Validate — a Belfast Visitor Pass Child (Glider) is accepted for a boarding within its zone | Functional / Smartcards & ABT | FBD-100250, FBD-100389, REQ-0862, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0879, REQ-0885, REQ-0912, REQ-0913, REQ-0914, REQ-0915, REQ-0919, REQ-0927, REQ-3473, REQ-3478 | yes |
| C4104679 | Validate — a Metro Travelcard Adult (Glider) is accepted for a boarding within its zone | Functional / Smartcards & ABT | FBD-100250, FBD-100389, REQ-0862, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0879, REQ-0885, REQ-0912, REQ-0913, REQ-0914, REQ-0915, REQ-0919, REQ-0927, REQ-3473, REQ-3478 | yes |
| C4104680 | Validate — a Metro Travelcard Child (Glider) is accepted for a boarding within its zone | Functional / Smartcards & ABT | FBD-100250, FBD-100389, REQ-0862, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0879, REQ-0885, REQ-0912, REQ-0913, REQ-0914, REQ-0915, REQ-0919, REQ-0927, REQ-3473, REQ-3478 | yes |
| C4104681 | Validate — a Blind concession is accepted | Functional / Smartcards & ABT | FBD-100250, REQ-0840, REQ-0841, REQ-0842, REQ-0843, REQ-0844, REQ-0845, REQ-0851, REQ-0852, REQ-0853 | yes |
| C4104682 | Validate — a War Pensioner concession is accepted | Functional / Smartcards & ABT | FBD-100250, REQ-0840, REQ-0841, REQ-0842, REQ-0843, REQ-0844, REQ-0845, REQ-0851, REQ-0852, REQ-0853 | yes |
| C4104683 | Validate — a 60 Plus concession is accepted | Functional / Smartcards & ABT | FBD-100250, REQ-0840, REQ-0841, REQ-0842, REQ-0843, REQ-0844, REQ-0845, REQ-0851, REQ-0852, REQ-0853 | yes |
| C4104684 | Validate — a ROI Senior Smartpass concession is accepted | Functional / Smartcards & ABT | FBD-100250, REQ-0840, REQ-0841, REQ-0842, REQ-0843, REQ-0844, REQ-0845, REQ-0851, REQ-0852, REQ-0853 | yes |
| C4104685 | Validate — a Learning Disability concession is accepted | Functional / Smartcards & ABT | FBD-100250, REQ-0840, REQ-0841, REQ-0842, REQ-0843, REQ-0844, REQ-0845, REQ-0851, REQ-0852, REQ-0853 | yes |
| C4104686 | Validate — a DLA concession is accepted | Functional / Smartcards & ABT | FBD-100250, REQ-0840, REQ-0841, REQ-0842, REQ-0843, REQ-0844, REQ-0845, REQ-0851, REQ-0852, REQ-0853 | yes |
| C4104687 | Validate — a No Driving Licence concession is accepted | Functional / Smartcards & ABT | FBD-100250, REQ-0840, REQ-0841, REQ-0842, REQ-0843, REQ-0844, REQ-0845, REQ-0851, REQ-0852, REQ-0853 | yes |
| C4104688 | Validate — a Partially Sighted concession is accepted | Functional / Smartcards & ABT | FBD-100250, REQ-0840, REQ-0841, REQ-0842, REQ-0843, REQ-0844, REQ-0845, REQ-0851, REQ-0852, REQ-0853 | yes |
| C4104689 | Validate — a PIPS Half-Fare concession is accepted | Functional / Smartcards & ABT | FBD-100250, REQ-0840, REQ-0841, REQ-0842, REQ-0843, REQ-0844, REQ-0845, REQ-0851, REQ-0852, REQ-0853 | yes |
| C4104690 | Validate — a Staff Spouse Pass is accepted | Functional / Smartcards & ABT | FBD-100250, REQ-0855, REQ-0856, REQ-2025, REQ-2026 | yes |
| C4104691 | Validate — a Dependants Pass is accepted | Functional / Smartcards & ABT | FBD-100250, REQ-0855, REQ-0856, REQ-2025, REQ-2026 | yes |
| C4104692 | Validate — a External Staff Pass is accepted | Functional / Smartcards & ABT | FBD-100250, REQ-0855, REQ-0856, REQ-2025, REQ-2026 | yes |
| C4104693 | Validate — a Retired Staff Pass is accepted | Functional / Smartcards & ABT | FBD-100250, REQ-0855, REQ-0856, REQ-2025, REQ-2026 | yes |
| C4105267 | Mini Statement Printing — a print failure lets the operator retry | Functional / Smartcards & ABT | — | yes |
| C4105268 | Mini Statement Printing — a print failure can be cancelled | Functional / Smartcards & ABT | — | yes |
| C4105271 | Smartcard Rail Sales — valid Discount card opens Discount Sales screen | Functional / Smartcards & ABT | — | yes |
| C4105272 | Smartcard Rail Sales — valid Concessionary card opens Concessionary Sales screen | Functional / Smartcards & ABT | — | yes |
| C4105273 | Smartcard Rail Sales — clearing the Discount basket returns to Sales | Functional / Smartcards & ABT | — | yes |
| C4105274 | Smartcard Rail Sales — clearing the Concessionary basket returns to Sales | Functional / Smartcards & ABT | — | yes |
| C4105275 | Smartcard Rail Sales — previously-presented card shows Error - Passback | Functional / Smartcards & ABT | — | yes |
| C4105276 | Smartcard Rail Sales — invalid card critical error retries to a card presentation screen | Functional / Smartcards & ABT | — | yes |
| C4105277 | Smartcard Rail Sales — invalid card critical error cancel returns to Sales | Functional / Smartcards & ABT | — | yes |
| C4105278 | Smartcard Rail Sales — read/write fail retry returns to card validation | Functional / Smartcards & ABT | — | yes |
| C4103836 | Annul — a cash paper-ticket sale is annulled before sign-off | Functional / Annulment & Reversal | FBD-100373 | yes |
| C4103837 | Annul — a card paper-ticket sale is annulled | Functional / Annulment & Reversal | FBD-100373 | yes |
| C4103838 | Annul — an iLink top-up paid by cash is annulled | Functional / Annulment & Reversal | FBD-100373, REQ-2836 | yes |
| C4103839 | Annul — an iLink top-up paid by card is annulled | Functional / Annulment & Reversal | FBD-100373 | yes |
| C4103840 | Annul — a yLink discount sale is annulled | Functional / Annulment & Reversal | FBD-100373 | yes |
| C4103841 | Annul — nothing to annul shows a message | Functional / Annulment & Reversal | FBD-100373 | yes |
| C4103842 | Annul — outstanding sales are annulled at sign-off | Functional / Annulment & Reversal | FBD-100373 | yes |
| C4103843 | Reversal — a card sale is reversed on the M020 before settlement | Functional / Annulment & Reversal | FBD-100373 | yes |
| C4103844 | Annul Unique Reference — a card transaction is annulled by its PRN | Functional / Annulment & Reversal | FBD-100373 | yes |
| C4103845 | No Refund — the HHD offers no refund function | Functional / Annulment & Reversal | FBD-100373, REQ-1630 | yes |
| C4103846 | No Refund — a refund of an HHD sale is performed on the POS only | Functional / Annulment & Reversal | FBD-100373 | yes |
| C4104694 | Annul — a 24+ Discount sale is annulled | Functional / Annulment & Reversal | FBD-100373 | yes |
| C4105220 | Annulment — exiting Annul Transaction (Glider) returns to Operator Menu | Functional / Annulment & Reversal | — | yes |
| C4105221 | Annulment — Rail ticket search locates a transaction to annul | Functional / Annulment & Reversal | — | yes |
| C4105222 | Annulment — Cancel on Annul Transaction (Rail) returns to the transaction list | Functional / Annulment & Reversal | — | yes |
| C4105223 | Annulment — annulling a non-latest Rail top-up shows Invalid Transaction Selected | Functional / Annulment & Reversal | — | yes |
| C4105224 | Annulment — unreadable smartcard Retry returns to Present Smart Card | Functional / Annulment & Reversal | — | yes |
| C4105225 | Annulment — unreadable smartcard Cancel returns to Operator Menu | Functional / Annulment & Reversal | — | yes |
| C4105226 | Annulment — invalid smartcard shows Critical Error - Invalid Card | Functional / Annulment & Reversal | — | yes |
| C4105227 | Annulment — last operation a discount card validation routes to the print annulment flow | Functional / Annulment & Reversal | — | yes |
| C4105228 | Annulment — last operation a top-up routes to the print annulment flow | Functional / Annulment & Reversal | — | yes |
| C4105229 | Annulment — last operation not a top-up shows Critical Error | Functional / Annulment & Reversal | — | yes |
| C4105230 | Annulment — failed EMV receipt print, Continue without Printing returns to Operator Menu | Functional / Annulment & Reversal | — | yes |
| C4105231 | Annulment — failed EMV receipt print Retry reprints the card receipt | Functional / Annulment & Reversal | — | yes |
| C4105232 | Annulment — declining the EMV receipt print returns to Sales | Functional / Annulment & Reversal | — | yes |
| C4105233 | Annulment — successful refund print shows Printing Refund - Confirm | Functional / Annulment & Reversal | — | yes |
| C4105234 | Annulment — failed refund print, before the third attempt, retries the print | Functional / Annulment & Reversal | — | yes |
| C4105235 | Annulment — third failed refund print routes to Contact Ticket Office | Functional / Annulment & Reversal | — | yes |
| C4105236 | Annulment — Retry from Continue without Print retries the refund print | Functional / Annulment & Reversal | — | yes |
| C4105237 | Annulment — Performing Card Refund feeds into the shared Printing Refund flow | Functional / Annulment & Reversal | — | yes |
| C4103847 | Ticket Issue — a selected product is issued and printed | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100207, FBD-100336, REQ-0113 | yes |
| C4103848 | Ticket Issue — Adult single ticket | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100207, FBD-100336, REQ-0113 | yes |
| C4103849 | Ticket Issue — Child single ticket | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100207, FBD-100336, REQ-0113 | yes |
| C4103850 | Ticket Issue — default passenger and ticket type on entry | Functional / Sales - Paper Tickets / Ticket Issue | REQ-0235 | yes |
| C4103851 | Ticket Issue — boarding and alighting stage selection (menu) | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100207, FBD-100336, REQ-0113, REQ-0142 | yes |
| C4103852 | Ticket Issue — cash payment giving change | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100336 | yes |
| C4103853 | Ticket Issue — warrant payment | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100336 | yes |
| C4103854 | Ticket Issue — each issued ticket carries a unique ticket number | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100336, FBD-100373 | yes |
| C4103855 | Ticket Issue — an advance-dated ticket (Adult) | Functional / Sales - Paper Tickets / Ticket Issue | REQ-0142, REQ-0446, REQ-3094 | yes |
| C4103856 | Ticket Issue — period product (Student Monthly, Adult) | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100336 | yes |
| C4103857 | Ticket Issue — Bus Rambler ticket | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100336 | yes |
| C4103858 | Ticket Issue — 3 Day Select ticket (NIR-Rail, Adult) | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100167, FBD-100450 | yes |
| C4103859 | Ticket Issue — issued ticket carries a barcode when the ticket type is barcode-enabled | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100167, FBD-100318 | yes |
| C4103860 | Ticket Issue — a single ticket for multiple passengers carries no barcode | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100167 | yes |
| C4103861 | Ticket Issue — the sale posts an audit record to the back office | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100341 | yes |
| C4104695 | Ticket Issue — a selected product is issued and printed (warrant payment) | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100207, FBD-100336, REQ-0113 | yes |
| C4104696 | Ticket Issue — a selected product is issued and printed (cEMV card payment) | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100207, FBD-100336, REQ-0113 | yes |
| C4104697 | Ticket Issue — Adult single ticket (warrant payment) | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100207, FBD-100336, REQ-0113 | yes |
| C4104698 | Ticket Issue — Adult single ticket (cEMV card payment) | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100207, FBD-100336, REQ-0113 | yes |
| C4104699 | Ticket Issue — Child single ticket (warrant payment) | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100207, FBD-100336, REQ-0113 | yes |
| C4104700 | Ticket Issue — Child single ticket (cEMV card payment) | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100207, FBD-100336, REQ-0113 | yes |
| C4104701 | Ticket Issue — boarding and alighting stage selection (manual character entry) | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100207, FBD-100336, REQ-0113, REQ-0142 | yes |
| C4104702 | Ticket Issue — an advance-dated ticket (Child) | Functional / Sales - Paper Tickets / Ticket Issue | REQ-0142, REQ-0446, REQ-3094 | yes |
| C4104703 | Ticket Issue — period product (Weekly) | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100336 | yes |
| C4104704 | Ticket Issue — period product (Monthly) | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100336 | yes |
| C4104705 | Ticket Issue — period product (Student Monthly, Child) | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100336 | yes |
| C4104706 | Ticket Issue — Bus Rambler ticket (Child) | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100336 | yes |
| C4104707 | Ticket Issue — Bus Rambler ticket (cEMV card payment) | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100336 | yes |
| C4104708 | Ticket Issue — 3 Day Select ticket (NIR-Rail, Child) | Functional / Sales - Paper Tickets / Ticket Issue | FBD-100167, FBD-100450 | yes |
| C4105239 | Ticket Issue — retyping a corrected Alighting Stage search finds the stage | Functional / Sales - Paper Tickets / Ticket Issue | — | yes |
| C4105240 | Ticket Issue — Rail Family & Friends selection reaches product selection | Functional / Sales - Paper Tickets / Ticket Issue | — | yes |
| C4105241 | Ticket Issue — Glider passenger adjustment selects a Child | Functional / Sales - Paper Tickets / Ticket Issue | — | yes |
| C4105242 | Ticket Issue — choosing a different Glider product updates the Sales screen | Functional / Sales - Paper Tickets / Ticket Issue | — | yes |
| C4105243 | Ticket Issue — an invalid Boarding/Alighting combination shows No Valid Tickets | Functional / Sales - Paper Tickets / Ticket Issue | — | yes |
| C4105244 | Ticket Issue — cancelling Three-Day Travel date selection returns to Sales | Functional / Sales - Paper Tickets / Ticket Issue | — | yes |
| C4105245 | Ticket Issue — acting on an issued Advanced Ticket shows Are you sure? | Functional / Sales - Paper Tickets / Ticket Issue | — | yes |
| C4105258 | Ticket Printing — a print failure routes to Annulment | Functional / Sales - Paper Tickets / Ticket Issue | — | yes |
| C4105259 | No-Header Ticket Printing — a print failure lets the operator retry | Functional / Sales - Paper Tickets / Ticket Issue | — | yes |
| C4105260 | No-Header Ticket Printing — a print failure can be cancelled to Sales | Functional / Sales - Paper Tickets / Ticket Issue | — | yes |
| C4105261 | Card Ticket Printing — a print failure routes to Annulment | Functional / Sales - Paper Tickets / Ticket Issue | — | yes |
| C4105297 | Favourites — using a favourite during an active time band shows Unavailable | Functional / Sales - Paper Tickets / Ticket Issue | — | yes |
| C4105298 | Favourites — using a favourite adds it to the basket | Functional / Sales - Paper Tickets / Ticket Issue | — | yes |
| C4105299 | Favourites — using a favourite past the maximum revenue limit shows Max Revenue Exceeded | Functional / Sales - Paper Tickets / Ticket Issue | — | yes |
| C4105300 | Favourites — no available Passenger Type for a chosen Ticket Type | Functional / Sales - Paper Tickets / Ticket Issue | — | yes |
| C4103862 | Basket — a single product is added to the basket | Functional / Sales - Paper Tickets / Basket | FBD-100336, FBD-100373 | yes |
| C4103863 | Basket — tickets with different alighting stages form separate lines | Functional / Sales - Paper Tickets / Basket | FBD-100207, FBD-100336, FBD-100373, REQ-0113 | yes |
| C4103864 | Basket — a basket ticket is amended before purchase | Functional / Sales - Paper Tickets / Basket | FBD-100207, FBD-100336, FBD-100373, REQ-0113 | yes |
| C4103865 | Basket — a basket line is deleted | Functional / Sales - Paper Tickets / Basket | FBD-100336, FBD-100373 | yes |
| C4103866 | Basket — the basket is cleared | Functional / Sales - Paper Tickets / Basket | FBD-100336, FBD-100373 | yes |
| C4103867 | Basket — a completed basket sale prints all tickets in one transaction | Functional / Sales - Paper Tickets / Basket | FBD-100336, FBD-100373 | yes |
| C4105246 | Basket — duplicating a basket item adds a copy | Functional / Sales - Paper Tickets / Basket | — | yes |
| C4105247 | Basket — adding a favourite to a full basket shows Basket Full | Functional / Sales - Paper Tickets / Basket | — | yes |
| C4105248 | Payment Area — Cancel returns to the Sales screen | Functional / Sales - Paper Tickets / Basket | — | yes |
| C4103868 | Group Ticket Sales — a group of the same product is issued | Functional / Sales - Paper Tickets / Group Ticket Sales | FBD-100336, FBD-100373 | yes |
| C4103869 | Group Ticket Sales — a group is built and amended in the basket | Functional / Sales - Paper Tickets / Group Ticket Sales | FBD-100336, FBD-100373 | yes |
| C4103870 | Visual Inspection — a paper ticket is visually inspected | Functional / Sales - Paper Tickets / Visual Inspection | FBD-100336 | yes |
| C4103871 | Cross-Border — single with an ROI alighting stage | Functional / Sales - Paper Tickets / Cross-Border Tickets | FBD-100450, REQ-1138 | yes |
| C4103872 | Cross-Border — single from an ROI boarding stage | Functional / Sales - Paper Tickets / Cross-Border Tickets | FBD-100450, REQ-1138 | yes |
| C4103873 | Cross-Border — cash tendered in Euro is accepted and change given | Functional / Sales - Paper Tickets / Cross-Border Tickets | FBD-100450 | yes |
| C4103874 | Cross-Border — ticket prints on the cross-border layout | Functional / Sales - Paper Tickets / Cross-Border Tickets | FBD-100450 | yes |
| C4104709 | Cross-Border — single with an ROI alighting stage (cash, Euro) | Functional / Sales - Paper Tickets / Cross-Border Tickets | FBD-100450, REQ-1138 | yes |
| C4104710 | Cross-Border — single with an ROI alighting stage (warrant, Euro) | Functional / Sales - Paper Tickets / Cross-Border Tickets | FBD-100450, REQ-1138 | yes |
| C4104711 | Cross-Border — single from an ROI boarding stage (cash, Euro) | Functional / Sales - Paper Tickets / Cross-Border Tickets | FBD-100450, REQ-1138 | yes |
| C4104712 | Cross-Border — single from an ROI boarding stage (warrant, Euro) | Functional / Sales - Paper Tickets / Cross-Border Tickets | FBD-100450, REQ-1138 | yes |
| C4103875 | Metro Products — a Metro product ticket is issued | Functional / Sales - Paper Tickets / Metro & Ulsterbus Products | FBD-100207, FBD-100336, REQ-0113, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0914, REQ-0915 | yes |
| C4103876 | Ulsterbus Products — an Ulsterbus product ticket is issued | Functional / Sales - Paper Tickets / Metro & Ulsterbus Products | FBD-100207, FBD-100336, REQ-0113, REQ-0879, REQ-0885 | yes |
| C4103877 | Ulsterbus Town Service — a Town Service ticket is limited to the boarding town | Functional / Sales - Paper Tickets / Metro & Ulsterbus Products | FBD-100207, FBD-100340, REQ-0113 | yes |
| C4103878 | Ulsterbus Town Service — boarding outside the town-service zone is rejected | Functional / Sales - Paper Tickets / Metro & Ulsterbus Products | FBD-100340 | yes |
| C4104713 | Metro Products — a Metro Day ticket is issued | Functional / Sales - Paper Tickets / Metro & Ulsterbus Products | FBD-100207, FBD-100336, REQ-0113, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0914, REQ-0915 | yes |
| C4104714 | Metro Products — a Metro Evening ticket is issued | Functional / Sales - Paper Tickets / Metro & Ulsterbus Products | FBD-100207, FBD-100336, REQ-0113, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0914, REQ-0915 | yes |
| C4104715 | Metro Products — a Metro Single ticket is issued (Child) | Functional / Sales - Paper Tickets / Metro & Ulsterbus Products | FBD-100207, FBD-100336, REQ-0113, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0914, REQ-0915 | yes |
| C4104716 | Metro Products — a Metro DayLink ticket is issued (Adult) | Functional / Sales - Paper Tickets / Metro & Ulsterbus Products | FBD-100207, FBD-100336, REQ-0113, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0914, REQ-0915 | yes |
| C4104717 | Metro Products — a Metro DayLink ticket is issued (Child) | Functional / Sales - Paper Tickets / Metro & Ulsterbus Products | FBD-100207, FBD-100336, REQ-0113, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0914, REQ-0915 | yes |
| C4104718 | Metro Products — a Metro Multi-Journey ticket is issued (Adult) | Functional / Sales - Paper Tickets / Metro & Ulsterbus Products | FBD-100207, FBD-100336, REQ-0113, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0914, REQ-0915 | yes |
| C4104719 | Metro Products — a Metro Multi-Journey ticket is issued (Child) | Functional / Sales - Paper Tickets / Metro & Ulsterbus Products | FBD-100207, FBD-100336, REQ-0113, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0914, REQ-0915 | yes |
| C4104720 | Metro Products — a Metro Travelcard ticket is issued (Adult) | Functional / Sales - Paper Tickets / Metro & Ulsterbus Products | FBD-100207, FBD-100336, REQ-0113, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0914, REQ-0915 | yes |
| C4104721 | Metro Products — a Metro Travelcard ticket is issued (Child) | Functional / Sales - Paper Tickets / Metro & Ulsterbus Products | FBD-100207, FBD-100336, REQ-0113, REQ-0863, REQ-0864, REQ-0871, REQ-0874, REQ-0914, REQ-0915 | yes |
| C4104722 | Ulsterbus Products — a Day Return ticket is issued | Functional / Sales - Paper Tickets / Metro & Ulsterbus Products | FBD-100207, FBD-100336, REQ-0113, REQ-0879, REQ-0885 | yes |
| C4104723 | Ulsterbus Products — a Single ticket is issued (Child) | Functional / Sales - Paper Tickets / Metro & Ulsterbus Products | FBD-100207, FBD-100336, REQ-0113, REQ-0879, REQ-0885 | yes |
| C4104724 | Ulsterbus Products — a Multi-Journey ticket is issued (Adult) | Functional / Sales - Paper Tickets / Metro & Ulsterbus Products | FBD-100207, FBD-100336, REQ-0113, REQ-0879, REQ-0885 | yes |
| C4104725 | Ulsterbus Products — a Multi-Journey ticket is issued (Child) | Functional / Sales - Paper Tickets / Metro & Ulsterbus Products | FBD-100207, FBD-100336, REQ-0113, REQ-0879, REQ-0885 | yes |
| C4103879 | Top-Up — a smartcard top-up completes and prints a receipt | Functional / Top-Ups | FBD-100261, FBD-100268, REQ-0873, REQ-0878, REQ-0881, REQ-0887, REQ-2065, REQ-2070, REQ-2461, REQ-2463, REQ-2618, REQ-2633 | yes |
| C4103880 | Top-Up — Multi-Journey top-up adds the selected journeys | Functional / Top-Ups | FBD-100261 | yes |
| C4103881 | Top-Up — a Multi-Journey top-up exceeding the configured maximum is prevented | Functional / Top-Ups | FBD-100261 | yes |
| C4103882 | Top-Up — expired journeys are removed before an amount-entered top-up | Functional / Top-Ups | FBD-100261, REQ-0001, REQ-0873, REQ-0878, REQ-0881, REQ-0887 | yes |
| C4103883 | Top-Up — an expired smartcard is topped up and reactivated | Functional / Top-Ups | FBD-100261 | yes |
| C4103884 | Top-Up — the Operator enters the exact amount owed manually | Functional / Top-Ups | FBD-100261 | yes |
| C4103885 | Top-Up — a quick-select cash amount over the amount owed gives change | Functional / Top-Ups | FBD-100261 | yes |
| C4103886 | Top-Up — the Operator starts a top-up and cancels it | Functional / Top-Ups | FBD-100261 | yes |
| C4103887 | Top-Up — presenting a different card when completing the top-up is rejected | Functional / Top-Ups | FBD-100261 | yes |
| C4103888 | Top-Up — a non-Translink smartcard is rejected | Functional / Top-Ups | FBD-100236, FBD-100261 | yes |
| C4103889 | Top-Up — an unsuccessful top-up print is retried | Functional / Top-Ups | FBD-100261 | yes |
| C4103890 | Top-Up — an unsuccessful top-up print is annulled and cash refunded | Functional / Top-Ups | FBD-100261 | yes |
| C4103891 | Top-Up — a mini-statement after a top-up shows the updated Multi-Journey balance | Functional / Top-Ups | FBD-100261 | yes |
| C4103892 | Top-Up — a completed top-up posts an audit record to the back office | Functional / Top-Ups | FBD-100261 | yes |
| C4104726 | Top-Up — a Daylink top-up completes and prints a receipt | Functional / Top-Ups | FBD-100261, FBD-100268, REQ-0873, REQ-0878, REQ-0881, REQ-0887, REQ-2065, REQ-2070, REQ-2461, REQ-2463, REQ-2618, REQ-2633 | yes |
| C4104727 | Top-Up — a Metro Travelcard top-up completes and prints a receipt | Functional / Top-Ups | FBD-100261, FBD-100268, REQ-0873, REQ-0878, REQ-0881, REQ-0887, REQ-2065, REQ-2070, REQ-2461, REQ-2463, REQ-2618, REQ-2633 | yes |
| C4104728 | Top-Up — a Belfast Visitor Pass top-up completes and prints a receipt | Functional / Top-Ups | FBD-100261, FBD-100268, REQ-0873, REQ-0878, REQ-0881, REQ-0887, REQ-2065, REQ-2070, REQ-2461, REQ-2463, REQ-2618, REQ-2633 | yes |
| C4104729 | Top-Up — a Period product top-up completes and prints a receipt | Functional / Top-Ups | FBD-100261, FBD-100268, REQ-0873, REQ-0878, REQ-0881, REQ-0887, REQ-2065, REQ-2070, REQ-2461, REQ-2463, REQ-2618, REQ-2633 | yes |
| C4104730 | Top-Up — a smartcard top-up completes and prints a receipt (Child) | Functional / Top-Ups | FBD-100261, FBD-100268, REQ-0873, REQ-0878, REQ-0881, REQ-0887, REQ-2065, REQ-2070, REQ-2461, REQ-2463, REQ-2618, REQ-2633 | yes |
| C4104731 | Top-Up — a smartcard top-up completes and prints a receipt (cEMV card payment) | Functional / Top-Ups | FBD-100261, FBD-100268, REQ-0873, REQ-0878, REQ-0881, REQ-0887, REQ-2065, REQ-2070, REQ-2461, REQ-2463, REQ-2618, REQ-2633 | yes |
| C4104732 | Top-Up — Multi-Journey top-up adds the selected journeys (Ulsterbus) | Functional / Top-Ups | FBD-100261 | yes |
| C4104733 | Top-Up — Multi-Journey top-up adds the selected journeys (Child) | Functional / Top-Ups | FBD-100261 | yes |
| C4104734 | Top-Up — expired journeys are removed before a quick-selection top-up | Functional / Top-Ups | FBD-100261, REQ-0001, REQ-0873, REQ-0878, REQ-0881, REQ-0887 | yes |
| C4104735 | Top-Up — an expired Belfast Visitor Pass is topped up and reactivated | Functional / Top-Ups | FBD-100261 | yes |
| C4104736 | Top-Up — an expired Metro Travelcard is topped up and reactivated | Functional / Top-Ups | FBD-100261 | yes |
| C4104737 | Top-Up — an expired Daylink is topped up and reactivated | Functional / Top-Ups | FBD-100261 | yes |
| C4104738 | Top-Up — an expired smartcard is topped up and reactivated (Child) | Functional / Top-Ups | FBD-100261 | yes |
| C4104739 | Top-Up — a mini-statement after a top-up shows the updated Period expiry | Functional / Top-Ups | FBD-100261 | yes |
| C4104740 | Top-Up — a mini-statement after a top-up shows the updated Daylink days | Functional / Top-Ups | FBD-100261 | yes |
| C4105279 | Smartcard Top-Up — unreadable card at Present Smart Card retries | Functional / Top-Ups | — | yes |
| C4105280 | Smartcard Top-Up — unreadable card at Present Smart Card cancels to Sales | Functional / Top-Ups | — | yes |
| C4105281 | Smartcard Top-Up — invalid card retry prompts Represent Smartcard | Functional / Top-Ups | — | yes |
| C4105282 | Smartcard Top-Up — invalid card cancel voids prior card payment | Functional / Top-Ups | — | yes |
| C4105283 | Smartcard Top-Up — invalid card cancel returns to Sales when no card payment taken | Functional / Top-Ups | — | yes |
| C4105284 | Smartcard Top-Up — no eligible products returns to Present Smart Card | Functional / Top-Ups | — | yes |
| C4105285 | Smartcard Top-Up — unreadable card at Represent Smartcard retries | Functional / Top-Ups | — | yes |
| C4105286 | Smartcard Top-Up — Represent Smartcard critical error cancel voids prior card payment | Functional / Top-Ups | — | yes |
| C4103893 | Penalty Warning — a penalty warning is issued and printed | Functional / Penalty Warning & Fares | REQ-0062, REQ-1449, REQ-3048 | yes |
| C4103894 | Penalty Warning — a penalty warning is issued during a smartcard inspection | Functional / Penalty Warning & Fares | REQ-0062, REQ-1449 | yes |
| C4103895 | Penalty Fare — a penalty fare is issued from the operator menu | Functional / Penalty Warning & Fares | REQ-0062, REQ-1449, REQ-3048 | yes |
| C4103896 | Penalty Fare — a penalty fare is issued for an invalid or expired smartcard | Functional / Penalty Warning & Fares | REQ-1449, REQ-3049 | yes |
| C4103897 | Penalty Fare — the penalty ticket prints correct details for Operator and Supervisor | Functional / Penalty Warning & Fares | REQ-1449 | yes |
| C4103898 | Penalty Fare — only a whitelisted operator can issue a penalty fare | Functional / Penalty Warning & Fares | REQ-3049 | yes |
| C4103899 | Penalty Fare — issuing a penalty fare posts an audit event to the back office | Functional / Penalty Warning & Fares | REQ-1449, REQ-2255 | yes |
| C4103900 | Penalty Warning & Fares — a waybill reflects issued penalties | Functional / Penalty Warning & Fares | REQ-0329, REQ-3047 | yes |
| C4104741 | Penalty Fare — a penalty fare is issued for an invalid or expired Child smartcard | Functional / Penalty Warning & Fares | REQ-1449, REQ-3049 | yes |
| C4104742 | Penalty Fare — a penalty fare is issued for an invalid or expired Free smartcard | Functional / Penalty Warning & Fares | REQ-1449, REQ-3049 | yes |
| C4104743 | Penalty Fare — a penalty fare is issued for an invalid or expired yLink smartcard | Functional / Penalty Warning & Fares | REQ-1449, REQ-3049 | yes |
| C4104744 | Penalty Fare — a penalty fare is issued for an invalid or expired 24+ smartcard | Functional / Penalty Warning & Fares | REQ-1449, REQ-3049 | yes |
| C4104745 | Penalty Fare — a penalty fare is issued for an invalid or expired Staff Pass smartcard | Functional / Penalty Warning & Fares | REQ-1449, REQ-3049 | yes |
| C4104746 | Penalty Fare — the penalty ticket prints correct details for a Supervisor | Functional / Penalty Warning & Fares | REQ-1449 | yes |
| C4103901 | Sign On — Operator sign on (manual and smartcard) | Functional / Sign On & Session | REQ-0056, REQ-0396 | yes |
| C4103902 | Sign On — invalid ID or password is rejected | Functional / Sign On & Session | REQ-0056 | yes |
| C4103903 | Sign On — device locks after the configured failed attempts | Functional / Sign On & Session | — | yes |
| C4103904 | Sign On — Communication Locked when CloudFare comms are lost | Functional / Sign On & Session | FBD-100359 | yes |
| C4103905 | Sign On — duty number entry | Functional / Sign On & Session | REQ-0050, REQ-0396 | yes |
| C4103906 | Sign On — Message and Word & Colour of the Day | Functional / Sign On & Session | REQ-0056, REQ-0276 | yes |
| C4103907 | Sign On — correct topology data is presented for the signed-on location | Functional / Sign On & Session | FBD-100383 | yes |
| C4103908 | Sign On — route or service selection | Functional / Sign On & Session | FBD-100296 | yes |
| C4103909 | Sign Off — Operator sign off | Functional / Sign On & Session | REQ-0396 | yes |
| C4103910 | Sign Off — automatic sign off after inactivity | Functional / Sign On & Session | — | yes |
| C4103911 | Sign Off — forced sign off when the HHD is docked | Functional / Sign On & Session | REQ-0384, REQ-1478 | yes |
| C4103912 | Session — 15-minute staff-list heartbeat call-in | Functional / Sign On & Session | FBD-100266 | yes |
| C4103913 | Break-Mode Sign On — HHD resumes the same mode after an operator break | Functional / Sign On & Session | FBD-100651, FBD-100690, REQ-0305 | yes |
| C4104128 | Sign On — device resets to Inspector Mode after a full sign-off | Functional / Sign On & Session | FBD-100651 | yes |
| C4104747 | Break-Mode Sign On — HHD resumes Validation Mode after an operator break | Functional / Sign On & Session | FBD-100651, FBD-100690, REQ-0305 | yes |
| C4104748 | Operator — take an operator break and resume in Inspection Mode | Functional / Sign On & Session | FBD-100651, FBD-100690, REQ-0305 | yes |
| C4105215 | Sign On — hotlisted or invalid supervisor card during unlock returns to Device Locked | Functional / Sign On & Session | — | yes |
| C4105216 | Sign On — hotlisted or invalid card at login start returns to Login Start | Functional / Sign On & Session | — | yes |
| C4105217 | Sign On — Test Printer failure Retry returns to Test Printer | Functional / Sign On & Session | — | yes |
| C4105218 | Sign On — Test Printer failure Continue Without Printing proceeds to login flow | Functional / Sign On & Session | — | yes |
| C4105219 | Select Route — Menu icon opens Select Route - Menu | Functional / Sign On & Session | — | yes |
| C4103914 | Operator Menu — navigation and available options | Functional / Operator | — | yes |
| C4103915 | Operator Menu — role scope excludes Supervisor and Technician functions | Functional / Operator | FBD-100342 | yes |
| C4103916 | Operator Menu — view totals for the current journey and duty | Functional / Operator | REQ-0299, REQ-0350 | yes |
| C4103917 | Operator — print a mini-statement | Functional / Operator | REQ-2452 | yes |
| C4103918 | Operator — manage sale favourites (add, modify, delete) | Functional / Operator | REQ-0307 | yes |
| C4103919 | Operator — take an operator break and resume in the same mode | Functional / Operator | FBD-100651, FBD-100690, REQ-0305 | yes |
| C4103920 | Operator — view device status | Functional / Operator | — | yes |
| C4103921 | Operator — issue a penalty fare warning | Functional / Operator | FBD-100690, REQ-0062, REQ-1449 | yes |
| C4103922 | Operator — pair the printer | Functional / Operator | FBD-100320, REQ-0819 | yes |
| C4105238 | Mini Statement — invalid smartcard shows Critical Error | Functional / Operator | — | yes |
| C4103923 | Sign On — Supervisor sign on (manual and smartcard) | Functional / Supervisor | REQ-0050 | yes |
| C4103924 | Supervisor — act as Operator (sign on, sign off, end duty) | Functional / Supervisor | — | yes |
| C4103925 | Supervisor — override/end an operator break (ID entry and card) | Functional / Supervisor | REQ-0305, REQ-0360, REQ-1137 | yes |
| C4103926 | Sign On — Supervisor unlocks a PIN-locked HHD | Functional / Supervisor | REQ-0099 | yes |
| C4103927 | Supervisor — view and print previous waybills | Functional / Supervisor | REQ-0350 | yes |
| C4103928 | Supervisor — print software versions | Functional / Supervisor | REQ-0353 | yes |
| C4103929 | Supervisor — pair with a different payment device | Functional / Supervisor | FBD-100320 | yes |
| C4103930 | Supervisor Menu — navigation and role scope | Functional / Supervisor | REQ-0656 | yes |
| C4103931 | Sign Off — Supervisor sign off | Functional / Supervisor | FBD-100358, REQ-0098 | yes |
| C4104127 | Sign On — an incorrect Supervisor PIN leaves a PIN-locked HHD locked | Functional / Supervisor | REQ-0099 | yes |
| C4105287 | Supervisor Menu — Start Duty reaches the Signed in On Duty screen | Functional / Supervisor | — | yes |
| C4105288 | Supervisor Menu — End Duty starts the Waybill Print flow | Functional / Supervisor | — | yes |
| C4105291 | Connect Printer — invalid barcode scan for MAC address returns to Enter MAC Address | Functional / Supervisor | — | yes |
| C4105292 | Connect Printer — connection failure shows Unable to Connect | Functional / Supervisor | — | yes |
| C4105293 | Pair with Payment Device — pairing failure shows Card_Reader_Not_Connected | Functional / Supervisor | — | yes |
| C4103932 | Sign On — Technician sign on (manual and smartcard) | Functional / Technician | REQ-0050 | yes |
| C4103933 | Technician — set the device home location | Functional / Technician | REQ-0514 | yes |
| C4103934 | Technician — set the Terminal ID and Transaction Key | Functional / Technician | FBD-100320 | yes |
| C4103935 | Technician — pair with the payment device | Functional / Technician | FBD-100320 | yes |
| C4103936 | Technician — connect the printer (MAC entered or scanned) | Functional / Technician | REQ-0819 | yes |
| C4103937 | Technician Menu — navigation and role scope | Functional / Technician | REQ-0656 | yes |
| C4103938 | Sign Off — Technician sign off | Functional / Technician | FBD-100358, REQ-0098 | yes |
| C4105289 | Technician Mode — Apply Printer Firmware starts the firmware update | Functional / Technician | — | yes |
| C4105290 | Technician Mode — Configure Penalty Fare Application opens the third-party app | Functional / Technician | — | yes |
| C4105294 | Printer Firmware — applying firmware returns to Technician Menu | Functional / Technician | — | yes |
| C4105295 | Home Location — Back Office unavailable returns to Technician Menu | Functional / Technician | — | yes |
| C4105296 | Penalty Fare Application — opens the third-party app | Functional / Technician | — | yes |
| C4103939 | Ticket Format — NIR Layout 1 (Single/Day Return) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4103940 | Ticket Format — Cross-Border ticket format (NIR) | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4103941 | Ticket Format — Glider Format 8a/8b (Half-Fare Smartpass) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4103942 | Ticket Format — Glider Format 13 (DayLink top-up) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4103943 | Ticket Format — annul or cancel ticket (Format 16) and Non-Issue | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4103944 | Ticket Format — faulty smartpass or smartcard receipt | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4103945 | Ticket Format — travel receipt and print-test ticket | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4103946 | Ticket Format — penalty fare warning ticket | Functional / Ticket Formats & Waybill | FBD-100363, FBD-100716 | yes |
| C4103947 | Waybill — Operator Waybill prints the duty's transactions | Functional / Ticket Formats & Waybill | REQ-0329 | yes |
| C4103948 | Waybill — end-of-shift waybill with no transactions | Functional / Ticket Formats & Waybill | REQ-0329 | yes |
| C4103949 | Waybill — annulment lines are included | Functional / Ticket Formats & Waybill | — | yes |
| C4103950 | Waybill — validation, inspection and barcode activity are included | Functional / Ticket Formats & Waybill | REQ-0329 | yes |
| C4104749 | Ticket Format — NIR Layout 2 (Weekly/Monthly/Warrant Return) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104750 | Ticket Format — NIR Layout 3 (Three Day Select) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104751 | Ticket Format — NIR Layout 4 (iLink Single) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104752 | Ticket Format — NIR Layout 10 (Family & Friends) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104753 | Ticket Format — NIR Layout 11 (Family & Friends) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104754 | Ticket Format — NIR Layout 13 (Family Day) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104755 | Ticket Format — Glider Format 1 (Adult Single) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104756 | Ticket Format — Glider Format 2 (Adult Day) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104757 | Ticket Format — Glider Format 3 (Family & Friends) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104758 | Ticket Format — Glider Format 4 (Family & Friends) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104759 | Ticket Format — Glider Format 5 (Family Day) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104760 | Ticket Format — Glider Format 6 (Family Day) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104761 | Ticket Format — Glider Format 7 (Summer Bus Rambler) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104762 | Ticket Format — Glider Format 9 (yLink Single) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104763 | Ticket Format — NIR Layout 7a/7b (Half fare, yLink, 24+) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104764 | Ticket Format — NIR Layout 8a/8b (Free Concession Pass) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104765 | Ticket Format — Glider Format 10a/10b (Free Smartpass) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104766 | Ticket Format — Glider Format 13A (Period Pass top-up) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104767 | Ticket Format — Glider Format 13B (Multi-Journey top-up) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104768 | Ticket Format — Glider Format 13C (Top-up Expiry) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104769 | Ticket Format — NIR Layout 12 (iLink Top-Up) prints to the approved layout | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104770 | Ticket Format — annul/cancel ticket (Format 16, Paper Ticket) | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104771 | Ticket Format — annul/cancel ticket (Format 16, Multi-Journey Top-Up) | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4104772 | Ticket Format — annul/cancel ticket (Format 16, DayLink Top-Up) | Functional / Ticket Formats & Waybill | FBD-100363 | yes |
| C4105264 | Waybill Printing (menu access) — a print failure shows Printing Failed | Functional / Ticket Formats & Waybill | — | yes |
| C4105265 | Waybill Printing — a print failure lets the operator retry | Functional / Ticket Formats & Waybill | — | yes |
| C4105266 | Waybill Printing — continuing without printing exits the print-failure flow | Functional / Ticket Formats & Waybill | — | yes |
| C4103951 | Single-Use Barcode — encryption keys are fetched once per shift at sign-on | Functional / Single-Use Barcodes (NIR) | FBD-100483 | yes |
| C4103952 | Single-Use Barcode — an encryption-key fetch failure does not block sign-on | Functional / Single-Use Barcodes (NIR) | FBD-100483 | yes |
| C4103953 | Single-Use Barcode — AES versus TripleDES is selected from the encrypted string | Functional / Single-Use Barcodes (NIR) | FBD-100483 | yes |
| C4103954 | Single-Use Barcode — a valid decrypt has exactly 17 commas and a known type | Functional / Single-Use Barcodes (NIR) | FBD-100483 | yes |
| C4103955 | Single-Use Barcode — a decrypt failure shows the decryption-failed message | Functional / Single-Use Barcodes (NIR) | FBD-100483 | yes |
| C4103956 | Single-Use Barcode — a manual 12-digit reference is validated as the ShortID | Functional / Single-Use Barcodes (NIR) | FBD-100483 | yes |
| C4103957 | Single-Use Barcode — a locally used ShortID is rejected before going online | Functional / Single-Use Barcodes (NIR) | FBD-100483 | yes |
| C4103958 | Single-Use Barcode — a redeemed barcode emits the Barcode Redemption event 1412 | Functional / Single-Use Barcodes (NIR) | FBD-100483 | yes |
| C4103959 | Single-Use Barcode — a redeem timeout queues offline and emits event 1416 | Functional / Single-Use Barcodes (NIR) | FBD-100483 | yes |
| C4103960 | Single-Use Barcode — offline value above the ceiling limit is rejected | Functional / Single-Use Barcodes (NIR) | FBD-100483 | yes |
| C4103961 | Single-Use Barcode — the offline sweep redeems queued barcodes without CloudFare events | Functional / Single-Use Barcodes (NIR) | FBD-100483 | yes |
| C4105179 | Single-Use Barcode — a barcode failing the Single-Use format check shows Not Valid | Functional / Single-Use Barcodes (NIR) | — | yes |
| C4105180 | Barcode Reference Entry — selecting Cancel from the entry screen | Functional / Single-Use Barcodes (NIR) | — | yes |
| C4105181 | Barcode Reference Entry — cancelling a keyed reference returns to Sales | Functional / Single-Use Barcodes (NIR) | — | yes |
| C4105182 | Single-Use Barcode — cancelling a failed validation returns to Sales | Functional / Single-Use Barcodes (NIR) | — | yes |
| C4105183 | Single-Use Barcode — a barcode passing the offline limit check but failing validation shows Not Valid | Functional / Single-Use Barcodes (NIR) | — | yes |
| C4105184 | Single-Use Barcode — a Type U barcode with mismatched dates shows Ticket Valid inc. Date with Expiry and Depart Time | Functional / Single-Use Barcodes (NIR) | — | yes |
| C4105185 | Single-Use Barcode — a Type U barcode with matching dates shows Ticket Valid inc. Date and Depart Time | Functional / Single-Use Barcodes (NIR) | — | yes |
| C4105186 | Single-Use Barcode — a Type B or E barcode shows Ticket Valid inc. Date and Depart Time | Functional / Single-Use Barcodes (NIR) | — | yes |
| C4105187 | Single-Use Barcode — a Type D barcode shows Ticket Valid inc. 3 Use Times | Functional / Single-Use Barcodes (NIR) | — | yes |
| C4105188 | Single-Use Barcode — a Type H or S barcode shows Ticket Valid inc. Outbound and Return | Functional / Single-Use Barcodes (NIR) | — | yes |
| C4105189 | Single-Use Barcode — a ticket failing visual inspection shows Not Passed Visual Inspection | Functional / Single-Use Barcodes (NIR) | — | yes |
| C4105190 | Single-Use Barcode — a failed redemption shows Not Valid | Functional / Single-Use Barcodes (NIR) | — | yes |
| C4103962 | Multi-Use Barcode — a valid barcode shows a green tick and audio | Functional / Multi-Use Barcodes | FBD-100167 | yes |
| C4103963 | Multi-Use Barcode — a route/location-only failure shows a yellow question mark | Functional / Multi-Use Barcodes | FBD-100167 | yes |
| C4103964 | Multi-Use Barcode — an invalid barcode shows a red cross and reason | Functional / Multi-Use Barcodes | FBD-100167 | yes |
| C4103965 | Multi-Use Barcode — a re-presented barcode within the passback window is rejected | Functional / Multi-Use Barcodes | FBD-100167 | yes |
| C4103966 | Multi-Use Barcode — a rail location failure falls back to valid above the fare threshold | Functional / Multi-Use Barcodes | FBD-100167 | yes |
| C4103967 | Multi-Use Barcode — a successful validation audits a zero-fare BarcodeUsage transaction | Functional / Multi-Use Barcodes | FBD-100167 | yes |
| C4103968 | Multi-Use Barcode — a failed validation sends an event with the Unique ID | Functional / Multi-Use Barcodes | FBD-100167 | yes |
| C4103969 | Multi-Use Barcode — a midnight-to-4am expiry displays the previous day and no time | Functional / Multi-Use Barcodes | FBD-100167 | yes |
| C4105169 | Multi-Use Barcode — vehicle type invalid for route shows Invalid Service | Functional / Multi-Use Barcodes | — | yes |
| C4105170 | Multi-Use Barcode — Start Date/Time not yet reached shows Invalid Time | Functional / Multi-Use Barcodes | — | yes |
| C4105171 | Multi-Use Barcode — End Date/Time passed shows Invalid Time | Functional / Multi-Use Barcodes | — | yes |
| C4105172 | Multi-Use Barcode — product not valid on route shows Invalid Service | Functional / Multi-Use Barcodes | — | yes |
| C4105173 | Multi-Use Barcode — 3 Day Select date mismatch shows Invalid Time | Functional / Multi-Use Barcodes | — | yes |
| C4105174 | Multi-Use Barcode — Rail location outside Boarding/Alighting shows Invalid Location | Functional / Multi-Use Barcodes | — | yes |
| C4105175 | Multi-Use Barcode — CR105 route product under £90 shows Invalid Location | Functional / Multi-Use Barcodes | — | yes |
| C4105176 | Multi-Use Barcode — Query mode result shown per product type | Functional / Multi-Use Barcodes | — | yes |
| C4105177 | Multi-Use Barcode — Scan from a result screen returns to barcode decryption check | Functional / Multi-Use Barcodes | — | yes |
| C4105178 | Multi-Use Barcode — non-Multi-Use format bridges to Single-Use flow | Functional / Multi-Use Barcodes | — | yes |
| C4105269 | Barcode Ticket Printing — a successful print confirms transaction complete | Functional / Multi-Use Barcodes | — | yes |
| C4105270 | Barcode Ticket Printing — a failed print confirmation triggers a reprint | Functional / Multi-Use Barcodes | — | yes |
| C4103970 | Old Barcode Redemption — a legacy BRS barcode is redeemed on Glider | Functional / Multi-Use Barcodes / Old Barcode Redemption (BRS) | FBD-100317, FBD-100483 | yes |
| C4103971 | Smartcard Inspection — a valid period pass is inspected successfully | Functional / Smartcard Inspection | REQ-0837 | yes |
| C4103972 | Smartcard Inspection — an adult iLink pass shows the adult colour on inspection | Functional / Smartcard Inspection | — | yes |
| C4103973 | Smartcard Inspection — a child pass shows the child colour on inspection | Functional / Smartcard Inspection | — | yes |
| C4103974 | Smartcard Inspection — an expired smartcard fails inspection | Functional / Smartcard Inspection | — | yes |
| C4103975 | Smartcard Inspection — a pass inspected within the transfer period is accepted | Functional / Smartcard Inspection | REQ-3488 | yes |
| C4103976 | Smartcard Inspection — a pass inspected after the transfer period offers revalidation | Functional / Smartcard Inspection | REQ-3488 | yes |
| C4103977 | ZZ_DELETE_REVIEW - Smartcard Inspection — inspection is available in break mode | Functional / Smartcard Inspection | — | yes |
| C4104773 | Smartcard Inspection — a valid Blind concession is inspected successfully | Functional / Smartcard Inspection | REQ-0837 | yes |
| C4104774 | Smartcard Inspection — a valid War Pensioner concession is inspected successfully | Functional / Smartcard Inspection | REQ-0837 | yes |
| C4104775 | Smartcard Inspection — a valid 60 Plus concession is inspected successfully | Functional / Smartcard Inspection | REQ-0837 | yes |
| C4104776 | Smartcard Inspection — a valid ROI Senior Smartpass concession is inspected successfully | Functional / Smartcard Inspection | REQ-0837 | yes |
| C4104777 | Smartcard Inspection — a valid Learning Disability half-fare pass is inspected successfully | Functional / Smartcard Inspection | REQ-0837 | yes |
| C4104778 | Smartcard Inspection — a valid DLA half-fare pass is inspected successfully | Functional / Smartcard Inspection | REQ-0837 | yes |
| C4104779 | Smartcard Inspection — a valid No Driving Licence half-fare pass is inspected successfully | Functional / Smartcard Inspection | REQ-0837 | yes |
| C4104780 | Smartcard Inspection — a valid Partially Sighted half-fare pass is inspected successfully | Functional / Smartcard Inspection | REQ-0837 | yes |
| C4104781 | Smartcard Inspection — a valid PIPS half-fare pass is inspected successfully | Functional / Smartcard Inspection | REQ-0837 | yes |
| C4104782 | Smartcard Inspection — a valid Staff Pass is inspected successfully | Functional / Smartcard Inspection | REQ-0837 | yes |
| C4104783 | Smartcard Inspection — a valid EA Pupil/Further-Education (Bus & Rail) pass is inspected successfully | Functional / Smartcard Inspection | REQ-0837 | yes |
| C4104784 | Smartcard Inspection — a valid Discounted Youth (yLink) pass is inspected successfully | Functional / Smartcard Inspection | REQ-0837 | yes |
| C4105196 | Smartcard Inspection — swiping the mode toggle keeps the Inspection device view | Functional / Smartcard Inspection | — | yes |
| C4105197 | Smartcard Inspection — Rail Inspection/Validation toggle switches both ways | Functional / Smartcard Inspection | — | yes |
| C4105198 | Smartcard Inspection — unreadable card marked Faulty Smartpass routes to Top-Up Receipt Print | Functional / Smartcard Inspection | — | yes |
| C4105199 | Smartcard Inspection — card failing pre-validation shows Error | Functional / Smartcard Inspection | — | yes |
| C4105200 | Smartcard Inspection — card not previously validated shows Invalid | Functional / Smartcard Inspection | — | yes |
| C4105201 | Smartcard Inspection — direction mismatch within the transfer period shows Invalid | Functional / Smartcard Inspection | — | yes |
| C4105202 | Smartcard Inspection — direction mismatch outside the transfer period shows Invalid | Functional / Smartcard Inspection | — | yes |
| C4105203 | Smartcard Inspection — overriding a Valid card to Not Valid shows Error | Functional / Smartcard Inspection | — | yes |
| C4105204 | Smartcard Inspection — validating an Invalid card routes by Glider or Rail | Functional / Smartcard Inspection | — | yes |
| C4105205 | Smartcard Validation — travel-prohibited card shows Error | Functional / Smartcard Inspection | — | yes |
| C4105206 | Smartcard Top-Up — invalid top-up card shows Critical Error | Functional / Smartcard Inspection | — | yes |
| C4105207 | Smartcard Validation — Half-Fare card routes by Glider or Rail to Discount Sales mode | Functional / Smartcard Inspection | — | yes |
| C4105208 | Smartcard Validation — Concession Fare card routes by Glider or Rail to Concessionary Card sales mode | Functional / Smartcard Inspection | — | yes |
| C4105209 | Concessionary Card Sales — cross-border ticket type selection returns to Rail sales mode | Functional / Smartcard Inspection | — | yes |
| C4105210 | Concessionary Card Sales — no other ticket types keeps the current screen displayed | Functional / Smartcard Inspection | — | yes |
| C4105211 | Discount Sales — yLink alighting selection reaches Discount Summary and Payment Area | Functional / Smartcard Inspection | — | yes |
| C4105212 | Payment Area — successful card payment proceeds to Represent Smartcard | Functional / Smartcard Inspection | — | yes |
| C4105213 | Payment Area — cash or Warrant payment proceeds to print or Represent Smartcard | Functional / Smartcard Inspection | — | yes |
| C4105214 | Critical Error — cancelling after a used payment card voids the transaction | Functional / Smartcard Inspection | — | yes |
| C4103978 | Revenue Inspection — Inspection Mode is enabled on a Tap-On-Only route | Functional / Revenue Inspection (cEMV/RID) | FBD-100651, FBD-100716 | yes |
| C4103979 | Revenue Inspection — Inspection Mode is disabled on a non-Tap-On-Only route | Functional / Revenue Inspection (cEMV/RID) | FBD-100651, FBD-100716 | yes |
| C4103980 | Revenue Inspection — a valid Visa Debit card inspection succeeds and emits event 5008 | Functional / Revenue Inspection (cEMV/RID) | FBD-100716 | yes |
| C4103981 | Revenue Inspection — a card on the RID List fails and emits event 5009 | Functional / Revenue Inspection (cEMV/RID) | FBD-100716 | yes |
| C4103982 | Revenue Inspection — an expired card is declined and emits event 5010 | Functional / Revenue Inspection (cEMV/RID) | FBD-100716 | yes |
| C4103983 | Revenue Inspection — a card failing ODA is declined and emits event 5011 | Functional / Revenue Inspection (cEMV/RID) | FBD-100716 | yes |
| C4103984 | Revenue Inspection — an American Express card is declined as an unsupported scheme and emits event 5012 | Functional / Revenue Inspection (cEMV/RID) | FBD-100716 | yes |
| C4103985 | Revenue Inspection — no connection to the back office shows the try-again message | Functional / Revenue Inspection (cEMV/RID) | FBD-100716 | yes |
| C4103986 | Revenue Inspection — no card within 30 seconds times out to the Sales screen | Functional / Revenue Inspection (cEMV/RID) | FBD-100716 | yes |
| C4103987 | Revenue Inspection — an inspection tap cannot be annulled | Functional / Revenue Inspection (cEMV/RID) | FBD-100716 | yes |
| C4103988 | Revenue Inspection — the full RID List is requested on application start-up | Functional / Revenue Inspection (cEMV/RID) | FBD-100716 | yes |
| C4103989 | Revenue Inspection — a 15-minute poll requests a delta RID List update | Functional / Revenue Inspection (cEMV/RID) | FBD-100716 | yes |
| C4103990 | Revenue Inspection — the first poll after End-of-Day requests a full RID List | Functional / Revenue Inspection (cEMV/RID) | FBD-100716 | yes |
| C4104785 | Revenue Inspection — a valid Visa Credit card inspection succeeds and emits event 5008 | Functional / Revenue Inspection (cEMV/RID) | FBD-100716 | yes |
| C4104786 | Revenue Inspection — a valid Mastercard Credit card inspection succeeds and emits event 5008 | Functional / Revenue Inspection (cEMV/RID) | FBD-100716 | yes |
| C4104787 | Revenue Inspection — a valid Mastercard Debit card inspection succeeds and emits event 5008 | Functional / Revenue Inspection (cEMV/RID) | FBD-100716 | yes |
| C4104788 | Revenue Inspection — a valid Maestro card inspection succeeds and emits event 5008 | Functional / Revenue Inspection (cEMV/RID) | FBD-100716 | yes |
| C4104789 | Revenue Inspection — a Diners card is declined as an unsupported scheme and emits event 5012 | Functional / Revenue Inspection (cEMV/RID) | FBD-100716 | yes |
| C4105191 | Revenue Inspection — Connecting screen times out back to Sales | Functional / Revenue Inspection (cEMV/RID) | — | yes |
| C4105192 | Revenue Inspection — Success times out to the next card prompt | Functional / Revenue Inspection (cEMV/RID) | — | yes |
| C4105193 | Revenue Inspection — Denylist failure times out to the next card prompt | Functional / Revenue Inspection (cEMV/RID) | — | yes |
| C4105194 | Revenue Inspection — change boarding location via numerical search | Functional / Revenue Inspection (cEMV/RID) | — | yes |
| C4105195 | Revenue Inspection — change boarding location via boarding list | Functional / Revenue Inspection (cEMV/RID) | — | yes |
| C4105162 | Payment Device Update — fullscreen update shown, HHD actions still available | Functional / Additional Features / Device Updates & Docking | — | yes |
| C4105163 | Device Docked — immediate update scheduled shows update icon | Functional / Additional Features / Device Updates & Docking | — | yes |
| C4105164 | Device Docked — no update pending shows plain Device Docked message | Functional / Additional Features / Device Updates & Docking | — | yes |
| C4105165 | Software Update — future-scheduled update does not require docking | Functional / Additional Features / Device Updates & Docking | — | yes |
| C4105166 | Fares Updating — LogOn screen shows transition to future fares | Functional / Additional Features / Device Updates & Docking | — | yes |
| C4105167 | Revenue Limit — approaching notification shows amount remaining | Functional / Additional Features / Revenue Limit | — | yes |
| C4105168 | Revenue Limit — reached signs off operator and locks the device | Functional / Additional Features / Revenue Limit | — | yes |
| C4103991 | Power & Battery — the operator's session recovers after a power loss | Non-Functional / Resilience / Power & Battery | REQ-0105 | yes |
| C4103992 | Power & Battery — the operator can sign on after replacing the battery | Non-Functional / Resilience / Power & Battery | REQ-0105 | yes |
| C4103993 | Power & Battery — a low-battery warning is shown to the operator | Non-Functional / Resilience / Power & Battery | REQ-1389 | yes |
| C4105302 | Power On — critical battery shows the Critical Battery Power On screen | Non-Functional / Resilience / Power & Battery | — | yes |
| C4103994 | Printer — a partially printed ticket is reported to the operator | Non-Functional / Resilience / Printer | REQ-1741 | yes |
| C4103995 | ZZ_DELETE_REVIEW - Printer — the HHD pairs to a printer by presenting its NFC chip | Non-Functional / Resilience / Printer | FBD-100320, REQ-0819 | yes |
| C4103996 | Heartbeat — the HHD calls in at least every 15 minutes even when signed off | Non-Functional / Resilience / Comms / SaaS / Heartbeat | FBD-100266 | yes |
| C4103997 | Heartbeat — a StaffList message resets Hours Since Last Communication to zero | Non-Functional / Resilience / Comms / SaaS / Heartbeat | FBD-100266 | yes |
| C4103998 | Comms — a sustained network outage takes the HHD offline | Non-Functional / Resilience / Comms / SaaS / Heartbeat | REQ-2576 | yes |
| C4103999 | Comms — queued transactions are delivered to the back office on restore | Non-Functional / Resilience / Comms / SaaS / Heartbeat | FBD-100359, REQ-2576 | yes |
| C4105159 | Additional Features — HHD shows Device Out of Service on a critical issue | Non-Functional / Resilience / Comms / SaaS / Heartbeat | — | yes |
| C4105160 | Additional Features — HHD shows Remotely Locked state | Non-Functional / Resilience / Comms / SaaS / Heartbeat | — | yes |
| C4105161 | Additional Features — HHD shows Remotely Out of Service state | Non-Functional / Resilience / Comms / SaaS / Heartbeat | — | yes |
| C4104000 | Network — the operator can view the HHD connectivity type and strength | Non-Functional / Resilience / Network | REQ-2854 | yes |
| C4104001 | Security — the panic button raises an alert | Non-Functional / Resilience / Security | REQ-0437 | yes |
| C4104002 | Security — the HHD upgrades from OS 7 to OS 8 | Non-Functional / Resilience / Security | REQ-0569, REQ-1618 | yes |
| C4104003 | Timings — a smartcard validation completes within the expected time | Non-Functional / Resilience / Timings | REQ-3364, REQ-3365 | yes |
| C4104004 | Timings — a barcode read to beep completes within one second | Non-Functional / Resilience / Timings | FBD-100167, REQ-3132 | yes |
