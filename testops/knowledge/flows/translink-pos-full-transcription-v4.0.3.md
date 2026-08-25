# v4.0.3 Translink POS — Full Flow Transcription

Source: Overflow.io project "v4.0.3 Translink POS" (https://overflow.io/s/RCZ9UPQF/)
Extracted: full text content of all 17 boards — screen titles, decision points, annotations/spec notes, and screen-to-screen connections.
Note: This document captures TEXT content and FLOW STRUCTURE only. It does not include the actual visual mockup images (screens are referenced by their title/ID only).

## Board Index
1. Welcome Page
2. 1.0 Sign On
3. 2.0 FLU - Bus
4. 3.0 FLU - Rail
5. 4.0 Basket & Payment
6. 5.0 Card Payment
7. 6.0 Numerical Input
8. 7.0 Top Up & Validation
9. 8.0 Issue Card
10. 9.0 Operator
11. 10.0 Supervisor
12. 11.0 Technician
13. 12.0 Administrator
14. 13.0 Customer Displays
15. 14.0 Barcode Scanning
16. 15.0 Printer Errors
17. 16.0 Power Interruption & Audio Tones

---


## 1. Welcome Page

### Screens (22)
- 1.0 Idle Screen
- 01.0.0 - Idle Screen
- 01.0.0 - Idle Screen
- Main Screen
- Contactless/active/bglight
- Contactless/active/bgdark
- Contactless/faulty/bglight
- Contactless/faulty/bgdark
- Frame 26
- Frame 27
- Frame 20
- Frame 21
- Cellular/4bar/bglight
- Cellular/4bar/bgdark
- Cellular/3bar/bglight
- Cellular/3bar/bgdark
- Cellular/2bar/bglight
- Cellular/2bar/bgdark
- Cellular/1bar/bglight
- Cellular/1bar/bgdark
- Cellular/0bar/bglight
- Cellular/0bar/bgdark

### Decision Points (1)
- In the event that there is no ethernet connectivity available but a cellular connection is, a cellular icon will be displayed to indicate the signal strength.  In the event that cellular is not available either the Celllular Unavailable icon will be displayed.

### Annotations / Spec Notes (20)
- POS v4.0.3
- Welcome Page
- Translink POS User Flows Contents
- Welcome Page
- 1.0 Sign On 2.0 FLU - Bus 3.0 FLU - Rail 4.0 Basket & Payment 5.0 Card Payment 6.0 Numerical Input 7.0 Top Up & Validation 8.0 Issue Card 9.0 Operator 10.0 Supervisor 11.0 Technician 12.0 Administrator 13.0 Customer Displays 14.0 Barcode Scanning 15.0 Printer Errors 16.0 Power Interruption & Audio Tones
- Symbols
- The following symbols showing the availablility of three features, being permanently positioned in the upper left side of the screen, as a part of the status bar. For accessibility reasons, the symbols may vary between two colors: blue on a light background and white on a dark background. The Faulty Device icon is used to remind the driver that they have already reported the device as faulty. It is technically a different state to Card Reader Unavailable.
- Available
- Unavailable
- Faulty Payment Device
- Light background
- Dark background
- Light background
- Dark background
- Light background
- Dark background
- Card Reader
- Network
- Ethernet
- Cellular

### Connections / Flow (0)


## 2. 1.0 Sign On

### Screens (15)
- 1.0 Idle Screen
- 1.1.1 Sign On - Empty Fields
- 1.1.2 Sign On - ID Entered
- 1.1.3 Sign On - PIN Entry
- 1.1.4 Sign On - PIN Entry - 4*
- 1.2.1 Communications Locked
- 1.2.2 Please Wait...
- 1.3.1 Sign On - Incorrect Details
- 1.3.2 Message of the Day
- 1.4.1 Sign On - Device Locked
- 1.4.2 Word and Colour of the Day - Simpler UI
- 1.5.1 Message of the Day - Unavailable
- 2.2 Main Screen-Rail selected
- 7.1.2 Metro Smartcard/Please Present Smartcard
- 1.6.1 Word and Colour of the Day - Unavailable

### Decision Points (4)
- Present Card?
- Sign On Succesful?
- Is Message of the Day available?
- Are Word and Colour of the Day available?

### Annotations / Spec Notes (22)
- Sign On
- Presenting Card will redirect User to Sign On Page with the ID automatically entered and Pin field active.
- YES
- YES
- NO
- POS will display this screen whilst it is loading. In normal operating conditions with a good network connection this screen will be shown for a minimal period.
- If User doesn't present Card, he has to Press Any Key to progress to Sign On Page with ID field active.
- NO
- Pressing 'C' button will delete 1 character at a time. If the field is empty it will switch to the previous field.
- If Message of the Day is available, The specific Page will be displayed.
- If the Device cannot establish a correct Communication it will be locked and present a screen  with an Error Message and "Please Notify a Supervisor or Technician".
- YES
- If Word and Coulour of the Day is available, The specific Page will be displayed.
- NO
- User will be redirected to ID field active (if he tried to Sign On manually entering ID) or PIN field active accordingly (if he tried to Sign On automatically presenting Card) after 3 seconds or by pressing Enter button.
- Pressing any key will send operator to main screen.
- Metro Operator will go to this screen after Sign On.
- YES
- If User enters an incorrect Pin for more than the allowed number of attempts, the Device will become locked and will require a Supervisor Card to unlock.
- NO
- If Message of the Day is not Available, User will be taken to an error screen.
- If Word and Colour of the Day is not Available,  User will be taken to an error screen.

### Connections / Flow (26)
- Screen: "1.2.2 Please Wait..." → Decision: "Is Message of the Day available?"
- Screen: "1.3.1 Sign On - Incorrect Details" → Screen: "1.1.1 Sign On - Empty Fields"
- Screen: "1.1.1 Sign On - Empty Fields" → Screen: "1.1.2 Sign On - ID Entered" [User enters ID.]
- Screen: "1.0 Idle Screen" → Screen: "1.2.1 Communications Locked"
- Screen: "1.3.1 Sign On - Incorrect Details" → Screen: "1.1.3 Sign On - PIN Entry"
- Screen: "1.5.1 Message of the Day - Unavailable" → Decision: "Are Word and Colour of the Day available?"
- Decision: "Are Word and Colour of the Day available?" → Screen: "1.4.2 Word and Colour of the Day - Simpler UI"
- Screen: "1.1.2 Sign On - ID Entered" → Screen: "1.1.3 Sign On - PIN Entry" [User presses Enter button.]
- Screen: "1.1.4 Sign On - PIN Entry - 4*" → Screen: "1.1.2 Sign On - ID Entered"
- Decision: "Is Message of the Day available?" → Screen: "1.5.1 Message of the Day - Unavailable"
- Decision: "Is Message of the Day available?" → Screen: "1.3.2 Message of the Day"
- Screen: "1.3.1 Sign On - Incorrect Details" → Screen: "1.4.1 Sign On - Device Locked"
- Screen: "1.1.3 Sign On - PIN Entry" → Screen: "1.1.2 Sign On - ID Entered"
- Screen: "1.3.2 Message of the Day" → Decision: "Are Word and Colour of the Day available?"
- Screen: "1.1.4 Sign On - PIN Entry - 4*" → Decision: "Sign On Succesful?"
- Decision: "Sign On Succesful?" → Screen: "1.2.2 Please Wait..."
- Screen: "1.1.3 Sign On - PIN Entry" → Screen: "1.1.4 Sign On - PIN Entry - 4*" [User enters Pin.]
- Decision: "Sign On Succesful?" → Screen: "1.3.1 Sign On - Incorrect Details" [If user enters a
wrong ID/Pin
he will be taken
to an Error screen.
]
- Decision: "Present Card?" → Screen: "1.1.1 Sign On - Empty Fields"
- Decision: "Present Card?" → Screen: "1.1.3 Sign On - PIN Entry"
- Screen: "1.0 Idle Screen" → Decision: "Present Card?"
- Decision: "Are Word and Colour of the Day available?" → Screen: "1.6.1 Word and Colour of the Day - Unavailable"
- Screen: "1.4.2 Word and Colour of the Day - Simpler UI" → Screen: "2.2 Main Screen-Rail selected"
- Screen: "1.6.1 Word and Colour of the Day - Unavailable" → Screen: "2.2 Main Screen-Rail selected"
- Screen: "1.4.2 Word and Colour of the Day - Simpler UI" → Screen: "7.1.2 Metro Smartcard/Please Present Smartcard"
- Screen: "1.6.1 Word and Colour of the Day - Unavailable" → Screen: "7.1.2 Metro Smartcard/Please Present Smartcard"


## 3. 2.0 FLU - Bus

### Screens (45)
- 2.2 Main Screen-Rail selected
- 2.0 Main Screen
- 2.1 Main Screen - digits entered
- 2.3 Main Screen - route entered
- 2.4 Main Screen - direction changed
- Day Tours - digits entered
- Day Tours - route entered
- 2.3.3 Main Screen - Misc
- Day Tours - empty
- 2.5.2 Main Screen-Ulsterbus selected
- 2.5.5 Main Screen - FLU - Change Fare type
- 2.7.1 Main Screen - FLU - Change Ticket type
- 2.2.1 Route Number - Letters ETM - empty
- 2.2.2 Route Number - Letters ETM
- 2.5.3 Main Screen - FLU - Change Boarding Stage
- 2.5.4 Main Screen - FLU - Alighting Stages 23 & 24
- 2.3.1 FLU - Misc Product Open Fare
- 2.3.2 FLU - Misc Product Open Fare Entered
- Day Tours - Letters ETM - empty
- Day Tours - Letters ETM
- 2.6.1 FLU - Other
- 2.6.2 Main Screen - FLU - Alighting Selected
- 2.6.3 Main Screen - Added to Basket
- 9.1.4 Main Screen-Euro currency
- 2.9 FLU - Day Tour Product
- 4.8.3 Payment-Misc Product
- 2.2.3 Route Number - Letters - Error
- 2.2.4 Main Screen - Error
- 2.7.2 Toggle Group - Flu Product Selected from Menu
- 2.9.1 FLU - Day Tour Product - Seat Number Entry
- 2.9.1.1 FLU - Day Tour Product - Seat Number Entered
- 2.7.3 Main Screen - Last Transaction 200 - Confirm
- 2.4.1 FLU - Misc Product Open Fare Invalid
- 2.9.2 FLU - Day Tour Product - Date Entry
- 2.9.2.1 FLU - Day Tour Product - Date Entered
- Day Tours - Error
- Day Tours - Letters - Error
- 4.8.2 Payment-Tour
- 2.6.3 Main Screen - Added to Basket
- 2.7.3 Main Screen - Last Transaction 200 - Confirm
- 2.10.1 Bus FLU - Cash Limit
- 7.5.3 Smartcard/Top Up/Remove Smartcard/Expiry
- 4.3.1 FLU/Bank Card/Basket Full
- 1.3.1 Sign On - Incorrect Details
- 3.2.3 Cash Limit Error

### Decision Points (6)
- Is the route number correct?
- Typing a number will display numerical input menu.
- Pressing the "-" key will allow the operator to see another set of product groups down the L buttons.
- Is the route number associated to a Day Tours product?
- Basket
- Payment

### Annotations / Spec Notes (59)
- Bus Ticket Flow
- If the POS reaches the configured time out on the FLU screens, the user is signed out and break mode is skipped.
- POS will display the first boarding stage and last alighting stage of the selected route.  Operator will be able to use "⌃" and "⌵" keys to scroll between routes.
- The operator will be able to choose the direction of the route pressing R2 key. Pressing R6 or enter key will confirm the Route entered.
- The unused buttons that have been left blank (L4-L5) may be used by Translink at a later date if required. User is able to select Bus from this screen pressing L1 key.
- Operator will be able to enter Route Number in numerical keyboard.
- Pressing 'C' button will take operator back to main screen.
- POS will display the FLU screen for bus, containing products which can be selected using L1-L5 keys and stages which can be selected using R1-R5 keys.  After signing on and route selection, the POS will check the default boarding stage text (available for setting in Technician Mode) against the list of boarding stage names on the route and if any contain the text of the default stage then that boarding stage will be used as the default for that route. L1 - L5 buttons can be configured to result in a sub-menu or a list of products with fares.  Products with a £0.00 fare will display as "Invalid".
- POS will display the Day Tour product name for the selected route.  Operator will be able to use "⌃" and "⌵" keys to scroll between routes.
- Operator will be able to enter Route Number in numerical keyboard.
- Pressing 'C' button will take operator back to main screen.
- Pressing "*" button here does the following:-  - Press once shows the fare breaks  - Press twice shows the favourites that have been selected in Cloudfare - Press again and it goes back to normal display
- Operator will be able to access letters pressing '*' key.
- Operator will be able to access letters pressing '*' key.
- User can use "⌃" and "⌵" buttons to load next or previous 4 stages.
- Ticket type changed
- End of stages list
- Yes
- User can change boarding stage using "<" and ">" buttons.
- Operator can use "⌃" and "⌵" buttons to load next or previous 4 stages. Boarding stage change or ticket type change will deselect the alighting stage.
- Pressing Enter will confirm the route entered.
- Selecting one of the misc products available will require operator to type in an open fare for the selected product.
- Operator is able to confirm value pressing R6 or Enter.
- After selecting alighting stage, the operator will be able to add the product in the basket pressing R6 key.
- Pressing the Alighting Stage again will allow the user to change Currency. If they press the Alighting Stage button again, this will change the currency back to GBP.
- Pressing "+" button when a toggle button is selected will show a menu with all items (ticket types)
- Operator will be able to access letters pressing '*' key.
- Operator will be able to access letters pressing '*' key.
- No
- User Selects Day Tour product from the list
- Pressing '*' key again will take operator back to Main screen with the entered route available.
- Pressing Enter on FLU screen when the basket is not empty will take operator to the basket.
- Pressing 'C' button from any FLU screen will take operator to Route Selection screen.
- Yes
- Pressing Enter will confirm the route entered.
- After Payment POS will print the ticket(s) and will return to FLU screen defaulting to Adult Single and deselect alighting stage, while displaying a confirmation message in the top bar with a configurable timeout of 2 seconds.
- The error message will have a 2 seconds timeout.
- Pressing '*' key again will take operator back to previous screen with the entered route available.
- No
- After selecting, user will see ticket type in bottom bar.
- Pressing the 'Back' key will take the user to the main screen.  The list of products on this screen will depend on the day tour that has been selected.  To keep compatibility with the legacy system, the user will only be able to issue one ticket/seat per transaction.
- Pressing Enter on FLU screen when the basket is empty will take operator directly to the payment screen.
- Payment
- Payment
- If operator eneters an invalid value (minimum and maximum values to be determined), an error banner will be displayed.
- Pressing the 'Back' key will take the user to the 'Day Tour Product' screen.  The input is numbers-only.
- Pressing the 'Back' key will take the user to the 'Day Tour Product' screen.  Pressing the 'C' key will clear one character at a time in the input field. If the input field is empty, the user will be taken back one screen.
- The error message will have a 2 seconds timeout.
- The input field will default to today's date.  The up and down arrows will increment the date. The user will not be able to go behind today's date.  Pressing the 'Back' key will take the user to the 'Seat Number Entry' screen.  Pressing the 'C' key will go back to today's date.
- Pressing the 'Back' key will take the user to the 'Seat Number Entry' screen.  Pressing the 'C' key will go back to today's date.
- Pressing the 'Back' key will take the user to the 'Date Entry' screen.  This will follow the usual payment flow.
- Cash Limit
- Tone sounds
- If links for the sounds below don't work, please use the following link and download the sound on your computer: https://drive.google.com/drive/folders/1GeCT1YdpNuqKTRN1C_swZw4rdAD_vkat
- If a preconfigured amount is approaching a notification will be displayed. This will appear after ticket confirmation is displayed and will have a timeout of 3 seconds.
- Whenever an error screen is displayed on POS, an error tone will be played: https://sndup.net/29yg/Error.wav
- Whenever an success screen is displayed on POS, an success tone will be played: https://sndup.net/6n62/Success.wav
- Whenever a screen times out on POS, a time out tone will be played: https://sndup.net/3ckg/Timeout.wav
- If the maximum revenue is reached, the POS machine will lock and a Supervisor or Technician will need to be notified.  The POS needs to retrieve the connection with the back office, operation that will be done in the background.

### Connections / Flow (58)
- Screen: "2.5.3 Main Screen - FLU - Change Boarding Stage" → Screen: "2.5.4 Main Screen - FLU - Alighting Stages 23 & 24"
- Screen: "2.5.3 Main Screen - FLU - Change Boarding Stage" → Decision: "76e88af1-df3f-43cb-aca4-240155061c6f"
- Screen: "2.5.3 Main Screen - FLU - Change Boarding Stage" → Screen: "2.5.5 Main Screen - FLU - Change Fare type"
- Screen: "2.6.1 FLU - Other" → Screen: "2.7.2 Toggle Group - Flu Product Selected from Menu"
- Screen: "2.6.3 Main Screen - Added to Basket" → Decision: "Basket"
- Screen: "2.6.2 Main Screen - FLU - Alighting Selected" → Screen: "2.6.3 Main Screen - Added to Basket"
- Decision: "Basket" → Decision: "c40a40ea-e098-4be3-965b-7ad343eee28c"
- Screen: "2.5.3 Main Screen - FLU - Change Boarding Stage" → Screen: "2.6.1 FLU - Other"
- Screen: "2.5.2 Main Screen-Ulsterbus selected" → Screen: "2.7.1 Main Screen - FLU - Change Ticket type"
- Screen: "2.5.2 Main Screen-Ulsterbus selected" → Screen: "2.5.3 Main Screen - FLU - Change Boarding Stage"
- Decision: "c40a40ea-e098-4be3-965b-7ad343eee28c" → Screen: "2.7.3 Main Screen - Last Transaction 200 - Confirm"
- Screen: "2.5.2 Main Screen-Ulsterbus selected" → Screen: "2.6.2 Main Screen - FLU - Alighting Selected"
- Screen: "2.0 Main Screen" → Screen: "2.1 Main Screen - digits entered"
- Screen: "2.1 Main Screen - digits entered" → Screen: "2.2.2 Route Number - Letters ETM"
- Screen: "2.0 Main Screen" → Screen: "2.2.1 Route Number - Letters ETM - empty"
- Screen: "2.2.2 Route Number - Letters ETM" → Screen: "2.3 Main Screen - route entered"
- Screen: "2.3 Main Screen - route entered" → Screen: "2.4 Main Screen - direction changed"
- Decision: "Is the route number
correct?" → Screen: "2.5.2 Main Screen-Ulsterbus selected"
- Decision: "Is the route number
correct?" → Screen: "2.2.3 Route Number - Letters - Error"
- Screen: "2.2.2 Route Number - Letters ETM" → Decision: "Is the route number
correct?"
- Decision: "Is the route number
correct?" → Screen: "2.2.4 Main Screen - Error"
- Screen: "2.4 Main Screen - direction changed" → Decision: "Is the route number
correct?"
- Screen: "2.6.2 Main Screen - FLU - Alighting Selected" → Decision: "c40a40ea-e098-4be3-965b-7ad343eee28c"
- Screen: "2.5.2 Main Screen-Ulsterbus selected" → Screen: "2.0 Main Screen"
- Screen: "2.2 Main Screen-Rail selected" → Screen: "2.0 Main Screen"
- Screen: "2.0 Main Screen" → Screen: "2.2 Main Screen-Rail selected"
- Screen: "2.5.2 Main Screen-Ulsterbus selected" → Decision: "Typing a number will display numerical input menu."
- Screen: "2.9 FLU - Day Tour Product" → Screen: "2.9.1 FLU - Day Tour Product - Seat Number Entry" [User selects a product.]
- Screen: "2.9.1 FLU - Day Tour Product - Seat Number Entry" → Screen: "2.9.1.1 FLU - Day Tour Product - Seat Number Entered" [User enters a seat number.]
- Screen: "2.9.1.1 FLU - Day Tour Product - Seat Number Entered" → Screen: "2.9.2 FLU - Day Tour Product - Date Entry" [User presses 'Enter' key.]
- Screen: "2.9.2 FLU - Day Tour Product - Date Entry" → Screen: "2.9.2.1 FLU - Day Tour Product - Date Entered" [User inputs new date
using numerical keys.
The up and down arrows
will increment the date]
- Screen: "2.9.2.1 FLU - Day Tour Product - Date Entered" → Screen: "4.8.2 Payment-Tour" [User presses 'Enter' key.]
- Screen: "2.2 Main Screen-Rail selected" → Screen: "2.3.3 Main Screen - Misc"
- Decision: "d5141f9e-2f90-44ac-82b7-b6fa905a01d7" → Screen: "2.2 Main Screen-Rail selected"
- Screen: "2.3.3 Main Screen - Misc" → Screen: "2.3.1 FLU - Misc Product Open Fare"
- Screen: "4.8.3 Payment-Misc Product" → Decision: "d5141f9e-2f90-44ac-82b7-b6fa905a01d7"
- Screen: "2.10.1 Bus FLU - Cash Limit" → Screen: "3.2.3 Cash Limit Error"
- Screen: "2.7.3 Main Screen - Last Transaction 200 - Confirm" → Screen: "2.10.1 Bus FLU - Cash Limit"
- Screen: "4.3.1 FLU/Bank Card/Basket Full" → Screen: "2.6.3 Main Screen - Added to Basket" [3 seconds timeout
to return to FLU screen]
- Screen: "2.3.1 FLU - Misc Product Open Fare" → Screen: "2.3.2 FLU - Misc Product Open Fare Entered"
- Screen: "2.3.2 FLU - Misc Product Open Fare Entered" → Screen: "4.8.3 Payment-Misc Product"
- Screen: "2.3.1 FLU - Misc Product Open Fare" → Screen: "2.4.1 FLU - Misc Product Open Fare Invalid"
- Screen: "2.3.2 FLU - Misc Product Open Fare Entered" → Screen: "2.4.1 FLU - Misc Product Open Fare Invalid"
- Screen: "2.3.2 FLU - Misc Product Open Fare Entered" → Screen: "4.8.3 Payment-Misc Product"
- Screen: "2.9.2 FLU - Day Tour Product - Date Entry" → Screen: "2.9.2.1 FLU - Day Tour Product - Date Entered"
- Screen: "2.5.3 Main Screen - FLU - Change Boarding Stage" → Decision: "Pressing the "-" key will allow the operator to see another set of product groups down the L buttons."
- Screen: "4.8.2 Payment-Tour" → Decision: "Payment"
- Screen: "2.2 Main Screen-Rail selected" → Screen: "Day Tours - empty"
- Screen: "Day Tours - empty" → Screen: "Day Tours - digits entered"
- Screen: "Day Tours - empty" → Screen: "Day Tours - Letters ETM - empty"
- Screen: "Day Tours - digits entered" → Screen: "Day Tours - Letters ETM"
- Screen: "Day Tours - Letters ETM - empty" → Screen: "Day Tours - empty"
- Screen: "Day Tours - Letters ETM" → Screen: "Day Tours - route entered"
- Screen: "Day Tours - route entered" → Decision: "Is the route number
associated to a
Day Tours product?"
- Decision: "Is the route number
associated to a
Day Tours product?" → Screen: "2.9 FLU - Day Tour Product"
- Decision: "Is the route number
associated to a
Day Tours product?" → Screen: "Day Tours - Error"
- Decision: "Is the route number
associated to a
Day Tours product?" → Screen: "Day Tours - Letters - Error"
- Screen: "Day Tours - Letters ETM" → Decision: "Is the route number
associated to a
Day Tours product?"


## 4. 3.0 FLU - Rail

### Screens (26)
- 2.2 Main Screen-Rail selected
- 2.2.5 Main Screen-Rail-FavTicketIssued
- 2.3 Main Screen-Rail-No Fav
- 3.2 Main Screen-Rail-3DayTicket
- 3.4 Main Screen-Rail-Added in Basket
- 3.3 Main Screen-Advance TIcket Selected 
- 3.5 Main Screen-Rail-Confirmed Ticket
- 3.0 Main Screen-Rail-v4
- 3.1.3 Passengers Type
- 3.1.4 Ticket Type
- 4.2.1 Main Screen - FLU - Advance Ticket
- 4.2.2 Main Screen - FLU - Advance Ticket-complete
- 3.1.2 Main Screen-Rail-Alighting Stations
- 3.1.5 Favourite Tickets/List
- 3.1.7 Favourite Tickets/Overwrite
- 3.1.1 Main Screen-Rail-Board Stations
- 3.1.6 Favourite Tickets/List-Next Page
- 3.4.1 FLU-3DayTicket-Available Days
- 3.4.2 FLU-3DayTicket-Selected Days
- 3.3.3 FLU-3DayTicket-Start
- 4.5.1 FLU/Invalid Date
- 3.1 Main Screen-Rail-currency changed
- Main Screen-Rail-boarding-alighting-same
- 2.2.5 Main Screen-Rail-FavTicketIssued
- 3.2.2 FLU Rail-Cash Limit
- 3.2.3 Cash Limit Error

### Decision Points (13)
- After payment, operator will return automatically to main screen while displaying a confirmation message in the top bar with a timeout of 2 seconds.
- If No Favourite Ticket was set, POS will show this as Main Screen.
- Operator may select any of the favourites displayed pressing R1-R5 keys.
- Operator may select any of the favourites displayed pressing R1-R5 keys.
- If the chosen ticket type here is not available after the advance date is entered (i.e. that ticket type is invalid on the advance date) then the POS will revert to show a ticket type which is valid on the advance date.
- Typing a number followed by L1/L2 key will automatically set boarding/alighting stations, as described in numerical input flows.
- Pressing the down arrow shows the Operator Favourites 6 to 10, then pressing up will return to this screen.
- Basket
- L4 button will have the functionability of a toggle button, switching between ticket types  when depressed.
- Operator will be able to use 'right' and 'left' buttons increment and decrement the boarding station and 'up' and 'down' buttons increment and decrement the alighting station".
- Is the date valid?
- Pressing Cancel will return to Rail FLU screen
- If Cancel is pressed, POS will return to the FLU screen, discarding advance ticket option.

### Annotations / Spec Notes (34)
- Rail Ticket Flow
- If the POS reaches the configured time out on the FLU screens, the user is signed out and break mode is skipped.
- Payment
- When the advance date is set the POS operator will have the ability to select a ticket type after this without the advance date defaulting back to current date. This means that the advance date will stay on screen until a) a ticket is issued or b) the operator changes the advance date. The Advanced Date, Passenger Type and Ticket Type will be reset if the POS is inactive for 1 minute.
- After Payment POS will print the ticket(s) and will return to FLU screen keeping the last ticket it issued and only changing ticket type to Adult Single default, if the operator changes the Boarding or Alighting Station.  A confirmation beep sound is produced when ticket is issued.  The confirmation banner will have a timeout of 2 seconds.
- An advance ticket can only be purchased as one ticket at a time. The advance ticket option will not be available if there are multiple products in the basket.
- Choosing 'Rail FLU' will show the specific Rail FLU page.
- Pressing Enter on FLU screen when the basket is empty will take operator directly to the payment screen.
- All products will be displayed (available for passenger type selection). The product list can be ordere by Translink on Cloudfare. Selecting any will populate the field on the main FLU screen.
- User will receive a list with passenger types which can be ordered by Translink on Cloudfare. Selecting any will return to the previous screen keeping the selection. If more passengers types are added from Cloudfare and will not fit in the page, then the page will become scrollable and display in bottom navigation bar the afferent message for scrolling.
- Pressing + key in FLU screen will show a list with favourite tickets if set. If no favourite ticket was set, POS will display open slots items.  Slots numbering will sort the order of the favourites displayed in the Main Menu screen.
- Payment
- If a date for advance ticket is selected the information for the advance button will change to 'Ticket Date DD/MM/YY'. If operator will press this button will go back to date selection screen for advance ticket.
- Choosing an already set favourite, operator will be able to see the complete information of the ticket to be overwritten and the information  for their current selection on the Rail FLU screen.
- User will receive a scrollable list with stations. Selecting any will return to the main screen keeping the selection. Other method is to use Numerical input from previous screen.
- The POS operator will only be able to see the ticket types which are available on the date in question. If the FLU has been advance dated it will show the ticket types which are available on that date.
- This screen shows cross border ticket types if the Boarding or Alighting station is a cross border station and local ticket types if neither Boarding nor Alighting station is a cross border station.
- Pressing 'C' button from any FLU screen would take user to Main Screen.
- After favourite ticket setting is finished, POS will return automatically to Rail FLU screen.
- YES
- Favourite Ticket Set Successfully
- If a day selected, operator presses again the same button it will deselect that specific day. The days unavailable for selection will be greyed out. After confirming operator will return to FLU screen with the specific product selected. He will be able to press Enter to issue the ticket or to press 'Add to Basket button' from FLU screen.
- User has to choose available starting date.
- NO
- User will receive a scrollable list with stations. Selecting any will return to the previous screen keeping the selection. Other method is to use Numerical input from previous screen.
- After sign on, Rail Flu will default to the last stations entered before sign-off.
- Choosing an available slot will directly set as favourite in that desired slot.
- Operator has to enter date of the advance ticket. After confirming operator will return to FLU screen.  He will be able to press Enter to issue the ticket or to press 'Add to Basket button' from FLU screen. "Pressing "C" will take the operator back to the date input screen.
- Pressing the button corresponding the price will change currency to euro if cross border journey was selected. Pressing it again will change to default currency.
- If operator choses for both boarding and alighting the same station, then the passenger and ticket types, along with the price, advance ticket option and basket will become unavailable.
- The error will have a 3 seconds timeout for returning to the previous screen. User will be able to override pressing any key. This screen appears if the date entered is invalid or the advance date is valid but is outside the valid advance date range for that ticket type on Cloudfare.
- Cash Limit
- If a preconfigured amount is approaching a notification will be displayed. This will appear after ticket confirmation is displayed and will have a timeout of 3 seconds.
- If the maximum revenue is reached, the POS machine will lock and a Supervisor or Technician will need to be notified.  The POS needs to retrieve the connection with the back office, operation that will be done in the background.

