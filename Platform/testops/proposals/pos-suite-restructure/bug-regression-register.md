# Bug-regression register - Translink POS (from `AA-POS Acceptance Test`)

Auto-extracted 247 distinct `TIBU` defects that have a confirmation/regression test in
the old suite (bug id taken from the case title). **Goal:** ensure every one is pinned in the new
suite `GG - POS - Claude Suite` - either by folding a **regression step** into the relevant
functional case, or by a dedicated **regression case** - organised by behaviour (not by release),
and linked via the **Refs** field (`TIBU-#####`), not the title.

Fill "New coverage" during the build: `fold into C<new>` | `new regression case` | `covered by <area>` | `obsolete (leave)`.

| TIBU | Old case | Release | Bug summary | Functional area (TBD) | New coverage (TBD) |
|---|---|---|---|---|---|
| TIBU-30634 | C4094862 | 1.3.12 | - POS/Cloudfare - Shift Annul Ticket Total 0 even with Annullments | | |
| TIBU-30633 | C4094861 | 1.3.12 | - Sign on Failed (Break Mode) - Text Mispelling | | |
| TIBU-29752 | C4094859 | 1.3.12 | - Power Cycle / Soft Reboot during Shift | | |
| TIBU-29484 | C4094860 | 1.3.12 | - POS/Cloudfare - EOS Cash Total is Gross (Rather than Net) | | |
| TIBU-28530 | C4091944 | 1.3.11 | - Device fails to enter Comms Lock state after exceeding configured Comms Lock period | | |
| TIBU-27664 | C4091892 | 1.3.11 | - POS v.1.3.10 > Randomly went Comms Locked | | |
| TIBU-27444 | C4083463 | 1.3.10 | Operator Menu- Ticket History- cannot scroll to the second page | | |
| TIBU-27443 | C4083465 | 1.3.10 | Supervisor Duty Information- cannot scroll through the duties | | |
| TIBU-26995 | C4079311 | 1.3.10 | TL POS : Paper Low Not Being Displayed | | |
| TIBU-26931 | C4079310 | 1.3.10 | POS > Issue Card > Metro Travelcard Expiry Date Missing | | |
| TIBU-26930 | C4079309 | 1.3.10 | POS > Issue Card > iLinks Expiry Date Missing | | |
| TIBU-26905 | C4079308 | 1.3.10 | TL POS : Add ability to manually adjust Ethernet network settings from Technician Menu | | |
| TIBU-26880 | C4079307 | 1.3.10 | POS > Merit > Product Class Issues | | |
| TIBU-26872 | C4079322 | 1.3.10 | POS > UX Screen > Ilink Issue Flow > Screen 8.3.7 | | |
| TIBU-26871 | C4079321 | 1.3.10 | POS > UX Screen > BVP Issue Flow > Screen 8.3.5 | | |
| TIBU-26865 | C4079320 | 1.3.10 | POS > UX Screen > Daylink Issue Flow > Screen 8.3.4 | | |
| TIBU-26864 | C4079319 | 1.3.10 | POS > UX Screen > Metro MJ Issue Flow > Screen 8.7.1 | | |
| TIBU-26863 | C4079318 | 1.3.10 | POS > UX Screen > Metro Travelcard Issue Flow > Screen 8.7.2 | | |
| TIBU-26862 | C4079317 | 1.3.10 | POS > UX Screen > Ulsterbus Town Service Top-Up > Screen 7.5.6 | | |
| TIBU-26861 | C4079316 | 1.3.10 | POS > UX Screen > Ulsterbus MJ Top-Up > Screen 7.5.7 | | |
| TIBU-26860 | C4079315 | 1.3.10 | POS > UX Screen > Metro Travelcard Top-Up > Screen 7.5.8 | | |
| TIBU-26859 | C4079314 | 1.3.10 | POS > UX Screen > Ilink Top-Up Flow > Screen 7.5.11 | | |
| TIBU-26858 | C4079313 | 1.3.10 | POS > UX Screen > BVP/Ilink Top-Up Flow > Screen 7.5.10 | | |
| TIBU-26857 | C4079312 | 1.3.10 | POS > UX Screen > Daylink Top-Up Flow > Screen 7.5.9 | | |
| TIBU-26855 | C4078980 | 1.3.10 | POS > Driver Break causes Out Of Service | | |
| TIBU-26846 | C4078979 | 1.3.10 | POS > Out Of Service from Sign off | | |
| TIBU-26845 | C4082847 | 1.3.10 | POS > Issuing Blank Card > Please wait loop | | |
| TIBU-26763 | C4078978 | 1.3.10 | POS > Randomly crashes & automatically reboots | | |
| TIBU-26760 | C4078977 | 1.3.10 | POS > Card issued from blank on New POS > Unsuccessful issue / annulment | | |
| TIBU-26727 | C4078976 | 1.3.10 | POS > 1.3.9 > DayLink displaying "Card Not Used" messaging incorrectly | | |
| TIBU-26723 | C4078975 | 1.3.10 | POS > Printer Jam screens appearing on first shift of the day | | |
| TIBU-26722 | C4078974 | 1.3.10 | POS > Card issued from blank on Legacy POS > Attempt to Top-Up | | |
| TIBU-26721 | C4078973 | 1.3.10 | POS > Card issued from blank on New POS > Attempt to Top-Up | | |
| TIBU-26720 | C4078972 | 1.3.10 | POS > Unable to Top-up > AD/CH Ulsterbus Townservice (travel activated) | | |
| TIBU-26713 | C4078971 | 1.3.10 | POS > Card from first use > AD/CH Ulsterbus Townservice | | |
| TIBU-26648 | C4078970 | 1.3.10 | POS > Stuck on Please Wait screen | | |
| TIBU-25935 | C4075926 | 1.3.9 | Device freeze on 'Please wait' screen on startup | | |
| TIBU-25891 | C4075925 | 1.3.9 | POS > Issuing Blank Card > Metro Multi-Journey > 40 Journey Name | | |
| TIBU-25890 | C4075924 | 1.3.9 | POS > Issuing > Top-Up option cut short | | |
| TIBU-25889 | C4075921 | 1.3.9 | POS > Annulment > Annulment card type is cut short | | |
| TIBU-25888 | C4075920 | 1.3.9 | POS > Annulment > Annulment title is incorrect | | |
| TIBU-25886 | C4075918 | 1.3.9 | POS > Smartlinks > Cannot Top-Up Journeys if a card has expired journeys | | |
| TIBU-25885 | C4075917 | 1.3.9 | POS > Issuing Blank Card > Metro Multi-Journey > Back button non responsive | | |
| TIBU-25826 | C4073950 | 1.3.9 | POS > Please Wait infinite loop | | |
| TIBU-25825 | C4073949 | 1.3.9 | POS > Please Wait Freeze | | |
| TIBU-25818 | C4073948 | 1.3.9 | POS - No "Cancel" button on faulty smartcard screen | | |
| TIBU-25800 | C4073855 | 1.3.9 | TL POS Metro - Incorrect Journey's on card  on Annulment receipts for iLink & Metro Travel | | |
| TIBU-25617 | C4073115 | 1.3.9 | TL POS: Unable to create a product on a blank Child Daylink card | | |
| TIBU-25615 | C4073114 | 1.3.9 | TL POS: Unable to issue a topup for a Metro travelcard | | |
| TIBU-25404 | C4073113 | 1.3.9 | TL POS Metro- Incorrect Journey's on card and Journeys cancelled on Annulment receipts for | | |
| TIBU-25402 | C4073112 | 1.3.9 | TL POS Metro - Annulment receipts for card top's are missing TrayID in the receipt | | |
| TIBU-25148 | C4072846 | 1.3.8 | POS > Ghost Buttons > Ilink (all zones) | | |
| TIBU-25116 | C4072845 | 1.3.8 | POS > Cancelled Tickets information is incorrect | | |
| TIBU-25100 | C4072844 | 1.3.8 | POS > CH Metro Travelcards > Unable to Annul Top-Up | | |
| TIBU-25099 | C4072839 | 1.3.8 | POS > Metro Travelcards > Unable to top-up with travel | | |
| TIBU-25098 | C4072843 | 1.3.8 | POS > Metro Travelcards > Expired cards only showing the last topped up option | | |
| TIBU-25081 | C4072842 | 1.3.8 | POS > Incorrect Expiry text showing for Metro MJ Mini Statement | | |
| TIBU-25078 | C4072841 | 1.3.8 | POS > Travlecard from first use > not showing correct error screen | | |
| TIBU-25077 | C4072840 | 1.3.8 | POS > Slow Device Performance | | |
| TIBU-25073 | C4072838 | 1.3.8 | POS > Re-presenting a different card during the Annul last transaction gets device stuck i | | |
| TIBU-25072 | C4072837 | 1.3.8 | POS > Multijourney smartcards > Annul Tickets showing 0 journeys cancelled | | |
| TIBU-25071 | C4072836 | 1.3.8 | POS > Tray ID reporting incorrectly on Cloudfare | | |
| TIBU-24891 | C4078787 | 2.0.X | TL POS- POS didnt signoff automatically | | |
| TIBU-24890 | C4078786 | 2.0.X | TL POS- If a ticket template isnt available to print a ticket , device should show a print | | |
| TIBU-24889 | C4078785 | 2.0.X | TL POS- Device status is sent as 'Not Defined' on Cloudfare | | |
| TIBU-24888 | C4078784 | 2.0.X | TL POS - Peripheral Device message for M010 gets sent to CloudFare even though no M020 con | | |
| TIBU-24886 | C4078783 | 2.0.X | TL POS Rail- Pressing Cancel on the Overwrite favorite screen should go back to Rail FLU | | |
| TIBU-24884 | C4078782 | 2.0.X | TL POS- Ticket history is missing up and down arrows to view more | | |
| TIBU-24879 | C4078781 | Bus? | TL POS- Bus No exist in the corner of operator break when it shouldnt | | |
| TIBU-24878 | C4078780 | 2.0.X | TL POS- 'No ticket to Annul' should be greyed out | | |
| TIBU-24876 | C4078779 | 2.0.X | TL POS Rail- Pressing Back button from payment screen for a single ticket that wasn't in t | | |
| TIBU-24870 | C4078778 | 2.0.X | TL POS- Software versions send separate versions rather than a batch at once | | |
| TIBU-24869 | C4078777 | 2.0.X | TL POS- User should be able to increase or decrease Brightness and Volume from the Technic | | |
| TIBU-24868 | C4078747 | 2.0.0 | TL POS Rail - Ability to change the operating mode from Technician Menu | | |
| TIBU-24866 | C4078776 | Delete | TL POS- Changes need to be done to Device settings UI | | |
| TIBU-24865 | C4078775 | 2.0.X | TL POS Rail-Issuing a ticket that isn't adult single reverts the Rail FLU screen to Adult  | | |
| TIBU-24864 | C4078746 | 2.0.0 | TL POS Rail- Need to remove 'Bus' and ''Day Tours' button from Main screen | | |
| TIBU-24862 | C4078774 | 2.0.X | TL POS Rail- Layout of the boarding/alighting/ticket type fields does not match the UX on  | | |
| TIBU-24860 | C4078773 | 2.0.X | TL POS Rail- Add more to basket button is still available even if basket is full | | |
| TIBU-24858 | C4078772 | 2.0.X | TL POS Rail- Cancelling a Topup from Rail FLU screen , the screen goes back to Main Screen | | |
| TIBU-24855 | C4078771 | 2.0.X | TL POS - Route reference id is not being audited in the transactions | | |
| TIBU-24853 | C4078770 | 2.0.X | TL POS Rail- Device is auditing wrong boarding , alighting stations and purchase locations | | |
| TIBU-24848 | C4078745 | 2.0.0 | TL POS Rail - Alignment of RAIL ticket templates with revised naming conventions | | |
| TIBU-24845 | C4078744 | 2.0.0 | TL POS- Passenger display not working | | |
| TIBU-24837 | C4078743 | 2.0.0 | TL POS Rail-  User should be able to use '+' and '-' button to increment or decrement the  | | |
| TIBU-24834 | C4078769 | 2.0.X | TL POS - Rail - Investigate payment device | | |
| TIBU-24829 | C4078742 | 2.0.0 | TL POS Rail- 3 Day Select product doesn't allow the user to select the 3 dates | | |
| TIBU-24828 | C4078768 | 2.0.X | TL POS Rail- On Rail FLU Screen ,operator will be able to press the UP and down buttons to | | |
| TIBU-24827 | C4078767 | 2.0.X | TL POS Rail- On Rail FLU Screen ,operator will be able to press the left and right buttons | | |
| TIBU-24826 | C4078766 | 2.0.X | TL POS Rail- If an advanced ticket is added to a basket you should not be able to add any  | | |
| TIBU-24810 | C4078765 | 2.0.X | TL POS Rail- Pressing 'C' button on any FLU screen should return to main screen | | |
| TIBU-24804 | C4078764 | 2.0.X | TL POS Rail- Operator Menu- Excess Ticket Feature doesnt exist | | |
| TIBU-24800 | C4078741 | 2.0.0 | TL POS: Day summary Print out does not include details of any Cards issued | | |
| TIBU-24795 | C4078740 | 2.0.0 | TL POS Rail - Presenting a half fare/concession smartcard is saying Card not recgonised fr | | |
| TIBU-24792 | C4078739 | 2.0.0 | TL POS: Technician Mode: Please Present Smartcard to Test Screen has additional text | | |
| TIBU-24790 | C4078738 | 2.0.0 | TL POS: Cloudfare is recording two instances of Forced Signoff in Administrator Mode. | | |
| TIBU-24786 | C4078737 | 2.0.0 | TL POS: Supervisor Menu/Sales Breakdown Print & Zero Accumulated and Print & Zero Current  | | |
| TIBU-24785 | C4078736 | 2.0.0 | TL POS: Supervisor Menu/Day Information print out displays 7 Shifts but the screen only di | | |
| TIBU-24783 | C4078735 | 2.0.0 | TL POS  Rail- Selecting a favourite should trigger the payment screen to be displayed | | |
| TIBU-24781 | C4078763 | 2.0.X | TL POS Rail- Ticket details are not shown on the screen if you go to the payment screen fr | | |
| TIBU-24778 | C4078762 | 2.0.X | TL POS Rail- Warrant button is not shown for tickets/smartcard top ups/smartcard issues | | |
| TIBU-24776 | C4078761 | 2.0.X | TL POS- Rail - Overwriting a favourite ticket the favourite slot number is shown as {0} on | | |
| TIBU-24774 | C4078732 | 2.0.0 | TL POS Rail - Pressing R3 Button should show the list of all passenger types | | |
| TIBU-24740 | C4078731 | 2.0.0 | TL POS: Administrator Mode - Network Settings, nothing happens when a button is pressed ad | | |
| TIBU-24727 | C4066722 | 1.3.7 | TL POS: Operator Options - Pressing the Cancel Button when on Soft Reboot Screen takes the | | |
| TIBU-24718 | C4066723 | 1.3.7 | TL POS: Ticket History for an annulled card issue should include the card deposit | | |
| TIBU-24715 | C4066724 | 1.3.7 | TL POS: POS stuck on Card Write Failed Screen | | |
| TIBU-24379 | C4066694 | 1.3.6 | TL POS: Sign on Screen: The ID is missed out and the POS goes directly to the PIN | | |
| TIBU-24368 | C4078760 | 2.0.X | TL POS Rail - Clear Basket button doesn't work | | |
| TIBU-24364 | C4078759 | 2.0.X | TL POS Rail- button Missing from Basket Screen | | |
| TIBU-24350 | C4066693 | 1.3.6 | TL POS: Selecting the Top Up Option on a Metro Travelcard results in the POS not moving to | | |
| TIBU-24340 | C4066705 | 1.3.6 | TL POS: Selecting the Top Up Option on a Metro Travelcard results in the POS not moving to | | |
| TIBU-24335 | C4078758 | 2.0.X | TL POS: Entering Operator Break Mode is missing a confirm screen | | |
| TIBU-24334 | C4066692 | 1.3.6 | TL POS: Annulling a Newly issued Smartcard results in the POS only printing an Annulment o | | |
| TIBU-24332 | C4066691 | 1.3.6 | TL POS: Leaving the POS on any Ticket History Screen results in a fatal error and the POS  | | |
| TIBU-24329 | C4066690 | 1.3.6 | TL POS: Ticket History does not include any information | | |
| TIBU-24328 | C4066689 | 1.3.6 | TL POS: Stuck on Please wait screen when adding to an iLink or BVP Smartcard | | |
| TIBU-24273 | C4062644 | Delete | (see case) | | |
| TIBU-24146 | C4066688 | 1.3.6 | TL POS- Ticket details are not displayed when accessed via the "Ticket History" button. | | |
| TIBU-24098 | C4078757 | 2.0.X | TL POS - Rail- Incorrect basket checkout amount | | |
| TIBU-24095 | C4078756 | 2.0.X | TL POS Rail- Overwriting Favourite ticket will throw a 'Fatal Error' | | |
| TIBU-24051 | C4062645 | 1.3.5 | TL POS: Topping up an Adult MJ Inner Zone Card caused the POS to Crash and restart | | |
| TIBU-24026 | C4078730 | 2.0.0 | TL POS: Default Boarding Stage: Pressing the "*" Button results in no keys working until t | | |
| TIBU-23996 | C4062646 | 1.3.5 | TL POS: Metro Multi Journey Cards created on the POS are not being accepted on the ETM | | |
| TIBU-23992 | C4062647 | 1.3.5 | TL POS: Child BVP and iLink Zone 1 cards do not offer options when blank card is presented | | |
| TIBU-23990 | C4062648 | 1.3.5 | TL POS: iLink Cards only have one top up value available | | |
| TIBU-23989 | C4062649 | 1.3.5 | TL POS: Metro Travel Card mini statement print does not have expiry date | | |
| TIBU-23963 | C4062650 | Delete | (see case) | | |
| TIBU-23949 | C4062651 | 1.3.5 | TL POS: Annulment ticket is not printed for a new card which causes a fatal error message | | |
| TIBU-23936 | C4062652 | 1.3.5 | TL POS: Sales Breakdown Report Accumulated print out includes 'Paper Tickets' when it shou | | |
| TIBU-23932 | C4062653 | 1.3.5 | TL POS: Annulment receipts doesn't print the correct information | | |
| TIBU-23928 | C4062654 | 1.3.5 | TL POS: Pressing 'Back' button on 'Paper Status' screen will throw a Fatal Error | | |
| TIBU-23835 | C4062655 | 1.3.5 | TL POS : Ensure the correct ticket template is used for printing historic duty information | | |
| TIBU-23096 | C4056172 | 1.3.3 | Issue with TL Test POS Failing to load fonts or print tickets | | |
| TIBU-23091 | C4066684 | 1.3.6 | TL POS: Pressing Ticket History causes the POS to reboot | | |
| TIBU-23016 | C4056196 | 1.3.4 | TL POS-Device doesn't print receipts for Top-up's | | |
| TIBU-23009 | C4062658 | 1.3.5 | TL POS Metro- Metro Multi Journey Issue doesnt match the UX flow | | |
| TIBU-22985 | C4056195 | 1.3.4 | TL POS Rail- Unable to Top up/Issue smartcards | | |
| TIBU-22963 | C4056194 | 1.3.5 | TL POS : Confirm process for cellular connection/configuration | | |
| TIBU-22953 | C4078754 | 2.0.X | TL POS Rail- List of Boarding and Alighting stations are not shown | | |
| TIBU-22824 | C4078753 | 2.0.X | TL POS Rail - Advance Ticket - Invalid Date | | |
| TIBU-22672 | C4056193 | 1.3.4 | TL POS: Sign on - Device Locked screen incorrect | | |
| TIBU-22671 | C4056192 | 1.3.4 | TL POS: Sign on - Incorrect Details screen is incorrect | | |
| TIBU-22649 | C4056191 | 1.3.4 | TL POS: Technician Menu - There are additional Options to be able to choose from | | |
| TIBU-22647 | C4056190 | 1.3.4 | TL POS: Day Information Screen does not have instructions to use the Chevron Keys [Up and  | | |
| TIBU-22643 | C4056189 | Delete | TL POS: Duty Information Screen does not have instructions to use the Chevron Keys [Up and | | |
| TIBU-22640 | C4056188 | 1.3.4 | TL POS: Operator Options has additional 'Report Faulty Payment Device' option | | |
| TIBU-22632 | C4056187 | 1.3.4 | TL POS: Administrator Menu: Default Boarding Stage, and Mounting Point have the prefix AT | | |
| TIBU-22603 | C4056186 | 1.3.4 | TL POS: A Daylink Card created on the POS is not recognised by an ETM. | | |
| TIBU-22578 | C4056185 | 1.3.4 | TL POS: Unable to create any new Metro Multi Journey Cards | | |
| TIBU-22563 | C4073110 | 1.3.9 | TL POS: Pressing the 'C' Button when on the Sign in Screen following operator Break does n | | |
| TIBU-22558 | C4056184 | 1.3.4 | TL POS: The onscreen Mini Statement does not show Card Type, number , start date, expiry d | | |
| TIBU-22557 | C4056183 | 1.3.4 | TL POS: Metro Multi-journey Card is printing out 2 receipts when topped up, 1 is removing  | | |
| TIBU-22548 | C4056182 | 1.3.4 | TL POS: Daylink Child 'Blank' issues 2 receipts when days added to card | | |
| TIBU-22546 | C4056181 | 1.3.4 | TL POS: Pressing Back Button on BVP or iLink zone 1 'Blank Card' on top up amount displays | | |
| TIBU-22545 | C4056180 | 1.3.4 | TL POS: Transactions are not appearing in Smartrack | | |
| TIBU-22398 | C4056179 | 1.3.4 | TL POS - Card TopUp - Causing Incorrect Mini-Statement info on TVM and ETM | | |
| TIBU-22003 | C4049269 | 1.3.2 | TL POS - Pin lock is removed by rebooting device | | |
| TIBU-21992 | C4049268 | 1.3.2 | TL POS - TopUp - Topping Up a multijourney card does not show topup amount and cost on Rec | | |
| TIBU-21933 | C4057173 | 2.0.0 | TL POS Rail - Presenting a Smartcard on the Flu Screen causes a Fatal error | | |
| TIBU-21825 | C4049267 | 1.3.2 | TL POS - Incorrect ESN from the CLess Stack when reading the card's customer area | | |
| TIBU-21792 | C4057172 | 2.0.0 | TL POS Rail - "Advance Ticket" crashing and resetting device | | |
| TIBU-21786 | C4057171 | 2.0.0 | TL POS Rail - Smartcard Screen - Cannot Return to Rail Flu screen | | |
| TIBU-21779 | C4057170 | 2.0.0 | TL POS Rail - Flu Screen - R1 to R4 Crashing device | | |
| TIBU-21777 | C4057169 | 2.0.0 | TL POS Rail - Flu Screen - Unable to go to Basket | | |
| TIBU-21771 | C4057167 | 2.0.0 | TL POS Rail - Numerical Input for Boarding/Alighting not working | | |
| TIBU-21770 | C4057168 | 2.0.0 | TL POS Rail - Flu Screen - (L4) Text just says "example" even when pressed and *light disp | | |
| TIBU-21581 | C4048596 | 1.3.2 | TL POS: Mini Statement is not displaying the correct information on screen or when Printed | | |
| TIBU-21463 | C4048597 | 1.3.2 | TL POS: An Expired Multi Journey does not print any receipts when topped up | | |
| TIBU-21450 | C4056177 | 1.3.4 | TL POS: Mini Statement on an ETM is not showing top ups produced on POS | | |
| TIBU-21447 | C4048598 | 1.3.2 | TL POS: Device Log Manger is not configured for the POS | | |
| TIBU-21446 | C4048599 | 1.3.2 | TL POS: A 'Blank' New Multi-Journey Card created on the POS is not accepted on the ETM | | |
| TIBU-21443 | C4048600 | 1.3.2 | TL POS: A New Adult Belfast Visitors Pass is unable to be annulled | | |
| TIBU-21441 | C4048601 | 1.3.2 | TL POS: Child Daylink 'Blank' Card when put onto POS displays Invalid Smartcard Screen | | |
| TIBU-21440 | C4048602 | 1.3.2 | TL POS: Logging out of Operator caused the POS to reboot | | |
| TIBU-21430 | C4048603 | 1.3.2 | TL POS: New Adult or Child Multi Journey Card creation does not work | | |
| TIBU-21411 | C4048604 | 1.3.2 | TL POS: The time being displayed by the POS is one hour in the future | | |
| TIBU-21397 | C4048605 | 1.3.2 | TL POS: 'BRReportTransactionSequenceIdsOutOfSync' in the logs is causing the POS to go out | | |
| TIBU-21384 | C4048606 | 1.3.2 | TL POS: Device in a locked State cannot be unlocked with a Supervisor Card | | |
| TIBU-21367 | C4056176 | Delete | TL POS: Supervisor - Duty Information - Details page is not displayed when selecting a Dut | | |
| TIBU-21325 | C4056175 | 1.3.4 | TL POS - Supervisor Duty Information - Individual Duty's unviewable | | |
| TIBU-21323 | C4056174 | 1.3.4 | TL POS - Supervisor Menu - Duty Information Screen missing Text "Up or Down" | | |
| TIBU-21280 | C4051533 | 1.3.2 | TL POS - Card TopUps - After "Please Remove Smartcard" Screen changes to "No word Defined" | | |
| TIBU-21278 | C4048607 | 1.3.2 | TL POS: a POS that has been Communication Locked is capable of being brought back into ser | | |
| TIBU-21277 | C4048608 | 1.3.2 | TL POS: Keycloak token was 'lost' causing POS to enter 'Out of Service' Mode | | |
| TIBU-21266 | C4048609 | 1.3.2 | TL POS: Issue Cards - No Receipts Printing | | |
| TIBU-21264 | C4048610 | 1.3.2 | TL POS: Card Issue - Child iLink Zone 1/Belfast Visitors Pass- Cannot Issue | | |
| TIBU-21256 | C4048611 | 1.3.2 | TL POS: Faulty Smartcard - "Issue Receipt" button does nothing | | |
| TIBU-21219 | C4051534 | 1.3.2 | TL POS: Presenting a card that does not have the ability to be topped up causes the POS to | | |
| TIBU-21208 | C4040423 | 1.3.1 | TL POS - Issue Cards - Invalid Price being pulled from database | | |
| TIBU-21184 | C4048612 | 1.3.2 | TL POS iLink Top ups are not showing on mini statement | | |
| TIBU-21178 | C4048613 | 1.3.2 | TL POS iLink Top Up Receipt is not long enough | | |
| TIBU-21176 | C4048614 | 1.3.2 | TL POS: Does not print out a receipt for a Child Travel Card | | |
| TIBU-21138 | C4048615 | 1.3.2 | TL POS: Supervisor Menu: Pressing the Duty Information Button causes the POS to Reboot | | |
| TIBU-21135 | C4048616 | 1.3.2 | TL POS: No Transactions are printing out a receipt | | |
| TIBU-21133 | C4048617 | 1.3.2 | TL POS: All Metro Multi-Journey Card allow more than 50 journeys to be added to Card | | |
| TIBU-21129 | C4078752 | 2.0.X | TL POS: Display Settings Screen shows no indication of what level Brightness and Volume ar | | |
| TIBU-21122 | C4040424 | 1.3.1 | TL POS: Transactions do not appear in Merit | | |
| TIBU-21121 | C4048620 | 1.3.2 | TL POS: All Transactions in Cloudfare have the same number | | |
| TIBU-21119 | C4072835 | 1.3.8 | TL POS: The Description of any Card during Top up process in incorrect | | |
| TIBU-21118 | C4048621 | 1.3.2 | TL POS: Unable to update Software from Cloudfare. The only way to update was to drop the f | | |
| TIBU-21117 | C4040425 | 1.3.1 | TL POS: Topping up and Printing a Mini Statement for an Adult Daylink Card caused the POS  | | |
| TIBU-21115 | C4040429 | 1.3.1 | TL POS - Adult Metro Travelcard TopUp Error | | |
| TIBU-21110 | C4040430 | 1.3.1 | TL POS - Supervisor Menu - Duty Information resets device | | |
| TIBU-21096 | C4048622 | 1.3.2 | TL POS: Technician menu, Force Comms causing Fatal Error | | |
| TIBU-20980 | C4048623 | 1.3.2 | TL POS: Metro - Paper Jam Screen Annulment | | |
| TIBU-20967 | C4048624 | 1.3.2 | TL POS - Tray ID Field is not prefixed with "AT" | | |
| TIBU-20914 | C4038538 | 1.2.1 | POS - Fatal error caused when printing Totals | | |
| TIBU-20913 | C4038540 | 1.2.1 | TL POS - Metro - Driver Break gets stuck on loading screen | | |
| TIBU-20886 | C4038541 | 1.2.1 | TL POS - Fix commissioning of device from decommissioned device state | | |
| TIBU-20876 | C4057161 | 2.0.X | TL POS Rail - USB access prompt - pop-up on startup - MIURA | | |
| TIBU-20868 | C4038547 | 1.2.1 | Metro Daylink Adult - Card Ref Amount used in Days Left Field | | |
| TIBU-20851 | C4038552 | 1.2.1 | TL POS Metro - Invalid top up card not detected as removed | | |
| TIBU-20815 | C4048625 | Delete | TL POS: Bixolon LCD Display - No Display and USB permission prompts sometimes displayed | | |
| TIBU-20813 | C4038559 | 1.2.1 | POS - Sign on cards killing device | | |
| TIBU-20759 | C4038562 | 1.2.1 | Mini Statement Printout - ${ExpirationDate} placeholder instead of date | | |
| TIBU-19682 | C4048627 | 1.3.2 | TL POS: Sales Breakdown Print out does not print the correct information | | |
| TIBU-19560 | C4038563 | 1.2.1 | POS: Time is displayed as 12hr not 24hr and there are no seconds included in the timestamp | | |
| TIBU-19559 | C3560171 | 1.2.1 | POS: Signing on to Metro Home Location displays the incorrect Screen | | |
| TIBU-19460 | C4057163 | Bus? | TL POS Rail - Bus - Products cannot be purchased | | |
| TIBU-19459 | C4057164 | Bus? | TL POS Rail - Bus - Products cannot be added to the basket | | |
| TIBU-19458 | C4057166 | Bus? | TL POS Rail - Bus - Pressing "*" does not show Letters | | |
| TIBU-19456 | C4057165 | 2.0.0 | TL POS Rail - Adding Rail Favorites - Buttons Unaligned | | |
| TIBU-19454 | C4057162 | 2.0.0 | TL POS Rail - Misc Button on Main Flu screen causes Fatal Error | | |
| TIBU-19374 | C4078751 | 2.0.X | TL POS Rail - Cross Border (XB) Tickets not displaying the correct Price | | |
| TIBU-19373 | C4038565 | Delete | Perth ETIM - ETIM is not rebooting at the scheduled reboot time | | |
| TIBU-19371 | C4057160 | 2.0.X | TL POS Rail - Main Rail Screen - Favorites do not take user to the Payment Screen | | |
| TIBU-19352 | C4057159 | 2.0.0 | TL POS Rail - Ticket Annulment Greyed Out | | |
| TIBU-19341 | C3552016 | 1.1.1 | Sign On Screen - Cancel Button doesn't return to the previous field | | |
| TIBU-19336 | C4057158 | 2.0.0 | TL POS Rail - Following Initial issue of a basket via Cash, subsequent basket issue fails  | | |
| TIBU-19311 | C4057156 | 2.0.0 | TL POS Rail - Paper Jam - Annul transaction button not Responding | | |
| TIBU-19299 | C3552017 | 1.1.1 | Monthly Season Pass not showing correct "To" Date | | |
| TIBU-19292 | C3552018 | 1.1.1 | If Boarding and Alighting are set the same then all buttons on screen are greyed out | | |
| TIBU-19017 | C4038567 | Delete | Perth ETIM - Supervisor is not auto-logging off. | | |
| TIBU-18897 | C3552019 | Delete | TL POS CLESS Fix - Implement working solution | | |
| TIBU-18895 | C4038568 | 1.2.1 | TL POS CLESS fix analyse CLESS failure | | |
| TIBU-17471 | C4038577 | Delete | Perth ETIM - Passenger screen displays "Out of Service" when the ETIM is in service. | | |
| TIBU-16228 | C4038639 | 1.2.1 | TL POS - Cannot update Mounting Point ID | | |
| TIBU-16113 | C4038588 | 1.2.1 | POS-Performance slow | | |
| TIBU-16109 | C4057155 | 2.0.X | TL POS - Rail -Old Translink logo on some printouts | | |
| TIBU-16106 | C3560168 | 1.2.1 | POS-Card Reader failures are unexpectedly spamming Cloudfare | | |
| TIBU-16044 | C4038592 | 1.2.1 | POS-Cannot update Tray ID | | |
| TIBU-15942 | C4038593 | 1.2.1 | TL POS - USB access prompt - pop-up on startup - Metro | | |
| TIBU-15782 | C4038597 | 1.2.1 | POS-Software Versions does not include real version numbers | | |
| TIBU-13513 | C4078750 | 2.0.X | [Post Hub] Application must be able to store an array of encryption keys and encrypt a bar | | |
| TIBU-13180 | C4078749 | 2.0.X | As a POS Operator I want my device to be capable of printing a barcode on a ticket | | |
| TIBU-7379 | C4078748 | Bus? | TL POS Rail - Bus: cash payment with two different routes freezes or restarts the app | | |
