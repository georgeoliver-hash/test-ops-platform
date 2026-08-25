# TVM v3.4.4 — Translink TVM UX — Full Flow Transcription

Source: Overflow.io project "TVM" (https://overflow.io/s/08CCGD4Q/)
Extracted: full text content of all boards — screen titles, decision points, annotations/spec notes, and screen-to-screen connections.
Note: This document captures TEXT content and FLOW STRUCTURE only. It does not include the actual visual mockup images (screens are referenced by their title/ID only).

## Board Index (main navigation order)
1. Welcome Page
2. Map
3. Multi Modal Home Screen
4. Home Screen
5. Buy Tickets
6. Destination and Boarding Selection
7. Choose Ticket Details
8. Buy ABT Card
9. Smartcards
10. Collect Tickets by Reference
11. Payment Process
12. Ticket Printing
13. Basket
14. Timeouts

---


## 1. Welcome Page

### Screens (0)

### Decision Points (0)

### Annotations / Spec Notes (11)
- Welcome Page
- Version: 3.4.4
- TVM InVision Project: https://parkeon.invisionapp.com/share/R6X3KVXX3N9  The project link is for developers. You can use the <inspect> option to view CSS styles of individual elements. You can also access the assets for the project in the <inspect> area.
- TVM User Flows Contents:  1.   Welcome Page  2.   Map   3.   Multi Modal Home Screen  4.   Home Screen  5.   Buy Tickets  6.   Destination and Boarding Selection  7.   Choose Ticket Details  8.   Buy ABT Card  9.    Smartcards  10.  Collect Tickets by Reference  11.  Payment Process  12.  Ticket Printing  13.  Basket  14.  Timeouts  15. Changes log
- An overview of the full system
- Including Language Change
- Including flow for Changing Boarding Stage
- Including flow for both Cash and Card payment
- Including flow for receipt printing
- Editting and removing items
- Note: On almost all screens pressing 'Cancel' will return the user to the home screen, and pressing 'Back' will take the user back one screen, exceptions to this are documented in the flow.

### Connections / Flow (0)


## 2. Map

### Screens (0)

### Decision Points (24)
- Multi Modal Home Screen
- Home Screen
- Choose Ticket Details
- Smartcards
- Buy Tickets
- Collect Tickets by Reference
- Choose Ticket Details
- Smartcards
- Destination
- Collect Tickets by Reference
- Payment Process
- Ticket Printing
- Payment Process
- Ticket Printing
- Destination
- Buy Tickets
- Choose Ticket Details
- Ticket Printing
- Choose Ticket Details
- Ticket Printing
- Payment Process
- Payment Process
- Ticket Printing
- Ticket Printing

### Annotations / Spec Notes (3)
- Each board focuses on one specific section of the user flow, refer back this map if you become unsure which board to view next.
- Payment and Printing included in smartcard flow
- Payment and Printing included in smartcard flow

### Connections / Flow (22)
- Decision: "Payment Process" → Decision: "Ticket Printing" [Pay]
- Decision: "Choose Ticket Details" → Decision: "Payment Process" [Confirm Selection]
- Decision: "Destination" → Decision: "Buy Tickets"
- Decision: "Home Screen" → Decision: "Collect Tickets by Reference" [Press 'Collect Tickets']
- Decision: "Home Screen" → Decision: "Smartcards" [Press Smartcard button or present Smartcard]
- Decision: "Choose Ticket Details" → Decision: "Payment Process" [Confirm Selection]
- Decision: "Home Screen" → Decision: "Choose Ticket Details" [Pick a quick ticket]
- Decision: "Home Screen" → Decision: "Destination" [Press 'Buy Tickets']
- Decision: "Collect Tickets by Reference" → Decision: "Ticket Printing" [Identify and confirm tickets]
- Decision: "Payment Process" → Decision: "Ticket Printing" [Pay]
- Decision: "Buy Tickets" → Decision: "Choose Ticket Details"
- Decision: "Payment Process" → Decision: "Ticket Printing" [Pay]
- Decision: "Choose Ticket Details" → Decision: "Payment Process" [Confirm Selection]
- Decision: "Buy Tickets" → Decision: "Destination"
- Decision: "Multi Modal Home Screen" → Decision: "Collect Tickets by Reference" [Press 'Collect Tickets']
- Decision: "Multi Modal Home Screen" → Decision: "Smartcards" [Press Smartcard button or present Smartcard]
- Decision: "Choose Ticket Details" → Decision: "Payment Process" [Confirm Selection]
- Decision: "Multi Modal Home Screen" → Decision: "Buy Tickets" [Press 'Buy Tickets']
- Decision: "Collect Tickets by Reference" → Decision: "Ticket Printing" [Identify and confirm tickets]
- Decision: "Payment Process" → Decision: "Ticket Printing" [Pay]
- Decision: "Destination" → Decision: "Choose Ticket Details"
- Decision: "Multi Modal Home Screen" → Decision: "Choose Ticket Details" [Pick a quick ticket]


## 3. Multi Modal Home Screen

### Screens (6)
- 1.2.0. Message (Machine not available)
- 0.0.0 Select transport type 
- 1.0.2. Home Screen, Multi modal - Bus
- 1.0.3. Home Screen, Multi modal - Rail
- 0.1.0 Select transport type  for Discount 
- 0.1.0 Select transport type  for Free Smartpass

### Decision Points (6)
- ADVERTS
- Choose Ticket Details
- Smartcards
- Buy Tickets
- Collect Tickets by Reference
- Buy ABT Card

### Annotations / Spec Notes (5)
- Home screen for Multi Modal TVM  It will only be shown in Multi Modal solution
- Depending on what we choose (Bus or Rail) we will see screen for Bus or Rail with the appropriate tickets for the selected option
- If Discounted Smartcard is presented user would have  to choose for wich type of transport  he wants to buy ticket for
- If Free Smartpass card is presented user would have  to choose for wich type of transport  he wants to buy ticket for
- If 24+ card is presented then  flow immediately advances to the (3.1.3 Select Tickets - 24 Rail) 24+ ticket type selection screen

### Connections / Flow (17)
- Screen: "0.0.0 Select transport type " → Screen: "1.2.0. Message (Machine not available)" [Message shows when there is a fault in the machine]
- Screen: "1.2.0. Message (Machine not available)" → Decision: "ADVERTS" [30 Second Timeout, return on tap]
- Screen: "0.0.0 Select transport type " → Decision: "Smartcards" [ABT card or Top up only card presented]
- Screen: "0.0.0 Select transport type " → Screen: "1.0.2. Home Screen, Multi modal - Bus"
- Screen: "0.0.0 Select transport type " → Screen: "1.0.3. Home Screen, Multi modal - Rail"
- Screen: "1.0.2. Home Screen, Multi modal - Bus" → Screen: "0.0.0 Select transport type "
- Screen: "1.0.3. Home Screen, Multi modal - Rail" → Screen: "0.0.0 Select transport type "
- Screen: "0.0.0 Select transport type " → Screen: "0.1.0 Select transport type  for Discount " [Discount Smartcard presented]
- Screen: "0.0.0 Select transport type " → Screen: "0.1.0 Select transport type  for Free Smartpass" [Free Smartpass presented]
- Screen: "0.1.0 Select transport type  for Discount " → Decision: "Smartcards"
- Screen: "0.1.0 Select transport type  for Free Smartpass" → Decision: "Smartcards"
- Screen: "0.0.0 Select transport type " → Decision: "ADVERTS" [30 Second Timeout, return on tap]
- Screen: "1.0.2. Home Screen, Multi modal - Bus" → Decision: "Choose Ticket Details"
- Screen: "1.0.2. Home Screen, Multi modal - Bus" → Decision: "Buy Tickets"
- Screen: "1.0.2. Home Screen, Multi modal - Bus" → Decision: "Collect Tickets by Reference"
- Screen: "1.0.2. Home Screen, Multi modal - Bus" → Decision: "Buy ABT
Card"
- Screen: "1.0.2. Home Screen, Multi modal - Bus" → Decision: "Smartcards"


## 4. Home Screen

### Screens (4)
- 1.1.0. Home Screen, Language Choices
- 1.2.0. Message (Machine not available)
- 1.0.0. Home Screen, 3 choices
- 1.0.1. Home Screen, 3 choices, No ABT Cards

### Decision Points (6)
- ADVERTS
- Choose Ticket Details
- Smartcards
- Buy Tickets
- Collect Tickets by Reference
- Buy ABT Card

### Annotations / Spec Notes (2)
- English is the default language:  If a user changes the language, then later in the flow press 'Cancel', finish a transaction, or time out, the TVM returns to the Home Screen in English.
- Home screen with 'Buy ABT Card' button disabled.

### Connections / Flow (9)
- Screen: "1.0.0. Home Screen, 3 choices" → Decision: "Smartcards"
- Screen: "1.0.0. Home Screen, 3 choices" → Decision: "Collect Tickets by Reference"
- Screen: "1.0.0. Home Screen, 3 choices" → Screen: "1.2.0. Message (Machine not available)" [Message shows when there is a fault in the machine]
- Screen: "1.0.0. Home Screen, 3 choices" → Decision: "Buy ABT
Card"
- Screen: "1.0.0. Home Screen, 3 choices" → Screen: "1.1.0. Home Screen, Language Choices"
- Screen: "1.0.0. Home Screen, 3 choices" → Decision: "Buy Tickets"
- Screen: "1.0.0. Home Screen, 3 choices" → Decision: "ADVERTS" [30 Second Timeout, return on tap]
- Screen: "1.2.0. Message (Machine not available)" → Decision: "ADVERTS" [30 Second Timeout, return on tap]
- Screen: "1.0.0. Home Screen, 3 choices" → Decision: "Choose Ticket Details"


## 5. Buy Tickets

### Screens (7)
- 20.1.2. Single-Return - Metro (Airport)
- 20.1.7. Single-Return - Three-Day Ticket
- 20.1.8 Choose ticket Cross Border
- 2.4.1 Three-Day Travel - Start Date
- 2.4.2 Three-Day Travel - 1st selected 
- 2.4.3 Three-Day Travel - All selected
- 10.2.3. Payment method selection with 3 day ticket summary

### Decision Points (3)
- (From Destination)
- Choose Ticket Details
- Choose Ticket Details

### Annotations / Spec Notes (12)
- Product groups for NIR for cross border. If user selected one station from Northern Ireland 1-61 and one from Republic of Ireland 62-96 or both from Republic of Ireland 62-96
- Product groups for NIR local Rail. If user selected both stations from Northern Ireland 1-61
- For train we have a special Three-Day Ticket. Flow is shown below
- Up and down will scroll line by line
- Up and down will scroll line by line
- Fore every other ticket than Three-Day Travel user will go directly to "Chose Ticket Details" screen
- If the user selects 'Change start date', he will be taken back to the start of this flow (2.4.1 Three-Day Travel - Start Date) without any date selected
- User can tap on any date to select or deselect it
- After 3rd day picked 'Continue' button will be activated and all buttons for day selection will gray out
- This is an example payment type selection screen showing all the info that will be shown.
- User will see all days that they have selected
- The following synthesized speech is played according to the current state: "Speech 3 – Please select Payment type" "Speech 4 – Credit or Debit payments only" "Speech 5 – Cash payments only"

### Connections / Flow (12)
- Screen: "2.4.3 Three-Day Travel - All selected" → Decision: "Choose Ticket Details"
- Screen: "20.1.7. Single-Return - Three-Day Ticket" → Decision: "Choose Ticket Details"
- Screen: "2.4.2 Three-Day Travel - 1st selected " → Screen: "2.4.1 Three-Day Travel - Start Date"
- Screen: "2.4.2 Three-Day Travel - 1st selected " → Screen: "2.4.3 Three-Day Travel - All selected"
- Screen: "20.1.8 Choose ticket Cross Border" → Decision: "Choose Ticket Details"
- Screen: "20.1.2. Single-Return - Metro (Airport)" → Decision: "Choose Ticket Details"
- Screen: "2.4.1 Three-Day Travel - Start Date" → Screen: "2.4.2 Three-Day Travel - 1st selected " [The user selected the first day]
- Screen: "20.1.7. Single-Return - Three-Day Ticket" → Screen: "2.4.1 Three-Day Travel - Start Date"
- Decision: "Choose Ticket Details" → Screen: "10.2.3. Payment method selection with 3 day ticket summary"
- Decision: "(From Destination)" → Screen: "20.1.7. Single-Return - Three-Day Ticket" [Train tickets]
- Decision: "(From Destination)" → Screen: "20.1.8 Choose ticket Cross Border"
- Decision: "(From Destination)" → Screen: "20.1.2. Single-Return - Metro (Airport)" [Bus tickets]


## 6. Destination and Boarding Selection

### Screens (7)
- 4.0.0. Choose destination station - Main Screen
- 4.1.1. Choose destination station – search for station
- 4.1.4. Choose boarding station – search for station
- 4.1.2 Choose destination station – search for station, typing
- 4.0.1. Choose destination station - Alternative Departing
- 4.1.3 Choose destination station – search for station, typing, one left
- 4.1.5. Choose destination station –no stations

### Decision Points (1)
- Buy ticket screen: 20.1.2 ; 20.1.7 20.1.8

### Annotations / Spec Notes (10)
- The Boarding Stage is by default set to the location of the TVM. A User can change this by tapping on the 'Departing From' button.  From then, the process of selecting a new Boarding Stage is the same as the process for selecting an Alighting Stage.
- The following synthesized speech is played: "Speech 10 – Choose from popular destinations or search for another destination "
- As the user types, some keys become unavailable and go grey, other letters are available and brighten up.  This is to aid the user in typing quickly and without making a spelling mistake.
- As the user types, the selection of Alighting Stage options above become narrowed down to just those with the selected letters starting a word in their name.   When the user sees the Alighting Stage they want, they tap the button and move on to the Choose Ticket Details Flow.
- If user wishes, they can use the buttons on the right to scroll through remaining options.
- Now the user can select destination, with the Boarding Stage set as 'Rosepark'.
- Only the letters that can follow 'P' in the name of a possible Alighting Stage are lit up and usable, this should help customers type speedily with no mistakes.  The Delete button and 'Clear' are now also lit up.
- The following synthesized speech is played: "Speech 10 – Choose from popular destinations or search for another destination "
- When there are less than 6 possible Alighting Stages left, the scroll buttons disappear.
- In the event that a user selects a Boarding Stage without any possible Alighting Stages, all keyboard buttons grey out as they are unusable.

### Connections / Flow (7)
- Screen: "4.1.2 Choose destination station – search for station, typing" → Screen: "4.1.3 Choose destination station – search for station, typing, one left"
- Screen: "4.1.1. Choose destination station – search for station" → Screen: "4.1.2 Choose destination station – search for station, typing"
- Screen: "4.0.0. Choose destination station - Main Screen" → Decision: "Buy ticket
screen:
20.1.2 ; 20.1.7
20.1.8"
- Screen: "4.1.3 Choose destination station – search for station, typing, one left" → Decision: "Buy ticket
screen:
20.1.2 ; 20.1.7
20.1.8"
- Screen: "4.0.0. Choose destination station - Main Screen" → Screen: "4.1.1. Choose destination station – search for station"
- Screen: "4.1.4. Choose boarding station – search for station" → Screen: "4.0.1. Choose destination station - Alternative Departing"
- Screen: "4.1.3 Choose destination station – search for station, typing, one left" → Screen: "4.0.0. Choose destination station - Main Screen" ['Back' Closes the keyboard and clears any typed letters.
If the boarding stage has been changee, 'Back' wont undo this.]


## 7. Choose Ticket Details

### Screens (7)
- 3.0.3. Select Tickets - Rail 
- 3.0.0. Select Tickets 
- 3.0.2. Select Tickets - ticket selected
- 3.0.1. Select tickets – with tickets selected, no basket version
- 3.1.0 Select Tickets - yLink
- 3.0.6. Select Tickets - Rail  - low paper
- 3.0.7. Select Tickets - Rail  - invalid amount 

### Decision Points (3)
- Home Screen
- Basket
- Payment Process

### Annotations / Spec Notes (12)
- If no alternative ticket on Cloudfare then this right hand side of the screen will be blank
- This screen shows the  ticket type selected by the user.  For most ticket types, the TVM also offers an alternative ticket type.
- Pay Now and Add to Basket buttons are faded out to show they are unavailable. (As the user has not yet selected a number of tickets)
- If needed product description will be next to "Single"
- yLink Variation (see Smartcards)
- Quick Select Variation (No basket)
- Error Messages
- Pay Now an Alternative Tickets buttons gets replaced by an error message if there is an issue.
- Once one type of ticket has been selected, the other type becomes unavailable.
- This message is for when there's not enough ticket paper to print the amount of tickets requested.
- Add to Basket button is permenantly faded out as it is unavailable
- Machines are limited to purchases of £500.00. This error shows in priority to the paper level error.

### Connections / Flow (5)
- Screen: "3.0.0. Select Tickets " → Screen: "3.0.2. Select Tickets - ticket selected"
- Screen: "3.0.2. Select Tickets - ticket selected" → Decision: "Basket"
- Screen: "3.0.0. Select Tickets " → Screen: "3.0.1. Select tickets – with tickets selected, no basket version" [If arriving here via the quick selects tickets]
- Screen: "3.0.2. Select Tickets - ticket selected" → Decision: "Payment Process"
- Screen: "3.0.2. Select Tickets - ticket selected" → Decision: "Home Screen"


## 8. Buy ABT Card

### Screens (6)
- 5.5.1 Buy ABT card 
- 10.3.0. Select Payment Type - Buy ABT
- 5.6.3 Message (Printing unique code recepit) 
- 5.6.4 Message (Issuing card) 
- 5.7.4 Message (Card Jammed) 
- 5.6..5 Message (Take card and receipt(s)) 

### Decision Points (2)
- Payment Process
- Home Screen

### Annotations / Spec Notes (3)
- Top-up amonunts are  pre-configured
- TVM always prints special unique code receipt.
- User can click done. Which will send him to Home screen or there will be time countdown on this screen

### Connections / Flow (8)
- Screen: "5.5.1 Buy ABT card " → Screen: "10.3.0. Select Payment Type - Buy ABT" [User selects one of avaiable Top Up amount]
- Screen: "5.6.4 Message (Issuing card) " → Screen: "5.6..5 Message (Take card and receipt(s)) "
- Screen: "5.6..5 Message (Take card and receipt(s)) " → Decision: "Home Screen"
- Screen: "5.6.3 Message (Printing unique code recepit) " → Screen: "5.6.4 Message (Issuing card) "
- Screen: "5.7.4 Message (Card Jammed) " → Decision: "Home Screen"
- Decision: "Payment Process" → Screen: "5.6.3 Message (Printing unique code recepit) "
- Screen: "5.6.4 Message (Issuing card) " → Screen: "5.7.4 Message (Card Jammed) "
- Screen: "10.3.0. Select Payment Type - Buy ABT" → Decision: "Payment Process"


## 9. Smartcards

### Screens (52)
- 1.0.0. Home Screen, 3 choices
- 5.0.1.Message (take your smartcard)
- 5.1.2. Select top up volume (iLink Zone 1 Adult), with receipt
- 5.1.1. Select top up volume (iLink Zone 1 Adult)
- 5.1.0. Select top up volume (UMJ)
- 5.3.0 Message (Faulty smartcard - bold)
- 5.5.4 Top-up ABT - Standard Amounts 
- 5.5.5 Top-up ABT - Receipt
- 5.5.1 Message (Deny List)
- 5.5.6 Top-up ABT - Standard Amounts  -  Limited Amounts 
- 5.5.8 Top-up ABT - Standard Amounts  -  Limited Amounts 
- 5.2.3. Message (Present to Driver)
- 5.2.1. Message (Use before top up)
- 5.2.2. Message (No more top up)
- 5.5.2 Top-up ABT - Standard Amounts - Deny list  
- 5.5.3 Top-up ABT - Receipt - Deny list 
- 5.4.0. Smartpass statement
- 5.4.1. DayLink statement
- 5.4.5. yLink statement
- 5.4.6. Dependant Child 1 statement
- 13.1.15. Message (Card recently used)
- 10.2.2. Payment method selection with ABT Top Up Summary 
- 10.2.0. Payment method selection with Top Up Summary (iLink)
- 10.2.1. Payment method selection with Top Up Summary (UMJ)
- 5.4.2 Message (Take your statement)
- 3.1.0 Select Tickets - yLink
- 3.1.2 Select Tickets - yLink Rail
- 3.1.3 Select Tickets - 24 Rail
- 3.1.4 Select Tickets - Half-Fare Smartpass
- 3.1.1 Select Tickets - DepCh1
- 3.1.5 Select Tickets - DepCh1 Rail
- 3.1.6 Select Tickets - Free Smartpass
- 5.4.3. Smartpass statement - Post-Print
- 5.0.0. Message (Place your card)
- 5.7.0 Message (Different card presented - Try Again)
- 5.7.3. Message (Faulty smartcard – Try Again)
- 5.0.0. Message (Place your card)
- 5.7.0 Message (Different card presented - Try Again)
- 5.7.3. Message (Faulty smartcard – Try Again)
- 5.6.0 Message (top up complete - iLink)
- 5.6.1. Message (top up complete - UMJ)
- 5.7.1. Message (Faulty smartcard – No Update)
- 5.7.2. Message (Faulty smartcard – No Update - Cash)
- 5.6.2. Message (top up complete - ABT) 
- 5.7.1. Message (Faulty smartcard – No Update)
- 5.7.2. Message (Faulty smartcard – No Update - Cash)
- 5.0.1.Message (take your smartcard)
- 5.0.1.Message (take your smartcard)
- 13.1.13. Message (Take your top up receipt)
- 13.1.13. Message (Take your top up receipt)
- 13.1.14. Message (Take your card receipt)
- 13.1.14. Message (Take your card receipt)

### Decision Points (11)
- Destination (and Boarding) Selection
- Payment Process
- Payment Process
- Payment Process
- Ticket Printing
- Topup Receipt
- Topup Receipt
- Card Receipt
- Card Receipt
- Home Screen
- Home Screen

### Annotations / Spec Notes (43)
- Cards that cannot be read by the machine ->
- Example of screens, showing limited top up amount depending on balance
- Cards that cannot be used on the machine ->
- Account balance is shown based on ePurse balance
- Cancelations:   If a user presses 'Cancel' while their card is inserted, they will be shown this screen (Please take your smartcard). On this screen, when the user removes their card, the TVM returns to the home screen.  The user removing their card during the Smartcard flow wont automatically cancel the transaction, instead, when the TVM needs to update the card it will prompt for the card to be re-inserted. - Only the user pressing 'Cancel' cancels the transaction.  If the user removes their card and then presses 'Cancel', the TVM returns to home screen with out displaying this screen.  After a timeout screen, the flow acts the same as described above, as if the user pressed cancel.
- User can toggle on/off the Top Up Receipt button
- Screens shows current ePurse Balance and calculates minimum top up balance to be able to travel
- This screen will only be displayed when the Free Smartpass or Half-fare Smartpass customer selects BUS option or is using BUS TVM
- Minimum acount balance is £3.00 and maximum is £50.00  This is representation on button behavior dependent on current balance.  Top up buttons will be grayed out to not let balance go under minimum or above maximum balance.
- Minimum acount balance is £3.00 and maximum is £50.00  This is representation on button behavior dependent on current balance.  Top up buttons will be grayed out to not let balance go under minimum or above maximum balance.
- The following synthesized speech is played: "Speech 2 – Please take your Smartcard "
- Example where the user has opted for a receipt
- Example of topping up time on the card
- Example of topping up journeys on the card
- If the discount card has recently been used to make a purchase, this screen will show instead of the destination selection screen.
- All multi-journey cards are capped at 50 journeys, so if the card already had journeys on it, top ups that would take the total number of journeys on the card over 50 are not shown. The remaining bubbles are repositioned accordingly.
- If Account balance is below minimum balance, ammount will be in orange color
- User can toggle on/off the Top Up Receipt button
- An example details screen for cards that can be topped up ('Top Up' button is available)
- An example details screen
- Pay screen will show current account balance and balance after Top up
- Card type
- Price
- Payment Option Buttons
- On smartcards the user gets displayed the top up information
- Top Up details
- Unavailable payment type notice
- Escape Buttons
- RAIL selected or RAIL TVM
- BUS selected or BUS TVM
- BUS selected or BUS TVM
- This is an example payment type selection screen showing all the info that can show.
- RAIL selected or RAIL TVM
- The following synthesized speech is played: "Speech 3 – Please select Payment type"
- Mini-statement can only be printed once, so print button fades.
- (First screen replaced by the screens showing added information, above)
- (First screen replaced by the screens showing added information, above)
- The following synthesized speech is played: "Speech 1 – Please place your smartcard in the holder"
- The following synthesized speech is played: "Speech 1 – Please place your smartcard in the holder"
- Example for a dayLink card
- Example for a journey card
- The following synthesized speech is played: "Speech 2 – Please take your Smartcard "
- The following synthesized speech is played: "Speech 2 – Please take your Smartcard "

### Connections / Flow (82)
- Screen: "5.7.3. Message (Faulty smartcard – Try Again)" → Screen: "5.7.1. Message (Faulty smartcard – No Update)"
- Screen: "1.0.0. Home Screen, 3 choices" → Screen: "5.3.0 Message (Faulty smartcard - bold)" [Cards that cannot be read]
- Screen: "10.2.0. Payment method selection with Top Up Summary (iLink)" → Decision: "Payment Process"
- Decision: "Payment Process" → Screen: "5.6.2. Message (top up complete - ABT) "
- Screen: "5.0.0. Message (Place your card)" → Screen: "5.7.1. Message (Faulty smartcard – No Update)"
- Screen: "5.0.0. Message (Place your card)" → Screen: "5.6.2. Message (top up complete - ABT) "
- Screen: "1.0.0. Home Screen, 3 choices" → Screen: "5.2.2. Message (No more top up)" [Fully topped up cards]
- Decision: "Payment Process" → Screen: "5.7.3. Message (Faulty smartcard – Try Again)" [Card write error]
- Screen: "5.1.0. Select top up volume (UMJ)" → Screen: "10.2.1. Payment method selection with Top Up Summary (UMJ)"
- Screen: "5.6.2. Message (top up complete - ABT) " → Screen: "5.0.1.Message (take your smartcard)"
- Screen: "1.0.0. Home Screen, 3 choices" → Screen: "5.1.0. Select top up volume (UMJ)" [Top Up Cards]
- Screen: "5.0.0. Message (Place your card)" → Screen: "5.7.1. Message (Faulty smartcard – No Update)"
- Decision: "Topup Receipt" → Screen: "13.1.13. Message (Take your top up receipt)" [Yes]
- Screen: "5.7.3. Message (Faulty smartcard – Try Again)" → Screen: "5.0.0. Message (Place your card)" [User removes their card and presses Try Again]
- Screen: "5.4.2 Message (Take your statement)" → Screen: "5.4.3. Smartpass statement - Post-Print"
- Screen: "5.4.0. Smartpass statement" → Screen: "5.4.2 Message (Take your statement)" [Statement prints]
- Screen: "5.0.0. Message (Place your card)" → Screen: "5.6.0 Message (top up complete - iLink)"
- Screen: "5.7.2. Message (Faulty smartcard – No Update - Cash)" → Screen: "5.0.1.Message (take your smartcard)"
- Screen: "5.1.1. Select top up volume (iLink Zone 1 Adult)" → Screen: "10.2.0. Payment method selection with Top Up Summary (iLink)"
- Screen: "5.7.3. Message (Faulty smartcard – Try Again)" → Screen: "5.7.2. Message (Faulty smartcard – No Update - Cash)"
- Screen: "5.0.1.Message (take your smartcard)" → Decision: "Topup Receipt"
- Screen: "5.2.2. Message (No more top up)" → Screen: "5.4.0. Smartpass statement"
- Decision: "Payment Process" → Screen: "5.7.3. Message (Faulty smartcard – Try Again)" [Card write error]
- Screen: "5.7.3. Message (Faulty smartcard – Try Again)" → Screen: "5.0.0. Message (Place your card)" [User removes their card and presses Try Again]
- Screen: "5.7.0 Message (Different card presented - Try Again)" → Screen: "5.7.2. Message (Faulty smartcard – No Update - Cash)"
- Screen: "5.7.0 Message (Different card presented - Try Again)" → Screen: "5.7.2. Message (Faulty smartcard – No Update - Cash)"
- Screen: "5.7.3. Message (Faulty smartcard – Try Again)" → Screen: "5.7.1. Message (Faulty smartcard – No Update)"
- Screen: "1.0.0. Home Screen, 3 choices" → Decision: "Destination (and Boarding) Selection" [Discount cards]
- Screen: "13.1.13. Message (Take your top up receipt)" → Decision: "Card Receipt"
- Decision: "Destination (and Boarding) Selection" → Screen: "3.1.1 Select Tickets - DepCh1" [If user selected BUS or is using BUS TVM]
- Decision: "Topup Receipt" → Decision: "Card Receipt" [No]
- Decision: "Payment Process" → Decision: "Ticket Printing" [Note: The TVM will ask for the card to be presented here, if it has been removed earlier in the process.]
- Decision: "Destination (and Boarding) Selection" → Screen: "3.1.0 Select Tickets - yLink" [If user selected BUS or is using BUS TVM]
- Screen: "5.2.3. Message (Present to Driver)" → Screen: "5.4.0. Smartpass statement"
- Screen: "5.7.2. Message (Faulty smartcard – No Update - Cash)" → Screen: "5.0.1.Message (take your smartcard)"
- Screen: "5.2.1. Message (Use before top up)" → Screen: "5.4.0. Smartpass statement"
- Screen: "5.6.0 Message (top up complete - iLink)" → Screen: "5.0.1.Message (take your smartcard)"
- Decision: "Card Receipt" → Screen: "13.1.14. Message (Take your card receipt)" [Yes]
- Screen: "5.0.0. Message (Place your card)" → Screen: "5.7.0 Message (Different card presented - Try Again)" [Insert Wrong Card]
- Screen: "5.7.0 Message (Different card presented - Try Again)" → Screen: "5.7.1. Message (Faulty smartcard – No Update)"
- Decision: "Payment Process" → Screen: "5.0.0. Message (Place your card)" [User removed smartcard]
- Screen: "5.7.0 Message (Different card presented - Try Again)" → Screen: "5.7.1. Message (Faulty smartcard – No Update)"
- Decision: "Payment Process" → Screen: "5.0.0. Message (Place your card)" [User removed smartcard]
- Screen: "5.7.3. Message (Faulty smartcard – Try Again)" → Screen: "5.7.2. Message (Faulty smartcard – No Update - Cash)"
- Screen: "5.7.1. Message (Faulty smartcard – No Update)" → Screen: "5.0.1.Message (take your smartcard)" [Go direct to Home Screen if card already removed]
- Screen: "1.0.0. Home Screen, 3 choices" → Screen: "5.1.1. Select top up volume (iLink Zone 1 Adult)" [Top Up Cards]
- Screen: "5.7.1. Message (Faulty smartcard – No Update)" → Screen: "5.0.1.Message (take your smartcard)" [Go direct to Home Screen if card already removed]
- Screen: "5.1.1. Select top up volume (iLink Zone 1 Adult)" → Screen: "5.1.2. Select top up volume (iLink Zone 1 Adult), with receipt"
- Screen: "5.5.1 Message (Deny List)" → Screen: "5.5.2 Top-up ABT - Standard Amounts - Deny list  "
- Screen: "10.2.2. Payment method selection with ABT Top Up Summary " → Decision: "Payment Process"
- Screen: "10.2.1. Payment method selection with Top Up Summary (UMJ)" → Decision: "Payment Process"
- Screen: "1.0.0. Home Screen, 3 choices" → Screen: "5.2.1. Message (Use before top up)" [New cards and
cards which have been topped up with "From first use" expiry date]
- Decision: "Card Receipt" → Decision: "Home Screen" [No]
- Screen: "1.0.0. Home Screen, 3 choices" → Screen: "5.5.1 Message (Deny List)" [ABT Card Inserted
Deny list
]
- Screen: "5.0.0. Message (Place your card)" → Screen: "5.7.0 Message (Different card presented - Try Again)" [Insert Wrong Card]
- Screen: "3.1.1 Select Tickets - DepCh1" → Decision: "Ticket Printing" [Skip payment process if a free ticket]
- Screen: "1.0.0. Home Screen, 3 choices" → Screen: "5.5.4 Top-up ABT - Standard Amounts " [ABT card inserted]
- Decision: "Payment Process" → Screen: "5.6.0 Message (top up complete - iLink)"
- Screen: "1.0.0. Home Screen, 3 choices" → Screen: "5.2.3. Message (Present to Driver)" [Cards offering free travel, or half-fare travel.
]
- Screen: "5.5.2 Top-up ABT - Standard Amounts - Deny list  " → Screen: "10.2.2. Payment method selection with ABT Top Up Summary "
- Screen: "5.5.2 Top-up ABT - Standard Amounts - Deny list  " → Screen: "5.5.3 Top-up ABT - Receipt - Deny list "
- Screen: "5.5.4 Top-up ABT - Standard Amounts " → Screen: "10.2.2. Payment method selection with ABT Top Up Summary "
- Screen: "5.5.4 Top-up ABT - Standard Amounts " → Screen: "5.5.5 Top-up ABT - Receipt"
- Screen: "13.1.14. Message (Take your card receipt)" → Decision: "Home Screen"
- Decision: "Topup Receipt" → Screen: "13.1.13. Message (Take your top up receipt)" [Yes]
- Screen: "13.1.13. Message (Take your top up receipt)" → Decision: "Card Receipt"
- Decision: "Topup Receipt" → Decision: "Card Receipt" [No]
- Decision: "Card Receipt" → Screen: "13.1.14. Message (Take your card receipt)" [Yes]
- Decision: "Card Receipt" → Decision: "Home Screen" [No]
- Screen: "13.1.14. Message (Take your card receipt)" → Decision: "Home Screen"
- Screen: "5.0.1.Message (take your smartcard)" → Decision: "Topup Receipt"
- Screen: "3.1.0 Select Tickets - yLink" → Decision: "Payment Process"
- Decision: "Destination (and Boarding) Selection" → Screen: "3.1.2 Select Tickets - yLink Rail" [If user selected RAIL or is using RAIL TVM]
- Decision: "Destination (and Boarding) Selection" → Screen: "3.1.3 Select Tickets - 24 Rail" [If user selected RAIL or is using RAIL TVM]
- Decision: "Destination (and Boarding) Selection" → Screen: "3.1.4 Select Tickets - Half-Fare Smartpass" [If user selected RAIL or is using RAIL TVM]
- Decision: "Destination (and Boarding) Selection" → Screen: "3.1.5 Select Tickets - DepCh1 Rail" [If user selected RAIL or is using RAIL TVM]
- Decision: "Destination (and Boarding) Selection" → Screen: "3.1.6 Select Tickets - Free Smartpass" [If user selected RAIL or is using RAIL TVM]
- Screen: "3.1.5 Select Tickets - DepCh1 Rail" → Decision: "Ticket Printing"
- Screen: "3.1.6 Select Tickets - Free Smartpass" → Decision: "Ticket Printing"
- Screen: "3.1.2 Select Tickets - yLink Rail" → Decision: "Payment Process"
- Screen: "3.1.3 Select Tickets - 24 Rail" → Decision: "Payment Process"
- Screen: "3.1.4 Select Tickets - Half-Fare Smartpass" → Decision: "Payment Process"


## 10. Collect Tickets by Reference

### Screens (10)
- 6.0.0. Enter booking reference number
- 6.0.1. Entering booking reference number
- 13.1.8. Message (Please wait)
- 6.1.0. Booked ticket data, updated data
- 6.0.2. Enter booking reference number retry - cleared field
- 6.0.3. Message (Reference Used)
- 6.0.5. Message (Location Error)
- 13.2.4. Message (Take your tickets)
- 6.0.4. Attempt Limit
- 13.1.8. Message (Please wait)

### Decision Points (1)
- Home Screen

### Annotations / Spec Notes (9)
- 'Confirm' button stays unavailable until the first letter/number is pressed
- The following synthesized speech is played: "Speech 12 – Please enter your booking reference number"
- The data shown here is dependant on the type of ticket being sold.  i.e. 'Date of Use' is an optional field that only shows if it is relevant for the tickets collected.
- Back takes you to 6.0.0.
- Timeout to Home Screen
- The following synthesized speech is played: "Speech 12 – Please enter your booking reference number"
- An error for if tickets can only be picked up in certain locations
- Timeout to Home Screen
- "Speech 11 – Please take your tickets " is played

### Connections / Flow (9)
- Screen: "6.0.1. Entering booking reference number" → Screen: "13.1.8. Message (Please wait)"
- Screen: "13.1.8. Message (Please wait)" → Screen: "6.1.0. Booked ticket data, updated data" [Reference Valid]
- Screen: "6.0.2. Enter booking reference number retry - cleared field" → Screen: "6.0.4. Attempt Limit" [On the 3rd invalid attempt]
- Screen: "13.1.8. Message (Please wait)" → Screen: "6.0.2. Enter booking reference number retry - cleared field" [Reference invalid]
- Screen: "13.1.8. Message (Please wait)" → Screen: "6.0.3. Message (Reference Used)" [Tickets have already been collected]
- Screen: "6.0.0. Enter booking reference number" → Screen: "6.0.1. Entering booking reference number"
- Screen: "6.1.0. Booked ticket data, updated data" → Screen: "13.2.4. Message (Take your tickets)"
- Screen: "13.2.4. Message (Take your tickets)" → Screen: "13.1.8. Message (Please wait)" [Timeout, or user taps done]
- Screen: "13.1.8. Message (Please wait)" → Decision: "Home Screen"


## 11. Payment Process

### Screens (21)
- 10.0.0. Select Payment Type
- 10.1.1. Cash payment not available
- 10.1.2. Card (EMV) payment not available
- 13.2.2. Message (Error occured while processing)
- 11.0.0 Card payment, without receipt
- 11.0.1 Card payment, with receipt
- 12.0.0. Cash payment
- 13.1.12 Message (payment is being processed)
- 13.1.2. Message (payment cancelled)
- 13.1.11. Message (payment cancelled please wait)
- 12.0.1. Cash payment - Halfway Through
- 12.1.1. Cash payment no more coins
- 12.1.2. Cash payment no more notes
- 12.1.3. No more cash accepted
- 13.1.8. Message (Please wait)
- 13.1.1. Message (EMV payment complete)
- 12.2.0. Change Voucher- PayPoint
- 13.1.3. Message (Payment Cancelled - Change returned)
- 13.1.4. Message (Please take your card)
- 13.1.5. Payment Failed
- 13.2.1. Message (Payment Cancelation Failure)

### Decision Points (9)
- Payment type
- Back or Cancel
- Home Screen
- Ticket Printing
- Back to 10.0.0.
- Ticket Printing
- Try Again, Back or Cancel
- Home Screen
- Back to 10.0.0.

### Annotations / Spec Notes (19)
- Cancelations: After a payment type has been selected, the user pressing 'Cancel' wont take the user immediately to the home screen. Instead, a message will appear for a short time before the TVM returns to the home screen. The message diplays information relevant to the payment stage the user is on e.g. reminding the user to collect their returned cash or to take their bank card. These messages are shown in the flow.
- The following synthesized speech is played: "Speech 3 – Please select Payment type"
- The following synthesized speech is played: "Speech 4 – Credit or Debit payments only"
- The following synthesized speech is played: "Speech 5 – Cash payments only"
- This screen is the catch all error screen, it should never show. If it does, something has gone wrong that really wasn't supposed to. e.g. cash or card payment have become unavailable during the payment process.
- User taps 'Receipt?' if they would like a receipt, the button goes green to signify that a receipt will be printed.  The user can tap the button again if they decide they don't need a receipt.
- These are the screens that show if the user presses 'cancel'/'back' before the point where they have inserted cash (right) or their payment card (left).
- The following synthesized speech is played: "Speech 8 – Present or insert your credit or debit card to pay"
- The following synthesized speech is played: "Speech 6 – Insert coins or notes to pay"
- The following synthesized speech is played: "Speech 7 – Payment Cancelled"
- The following synthesized speech is played: "Speech 7 – Payment Cancelled"
- The following synthesized speech is played: "Speech 7 – Payment Cancelled"
- If the customer inserts coins or notes for a ticket of less value (e.g. £5 note for a £3 ticket), then the TVM will automatically calculate and issue change to the customer if there is sufficient change available in the change hoppers in the TVM.  The screen below is displayed only when there is insufficient change in the change hoppers
- (Or for Top Up - Continue Smartcards Flow)
- (Or for Top Up - Continue Smartcards Flow)
- The following synthesized speech is played: "Speech 7 – Payment Cancelled"
- This screen shows (after 'Try Again' or 'Cancel' selected) if the payment card needs removing.
- The following synthesized speech is played: "Speech 9 – Please take your debit or credit card"
- This screen also shows if the user presses cancel on the PIN pad or removes their card without completing the transaction.

### Connections / Flow (20)
- Screen: "12.0.1. Cash payment - Halfway Through" → Screen: "13.1.8. Message (Please wait)"
- Decision: "Back or Cancel" → Decision: "Home Screen" [Cancel]
- Screen: "13.1.12 Message (payment is being processed)" → Decision: "Payment type"
- Screen: "12.0.0. Cash payment" → Screen: "12.1.2. Cash payment no more notes"
- Screen: "13.1.11. Message (payment cancelled please wait)" → Decision: "Back or Cancel"
- Decision: "Back or Cancel" → Decision: "Back to 10.0.0." [Back]
- Decision: "Payment type" → Decision: "Ticket Printing" [Contactless]
- Screen: "13.1.5. Payment Failed" → Screen: "13.1.4. Message (Please take your card)"
- Screen: "11.0.0 Card payment, without receipt" → Screen: "13.1.12 Message (payment is being processed)" [Insert card and follow instructions]
- Decision: "Payment type" → Screen: "13.1.1. Message (EMV payment complete)" [Chip and PIN]
- Decision: "Try Again, Back or Cancel" → Decision: "Back to 10.0.0." [Try Again, Back]
- Screen: "12.0.0. Cash payment" → Screen: "12.0.1. Cash payment - Halfway Through"
- Screen: "12.0.0. Cash payment" → Screen: "12.1.1. Cash payment no more coins"
- Screen: "12.0.0. Cash payment" → Screen: "12.1.3. No more cash accepted"
- Decision: "Try Again, Back or Cancel" → Decision: "Home Screen" [Cancel]
- Screen: "13.1.3. Message (Payment Cancelled - Change returned)" → Decision: "Try Again, Back or Cancel"
- Screen: "13.1.2. Message (payment cancelled)" → Decision: "Back or Cancel"
- Screen: "13.1.8. Message (Please wait)" → Decision: "Ticket Printing"
- Screen: "13.1.3. Message (Payment Cancelled - Change returned)" → Screen: "13.2.1. Message (Payment Cancelation Failure)"
- Screen: "13.1.1. Message (EMV payment complete)" → Decision: "Ticket Printing"


## 12. Ticket Printing

### Screens (8)
- 13.1.9. Message (Printing tickets)
- 13.1.14. Message (Take your card receipt)
- 13.1.7. Message (Take your tickets, no button)
- 13.2.3. Message (Take your tickets and change)
- 13.2.15. Message (Take your tickets and change voucher)
- 13.1.10.Message (Change Voucher failed)
- 13.2.4. Message (Take your tickets)
- 13.1.8. Message (Please wait)

### Decision Points (3)
- Payment type
- Change
- Home Screen

### Annotations / Spec Notes (6)
- This screen shows when a card receipt has been requested.
- The following synthesized speech is played: "Speech 9 – Please take your debit or credit card"
- The following synthesized speech is played: "Speech 11 – Please take your tickets"
- The following synthesized speech is played: "Speech 13 – Please remember to take your change "
- The following synthesized speech is played: "Speech 11 – Please take your tickets"
- This is the error screen for if the change voucher fails to print

### Connections / Flow (12)
- Decision: "Payment type" → Decision: "Change" [Cash]
- Decision: "Change" → Screen: "13.1.7. Message (Take your tickets, no button)" [Exact value given]
- Decision: "Change" → Screen: "13.2.15. Message (Take your tickets and change voucher)" [No change, change voucher requireed]
- Screen: "13.1.7. Message (Take your tickets, no button)" → Screen: "13.1.8. Message (Please wait)"
- Screen: "13.2.15. Message (Take your tickets and change voucher)" → Screen: "13.1.8. Message (Please wait)"
- Screen: "13.1.8. Message (Please wait)" → Decision: "Home Screen"
- Decision: "Change" → Screen: "13.2.3. Message (Take your tickets and change)" [Change required]
- Screen: "13.1.9. Message (Printing tickets)" → Screen: "13.1.14. Message (Take your card receipt)" [User requested receipt ]
- Screen: "13.1.9. Message (Printing tickets)" → Screen: "13.2.4. Message (Take your tickets)"
- Screen: "13.1.14. Message (Take your card receipt)" → Screen: "13.2.4. Message (Take your tickets)"
- Screen: "13.2.4. Message (Take your tickets)" → Screen: "13.1.8. Message (Please wait)" [Timeout, or user taps done]
- Decision: "Payment type" → Screen: "13.1.9. Message (Printing tickets)"


## 13. Basket

### Screens (17)
- 7.0.3. Basket (Spanish)
- 7.0.0. Basket
- 10.0.0.2. Select Payment Type (Basket - 1050)
- 7.0.1. Basket item removal prompt
- 7.1.3. Edit Basket Item Day Ticket
- 7.1.1. Edit Basket Item Single/Return
- 4.0.3.1. Choose destination station - Main Screen (Basket)
- 4.1.3. Modify destination station from basket
- 7.0.2. Basket after item removed
- 4.1.5.1. Choose destination station – search for station - Basket
- 20.1.5.1. Single-Return - Ulsterbus (Basket)
- 7.1.2. Edit Basket Item Single/Return - Change of Destination or Increase/Decrease Tickets
- 3.0.0.1. Select Tickets (Basket)
- 3.0.2.1. Select tickets – with tickets selected (Basket)
- 7.0.0. Basket
- 10.0.0.2. Select Payment Type (Basket - 2025)
- 10.0.0.2. Select Payment Type (Basket - 2025)

### Decision Points (5)
- Payment Process
- Basket shows, when the user clicks 'Add More Items', the user is returned precisely to the screen they were on before.  This is the same for the 'View Basket' Button on all other screens, hence is not marked on the flow repeatedly.
- Continue with payment flow as normal.
- On to Operator Selection, flow for Selecting another Ticket
- Continue with payment flow as normal.

### Annotations / Spec Notes (10)
- When a user presses 'Add To Basket', the next screen they see is the Basket.
- Cancelations: Pressing cancel while items are in the backet will return the user to the home screen. All items in the basket are removed.
- In languages other than English, a pencil symbol appears on the 'Edit' Button
- User can change destination, departing point, and/or number of tickets. User presses done when ready, and returns to Basket.
- The following synthesized speech is played: "Speech 3 – Please select Payment type"
- User can change  number of tickets, and press 'Done' when ready. (Returns to Basket)
- The following synthesized speech is played: "Speech 10 – Choose from popular destinations or search for another destination "
- (User can also change number of tickets, by tapping up/down arrows)
- The following synthesized speech is played: "Speech 3 – Please select Payment type"
- The following synthesized speech is played: "Speech 3 – Please select Payment type"

### Connections / Flow (27)
- Screen: "7.1.1. Edit Basket Item Single/Return" → Screen: "4.1.3. Modify destination station from basket" [User opts to change Boarding/Alighting Stage]
- Screen: "10.0.0.2. Select Payment Type (Basket - 2025)" → Decision: "Continue with payment flow as normal."
- Screen: "3.0.0.1. Select Tickets (Basket)" → Screen: "3.0.2.1. Select tickets – with tickets selected (Basket)" [User selects number of tickets, by tapping Arrow Buttons]
- Screen: "4.1.5.1. Choose destination station – search for station - Basket" → Screen: "20.1.5.1. Single-Return - Ulsterbus (Basket)" [User selects Destination]
- Screen: "7.0.0. Basket" → Screen: "7.1.1. Edit Basket Item Single/Return" [User opts to Edit a ticket for a journey]
- Screen: "10.0.0.2. Select Payment Type (Basket - 2025)" → Screen: "3.0.2.1. Select tickets – with tickets selected (Basket)" [User Presses Back]
- Screen: "10.0.0.2. Select Payment Type (Basket - 2025)" → Screen: "7.0.0. Basket" [User presses Back or 'View Basket']
- Screen: "7.0.1. Basket item removal prompt" → Screen: "7.0.2. Basket after item removed" [User Chooses 'Yes']
- Screen: "7.0.0. Basket" → Screen: "7.1.3. Edit Basket Item Day Ticket" [User opts to Edit a Day travel item]
- Screen: "4.1.5.1. Choose destination station – search for station - Basket" → Screen: "4.0.3.1. Choose destination station - Main Screen (Basket)" [User presses Back]
- Screen: "7.0.0. Basket" → Screen: "10.0.0.2. Select Payment Type (Basket - 2025)" [User presses 'Pay Now']
- Screen: "7.0.0. Basket" → Screen: "7.0.1. Basket item removal prompt" [User opts to Delete an item]
- Screen: "4.0.3.1. Choose destination station - Main Screen (Basket)" → Screen: "20.1.5.1. Single-Return - Ulsterbus (Basket)" [User selects Destination]
- Screen: "10.0.0.2. Select Payment Type (Basket - 1050)" → Decision: "Payment Process" [User Selects Payment Type]
- Screen: "20.1.5.1. Single-Return - Ulsterbus (Basket)" → Screen: "3.0.0.1. Select Tickets (Basket)"
- Screen: "20.1.5.1. Single-Return - Ulsterbus (Basket)" → Screen: "4.0.3.1. Choose destination station - Main Screen (Basket)" [User presses Back]
- Screen: "4.0.3.1. Choose destination station - Main Screen (Basket)" → Screen: "4.1.5.1. Choose destination station – search for station - Basket" [User taps Search Bar]
- Screen: "3.0.0.1. Select Tickets (Basket)" → Screen: "20.1.5.1. Single-Return - Ulsterbus (Basket)" [User pressea Back]
- Screen: "4.1.5.1. Choose destination station – search for station - Basket" → Decision: "Basket shows, when the user clicks 'Add More Items', the user is returned precisely to the screen they were on before.

This is the same for the 'View Basket' Button on all other screens, hence is not marked on the flow repeatedly." [User presses 'View Basket']
- Screen: "7.0.0. Basket" → Screen: "10.0.0.2. Select Payment Type (Basket - 1050)" [User selects 'Pay Now']
- Screen: "7.0.0. Basket" → Screen: "4.0.3.1. Choose destination station - Main Screen (Basket)" [User selects 'Add More Items']
- Screen: "3.0.2.1. Select tickets – with tickets selected (Basket)" → Screen: "20.1.5.1. Single-Return - Ulsterbus (Basket)" [User preses Back]
- Screen: "10.0.0.2. Select Payment Type (Basket - 2025)" → Decision: "Continue with payment flow as normal."
- Screen: "7.0.0. Basket" → Decision: "On to Operator Selection, flow for Selecting another Ticket" [User Presses 'Add More Items']
- Screen: "3.0.2.1. Select tickets – with tickets selected (Basket)" → Screen: "7.0.0. Basket"
- Screen: "3.0.2.1. Select tickets – with tickets selected (Basket)" → Screen: "10.0.0.2. Select Payment Type (Basket - 2025)"
- Screen: "4.1.3. Modify destination station from basket" → Screen: "7.1.2. Edit Basket Item Single/Return - Change of Destination or Increase/Decrease Tickets"


## 14. Timeouts

### Screens (3)
- 13.2.5. More Time Required
- 13.1.3. Message (Payment Cancelled - Change returned)
- 13.1.11. Message (payment cancelled please wait)

### Decision Points (0)

### Annotations / Spec Notes (3)
- All screens have a timeout, after which '13.2.5. More Time Required' shows. The length of the timeout is configurable per screen.  After the countdown on this screen, the TVM returns to the Home Screen.  If 'Yes (X)' is pressed, the user is returned back to the screen they timed-out on.
- If the user has already entered some cash, but not yet completed payment, this screen shows after '13.2.5. More Time Required'  and then the TVM returns to the Home Screen.
- If the user has already selected a payment type, this screen shows after '13.2.5. More Time Required'  and then the TVM returns to the Home Screen.

### Connections / Flow (0)


---

# Additional Boards (not in main navigation list)


## Changes log (extra board)

### Screens (23)
- 0.0.0 Select transport type 
- 0.1.0 Select transport type  for Discount 
- 0.1.0 Select transport type  for Free Smartpass
- 1.0.0. Home Screen, 3 choices
- 1.0.2. Home Screen, Multi modal - Bus
- 1.0.1. Home Screen, 4 choices
- 1.0.1. Home Screen, 3 choices, No ABT Cards
- 1.0.0. Home Screen, 3 choices
- 5.0.0. Message (Place your card)
- 3.1.0 Select Tickets - yLink
- 10.0.0. Select Payment Type
- 10.1.1. Cash payment not available
- 11.0.0 Card payment, without receipt
- 11.0.1 Card payment, with receipt
- 12.0.0. Cash payment
- 12.0.0. Cash payment
- 5.1.2. Select top up volume (iLink Zone 1 Adult), with receipt
- 5.1.1. Select top up volume (iLink Zone 1 Adult)
- 5.1.1. Select top up volume (iLink Zone 1 Adult)
- 5.1.0. Select top up volume (UMJ)
- 5.1.0. Select top up volume (UMJ)
- 3.0.0.1. Select Tickets (Basket)
- 3.0.0.1. Select Tickets (Basket)

### Decision Points (0)

### Annotations / Spec Notes (17)
- New UI
- Old UI
- Home Screen
- Buy ABT button is disabled when there are no cards in machine, card  is jamed etc.
- Smart card and ABT top up first screen
- Quick Select Variation (No basket)
- - Ticket icon changed to square - Removed yellow triangle before message
- Payment Selection
- Only icons shape changed to square
- Payment with Card
- - Removed red triangles - Placed information about possibility to get receip in Information box - Changed 'Receipt' button fill color
- Payment with Cash
- Added Icon and description  for correct note insert
- Smartcard top up
- - chnged 'Top Up Receipt' button color after selecting it to darker green. Used in the project .
- - Buttons shape changed to square - Top Up Receipt button fill changed
- - Buttons shape changed to square - Top Up Receipt button fill changed

### Connections / Flow (2)
- Screen: "0.0.0 Select transport type " → Screen: "0.1.0 Select transport type  for Discount "
- Screen: "0.0.0 Select transport type " → Screen: "0.1.0 Select transport type  for Free Smartpass"