### Connections / Flow (56)
- Screen: "2.2 Main Screen-Rail selected" → Screen: "3.0 Main Screen-Rail-v4"
- Screen: "3.0 Main Screen-Rail-v4" → Screen: "3.1.1 Main Screen-Rail-Board Stations"
- Screen: "3.0 Main Screen-Rail-v4" → Screen: "3.1.2 Main Screen-Rail-Alighting Stations"
- Screen: "3.0 Main Screen-Rail-v4" → Screen: "3.1.3 Passengers Type"
- Screen: "3.0 Main Screen-Rail-v4" → Screen: "3.1.4 Ticket Type"
- Screen: "3.0 Main Screen-Rail-v4" → Screen: "2.2 Main Screen-Rail selected"
- Screen: "3.1.4 Ticket Type" → Screen: "3.3.3 FLU-3DayTicket-Start"
- Screen: "3.3.3 FLU-3DayTicket-Start" → Screen: "3.4.1 FLU-3DayTicket-Available Days"
- Screen: "3.4.1 FLU-3DayTicket-Available Days" → Screen: "3.4.2 FLU-3DayTicket-Selected Days"
- Decision: "Basket" → Decision: "06a58d4e-0c5f-4f50-af99-48f876170c03"
- Screen: "3.4 Main Screen-Rail-Added in Basket" → Decision: "Basket"
- Decision: "06a58d4e-0c5f-4f50-af99-48f876170c03" → Screen: "3.5 Main Screen-Rail-Confirmed Ticket"
- Screen: "3.0 Main Screen-Rail-v4" → Decision: "L4 button will have the functionability of a toggle button, switching between ticket types 
when depressed."
- Screen: "2.2 Main Screen-Rail selected" → Decision: "c650528b-99ed-4e79-9e8b-33acde8aa314"
- Screen: "2.2.5 Main Screen-Rail-FavTicketIssued" → Screen: "2.2 Main Screen-Rail selected"
- Decision: "c650528b-99ed-4e79-9e8b-33acde8aa314" → Screen: "2.2.5 Main Screen-Rail-FavTicketIssued"
- Screen: "3.0 Main Screen-Rail-v4" → Decision: "Operator will be able to use 'right' and 'left' buttons increment and decrement the boarding station and 'up' and 'down' buttons increment and decrement the alighting station"."
- Screen: "3.0 Main Screen-Rail-v4" → Screen: "3.4 Main Screen-Rail-Added in Basket"
- Screen: "3.0 Main Screen-Rail-v4" → Decision: "06a58d4e-0c5f-4f50-af99-48f876170c03"
- Screen: "3.0 Main Screen-Rail-v4" → Screen: "4.2.1 Main Screen - FLU - Advance Ticket"
- Screen: "4.2.1 Main Screen - FLU - Advance Ticket" → Screen: "4.2.2 Main Screen - FLU - Advance Ticket-complete"
- Screen: "4.2.2 Main Screen - FLU - Advance Ticket-complete" → Decision: "Is the date valid?"
- Screen: "3.3 Main Screen-Advance TIcket Selected " → Decision: "06a58d4e-0c5f-4f50-af99-48f876170c03"
- Screen: "3.4.2 FLU-3DayTicket-Selected Days" → Screen: "3.2 Main Screen-Rail-3DayTicket"
- Screen: "3.4.1 FLU-3DayTicket-Available Days" → Screen: "3.3.3 FLU-3DayTicket-Start"
- Screen: "4.2.1 Main Screen - FLU - Advance Ticket" → Decision: "If Cancel is pressed, POS will return to the FLU screen, discarding advance ticket option."
- Screen: "3.3 Main Screen-Advance TIcket Selected " → Screen: "4.2.2 Main Screen - FLU - Advance Ticket-complete"
- Screen: "3.4.2 FLU-3DayTicket-Selected Days" → Screen: "3.2 Main Screen-Rail-3DayTicket"
- Screen: "4.2.2 Main Screen - FLU - Advance Ticket-complete" → Decision: "Is the date valid?"
- Screen: "3.0 Main Screen-Rail-v4" → Screen: "3.1 Main Screen-Rail-currency changed"
- Screen: "3.1 Main Screen-Rail-currency changed" → Screen: "3.0 Main Screen-Rail-v4"
- Screen: "4.2.2 Main Screen - FLU - Advance Ticket-complete" → Screen: "4.2.1 Main Screen - FLU - Advance Ticket"
- Decision: "Is the date valid?" → Screen: "3.3 Main Screen-Advance TIcket Selected "
- Decision: "Is the date valid?" → Screen: "4.5.1 FLU/Invalid Date"
- Screen: "3.2 Main Screen-Rail-3DayTicket" → Decision: "Basket"
- Screen: "3.2 Main Screen-Rail-3DayTicket" → Decision: "06a58d4e-0c5f-4f50-af99-48f876170c03"
- Screen: "3.5 Main Screen-Rail-Confirmed Ticket" → Screen: "3.0 Main Screen-Rail-v4"
- Screen: "3.3.3 FLU-3DayTicket-Start" → Screen: "3.1.4 Ticket Type"
- Screen: "3.2 Main Screen-Rail-3DayTicket" → Screen: "3.0 Main Screen-Rail-v4"
- Screen: "3.0 Main Screen-Rail-v4" → Decision: "Typing a number followed by L1/L2 key will automatically set boarding/alighting stations, as described in numerical input flows."
- Screen: "3.0 Main Screen-Rail-v4" → Decision: "Typing a number followed by L1/L2 key will automatically set boarding/alighting stations, as described in numerical input flows."
- Screen: "2.2 Main Screen-Rail selected" → Decision: "Pressing the down arrow shows the Operator Favourites 6 to 10, then pressing up will return to this screen."
- Screen: "3.0 Main Screen-Rail-v4" → Screen: "3.1.5 Favourite Tickets/List"
- Screen: "3.1.5 Favourite Tickets/List" → Screen: "3.1.7 Favourite Tickets/Overwrite"
- Screen: "3.1.6 Favourite Tickets/List-Next Page" → Decision: "e02ca855-11da-4624-a139-7c2a5a37f125"
- Screen: "3.1.7 Favourite Tickets/Overwrite" → Decision: "e02ca855-11da-4624-a139-7c2a5a37f125"
- Screen: "3.1.5 Favourite Tickets/List" → Decision: "Pressing Cancel will return to Rail FLU screen"
- Screen: "3.1.7 Favourite Tickets/Overwrite" → Decision: "Pressing Cancel will return to Rail FLU screen"
- Screen: "2.2.5 Main Screen-Rail-FavTicketIssued" → Screen: "3.2.2 FLU Rail-Cash Limit"
- Screen: "3.2.2 FLU Rail-Cash Limit" → Screen: "3.2.3 Cash Limit Error"
- Screen: "3.1.5 Favourite Tickets/List" → Screen: "3.1.6 Favourite Tickets/List-Next Page"
- Screen: "3.1.6 Favourite Tickets/List-Next Page" → Screen: "3.1.5 Favourite Tickets/List"
- Screen: "3.1.5 Favourite Tickets/List" → Screen: "3.1.7 Favourite Tickets/Overwrite"
- Screen: "3.1.6 Favourite Tickets/List-Next Page" → Decision: "e02ca855-11da-4624-a139-7c2a5a37f125"
- Screen: "3.3 Main Screen-Advance TIcket Selected " → Decision: "If the chosen ticket type here is not available after the advance date is entered (i.e. that ticket type is invalid on the advance date) then the POS will revert to show a ticket type which is valid on the advance date."
- Screen: "3.1.2 Main Screen-Rail-Alighting Stations" → Screen: "Main Screen-Rail-boarding-alighting-same"


## 5. 4.0 Basket & Payment

### Screens (45)
- 3.0 Main Screen-Rail-v4
- 3.4 Main Screen-Rail-Added in Basket
- 4.1.2  Main Screen - FLU - Multiple Items - Basket - Page 1
- 4.1.6 Main Screen - FLU - Multiple Items - Basket - Selected Added
- 4.1.5 Main Screen - FLU - Multiple Items - Basket is Full
- 4.1.1 Main Screen - FLU - Multiple Items - Basket - 1Item
- 4.1.3 Main Screen - FLU - Multiple Items - Basket - Selected
- 4.1.4 Main Screen - FLU - Multiple Items - Basket - Item removed
- 4.2.3 Main Screen - FLU - Multiple Items - Payment
- 4.3.1 FLU/Bank Card/Basket Full
- 4.3.3 FLU - Clear Basket
- 3.5 Main Screen-Rail-Confirmed Ticket
- 4.2.4 Main Screen - FLU - Multiple Items - Payment - Bank Card Unavailable
- 2.5.2 Main Screen-Ulsterbus selected
- 2.6.2 Main Screen - FLU - Alighting Selected
- 2.6.3 Main Screen - Added to Basket
- 4.1.2  Main Screen - FLU - Multiple Items - Basket - Page 1
- 4.1.6 Main Screen - FLU - Multiple Items - Basket - Selected Added
- 4.1.5 Main Screen - FLU - Multiple Items - Basket is Full
- 4.1.1 Main Screen - FLU - Multiple Items - Basket - 1Item
- 4.1.7 Main Screen - FLU - Multiple Items - Basket - 1Item - Bus Advance Ticket
- 4.1.6 Main Screen - FLU - Multiple Items - Basket - Selected
- 4.1.4 Main Screen - FLU - Multiple Items - Basket - Item removed
- 4.2.1 Main Screen - FLU - Advance Ticket
- 4.2.2 Main Screen - FLU - Advance Ticket-complete
- 4.3.3 FLU - Clear Basket
- 4.2.3 Main Screen - FLU - Multiple Items - Payment
- 4.3.1 FLU/Bank Card/Basket Full
- 4.5.1 FLU/Invalid Date
- 2.7.3 Main Screen - Last Transaction 200 - Confirm
- 4.2.4 Main Screen - FLU - Multiple Items - Payment - Bank Card Unavailable
- 3.3 Main Screen-Advance TIcket Selected 
- 2.2.5 Main Screen-Rail-FavTicketIssued
- 3.2 Main Screen-Rail-3DayTicket
- 3.5 Main Screen-Rail-Confirmed Ticket
- 2.2 Main Screen-Rail selected
- 4.8.1 Payment-3day ticket
- 4.6.1 Main Screen - FLU - Payment - Popular
- 4.1.7 Main Screen - FLU - Multiple Items - Basket - 1Item - Bus Advance Ticket
- 3.5 Main Screen-Rail-Confirmed Ticket
- 4.2.2 Main Screen - FLU - Advance Ticket-complete
- 4.4.1 Main Screen - FLU - Payment - Advance Ticket
- 4.6.1 Main Screen - FLU - Payment - Popular - Card Unavailable
- 4.8.1 Payment-3day ticket-card unavailable
- 4.4.2 Main Screen - FLU - Payment - Advance Ticket - Card Unavailable

### Decision Points (13)
- User tries to add more then 9 tickets to basket
- Pressing R6 again will add another ticket to the basket.
- The operator may select Advance Ticket option from the basket if only one ticket is added to the basket, as well from the FLU screen.  For Advance Ticket flow on the Rail Basket please see screens 4.2.1 and 4.2.2 in the Bus Basket flow.
- Is PCD attached to the POS?
- User tries to add more then 9 tickets to basket
- Pressing R6 again will add another ticket to the basket.
- The operator may select Advance Ticket option from the basket if only one ticket is added to the basket.
- Is the date valid?
- Is PCD attached to the POS?
- If Cancel is pressed, POS will return to the FLU screen, discarding advance ticket option.
- Is PCD attached to the POS?
- Is PCD attached to the POS?
- Is PCD attached to the POS?

### Annotations / Spec Notes (79)
- Basket Flow Rail
- Senior Single (and all other smartcard pass types e.g. War Pensioner, Blind, yLink, 24+, Half-Fare etc) cannot be added to a basket as they require Smartcard validation per individual transaction.
- Operator chooses boarding and alighting stages.
- After selecting alighting stage, the operator will be able to add the product in the basket pressing R6 key.
- No
- In basket screen, user may scroll between tickets if more then 3 tickets added, add more tickets, clear basket or remove tickets from the basket using R1-R3 buttons.
- User is allowed to add a maximum of 9 tickets to the basket. If the maximum is reached the 'Add More' button becomes unavailable so the operator is unable to add any more tickets to the basket. If an item is deleted from the basket then the 'Add More' button will become available again.
- Pressing Enter on FLU screen when the basket is not empty will take operator to the basket.
- User may select an item, pressing the corresponding L1-L3 / R1-R3 buttons. When selected, the 'Delete item'option will become available.
- If a ticket is selected, operator may increase or decrease the number of passengers on that line using + and - keys.  Maximum of passengers per line is 100. Each line will result in one printed ticket.
- Yes
- Pressing Add More button, user will go back to Main Screen, to add another ticket to the basket.
- After confirming, user will be able to select payment method. He will still be able to scroll ticket list or to add more tickets to basket, if the maximum amount is not reached.
- User is allow to add maximum 9 tickets to basket. If trying to add more he will receive an error message and is able to press any key to go back.
- User will follow Card Payment flow.
- The error will have a 3 seconds timeout for returning to the previous screen. User will be able to override pressing any key.
- Yes
- Card Payment
- Choosing 'Clear basket' will show a confirmation screen. If confirmed, the basket is cleared and user is taken back to Main Screen.
- No
- After Payment POS prints the ticket(s) and returns back to the default Rail screen once the confirmation banner has timed out.
- Pressing back will take user back to basket. Add more will take user back to the specific FLU screen he started (if Bus with route selected, then route should be memorised).
- Add More option will take user back to Rail FLU for adding more products to the basket.
- If there isn't any PCD attached to the POS, Bank Card option will be unavailable.
- Basket Flow Bus
- Senior Single (and all other smartcard pass types e.g. War Pensioner, Blind, yLink, 24+, Half-Fare etc) cannot be added to a basket as they require Smartcard validation per individual transaction.
- Operator chooses boarding and alighting stages.
- After selecting alighting stage, the operator will be able to add the product in the basket pressing R6 key.
- No
- In basket screen, user may scroll between tickets if more then 3 tickets added, add more tickets, clear basket or remove tickets from the basket using R1-R3 buttons.
- User is allowed to add a maximum of 9 tickets to the basket. If the maximum is reached the 'Add More' button becomes unavailable so the operator is unable to add any more tickets to the basket. If an item is deleted from the basket then the 'Add More' button will become available again
- User may select an item, pressing the corresponding L1-L3 / R1-R3 buttons. When selected, the 'Delete item'option will become available.
- If a ticket is selected, operator may increase or decrease the number of passengers on that line using + and - keys.  Maximum of passengers per line is 100. Each line will result in one printed ticket.
- Pressing Enter on FLU screen when the basket is not empty will take operator to the basket.
- Yes
- If a date for advance ticket is selected the information for the advance button will change to 'Ticket Date DD/MM/YY'. If operator will press this button will go back to date selection screen for advance ticket.
- Pressing Add More button, user will go back to Main Screen, to add another ticket to the basket. On Bus Basket the operator cannot add tickets from 2 different routes. On Bus Basket the operator can add tickets with 2 different boarding stages on the same route.
- After confirming, user will be able to select payment method. He will still be able to scroll ticket list or to add more tickets to basket, if the maximum amount is not reached.
- Choosing 'Clear basket' will show a confirmation screen. If confirmed, the basket is cleared and user is taken back to Main Screen.
- User is allow to add maximum 9 tickets to basket. If trying to add more he will receive an error message and is able to press any key to go back.
- User will follow Card Payment flow.
- The error will have a 3 seconds timeout for returning to the previous screen. User will be able to override pressing any key.
- YES
- Yes
- Card Payment
- This screen appears if the date entered is invalid or the advance date is valid but is outside the valid advance date range for that ticket type on Cloudfare.
- NO
- No
- After Payment POS will print the ticket(s) and will return to FLU screen defaulting to Adult Single and deselect alighting stage, while displaying a confirmation message in the top bar with a configurable timeout of 2 seconds.
- Operator has to enter date of the advance ticket. After confirming the POS will display Payment screen.  He will be able to press Enter to issue the ticket or to press 'Add to Basket button' from FLU screen. Pressing C will delete a character at a time.
- Pressing back will take user back to basket. Add more will take user back to the specific FLU screen he started (if Bus with route selected, then route should be memorised).
- If there isn't any PCD attached to the POS, Bank Card option will be unavailable.
- The error will have a 3 seconds timeout for returning to the previous screen. User will be able to override pressing any key.
- Favourite tickets payment
- Advance Ticket
- Three Day Ticket
- User may select one of the popular rail tickets in main screen and will be taken to payment screen directly. This type of ticket cannot be sent to the basket or added to another tickets in the basket.
- After payment a notification containing alighting station and price will be displyed in the top bar.
- Three Day Ticket was previously selected by the operator and data was updated in this screen.
- After payment a notification containing alighting station and price will be displyed in the top bar.
- When issuing an advanced ticket within the rail FLU straight to the basket or payment screen depending on the button selected as only one advanced ticket is allowed in the basket at a time.
- Operator will choose passengers' choise of payment. Choosing Cash/Warrant options will imediately issue the ticket, Bank Card will follow the specific flow (5.0).
- Operator will choose passengers' choise of payment. Choosing Cash/Warrant options will imediately issue the ticket, Bank Card will follow the specific flow (5.0).
- Operator will be able to go to the date screen selection for changing the date of the advance ticket pressing L4.
- After payment a notification containing alighting station and price will be displyed in the top bar.
- Yes
- Yes
- Card Payment
- Card Payment
- Operator will choose passengers' choise of payment. Choosing Cash/Warrant options will imediately issue the ticket, Bank Card will follow the specific flow (5.0).
- After confirming the date for the advance ticket the bus operator will be taken to the basket automatically.
- No
- No
- Yes
- Card Payment
- If there isn't any PCD attached to the POS, Bank Card option will be unavailable.
- If there isn't any PCD attached to the POS, Bank Card option will be unavailable.
- No
- If there isn't any PCD attached to the POS, Bank Card option will be unavailable.

### Connections / Flow (93)
- Screen: "4.6.1 Main Screen - FLU - Payment - Popular" → Decision: "57e88179-fb1e-4d01-88c3-54646a71001b"
- Screen: "4.8.1 Payment-3day ticket" → Decision: "9ba59e8a-fde8-4974-8101-a63cc3aac2ac"
- Decision: "57e88179-fb1e-4d01-88c3-54646a71001b" → Screen: "2.2.5 Main Screen-Rail-FavTicketIssued"
- Screen: "2.2.5 Main Screen-Rail-FavTicketIssued" → Screen: "2.2 Main Screen-Rail selected"
- Screen: "3.3 Main Screen-Advance TIcket Selected " → Decision: "Is PCD attached
to the POS?"
- Decision: "Is PCD attached
to the POS?" → Screen: "4.4.1 Main Screen - FLU - Payment - Advance Ticket"
- Decision: "Is PCD attached
to the POS?" → Screen: "4.4.2 Main Screen - FLU - Payment - Advance Ticket - Card Unavailable"
- Screen: "4.4.1 Main Screen - FLU - Payment - Advance Ticket" → Decision: "66903a97-1451-4238-801a-a37ffd2d42b2"
- Screen: "4.4.1 Main Screen - FLU - Payment - Advance Ticket" → Screen: "3.5 Main Screen-Rail-Confirmed Ticket"
- Screen: "4.4.1 Main Screen - FLU - Payment - Advance Ticket" → Screen: "3.5 Main Screen-Rail-Confirmed Ticket"
- Decision: "66903a97-1451-4238-801a-a37ffd2d42b2" → Screen: "3.5 Main Screen-Rail-Confirmed Ticket"
- Screen: "3.2 Main Screen-Rail-3DayTicket" → Decision: "Is PCD attached
to the POS?"
- Decision: "Is PCD attached
to the POS?" → Screen: "4.8.1 Payment-3day ticket"
- Decision: "Is PCD attached
to the POS?" → Screen: "4.8.1 Payment-3day ticket-card unavailable"
- Decision: "9ba59e8a-fde8-4974-8101-a63cc3aac2ac" → Screen: "3.5 Main Screen-Rail-Confirmed Ticket"
- Screen: "4.8.1 Payment-3day ticket" → Screen: "3.5 Main Screen-Rail-Confirmed Ticket"
- Screen: "4.8.1 Payment-3day ticket" → Screen: "3.5 Main Screen-Rail-Confirmed Ticket"
- Screen: "3.5 Main Screen-Rail-Confirmed Ticket" → Screen: "3.2 Main Screen-Rail-3DayTicket"
- Screen: "2.2 Main Screen-Rail selected" → Decision: "Is PCD attached
to the POS?"
- Decision: "Is PCD attached
to the POS?" → Screen: "4.6.1 Main Screen - FLU - Payment - Popular"
- Decision: "Is PCD attached
to the POS?" → Screen: "4.6.1 Main Screen - FLU - Payment - Popular - Card Unavailable"
- Screen: "4.6.1 Main Screen - FLU - Payment - Popular" → Screen: "2.2.5 Main Screen-Rail-FavTicketIssued"
- Screen: "4.6.1 Main Screen - FLU - Payment - Popular" → Screen: "2.2.5 Main Screen-Rail-FavTicketIssued"
- Screen: "4.8.1 Payment-3day ticket-card unavailable" → Screen: "3.2 Main Screen-Rail-3DayTicket"
- Screen: "4.6.1 Main Screen - FLU - Payment - Popular - Card Unavailable" → Screen: "2.2 Main Screen-Rail selected"
- Screen: "4.2.3 Main Screen - FLU - Multiple Items - Payment" → Decision: "7698c19e-f15d-471b-afe9-c87ac3fefc2a"
- Screen: "4.1.2  Main Screen - FLU - Multiple Items - Basket - Page 1" → Screen: "4.1.5 Main Screen - FLU - Multiple Items - Basket is Full"
- Screen: "4.1.2  Main Screen - FLU - Multiple Items - Basket - Page 1" → Screen: "4.1.3 Main Screen - FLU - Multiple Items - Basket - Selected"
- Decision: "User tries to add more then
9 tickets to basket" → Screen: "4.1.2  Main Screen - FLU - Multiple Items - Basket - Page 1"
- Decision: "User tries to add more then
9 tickets to basket" → Screen: "4.3.1 FLU/Bank Card/Basket Full"
- Screen: "4.1.5 Main Screen - FLU - Multiple Items - Basket is Full" → Decision: "Is PCD attached
to the POS?"
- Screen: "3.0 Main Screen-Rail-v4" → Decision: "User tries to add more then
9 tickets to basket"
- Decision: "User tries to add more then
9 tickets to basket" → Screen: "3.4 Main Screen-Rail-Added in Basket"
- Screen: "4.2.3 Main Screen - FLU - Multiple Items - Payment" → Decision: "95220f0c-7a97-4540-abb1-28a9193b42f1"
- Decision: "95220f0c-7a97-4540-abb1-28a9193b42f1" → Screen: "3.5 Main Screen-Rail-Confirmed Ticket"
- Screen: "4.1.3 Main Screen - FLU - Multiple Items - Basket - Selected" → Screen: "4.1.4 Main Screen - FLU - Multiple Items - Basket - Item removed"
- Screen: "4.1.3 Main Screen - FLU - Multiple Items - Basket - Selected" → Screen: "4.1.6 Main Screen - FLU - Multiple Items - Basket - Selected Added"
- Decision: "Is PCD attached
to the POS?" → Screen: "4.2.3 Main Screen - FLU - Multiple Items - Payment"
- Screen: "4.2.3 Main Screen - FLU - Multiple Items - Payment" → Screen: "3.5 Main Screen-Rail-Confirmed Ticket"
- Screen: "4.1.1 Main Screen - FLU - Multiple Items - Basket - 1Item" → Screen: "4.3.3 FLU - Clear Basket"
- Screen: "4.3.3 FLU - Clear Basket" → Screen: "4.1.1 Main Screen - FLU - Multiple Items - Basket - 1Item"
- Screen: "4.1.1 Main Screen - FLU - Multiple Items - Basket - 1Item" → Decision: "Is PCD attached
to the POS?"
- Screen: "4.1.1 Main Screen - FLU - Multiple Items - Basket - 1Item" → Screen: "3.4 Main Screen-Rail-Added in Basket"
- Decision: "Is PCD attached
to the POS?" → Screen: "4.2.4 Main Screen - FLU - Multiple Items - Payment - Bank Card Unavailable"
- Screen: "3.5 Main Screen-Rail-Confirmed Ticket" → Screen: "3.0 Main Screen-Rail-v4"
- Screen: "4.2.3 Main Screen - FLU - Multiple Items - Payment" → Decision: "545d6a9f-6515-4830-88bd-422c6ec0d03d"
- Screen: "4.1.2  Main Screen - FLU - Multiple Items - Basket - Page 1" → Screen: "4.1.5 Main Screen - FLU - Multiple Items - Basket is Full"
- Screen: "4.1.2  Main Screen - FLU - Multiple Items - Basket - Page 1" → Screen: "4.1.6 Main Screen - FLU - Multiple Items - Basket - Selected"
- Decision: "User tries to add more then
9 tickets to basket" → Screen: "4.1.2  Main Screen - FLU - Multiple Items - Basket - Page 1"
- Decision: "User tries to add more then
9 tickets to basket" → Screen: "4.3.1 FLU/Bank Card/Basket Full"
- Screen: "4.3.1 FLU/Bank Card/Basket Full" → Screen: "2.6.2 Main Screen - FLU - Alighting Selected"
- Screen: "4.1.5 Main Screen - FLU - Multiple Items - Basket is Full" → Decision: "Is PCD attached
to the POS?"
- Decision: "User tries to add more then
9 tickets to basket" → Screen: "2.6.3 Main Screen - Added to Basket"
- Screen: "2.6.2 Main Screen - FLU - Alighting Selected" → Decision: "User tries to add more then
9 tickets to basket"
- Screen: "4.2.3 Main Screen - FLU - Multiple Items - Payment" → Decision: "dfbed113-1d08-4f7e-812f-1a1c0c5c1999"
- Decision: "dfbed113-1d08-4f7e-812f-1a1c0c5c1999" → Screen: "2.7.3 Main Screen - Last Transaction 200 - Confirm"
- Screen: "4.1.6 Main Screen - FLU - Multiple Items - Basket - Selected" → Screen: "4.1.4 Main Screen - FLU - Multiple Items - Basket - Item removed"
- Screen: "4.1.6 Main Screen - FLU - Multiple Items - Basket - Selected" → Screen: "4.1.6 Main Screen - FLU - Multiple Items - Basket - Selected Added"
- Decision: "Is PCD attached
to the POS?" → Screen: "4.2.3 Main Screen - FLU - Multiple Items - Payment"
- Screen: "4.2.3 Main Screen - FLU - Multiple Items - Payment" → Screen: "4.1.1 Main Screen - FLU - Multiple Items - Basket - 1Item"
- Screen: "4.2.3 Main Screen - FLU - Multiple Items - Payment" → Screen: "2.7.3 Main Screen - Last Transaction 200 - Confirm"
- Screen: "4.2.3 Main Screen - FLU - Multiple Items - Payment" → Screen: "2.7.3 Main Screen - Last Transaction 200 - Confirm"
- Screen: "4.3.3 FLU - Clear Basket" → Screen: "2.5.2 Main Screen-Ulsterbus selected"
- Screen: "2.6.3 Main Screen - Added to Basket" → Screen: "4.1.1 Main Screen - FLU - Multiple Items - Basket - 1Item"
- Screen: "4.1.1 Main Screen - FLU - Multiple Items - Basket - 1Item" → Screen: "2.6.3 Main Screen - Added to Basket"
- Screen: "4.1.1 Main Screen - FLU - Multiple Items - Basket - 1Item" → Decision: "Is PCD attached
to the POS?"
- Screen: "2.5.2 Main Screen-Ulsterbus selected" → Screen: "2.6.2 Main Screen - FLU - Alighting Selected"
- Screen: "2.6.3 Main Screen - Added to Basket" → Decision: "Pressing R6 again will add another ticket to the basket."
- Screen: "2.7.3 Main Screen - Last Transaction 200 - Confirm" → Screen: "2.5.2 Main Screen-Ulsterbus selected"
- Decision: "Is PCD attached
to the POS?" → Screen: "4.2.4 Main Screen - FLU - Multiple Items - Payment - Bank Card Unavailable"
- Screen: "4.3.1 FLU/Bank Card/Basket Full" → Screen: "3.0 Main Screen-Rail-v4"
- Screen: "4.2.3 Main Screen - FLU - Multiple Items - Payment" → Screen: "4.1.1 Main Screen - FLU - Multiple Items - Basket - 1Item"
- Screen: "4.2.3 Main Screen - FLU - Multiple Items - Payment" → Screen: "3.5 Main Screen-Rail-Confirmed Ticket"
- Screen: "4.2.3 Main Screen - FLU - Multiple Items - Payment" → Decision: "4f7a3501-4715-4709-9abb-fe283c03c1fd"
- Screen: "4.2.1 Main Screen - FLU - Advance Ticket" → Screen: "4.2.2 Main Screen - FLU - Advance Ticket-complete"
- Screen: "4.2.2 Main Screen - FLU - Advance Ticket-complete" → Decision: "Is the date valid?"
- Screen: "4.2.1 Main Screen - FLU - Advance Ticket" → Decision: "If Cancel is pressed, POS will return to the FLU screen, discarding advance ticket option."
- Screen: "4.2.2 Main Screen - FLU - Advance Ticket-complete" → Decision: "Is the date valid?"
- Screen: "4.2.2 Main Screen - FLU - Advance Ticket-complete" → Screen: "4.2.1 Main Screen - FLU - Advance Ticket"
- Decision: "Is the date valid?" → Screen: "4.5.1 FLU/Invalid Date"
- Screen: "4.1.1 Main Screen - FLU - Multiple Items - Basket - 1Item" → Screen: "4.2.1 Main Screen - FLU - Advance Ticket"
- Decision: "Is the date valid?" → Screen: "4.1.7 Main Screen - FLU - Multiple Items - Basket - 1Item - Bus Advance Ticket"
- Screen: "4.1.7 Main Screen - FLU - Multiple Items - Basket - 1Item - Bus Advance Ticket" → Screen: "4.2.2 Main Screen - FLU - Advance Ticket-complete"
- Screen: "4.1.7 Main Screen - FLU - Multiple Items - Basket - 1Item - Bus Advance Ticket" → Decision: "Is PCD attached
to the POS?"
- Screen: "4.2.2 Main Screen - FLU - Advance Ticket-complete" → Screen: "4.1.7 Main Screen - FLU - Multiple Items - Basket - 1Item - Bus Advance Ticket"
- Screen: "3.4 Main Screen-Rail-Added in Basket" → Decision: "Pressing R6 again will add another ticket to the basket."
- Screen: "4.1.6 Main Screen - FLU - Multiple Items - Basket - Selected Added" → Screen: "4.1.3 Main Screen - FLU - Multiple Items - Basket - Selected"
- Screen: "4.1.6 Main Screen - FLU - Multiple Items - Basket - Selected Added" → Screen: "4.1.6 Main Screen - FLU - Multiple Items - Basket - Selected"
- Screen: "4.4.1 Main Screen - FLU - Payment - Advance Ticket" → Screen: "4.1.7 Main Screen - FLU - Multiple Items - Basket - 1Item - Bus Advance Ticket" [Pressing back will take operator
back to the basket, while 
keeping advance date ticket selection.]
- Screen: "3.3 Main Screen-Advance TIcket Selected " → Screen: "4.1.7 Main Screen - FLU - Multiple Items - Basket - 1Item - Bus Advance Ticket"
- Screen: "4.1.7 Main Screen - FLU - Multiple Items - Basket - 1Item - Bus Advance Ticket" → Decision: "Is PCD attached
to the POS?"
- Screen: "4.1.7 Main Screen - FLU - Multiple Items - Basket - 1Item - Bus Advance Ticket" → Screen: "4.2.2 Main Screen - FLU - Advance Ticket-complete"
- Screen: "4.1.1 Main Screen - FLU - Multiple Items - Basket - 1Item" → Screen: "4.3.3 FLU - Clear Basket"


