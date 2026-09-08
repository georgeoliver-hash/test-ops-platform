# Alignment audit - suite 30285

- Cases audited: **479**
- Blocking findings: **0**
- Advisory (reviewed-intentional) findings: **157**

## Residual mojibake in any field - 0
_none_

## Title missing the ' - ' feature separator _(advisory)_ - 0
_none_

## Title over 72 chars _(advisory)_ - 157
- C4103801 | M020 Commissioning — TID and TK download from TMS by serial after pairing - 73 chars
- C4103817 | Payment Device On Charge — a card sale completes while the M020 is on charge - 76 chars
- C4104669 | Card Declined — an unsupported-scheme card is declined without a PIN prompt - 75 chars
- C4105250 | Card Payment — a swiped Chip & PIN-capable card is redirected to Chip & PIN - 75 chars
- C4105263 | Card Payment Print Failure — continuing without printing returns to Sales - 73 chars
- C4105301 | Payment Device Status — reporting a faulty device notifies the back office and removes card payment - 99 chars
- C4103818 | Reference-Number Station — a card sale is keyed to the station reference number (NIR only) - 90 chars
- C4103819 | Reference-Number Station — the sale settles while the payment device is on charge (NIR only) - 92 chars
- C4103833 | ABT Tap — a Glider inspection tap audits as an inspection with product 5001 - 75 chars
- C4104673 | Validate — an EA Pupil/Further-Education is accepted for a boarding within its zone - 83 chars
- C4104674 | Validate — a Metro DayLink (Glider) is accepted for a boarding within its zone - 78 chars
- C4104675 | Validate — a Metro Multi-Journey Adult (Glider) is accepted for a boarding within its zone - 90 chars
- C4104676 | Validate — a Metro Multi-Journey Child (Glider) is accepted for a boarding within its zone - 90 chars
- C4104677 | Validate — a Belfast Visitor Pass Adult (Glider) is accepted for a boarding within its zone - 91 chars
- C4104678 | Validate — a Belfast Visitor Pass Child (Glider) is accepted for a boarding within its zone - 91 chars
- C4104679 | Validate — a Metro Travelcard Adult (Glider) is accepted for a boarding within its zone - 87 chars
- C4104680 | Validate — a Metro Travelcard Child (Glider) is accepted for a boarding within its zone - 87 chars
- C4105272 | Smartcard Rail Sales — valid Concessionary card opens Concessionary Sales screen - 80 chars
- C4105274 | Smartcard Rail Sales — clearing the Concessionary basket returns to Sales - 73 chars
- C4105276 | Smartcard Rail Sales — invalid card critical error retries to a card presentation screen - 88 chars
- C4105277 | Smartcard Rail Sales — invalid card critical error cancel returns to Sales - 74 chars
- C4105222 | Annulment — Cancel on Annul Transaction (Rail) returns to the transaction list - 78 chars
- C4105223 | Annulment — annulling a non-latest Rail top-up shows Invalid Transaction Selected - 81 chars
- C4105227 | Annulment — last operation a discount card validation routes to the print annulment flow - 88 chars
- C4105230 | Annulment — failed EMV receipt print, Continue without Printing returns to Operator Menu - 88 chars
- C4105234 | Annulment — failed refund print, before the third attempt, retries the print - 76 chars
- C4105237 | Annulment — Performing Card Refund feeds into the shared Printing Refund flow - 77 chars
- C4103859 | Ticket Issue — issued ticket carries a barcode when the ticket type is barcode-enabled - 86 chars
- C4103860 | Ticket Issue — a single ticket for multiple passengers carries no barcode - 73 chars
- C4104695 | Ticket Issue — a selected product is issued and printed (warrant payment) - 73 chars
- C4104696 | Ticket Issue — a selected product is issued and printed (cEMV card payment) - 75 chars
- C4104701 | Ticket Issue — boarding and alighting stage selection (manual character entry) - 78 chars
- C4105239 | Ticket Issue — retyping a corrected Alighting Stage search finds the stage - 74 chars
- C4105242 | Ticket Issue — choosing a different Glider product updates the Sales screen - 75 chars
- C4105243 | Ticket Issue — an invalid Boarding/Alighting combination shows No Valid Tickets - 79 chars
- C4105244 | Ticket Issue — cancelling Three-Day Travel date selection returns to Sales - 74 chars
- C4105297 | Favourites — using a favourite during an active time band shows Unavailable - 75 chars
- C4105299 | Favourites — using a favourite past the maximum revenue limit shows Max Revenue Exceeded - 88 chars
- C4103877 | Ulsterbus Town Service — a Town Service ticket is limited to the boarding town - 78 chars
- C4103878 | Ulsterbus Town Service — boarding outside the town-service zone is rejected - 75 chars
- C4103881 | Top-Up — a Multi-Journey top-up exceeding the configured maximum is prevented - 77 chars
- C4103887 | Top-Up — presenting a different card when completing the top-up is rejected - 75 chars
- C4103891 | Top-Up — a mini-statement after a top-up shows the updated Multi-Journey balance - 80 chars
- C4104731 | Top-Up — a smartcard top-up completes and prints a receipt (cEMV card payment) - 78 chars
- C4105280 | Smartcard Top-Up — unreadable card at Present Smart Card cancels to Sales - 73 chars
- C4105283 | Smartcard Top-Up — invalid card cancel returns to Sales when no card payment taken - 82 chars
- C4105286 | Smartcard Top-Up — Represent Smartcard critical error cancel voids prior card payment - 85 chars
- C4103894 | Penalty Warning — a penalty warning is issued during a smartcard inspection - 75 chars
- C4103896 | Penalty Fare — a penalty fare is issued for an invalid or expired smartcard - 75 chars
- C4103897 | Penalty Fare — the penalty ticket prints correct details for Operator and Supervisor - 84 chars
- C4103899 | Penalty Fare — issuing a penalty fare posts an audit event to the back office - 77 chars
- C4104741 | Penalty Fare — a penalty fare is issued for an invalid or expired Child smartcard - 81 chars
- C4104742 | Penalty Fare — a penalty fare is issued for an invalid or expired Free smartcard - 80 chars
- C4104743 | Penalty Fare — a penalty fare is issued for an invalid or expired yLink smartcard - 81 chars
- C4104744 | Penalty Fare — a penalty fare is issued for an invalid or expired 24+ smartcard - 79 chars
- C4104745 | Penalty Fare — a penalty fare is issued for an invalid or expired Staff Pass smartcard - 86 chars
- C4104746 | Penalty Fare — the penalty ticket prints correct details for a Supervisor - 73 chars
- C4105215 | Sign On — hotlisted or invalid supervisor card during unlock returns to Device Locked - 85 chars
- C4105216 | Sign On — hotlisted or invalid card at login start returns to Login Start - 73 chars
- C4105218 | Sign On — Test Printer failure Continue Without Printing proceeds to login flow - 79 chars
- C4105291 | Connect Printer — invalid barcode scan for MAC address returns to Enter MAC Address - 83 chars
- C4105293 | Pair with Payment Device — pairing failure shows Card_Reader_Not_Connected - 74 chars
- C4105290 | Technician Mode — Configure Penalty Fare Application opens the third-party app - 78 chars
- C4103939 | Ticket Format — NIR Layout 1 (Single/Day Return) prints to the approved layout - 78 chars
- C4103941 | Ticket Format — Glider Format 8a/8b (Half-Fare Smartpass) prints to the approved layout - 87 chars
- C4103942 | Ticket Format — Glider Format 13 (DayLink top-up) prints to the approved layout - 79 chars
- C4104749 | Ticket Format — NIR Layout 2 (Weekly/Monthly/Warrant Return) prints to the approved layout - 90 chars
- C4104750 | Ticket Format — NIR Layout 3 (Three Day Select) prints to the approved layout - 77 chars
- C4104751 | Ticket Format — NIR Layout 4 (iLink Single) prints to the approved layout - 73 chars
- C4104752 | Ticket Format — NIR Layout 10 (Family & Friends) prints to the approved layout - 78 chars
- C4104753 | Ticket Format — NIR Layout 11 (Family & Friends) prints to the approved layout - 78 chars
- C4104755 | Ticket Format — Glider Format 1 (Adult Single) prints to the approved layout - 76 chars
- C4104756 | Ticket Format — Glider Format 2 (Adult Day) prints to the approved layout - 73 chars
- C4104757 | Ticket Format — Glider Format 3 (Family & Friends) prints to the approved layout - 80 chars
- C4104758 | Ticket Format — Glider Format 4 (Family & Friends) prints to the approved layout - 80 chars
- C4104759 | Ticket Format — Glider Format 5 (Family Day) prints to the approved layout - 74 chars
- C4104760 | Ticket Format — Glider Format 6 (Family Day) prints to the approved layout - 74 chars
- C4104761 | Ticket Format — Glider Format 7 (Summer Bus Rambler) prints to the approved layout - 82 chars
- C4104762 | Ticket Format — Glider Format 9 (yLink Single) prints to the approved layout - 76 chars
- C4104763 | Ticket Format — NIR Layout 7a/7b (Half fare, yLink, 24+) prints to the approved layout - 86 chars
- C4104764 | Ticket Format — NIR Layout 8a/8b (Free Concession Pass) prints to the approved layout - 85 chars
- C4104765 | Ticket Format — Glider Format 10a/10b (Free Smartpass) prints to the approved layout - 84 chars
- C4104766 | Ticket Format — Glider Format 13A (Period Pass top-up) prints to the approved layout - 84 chars
- C4104767 | Ticket Format — Glider Format 13B (Multi-Journey top-up) prints to the approved layout - 86 chars
- C4104768 | Ticket Format — Glider Format 13C (Top-up Expiry) prints to the approved layout - 79 chars
- C4104769 | Ticket Format — NIR Layout 12 (iLink Top-Up) prints to the approved layout - 74 chars
- C4105266 | Waybill Printing — continuing without printing exits the print-failure flow - 75 chars
- C4103951 | Single-Use Barcode — encryption keys are fetched once per shift at sign-on - 74 chars
- C4103952 | Single-Use Barcode — an encryption-key fetch failure does not block sign-on - 75 chars
- C4103953 | Single-Use Barcode — AES versus TripleDES is selected from the encrypted string - 79 chars
- C4103954 | Single-Use Barcode — a valid decrypt has exactly 17 commas and a known type - 75 chars
- C4103955 | Single-Use Barcode — a decrypt failure shows the decryption-failed message - 74 chars
- C4103956 | Single-Use Barcode — a manual 12-digit reference is validated as the ShortID - 76 chars
- C4103957 | Single-Use Barcode — a locally used ShortID is rejected before going online - 75 chars
- C4103958 | Single-Use Barcode — a redeemed barcode emits the Barcode Redemption event 1412 - 79 chars
- C4103959 | Single-Use Barcode — a redeem timeout queues offline and emits event 1416 - 73 chars
- C4103961 | Single-Use Barcode — the offline sweep redeems queued barcodes without CloudFare events - 87 chars
- C4105179 | Single-Use Barcode — a barcode failing the Single-Use format check shows Not Valid - 82 chars
- C4105183 | Single-Use Barcode — a barcode passing the offline limit check but failing validation shows Not Valid - 101 chars
- C4105184 | Single-Use Barcode — a Type U barcode with mismatched dates shows Ticket Valid inc. Date with Expiry and Depart Time - 116 chars
- C4105185 | Single-Use Barcode — a Type U barcode with matching dates shows Ticket Valid inc. Date and Depart Time - 102 chars
- C4105186 | Single-Use Barcode — a Type B or E barcode shows Ticket Valid inc. Date and Depart Time - 87 chars
- C4105187 | Single-Use Barcode — a Type D barcode shows Ticket Valid inc. 3 Use Times - 73 chars
- C4105188 | Single-Use Barcode — a Type H or S barcode shows Ticket Valid inc. Outbound and Return - 86 chars
- C4105189 | Single-Use Barcode — a ticket failing visual inspection shows Not Passed Visual Inspection - 90 chars
- C4103963 | Multi-Use Barcode — a route/location-only failure shows a yellow question mark - 78 chars
- C4103965 | Multi-Use Barcode — a re-presented barcode within the passback window is rejected - 81 chars
- C4103966 | Multi-Use Barcode — a rail location failure falls back to valid above the fare threshold - 88 chars
- C4103967 | Multi-Use Barcode — a successful validation audits a zero-fare BarcodeUsage transaction - 87 chars
- C4103968 | Multi-Use Barcode — a failed validation sends an event with the Unique ID - 73 chars
- C4103969 | Multi-Use Barcode — a midnight-to-4am expiry displays the previous day and no time - 82 chars
- C4105174 | Multi-Use Barcode — Rail location outside Boarding/Alighting shows Invalid Location - 83 chars
- C4105177 | Multi-Use Barcode — Scan from a result screen returns to barcode decryption check - 81 chars
- C4105269 | Barcode Ticket Printing — a successful print confirms transaction complete - 74 chars
- C4103972 | Smartcard Inspection — an adult iLink pass shows the adult colour on inspection - 79 chars
- C4103975 | Smartcard Inspection — a pass inspected within the transfer period is accepted - 78 chars
- C4103976 | Smartcard Inspection — a pass inspected after the transfer period offers revalidation - 85 chars
- C4104773 | Smartcard Inspection — a valid Blind concession is inspected successfully - 73 chars
- C4104774 | Smartcard Inspection — a valid War Pensioner concession is inspected successfully - 81 chars
- C4104775 | Smartcard Inspection — a valid 60 Plus concession is inspected successfully - 75 chars
- C4104776 | Smartcard Inspection — a valid ROI Senior Smartpass concession is inspected successfully - 88 chars
- C4104777 | Smartcard Inspection — a valid Learning Disability half-fare pass is inspected successfully - 91 chars
- C4104778 | Smartcard Inspection — a valid DLA half-fare pass is inspected successfully - 75 chars
- C4104779 | Smartcard Inspection — a valid No Driving Licence half-fare pass is inspected successfully - 90 chars
- C4104780 | Smartcard Inspection — a valid Partially Sighted half-fare pass is inspected successfully - 89 chars
- C4104781 | Smartcard Inspection — a valid PIPS half-fare pass is inspected successfully - 76 chars
- C4104783 | Smartcard Inspection — a valid EA Pupil/Further-Education (Bus & Rail) pass is inspected successfully - 101 chars
- C4104784 | Smartcard Inspection — a valid Discounted Youth (yLink) pass is inspected successfully - 86 chars
- C4105196 | Smartcard Inspection — swiping the mode toggle keeps the Inspection device view - 79 chars
- C4105197 | Smartcard Inspection — Rail Inspection/Validation toggle switches both ways - 75 chars
- C4105198 | Smartcard Inspection — unreadable card marked Faulty Smartpass routes to Top-Up Receipt Print - 93 chars
- C4105201 | Smartcard Inspection — direction mismatch within the transfer period shows Invalid - 82 chars
- C4105202 | Smartcard Inspection — direction mismatch outside the transfer period shows Invalid - 83 chars
- C4105204 | Smartcard Inspection — validating an Invalid card routes by Glider or Rail - 74 chars
- C4105207 | Smartcard Validation — Half-Fare card routes by Glider or Rail to Discount Sales mode - 85 chars
- C4105208 | Smartcard Validation — Concession Fare card routes by Glider or Rail to Concessionary Card sales mode - 101 chars
- C4105209 | Concessionary Card Sales — cross-border ticket type selection returns to Rail sales mode - 88 chars
- C4105210 | Concessionary Card Sales — no other ticket types keeps the current screen displayed - 83 chars
- C4105211 | Discount Sales — yLink alighting selection reaches Discount Summary and Payment Area - 84 chars
- C4105213 | Payment Area — cash or Warrant payment proceeds to print or Represent Smartcard - 79 chars
- C4105214 | Critical Error — cancelling after a used payment card voids the transaction - 75 chars
- C4103979 | Revenue Inspection — Inspection Mode is disabled on a non-Tap-On-Only route - 75 chars
- C4103980 | Revenue Inspection — a valid Visa Debit card inspection succeeds and emits event 5008 - 85 chars
- C4103984 | Revenue Inspection — an American Express card is declined as an unsupported scheme and emits event 5012 - 103 chars
- C4103985 | Revenue Inspection — no connection to the back office shows the try-again message - 81 chars
- C4103986 | Revenue Inspection — no card within 30 seconds times out to the Sales screen - 76 chars
- C4103988 | Revenue Inspection — the full RID List is requested on application start-up - 75 chars
- C4103990 | Revenue Inspection — the first poll after End-of-Day requests a full RID List - 77 chars
- C4104785 | Revenue Inspection — a valid Visa Credit card inspection succeeds and emits event 5008 - 86 chars
- C4104786 | Revenue Inspection — a valid Mastercard Credit card inspection succeeds and emits event 5008 - 92 chars
- C4104787 | Revenue Inspection — a valid Mastercard Debit card inspection succeeds and emits event 5008 - 91 chars
- C4104788 | Revenue Inspection — a valid Maestro card inspection succeeds and emits event 5008 - 82 chars
- C4104789 | Revenue Inspection — a Diners card is declined as an unsupported scheme and emits event 5012 - 92 chars
- C4105162 | Payment Device Update — fullscreen update shown, HHD actions still available - 76 chars
- C4103996 | Heartbeat — the HHD calls in at least every 15 minutes even when signed off - 75 chars
- C4103997 | Heartbeat — a StaffList message resets Hours Since Last Communication to zero - 77 chars
- C4105159 | Additional Features — HHD shows Device Out of Service on a critical issue - 73 chars

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
