# Alignment audit - suite 30254

- Cases audited: **455**
- Blocking findings: **0**
- Advisory (reviewed-intentional) findings: **76**

## Residual mojibake in any field - 0
_none_

## Title missing the ' - ' feature separator _(advisory)_ - 9
- C4100524 | Driver Sign Off
- C4100648 | ETM continues working when the BOS connection is lost
- C4100649 | Download configuration files from the back office
- C4100650 | Software distribution and fare-mode transition
- C4100651 | Upload audit files and data to the back office
- C4100654 | Auto sign-off
- C4100655 | MIFARE card type validation on the ETM
- C4100656 | Smartcard and EMV transaction timings
- C4100657 | Interface with other on-vehicle third-party equipment

## Title over 72 chars _(advisory)_ - 67
- C4100514 | Driver Sign On — incorrect PIN locks the device after the configured attempts - 77 chars
- C4100515 | Driver Sign On — communications locked / not communicating with CloudFare - 73 chars
- C4103553 | Transfer — the ETM decides transfer vs journey from the ROUTE Transfer Time - 75 chars
- C4103554 | Transfer — a stop outside the Metro Transfer Zone is charged as a journey - 73 chars
- C4103556 | Transfer — a transfer audits WTS SmartTransfer while a journey audits WTS SmartUse - 82 chars
- C4103546 | Rail Substitution — GPS auto-advances the boarding stop with widened tolerances - 79 chars
- C4103548 | Rail Substitution — the back office ignores PJT but applies MJT on a rail-sub journey - 85 chars
- C4103552 | Shift Board — import sets Valid From at 4am and purges entries older than 7 days - 80 chars
- C4103557 | ABT Audit — a TOO tap records ABT payment, zero revenue and product id 7000 - 75 chars
- C4100661 | Screen Validation — 12.1.1 - Barcode Scan - Transaction Cancelled - Ticket Not Valid - 84 chars
- C4100662 | Screen Validation — 12.1.2 - Barcode Scan - Transaction Cancelled - Ticket Not Passed Visual Inspection - 103 chars
- C4100667 | Screen Validation — 12.5.1 - Barcode Scan - Ticket Valid inc. Date and Depart Time - 82 chars
- C4100668 | Screen Validation — 12.5.2 - Barcode Scan - Ticket Valid inc_ Date with Expiry and Depart Time - 94 chars
- C4100669 | Screen Validation — 12.5.3 - Barcode Scan - Ticket Valid inc_ Outbound ands Return - 82 chars
- C4100670 | Screen Validation — 12.5.3.1 - Barcode Scan - Ticket Valid inc_ Outbound ands Return - Page 2 - 93 chars
- C4100671 | Screen Validation — 12.5.4 - Barcode Scan - Ticket Valid inc_ 3 Use Times - 73 chars
- C4100672 | Screen Validation — 12.5.4.1 - Barcode Scan - Ticket Valid inc_ 3 Use Times - Page 2 - 84 chars
- C4100674 | Screen Validation — 05.0.1 - FLU - Smartcard Top Up - No Journeys Left Error - 76 chars
- C4100718 | Screen Validation — 08.0.2.2 - Driver Menu - Annulment Successful - Smartcard - 77 chars
- C4100719 | Screen Validation — 08.0.2.3 - Driver Menu - Annulment unsuccessful - Incorrect Card - 84 chars
- C4100738 | Screen Validation — 08.2.1 - Driver Menu - Ticket History - View Ticket - Annulled - 82 chars
- C4100741 | Screen Validation — 08.4.0 - Driver Menu - Display Settings - Brightness and Volume - 83 chars
- C4100744 | Screen Validation — 08.6.1 - Driver Menu - Word and Colour of the Day - Unavailable - 83 chars
- C4100757 | Screen Validation — 02.0.2.1 | Main Screen - FLU - Change Boarding Stage 2 - 74 chars
- C4100770 | Screen Validation — 02.1.0.1 | Toggle Group - Group - Alighting Stage Selected - 78 chars
- C4100775 | Screen Validation — 02.1.3 Flu Product Selected - Alighting Stage Selected - 74 chars
- C4100787 | Screen Validation — 02.6.4 | EMV Validation Failure - Card has been declined - 76 chars
- C4100788 | Screen Validation — 02.6.5 | EMV Validation Failure - Card already validated - 76 chars
- C4100789 | Screen Validation — 02.7 | Main Screen - FLU - Multiple Items - Basket Mode Selected - 84 chars
- C4100790 | Screen Validation — 02.7.1 | Main Screen - FLU - Multiple Items - 1 Ticket Chosen - 81 chars
- C4100791 | Screen Validation — 02.7.2 | Main Screen - FLU - Multiple Items - Basket - Page 1 - 81 chars
- C4100792 | Screen Validation — 02.7.2.1 | Main Screen - FLU - Multiple Items - Basket - Euros - 82 chars
- C4100793 | Screen Validation — 02.7.3 | Main Screen - FLU - Multiple Items - Basket - Page 2 - 81 chars
- C4100794 | Screen Validation — 02.7.3.1 | Main Screen - FLU - Multiple Items - Basket - Delete Item - 88 chars
- C4100795 | Screen Validation — 02.7.3.2 | Main Screen - FLU - Multiple Items - Basket - Quantity Error - 91 chars
- C4100796 | Screen Validation — 02.7.4 | Main Screen - FLU - Multiple Items - Basket - Item Deleted - 87 chars
- C4100797 | Screen Validation — 02.7.5 | Main Screen - FLU - Multiple Items - Basket - Confirmed - 84 chars
- C4100798 | Screen Validation — 02.7.8 | Main Screen - FLU - Multiple Items - Basket is Full - 80 chars
- C4100799 | Screen Validation — 02.7.8.1 | Main Screen - FLU - Multiple Items - Basket Full - Error - 87 chars
- C4100804 | Screen Validation — 2.5.2 | Main Screen - Last Transaction - Multiple Tickets in Basket - Success - 97 chars
- C4100808 | Screen Validation — 04.0.1.2 | Numeric Entry - 9017 - Change & Alighting - Error Bar - 84 chars
- C4100809 | Screen Validation — 04.0.1.3 | Main Screen - FLU - 9017 Alighting Stage Chosen - 78 chars
- C4100820 | Screen Validation — 07.0.6.1 - Main Screen - Travel Mode - Schedule Adherence - Outside Set Times - 97 chars
- C4100821 | Screen Validation — 07.0.6.2 - Main Screen - Travel Mode - Schedule Adherence - In Set Times - 92 chars
- C4100838 | Screen Validation — 00.0.0 | Adult Single - Issuance - Alighting Selected - 73 chars
- C4100839 | Screen Validation — 00.0.0 | Child Single - Issuance - Alighting Selected - 73 chars
- C4100852 | Screen Validation — 01.2.0 - Sign On Details Entered - First Use Safety Check - 77 chars
- C4100853 | Screen Validation — 01.2.1 - Sign on Details Entered - First Use Safety Check On Board - 86 chars
- C4100854 | Screen Validation — 01.2.2 - Sign on Details Entered - There Must be a First Use Safety Check - 93 chars
- C4100855 | Screen Validation — 01.2.3 - Sign on Details Entered - Bus Check - Any Defects - 78 chars
- C4100861 | Screen Validation — 01.4.2 - Type Route - With Letters - Hiddent - 10 Typed - 75 chars
- C4100865 | Screen Validation — 01.4.5 - Type Route - With Number - Outbound Filtered - 73 chars
- C4100885 | Screen Validation — 06.0.1.3 - FLU - Smartcard Top Up - Error - Remove Smartcard - 80 chars
- C4100888 | Screen Validation — 06.0.10.1 - FLU Product - Alighting Stage selected - ABT - 76 chars
- C4100889 | Screen Validation — 06.0.2.0 -  FLU - Smartcard - Faulty - Select Card Type - 75 chars
- C4100890 | Screen Validation — 06.0.3.0 -  FLU - Smartcard - Faulty - Charge Full Fare - 75 chars
- C4100893 | Screen Validation — 06.0.5.1 - FLU Product - Alighting Stage selected - yLink - 77 chars
- C4100894 | Screen Validation — 06.0.5.3 - FLU Product - Alighting Stage selected - yLink - Basket - Added - 94 chars
- C4100896 | Screen Validation — 06.0.7.0 -  Main Screen - FLU - Free Product - Notification - 79 chars
- C4100905 | Screen Validation — 09.3.2.1 Supervisor Menu - Waybills - Detailed - Page 2 - 75 chars
- C4100910 | Screen Validation — 09.5.3.1 Supervisor Menu - Configuration Versions - Page 2 - 78 chars
- C4100913 | Screen Validation — 10.1.1 - Technician - Device Settings - Edit Input Field - 76 chars
- C4100914 | Screen Validation — 10.1.1.2 - Technician - Device Settings -Confirm Input - 74 chars
- C4100915 | Screen Validation — 10.1.2 - Technician - Device Settings - Edit Home Location - 78 chars
- C4100916 | Screen Validation — 10.1.3 - Technician - Device Settings - Home location not available - 87 chars
- C4100922 | Screen Validation — 10.3.3.1 - Technician - Card Reader - Smartcard Details - 75 chars
- C4100935 | Screen Validation — 10.7.3.1 - Technician Menu - Configuration Versions - Page 2 - 80 chars

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