## 6. 5.0 Card Payment

### Screens (21)
- 4.2.3 Main Screen - FLU - Multiple Items - Payment
- 5.1.1 FLU/Bank Card/Initialising Transaction
- 5.2.1 FLU/Bank Card/Present
- 5.3.2 FLU/Bank Card/User Confirming Amount
- 5.3.1 FLU/Bank Card/Customer Confirmation
- 5.5.1 FLU/Bank Card/Transaction Declined 2
- 5.3.2 FLU/Bank Card/User Confirming Amount
- 5.4.1 FLU/Bank Card/Transaction Declined
- 5.4.3 FLU/Transaction Approved-Confirmation
- 5.3.1 FLU/Bank Card/Customer Confirmation
- 5.3.1 FLU/Bank Card/Customer Confirmation
- 5.4.2 FLU/Transaction Approved
- 5.4.3 FLU/Transaction Approved-Confirmation
- 5.2.1.1 FLU/Bank Card/Present Card PIN
- 5.4.1 FLU/Bank Card/Transaction Declined
- 5.5.2 FLU/Bank Card/Customer Signature
- 5.5.1 FLU/Bank Card/Transaction Declined 2
- 5.5.1 FLU/Bank Card/Transaction Declined 2
- 5.4.3 FLU/Transaction Approved-Confirmation
- 5.4.1 FLU/Bank Card/Transaction Declined
- 5.4.1 FLU/Bank Card/Transaction Declined

### Decision Points (16)
- Amount too large? (Test transactions only)
- Payment type
- Over £45, customer decides Chip & PIN, or payment device asks customer to insert their card?
- The operator will be able to cancel a transaction at any time pressing C button which will automatically return to payment screen. If a transaction is cancelled, no receipt will be printed.
- Chip & PIN card available?
- Transaction Succesful?
- Correct PIN Entered?
- When the Print Receipt button is pressed a payment card receipt will be printed and the POS will return to the FLU screen.
- Transaction Succesful?
- A declined card payment receipt will be printed when this screen is displayed.
- Transaction Succesful?
- When the Print Receipt button is pressed a payment card receipt will be printed and the POS will return to the FLU screen.
- A declined card payment receipt will be printed when this screen is displayed.
- When the Print Receipt button is pressed a payment card receipt will be printed and the POS will return to the FLU screen.
- A declined card payment receipt will be printed when this screen is displayed.
- A declined card payment receipt will be printed when this screen is displayed.

### Annotations / Spec Notes (52)
- Card Payment Flow
- From payment screen, user chooses Bank Card.
- Customer has to insert or swipe the card for initialising transaction. If it's a contactless card, the customer can present their card to the device straight away.
- No
- Waiting for customer to press green button on M020 to confirm the amount. The POS will be told the status by the card reader, and will reflect the status from this. Starting transaction > Event (Awaiting card) > Insert card into reader > Events back from card
- the POS will be told the status by the card reader, and will reflect the status from this.  Starting transaction > Event (Awaiting card) > Insert card into reader > Events back from card
- Chip & PIN
- Contactless
- Swipe Card
- Customer is confirming the transaction amount and inputting their PIN.
- Payment terminal is in the process of authorising transaction.
- Yes
- No
- Yes
- As soon as this screen appears the ticket is immediately printed.  Only after the ticket prints does the customer have the option to print a payment card receipt (or not print a payment card receipt and go back to Main Screen).
- Yes
- No
- The value  of transaction is too big for a card payment.
- Payment terminal is in the process of authorising transaction.
- Payment terminal is in the process of authorising transaction.
- No
- Yes
- No
- Yes
- Yes
- Yes
- As soon as this screen appears the ticket is immediately printed.  Only after the ticket prints does the customer have the option to print a payment card receipt (or not print a payment card receipt and go back to Main Screen).
- Timeout of 3 seconds or press any key will go back to Payment Screen.
- Print Ticket
- No
- No
- Regardless of which option is chosen by the POS operator (i.e. Print receipt or Back to Main/No receipt) the POS will revert to screen 2.7.3 (Bus Flu) or 3.2 (Rail Flu) .
- Timeout of 3 seconds or press any key will go back to Payment Screen.
- Print Ticket
- Print a receipt for customer to sign.
- Once the customer presses Yes on this screen the ticket will be printed and the POS will revert to screen 2.7.3 (Bus Flu) or 3.2 (Rail Flu).
- The error messages displayed on the POS screen will be dependent on the error messages received from the M020.
- Customer cancels transaction on PIN pad.
- Customer cancels transaction on PIN pad.
- Regardless of which option is chosen by the POS operator (i.e. Print receipt or Back to Main/No receipt) the POS will revert to screen 2.7.3 (Bus Flu) or 3.2 (Rail Flu) .
- If the provided signature does not match the payment card, user wil receive an error screen with  'Sigature doesn't match payment card'
- The user will be asked to insert their card to pay for the transaction.
- The error messages displayed on the POS screen will be dependent on the error messages received from the M020.
- A declined card payment receipt will be printed when this screen is displayed.  If the customer presses the red x on the M020 before entering the pin there is no cancelled payment receipt.
- If user enters PIN incorrectly more then the accepted amount of times, user will receive an error screen with 'Incorrect PIN entered too many times'.
- If transaction was declined then user will receive the appropriate error message.
- Timeout of 3 seconds or press any key will go back to Payment Screen.
- Timeout of 3 seconds or press any key will go back to Payment Screen.
- Print Ticket
- Timeout of 3 seconds or press any key will go back to Payment Screen.
- Timeout of 3 seconds or press any key will go back to Payment Screen.
- Timeout of 3 seconds or press any key will go back to Payment Screen.

### Connections / Flow (55)
- Screen: "5.3.1 FLU/Bank Card/Customer Confirmation" → Decision: "Transaction Succesful?"
- Decision: "Transaction Succesful?" → Screen: "5.4.3 FLU/Transaction Approved-Confirmation"
- Screen: "5.3.2 FLU/Bank Card/User Confirming Amount" → Screen: "5.5.1 FLU/Bank Card/Transaction Declined 2"
- Screen: "5.4.3 FLU/Transaction Approved-Confirmation" → Decision: "46190e4d-2ebc-436f-99fa-4e61cb197dc5"
- Screen: "5.3.1 FLU/Bank Card/Customer Confirmation" → Decision: "Transaction Succesful?"
- Decision: "Transaction Succesful?" → Screen: "5.4.2 FLU/Transaction Approved"
- Decision: "a533483e-975a-4db6-b31a-4479f181567e" → Decision: "Over £45, customer decides
Chip & PIN, or payment device
asks customer to insert their card?"
- Screen: "5.5.2 FLU/Bank Card/Customer Signature" → Screen: "5.4.1 FLU/Bank Card/Transaction Declined"
- Screen: "5.1.1 FLU/Bank Card/Initialising Transaction" → Screen: "5.2.1 FLU/Bank Card/Present"
- Screen: "5.3.2 FLU/Bank Card/User Confirming Amount" → Decision: "Correct PIN Entered?"
- Screen: "5.5.1 FLU/Bank Card/Transaction Declined 2" → Decision: "3fc532ce-c7d5-4ae5-b76e-cf42431a605f"
- Decision: "Payment type" → Decision: "55798a1f-ccdf-423c-9fce-b9c1e63296ab"
- Decision: "Transaction Succesful?" → Screen: "5.4.3 FLU/Transaction Approved-Confirmation"
- Screen: "5.3.2 FLU/Bank Card/User Confirming Amount" → Screen: "5.5.1 FLU/Bank Card/Transaction Declined 2"
- Decision: "Over £45, customer decides
Chip & PIN, or payment device
asks customer to insert their card?" → Screen: "5.3.1 FLU/Bank Card/Customer Confirmation"
- Screen: "5.4.1 FLU/Bank Card/Transaction Declined" → Decision: "8fd0b3e2-c768-4bcf-ac0b-f56e63176043"
- Decision: "Transaction Succesful?" → Screen: "5.4.1 FLU/Bank Card/Transaction Declined"
- Decision: "Payment type" → Decision: "ea99a1eb-7c18-4cf5-b77c-268731297da8"
- Decision: "Chip & PIN card available?" → Screen: "5.3.2 FLU/Bank Card/User Confirming Amount"
- Decision: "ea99a1eb-7c18-4cf5-b77c-268731297da8" → Screen: "5.3.2 FLU/Bank Card/User Confirming Amount"
- Decision: "Transaction Succesful?" → Screen: "5.4.1 FLU/Bank Card/Transaction Declined"
- Decision: "Amount too large?
(Test transactions only)" → Screen: "5.4.1 FLU/Bank Card/Transaction Declined"
- Decision: "55798a1f-ccdf-423c-9fce-b9c1e63296ab" → Decision: "Chip & PIN card available?"
- Screen: "5.2.1 FLU/Bank Card/Present" → Decision: "Amount too large?
(Test transactions only)"
- Screen: "5.4.2 FLU/Transaction Approved" → Decision: "edd9f3ff-36e9-4638-891d-4f421af42546"
- Screen: "5.3.1 FLU/Bank Card/Customer Confirmation" → Decision: "Transaction Succesful?"
- Decision: "Transaction Succesful?" → Screen: "5.4.1 FLU/Bank Card/Transaction Declined"
- Decision: "Payment type" → Decision: "a533483e-975a-4db6-b31a-4479f181567e"
- Decision: "Chip & PIN card available?" → Decision: "ea99a1eb-7c18-4cf5-b77c-268731297da8"
- Decision: "Amount too large?
(Test transactions only)" → Decision: "Payment type"
- Screen: "5.3.2 FLU/Bank Card/User Confirming Amount" → Screen: "5.3.1 FLU/Bank Card/Customer Confirmation"
- Screen: "5.5.1 FLU/Bank Card/Transaction Declined 2" → Decision: "048b82fc-021f-4c10-ad4a-a3a7a71e7a41"
- Screen: "5.4.1 FLU/Bank Card/Transaction Declined" → Decision: "71a331ad-969a-48b4-9c09-15cd7d34aac7"
- Decision: "edd9f3ff-36e9-4638-891d-4f421af42546" → Screen: "5.5.2 FLU/Bank Card/Customer Signature"
- Screen: "5.4.1 FLU/Bank Card/Transaction Declined" → Decision: "91898426-d672-4c5a-b847-618bf258bb11"
- Screen: "5.2.1 FLU/Bank Card/Present" → Screen: "4.2.3 Main Screen - FLU - Multiple Items - Payment"
- Screen: "5.4.1 FLU/Bank Card/Transaction Declined" → Screen: "4.2.3 Main Screen - FLU - Multiple Items - Payment"
- Screen: "5.4.1 FLU/Bank Card/Transaction Declined" → Decision: "9c2a019e-2f2a-41a8-8e28-e0a8a4a32cc7"
- Screen: "4.2.3 Main Screen - FLU - Multiple Items - Payment" → Screen: "5.1.1 FLU/Bank Card/Initialising Transaction"
- Screen: "5.4.3 FLU/Transaction Approved-Confirmation" → Decision: "When the Print Receipt button is pressed a payment card receipt will be printed and the POS will return to the FLU screen."
- Screen: "5.4.3 FLU/Transaction Approved-Confirmation" → Decision: "When the Print Receipt button is pressed a payment card receipt will be printed and the POS will return to the FLU screen."
- Screen: "5.4.3 FLU/Transaction Approved-Confirmation" → Decision: "c276d0ff-db88-451c-b6d1-5016c8433786"
- Screen: "5.2.1 FLU/Bank Card/Present" → Screen: "5.5.1 FLU/Bank Card/Transaction Declined 2" [Customer cancels
the transaction
using the Cancel button
on the Miura M020.]
- Screen: "5.5.1 FLU/Bank Card/Transaction Declined 2" → Decision: "9bb3e5bb-7ec5-4a33-a433-e8689a402cde"
- Screen: "5.5.1 FLU/Bank Card/Transaction Declined 2" → Screen: "4.2.3 Main Screen - FLU - Multiple Items - Payment"
- Screen: "5.4.1 FLU/Bank Card/Transaction Declined" → Decision: "A declined card payment receipt will be printed when this screen is displayed."
- Screen: "5.4.1 FLU/Bank Card/Transaction Declined" → Decision: "A declined card payment receipt will be printed when this screen is displayed."
- Screen: "5.4.1 FLU/Bank Card/Transaction Declined" → Decision: "A declined card payment receipt will be printed when this screen is displayed."
- Screen: "5.4.1 FLU/Bank Card/Transaction Declined" → Decision: "A declined card payment receipt will be printed when this screen is displayed."
- Screen: "5.5.2 FLU/Bank Card/Customer Signature" → Screen: "5.4.3 FLU/Transaction Approved-Confirmation"
- Screen: "5.4.3 FLU/Transaction Approved-Confirmation" → Decision: "cf709527-de22-47a2-b660-6b509eeffa3b"
- Decision: "Correct PIN Entered?" → Screen: "5.3.1 FLU/Bank Card/Customer Confirmation"
- Decision: "Correct PIN Entered?" → Screen: "5.4.1 FLU/Bank Card/Transaction Declined"
- Decision: "Over £45, customer decides
Chip & PIN, or payment device
asks customer to insert their card?" → Screen: "5.2.1.1 FLU/Bank Card/Present Card PIN"
- Screen: "5.2.1.1 FLU/Bank Card/Present Card PIN" → Decision: "ea99a1eb-7c18-4cf5-b77c-268731297da8"


## 7. 6.0 Numerical Input

### Screens (15)
- 2.5.2 Main Screen-Ulsterbus selected
- 6.1.1. Numeric Entry 9 Calculate Change and Group ticket 
- 6.1.2 Numeric Entry 90 All Numeric Functions Available 
- 6.1.3 Numeric Entry - 9002 - Change Boarding and Alighting 
- 6.2.1 FLU/Cash/Change
- 6.2.3 Basket- Group Ticket
- 2.6.2 Main Screen - FLU - Alighting Selected
- 6.2.2 Payment - Group Ticket
- 6.3.2 Numeric Entry 9 No Alighting Stage
- 6.3.1 Numeric Entry - 9017 - Change & Alighting - Unable to calculate change
- 6.3.3 Numeric Entry 9 No Group Ticket
- 6.3.4 Numeric Entry 9 Group Ticket Unavailable
- 3.0 Main Screen-Rail-v4
- 3.0 Main Screen-Rail-numerical input
- 3.0 Main Screen-Rail-invalid station no

### Decision Points (11)
- Is number entered valid as an alighting stage?
- Is the selected product  available as a group ticket or is POS able to set group ticket with the amount entered?
- POS is able to calculate change?
- Advance Ticket Flow
- If operator chooses to change the boarding stage and the number entered doesn't match any of the stages available, the following error will be displayed: "Unable to Set Boarding Stage"
- Operator will be able to use numerical keys to set boarding station by entering 1, 2 or 3 digits followed by L1 key will change the boarding station (e.g if 2 is entered it will be interpreted as 02 by the machine). For setting alighting station, operator will enter the 1, 2 or 3 digits corresponding the desired station followed by L2 key (e.g if 2 is entered it will be interpreted as 02 by the machine). The number entered will be shown in the bottom bar of the POS screen.
- The timeout before pressing L1 or L2 key should be 3 seconds. Also the operator has to wait for 3 seconds to input another number if mistaken.  If more than 3 digits are entered for selecting a station then any extra digits will be ignored.
- Once the boarding or alighting station is set, the number entered will disappear and operator will be able to enter another one.
- Set boarding / alighting station.
- Is the Station Number Valid?
- If station number entered is invalid, it will be stated in the bottom bar with a timeout of 3 seconds.

### Annotations / Spec Notes (24)
- Numerical Input Bus
- User enters a number at any given time in the main Bus FLU screen.
- According to amount entered, User will not be able to access some of the functionality. For example, group ticket has a limit of 100 tickets.
- User may set boarding stage using Unique Farestage ID. This will automatically return to Main FLU screen with boarding stage changed.
- There will be a setting within Cloudfare which allows Translink to configure which ticket types will be allowed to be issued as a Group Tickets and which will not.
- User may set alighting stage using ID number. This will automatically return to Main FLU screen with the entered ID station selected.
- User is able to issue a group ticket with the selected boarding and alighting stages multiplied with the number entered.
- User is able to calculate change.
- Timeout will not occur, 'Back or Main' keys must be pressed.
- Yes
- Yes
- The machine will print a single group ticket receipt.  Upon ticket issue a single transaction record will be sent to the back office that includes sub-elements for each passenger that is part of the group ticket
- No
- No
- Operator will be able to set an advance date ticket following the specific flow.
- Yes
- User will receive an error notification if change couldn't be calculated.  The Calculate Change option will not be available if: 1. entering too many digits 2. the amount entered is less than the ticket value 3. previous transaction had no value
- If the number entered doesn't match any of the stages available, an error will be displayed.
- No
- The POS will display an error banner if the amount entered cannot be used for a group ticket.
- The POS will display an error banner if the product selected is not available as a group ticket.
- Numerical Input Rail
- YES
- NO

### Connections / Flow (25)
- Screen: "6.1.2 Numeric Entry 90 All Numeric Functions Available " → Screen: "6.1.3 Numeric Entry - 9002 - Change Boarding and Alighting "
- Screen: "6.1.2 Numeric Entry 90 All Numeric Functions Available " → Decision: "POS is able to
calculate change?"
- Screen: "6.1.1. Numeric Entry 9 Calculate Change and Group ticket " → Decision: "Is the
selected product 
available as a group ticket
or is POS able to
set group ticket
with the amount
entered?"
- Screen: "6.1.1. Numeric Entry 9 Calculate Change and Group ticket " → Screen: "2.5.2 Main Screen-Ulsterbus selected"
- Decision: "POS is able to
calculate change?" → Screen: "6.3.1 Numeric Entry - 9017 - Change & Alighting - Unable to calculate change"
- Screen: "6.1.3 Numeric Entry - 9002 - Change Boarding and Alighting " → Decision: "c21fc315-f98c-4709-a1a2-9528afd36f86"
- Screen: "6.1.3 Numeric Entry - 9002 - Change Boarding and Alighting " → Decision: "Is number entered valid
as an alighting stage?"
- Decision: "POS is able to
calculate change?" → Screen: "6.2.1 FLU/Cash/Change"
- Screen: "2.5.2 Main Screen-Ulsterbus selected" → Screen: "6.1.1. Numeric Entry 9 Calculate Change and Group ticket "
- Screen: "6.1.1. Numeric Entry 9 Calculate Change and Group ticket " → Screen: "6.1.2 Numeric Entry 90 All Numeric Functions Available "
- Screen: "3.0 Main Screen-Rail-v4" → Screen: "3.0 Main Screen-Rail-numerical input"
- Screen: "3.0 Main Screen-Rail-numerical input" → Decision: "Is the Station
Number Valid?"
- Decision: "Is the Station
Number Valid?" → Decision: "Set boarding / alighting station."
- Decision: "Is the Station
Number Valid?" → Screen: "3.0 Main Screen-Rail-invalid station no"
- Screen: "6.2.3 Basket- Group Ticket" → Screen: "6.2.2 Payment - Group Ticket"
- Screen: "6.2.3 Basket- Group Ticket" → Decision: "Advance Ticket
Flow"
- Screen: "6.2.3 Basket- Group Ticket" → Screen: "6.2.2 Payment - Group Ticket"
- Screen: "6.2.3 Basket- Group Ticket" → Screen: "6.1.1. Numeric Entry 9 Calculate Change and Group ticket "
- Screen: "6.2.1 FLU/Cash/Change" → Screen: "6.1.3 Numeric Entry - 9002 - Change Boarding and Alighting "
- Screen: "6.2.1 FLU/Cash/Change" → Screen: "2.5.2 Main Screen-Ulsterbus selected"
- Decision: "Is number entered valid
as an alighting stage?" → Screen: "2.6.2 Main Screen - FLU - Alighting Selected"
- Decision: "Is number entered valid
as an alighting stage?" → Screen: "6.3.2 Numeric Entry 9 No Alighting Stage"
- Decision: "Is the
selected product 
available as a group ticket
or is POS able to
set group ticket
with the amount
entered?" → Screen: "6.2.3 Basket- Group Ticket"
- Decision: "Is the
selected product 
available as a group ticket
or is POS able to
set group ticket
with the amount
entered?" → Screen: "6.3.3 Numeric Entry 9 No Group Ticket"
- Decision: "Is the
selected product 
available as a group ticket
or is POS able to
set group ticket
with the amount
entered?" → Screen: "6.3.4 Numeric Entry 9 Group Ticket Unavailable"


## 8. 7.0 Top Up & Validation

### Screens (119)
- 2.2 Main Screen-Rail selected
- 2.5.2 Main Screen-Ulsterbus selected
- 3.0 Main Screen-Rail-v4
- 7.1.1 Smartcard/Please Present Smartcard
- 7.2.1 Smartcard/Menu
- 2.2 Main Screen-Rail selected
- 7.3.2 Smartcard/Ulsterbus Multi Journey/Mini Statement
- 7.3.3 Smartcard/Town Service Travelcard/Mini Statement
- 7.4.3 Ulsterbus Smartcard/Top Up
- 7.5.1 Smartcard/Error
- 7.5.7 Ulsterbus Smartcard/Top Up/Basket
- 7.7.1 Top Up/Top Up Error Not Used
- 7.5.3 Smartcard/Top Up/Remove Smartcard
- 7.6.2 Smartcard/Top Up-Ulsterbus Travelcard-Expired
- 7.5.6 Smartcard/Top Up/Ulsterbus Travelcard/Basket
- 7.6.1 Top Up/Top Up Error
- 7.5.3 Smartcard/Top Up/Remove Smartcard/Expiry
- 7.4.4 Smartcard/Top Up-Ulsterbus Travelcard
- 7.6.1 Top Up/Top Up Error
- 7.1.2 Metro Smartcard/Please Present Smartcard
- 7.2.1 Smartcard/Menu
- 7.3.4 Smartcard/Metro Multi Journey/Mini Statement
- 7.3.5 Smartcard/Metro Travelcard/Mini Statement
- 7.3.1 Smartcard/Top Up
- 2.2 Main Screen-Rail selected
- 7.4.2 Smartcard/Top Up/Basket
- 7.5.1 Smartcard/Error
- 7.7.1 Top Up/Top Up Error Not Used
- 7.5.3 Smartcard/Top Up/Remove Smartcard
- 7.6.3 Smartcard/Top Up-Metro Travelcard-Expired
- 7.6.1 Top Up/Top Up Error
- 7.5.8 Smartcard/Top UpMetro Travelcard/Basket
- 7.5.3 Smartcard/Top Up/Remove Smartcard/Expiry
- 7.4.5 Smartcard/Top Up-Metro Travelcard
- 7.6.1 Top Up/Top Up Error
- 2.2 Main Screen-Rail selected
- 2.5.2 Main Screen-Ulsterbus selected
- 3.0 Main Screen-Rail-v4
- 7.2.2.1 Smartcard/Menu-ABT/NegativeList
- 7.1.1 Smartcard/Please Present Smartcard
- 7.2.2 Smartcard/Menu-ABT
- 7.4.6.1 ABT Smartcard/Top Up/NegativeList
- 7.4.6 ABT Smartcard/Top Up
- 7.3.6 Smartcard/ABT/Mini Statement
- 7.5.8 Smartcard/Top Up/ABT/Basket/Expired
- 7.5.1 Smartcard/Error
- 7.5.3 Smartcard/Top Up/Remove Smartcard/Value
- 7.6.1 Top Up/Top Up Error
- 2.2 Main Screen-Rail selected
- 2.5.2 Main Screen-Ulsterbus selected
- 3.0 Main Screen-Rail-v4
- 7.1.1 Smartcard/Please Present Smartcard
- 7.2.1 Smartcard/Menu
- 7.3.7 Smartcard/DayLink/Mini Statement
- 7.4.7 Smartcard/Top Up-Daylink
- 7.5.1 Smartcard/Error
- 7.5.9 Smartcard/Top Up/Daylink/Payment
- 7.5.3 Smartcard/Top Up/Remove Smartcard/Daylink
- 7.6.1 Top Up/Top Up Error
- 2.2 Main Screen-Rail selected
- 2.5.2 Main Screen-Ulsterbus selected
- 3.0 Main Screen-Rail-v4
- 7.1.1 Smartcard/Please Present Smartcard
- 7.2.1 Smartcard/Menu
- 2.2 Main Screen-Rail selected
- 7.3.8 Smartcard/Belfast Visitor Pass/Mini Statement
- 7.7.1 Top Up/Top Up Error Not Used
- 7.5.1 Smartcard/Error
- 7.4.9 Smartcard/Top Up-Belfast Visitor/Expired
- 7.5.10 Smartcard/Top Up/Belfast Visitor/Payment
- 7.5.3 Smartcard/Top Up/Remove Smartcard/Expiry
- 7.4.8 Smartcard/Top Up-Belfast Visitor
- 7.6.1 Top Up/Top Up Error
- 2.2 Main Screen-Rail selected
- 2.5.2 Main Screen-Ulsterbus selected
- 3.0 Main Screen-Rail-v4
- 7.1.1 Smartcard/Please Present Smartcard
- 7.2.1 Smartcard/Menu
- 2.2 Main Screen-Rail selected
- 7.3.9 Smartcard/iLink/Mini Statement
- 7.7.1 Top Up/Top Up Error Not Used
- 7.5.1 Smartcard/Error
- 7.4.11 Smartcard/Top Up/iLink/Expired
- 7.5.11 Smartcard/Top Up/iLink/Payment
- 7.4.10 Smartcard/Top Up/iLink
- 7.5.3 Smartcard/Top Up/Remove Smartcard/Expiry
- 7.6.1 Top Up/Top Up Error
- 7.9.3 Main Screen-Rail-Senior Single
- 7.9.1 Bus Main Screen-Senior Single
- 7.9.2 Bus Main Screen-Senior Single-Alighting Selected
- 7.11.1 Smartcard - Faulty - Select Card Type
- 7.11.2 Smartcard - Faulty - Charge Full Fare
- 7.11.3 Smartcard - Faulty - Issue Ticket
- 7.9.4 Main Screen-Rail-Senior Single Cross Border
- 7.11.4 Smartcard - Faulty - Outside Time Band
- 7.11.5 FLU - Smartcard Already Validated
- 7.11.6 Hotlisted Error
- 7.10.1 Main Screen-Validation-Confirmation-000
- 7.10.2 Rail-Validation-Confirmation-000
- 7.9.5 Bus Main Screen-DLA Single
- 7.9.6 Bus Main Screen-DLA Single-Alighting Selected
- 7.9.7 Main Screen-Rail-DLA Single
- 7.9.8 Smartcard/Validation/DLA Single/Payment
- 7.10.3 Main Screen-Validation-Confirmation
- 7.10.4 Rail-Validation-Confirmation
- 7.9.9 Bus Main Screen-yLink Single
- 7.9.10 Bus Main Screen-yLink Single-Alighting Selected
- 7.9.11 Main Screen-Rail-yLink Single
- 7.9.12 Smartcard/Validation/yLink Single/Payment
- 7.10.3 Main Screen-Validation-Confirmation
- 7.10.4 Rail-Validation-Confirmation
- 7.9.13 Main Screen-Rail-24+
- 7.9.14 Smartcard/Validation/24+/Payment
- 7.10.4 Rail-Validation-Confirmation
- 7.9.15 Bus Main Screen-Dependants Pass
- 7.9.16 Bus Main Screen-yLink Single-Dependants Pass
- 7.9.17 Main Screen-Rail-Dependants Pass
- 7.10.1 Main Screen-Validation-Confirmation-000
- 7.10.2 Rail-Validation-Confirmation-000

### Decision Points (86)
- Is the Smartcard valid?
- Adult
- Child
- Multi journey
- Town Service Travelcard
- If the user presses any button or removes the card, they'll be taken back to the main screen (rail or bus, depending on which login has been used).
- After printing process, user will automatically return to Top up menu.
- Is the product "FirstUse"?
- If the product is expired and a period of travel is loaded onto it then this screen will show "New Expiry date: From First Use".  If the product is not expired and a period of travel is loaded onto it then this screen will show the expiry date as per your example below.
- Is the product expired?
- Card Write Success?
- Card Write Success?
- Is the Smartcard valid?
- Adult
- Child
- Metro Multi-Journey
- Metro Travelcard
- If the user presses any button or removes the card, they'll be taken back to the main screen (rail or bus, depending on which login has been used).
- After printing process, user will automatically return to Top up menu.
- Is the product "FirstUse"?
- Card Write Success?
- - If the card is expired and a period of travel is loaded onto it then this screen will show "New Expiry date: From First Use" - If the card is not expired and a period of travel is loaded onto it then this screen will show the expiry date as per your example below
- Is the product expired?
- Card Write Success?
- Is the Smartcard valid?
- Adult
- Child
- Pressing the 'Recover Unique Code' button will print a receipt with the Smartcard code on.
- Card Issue flow
- After printing process, user will automatically return to Top up menu.
- Return to beginning of the flow
- Card Write Success?
- Is the Smartcard valid?
- Adult
- Child
- After printing process, user will automatically return to Top up menu.
- Return to the beginning of the flow
- Card Write Success?
- Is the Smartcard valid?
- Adult
- Child
- If the user presses any button or removes the card, they'll be taken back to the main screen (rail or bus, depending on which login has been used).
- Is the product "FirstUse"?
- After printing process, user will automatically return to Top up menu.
- Is the product expired?
- If the card is expired and a period of travel is loaded onto it then this screen will show "New Expiry Date: From First Use". If the card is not expired and a period of travel is loaded onto it then this screen will show the expiry date.
- Return to the beginning of the flow
- Card Write Success?
- Is the Smartcard valid?
- Adult
- Child
- If the user presses any button or removes the card, they'll be taken back to the main screen (rail or bus, depending on which login has been used).
- Is the product "FirstUse"?
- After printing process, user will automatically return to Top up menu.
- If the card is expired and a period of travel is loaded onto it then this screen will show "New Expiry date: From First Use".  If the card is not expired and a period of travel is loaded onto it then this screen will show the expiry date as per your example below.
- Is the product expired?
- Return to the beginning of the flow
- Card Write Success?
- Free Smartpasses
- Customer presents card.
- Senior Smartpass
- 60+ Smartpass
- RoI Senior Smartpass
- Blind Smartpass
- War Pensioner Smartpass
- Faulty Smartcard presented
- Smartcard presented outside of a relevant Time Band.
- Passback of Smartcard/Smartpass
- Hotlisted/Expired Card
- 7 Day Faulty Ticket is printed
- Ticket is printed.
- If operator sets a cross border journey ticket type will change to Senior XB Single and will be available to change to: Senior XB Day Return Senior XB 1 Mth Return using R4 key and then choose from the list or using L4 toggle key.
- Half-Fare Smartpass
- Disability Living  Allowance
- Learning Disability
- Partially Sighted
- PIPS
- No Driving Licence
- Although the ticket types are displayed as Half Fare on the screens and half fare is printed in the tickets it is important to note that they will be audited as the sub-types of DLA, No Driving Licence, Partially Sighted, PIPs, Learning Disability.
- After Payment flow is completed the selected ticket is printed.
- yLink
- After Payment flow is completed the selected ticket is printed.
- 24+
- After Payment flow is completed the selected ticket is printed.
- Dependants Pass
- The selected ticket is printed.

### Annotations / Spec Notes (205)
- Top Up
- In regards to Mini Statements, if the card does not have a card reference number then "N/A" will be displayed.
- Ulsterbus Top Up Flow
- All Ulsterbus cards can be topped up on any POS (i.e. Metro, Ulsterbus or Rail POS)
- User may choose 'Smartcard' at any given time on the Main Screen and both Bus or Rail FLU screens.
- User will be prompted to present Smartcard.
- Yes
- User selects Smartcard from Main Menu.
- If the Smartcard card is valid and not blank, user is presented the Smartcard menu.
- When Mini Statement is selected, the POS will display data for the smarcard previously presented.
- No
- All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- User is able to choose a product pressing the corresponding buttons. If choosing a product will overcome the maximum amount allowed for that card, then that menu option will not be displayed.
- If a Multi-Journey card is expired and journeys are added to it then all existing journeys are removed following the successful top-up (and a journey removal receipt is printed).
- This is a catch all error screen for issues with the smartcard. For example, this could be a card that is not specific for Translink (anything not in a recognised format) . Timeout of 3 seconds or press any key will go back to Main Menu.
- Pressing 'C' button will reset value and journeys number.
- Card payment flow
- Yes
- A Top Up Successful screen is presented and user has to remove Smartcard to continue.
- No
- *Enter button has no function on this screen*
- *Only the cash option is available to Metro users*
- If the product is expired it will be stated in the screen.
- Yes
- Yes
- No
- When this screen is shown:  1) the Cash or Warrant payment is not recorded in the POS audit data (and a diagnostic/event is recorded to audit this error occured)  2) Any payment card transaction is automatically voided by the POS (and a diagnostic/event is recorded to audit this error occured)
- No
- A Top Up Successful screen is presented and user has to remove Smartcard to continue.
- User is able to choose a product pressing the corresponding buttons.  The expiry for the product is also shown.
- *Enter button has no function on this screen*
- *Only the cash option is available to Metro users*
- Card payment flow
- Yes
- Timeout of 3 seconds or press any key will go back to the previous screen.
- When this screen is shown:  1) the Cash or Warrant payment is not recorded in the POS audit data (and a diagnostic/event is recorded to audit this error occured)  2) Any payment card transaction is automatically voided by the POS (and a diagnostic/event is recorded to audit this error occured)
- No
- Timeout of 3 seconds or pressing any key will go back to the previous screen.
- Metro Top Up Flow
- All Metro cards can be topped up on any POS (i.e. Metro, Ulsterbus or Rail POS)
- User will be prompted to present Smartcard. This is the first screen Metro operator will be presented after sign on process.
- Yes
- If the Smartcard card is valid and not blank, user is presented the Smartcard menu.
- When Mini Statement is selected, the POS will display data for the smarcard previously presented.
- No
- All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- User is able to choose a product pressing the corresponding buttons. If choosing a product will overcome the maximum amount allowed for that card, then that menu option will not be displayed.
- After printing process, user will automatically return to Top up menu.
- This is a catch all error screen for issues with the smartcard. For example, this could be a card that is not specific for Translink (anything not in a recognised format). Timeout of 3 seconds or pressing any key will go back to previous screen.
- Pressing 'C' button will reset value and journeys number.
- A Top Up Successful screen is presented and user has to remove Smartcard to continue.
- If a Multi-Journey card is expired and journeys are added to it then all existing journeys are removed following the successful top-up (and a journey removal receipt is printed).
- Yes
- No
- *Enter button has no function on this screen*
- Warrant and card is available for NIR and Ulsterbus
- If the card expired it will be stated in the screen.  The user is able to choose a product pressing the corresponding buttons.
- Yes
- When this screen is shown:  1) the Cash or Warrant payment is not recorded in the POS audit data (and a diagnostic/event is recorded to audit this error occured)  2) Any payment card transaction is automatically voided by the POS (and a diagnostic/event is recorded to audit this error occured)
- No
- Yes
- No
- A Top Up Successful screen is presented and user has to remove Smartcard to continue.
- *Enter button has no function on this screen*
- Timeout of 3 seconds or pressing any key will go back to the previous screen.
- *Only the cash option is available to Metro users*
- Card payment flow
- Return to beginning of the flow
- Yes
- ABT Top Up Flow
- When this screen is shown:  1) the Cash or Warrant payment is not recorded in the POS audit data (and a diagnostic/event is recorded to audit this error occured)  2) Any payment card transaction is automatically voided by the POS (and a diagnostic/event is recorded to audit this error occured)
- All ABT cards (Adult or Child) can be topped up on any POS (i.e. Metro, Ulsterbus or Rail POS). The text 'ABT' on screens will be replaced by the ABT brand name
- No
- User will be prompted to present Smartcard.
- Example of ABT card in negative list (variant of screen 7.2.2 Smartcard/Menu-ABT)
- Timeout of 3 seconds or pressing any key will go back to the previous screen.
- Yes
- User selects Smartcard from Main Menu.
- If the Smartcard card is valid and not blank, user is presented the Smartcard menu.
- No
- All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- After printing process, user will automatically return to Top up menu.
- Example of ABT card in negative list (variant of screen 7.4.6 ABT Smartcard/Top Up)
- This is a catch all error screen for issues with the smartcard. For example, this could be a card that is not specific for Translink (anything not in a recognised format) . Timeout of 3 seconds or press any key will go back to Main Menu.
- A Top Up Successful screen is presented and user has to remove Smartcard to continue.
- Card payment flow
- *Enter button has no function on this screen*
- *Only the cash option is available to Metro users*
- Yes
- When this screen is shown:  1) the Cash or Warrant payment is not recorded in the POS audit data (and a diagnostic/event is recorded to audit this error occured)  2) Any payment card transaction is automatically voided by the POS (and a diagnostic/event is recorded to audit this error occured)
- No
- Timeout of 3 seconds or pressing any key will go back to the previous screen.
- DayLink Top Up Flow
- All DayLink cards can be topped up on any POS (i.e. Metro, Ulsterbus or Rail POS)
- User may choose 'Smartcard' at any given time on the Main Screen and both Bus or Rail FLU screens.
- User will be prompted to present Smartcard.
- Yes
- User selects Smartcard from Main Menu.
- If the Smartcard card is valid and not blank, user is presented the Smartcard menu.
- No
- All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- After printing process, user will automatically return to Top up menu.
- User is able to choose a product pressing the corresponding buttons.
- This is a catch all error screen for issues with the smartcard. For example, this could be a card that is not specific for Translink (anything not in a recognised format) . Timeout of 3 seconds or press any key will go back to Main Menu.
- A Top Up Successful screen is presented and user has to remove Smartcard to continue.
- *Enter button has no function on this screen*
- *Only the cash option is available to Metro users*
- Card payment flow
- Yes
- When this screen is shown:  1) the Cash or Warrant payment is not recorded in the POS audit data (and a diagnostic/event is recorded to audit this error occured)  2) Any payment card transaction is automatically voided by the POS (and a diagnostic/event is recorded to audit this error occured)
- No
- Timeout of 3 seconds or pressing any key will go back to the previous screen.
- Belfast Visitor Pass Top Up Flow
- All Belfast Visitor cards can be topped up on any POS (i.e. Metro, Ulsterbus or Rail POS)
- User may choose 'Smartcard' at any given time on the Main Screen and both Bus or Rail FLU screens.
- User will be prompted to present Smartcard.
- Yes
- User selects Smartcard from Main Menu.
- If the Smartcard card is valid and not blank, user is presented the Smartcard menu.
- No
- All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- After printing process, user will automatically return to Top up menu.
- This is a catch all error screen for issues with the smartcard. For example, this could be a card that is not specific for Translink (anything not in a recognised format) . Timeout of 3 seconds or press any key will go back to Main Menu.
- Yes
- No
- Yes
- No
- A Top Up Successful screen is presented and user has to remove Smartcard to continue.
- User is able to choose a product pressing the corresponding buttons.
- *Enter button has no function on this screen*
- *Only the cash option is available to Metro users*
- Card payment flow
- Yes
- When this screen is shown:  1) the Cash or Warrant payment is not recorded in the POS audit data (and a diagnostic/event is recorded to audit this error occured)  2) Any payment card transaction is automatically voided by the POS (and a diagnostic/event is recorded to audit this error occured)
- No
- iLink Top Up Flow
- All iLink cards can be topped up on any POS (i.e. Metro, Ulsterbus or Rail POS)
- Timeout of 3 seconds or pressing any key will go back to the previous screen.
- User may choose 'Smartcard' at any given time on the Main Screen and both Bus or Rail FLU screens.
- User will be prompted to present Smartcard.
- Yes
- User selects Smartcard from Main Menu.
- If the Smartcard card is valid and not blank, user is presented the Smartcard menu.
- No
- All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- After printing process, user will automatically return to Top up menu.
- This is a catch all error screen for issues with the smartcard. For example, this could be a card that is not specific for Translink (anything not in a recognised format) . Timeout of 3 seconds or press any key will go back to Main Menu.
- Yes
- No
- If the card expired it will be stated in the screen.
- Yes
- No
- A Top Up Successful screen is presented and user has to remove Smartcard to continue.
- User is able to choose a product pressing the corresponding buttons.
- *Enter button has no function on this screen*
- *Only the cash option is available to Metro users*
- Card payment flow
- Yes
- When this screen is shown:  1) the Cash or Warrant payment is not recorded in the POS audit data (and a diagnostic/event is recorded to audit this error occured)  2) Any payment card transaction is automatically voided by the POS (and a diagnostic/event is recorded to audit this error occured)
- No
- Timeout of 3 seconds or pressing any key will go back to the previous screen.
- Discount/Entitlement Smartcards Validation
- Faulty Cards Flow
- There are no validations for Metro POS
- All XB ticket types are only available on Rail POS.
- The operator will still be able to change boarding or alighting station at this point without removing the ticket type initiated by presenting the free Smartpass.
- After operator chooses alighting stage the ticket is printed automatically. No aditional action is needed.
- Operator may choose to go back to previous screen or press Continue key to go to Main Screen or FLU screen (where initially started).
- Operator may choose to go back to previous screen or press Issue Receipt key to print receipt and go to Main Screen or FLU screen (where initially started).
- Similar to the Senior Smartpass. Ticket type will be displayed accordingly: Blind Single. Cross Border tickets will be display as: Blind XB Single Blind XB Day Return Blind XB 1 Mth Return and will be available to change using L4 toggle or R4 menu keys.
- Similar to the Senior Smartpass. Ticket type will be displayed accordingly: 60+ Single.
- Similar to the Senior Smartpass. Ticket type will be displayed accordingly: War Pensioner Single. Cross Border tickets will be display as: War Pensioner XB Single War Pensioner XB Day Return War Pensioner XB 1 Mth Return and will be available to change using L4 toggle or R4 menu keys.
- Similar to the Senior Smartpass. Ticket type will be displayed accordingly: RoI Senior Single. Cross Border tickets will be display as: RoI Senior XB Single RoI Senior XB Day Return RoI Senior XB 1 Mth Return and will be available to change using L4 toggle or R4 menu keys.
- This ticket type will not be accepted for Rail Cross Border travel. Cross Border stations will not be displayed/available for numerical input.
- Customer will be unable to validate the card again if the last validation was made in less then X minutes prior to the second attempt (this time should be configured to TL demand).  This error will have a timeout of 3 seconds and will send operator to Main Screen or FLU screen (where initially started).
- If the card presented is Hotlisted POS will show this error. If expired, it will state Expired Smartcard. This error will have a timeout of 3 seconds and will send operator to Main Screen or FLU screen (where initially started).
- Customer will be unable to use the Smartcard if presented outside of a relevant time band. This error will have a timeout of 3 seconds and will send operator to Main Screen or FLU screen (where initially started).
- For rail operator has to confirm pressing Enter for the ticket to be issued.
- This ticket type will not be accepted for Rail Cross Border travel. Cross Border stations will not be displayed/available for numerical input.
- Rail operator can choose between Half Fare Single and Half Fare Return using L4 toggle key or R4 key and select from the list.
- Operator chooses alighting stage
- Similar to the Senior Smartpass.
- Similar to the Senior Smartpass.
- Similar to the Senior Smartpass.
- Similar to the Senior Smartpass.
- This ticket types will not be accepted for Rail Cross Border travel. Cross Border stations will not be displayed/available for numerical input.
- This ticket types will not be accepted for Rail Cross Border travel. Cross Border stations will not be displayed/available for numerical input.
- This ticket types will not be accepted for Rail Cross Border travel. Cross Border stations will not be displayed/available for numerical input.
- This ticket types will not be accepted for Rail Cross Border travel. Cross Border stations will not be displayed/available for numerical input.
- For both rail and bus operator has to confirm pressing Enter to go to payment screen.
- The operator should still be able to change boarding or alighting station at this point without removing the ticket type initiated by presenting the Half Fare Smartpass
- Rail operator can choose between yLink Single, yLink Return, yLink Weekly and yLink Monthly using L4 toggle key or R4 key and select from the list.
- This ticket type will not be accepted for Rail Cross Border travel. Cross Border stations will not be displayed/available for numerical input.
- Operator chooses alighting stage
- For both rail and bus operator has to confirm pressing Enter to go to payment screen.
- The operator should still be able to change boarding or alighting station at this point without removing the ticket type initiated by presenting the yLink Smartpass.
- This card type will only be accepted for rail.
- Rail operator can choose between 24+ Single, 24+ Return, 24+ Weekly, and 24+ Monthly using L4 toggle key or R4 key and select from the list.
- This ticket type will not be accepted for Rail Cross Border travel. Cross Border stations will not be displayed/available for numerical input.
- Operator has to confirm pressing Enter to go to payment screen.
- The operator should still be able to change boarding or alighting station at this point without removing the ticket type initiated by presenting the 24+ Smartpass.
- After operator chooses alighting stage the ticket is printed automatically. No aditional action is needed.
- This ticket type will not be accepted for Rail Cross Border travel. Cross Border stations will not be displayed/available for numerical input.
- For Rail, operator has to confirm pressing enter for the ticket to be issued.
- The operator should still be able to change boarding or alighting station at this point without removing the ticket type initiated by presenting the Dependants Smartpass.

### Connections / Flow (237)
- Decision: "Is the Smartcard valid?" → Screen: "7.5.1 Smartcard/Error"
- Decision: "6fc5065d-13a8-4488-b5de-83660a91295a" → Decision: "Card Write Success?"
- Decision: "Card Write Success?" → Screen: "7.5.3 Smartcard/Top Up/Remove Smartcard" [Top up receipt is printed]
- Screen: "7.1.1 Smartcard/Please Present Smartcard" → Decision: "Is the Smartcard valid?"
- Screen: "2.5.2 Main Screen-Ulsterbus selected" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Screen: "3.0 Main Screen-Rail-v4" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Screen: "7.2.1 Smartcard/Menu" → Screen: "7.3.2 Smartcard/Ulsterbus Multi Journey/Mini Statement"
- Screen: "7.5.7 Ulsterbus Smartcard/Top Up/Basket" → Decision: "Card Write Success?"
- Screen: "2.2 Main Screen-Rail selected" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Decision: "Card Write Success?" → Screen: "7.6.1 Top Up/Top Up Error"
- Screen: "7.5.7 Ulsterbus Smartcard/Top Up/Basket" → Decision: "6fc5065d-13a8-4488-b5de-83660a91295a"
- Screen: "7.4.3 Ulsterbus Smartcard/Top Up" → Screen: "7.5.7 Ulsterbus Smartcard/Top Up/Basket"
- Decision: "Is the Smartcard valid?" → Screen: "7.2.1 Smartcard/Menu"
- Screen: "7.2.1 Smartcard/Menu" → Decision: "Adult"
- Screen: "7.2.1 Smartcard/Menu" → Decision: "Child"
- Decision: "Adult" → Decision: "Multi journey"
- Decision: "Multi journey" → Screen: "7.4.3 Ulsterbus Smartcard/Top Up"
- Decision: "Is the Smartcard valid?" → Screen: "7.5.1 Smartcard/Error"
- Screen: "7.1.2 Metro Smartcard/Please Present Smartcard" → Decision: "Is the Smartcard valid?"
- Screen: "7.2.1 Smartcard/Menu" → Screen: "7.3.4 Smartcard/Metro Multi Journey/Mini Statement"
- Screen: "7.3.1 Smartcard/Top Up" → Screen: "7.4.2 Smartcard/Top Up/Basket"
- Decision: "Is the Smartcard valid?" → Screen: "7.2.1 Smartcard/Menu"
- Screen: "7.2.1 Smartcard/Menu" → Decision: "Child"
- Decision: "Adult" → Decision: "Metro
Multi-Journey"
- Decision: "Metro
Multi-Journey" → Screen: "7.3.1 Smartcard/Top Up"
- Screen: "7.5.7 Ulsterbus Smartcard/Top Up/Basket" → Decision: "Card Write Success?"
- Decision: "Adult" → Decision: "Town Service Travelcard"
- Screen: "7.5.3 Smartcard/Top Up/Remove Smartcard" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Decision: "Adult" → Decision: "Metro Travelcard"
- Screen: "7.4.5 Smartcard/Top Up-Metro Travelcard" → Screen: "7.5.8 Smartcard/Top UpMetro Travelcard/Basket"
- Screen: "7.6.3 Smartcard/Top Up-Metro Travelcard-Expired" → Screen: "7.5.8 Smartcard/Top UpMetro Travelcard/Basket"
- Decision: "aa826a0a-901f-4160-a083-d5fc90e24d91" → Decision: "Card Write Success?"
- Decision: "Card Write Success?" → Screen: "7.5.3 Smartcard/Top Up/Remove Smartcard/Expiry" [Top up receipt is printed]
- Decision: "Card Write Success?" → Screen: "7.6.1 Top Up/Top Up Error"
- Screen: "7.5.8 Smartcard/Top UpMetro Travelcard/Basket" → Decision: "Card Write Success?"
- Screen: "7.5.8 Smartcard/Top UpMetro Travelcard/Basket" → Decision: "Card Write Success?"
- Screen: "7.5.8 Smartcard/Top UpMetro Travelcard/Basket" → Decision: "aa826a0a-901f-4160-a083-d5fc90e24d91"
- Screen: "7.5.8 Smartcard/Top UpMetro Travelcard/Basket" → Decision: "- If the card is expired and a period of travel is loaded onto it then this screen will show "New Expiry date: From First Use"
- If the card is not expired and a period of travel is loaded onto it then this screen will show the expiry date as per your example below"
- Screen: "7.6.1 Top Up/Top Up Error" → Screen: "7.5.8 Smartcard/Top UpMetro Travelcard/Basket"
- Decision: "Is the Smartcard valid?" → Screen: "7.5.1 Smartcard/Error"
- Screen: "7.1.1 Smartcard/Please Present Smartcard" → Decision: "Is the Smartcard valid?"
- Screen: "2.5.2 Main Screen-Ulsterbus selected" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Screen: "3.0 Main Screen-Rail-v4" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Screen: "7.2.2 Smartcard/Menu-ABT" → Screen: "7.3.6 Smartcard/ABT/Mini Statement"
- Screen: "2.2 Main Screen-Rail selected" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Decision: "Is the Smartcard valid?" → Screen: "7.2.2 Smartcard/Menu-ABT"
- Screen: "7.2.2 Smartcard/Menu-ABT" → Decision: "Adult"
- Decision: "Card Write Success?" → Screen: "7.6.1 Top Up/Top Up Error"
- Screen: "7.5.8 Smartcard/Top Up/ABT/Basket/Expired" → Decision: "Card Write Success?"
- Screen: "7.4.6 ABT Smartcard/Top Up" → Screen: "7.5.8 Smartcard/Top Up/ABT/Basket/Expired"
- Screen: "7.4.6 ABT Smartcard/Top Up" → Screen: "7.2.2 Smartcard/Menu-ABT"
- Screen: "7.3.1 Smartcard/Top Up" → Screen: "7.2.1 Smartcard/Menu"
- Decision: "Card Write Success?" → Screen: "7.5.3 Smartcard/Top Up/Remove Smartcard" [Top up receipt is printed]
- Decision: "Card Write Success?" → Screen: "7.6.1 Top Up/Top Up Error"
- Screen: "7.4.2 Smartcard/Top Up/Basket" → Decision: "Card Write Success?"
- Screen: "7.6.1 Top Up/Top Up Error" → Screen: "7.4.2 Smartcard/Top Up/Basket"
- Decision: "42b85ecc-76cd-40bd-9d8d-3be3b6df8636" → Decision: "Card Write Success?"
- Decision: "Card Write Success?" → Screen: "7.5.3 Smartcard/Top Up/Remove Smartcard/Expiry" [Top up receipt is printed]
- Decision: "Card Write Success?" → Screen: "7.6.1 Top Up/Top Up Error"
- Screen: "7.5.6 Smartcard/Top Up/Ulsterbus Travelcard/Basket" → Decision: "Card Write Success?"
- Screen: "7.5.6 Smartcard/Top Up/Ulsterbus Travelcard/Basket" → Decision: "42b85ecc-76cd-40bd-9d8d-3be3b6df8636"
- Screen: "7.5.6 Smartcard/Top Up/Ulsterbus Travelcard/Basket" → Decision: "If the product is expired and a period of travel is loaded onto it then this screen will show "New Expiry date: From First Use".

If the product is not expired and a period of travel is loaded onto it then this screen will show the expiry date as per your example below."
- Screen: "7.5.6 Smartcard/Top Up/Ulsterbus Travelcard/Basket" → Decision: "Card Write Success?"
- Screen: "7.4.4 Smartcard/Top Up-Ulsterbus Travelcard" → Screen: "7.5.6 Smartcard/Top Up/Ulsterbus Travelcard/Basket"
- Screen: "7.6.2 Smartcard/Top Up-Ulsterbus Travelcard-Expired" → Screen: "7.5.6 Smartcard/Top Up/Ulsterbus Travelcard/Basket"
- Decision: "Is the Smartcard valid?" → Screen: "7.5.1 Smartcard/Error"
- Screen: "7.1.1 Smartcard/Please Present Smartcard" → Decision: "Is the Smartcard valid?"
- Screen: "2.5.2 Main Screen-Ulsterbus selected" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Screen: "3.0 Main Screen-Rail-v4" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Screen: "7.2.1 Smartcard/Menu" → Screen: "7.3.7 Smartcard/DayLink/Mini Statement"
- Screen: "2.2 Main Screen-Rail selected" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Decision: "Is the Smartcard valid?" → Screen: "7.2.1 Smartcard/Menu"
- Screen: "7.2.1 Smartcard/Menu" → Decision: "Adult"
- Screen: "7.2.1 Smartcard/Menu" → Decision: "Child"
- Decision: "5412e25a-717f-4d0d-a575-7efda88b8565" → Decision: "Card Write Success?"
- Decision: "Card Write Success?" → Screen: "7.5.3 Smartcard/Top Up/Remove Smartcard/Daylink" [Top up receipt is printed]
- Decision: "Card Write Success?" → Screen: "7.6.1 Top Up/Top Up Error"
- Screen: "7.5.3 Smartcard/Top Up/Remove Smartcard/Daylink" → Decision: "Return to the beginning of the flow"
- Decision: "Adult" → Screen: "7.4.7 Smartcard/Top Up-Daylink"
- Screen: "7.5.9 Smartcard/Top Up/Daylink/Payment" → Decision: "Card Write Success?"
- Screen: "7.5.9 Smartcard/Top Up/Daylink/Payment" → Decision: "5412e25a-717f-4d0d-a575-7efda88b8565"
- Screen: "7.5.9 Smartcard/Top Up/Daylink/Payment" → Decision: "Card Write Success?"
- Screen: "7.6.1 Top Up/Top Up Error" → Screen: "7.5.6 Smartcard/Top Up/Ulsterbus Travelcard/Basket"
- Screen: "7.4.7 Smartcard/Top Up-Daylink" → Screen: "7.5.9 Smartcard/Top Up/Daylink/Payment"
- Decision: "Is the Smartcard valid?" → Screen: "7.5.1 Smartcard/Error"
- Screen: "7.1.1 Smartcard/Please Present Smartcard" → Decision: "Is the Smartcard valid?"
- Screen: "2.5.2 Main Screen-Ulsterbus selected" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Screen: "3.0 Main Screen-Rail-v4" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Screen: "7.2.1 Smartcard/Menu" → Screen: "7.3.8 Smartcard/Belfast Visitor Pass/Mini Statement"
- Screen: "2.2 Main Screen-Rail selected" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Decision: "Is the Smartcard valid?" → Screen: "7.2.1 Smartcard/Menu"
- Screen: "7.2.1 Smartcard/Menu" → Decision: "Adult"
- Screen: "7.2.1 Smartcard/Menu" → Decision: "Child"
- Decision: "e086b0d1-abac-419c-a24c-a7866738648a" → Decision: "Card Write Success?"
- Decision: "Card Write Success?" → Screen: "7.5.3 Smartcard/Top Up/Remove Smartcard/Expiry" [Top up receipt is printed]
- Decision: "Card Write Success?" → Screen: "7.6.1 Top Up/Top Up Error"
- Screen: "7.5.3 Smartcard/Top Up/Remove Smartcard/Expiry" → Decision: "Return to the beginning of the flow"
- Screen: "7.5.10 Smartcard/Top Up/Belfast Visitor/Payment" → Decision: "Card Write Success?"
- Screen: "7.5.10 Smartcard/Top Up/Belfast Visitor/Payment" → Decision: "e086b0d1-abac-419c-a24c-a7866738648a"
- Screen: "7.5.10 Smartcard/Top Up/Belfast Visitor/Payment" → Decision: "If the card is expired and a period of travel is loaded onto it then this screen will show "New Expiry Date: From First Use". If the card is not expired and a period of travel is loaded onto it then this screen will show the expiry date."
- Screen: "7.5.10 Smartcard/Top Up/Belfast Visitor/Payment" → Decision: "Card Write Success?"
- Screen: "7.4.8 Smartcard/Top Up-Belfast Visitor" → Screen: "7.5.10 Smartcard/Top Up/Belfast Visitor/Payment"
- Screen: "7.4.9 Smartcard/Top Up-Belfast Visitor/Expired" → Screen: "7.5.10 Smartcard/Top Up/Belfast Visitor/Payment"
- Screen: "7.6.1 Top Up/Top Up Error" → Screen: "7.5.10 Smartcard/Top Up/Belfast Visitor/Payment"
- Decision: "Is the Smartcard valid?" → Screen: "7.5.1 Smartcard/Error"
- Screen: "7.1.1 Smartcard/Please Present Smartcard" → Decision: "Is the Smartcard valid?"
- Screen: "2.5.2 Main Screen-Ulsterbus selected" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Screen: "3.0 Main Screen-Rail-v4" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Screen: "7.2.1 Smartcard/Menu" → Screen: "7.3.9 Smartcard/iLink/Mini Statement"
- Screen: "2.2 Main Screen-Rail selected" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Decision: "Is the Smartcard valid?" → Screen: "7.2.1 Smartcard/Menu"
- Screen: "7.2.1 Smartcard/Menu" → Decision: "Adult"
- Screen: "7.2.1 Smartcard/Menu" → Decision: "Child"
- Decision: "f288076f-5cb2-43ba-af41-661b1fcda91b" → Decision: "Card Write Success?"
- Decision: "Card Write Success?" → Screen: "7.5.3 Smartcard/Top Up/Remove Smartcard/Expiry" [Top up receipt is printed]
- Decision: "Card Write Success?" → Screen: "7.6.1 Top Up/Top Up Error"
- Screen: "7.5.3 Smartcard/Top Up/Remove Smartcard/Expiry" → Decision: "Return to the beginning of the flow"
- Screen: "7.5.11 Smartcard/Top Up/iLink/Payment" → Decision: "Card Write Success?"
- Screen: "7.4.10 Smartcard/Top Up/iLink" → Screen: "7.5.11 Smartcard/Top Up/iLink/Payment"
- Screen: "7.4.11 Smartcard/Top Up/iLink/Expired" → Screen: "7.5.11 Smartcard/Top Up/iLink/Payment"
- Screen: "7.6.1 Top Up/Top Up Error" → Screen: "7.5.11 Smartcard/Top Up/iLink/Payment"
- Decision: "Free Smartpasses" → Decision: "Senior Smartpass"
- Decision: "Free Smartpasses" → Decision: "60+ Smartpass"
- Decision: "Free Smartpasses" → Decision: "RoI Senior Smartpass"
- Decision: "Free Smartpasses" → Decision: "Blind Smartpass"
- Decision: "Free Smartpasses" → Decision: "War Pensioner
Smartpass"
- Decision: "Senior Smartpass" → Screen: "7.9.1 Bus Main Screen-Senior Single"
- Decision: "Senior Smartpass" → Screen: "7.9.3 Main Screen-Rail-Senior Single"
- Screen: "7.9.1 Bus Main Screen-Senior Single" → Screen: "7.9.2 Bus Main Screen-Senior Single-Alighting Selected"
- Screen: "7.9.3 Main Screen-Rail-Senior Single" → Decision: "Ticket is printed."
- Screen: "7.9.2 Bus Main Screen-Senior Single-Alighting Selected" → Decision: "Ticket is printed."
- Screen: "7.9.3 Main Screen-Rail-Senior Single" → Screen: "7.9.4 Main Screen-Rail-Senior Single Cross Border"
- Screen: "7.9.4 Main Screen-Rail-Senior Single Cross Border" → Decision: "Ticket is printed."
- Screen: "7.9.4 Main Screen-Rail-Senior Single Cross Border" → Decision: "If operator sets a cross border journey ticket type will change to Senior XB Single and will be available to change to:
Senior XB Day Return
Senior XB 1 Mth Return
using R4 key and then choose from the list or using L4 toggle key."
- Decision: "Half-Fare Smartpass" → Decision: "Disability Living 
Allowance"
- Decision: "Half-Fare Smartpass" → Decision: "Learning Disability"
- Decision: "Half-Fare Smartpass" → Decision: "No Driving Licence"
- Decision: "Half-Fare Smartpass" → Decision: "Partially Sighted"
- Decision: "Half-Fare Smartpass" → Decision: "PIPS"
- Decision: "Disability Living 
Allowance" → Screen: "7.9.5 Bus Main Screen-DLA Single"
- Decision: "Disability Living 
Allowance" → Screen: "7.9.7 Main Screen-Rail-DLA Single"
- Screen: "7.9.5 Bus Main Screen-DLA Single" → Screen: "7.9.6 Bus Main Screen-DLA Single-Alighting Selected"
- Screen: "7.9.7 Main Screen-Rail-DLA Single" → Screen: "7.9.8 Smartcard/Validation/DLA Single/Payment"
- Screen: "7.9.6 Bus Main Screen-DLA Single-Alighting Selected" → Screen: "7.9.8 Smartcard/Validation/DLA Single/Payment"
- Screen: "7.9.8 Smartcard/Validation/DLA Single/Payment" → Decision: "After Payment
flow is completed
the selected ticket
is printed."
- Screen: "7.9.9 Bus Main Screen-yLink Single" → Screen: "7.9.10 Bus Main Screen-yLink Single-Alighting Selected"
- Screen: "7.9.12 Smartcard/Validation/yLink Single/Payment" → Decision: "After Payment
flow is completed
the selected ticket
is printed."
- Decision: "yLink" → Screen: "7.9.9 Bus Main Screen-yLink Single"
- Decision: "yLink" → Screen: "7.9.10 Bus Main Screen-yLink Single-Alighting Selected"
- Decision: "yLink" → Screen: "7.9.11 Main Screen-Rail-yLink Single"
- Screen: "7.9.10 Bus Main Screen-yLink Single-Alighting Selected" → Screen: "7.9.12 Smartcard/Validation/yLink Single/Payment"
- Screen: "7.9.11 Main Screen-Rail-yLink Single" → Screen: "7.9.12 Smartcard/Validation/yLink Single/Payment"
- Screen: "7.9.14 Smartcard/Validation/24+/Payment" → Decision: "After Payment
flow is completed
the selected ticket
is printed."
- Decision: "24+" → Screen: "7.9.13 Main Screen-Rail-24+"
- Screen: "7.9.13 Main Screen-Rail-24+" → Screen: "7.9.14 Smartcard/Validation/24+/Payment"
- Screen: "7.9.15 Bus Main Screen-Dependants Pass" → Screen: "7.9.16 Bus Main Screen-yLink Single-Dependants Pass"
- Decision: "Dependants Pass" → Screen: "7.9.15 Bus Main Screen-Dependants Pass"
- Decision: "Dependants Pass" → Screen: "7.9.16 Bus Main Screen-yLink Single-Dependants Pass"
- Decision: "Dependants Pass" → Screen: "7.9.17 Main Screen-Rail-Dependants Pass"
- Screen: "7.11.1 Smartcard - Faulty - Select Card Type" → Screen: "7.11.2 Smartcard - Faulty - Charge Full Fare"
- Screen: "7.11.1 Smartcard - Faulty - Select Card Type" → Screen: "7.11.2 Smartcard - Faulty - Charge Full Fare"
- Screen: "7.11.1 Smartcard - Faulty - Select Card Type" → Screen: "7.11.3 Smartcard - Faulty - Issue Ticket"
- Decision: "Faulty Smartcard presented" → Screen: "7.11.1 Smartcard - Faulty - Select Card Type"
- Screen: "7.11.2 Smartcard - Faulty - Charge Full Fare" → Screen: "7.11.1 Smartcard - Faulty - Select Card Type"
- Screen: "7.11.3 Smartcard - Faulty - Issue Ticket" → Screen: "7.11.1 Smartcard - Faulty - Select Card Type"
- Screen: "7.11.3 Smartcard - Faulty - Issue Ticket" → Decision: "7 Day Faulty Ticket
is printed"
- Decision: "Smartcard presented outside of a relevant
Time Band." → Screen: "7.11.4 Smartcard - Faulty - Outside Time Band"
- Decision: "Passback of Smartcard/Smartpass" → Screen: "7.11.5 FLU - Smartcard Already Validated"
- Decision: "Hotlisted/Expired Card" → Screen: "7.11.6 Hotlisted Error"
- Decision: "60+ Smartpass" → Decision: "Ticket is printed."
- Decision: "RoI Senior Smartpass" → Decision: "Ticket is printed."
- Decision: "Blind Smartpass" → Decision: "Ticket is printed."
- Decision: "War Pensioner
Smartpass" → Decision: "Ticket is printed."
- Screen: "7.2.1 Smartcard/Menu" → Decision: "Adult"
- Decision: "Customer
presents card." → Decision: "Faulty Smartcard presented"
- Decision: "Customer
presents card." → Decision: "Smartcard presented outside of a relevant
Time Band."
- Decision: "Customer
presents card." → Decision: "Passback of Smartcard/Smartpass"
- Decision: "Customer
presents card." → Decision: "Hotlisted/Expired Card"
- Screen: "7.5.3 Smartcard/Top Up/Remove Smartcard/Value" → Decision: "Return to beginning of the flow"
- Decision: "Card Write Success?" → Screen: "7.5.3 Smartcard/Top Up/Remove Smartcard/Value" [Top up receipt is printed]
- Decision: "Ticket is printed." → Screen: "7.10.1 Main Screen-Validation-Confirmation-000"
- Decision: "Ticket is printed." → Screen: "7.10.2 Rail-Validation-Confirmation-000"
- Decision: "After Payment
flow is completed
the selected ticket
is printed." → Screen: "7.10.3 Main Screen-Validation-Confirmation"
- Decision: "After Payment
flow is completed
the selected ticket
is printed." → Screen: "7.10.4 Rail-Validation-Confirmation"
- Decision: "After Payment
flow is completed
the selected ticket
is printed." → Screen: "7.10.3 Main Screen-Validation-Confirmation"
- Decision: "After Payment
flow is completed
the selected ticket
is printed." → Screen: "7.10.4 Rail-Validation-Confirmation"
- Decision: "The selected ticket
is printed." → Screen: "7.10.1 Main Screen-Validation-Confirmation-000"
- Decision: "The selected ticket
is printed." → Screen: "7.10.2 Rail-Validation-Confirmation-000"
- Decision: "After Payment
flow is completed
the selected ticket
is printed." → Screen: "7.10.4 Rail-Validation-Confirmation"
- Screen: "7.5.11 Smartcard/Top Up/iLink/Payment" → Decision: "f288076f-5cb2-43ba-af41-661b1fcda91b"
- Screen: "7.5.11 Smartcard/Top Up/iLink/Payment" → Decision: "If the card is expired and a period of travel is loaded onto it then this screen will show "New Expiry date: From First Use".

If the card is not expired and a period of travel is loaded onto it then this screen will show the expiry date as per your example below."
- Screen: "7.2.1 Smartcard/Menu" → Screen: "7.3.3 Smartcard/Town Service Travelcard/Mini Statement"
- Screen: "7.3.2 Smartcard/Ulsterbus Multi Journey/Mini Statement" → Decision: "After printing process,
user will automatically return to Top up menu."
- Screen: "7.3.3 Smartcard/Town Service Travelcard/Mini Statement" → Decision: "After printing process,
user will automatically return to Top up menu."
- Screen: "7.2.1 Smartcard/Menu" → Screen: "7.3.5 Smartcard/Metro Travelcard/Mini Statement"
- Screen: "7.3.4 Smartcard/Metro Multi Journey/Mini Statement" → Decision: "After printing process,
user will automatically return to Top up menu."
- Screen: "7.3.5 Smartcard/Metro Travelcard/Mini Statement" → Decision: "After printing process,
user will automatically return to Top up menu."
- Screen: "7.3.6 Smartcard/ABT/Mini Statement" → Decision: "After printing process,
user will automatically return to Top up menu."
- Screen: "7.3.7 Smartcard/DayLink/Mini Statement" → Decision: "After printing process,
user will automatically return to Top up menu."
- Screen: "7.3.8 Smartcard/Belfast Visitor Pass/Mini Statement" → Decision: "After printing process,
user will automatically return to Top up menu."
- Screen: "7.3.9 Smartcard/iLink/Mini Statement" → Decision: "After printing process,
user will automatically return to Top up menu."
- Screen: "7.5.11 Smartcard/Top Up/iLink/Payment" → Decision: "Card Write Success?"
- Screen: "7.9.16 Bus Main Screen-yLink Single-Dependants Pass" → Decision: "The selected ticket
is printed."
- Screen: "7.9.17 Main Screen-Rail-Dependants Pass" → Decision: "The selected ticket
is printed."
- Screen: "7.2.2 Smartcard/Menu-ABT" → Decision: "Child"
- Decision: "Adult" → Screen: "7.4.6 ABT Smartcard/Top Up"
- Screen: "7.2.2 Smartcard/Menu-ABT" → Decision: "Card Issue
flow"
- Decision: "Is the product "FirstUse"?" → Decision: "Is the product expired?"
- Decision: "Is the product expired?" → Screen: "7.6.2 Smartcard/Top Up-Ulsterbus Travelcard-Expired"
- Decision: "Is the product "FirstUse"?" → Screen: "7.7.1 Top Up/Top Up Error Not Used"
- Decision: "Is the product expired?" → Screen: "7.4.4 Smartcard/Top Up-Ulsterbus Travelcard"
- Screen: "7.7.1 Top Up/Top Up Error Not Used" → Screen: "2.2 Main Screen-Rail selected"
- Decision: "Is the product "FirstUse"?" → Decision: "Is the product expired?"
- Decision: "Is the product "FirstUse"?" → Screen: "7.7.1 Top Up/Top Up Error Not Used"
- Screen: "7.7.1 Top Up/Top Up Error Not Used" → Screen: "2.2 Main Screen-Rail selected"
- Decision: "Is the product expired?" → Screen: "7.6.3 Smartcard/Top Up-Metro Travelcard-Expired"
- Decision: "Is the product expired?" → Screen: "7.4.5 Smartcard/Top Up-Metro Travelcard"
- Decision: "Is the product "FirstUse"?" → Decision: "Is the product expired?"
- Decision: "Is the product "FirstUse"?" → Screen: "7.7.1 Top Up/Top Up Error Not Used"
- Screen: "7.7.1 Top Up/Top Up Error Not Used" → Screen: "2.2 Main Screen-Rail selected"
- Decision: "Is the product expired?" → Screen: "7.4.9 Smartcard/Top Up-Belfast Visitor/Expired"
- Decision: "Is the product expired?" → Screen: "7.4.8 Smartcard/Top Up-Belfast Visitor"
- Decision: "Is the product "FirstUse"?" → Decision: "Is the product expired?"
- Decision: "Is the product "FirstUse"?" → Screen: "7.7.1 Top Up/Top Up Error Not Used"
- Screen: "7.7.1 Top Up/Top Up Error Not Used" → Screen: "2.2 Main Screen-Rail selected"
- Decision: "Is the product expired?" → Screen: "7.4.11 Smartcard/Top Up/iLink/Expired"
- Decision: "Is the product expired?" → Screen: "7.4.10 Smartcard/Top Up/iLink"
- Screen: "7.2.2 Smartcard/Menu-ABT" → Decision: "Pressing the 'Recover Unique Code' button will print a receipt with the Smartcard code on."
- Screen: "7.5.8 Smartcard/Top Up/ABT/Basket/Expired" → Decision: "e6a4bd9a-4f1a-4564-8b8d-5cb6bf907b8e" [Bank Card]
- Screen: "7.5.8 Smartcard/Top Up/ABT/Basket/Expired" → Decision: "Card Write Success?" [Warrant]
- Screen: "7.5.3 Smartcard/Top Up/Remove Smartcard/Expiry" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Screen: "7.5.3 Smartcard/Top Up/Remove Smartcard" → Screen: "7.1.2 Metro Smartcard/Please Present Smartcard"
- Screen: "7.5.3 Smartcard/Top Up/Remove Smartcard/Expiry" → Decision: "60e3c3ad-8edc-49fd-9786-f98806b4659f"
- Decision: "Metro Travelcard" → Decision: "Is the product "FirstUse"?"
- Decision: "Town Service Travelcard" → Decision: "Is the product "FirstUse"?"
- Decision: "Adult" → Decision: "Is the product "FirstUse"?"
- Decision: "Adult" → Decision: "Is the product "FirstUse"?"


## 9. 8.0 Issue Card

### Screens (52)
- 2.2 Main Screen-Rail selected
- 2.5.2 Main Screen-Ulsterbus selected
- 3.0 Main Screen-Rail-v4
- 7.1.1 Smartcard/Please Present Smartcard
- 8.2.7 Smartcard/Issue Smartcard/iLink1/BVP
- 8.1.1 Smartcard/Issue Smartcard/Adult
- 7.2.2 Smartcard/Menu-ABT
- 8.2.4 Smartcard/Card Issue-Daylink
- 8.2.6 Smartcard/Card Issue/iLink
- 8.2.2 Smartcard/Card Issue-Ulsterbus Travelcard
- 8.2.1.1 Ulsterbus Smartcard/Reference Numbers
- 8.2.1 Ulsterbus Smartcard/Card Issue
- 8.3.4 Smartcard/Card Issue/Daylink/Payment
- Smartcard/Card Issue/iLink
- 8.3.7 Smartcard/Card Issue/iLink zone 3/Payment
- 8.2.5 Smartcard/Card Issue-Belfast Visitor
- 7.2.3 ABT Smartcard/Adult or Child
- 8.2.3 ABT Smartcard/Card Issue
- 7.5.1 Smartcard/Error
- 7.3.6 Smartcard/ABT/Mini Statement
- 8.3.2 Smartcard/Card Issue/Ulsterbus Travelcard/Basket
- 8.3.1 Ulsterbus Smartcard/Card Issue/Basket
- 8.5.1 Smartcard/Issue Card/Remove Smartcard
- 8.5.1 Smartcard/Issue Card/Remove Smartcard
- 8.3.5 Smartcard/Card Issue/Belfast Visitor/Payment
- 8.3.6 Smartcard/Card Issue/iLink/Payment
- 8.2.1.2 Ulsterbus Smartcard/Reference Numbers/Invalid
- 8.3.3 Smartcard/Card Issue/ABT/Basket/Expired
- 8.5.1 Smartcard/Issue Card/Remove Smartcard
- 8.5.1 Smartcard/Issue Card/Remove Smartcard
- 8.5.1 Smartcard/Issue Card/Remove Smartcard
- 8.2.3.1 ABT Smartcard/Card Issue/Custom Amount
- 8.5.1 Smartcard/Issue Card/Remove Smartcard
- 8.4.1 Card Issue/Card Issue Error
- 8.4.1 Card Issue/Card Issue Error
- 8.4.1 Card Issue/Card Issue Error
- 8.4.1 Card Issue/Card Issue Error
- 8.2.3.2 ABT Smartcard/Card Issue/Invalid Amount
- 8.4.1 Card Issue/Card Issue Error
- 8.4.1 Card Issue/Card Issue Error
- 7.1.2 Metro Smartcard/Please Present Smartcard
- 8.1.1.1 Smartcard/Issue Smartcard/Adult/Metro
- 8.6.2 Smartcard/Card Issue-Metro Travelcard
- 8.5.2 Smartcard/Issue Smartcard/Metro Zone
- 7.5.1 Smartcard/Error
- 8.6.1 Smartcard/Card Issue
- 8.7.2 Smartcard/Card Issue/Metro Travelcard/Basket
- 8.7.1 Smartcard/Card Issue/Basket
- 8.5.1 Smartcard/Issue Card/Remove Smartcard
- 8.5.1 Smartcard/Issue Card/Remove Smartcard
- Card Issue/Card Issue Error
- 8.4.1 Card Issue/Card Issue Error

### Decision Points (45)
- iLink (excluding Zone 1)
- Smartlink
- ABT
- Daylink
- iLink Zone 1 and Belfast Visitor Pass
- Child
- Adult
- Child
- Adult
- Child
- Adult
- Child
- Adult
- Is the Smartcard valid?
- See Metro flow below
- Top Up flow
- This will need to state the number of days topped up.
- This will need to state: <X> <Period> From First Use
- Card Issue receipt is printed
- Card Issue receipt is printed
- This will need to state <X> <Period> from first use.
- Card Write Success?
- Card Write Success?
- After printing process, user will automatically return back to previous screen.
- Card Issue receipt is printed
- This will need to state: <X> <Period> From First Use
- Card Issue receipt is printed
- Card Issue receipt is printed
- Card Write Success?
- This will need to state the value of the top up.
- Card Write Success?
- Card Write Success?
- Card Issue receipt is printed
- Card Write Success?
- Is it Smartlink?
- Adult
- Child
- Is the Smartcard valid?
- Metro card issues - can be paid for by card or warrant but only by a UB/NIR operator
- Metro card issues - can be paid for by card or warrant but only by a UB/NIR operator
- This will need to state <X> <Period> from first use.
- Card Issue receipt is printed
- Card Write Success?
- Card Issue receipt is printed
- Card Write Success?

### Annotations / Spec Notes (95)
- Issue Card
- Any Translink Smartcard can be issued from any Ulsterbus or NIR POS device.
- User may choose 'Smartcard' at any given time on the Main Screen and both Bus or Rail FLU screens.
- User will be prompted to present Smartcard.
- Yes
- User selects Smartcard from Main Menu.
- Selection of adult or child will be done automatically by the POS according to the data on the card. All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- Selection of adult or child will be done automatically by the POS according to the data on the card. All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- Selection of adult or child will be done automatically by the POS according to the data on the card. All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- If the Smartcard card is valid and blank (pre-encoded information only), user is able to select Issue Smartcard.
- Selection of adult or child will be done automatically by the POS according to the data on the card. All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- The text 'ABT' on screens will be replaced by the ABT brand name.
- User is able to choose a product pressing the corresponding buttons.
- User is able to choose a product pressing the corresponding buttons.
- The iLink zone is determined from the card encoding.
- No
- User is able to choose a product pressing the corresponding buttons.
- User is able to choose a product pressing the corresponding buttons.
- The text 'ABT' on screens will be replaced by the ABT brand name. The flow after selecting Adult or Child will remain the same.
- User will see a confirmation screen with options for payment methods.
- A Card Issue Successful screen is presented and user has to remove Smartcard to`continue.
- If the Smartcard presented is not valid, user will receive an Error Screen. Timeout of 3 seconds or press any key will go back to Main Menu.
- A Card Issue Successful screen is presented and user has to remove Smartcard to`continue.
- "Pressing "C" button will take the operator back to select an alternative card reference number.
- *Enter button has no function on this screen*
- *Enter button has no function on this screen*
- *Only the cash option is available to Metro users*
- Card payment flow
- *Only the cash option is available to Metro users*
- Card payment flow
- Card payment flow
- The text 'ABT' on screens will be replaced by the ABT brand name.
- A Card Issue Successful screen is presented and user has to remove Smartcard to`continue.
- A Card Issue Successful screen is presented and user has to remove Smartcard to`continue.
- A Card Issue Successful screen is presented and user has to remove Smartcard to`continue.
- *Only the cash option is available to Metro users*
- *Enter button has no function on this screen*
- *Enter button has no function on this screen*
- Yes
- *Enter button has no function on this screen*
- Yes
- When this screen is shown:  1) If payment was by card the card transaction is voided  2) No transaction record will have been recorded on the POS and subsequently no totals information would have been updated  3) Some data may have been written to the smartcard but it would have been written to a section of the smartcard that is not currently being used so will have no effect on smartcard operation  4) A diagnostic/event is recorded to audit this error occurred"
- When this screen is shown:  1) If payment was by card the card transaction is voided  2) No transaction record will have been recorded on the POS and subsequently no totals information would have been updated  3) Some data may have been written to the smartcard but it would have been written to a section of the smartcard that is not currently being used so will have no effect on smartcard operation  4) A diagnostic/event is recorded to audit this error occurred"
- *Only the cash option is available to Metro users*
- *Only the cash option is available to Metro users*
- *Only the cash option is available to Metro users*
- Card payment flow
- Card payment flow
- Card payment flow
- No
- A Card Issue Successful screen is presented and user has to remove Smartcard to`continue.
- No
- Customer access code is printed on the card issue receipt.
- Yes
- *Only the cash option is available to Metro users*
- When this screen is shown:  1) If payment was by card the card transaction is voided  2) No transaction record will have been recorded on the POS and subsequently no totals information would have been updated  3) Some data may have been written to the smartcard but it would have been written to a section of the smartcard that is not currently being used so will have no effect on smartcard operation  4) A diagnostic/event is recorded to audit this error occurred"
- When this screen is shown:  1) If payment was by card the card transaction is voided  2) No transaction record will have been recorded on the POS and subsequently no totals information would have been updated  3) Some data may have been written to the smartcard but it would have been written to a section of the smartcard that is not currently being used so will have no effect on smartcard operation  4) A diagnostic/event is recorded to audit this error occurred"
- Yes
- Yes
- When this screen is shown:  1) If payment was by card the card transaction is voided  2) No transaction record will have been recorded on the POS and subsequently no totals information would have been updated  3) Some data may have been written to the smartcard but it would have been written to a section of the smartcard that is not currently being used so will have no effect on smartcard operation  4) A diagnostic/event is recorded to audit this error occurred"
- Card payment flow
- No
- No
- No
- Yes
- When this screen is shown:  1) If payment was by card the card transaction is voided  2) No transaction record will have been recorded on the POS and subsequently no totals information would have been updated  3) Some data may have been written to the smartcard but it would have been written to a section of the smartcard that is not currently being used so will have no effect on smartcard operation  4) A diagnostic/event is recorded to audit this error occurred"
- The operator will be able to to try again to write information on the smartcard or to cancel the process which would void the transaction and return to the previous screen.
- The operator will be able to to try again to write information on the smartcard or to cancel the process which would void the transaction and return to the previous screen.
- No
- The operator will be able to to try again to write information on the smartcard or to cancel the process which would void the transaction and return to the previous screen.
- The operator will be able to to try again to write information on the smartcard or to cancel the process which would void the transaction and return to the previous screen.
- The operator will be able to to try again to write information on the smartcard or to cancel the process which would void the transaction and return to the previous screen.
- The operator will be able to to try again to write information on the smartcard or to cancel the process which would void the transaction and return to the previous screen.
- Metro POS Card Issue Flow
- Any Translink Smartcard can be issued from a Metro POS except for Ulsterbus Multi-Journey and Ulsterbus Town Services Travelcard
- User will be prompted to present Smartcard. This is the first screen Metro operator will be presented after sign on process.
- Yes
- Selection of adult or child will be done automatically by the POS according to the data on the card. All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- No
- User is able to choose a product pressing the corresponding buttons.
- This is a catch all error screen for issues with the smartcard. For example, this could be a card that is not specific for Translink (anything not in a recognised format). Timeout of 3 seconds or pressing any key will go back to previous screen.
- User will see a confirmation screen with options for payment methods.
- A Card Issue Successful screen is presented and user has to remove Smartcard to`continue.
- Pressing 'C' button will reset value and journeys number.
- *Enter button has no function on this screen*
- A Card Issue Successful screen is presented and user has to remove Smartcard to`continue.
- *Enter button has no function on this screen*
- Yes
- When this screen is shown:  1) If payment was by card the card transaction is voided  2) No transaction record will have been recorded on the POS and subsequently no totals information would have been updated  3) Some data may have been written to the smartcard but it would have been written to a section of the smartcard that is not currently being used so will have no effect on smartcard operation  4) A diagnostic/event is recorded to audit this error occurred"
- No
- Yes
- When this screen is shown:  1) If payment was by card the card transaction is voided  2) No transaction record will have been recorded on the POS and subsequently no totals information would have been updated  3) Some data may have been written to the smartcard but it would have been written to a section of the smartcard that is not currently being used so will have no effect on smartcard operation  4) A diagnostic/event is recorded to audit this error occurred"
- No
- The operator will be able to to try again to write information on the smartcard or to cancel the process which would void the transaction and return to the previous screen.
- The operator will be able to to try again to write information on the smartcard or to cancel the process which would void the transaction and return to the previous screen.

### Connections / Flow (129)
- Decision: "Is the Smartcard valid?" → Screen: "7.5.1 Smartcard/Error"
- Screen: "2.2 Main Screen-Rail selected" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Screen: "7.1.1 Smartcard/Please Present Smartcard" → Decision: "Is the Smartcard valid?"
- Screen: "3.0 Main Screen-Rail-v4" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Screen: "2.5.2 Main Screen-Ulsterbus selected" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Decision: "Is the Smartcard valid?" → Decision: "Smartlink"
- Decision: "754cd040-f4fe-40f9-bd58-af827e9b5b4b" → Decision: "Card Write Success?"
- Screen: "8.3.1 Ulsterbus Smartcard/Card Issue/Basket" → Decision: "Card Write Success?"
- Decision: "Card Write Success?" → Screen: "8.4.1 Card Issue/Card Issue Error"
- Screen: "8.3.1 Ulsterbus Smartcard/Card Issue/Basket" → Decision: "754cd040-f4fe-40f9-bd58-af827e9b5b4b"
- Screen: "8.2.1 Ulsterbus Smartcard/Card Issue" → Screen: "8.3.1 Ulsterbus Smartcard/Card Issue/Basket"
- Screen: "8.3.1 Ulsterbus Smartcard/Card Issue/Basket" → Decision: "Card Write Success?"
- Decision: "15828803-daff-476b-8a05-c2c2dfeae9ec" → Decision: "Card Write Success?"
- Decision: "Card Write Success?" → Screen: "8.5.1 Smartcard/Issue Card/Remove Smartcard"
- Decision: "Card Write Success?" → Screen: "8.4.1 Card Issue/Card Issue Error"
- Screen: "8.5.1 Smartcard/Issue Card/Remove Smartcard" → Decision: "Card Issue
receipt
is printed"
- Screen: "8.3.2 Smartcard/Card Issue/Ulsterbus Travelcard/Basket" → Decision: "Card Write Success?"
- Screen: "8.3.2 Smartcard/Card Issue/Ulsterbus Travelcard/Basket" → Decision: "15828803-daff-476b-8a05-c2c2dfeae9ec"
- Screen: "8.3.2 Smartcard/Card Issue/Ulsterbus Travelcard/Basket" → Decision: "Card Write Success?"
- Screen: "8.2.2 Smartcard/Card Issue-Ulsterbus Travelcard" → Screen: "8.3.2 Smartcard/Card Issue/Ulsterbus Travelcard/Basket"
- Screen: "8.4.1 Card Issue/Card Issue Error" → Screen: "8.3.2 Smartcard/Card Issue/Ulsterbus Travelcard/Basket"
- Decision: "Smartlink" → Decision: "Adult"
- Decision: "Adult" → Screen: "8.1.1 Smartcard/Issue Smartcard/Adult"
- Screen: "8.1.1 Smartcard/Issue Smartcard/Adult" → Screen: "8.2.1.1 Ulsterbus Smartcard/Reference Numbers"
- Decision: "Card Write Success?" → Screen: "8.5.1 Smartcard/Issue Card/Remove Smartcard"
- Screen: "8.5.1 Smartcard/Issue Card/Remove Smartcard" → Decision: "Card Issue
receipt
is printed"
- Decision: "Smartlink" → Decision: "Child"
- Decision: "Is the Smartcard valid?" → Screen: "7.5.1 Smartcard/Error"
- Screen: "7.1.2 Metro Smartcard/Please Present Smartcard" → Decision: "Is the Smartcard valid?"
- Screen: "8.6.1 Smartcard/Card Issue" → Screen: "8.7.1 Smartcard/Card Issue/Basket"
- Decision: "Card Write Success?" → Screen: "8.5.1 Smartcard/Issue Card/Remove Smartcard"
- Decision: "Card Write Success?" → Screen: "Card Issue/Card Issue Error"
- Screen: "8.5.1 Smartcard/Issue Card/Remove Smartcard" → Decision: "Card Issue
receipt
is printed"
- Screen: "8.7.2 Smartcard/Card Issue/Metro Travelcard/Basket" → Decision: "Card Write Success?"
- Screen: "Card Issue/Card Issue Error" → Screen: "8.7.2 Smartcard/Card Issue/Metro Travelcard/Basket"
- Decision: "Card Write Success?" → Screen: "8.5.1 Smartcard/Issue Card/Remove Smartcard"
- Decision: "Card Write Success?" → Screen: "8.4.1 Card Issue/Card Issue Error"
- Screen: "8.5.1 Smartcard/Issue Card/Remove Smartcard" → Decision: "Card Issue
receipt
is printed"
- Screen: "8.4.1 Card Issue/Card Issue Error" → Screen: "8.7.1 Smartcard/Card Issue/Basket"
- Decision: "Is it Smartlink?" → Decision: "Adult" [Yes]
- Decision: "Is it Smartlink?" → Decision: "Child"
- Screen: "8.6.2 Smartcard/Card Issue-Metro Travelcard" → Screen: "8.7.2 Smartcard/Card Issue/Metro Travelcard/Basket"
- Decision: "Is the Smartcard valid?" → Decision: "ABT"
- Decision: "65c98e6a-f3e3-4994-a6c0-50b6411181fe" → Decision: "Card Write Success?"
- Decision: "Card Write Success?" → Screen: "8.4.1 Card Issue/Card Issue Error"
- Screen: "8.2.3 ABT Smartcard/Card Issue" → Screen: "8.3.3 Smartcard/Card Issue/ABT/Basket/Expired"
- Screen: "8.5.1 Smartcard/Issue Card/Remove Smartcard" → Decision: "Card Issue
receipt
is printed"
- Decision: "Card Write Success?" → Screen: "8.5.1 Smartcard/Issue Card/Remove Smartcard"
- Decision: "Is the Smartcard valid?" → Decision: "Daylink"
- Decision: "b8a0e36b-27d4-4520-ad8e-5bc4a815ea3d" → Decision: "Card Write Success?"
- Decision: "Card Write Success?" → Screen: "8.4.1 Card Issue/Card Issue Error"
- Screen: "8.3.4 Smartcard/Card Issue/Daylink/Payment" → Decision: "Card Write Success?"
- Screen: "8.2.4 Smartcard/Card Issue-Daylink" → Screen: "8.3.4 Smartcard/Card Issue/Daylink/Payment"
- Decision: "Daylink" → Decision: "Adult"
- Decision: "Adult" → Screen: "8.2.4 Smartcard/Card Issue-Daylink"
- Decision: "Daylink" → Decision: "Child"
- Screen: "8.5.1 Smartcard/Issue Card/Remove Smartcard" → Decision: "Card Issue
receipt
is printed"
- Decision: "Card Write Success?" → Screen: "8.5.1 Smartcard/Issue Card/Remove Smartcard"
- Decision: "79750a57-0ad9-4b6b-bb0a-2bea1882bd53" → Decision: "Card Write Success?"
- Decision: "Card Write Success?" → Screen: "8.5.1 Smartcard/Issue Card/Remove Smartcard"
- Decision: "Card Write Success?" → Screen: "8.4.1 Card Issue/Card Issue Error"
- Screen: "8.5.1 Smartcard/Issue Card/Remove Smartcard" → Decision: "Card Issue
receipt
is printed"
- Screen: "8.3.5 Smartcard/Card Issue/Belfast Visitor/Payment" → Decision: "Card Write Success?"
- Screen: "8.4.1 Card Issue/Card Issue Error" → Screen: "8.3.5 Smartcard/Card Issue/Belfast Visitor/Payment"
- Decision: "iLink Zone 1 and
Belfast Visitor Pass" → Decision: "Adult"
- Decision: "iLink Zone 1 and
Belfast Visitor Pass" → Decision: "Child"
- Decision: "c16c2831-55b4-4488-b24e-bfaeb06a4c61" → Decision: "Card Write Success?"
- Decision: "Card Write Success?" → Screen: "8.4.1 Card Issue/Card Issue Error"
- Screen: "8.3.7 Smartcard/Card Issue/iLink zone 3/Payment" → Decision: "Card Write Success?"
- Screen: "8.2.6 Smartcard/Card Issue/iLink" → Screen: "8.3.7 Smartcard/Card Issue/iLink zone 3/Payment"
- Screen: "8.4.1 Card Issue/Card Issue Error" → Screen: "8.3.7 Smartcard/Card Issue/iLink zone 3/Payment"
- Decision: "iLink
(excluding Zone 1)" → Decision: "Adult"
- Decision: "iLink
(excluding Zone 1)" → Decision: "Child"
- Decision: "Is the Smartcard valid?" → Decision: "iLink Zone 1 and
Belfast Visitor Pass"
- Decision: "Is the Smartcard valid?" → Decision: "iLink
(excluding Zone 1)"
- Decision: "Card Write Success?" → Screen: "8.5.1 Smartcard/Issue Card/Remove Smartcard"
- Screen: "8.5.1 Smartcard/Issue Card/Remove Smartcard" → Decision: "Card Issue
receipt
is printed"
- Screen: "8.1.1 Smartcard/Issue Smartcard/Adult" → Screen: "8.2.2 Smartcard/Card Issue-Ulsterbus Travelcard"
- Decision: "ABT" → Screen: "7.2.2 Smartcard/Menu-ABT"
- Screen: "8.2.5 Smartcard/Card Issue-Belfast Visitor" → Screen: "8.3.5 Smartcard/Card Issue/Belfast Visitor/Payment"
- Screen: "8.3.3 Smartcard/Card Issue/ABT/Basket/Expired" → Decision: "Card Write Success?"
- Screen: "8.3.3 Smartcard/Card Issue/ABT/Basket/Expired" → Decision: "65c98e6a-f3e3-4994-a6c0-50b6411181fe"
- Screen: "8.3.3 Smartcard/Card Issue/ABT/Basket/Expired" → Decision: "Card Write Success?"
- Screen: "8.3.4 Smartcard/Card Issue/Daylink/Payment" → Decision: "Card Write Success?"
- Screen: "8.3.4 Smartcard/Card Issue/Daylink/Payment" → Decision: "b8a0e36b-27d4-4520-ad8e-5bc4a815ea3d"
- Screen: "8.4.1 Card Issue/Card Issue Error" → Decision: "Card Write Success?"
- Screen: "8.4.1 Card Issue/Card Issue Error" → Screen: "8.3.1 Ulsterbus Smartcard/Card Issue/Basket"
- Screen: "8.4.1 Card Issue/Card Issue Error" → Decision: "Card Write Success?"
- Screen: "8.4.1 Card Issue/Card Issue Error" → Decision: "Card Write Success?"
- Screen: "8.4.1 Card Issue/Card Issue Error" → Screen: "8.3.3 Smartcard/Card Issue/ABT/Basket/Expired"
- Screen: "8.4.1 Card Issue/Card Issue Error" → Decision: "Card Write Success?"
- Screen: "8.4.1 Card Issue/Card Issue Error" → Screen: "8.3.4 Smartcard/Card Issue/Daylink/Payment"
- Screen: "8.4.1 Card Issue/Card Issue Error" → Decision: "Card Write Success?"
- Screen: "8.4.1 Card Issue/Card Issue Error" → Decision: "Card Write Success?"
- Screen: "8.4.1 Card Issue/Card Issue Error" → Decision: "Card Write Success?"
- Screen: "Card Issue/Card Issue Error" → Decision: "Card Write Success?"
- Screen: "8.2.1.1 Ulsterbus Smartcard/Reference Numbers" → Screen: "8.1.1 Smartcard/Issue Smartcard/Adult"
- Screen: "8.5.2 Smartcard/Issue Smartcard/Metro Zone" → Screen: "8.6.1 Smartcard/Card Issue"
- Screen: "8.7.1 Smartcard/Card Issue/Basket" → Decision: "Card Write Success?"
- Screen: "8.3.5 Smartcard/Card Issue/Belfast Visitor/Payment" → Decision: "Card Write Success?"
- Screen: "8.3.5 Smartcard/Card Issue/Belfast Visitor/Payment" → Decision: "79750a57-0ad9-4b6b-bb0a-2bea1882bd53"
- Decision: "Adult" → Screen: "8.2.6 Smartcard/Card Issue/iLink"
- Decision: "Adult" → Screen: "8.2.7 Smartcard/Issue Smartcard/iLink1/BVP"
- Screen: "8.2.7 Smartcard/Issue Smartcard/iLink1/BVP" → Screen: "8.2.5 Smartcard/Card Issue-Belfast Visitor"
- Screen: "8.2.7 Smartcard/Issue Smartcard/iLink1/BVP" → Screen: "Smartcard/Card Issue/iLink"
- Screen: "Smartcard/Card Issue/iLink" → Screen: "8.3.6 Smartcard/Card Issue/iLink/Payment"
- Screen: "8.3.6 Smartcard/Card Issue/iLink/Payment" → Decision: "5881db98-ae18-42ed-8e93-b2a504101810"
- Screen: "8.3.6 Smartcard/Card Issue/iLink/Payment" → Decision: "Card Write Success?"
- Screen: "8.3.6 Smartcard/Card Issue/iLink/Payment" → Decision: "Card Write Success?"
- Decision: "5881db98-ae18-42ed-8e93-b2a504101810" → Decision: "Card Write Success?"
- Screen: "8.3.7 Smartcard/Card Issue/iLink zone 3/Payment" → Decision: "c16c2831-55b4-4488-b24e-bfaeb06a4c61"
- Screen: "8.3.7 Smartcard/Card Issue/iLink zone 3/Payment" → Decision: "Card Write Success?"
- Screen: "7.2.2 Smartcard/Menu-ABT" → Screen: "7.2.3 ABT Smartcard/Adult or Child" [Issue Card' option pressed.]
- Screen: "7.2.2 Smartcard/Menu-ABT" → Decision: "Top Up
flow"
- Decision: "Adult" → Screen: "8.1.1.1 Smartcard/Issue Smartcard/Adult/Metro"
- Screen: "8.1.1.1 Smartcard/Issue Smartcard/Adult/Metro" → Screen: "8.5.2 Smartcard/Issue Smartcard/Metro Zone"
- Screen: "8.1.1.1 Smartcard/Issue Smartcard/Adult/Metro" → Screen: "8.6.2 Smartcard/Card Issue-Metro Travelcard"
- Screen: "7.3.6 Smartcard/ABT/Mini Statement" → Decision: "After printing process,
user will automatically return back to previous screen."
- Screen: "7.2.2 Smartcard/Menu-ABT" → Screen: "7.3.6 Smartcard/ABT/Mini Statement"
- Screen: "7.2.3 ABT Smartcard/Adult or Child" → Screen: "8.2.3 ABT Smartcard/Card Issue"
- Screen: "8.2.1.1 Ulsterbus Smartcard/Reference Numbers" → Screen: "8.2.1 Ulsterbus Smartcard/Card Issue"
- Screen: "8.1.1 Smartcard/Issue Smartcard/Adult" → Decision: "See Metro flow below"
- Screen: "8.1.1 Smartcard/Issue Smartcard/Adult" → Decision: "See Metro flow below"
- Decision: "Is the Smartcard valid?" → Decision: "Is it Smartlink?"
- Decision: "Is it Smartlink?" → Decision: "ABT" [No]
- Screen: "8.2.1.1 Ulsterbus Smartcard/Reference Numbers" → Screen: "8.2.1.2 Ulsterbus Smartcard/Reference Numbers/Invalid" [Invalid card reference number entered]
- Screen: "8.2.3 ABT Smartcard/Card Issue" → Screen: "8.2.3.1 ABT Smartcard/Card Issue/Custom Amount" [Custom amount selected]
- Screen: "8.2.3.1 ABT Smartcard/Card Issue/Custom Amount" → Screen: "8.2.3.2 ABT Smartcard/Card Issue/Invalid Amount" [Invalid amount entered]
- Screen: "8.2.3.1 ABT Smartcard/Card Issue/Custom Amount" → Screen: "8.3.3 Smartcard/Card Issue/ABT/Basket/Expired" [Custom amount entered]


## 10. 9.0 Operator

### Screens (47)
- 2.2 Main Screen-Rail selected
- 2.5.2 Main Screen-Ulsterbus selected
- 3.0 Main Screen-Rail-v4
- 9.0 Operator Menu/Metro
- 9.1.6.1 Operator Menu/Operator Information/Metro
- 9.0 Operator Menu
- 9.1.7 Operator Menu/Annul Previous Ticket entered
- 9.1.2 Operator Menu/Totals
- 9.1.1 Operator Menu/Annul Rail/Misc Tickets
- 9.1.8 Operator Menu - Exccess Tickets
- 9.2.1 Operator Menu/Tickets & Totals/Annul Previous Ticket
- 9.1.3 Operator Menu/SignOff
- 9.1.5 Operator Menu/BreakMode
- 9.1.6 Operator Menu/Operator Information
- 7.1.1 Smartcard/Please Present Smartcard
- 9.2.5 Operator Menu/Tickets & Totals/Annul Previous Ticket Rail
- 9.2.7 Operator Menu - Exccess Tickets- Enter Value
- 9.2.8 Operator Menu - Exccess Tickets- Value Entered
- 9.4.5 Operator Menu/Operator Options/Ticket History
- 1.0 Idle Screen
- 9.4.4 Operator - Word and Colour of the Day
- 9.2.3 Idle Screen - Driver on Break
- 11.1.2 Soft Reboot - Confirm
- 11.2.5 Technician/PaperStatus
- 9.3.1 Operator Menu/ConsoleSettings
- 9.2.6 Operator Menu/Tickets & Totals/Annulment Options - Card Issue
- 9.2.2 Operator Menu/Tickets & Totals/Annulment Options - Card Top Up
- 9.2.4 Operator - Message of the Day
- 1.1.3 Sign On - PIN Entry
- 1.1.4 Sign On - PIN Entry - 4*
- 9.5.3 Operator Menu/Operator Options/Ticket History/Ticket
- 9.1 Operator Menu - inactive annul bus ticket
- 9.4.6 Operator Menu - Exccess Tickets- Value Exceeded
- 11.1.2 Soft Reboot - Please Wait...
- 9.5.1.1 Operator Menu/Tickets & Totals/Annulment - No Ticket - Error
- 9.6 Operator Menu/Report Faulty Device
- 9.6.3 Faulty Device Already Reported
- 1.2.2 Please Wait...
- 9.5.2 Word and Colour of the Day - Unavailable
- 9.4.3 Message of the Day - Unavailable
- 9.4.2 Operator Menu/SignOff Printer Error
- 9.4.1 Operator Menu/Tickets & Totals/Annulment Options - Confirmation
- 9.6.1 Operator Menu/Operator Information - Faulty Device
- 2.2 Main Screen-Rail selected
- 9.6.2 Main Screen-Ulsterbus selected - Faulty Device
- 9.5.1 Operator Menu/Tickets & Totals/Annulment Options - Error
- 1.3.1 Sign On - Incorrect Details

### Decision Points (14)
- Are there any transactions to annul?
- Correct Ticket Number entered?
- Is the device able to  print waybill?
- POS issues ticket and operator will return to Operator Menu
- Device already reported as faulty?
- Operator can go back to Operator Menu pressing Cancel.
- Operator can go back to Operator Menu pressing Back.
- Operator can go back to Operator Menu pressing Cancel.
- Are Word and Colour of the Day available?
- Is Message of the Day available?
- Operator can go to previous and next ticket screen using the up and down keys.
- 'Annul Current Rail Tickets' will be greyed out if there are no rail tickets issued on that POS in the current shift.
- Sign On Succesful?
- Annulment successful?

### Annotations / Spec Notes (56)
- Operator
- User is able to access Operator Menu, pressing the 'Wayfarer' button.
- User may press 'Wayfarer' button at any given time on the Main Screen and both Bus or Rail FLU screens.
- YES
- Example of Metro POS Operator Menu.
- NO
- Unless otherwise specified, the back button will take you back to the previous screen.
- Example of Metro POS Operator Options Menu.
- The 'Issue Refund' flow will be agreed between Flowbird and Translink following further analysis.
- Pressing the 'Barcode Reference Entry' key will take the user to the 'Barcode Scanning' flow.
- As per the CONOPs Flowbird were committed to provide a facility to reboot the card reader. As per email "POS CR Exchange" dated 20.07.20 12:36, this functionality has been exchanged, together with administrator mode commission card functionality, for CR034, the use of up and down arrows on the POS bus route selection screen and the addition of version screens in administrator mode.
- Pressing 'Annul Rail/Misc Tickets' will show a list with transaction from current shift. If a product is issued in euros then it is presented in euros on the annulment screen.
- Choosing 'Operator Options' will show a menu screen with specific options.
- Choosing a transaction will show full details and option to annul.
- Choosing Totals will display a list which will be available for printing.
- Pressing "Sign Off" will show user another screen that will require confirmation, before actually signing off.
- POS will print a waybill if confimed. Shift and day totals will appear on the waybill.
- Pressing "Break Mode" will show user another screen that will require confirmation, before actually going into break mode.
- The child flow will be the same as the Adult Excess Ticket flow.
- YES
- YES
- If on break for a configured amount of time, the user will be signed out
- After a certain amount of time has passed on any screen (apart from FLU), the POS enters breakmode.
- User will see a percentage for remaining paper and some average details. User will be able to print a test ticket and reverse paper feed.
- After signing off, the device will go automatically in idle mode.
- If Soft Reboot is chosen operator will have to press Confirm or Enter for rebooting the POS.
- Device will enter break mode and display a similar screen to idle mode.
- NO
- POS will display a list with tickets and transactions.
- NO
- If most recent transaction was a smartcard transaction, then it can be annulled.
- YES
- YES
- Reporting a faulty device means the Payment Device will no longer be available to use. An event will be sent to CloudFare to notify back end users of a Faulty Device.
- If on break for a configured amount of time, the user will be signed out
- If on break for a configured amount of time, the POS will be put in suspend mode.
- If a supervisor presents their card and enters a valid PIN then the Supervisor Menu is displayed and the current Operator is signed off. When the Supervisor signs off the Idle screen is displayed.
- If any of the following conditions have not been met then the "Annul Previous Transaction" option is not available:  - The previous transaction was a bus ticket that was issued within the last 60 seconds - The previous transaction was a smartcard transaction.
- Using L1-L5, operator can see details for the selected ticket/transaction.
- Operator presents card.
- NO
- NO
- Usr will be able to press any key to go back to the previous screen.
- Usr will be able to press any key to go back to the previous screen.
- User will be given the possibility to retry or to sign off anyway. Operator can retry indefinitely.
- If connection is slow, User might see a loading screen
- User will receive a confirmation screen and will be able to go back to operator menu, pressing any key.
- YES
- User will be return to the previous annulment screen pressing any key.
- YES
- An annulled ticket receipt will be printed showing which ticket has been annulled so that the operator can use this annulled receipt along with the original ticket issued to reconcile his cash takings.  If the transaction used a payment card then the card is automatically refunded and a payment card receipt is printed.
- NO
- If there is a faulty device, the Faulty Device icon is shown in the header.
- NO
- User will be return to the previous annulment screen pressing any key.
- User will be redirected to ID field active (if he tried to Sign On manually entering ID) or PIN field active accordingly (if he tried to Sign On automatically presenting Card) after 3 seconds or by pressing Enter button.

### Connections / Flow (75)
- Screen: "9.1.5 Operator Menu/BreakMode" → Screen: "9.2.3 Idle Screen - Driver on Break"
- Screen: "9.1.6 Operator Menu/Operator Information" → Screen: "9.3.1 Operator Menu/ConsoleSettings"
- Decision: "Is Message of the Day available?" → Screen: "9.2.4 Operator - Message of the Day"
- Decision: "Is the device able to 
print waybill?" → Screen: "1.0 Idle Screen"
- Decision: "Is Message of the Day available?" → Screen: "9.4.3 Message of the Day - Unavailable"
- Decision: "Are Word and Colour of the Day available?" → Screen: "9.5.2 Word and Colour of the Day - Unavailable"
- Screen: "1.2.2 Please Wait..." → Decision: "Sign On Succesful?"
- Screen: "1.1.3 Sign On - PIN Entry" → Screen: "1.1.4 Sign On - PIN Entry - 4*" [User enters Pin.]
- Screen: "9.0 Operator Menu" → Screen: "9.1.6 Operator Menu/Operator Information"
- Screen: "9.0 Operator Menu" → Screen: "9.1.5 Operator Menu/BreakMode"
- Decision: "Are Word and Colour of the Day available?" → Screen: "9.4.4 Operator - Word and Colour of the Day"
- Screen: "9.1.3 Operator Menu/SignOff" → Decision: "Is the device able to 
print waybill?"
- Screen: "9.0 Operator Menu" → Screen: "9.1.3 Operator Menu/SignOff"
- Screen: "9.1.6 Operator Menu/Operator Information" → Decision: "Are Word and Colour of the Day available?"
- Screen: "1.3.1 Sign On - Incorrect Details" → Screen: "1.1.3 Sign On - PIN Entry"
- Screen: "9.4.2 Operator Menu/SignOff Printer Error" → Screen: "1.0 Idle Screen"
- Decision: "Is the device able to 
print waybill?" → Screen: "9.4.2 Operator Menu/SignOff Printer Error"
- Decision: "Sign On Succesful?" → Screen: "1.3.1 Sign On - Incorrect Details" [If user enters a
wrong ID/Pin
he will be taken
to an Error screen.
]
- Decision: "Sign On Succesful?" → Screen: "2.2 Main Screen-Rail selected"
- Screen: "9.0 Operator Menu" → Screen: "9.1.2 Operator Menu/Totals"
- Screen: "1.1.4 Sign On - PIN Entry - 4*" → Screen: "1.2.2 Please Wait..."
- Screen: "9.2.3 Idle Screen - Driver on Break" → Screen: "1.1.3 Sign On - PIN Entry"
- Screen: "9.1.6 Operator Menu/Operator Information" → Decision: "Is Message of the Day available?"
- Decision: "Are there any transactions
to annul?" → Screen: "9.0 Operator Menu"
- Screen: "3.0 Main Screen-Rail-v4" → Decision: "Are there any transactions
to annul?"
- Screen: "2.5.2 Main Screen-Ulsterbus selected" → Decision: "Are there any transactions
to annul?"
- Screen: "2.2 Main Screen-Rail selected" → Decision: "Are there any transactions
to annul?"
- Screen: "9.1.6 Operator Menu/Operator Information" → Screen: "11.1.2 Soft Reboot - Confirm"
- Screen: "11.1.2 Soft Reboot - Please Wait..." → Screen: "9.2.3 Idle Screen - Driver on Break"
- Screen: "11.1.2 Soft Reboot - Confirm" → Screen: "9.1.6 Operator Menu/Operator Information"
- Screen: "9.0 Operator Menu" → Screen: "9.1.1 Operator Menu/Annul Rail/Misc Tickets"
- Screen: "9.0 Operator Menu" → Screen: "7.1.1 Smartcard/Please Present Smartcard"
- Screen: "7.1.1 Smartcard/Please Present Smartcard" → Screen: "9.2.2 Operator Menu/Tickets & Totals/Annulment Options - Card Top Up"
- Screen: "7.1.1 Smartcard/Please Present Smartcard" → Screen: "9.2.6 Operator Menu/Tickets & Totals/Annulment Options - Card Issue"
- Screen: "9.1.1 Operator Menu/Annul Rail/Misc Tickets" → Screen: "9.1.7 Operator Menu/Annul Previous Ticket entered"
- Screen: "9.1.7 Operator Menu/Annul Previous Ticket entered" → Decision: "Correct Ticket Number
entered?"
- Screen: "9.0 Operator Menu" → Screen: "9.2.1 Operator Menu/Tickets & Totals/Annul Previous Ticket"
- Decision: "Are there any transactions
to annul?" → Screen: "9.1 Operator Menu - inactive annul bus ticket"
- Screen: "9.2.6 Operator Menu/Tickets & Totals/Annulment Options - Card Issue" → Decision: "Annulment successful?"
- Screen: "9.2.2 Operator Menu/Tickets & Totals/Annulment Options - Card Top Up" → Decision: "Annulment successful?"
- Screen: "9.2.5 Operator Menu/Tickets & Totals/Annul Previous Ticket Rail" → Decision: "Annulment successful?"
- Screen: "9.2.1 Operator Menu/Tickets & Totals/Annul Previous Ticket" → Decision: "Annulment successful?"
- Screen: "9.1.6 Operator Menu/Operator Information" → Screen: "9.4.5 Operator Menu/Operator Options/Ticket History"
- Screen: "9.4.5 Operator Menu/Operator Options/Ticket History" → Screen: "9.5.3 Operator Menu/Operator Options/Ticket History/Ticket"
- Screen: "9.5.3 Operator Menu/Operator Options/Ticket History/Ticket" → Screen: "9.4.5 Operator Menu/Operator Options/Ticket History"
- Screen: "9.4.1 Operator Menu/Tickets & Totals/Annulment Options - Confirmation" → Screen: "9.0 Operator Menu"
- Screen: "9.4.5 Operator Menu/Operator Options/Ticket History" → Screen: "9.1.6 Operator Menu/Operator Information" [Pressing Back will return
to the previous screen]
- Screen: "9.1.6 Operator Menu/Operator Information" → Screen: "11.2.5 Technician/PaperStatus"
- Decision: "Annulment successful?" → Screen: "9.4.1 Operator Menu/Tickets & Totals/Annulment Options - Confirmation"
- Decision: "Annulment successful?" → Screen: "9.5.1 Operator Menu/Tickets & Totals/Annulment Options - Error"
- Screen: "9.2.5 Operator Menu/Tickets & Totals/Annul Previous Ticket Rail" → Decision: "Operator can go to previous and next ticket screen using the up and down keys."
- Screen: "9.2.5 Operator Menu/Tickets & Totals/Annul Previous Ticket Rail" → Screen: "9.1.7 Operator Menu/Annul Previous Ticket entered"
- Screen: "9.1.3 Operator Menu/SignOff" → Decision: "Operator can go back to Operator Menu pressing Cancel."
- Screen: "9.1.6 Operator Menu/Operator Information" → Decision: "Operator can go back to Operator Menu pressing Back."
- Screen: "9.1.5 Operator Menu/BreakMode" → Decision: "Operator can go back to Operator Menu pressing Cancel."
- Screen: "11.1.2 Soft Reboot - Confirm" → Screen: "11.1.2 Soft Reboot - Please Wait..."
- Screen: "11.1.2 Soft Reboot - Confirm" → Screen: "11.1.2 Soft Reboot - Please Wait..."
- Screen: "9.1 Operator Menu - inactive annul bus ticket" → Decision: "'Annul Current Rail Tickets' will be greyed out if there are no rail tickets issued on that POS in the current shift."
- Screen: "9.0 Operator Menu" → Screen: "9.1.8 Operator Menu - Exccess Tickets"
- Screen: "9.1.8 Operator Menu - Exccess Tickets" → Screen: "9.2.7 Operator Menu - Exccess Tickets- Enter Value"
- Screen: "9.2.7 Operator Menu - Exccess Tickets- Enter Value" → Screen: "9.2.8 Operator Menu - Exccess Tickets- Value Entered" [Oprators enters value]
- Screen: "9.2.7 Operator Menu - Exccess Tickets- Enter Value" → Screen: "9.1.8 Operator Menu - Exccess Tickets"
- Screen: "9.2.8 Operator Menu - Exccess Tickets- Value Entered" → Screen: "9.4.6 Operator Menu - Exccess Tickets- Value Exceeded" [Operators enters invalid value]
- Screen: "9.2.8 Operator Menu - Exccess Tickets- Value Entered" → Decision: "POS issues
ticket and
operator will
return to
Operator Menu"
- Decision: "Correct Ticket Number
entered?" → Screen: "9.2.5 Operator Menu/Tickets & Totals/Annul Previous Ticket Rail"
- Decision: "Correct Ticket Number
entered?" → Screen: "9.5.1.1 Operator Menu/Tickets & Totals/Annulment - No Ticket - Error"
- Screen: "9.5.1.1 Operator Menu/Tickets & Totals/Annulment - No Ticket - Error" → Screen: "9.1.7 Operator Menu/Annul Previous Ticket entered"
- Screen: "9.1.6 Operator Menu/Operator Information" → Decision: "Device already reported
as faulty?"
- Screen: "9.6.1 Operator Menu/Operator Information - Faulty Device" → Screen: "9.6.2 Main Screen-Ulsterbus selected - Faulty Device" [User navigates back to Main Screen.]
- Screen: "9.6.3 Faulty Device Already Reported" → Screen: "9.6.1 Operator Menu/Operator Information - Faulty Device" [Go back to Operator Menu which would
have the Faulty Device icon already.]
- Decision: "Device already reported
as faulty?" → Screen: "9.6 Operator Menu/Report Faulty Device" [No]
- Decision: "Device already reported
as faulty?" → Screen: "9.6.3 Faulty Device Already Reported" [Yes]
- Screen: "9.6 Operator Menu/Report Faulty Device" → Screen: "9.6.1 Operator Menu/Operator Information - Faulty Device" [User presses 'Confirm' key.]
- Screen: "9.2.3 Idle Screen - Driver on Break" → Decision: "7fb3f170-c492-4fce-a357-26dd28167e9d" [On break for configured amount of time]
- Decision: "ac96d55d-fb06-40ce-abe1-104d8446f9ba" → Screen: "9.2.3 Idle Screen - Driver on Break"


## 11. 10.0 Supervisor

### Screens (26)
- 1.0 Idle Screen
- 1.1.3 Sign On - PIN Entry
- 1.1.4 Sign On - PIN Entry - 4*
- 1.2.2 Please Wait...
- 1.1.1 Sign On - Empty Fields
- 1.1.2 Sign On - ID Entered
- 1.4.1 Sign On - Device Locked
- 10.0 Supervisor Menu
- 1.3.1 Sign On - Incorrect Details
- 10.1.6 Supervisor Menu/Force Comms
- 10.1.5 Supervisor Menu/Sale Breakdown
- 10.1.4 Supervisor Menu/Day Information
- 11.1.5 Technician/Versions
- 10.1.7 Supervisor/Sign Out
- 10.1.3 Supervisor Menu/Duty Information
- 10.2.2 Supervisor Menu/Duty Information - Page 2
- 10.2.3 Supervisor/Print&ZeroCurrent
- 10.2.4 Supervisor/Print&ZeroAccum
- 10.2.7 Supervisor Menu/Force Comms/Please Wait...
- 11.2.6 Technician/Versions/Configuration Versions
- 11.2.7 Technician/Versions/Software Versions
- 10.1.2 Supervisor Menu/Serial Numbers
- 10.2.2 Supervisor Menu/Duty Information - Details
- 10.2.5 Supervisor Menu/Duty Information - page2
- 10.3.1 Supervisor Menu/Duty Information/No Results
- 11.3.1 Technician/Versions/Configuration Versions Scroll

### Decision Points (6)
- Are the ID and PIN valid?
- Day Information is printed.
- Are there any duties to display?
- The up and down arrows allow to scroll if there are more than 4 duties in the one day.
- 'Press ▲ or ▼ to view more' will be available only when  the page is scrollable.
- Print Current Day/ Accumullated

### Annotations / Spec Notes (26)
- Supervisor
- Presenting an Supervisor card will redirect user to Sign on page with the ID automatically entered and PIN field active.
- Shown while the POS is performing sign on activities.
- Pressing any key will require to enter both ID and PIN to Sign On.
- User enters ID.
- User enters PIN.
- Yes
- User presses Enter.
- User presses Enter.
- Presenting an Supervisor card when a operator is signed in will automatically sign off the operator and unlock the device, if needed. After sign on, POS will display Supervisor Menu screen
- User is able to navigate to the specific items in the menu by pressing the corresponding button.
- Unless otherwise specified, the back button will take you back to the previous screen.
- No
- User will be redirected to ID field active (if he tried to Sign On manually entering ID) or PIN field active accordingly (if he tried to Sign On automatically presenting Card) after 3 seconds or by pressing Enter button.
- Selected any of the options will print the sales breakdown report.
- Day information details are displayed with an option to print. The duty numbers will be sequential and increase by 1 each duty.
- User is able to use the arrows buttons to scroll the list.
- Versions will show specific options.
- The ‘Print and Zero Totals’ and ‘Print and Zero Accummulated’ options will initially come up with a screen asking whether you really want to zero the totals after the print. If ‘Yes’ is selected, then the totals will be zeroed.  All printouts will contain the following information: - Operator number - POS number - Sign-on date and time - Sign-off date and time - No of tickets sold - Revenue collected - Miscellaneous revenue - No of smartcard validations - No of annulled tickets - First ticket number - Last ticket number - Individual detail (i.e. ticket type and prices) of all tickets and passes issued on that journey - Individual ticket numbers of any annulled tickets on that journey.
- Pressing the force comms button would trigger a check of the manifest in the back office and attempt to send audit files if they exist on the device. This would update the pending configuration files count and the pending audit files count. Refreshing the page will then update the count of these types of files to show how many of these items have been uploaded/downloaded.
- Yes
- User is able to select any of the duties by pressing corresponding button.
- User will be able to print the details presented in the specific screen.
- No
- After forcing communication, user will return to the updated Force Comms screen.
- Details will be displayed, with print option.

### Connections / Flow (43)
- Screen: "1.0 Idle Screen" → Screen: "1.1.1 Sign On - Empty Fields"
- Decision: "Are the ID and
PIN valid?" → Screen: "1.2.2 Please Wait..."
- Screen: "10.1.7 Supervisor/Sign Out" → Screen: "10.0 Supervisor Menu"
- Screen: "1.0 Idle Screen" → Screen: "1.1.3 Sign On - PIN Entry"
- Screen: "10.1.6 Supervisor Menu/Force Comms" → Screen: "10.2.7 Supervisor Menu/Force Comms/Please Wait..."
- Screen: "10.1.7 Supervisor/Sign Out" → Screen: "1.0 Idle Screen"
- Screen: "10.0 Supervisor Menu" → Screen: "10.1.5 Supervisor Menu/Sale Breakdown"
- Screen: "1.1.1 Sign On - Empty Fields" → Screen: "1.1.2 Sign On - ID Entered"
- Screen: "10.1.4 Supervisor Menu/Day Information" → Decision: "The up and down arrows allow to scroll if there are more than 4 duties in the one day."
- Screen: "10.0 Supervisor Menu" → Screen: "10.1.6 Supervisor Menu/Force Comms"
- Screen: "10.0 Supervisor Menu" → Screen: "10.1.4 Supervisor Menu/Day Information"
- Screen: "1.3.1 Sign On - Incorrect Details" → Screen: "1.1.1 Sign On - Empty Fields"
- Screen: "1.2.2 Please Wait..." → Screen: "10.0 Supervisor Menu"
- Screen: "10.1.3 Supervisor Menu/Duty Information" → Screen: "10.2.2 Supervisor Menu/Duty Information - Page 2"
- Screen: "10.2.2 Supervisor Menu/Duty Information - Details" → Screen: "10.2.2 Supervisor Menu/Duty Information - Page 2"
- Decision: "Are the ID and
PIN valid?" → Screen: "1.3.1 Sign On - Incorrect Details"
- Screen: "1.1.4 Sign On - PIN Entry - 4*" → Decision: "Are the ID and
PIN valid?"
- Screen: "10.0 Supervisor Menu" → Screen: "10.1.7 Supervisor/Sign Out"
- Decision: "Are there any duties
to display?" → Screen: "10.3.1 Supervisor Menu/Duty Information/No Results"
- Screen: "10.2.7 Supervisor Menu/Force Comms/Please Wait..." → Screen: "10.1.6 Supervisor Menu/Force Comms"
- Screen: "1.1.3 Sign On - PIN Entry" → Screen: "1.1.4 Sign On - PIN Entry - 4*"
- Screen: "10.2.2 Supervisor Menu/Duty Information - Page 2" → Screen: "10.2.2 Supervisor Menu/Duty Information - Details"
- Screen: "10.1.6 Supervisor Menu/Force Comms" → Screen: "10.2.7 Supervisor Menu/Force Comms/Please Wait..."
- Screen: "10.0 Supervisor Menu" → Decision: "Are there any duties
to display?"
- Screen: "10.2.2 Supervisor Menu/Duty Information - Page 2" → Decision: "'Press ▲ or ▼ to view more'
will be available only when 
the page is scrollable."
- Decision: "Are there any duties
to display?" → Screen: "10.1.3 Supervisor Menu/Duty Information"
- Screen: "1.1.2 Sign On - ID Entered" → Screen: "1.1.3 Sign On - PIN Entry"
- Screen: "1.4.1 Sign On - Device Locked" → Screen: "1.1.3 Sign On - PIN Entry"
- Screen: "10.1.5 Supervisor Menu/Sale Breakdown" → Screen: "10.2.3 Supervisor/Print&ZeroCurrent"
- Screen: "10.1.5 Supervisor Menu/Sale Breakdown" → Screen: "10.2.4 Supervisor/Print&ZeroAccum"
- Screen: "10.2.3 Supervisor/Print&ZeroCurrent" → Decision: "Print Current Day/
Accumullated"
- Screen: "10.2.4 Supervisor/Print&ZeroAccum" → Decision: "Print Current Day/
Accumullated"
- Decision: "Print Current Day/
Accumullated" → Screen: "10.1.5 Supervisor Menu/Sale Breakdown" [After printing POS will return to Sales Breakdown screen]
- Screen: "10.2.3 Supervisor/Print&ZeroCurrent" → Screen: "10.1.5 Supervisor Menu/Sale Breakdown"
- Screen: "11.1.5 Technician/Versions" → Screen: "11.2.6 Technician/Versions/Configuration Versions"
- Screen: "11.1.5 Technician/Versions" → Screen: "11.2.7 Technician/Versions/Software Versions"
- Screen: "11.2.6 Technician/Versions/Configuration Versions" → Screen: "11.3.1 Technician/Versions/Configuration Versions Scroll"
- Screen: "11.2.7 Technician/Versions/Software Versions" → Screen: "11.1.5 Technician/Versions"
- Screen: "10.0 Supervisor Menu" → Screen: "11.1.5 Technician/Versions"
- Screen: "10.1.4 Supervisor Menu/Day Information" → Decision: "Day Information
is printed."
- Screen: "10.2.2 Supervisor Menu/Duty Information - Details" → Screen: "10.2.5 Supervisor Menu/Duty Information - page2"
- Screen: "10.2.5 Supervisor Menu/Duty Information - page2" → Screen: "10.2.2 Supervisor Menu/Duty Information - Details"
- Screen: "11.1.5 Technician/Versions" → Screen: "10.1.2 Supervisor Menu/Serial Numbers"


## 12. 11.0 Technician

### Screens (34)
- 1.0 Idle Screen
- 1.1.4 Sign On - PIN Entry - 4*
- 1.2.2 Please Wait...
- 1.1.3 Sign On - PIN Entry
- 1.1.1 Sign On - Empty Fields
- 1.1.2 Sign On - ID Entered
- 11.0 Technician Menu
- 1.2.1 Communications Locked
- 1.3.1 Sign On - Incorrect Details
- 11.1.2 Soft Reboot - Confirm
- 11.1.4 Technician/Device Status
- 11.1.1.2 Technician/Device Settings - Summary
- 10.1.7 Supervisor/Sign Out
- 11.1.6 Supervisor Menu/Force Comms
- 11.1.5 Technician/Versions
- 11.1.8 Technician/Network Settings
- 9.3.1 Operator Menu/ConsoleSettings
- 11.2.4 Technician/Card Reader
- 11.2.3 Technician/Other Devices
- 11.1.2 Soft Reboot - Please Wait...
- 11.2.5 Technician/PaperStatus
- 11.2.6 Technician/Versions/Configuration Versions
- 11.2.7 Technician/Versions/Software Versions
- 11.2.8 Technician/Serial Numbers
- 11.2.10 Technician/Network Settings/Cell Modem
- 11.2.9 Force Comms - Please Wait...
- 11.2.11 Technician/Device Settings/POS Operating Company
- 1.0 Idle Screen
- 7.3.9 Smartcard/iLink/Mini Statement
- 11.3.1 Technician/Versions/Configuration Versions Scroll
- 11.2.1 Technician/Device Settings/Home Location
- 12.5.1 Administrator Mode/Device Settings/Boarding Location
- 12.6.3 Administrator Mode/Device Settings/Mounting Point/Active
- 11.1.1.2 Technician/Device Settings - Changes

### Decision Points (3)
- Are the ID and PIN valid?
- These settings will be configured in the back office via TMS
- The maintenance app will be capable of adjusting these settings and will be accessible from the technician mode. This will be provided at a later date.

### Annotations / Spec Notes (38)
- Technician
- Presenting an Technician card will redirect user to Sign on page with the ID automatically entered and PIN field active.
- Pressing any key will require to enter both ID and PIN to Sign On.
- Shown while the POS is performing sign on activities.
- User enters ID.
- User enters PIN.
- Yes
- User presses Enter.
- User presses Enter.
- User is able to navigate to the specific items in the menu by pressing the corresponding button.
- Unless otherwise specified, the back button will take you back to the previous screen.
- No
- Device will be configured to connect to Ethernet if available and fall back to cellular if not. User can see whether Ethernet is connected or not. If it is then that is the communications method that will be used. If it's not then it will be cellular.
- User will be redirected to ID field active (if he tried to Sign On manually entering ID) or PIN field active accordingly (if he tried to Sign On automatically presenting Card) after 3 seconds or by pressing Enter button.
- Pressing "Sign Off" will show user another screen that will require confirmation, before actually signing off.
- User will be able to incrementaly set brightness and volume and restore defaults.
- A information screen will be displayed.
- Device Status will show specific options.
- Versions will show specific options.
- Pressing the force comms button would trigger a check of the manifest in the back office and attempt to send audit files if they exist on the device. This would update the pending configuration files count and the pending audit files count. Refreshing the page will then update the count of these types of files to show how many of these items have been uploaded/downloaded.
- If the Device cannot establish a correct Communication it will become locked and present a screen with an Error Message and "Please Notify a Supervisor or Technician".
- Choosing Device Settings will show a menu page.
- User will be able to see which devices are currently connected or were previously connected.  The fields on this screen don't update automatically so would need a refresh. Either refresh or go back (has the same effect).  This will list devices such as:- - Payment Card Reader - Barcode Reader - Customer Information Display
- Shown while the POS is performing Soft Reboot activities.
- User will be able to test cards, a card status page will be displayed.
- User will see a percentage for remaining paper and some average details. User will be able to print a test ticket and reverse paper feed.
- Pressing refresh will retrieve information from the server and update information to the latest values.
- User will be able to print the details presented in the specific screen.
- Other diagnostic information will appear on this screen depending on what is available from the interface.
- Page displays the current configuration for the device.  A confirmation button will only be available when a change has been made.
- After forcing communication, user will return to the updated Force Comms screen.
- If the smartcard test is successful POS will show a ministatement.
- After reboot, Idle screen will be presented.
- Selecting an option will navigate back to the previous screen with the field updated.  Pressing 'Back' or 'C' will return with no updates to the fields.
- Locations will be available as a list and user will be able to see next or previous 10 locations using the arrow buttons.
- Pressing the 'Enter' key will take the user back to the 'Device Settings' screen with the Default Location updated according to the selection and pending confirmation.  Pressing 'C' will take the user back with no proposed changes.
- When the field is highlighted the number keys can be pressed to enter a numerical value.  Selecting 'Back' deselect the field and the previous setting will not be changed.  Pressing 'C' will delete characters.  (Note: The same behaviour occurs with TrayID)
- When changes have been made that need to be confirmed the relevant fields will be highlighted and the 'Confirm' button will be available.   Selecting 'Back' will cancel all proposed changes.  Selecting 'Confirm' will trigger a device reboot.

### Connections / Flow (47)
- Screen: "1.0 Idle Screen" → Screen: "1.1.3 Sign On - PIN Entry"
- Screen: "11.1.4 Technician/Device Status" → Screen: "11.2.3 Technician/Other Devices"
- Screen: "11.0 Technician Menu" → Screen: "11.1.8 Technician/Network Settings"
- Screen: "1.2.2 Please Wait..." → Screen: "11.0 Technician Menu"
- Decision: "Are the ID and
PIN valid?" → Screen: "1.2.2 Please Wait..."
- Screen: "11.0 Technician Menu" → Screen: "11.1.1.2 Technician/Device Settings - Summary"
- Screen: "11.0 Technician Menu" → Screen: "11.1.4 Technician/Device Status"
- Screen: "11.0 Technician Menu" → Screen: "10.1.7 Supervisor/Sign Out"
- Screen: "1.1.4 Sign On - PIN Entry - 4*" → Decision: "Are the ID and
PIN valid?"
- Screen: "1.0 Idle Screen" → Screen: "1.1.1 Sign On - Empty Fields"
- Screen: "11.1.6 Supervisor Menu/Force Comms" → Screen: "11.2.9 Force Comms - Please Wait..."
- Screen: "11.1.5 Technician/Versions" → Screen: "11.2.6 Technician/Versions/Configuration Versions"
- Screen: "11.1.4 Technician/Device Status" → Screen: "11.2.5 Technician/PaperStatus"
- Screen: "11.1.5 Technician/Versions" → Screen: "11.2.7 Technician/Versions/Software Versions"
- Screen: "10.1.7 Supervisor/Sign Out" → Screen: "1.0 Idle Screen"
- Screen: "1.3.1 Sign On - Incorrect Details" → Screen: "1.1.1 Sign On - Empty Fields"
- Decision: "Are the ID and
PIN valid?" → Screen: "1.3.1 Sign On - Incorrect Details"
- Screen: "11.1.8 Technician/Network Settings" → Screen: "11.2.10 Technician/Network Settings/Cell Modem"
- Screen: "11.1.5 Technician/Versions" → Screen: "11.2.8 Technician/Serial Numbers"
- Screen: "11.0 Technician Menu" → Screen: "11.1.5 Technician/Versions"
- Screen: "11.1.6 Supervisor Menu/Force Comms" → Screen: "11.2.9 Force Comms - Please Wait..."
- Screen: "11.0 Technician Menu" → Screen: "11.1.2 Soft Reboot - Confirm"
- Screen: "11.2.9 Force Comms - Please Wait..." → Screen: "11.1.6 Supervisor Menu/Force Comms"
- Screen: "11.0 Technician Menu" → Screen: "11.1.6 Supervisor Menu/Force Comms"
- Screen: "11.1.4 Technician/Device Status" → Screen: "11.2.4 Technician/Card Reader"
- Screen: "11.0 Technician Menu" → Screen: "9.3.1 Operator Menu/ConsoleSettings"
- Screen: "1.0 Idle Screen" → Screen: "1.2.1 Communications Locked"
- Screen: "1.1.1 Sign On - Empty Fields" → Screen: "1.1.2 Sign On - ID Entered"
- Screen: "11.2.6 Technician/Versions/Configuration Versions" → Screen: "11.3.1 Technician/Versions/Configuration Versions Scroll"
- Screen: "11.2.7 Technician/Versions/Software Versions" → Screen: "11.1.5 Technician/Versions"
- Screen: "11.2.4 Technician/Card Reader" → Screen: "7.3.9 Smartcard/iLink/Mini Statement" [Test Successful]
- Screen: "7.3.9 Smartcard/iLink/Mini Statement" → Screen: "11.2.4 Technician/Card Reader"
- Screen: "11.2.1 Technician/Device Settings/Home Location" → Screen: "11.1.1.2 Technician/Device Settings - Summary"
- Screen: "11.1.1.2 Technician/Device Settings - Summary" → Screen: "11.0 Technician Menu"
- Screen: "11.2.3 Technician/Other Devices" → Screen: "11.1.4 Technician/Device Status"
- Screen: "11.1.2 Soft Reboot - Please Wait..." → Screen: "1.0 Idle Screen"
- Screen: "11.1.2 Soft Reboot - Confirm" → Screen: "11.1.2 Soft Reboot - Please Wait..."
- Screen: "10.1.7 Supervisor/Sign Out" → Screen: "1.0 Idle Screen"
- Screen: "11.1.2 Soft Reboot - Confirm" → Screen: "11.1.2 Soft Reboot - Please Wait..."
- Screen: "1.1.2 Sign On - ID Entered" → Screen: "1.1.3 Sign On - PIN Entry"
- Screen: "1.1.3 Sign On - PIN Entry" → Screen: "1.1.4 Sign On - PIN Entry - 4*"
- Screen: "11.1.1.2 Technician/Device Settings - Summary" → Screen: "11.2.11 Technician/Device Settings/POS Operating Company"
- Screen: "11.1.1.2 Technician/Device Settings - Summary" → Screen: "11.2.1 Technician/Device Settings/Home Location"
- Screen: "11.1.1.2 Technician/Device Settings - Summary" → Screen: "12.5.1 Administrator Mode/Device Settings/Boarding Location"
- Screen: "11.2.11 Technician/Device Settings/POS Operating Company" → Screen: "11.1.1.2 Technician/Device Settings - Summary"
- Screen: "12.6.3 Administrator Mode/Device Settings/Mounting Point/Active" → Screen: "11.1.1.2 Technician/Device Settings - Changes"
- Screen: "11.1.1.2 Technician/Device Settings - Summary" → Screen: "12.6.3 Administrator Mode/Device Settings/Mounting Point/Active"


## 13. 12.0 Administrator

### Screens (32)
- 1.0 Idle Screen
- 1.1.3 Sign On - PIN Entry
- 1.1.4 Sign On - PIN Entry - 4*
- 1.2.2 Please Wait...
- 1.1.1 Sign On - Empty Fields
- 1.1.2 Sign On - ID Entered
- 12.0 Administrator Mode Menu
- 1.2.1 Communications Locked
- 1.3.1 Sign On - Incorrect Details
- 12.2 Administrator Mode/Please Present Smartcard
- 12.5 Administrator Mode/Device Settings
- 12.1 Administrator Mode/Force Comms
- 12.1.1 Administrator Mode/Network Settings
- 12.2 Administrator Mode/Please Present Smartcard
- 11.1.5 Technician/Versions
- 11.2.1 Technician/Device Settings/Home Location
- 11.2.2 Technician/Device Settings/Tray ID
- 12.5.1 Administrator Mode/Device Settings/Boarding Location
- 12.5.2 Administrator Mode/Device Settings/Mounting Point
- 11.2.10 Technician/Network Settings/Cell Modem
- 11.2.6 Technician/Versions/Configuration Versions
- 11.2.7 Technician/Versions/Software Versions
- 11.2.8 Technician/Serial Numbers
- 12.3 Clear Card - Confirm
- 12.2.1 Please Wait - Reading Card
- 12.2.3 Please Wait - Sending Data
- 11.2.2 Technician/Device Settings/Tray ID - Letters
- 12.6.1 Administrator Mode/Device Settings/Mounting Point/Letters
- 12.2.2.3 Administrator Mode/Card Cleared Success
- 12.2.2.2 Administrator Mode/Card Download Success
- 12.2.2 Administrator Mode/Card Fail
- 12.2.2 Administrator Mode/Card Fail

### Decision Points (4)
- Are the ID and PIN valid?
- Card clear success?
- Data download success?
- The maintenance app will be capable of adjusting these settings and will be accessible from the technician mode. This will be provided at a later date.

### Annotations / Spec Notes (33)
- Administrator
- Presenting an Administrator card will redirect user to Sign on page with the ID automatically entered and PIN field active.
- Pressing any key will require to enter both ID and PIN to Sign On.
- Shown while the POS is performing sign on activities.
- User enters ID.
- User enters PIN.
- Yes
- User presses Enter.
- User presses Enter.
- No
- User will be redirected to ID field active (if he tried to Sign On manually entering ID) or PIN field active accordingly (if he tried to Sign On automatically presenting Card) after 3 seconds or by pressing Enter button.
- 'Versions' screens and flow will match Technician menu, hen ce the screen names being 'Technician'.
- Translink no longer require the feature to commission a smartcard on the POS. As per email "POS CR Exchange" dated 20.07.20 12:36, this functionality has been exchanged, together with POS card reader reboot requirement removal, for CR034, the use of up and down arrows on the POS bus route selection screen and the addition of version screens in administrator mode.
- If the Device cannot establish a correct Communication it will become locked and present a screen with an Error Message and "Please Notify a Supervisor or Technician".
- Other diagnostic information will appear on this screen depending on what is available from the interface.
- User will be able to print the details presented in the specific screen.
- Pressing the 'Back' key will take the user to the 'Establish Comms' screen.
- Pressing the 'Back' key will take the user to the 'Establish Comms' screen.
- Pressing the 'Back' key will take the user to the Admin menu.
- Pressing the 'Back' key will take the user to the Admin menu.
- Pressing the 'Back' key will take the user to the Admin menu.
- Pressing the 'Enter' key will take the user back to the 'Device Settings' screen.
- Pressing the 'Enter' key will take the user back to the 'Device Settings' screen.
- The card data is sent directly to the back office.
- Pressing the 'Back' key will take the user to the 'Device Settings' screen.  Pressing the 'Enter' key will take the user back to the 'Device Settings' screen.
- Pressing the 'Back' key will take the user to the 'Device Settings' screen.  Pressing one of the Location keys will take the user back to the 'Device Settings' screen.  It will be possible to distinguish between locations that have the same name but a different mode. The mechanism to achieve this will be explained at a later date.
- if a boarding location has already been configured then when the page is loaded the currently configured boarding location will be prepopulated
- Pressing the 'Cancel' key will take the user to the Admin menu.
- Pressing the '*' key will take the user to the 'Tray ID' screen.  Pressing the 'Enter' key will take the user back to the 'Device Settings' screen.
- If the Clear Card attempt is successful, the user will have to remove the smartcard to be returned to the Admin menu.
- If the Card Dump data is successful in downloading, the user will be returned to the Admin menu after removing the smartcard.
- If the Card Dump data is unsuccessful in downloading, the user will be able to retry - this will take the user to the 'Please Wait - Downloading' screen above, or return to the Admin menu.
- If the Clear Card attempt is unsuccessful, the user will be able to retry - this will take them to the 'Clear Card' screen as long as the card has not been removed, or return to the Admin menu.

### Connections / Flow (38)
- Screen: "12.0 Administrator Mode Menu" → Screen: "12.2 Administrator Mode/Please Present Smartcard" ['Card Dump' key pressed.]
- Screen: "12.0 Administrator Mode Menu" → Screen: "12.2 Administrator Mode/Please Present Smartcard" ['Clear Card' key pressed.]
- Screen: "12.0 Administrator Mode Menu" → Screen: "12.1.1 Administrator Mode/Network Settings" ['Network Settings' key pressed.]
- Decision: "Data download success?" → Screen: "12.2.2.2 Administrator Mode/Card Download Success" [Data downloaded successfully.]
- Decision: "Data download success?" → Screen: "12.2.2 Administrator Mode/Card Fail" [Data downloaded unsuccessfully.]
- Decision: "Card clear success?" → Screen: "12.2.2.3 Administrator Mode/Card Cleared Success" [Card clear success.]
- Decision: "Card clear success?" → Screen: "12.2.2 Administrator Mode/Card Fail" [Card clear unsuccessful.]
- Screen: "12.3 Clear Card - Confirm" → Decision: "Card clear success?" [Attempt to clear the card...]
- Screen: "12.2 Administrator Mode/Please Present Smartcard" → Screen: "12.3 Clear Card - Confirm" [User presents a card...]
- Screen: "12.0 Administrator Mode Menu" → Screen: "12.1 Administrator Mode/Force Comms" ['Force Comms' key pressed.]
- Screen: "12.5 Administrator Mode/Device Settings" → Screen: "11.2.1 Technician/Device Settings/Home Location" ['Home Location' key pressed.]
- Screen: "12.5 Administrator Mode/Device Settings" → Screen: "11.2.2 Technician/Device Settings/Tray ID" ['Tray ID' key pressed.]
- Screen: "12.5 Administrator Mode/Device Settings" → Screen: "12.5.2 Administrator Mode/Device Settings/Mounting Point" ['Mounting Point' key pressed.]
- Screen: "12.2.1 Please Wait - Reading Card" → Screen: "12.2.3 Please Wait - Sending Data"
- Screen: "12.2 Administrator Mode/Please Present Smartcard" → Screen: "12.2.1 Please Wait - Reading Card" [Smartcard presented.]
- Screen: "12.2.3 Please Wait - Sending Data" → Decision: "Data download success?" [Check to see if card dump data has
transmited successfully...]
- Screen: "12.5.2 Administrator Mode/Device Settings/Mounting Point" → Screen: "12.6.1 Administrator Mode/Device Settings/Mounting Point/Letters"
- Screen: "12.6.1 Administrator Mode/Device Settings/Mounting Point/Letters" → Screen: "12.5.2 Administrator Mode/Device Settings/Mounting Point"
- Screen: "12.1.1 Administrator Mode/Network Settings" → Screen: "11.2.10 Technician/Network Settings/Cell Modem"
- Screen: "1.0 Idle Screen" → Screen: "1.1.3 Sign On - PIN Entry"
- Decision: "Are the ID and
PIN valid?" → Screen: "1.2.2 Please Wait..."
- Screen: "1.1.4 Sign On - PIN Entry - 4*" → Decision: "Are the ID and
PIN valid?"
- Screen: "1.0 Idle Screen" → Screen: "1.1.1 Sign On - Empty Fields"
- Screen: "1.3.1 Sign On - Incorrect Details" → Screen: "1.1.1 Sign On - Empty Fields"
- Decision: "Are the ID and
PIN valid?" → Screen: "1.3.1 Sign On - Incorrect Details"
- Screen: "1.1.3 Sign On - PIN Entry" → Screen: "1.1.4 Sign On - PIN Entry - 4*"
- Screen: "1.0 Idle Screen" → Screen: "1.2.1 Communications Locked"
- Screen: "1.1.1 Sign On - Empty Fields" → Screen: "1.1.2 Sign On - ID Entered"
- Screen: "1.1.2 Sign On - ID Entered" → Screen: "1.1.3 Sign On - PIN Entry"
- Screen: "1.2.2 Please Wait..." → Screen: "12.0 Administrator Mode Menu"
- Screen: "11.1.5 Technician/Versions" → Screen: "11.2.6 Technician/Versions/Configuration Versions"
- Screen: "11.1.5 Technician/Versions" → Screen: "11.2.7 Technician/Versions/Software Versions"
- Screen: "11.1.5 Technician/Versions" → Screen: "11.2.8 Technician/Serial Numbers"
- Screen: "11.2.7 Technician/Versions/Software Versions" → Screen: "11.1.5 Technician/Versions"
- Screen: "12.0 Administrator Mode Menu" → Screen: "11.1.5 Technician/Versions" ['Versions' key pressed.]
- Screen: "12.0 Administrator Mode Menu" → Screen: "12.5 Administrator Mode/Device Settings" ['Device Settings' key pressed.]
- Screen: "12.5 Administrator Mode/Device Settings" → Screen: "12.5.1 Administrator Mode/Device Settings/Boarding Location" ['Boarding Location' key pressed.]
- Screen: "11.2.2 Technician/Device Settings/Tray ID" → Screen: "11.2.2 Technician/Device Settings/Tray ID - Letters" ['*' key pressed to show letters.]


## 14. 13.0 Customer Displays

### Screens (9)
- 13.1 Customer Display - Out of Service
- 13.3 Customer Display - See Operator
- 13.6 Customer Display - Transaction Summary
- 13.5 Customer Display - Transaction Summary - Multiple
- 13.7 Customer Display - Transaction Complete
- 13.2 Customer Display - Please Wait
- 13.2.1 Customer Display - FLU
- 13.4.1 Customer Display - FLU Selection
- 13.8 Customer Display - Transaction Declined

### Decision Points (9)
- On entry to Main FLU you would see 13.2.1. Going to Bus or Rail FLU you would then see 13.4.1. Going to basket or Payment you would see 13.5 or 13.6 and then after payment you would see 13.7 (or 13.8 if the transaction is declined).  With the chosen Customer Display for the POS device the LED's indicated in these screens do not exist.
- "Out of Service": 'Idle', 'Driver Break', 'Technician', 'Supervisor' and 'Administrator' Menu screens.
- "See Operator": A situation where the passenger needs to talk to the operator (e.g. an expired card was presented).
- "Transaction Summary": If only one item is being purchased, it will show the item name, otherwise 'Multiple Items' will be shown instead.  Transaction type examples could be 'Ticket Issue', 'Top Up', 'Card Issue', 'Miscellaneous'.
- "Transaction Complete": Displays when a transaction is completed.
- "Please Wait": Any 'Sign On' page and any 'Operator Menu' page.
- "FLU": Any 'FLU' page.
- Once the placeholder items are selected on Bus and Rail FLU respectively, the items will fill in.
- "Transaction Declined": Any situation where a payment card transaction has failed.

### Annotations / Spec Notes (1)
- Customer Displays

### Connections / Flow (0)


## 15. 14.0 Barcode Scanning

### Screens (19)
- 2.5.2 Main Screen-Ulsterbus selected
- Barcode - Validating Details
- Barcode Scan - Ticket Valid inc. Date and Depart Time
- Barcode Ticket - Printed?
- Barcode Validation Failed
- Barcode Scan - Transaction Cancelled - Ticket Not Valid
- Barcode Scan - Transaction Cancelled - Ticket Not Valid
- Barcode Scan - Transaction Cancelled - Ticket Not Passed Visual Inspection
- Barcode Ticket - Print Error
- Barcode Validation Failed
- Barcode - Offline Check
- Barcode Validation Failed
- 9.0 Operator Menu
- Barcode Scan - Ticket Valid inc. 3 Use Times
- Barcode Scan - Ticket Valid inc. Date with Expiry and Depart Time
- Barcode Scan - Ticket Valid inc. Outbound ands Return
- Barcode Scan - Ticket Valid inc. Outbound ands Return - Page 2
- Barcode Reference
- Barcode Reference Entered

### Decision Points (35)
- Barcode data successfully retrieved?
- POS attempts to print ticket
- Barcode has been validated. Back to the FLU screen.
- Print successful?
- Decryption and parsing  successful?
- Is the barcode already offline validated?
- Online check available?
- Online?
- Valid barcode?
- Passed additional background checks?
- Barcode still valid. Back to the print check.
- If this is the first time this button has been pressed for the current barcode then it will attempt to reprint the ticket, audit the retry with Corethree and CloudFare and go back to the 'Print Successful?' check. If this is the second time this button has been pressed for the current barcode then it will return to the FLU screen and the barcode will no longer be valid.
- POS attempts to print ticket & Stores offline validation in the background
- This will state 'The ticket has already been offline validated'
- This will state 'The ticket is not valid' 'The ticket has already been used' 'The ticket is not valid on this date' 'The ticket has expired'
- This will state: 'Additional validation failed'
- This will state 'Barcode Decryption has failed'
- This will take the user to the 'Barcode Reference' screen seen in the 'Accessing Barcode Ref. via Operator Menu' flow below.
- This will take the user to the 'Barcode Reference' screen seen in the 'Accessing Barcode Ref. via Operator Menu' flow below.
- Go to 'Valid Barcode?' decision point.
- The flow will go back to the 'Print Successful' decision point.  A reprint will be be audited with Corethree as well.
- Back to 'Validating Ticket Details' check.
- Back to 'Validating Ticket Details' check.
- Ticket value less than or equal to the configurable limit & product is valid?
- Back to 'Validating Ticket Details' check.
- Back to 'Validating Ticket Details' check.
- If a barcode fails, it will not mark the barcode as redeemed in CoreThree.
- If a barcode fails, it will not mark the barcode as redeemed in CoreThree.
- If a barcode fails, it will not mark the barcode as redeemed in CoreThree.
- This will state 'The ticket is not valid' 'The ticket has already been used' 'The ticket is not valid on this date' 'The ticket has expired' 'The ticket value exceeds offline validation limit'
- This will take the user to the 'Barcode Reference' screen seen in the 'Accessing Barcode Ref. via Operator Menu' flow below.
- Back to 'Barcode - Validating Details' check.
- If the bacode number on the receipt is unreadable, operator may press Cancel key and go back to FLU screen.  Pressing the 'C' key will clear an entered number 1 digit at a time.
- Go to 'Barcode - Validating Details' check
- There is an upper limit of 12 characters for the 'Barcode Reference' field.

### Annotations / Spec Notes (26)
- Barcode Scan Validation
- The ticket will be visually checked by the operator.  All the necessary information for each type depending on which barcode type has been scanned.
- Yes
- No
- Yes
- No
- Yes
- Yes
- Yes
- Yes
- Yes
- Barcodes that have been validated offline will be stored in a list until a connection with Cloudfare and Corethree is re-established?
- No
- Yes
- No
- No
- No
- No
- No
- Yes
- Operator can navigate to the Barcode Reference Entry option on the Operator Menu. See 'Accessing Barcode Ref. via Operator Menu' below.
- No
- User may press any key to go back to FLU screen or timeout of 3 seconds.
- Accessing Barcode Ref. via Operator Menu
- Ticket Validation Screen Examples
- On this particular barcode type there can be Notes as well.

### Connections / Flow (50)
- Screen: "2.5.2 Main Screen-Ulsterbus selected" → Decision: "Barcode data
successfully
retrieved?" [The barcode has been
scanned by the reader...]
- Screen: "Barcode - Validating Details" → Decision: "Decryption
and parsing 
successful?"
- Decision: "Decryption
and parsing 
successful?" → Screen: "Barcode Validation Failed"
- Screen: "Barcode Validation Failed" → Decision: "Back to 'Validating Ticket Details' check."
- Decision: "Decryption
and parsing 
successful?" → Decision: "Is the barcode
already offline
validated?"
- Screen: "Barcode Validation Failed" → Screen: "2.5.2 Main Screen-Ulsterbus selected" [Back to FLU screen]
- Screen: "Barcode Validation Failed" → Decision: "Back to 'Validating Ticket Details' check."
- Decision: "Is the barcode
already offline
validated?" → Screen: "Barcode Validation Failed"
- Decision: "Is the barcode
already offline
validated?" → Decision: "Online check
available?"
- Decision: "Online check
available?" → Screen: "Barcode - Offline Check"
- Decision: "Online check
available?" → Decision: "Valid barcode?"
- Screen: "Barcode - Offline Check" → Decision: "Ticket
value less
than or equal to the configurable limit
& product is
valid?"
- Decision: "Ticket
value less
than or equal to the configurable limit
& product is
valid?" → Decision: "Go to 'Valid Barcode?' decision point."
- Screen: "Barcode Validation Failed" → Screen: "2.5.2 Main Screen-Ulsterbus selected"
- Screen: "Barcode Validation Failed" → Decision: "Back to 'Barcode - Validating Details' check."
- Decision: "Ticket
value less
than or equal to the configurable limit
& product is
valid?" → Screen: "Barcode Validation Failed"
- Screen: "Barcode Validation Failed" → Screen: "2.5.2 Main Screen-Ulsterbus selected"
- Decision: "Valid barcode?" → Screen: "Barcode Scan - Transaction Cancelled - Ticket Not Valid"
- Screen: "Barcode Scan - Transaction Cancelled - Ticket Not Valid" → Decision: "Back to 'Validating Ticket Details' check."
- Screen: "Barcode Scan - Transaction Cancelled - Ticket Not Valid" → Screen: "2.5.2 Main Screen-Ulsterbus selected"
- Decision: "Valid barcode?" → Decision: "Passed additional background checks?"
- Decision: "Passed additional background checks?" → Screen: "Barcode Scan - Transaction Cancelled - Ticket Not Valid"
- Decision: "Passed additional background checks?" → Screen: "Barcode Scan - Ticket Valid inc. Date and Depart Time"
- Screen: "Barcode Scan - Transaction Cancelled - Ticket Not Valid" → Decision: "Back to 'Validating Ticket Details' check."
- Screen: "Barcode Scan - Ticket Valid inc. Date and Depart Time" → Screen: "Barcode Scan - Transaction Cancelled - Ticket Not Passed Visual Inspection"
- Screen: "Barcode Scan - Transaction Cancelled - Ticket Not Valid" → Screen: "2.5.2 Main Screen-Ulsterbus selected"
- Screen: "Barcode Scan - Transaction Cancelled - Ticket Not Passed Visual Inspection" → Screen: "2.5.2 Main Screen-Ulsterbus selected"
- Screen: "Barcode Scan - Ticket Valid inc. Date and Depart Time" → Decision: "Online?"
- Decision: "Online?" → Decision: "POS attempts to print ticket"
- Decision: "Online?" → Decision: "POS attempts to print ticket & Stores offline validation in the background"
- Decision: "POS attempts to print ticket" → Decision: "Print successful?"
- Decision: "POS attempts to print ticket & Stores offline validation in the background" → Decision: "Print successful?"
- Decision: "Print successful?" → Screen: "Barcode Ticket - Print Error"
- Screen: "Barcode Ticket - Print Error" → Decision: "The flow will go back to the 'Print Successful' decision point.

A reprint will be be audited with Corethree as well."
- Screen: "Barcode Ticket - Print Error" → Screen: "2.5.2 Main Screen-Ulsterbus selected"
- Decision: "Print successful?" → Screen: "Barcode Ticket - Printed?"
- Screen: "Barcode Ticket - Printed?" → Decision: "Barcode has been validated. Back to the FLU screen."
- Screen: "Barcode Ticket - Printed?" → Decision: "Barcode still valid. Back to the print check."
- Decision: "Barcode has been validated. Back to the FLU screen." → Screen: "2.5.2 Main Screen-Ulsterbus selected"
- Screen: "9.0 Operator Menu" → Screen: "Barcode Reference"
- Screen: "Barcode Reference" → Screen: "Barcode Reference Entered" [Operator enters
barcode reference 
number.]
- Screen: "Barcode Reference" → Decision: "If the bacode number on the receipt is unreadable, operator may press Cancel key and go back to FLU screen.

Pressing the 'C' key will clear an entered number 1 digit at a time."
- Screen: "Barcode Reference Entered" → Decision: "Go to 'Barcode - Validating Details' check"
- Screen: "Barcode Scan - Ticket Valid inc. Outbound ands Return" → Screen: "Barcode Scan - Ticket Valid inc. Outbound ands Return - Page 2" [Next page]
- Screen: "Barcode Scan - Ticket Valid inc. Outbound ands Return - Page 2" → Screen: "Barcode Scan - Ticket Valid inc. Outbound ands Return"
- Decision: "Barcode data
successfully
retrieved?" → Screen: "Barcode - Validating Details"
- Decision: "Barcode data
successfully
retrieved?" → Decision: "3b5ae6dc-a37e-4fcb-8bf7-3afda54ad4ef"
- Screen: "Barcode Validation Failed" → Decision: "This will take the user to the 'Barcode Reference' screen seen in the 'Accessing Barcode Ref. via Operator Menu' flow below."
- Screen: "Barcode Validation Failed" → Decision: "This will take the user to the 'Barcode Reference' screen seen in the 'Accessing Barcode Ref. via Operator Menu' flow below."
- Screen: "Barcode Validation Failed" → Decision: "This will take the user to the 'Barcode Reference' screen seen in the 'Accessing Barcode Ref. via Operator Menu' flow below."


## 16. 15.0 Printer Errors

### Screens (3)
- 10.4.4 Main Menu-Paper Low
- 10.4.2 Error - Printer Error
- 10.4.5 Error - Paper Jam

### Decision Points (8)
- For 'Printer Error' and 'Paper Jam' screens, where the print attempt isn't a transaction, for example a Mini Statement, Annul Ticket confirmation, Version Report or a Waybill, the 'Annul Transaction' option will be 'Continue without Printing'.
- Back to FLU as if the print was successful
- Relevant screen where print was attempted.
- Annulment flow seen in Operator Board.
- POS will attempt to reverse the paper feed to fix the paper jam - there are no screen changes as a result of this function
- Annulment flow seen in Operator Board.
- The operator will be expected to annul the transaction which caused the paper jam.
- If a print fails again it will come back to this screen. It's an endless loop until it's Annulled to force the user to annul the transaction because it has taken place, but the ticket/receipt can't be printed. An event is sent to CloudFare when a print is retried.

### Annotations / Spec Notes (3)
- Printing errors
- These errors may occur when the following conditions are being met:  - Paper level is low - Printer is malfunctioning due to hardware or software errors. - There is no paper in the feeder and user is trying to print.  The device will send an event when a print fails, when a partial print occurs due to power loss and when a ticket resumes printing after power loss.
- If the printer paper is low, the user will get a temporary notification (3 seconds timeout).

### Connections / Flow (5)
- Screen: "10.4.2 Error - Printer Error" → Decision: "Annulment flow seen in Operator Board."
- Screen: "10.4.2 Error - Printer Error" → Decision: "Relevant screen where print was attempted."
- Screen: "10.4.5 Error - Paper Jam" → Decision: "Annulment flow seen in Operator Board."
- Screen: "10.4.5 Error - Paper Jam" → Decision: "POS will attempt to reverse the paper feed to fix the paper jam - there are no screen changes as a result of this function"
- Screen: "10.4.5 Error - Paper Jam" → Decision: "Back to FLU as if the print was successful"


## 17. 16.0 Power Interruption & Audio Tones

### Screens (3)
- 15.0 - Power Interruption
- 15.1 - Restarting
- 15.2 - Charging

### Decision Points (0)

### Annotations / Spec Notes (9)
- Auto sign off
- - If the device is inactive on any of the FLU screens for the configured Auto Sign Off period then the POS will revert to the Idle screen with no waybill printed   - If the device is inactive on the Idle screen for the configured Auto Suspend period then the POS will turn the screen off and go into suspend mode   - If the device is in suspend mode for the configured Suspend Duration period then the POS will automatically reboot and go to the Idle screen  - If the device is in suspend mode then a key press will trigger the POS to reboot and go to the Idle screen
- Power Interruption
- Power interruption occurs when the device loses power. It does have backup power, but only for a very small period of time. Care has been taken to ensure that any timeouts before shutting down will be enough to save the system state safely.
- This screen appears when power is interrupted.   If the power is interrupted temporarily, the device will take the user to the screen they were originally on.
- If the power is interrupted for a longer time, this screen will display.  The system is shutting down once this state is reached.  If the power is off for shorter amount of time than the configured Auto Sign Off time then upon resuming power the POS will go to the Operator Break screen.  If the power is off for longer than the configured Auto Sign Off time then upon resuming power the POS will go to the Idle screen with no waybill printed.
- This screen appears on boot to ensure the device has enough charge to successfully allow the state to be saved in the event of a power interruption.
- Audio Tones
- Success Tone - Top Ups, Card Issues, Ticket Issues   Error Tone - Any failure   Frequent beep - Smartcard left on reader

### Connections / Flow (0)
