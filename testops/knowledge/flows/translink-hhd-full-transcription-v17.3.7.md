# TFTS HHD V17.3.7 — Translink HHD UX — Full Flow Transcription

Source: Overflow.io project "TFTS HHD V17.3.7" (https://overflow.io/s/XP0NLVZZ/)
Extracted: full text content of all boards — screen titles, decision points, annotations/spec notes, and screen-to-screen connections.
Note: This document captures TEXT content and FLOW STRUCTURE only. It does not include the actual visual mockup images (screens are referenced by their title/ID only).

## Board Index (main navigation order)
1. Welcome Page
2. 2. Login
3. 3. Tabbed Navigation
4. 4. Sales Mode
5. 5. Operator Menu Functionality
6. 6. Supervisor / Technician Functionality
7. 7. Barcode and mLink Scan
8. 8. Additional Features
9. 9. Inspection & Validation V2
10. 10. Panic Mode Function

---


## 1. Welcome Page

### Screens (1)
- 2.0 Sales Screen

### Decision Points (0)

### Annotations / Spec Notes (17)
- Welcome Page
- Ver. 17.3.7
- HHD InVision Project
- https://parkeon.invisionapp.com/overview/HHD-V17.1.1-cki8n7y2i00e80163b5qh5p98/screens
- https://parkeon.invisionapp.com/console/share/M71VJ6KVGH
- The project link is for developers. You can use the <inspect> option to view CSS styles of individual elements. You can also access the assets for the project in the <inspect> area.
- HHD User Flows Contents
- 1. Welcome Page
- 2. Login
- 3. Tabbed Navigation
- 4. Sales Mode
- 5. Operator Menu Functionality
- 6. Supervisor / Technician Functionality
- 7. Barcode and mLink Scan Validation
- 8. Additional Features
- 9. Inspection & Validation V2
- 10. Panic Mode Function

### Connections / Flow (0)


## 2. 2. Login

### Screens (32)
- 1.1 Login/Start - NIR
- 1.1.1 Login/Start - Glider
- 1.4.2 Login/Card Error
- 1.2 Login/ID Selected
- 1.3 Login/Password
- 1.3.1 Login/Password Entered
- 1.3.1 Login/Password Entered - Keypad Closed
- 1.5 Login/Duty Number
- 1.8 - Supervisor Menu
- 1.9 Technician Mode
- 1.4 Login/Sign on Failed
- 1.4.1 Login/Device Locked
- 1.5.1 Login/Duty Number Entered
- 1.4.2 Login/Card Error
- 1.3 Login/Password
- 1.6 Login/Message of the Day - Loading
- 1.3.1 Login/Password Entered
- 1.6.2 Login/Message of the Day/Error
- 1.6.1 Login/Message of the Day
- 1.3.1 Login/Password Entered - Keypad Closed
- 1 Login/Low Battery
- 1.6.3 Login/Word of the Day - Loading
- 1.8 - Supervisor Menu
- 1.6.5 Login/Word of the Day/Error
- 1.6.4 Login/Word of the Day
- 1.10 Test Printer
- 1.10.2 Test Printer/Failed
- 1.10.1 Test Printer/Success
- 2.0.6 Sales Screen - Rail Login
- 1.7 Select Route
- 1.7.1 Select Route - Menu
- 2.0 Sales Screen - Inspection

### Decision Points (16)
- HHD - Login
- Back to start of Login flow.
- User Type?
- Correct Login Details entered?
- Incorrect details entered more than 3 times?
- Back to start of Login flow.
- Back to '1.4.1 Login/Device Locked' screen.
- Message of the Day available?
- Correct Login Details entered?
- Word and Colour of the Day available?
- Back to '1.4.1 Login/Device Locked' screen.
- Back to start of Login flow.
- Print Success?
- Back to 'Test Printer' screen.
- On a Glider login?
- Go to the Sales flow.

### Annotations / Spec Notes (6)
- The logo on the Login screen will depend on the Home Location set.
- Presented Operator Card is either hotlisted or unable to be read  Message to read; 'Card Hotlisted' or 'Invalid Card'
- For Supervisor and Technician flows, see the Supervisor/Technician Area.
- Only a Supervisor can unlock the HHD  if it is locked.  To unlock the device they must log in.
- The login screen will show x of 3 up to 3 (on the third failed attempt got to 1.4.1).
- Presented Supervisor Card is either hotlisted or unable to be read  Message to read; 'Card Hotlisted' or 'Invalid Card'

### Connections / Flow (49)
- Decision: "Correct Login Details
entered?" → Decision: "Back to '1.4.1 Login/Device Locked' screen." [No - incorrect details entered.]
- Screen: "1.10.2 Test Printer/Failed" → Decision: "Back to 'Test Printer' screen." [User taps
'Retry'
button.
]
- Decision: "Message of the Day available?" → Screen: "1.6.2 Login/Message of the Day/Error" [No]
- Decision: "Correct Login Details
entered?" → Screen: "1.8 - Supervisor Menu" [Yes - correct details entered.]
- Decision: "User Type?" → Screen: "1.9 Technician Mode" [Technician]
- Decision: "Message of the Day available?" → Screen: "1.6.1 Login/Message of the Day" [Yes]
- Screen: "1.6.1 Login/Message of the Day" → Screen: "1.6.3 Login/Word of the Day - Loading" [User taps
'Okay' button.
]
- Decision: "Incorrect details entered more than 3 times?" → Screen: "1.4.1 Login/Device Locked" [Yes
HHD is now locked.
]
- Screen: "1.6 Login/Message of the Day - Loading" → Decision: "Message of the Day available?"
- Decision: "Incorrect details entered more than 3 times?" → Screen: "1.4 Login/Sign on Failed" [No]
- Decision: "User Type?" → Screen: "1.8 - Supervisor Menu" [Supervisor]
- Screen: "1.1.1 Login/Start - Glider" → Screen: "1.4.2 Login/Card Error" [User presents a card
that is either
hotlisted or not valid.
]
- Screen: "1.4.1 Login/Device Locked" → Screen: "1.3 Login/Password" [User presents a valid
supervisor smartcard.
]
- Decision: "Print Success?" → Screen: "1.10.1 Test Printer/Success" [Yes]
- Screen: "1.4 Login/Sign on Failed" → Decision: "Back to start of Login flow." [Timeout of 1 second.
]
- Screen: "1.6.3 Login/Word of the Day - Loading" → Decision: "Word and Colour of the Day available?"
- Screen: "1.2 Login/ID Selected" → Screen: "1.3 Login/Password" [User inputs ID and presses
the tick on the keypad,
or taps the Password field
or presents a smartcard.
]
- Screen: "1.4.2 Login/Card Error" → Decision: "Back to start of Login flow." [If error is 'Invalid Card', timeout is 2 seconds.
If error is 'Hotlisted Card', timeout is 5 seconds.
]
- Screen: "1.3.1 Login/Password Entered" → Screen: "1.3.1 Login/Password Entered - Keypad Closed" [User taps off keypad.]
- Screen: "1.5 Login/Duty Number" → Screen: "1.5.1 Login/Duty Number Entered" [User enters a
Duty Number.
]
- Decision: "Word and Colour of the Day available?" → Screen: "1.6.5 Login/Word of the Day/Error" [No]
- Screen: "1.6.2 Login/Message of the Day/Error" → Screen: "1.6.3 Login/Word of the Day - Loading" [Timeout of 3 seconds or the
user taps 'Okay' button.
]
- Screen: "1.3.1 Login/Password Entered" → Screen: "1.3.1 Login/Password Entered - Keypad Closed" [User taps off keypad.]
- Decision: "On a Glider login?" → Screen: "1.7 Select Route" [Yes]
- Screen: "1.3.1 Login/Password Entered - Keypad Closed" → Decision: "Correct Login Details
entered?" [User presses 'Login' button.]
- Decision: "On a Glider login?" → Screen: "2.0.6 Sales Screen - Rail Login" [No - Rail]
- Decision: "Print Success?" → Screen: "1.10.2 Test Printer/Failed" [No]
- Decision: "Correct Login Details
entered?" → Decision: "Incorrect details entered more than 3 times?" [No - incorrect details entered.]
- Screen: "1.7 Select Route" → Screen: "1.7.1 Select Route - Menu" [User taps Menu icon.]
- Screen: "1.3 Login/Password" → Screen: "1.3.1 Login/Password Entered" [User inputs password.
]
- Screen: "1.10.2 Test Printer/Failed" → Decision: "On a Glider login?" [User taps 'Continue
Without Printing' button.
]
- Screen: "1.8 - Supervisor Menu" → Decision: "Back to start of Login flow." [Supervisor taps 'Sign Off'.]
- Screen: "1.5.1 Login/Duty Number Entered" → Screen: "1.6 Login/Message of the Day - Loading" [User presses
tick on keypad.
]
- Screen: "1.10 Test Printer" → Decision: "Print Success?"
- Screen: "1.6.5 Login/Word of the Day/Error" → Screen: "1.10 Test Printer" [Timeout of 3 seconds or the
user taps 'Okay' button.
]
- Screen: "1.7 Select Route" → Screen: "2.0 Sales Screen - Inspection" [User chooses a route from the
list provided by tapping an option.
]
- Screen: "1.4.1 Login/Device Locked" → Screen: "1.4.2 Login/Card Error" [User presents a card
that is either
hotlisted or not valid.
]
- Screen: "1.3.1 Login/Password Entered" → Decision: "Correct Login Details
entered?" [User presses tick on keypad.]
- Screen: "1.3.1 Login/Password Entered - Keypad Closed" → Decision: "Correct Login Details
entered?" [User presses Log in button.]
- Screen: "1.4.2 Login/Card Error" → Decision: "Back to '1.4.1 Login/Device Locked' screen." [If error is 'Invalid Card', timeout is 2 seconds.
If error is 'Hotlisted Card', timeout is 5 seconds.
]
- Screen: "1.10.1 Test Printer/Success" → Decision: "On a Glider login?" [User taps tick or
timeout of 3 seconds.
]
- Screen: "1.1.1 Login/Start - Glider" → Screen: "1.2 Login/ID Selected" [User taps the ID field.]
- Screen: "1.1.1 Login/Start - Glider" → Screen: "1.3 Login/Password" [User presents a valid
operator smartcard.
]
- Decision: "Correct Login Details
entered?" → Decision: "User Type?" [Yes, correct details entered.]
- Screen: "1.6.4 Login/Word of the Day" → Screen: "1.10 Test Printer" [User taps
'Okay' button.
]
- Screen: "1.3 Login/Password" → Screen: "1.3.1 Login/Password Entered" [User inputs Password.
]
- Screen: "2.0 Sales Screen - Inspection" → Decision: "Go to the Sales flow."
- Decision: "Word and Colour of the Day available?" → Screen: "1.6.4 Login/Word of the Day" [Yes]
- Decision: "User Type?" → Screen: "1.5 Login/Duty Number" [Operator]


## 3. 3. Tabbed Navigation

### Screens (31)
- 2.0 Sales Screen
- 20.2.2 Tabbed Navigation - Status - Payment Device Not Paired
- 20.2.3 Tabbed Navigation - Status - Low Battery
- 20.2.4 Tabbed Navigation - Menu - Status is Low Battery
- 17.1 Low Battery - HHD
- 17.3 Critical battery
- 17.4 Critical battery - Device Power On Attempt
- 17.2 Low Battery - Printer
- 20.1 Tabbed Navigation - No Favourites
- 20.2 Tabbed Navigation - Status
- 5. Menu
- 20.2 Tabbed Navigation - Favourites - Add - Select Boarding
- 20.2.5 Status - Report Faulty Device?
- 20.2.6 Tabbed Navigation - Status - Payment Device Faulty
- 2.4.1.3 Payment Area/No Card Available 
- 20.2.1 Tabbed Navigation - Favourites - Add - Select Alighting
- 20.2.2 Tabbed Navigation - Favourites - Add - Select Passenger Type
- 20.2.3 Tabbed Navigation - Favourites - Add - Select Ticket Type
- 20.3 Tabbed Navigation - 1 Favourite
- 20.4 Tabbed Navigation - Favourites - Full
- 20.2.2.1 Tabbed Navigation - Favourites - Add - No Passenger Type Available
- 20.4.1 Tabbed Navigation - Favourites - Full - Swipe Left
- 20.4.2 Tabbed Navigation - Favourites - Full - Swipe Right
- 20.4.2.1 Tabbed Navigation - Favourites - Favourite Deleted
- 20.5 Tabbed Navigation - Favourites - Edit
- 2.8.1 Tabbed Navigation - Tickets - Favourites Unavailable
- 20.2.2 Tabbed Navigation - Favourites - Add - Select Passenger Type
- 2.8.2 Tabbed Navigation - Tickets - Max Revenue Exceeded
- 2.8 Tabbed Navigation - Tickets - Favourite Chosen
- 20.5.1 Tabbed Navigation - Favourites - Edit - Select Ticket Type (Child)
- 20.5.2 Tabbed Navigation - Favourites - Edit Made

### Decision Points (3)
- HHD - Tabbed Navigation
- Is a time band in affect?
- Has the maximum revenue limit been surpassed?

### Annotations / Spec Notes (15)
- Additional Status Area screen
- If a device battery level reaches Low Level, the Status will update accordingly.
- This screen is shown on 'safe screens' - i.e., not screens where passenger input  is required (cash, present smartcard).  This screen is only shown for the HHD.
- This screen is shown on 'safe screens' - i.e., not screens where passenger input  is required (cash, present smartcard).  This screen is only shown for the printer.
- Critical Battery cannot be shown at anytime during the flow between the user pressing the  cash button and the end of the flow if in a transaction.  N.B. This screen is only shown for the HHD.
- If the HHD is turned on while battery is critical, this screen shows.
- For Menu flows, see '5. Driver Menu Fuctionality' or '6. Supervisor/Technician Menu Functionality'.
- The option to tap the Payment Device row will always be available if the Payment Device is paired.
- If the Payment Device is faulty, card payment button will be removed from the Payment Area.
- Glider Favourites Flow
- For Glider the 'Add Favourite' flow is:  Select Boarding, Select Alighting, Select Ticket Type and then Select Passenger Type.  If there are no passenger types available on Glider, this screen will display. The user will need to press the 'Back' button on the device and select a different Ticket Type.
- If the product is available then the basket screen should be displayed.  If the product is not available due to time-bands then an error screen is displayed.
- If the user chooses to edit the Passenger Type, they must choose a Ticket Type as well. This is in case the previously selected Ticket Type is not available for the newly selected Passenger Type.
- There will be a timeout of 3 seconds on this screen and the user will be taken back to the Favourites screen.
- User can Save Changes or Cancel.  Either button press will take the user back to the Favourites (20.4) screen.

### Connections / Flow (19)
- Screen: "20.4 Tabbed Navigation - Favourites - Full" → Decision: "Is a time band in affect?" [User taps a
favourite to use.
]
- Screen: "20.2.2 Tabbed Navigation - Favourites - Add - Select Passenger Type" → Screen: "20.2.3 Tabbed Navigation - Favourites - Add - Select Ticket Type" [User chosses a
Passenger Type.
]
- Screen: "20.5 Tabbed Navigation - Favourites - Edit" → Screen: "20.2.2 Tabbed Navigation - Favourites - Add - Select Passenger Type" [User taps 'Passenger
Type' row to edit.
]
- Screen: "20.2.3 Tabbed Navigation - Favourites - Add - Select Ticket Type" → Screen: "20.3 Tabbed Navigation - 1 Favourite" [User chooses a
Ticket Type,
which adds the favourite.
]
- Screen: "20.2.2 Tabbed Navigation - Favourites - Add - Select Passenger Type" → Screen: "20.5.1 Tabbed Navigation - Favourites - Edit - Select Ticket Type (Child)" [User chooses a
Passenger Type.
]
- Screen: "20.2.1 Tabbed Navigation - Favourites - Add - Select Alighting" → Screen: "20.2.2 Tabbed Navigation - Favourites - Add - Select Passenger Type" [User chooses
an Alighting
Stage.
]
- Screen: "20.2.5 Status - Report Faulty Device?" → Screen: "20.2.6 Tabbed Navigation - Status - Payment Device Faulty" [User taps 'Confirm' button.
This notifies the back office about
the faulty device.
]
- Screen: "20.2 Tabbed Navigation - Favourites - Add - Select Boarding" → Screen: "20.2.1 Tabbed Navigation - Favourites - Add - Select Alighting" [User chooses
a Boarding
Stage.
]
- Screen: "20.4.1 Tabbed Navigation - Favourites - Full - Swipe Left" → Screen: "20.4.2.1 Tabbed Navigation - Favourites - Favourite Deleted" [User taps
'Delete' button.
]
- Screen: "20.1 Tabbed Navigation - No Favourites" → Screen: "20.2 Tabbed Navigation - Favourites - Add - Select Boarding" [User taps 'Add Favourite'.]
- Screen: "20.5.1 Tabbed Navigation - Favourites - Edit - Select Ticket Type (Child)" → Screen: "20.5.2 Tabbed Navigation - Favourites - Edit Made" [User chooses a
Ticket Type.
]
- Screen: "20.2 Tabbed Navigation - Status" → Screen: "20.2.5 Status - Report Faulty Device?" [User taps 'Payment
Device Status' row.
]
- Screen: "20.4.2 Tabbed Navigation - Favourites - Full - Swipe Right" → Screen: "20.5 Tabbed Navigation - Favourites - Edit" [User taps
'Edit' square.
]
- Screen: "20.4 Tabbed Navigation - Favourites - Full" → Screen: "20.4.2 Tabbed Navigation - Favourites - Full - Swipe Right" [User swipes right
on a Favourite.
]
- Screen: "20.4 Tabbed Navigation - Favourites - Full" → Screen: "20.4.1 Tabbed Navigation - Favourites - Full - Swipe Left" [User swipes left
on a Favourite.
]
- Decision: "Is a time band in affect?" → Decision: "Has the maximum revenue
limit been surpassed?" [No, favourites are available.
]
- Decision: "Is a time band in affect?" → Screen: "2.8.1 Tabbed Navigation - Tickets - Favourites Unavailable" [Yes, a time band is in affect.]
- Decision: "Has the maximum revenue
limit been surpassed?" → Screen: "2.8 Tabbed Navigation - Tickets - Favourite Chosen" [No, so add the favourite
to the basket.]
- Decision: "Has the maximum revenue
limit been surpassed?" → Screen: "2.8.2 Tabbed Navigation - Tickets - Max Revenue Exceeded" [Yes, so the error screen displays.]


## 4. 4. Sales Mode

### Screens (152)
- 2.0 Sales Screen
- 2.5 Basket Full
- 2.4.1.3 Payment Area/No Card Available 
- 2.0.9 Select Boarding - List - Numerical Search
- 2.0.7 Select Boarding - List - HHD Screen Size
- 2.0.2 Select Alighting - List - HHD Screen Size
- 2.8.1 Tabbed Navigation - Tickets - Edit Passengers - Rail
- 2.8.2 Tabbed Navigation - Tickets - Edit Passengers Glider
- 22 - Sales - Select Product - Glider
- 2.2 Add To Basket
- 2.0.12 Sales Screen - Paper Ticket Inspect
- 2.0.3 Select Alighting - List - Search Tapped
- 2.2.1 Add Another to Basket
- 2.0.13 Sales Screen - Paper Ticket Inspect - Confirmed
- 2.0.1 Select Alighting - List
- 2.0.10 Sales Screen - Different Ticket Type Selected
- 22.5 - Sales - Family & Friends Selected
- 2.8.2.2 Tabbed Navigation - Tickets - Edit Passengers - 1 Selected Glider
- 2.0.9.1 Select Boarding - List - Number Entered
- 2.0.8 Select Alighting - List - Search Tapped - Search Entered - No Matches
- 2.3 Items in Basket
- 22.5 - Sales - Child Selected Glider
- 22.6 - Sales - Select Product - Rail
- 2.0.9.2 Select Boarding - List - Number Entered - Tick Pressed
- 2.0.4 Select Alighting - List - Search Tapped - Search Entered
- 2.3.2 Basket Functionality - Delete
- 2.3.1 Basket Functionality - EditDuplicate
- 2.4 Payment Area
- 2.2.2 - Different Products
Selected - Rail
- 2.1 Issue Ticket
- 2.3.1.2 Item in Basket
Duplicated
- 2.3.1.1 Basket - Edit
- 2.4.1 Payment Area/Cash/Keyboard
- 2.6.2.1 - Payment - Details Swiped Down
- 22 - Sales - Select Product
- 2.4.1.1 Payment Area/Cash/Keyboard/Specific Amount
- 2.3.1.1.1 Basket - Line Edited
- 2.0 Sales Screen
- 2.3 Items in Basket
- 2.5 View Basket/Reconnect Card Reader
- 2.0.5 Sales Screen - Currency Switch Available
- 2.7 Tabbed Navigation - Tickets - Currency Switch
- 2.4.1.2 Payment Area/Cash/Currency Change
- 2.4.1.3 Payment Area/Cash/Currency Changed
- 2.0.14 Error - No Valid Tickets Available
- 22.1 - Sales - 3 Day Travel Chosen
- 2.5.3.2 View Basket/Reconnecting/Status Bar/Connecting
- 2.0.14.1 Error - No Valid Tickets - Sales
- 22.2 - Sales - 3 Day Travel Chosen - First Date Chosen
- 22.3 - Sales - 3 Day Travel Chosen - First & Second Dates Chosen
- 2.5.3 View Basket/Reconnecting/Status Bar/Not Connected
- 2.1.1 Issue Ticket - Advanced Ticket
- 22.4 - Sales - 3 Day Travel Chosen - Third Date Chosen
- 2.1.1.1 Issue Ticket - Advanced Ticket - Calendar 2
- 2.5.3.1 View Basket/Reconnecting/Status Bar/Not Connected/Contact Supervisor
- 2.3.0.1 Items in Basket - 3 Dates
- 2.1.1.2 Issue Ticket - Advanced Ticket - Calendar 3
- 2.5 View Basket/Reconnect Card Reader
- 2.1.3 Issue Advanced Ticket
- 2.1.4 Issue Advanced Ticket - Are you sure?
- 2.1.5 Issue Advanced Ticket - Are you sure?
- 2.1.6 Issue Advanced Ticket - Are you sure?
- 2.4.0.1 Payment Area - No Warrant
- 2.4.2.2 Payment/Card/Initialising Transaction
- 2.4.2 Payment/Card/User to Present Card
- 2.4.2.8 Payment/Card/Declined
- 2.4.2.4 Payment/Card/User to Confirm Amount
- 2.4.2.4 Payment/Card/User to Confirm Amount
- 2.4.2.5 Payment/Card/Processing Transaction
- 2.4.2.5 Payment/Card/Processing Transaction
- 2.4.2.1 Payment/Card/User Cancelled Transaction
- 2.4.2.5 Payment/Card/Processing Transaction
- 2.4.2.3 Payment/Card/PIN Entry
- 2.4.2.8 Payment/Card/Declined
- 2.4.2.6 Payment/Card/Transaction Success
- 2.4.2.6 Payment/Card/Transaction Success
- 2.4.2.7 Payment/Card/Signature Okay?
- 2.4.2.8 Payment/Card/Declined
- 2.4.2.5 Payment/Card/Processing Transaction
- 4.6 Voiding Last Card Transaction
- 2.4.2.8 Payment/Card/Declined
- 2.4.2.6 Payment/Card/Transaction Success
- 2.0 Sales Screen
- 2.0 Sales Screen
- 2.5.4.2 Error - Passback
- 2.5.4.2 Error - Passback
- 2.6.1 Discount - Sales mode - Rail
- 2.6.5.1 Concessionary Card - Sales mode - Rail
- 4.1.3 Critical Error - Invalid Card - Generic Error
- 4.1.3 Critical Error - Invalid Card - Generic Error
- 2.6.1.1 - Concession - Sales mode - Select Product
- 2.6.1 - Discount - Sales mode - Select Product
- 3.3 Error - Read/Write Fail
- 3.3 Error - Read/Write Fail
- 2.6.5.2 Concessionary Card - Sales mode - Rail - Return Chosen
- 2.6.1.1 Discount - Sales mode - Return Chosen
- 2.6.6 Concessionary - Summary
- 2.6.2.1 Discount - Summary - Rail
- 2.4 Payment Area
- 8.5.1.1 Printing Receipt - Card
- 8.5.1.1 Printing Receipt - Card
- 2.4.3.1 Printing Ticket - No Header
- 26.2 Print Mini Statement
- 12.2 Printing Receipt
- 2.4.3 Printing Ticket
- 2.4.3.1 Printing Ticket - No Header
- 2.4.3.1 Printing Ticket - No Header
- 2.4.3.4 Transaction complete - Card
- 11.3 Printing Waybill
- 7. Printing Waybill
- 2.4.3.3 Printing Ticket - Card
- 7.2 Print Failed
- 2.4.3.4 Transaction complete - Card
- 2.4.3.2.1 Print Failed - Card
- 2.4.3.4 Transaction complete - Card
- 8.5.2.1 Printing Failed - Card
- Print Success
- Print Success
- 8.5.2.1 Printing Failed - Card
- 2.4.3.2 Print Failed
- 2.4.3.1 Transaction complete
- 11.4 Printing Failed
- 7.1 Transaction complete
- 7.2 Print Failed
- 2.4.3.4 Transaction complete - Card
- 8.5.2.1 Printing Failed - Card
- 27 Barcode Ticket - Printed?
- 8.5.2.1 Printing Failed - Card
- 7.1 Transaction complete
- 7.2 Print Failed
- 7.1 Transaction complete
- 2.4.3.2.1 Print Failed - Card
- 8.5.1 Print Receipt?
- 7.1 Transaction complete
- 8.5.1.1 Printing Receipt - Card
- 7.2.1 Print Failed Card Payment
- 4.2.2 Top Up - iLink - Expiry Date Set
- 4.2.2.2 Top Up - iLink - Expiry 1 Day from first use
- 2.0 Sales Screen
- 4.1 Present Smart Card
- 2.5.4.1 Critical Error
- 4.1.1 Critical Error - Incorrect Card
- 4.2.1 Top Up - No products available
- 4.2 Top Up - Select Amount
- 2.4.0.1 Payment Area - No Warrant
- 4.4 Represent Smartcard
- 2.5.4.1 Critical Error
- 4.1.2 Critical Error - Invalid Card
- 8.5.1.1 Printing Receipt - Card
- 4.8 Transaction complete
- 4.6 Voiding Last Card Transaction
- 4.6 Voiding Last Card Transaction

### Decision Points (121)
- HHD - Sales Mode, Boarding/Alighting Stage Selection, Basket and Payment Area
- Once confirmed, banner will fade out so back to 'Sales' screen.
- Back to 'Sales' screen.
- Once stage is selected, back to 'Sales' screen.
- Once stage is selected, back to 'Sales' screen.
- See Card Payment flow.
- Back to '2.4 - Payment Area'.
- Back to 'Payment Area' screen.
- Go to relevant 'Cash / Payment Card Print Flow' flow.
- HHD - Payment Device Re-Connection
- HHD Rail - Additional Functionality
- From Sales screen user selects 'Three-Day Travel' in the Ticket Type list...
- Connection Success?
- Go to Card Payment flow.
- Tries Remaining?
- Back to 'Sales'  with Three-Day Product selected and price displayed. From here it can be added to the basket.
- Back to 'Sales' screen.
- Go back to 'View Basket/Reconnecting/Status Bar/Connecting' screen.
- HHD - Payment with Card
- Amount too large?
- Payment Type?
- Chip & PIN card?
- Over £45, customer decides Chip & PIN, or payment device asks customer to insert their card?
- Go to Chip & PIN flow.
- Go Back to 'User to Present Card' then follow Chip & PIN Flow.
- Transaction Success?
- Print a receipt for customer to sign. Print will go through same checks - if you cannot print the user will need to annul the transaction.
- Customer Attempting PIN Entry
- Continue back to relevant flow.
- Continue back to relevant flow.
- Back to Sales.
- Transaction Success?
- Go to the 'Receipt Print' flow.
- Continue back to relevant flow.
- HHD Rail - Smartcard Sales Mode
- Smartcard not previously Presented & Validated?
- Smartcard not previously Presented & Validated?
- Valid Smartcard?
- Valid Smartcard?
- Go to 'Sales mode' screen.
- Go to 'Concessionary Card - Sales mode' screen.
- Go back to Sales screen.
- Go back to Sales screen.
- Go to 'Top Up Receipt Print' flow.
- Go to 'Card validation success?' check above.
- Go to 'Top Up Receipt Print' flow.
- Go to 'Card validation success?' check above.
- Go to 'Concessionary Print' flow.
- Back to Sales screen.
- Go back to Sales screen.
- Go back to Sales screen.
- Back to Sales screen.
- Go to relevant 'Cash / Payment Card Print Flow' flow.
- See Card Payment flow.
- HHD - Print Flow
- Accessed Waybill when Signing Off or in a menu?
- Print success?
- Print success?
- Print success?
- Print success?
- Print Success?
- Print Success?
- Print success?
- Print Success?
- Back to 'Sales' screen or previous flow if applicable.
- Back to 'Sales' screen or previous flow if applicable.
- Back to 'Menu' screen or previous flow if applicable.
- Back to 'Sales' screen or previous flow if applicable.
- Back to 'Sales' screen.
- Back to Supervisor menu.
- Back to 'Printing Receipt' screen.
- Go back to Sales screen.
- Go to Annulment flow seen in 'Driver Menu Functionality'.
- Print Success?
- Print Mini Statement
- Go back to 'Mini Statement' screen.
- Print Success?
- Back to 'Printing Ticket - No Header' screen.
- Go back to Sales screen.
- Print success?
- Go to Annulment flow seen in  'Driver Menu Functionality'.
- Go back to Sales screen.
- Back to 'Printing Receipt' screen.
- Go back to Sales screen.
- Back to 'Sales' screen.
- Go to 'Printing Ticket - No Header' screen.
- Go to 'Printing Ticket' screen.
- Back to relevant menu.
- Go to 'Login' flow.
- Back to 'Sales' screen.
- Go back to 'Printing Waybill' screen.
- Go back to 'Waybill' screen.
- Go to 'Login' flow.
- Go to 'Printing Waybill' screen.
- Back to 'Sales' screen or previous flow if applicable.
- Go to Annulment flow seen in 'Driver Menu Functionality'.
- Print success?
- Back to 'Printing Receipt' screen.
- Go back to Sales screen.
- Back to 'Sales' screen or previous flow if applicable.
- HHD Glider & Rail - Smartcard Top Up
- Smartcard Readable?
- Valid top-up card?
- Back to 'Present Smartcard' screen.
- Any products available?
- Back to 'Sales' screen.
- Back to 'Present Smartcard' screen.
- Back to 'Sales' screen.
- Back to 'Present Smartcard' screen.
- See Card Payment flow.
- Smartcard Readable?
- Valid top-up card?
- Back to 'Sales' screen.
- Payment card used?
- Payment card used?
- Back to 'Represent Smartcard' screen.
- Back to 'Represent Smartcard' screen.
- Go to 'Card Payment Receipt Print' Flow
- Back to 'Sales' screen.
- Go to 'Card Payment Receipt Print' Flow
- Back to 'Sales' screen.

### Annotations / Spec Notes (66)
- If no Card or Warrant option is available
- If the basket is full
- User can swipe Boarding & Alighting Stages, Passenger Type and Ticket Type to quickly go to the next option.  For example, swipe '1 Adult' to change to '1 Child'.  On Glider, 'Passenger Type' field cannot be swiped, for Rail, 'Ticket Type' cannot be swiped.
- This screen is only displayed when the operator attempts to add a favourite to a full basket.   If the operator attempts to add more tickets to the basket from the sales screen the Add To Basket button will grey out once the basket gets full.   If the basket is full and the user attempts to add a favourite, the 'Basket Full' screen will appear.  There will be a 3 second timeout, or the user can tap 'Back to Basket' to manage their basket, or issue the tickets in the basket.  The basket is full once there are 9 ticket lines.
- Pressing the ABC icon will change the view to alphanumeric.
- The current stage is highlighted in the middle of the screen.  Search and other functionality is the same as the Alighting Stage selection below. Tapping the number icon will change the view to numerical input.
- When on rail, the Passenger Types are not increased, just selected. The amount of tickets are based on Ticket Type numbers selected.
- When first arriving on 'Select Passenger Type' screen, the first product is set to 1.
- When on rail, the Ticket Types can be increased or decreased. Ticket Types are dependant on the Passenger Type selected.
- The price of the basket / ticket will be displayed in the header and in the £ Price field by default.  Warrant is used for paper tickets only, not top-ups. They will appear on Waybills and are available on Rail only.
- If different items are added to the basket they will be listed. The product area (1 Single | 1 Return etc.) will be scrollable if required. The monetary value on the left represents the currently selected product; the value on the right is the basket total.
- When cross border (XB) stations are set the operator can only view/select XB (not local) ticket types.  When local stations are set the operator can only view/select local (not XB) ticket types.
- 1. The operator can simply press the cash button to issue the ticket without having to enter amount given.  2. If the operator enters amount given and presses cash button HHD will calculate change due.  The operator can also use £5, £10 and £20 buttons for transaction below £20 without the need for pressing the cash button. HHD at that point will also calculate the change due.
- No Valid Tickets Available
- Three Day Product
- Currency Change Available
- User must choose a day within 4 days from today, and then the remaining 2 days within the next 7 days from the first date chosen.
- If a user chooses a Boarding and Alighting Stage that does not have a valid ticket, this error screen will display.  After 3 seconds, it will time out and take the user back to the Sales screen, with the Boarding and Alighting Stages that were selected shown, and Ticket Type & Passenger Type being disabled.
- From this screen tapping the back button on the device will take the operator to the Ticket Type Selection screen.   Tapping the 'Cancel' button from any other screen from this flow will take the operator to the Sales screen.
- Currency change is only available on cross border rail journeys i.e. :-   1. When the boarding station is between 1 and 61 AND the alighting station is between 62 and 96 then currency change is available but the default currency is in Sterling   2. When the boarding station is between 62 and 96 then currency change is available but the default currency is in Euro   If a currency change is available, the user will have the option to swipe right on the action bar in the Sales Area before adding items to the basket, or they can change currency in the Payment Area by tapping the 'To Pay' area above the Cash button.  Warrant is used for paper tickets only, not top-ups. They will appear on Waybills and are available on Rail only.
- If the user chooses to edit the first date after picking it anywhere in this flow, they will be taken back to the start of this flow ('3 Day Travel Chosen').  User will tap to select a date, and tap again to deselect the date.
- Advanced Ticket
- Users can purchase an advanced ticket if the option is available. Parameters for advanced tickets are set within CloudFare. The user must choose only one product, then navigate to the Basket. If they can book an advanced ticket, they will see the 'Advanced Ticket?' button in the basket. Tapping this will take them to a date picker where they can choose the date of travel, and tapping confirm will set the date.
- Reconnect attempt can be tried 3 times before advising to notify a Supervisor or Technician.
- The payment device has to be activated if in sleep mode.
- Only one advanced ticket can be added to the basket.
- This check only occurs on test transactions, not for commercial use.
- The sub-message will be 'Amount too large'. Timeout of 3 seconds and back to the Payment Area.
- Timeout of 3 seconds and back to Payment Area.
- Timeout of 3 seconds and back to Payment Area. The error message will be matched to the payment device.
- Timeout of 3 seconds and back to Payment Area.
- This flow is specifically for;  1. yLink Smartcards 2. 24+ Smartcards 3. Half Fare Smartcards (5 different types).
- Discount Card Presented
- Concessionary Card Presented
- All Half Fare Smartpass products will display the words "Half Fare Smartpass", and not the sub product name (PIPS, Disability Living allowance, Partially Sighted, No Driving Licence and Learning Disability).
- The error could be "Not valid at this Location", "Card Expired"
- 1. For Dependants Pass, Senior, Blind, War Pensioner, 60+ and ROI Senior single is the only product option for local travel i.e. where boarding station and alighting station are both 61 or less.    2. For Senior, Blind, War Pensioner and ROI Senior XB single, XB day return and XB 1 month return are the product options for Cross border travel i.e. where boarding station or alighting station are greater than 61.
- The error could be "Not valid at this Location", "Card Expired"
- 1. ylink and 24+ cards have single, return, weekly and monthly options for local stations only (there are no valid options for these products on cross border journeys)   2. Half fare Smartpasses have single and return options for local stations only (there are no valid options for these products on cross border journeys).  If any of these cards are presented for stages above stage 61, HHD will display "Not Valid at This Location" screen.
- Important to note that on Rail HHD:-  1. The selected alighting station chosen by the operator is recorded in the audit data for Free Concessionary smartpasses  2.  The fare foregone (i.e. what the Adult Single would have cost a fare paying customer) is captured in the audit data for this free transaction  3.  The operator must be able to change the boarding station and/or the alighting station after they have presented the Smartpass (as well as before)
- Free concession cards will display £0.00 in the price field.
- Warrant is used for paper tickets only, not top-ups. They will appear on Waybills and are available on Rail only.
- Payment Card Receipt Print Flow
- Top Up Receipt Flow
- Concessionary Print Flow
- Penalty Fare Warning Print Flow
- Versioning Print Flow
- Barcode Travel Ticket Print Flow
- Mini Statement Print Flow
- Waybill Print Flow
- Cash Print Flow
- Payment Card Print Flow
- If a merchant receipt is printed this will be 'printing 1 of 2'.
- The screen before this will be the 'Transaction Approved' screen as seen in the card payment flows. This flow covers printing only.
- If the user cannot print, they must annul the transaction.
- If the user cannot print, they must annul the transaction.
- Barcodes are only validated once the Operator confirms a ticket has successfully printed.
- Barcodes are only validated once the Operator confirms a ticket has successfully printed. Only one reprint attempt is allowed if a print fails.
- If a merchant receipt is printed it will go to receipt printing screen (1 of 1).  If 'No' is selected, the merchant receipt will still print if it's configured to do so in the back office. If yes, both will print. It will follow the Payment card receipt flow.
- If the user cannot print, they must annul the transaction.
- If the smartcard has an expiry date set, this screen will display.
- If the smartcard has a product added, you can only add the same period type.
- For DayLink this will display days and for period cards this will display periods.
- If the smartcard has too many journeys, the user cannot add more. The minimum amount of journeys a user can add is 5.
- If the 'Card' option was selected, the banner will read 'Card Payment' instead.
- At this point the card top up receipt should be printed. If the transaction was paid for by an EMV card then Card Payment should be displayed at the top of the screen as per Card Payment Print flow screen 2.4.3.3.   If cash was used, the screen should display £x.xx change.  N.B. 'Card Payment Receipt' header will only show if card was the payment method, otherwise it will be replaced with '£Price Change' if applicable. This also applies to the Transaction Complete screen.  The Transaction Complete screen displays 'days left' for DayLink cards, 'journeys left' for Multi Journey cards. Period Passes show the new expiry date.  Print will still go through same checks seen in Print flows.

### Connections / Flow (242)
- Decision: "Payment Type?" → Decision: "Over £45, customer decides
Chip & PIN, or payment device
asks customer to insert their card?" [Contactless
]
- Decision: "Print success?" → Screen: "8.5.2.1 Printing Failed - Card" [No]
- Screen: "2.4.0.1 Payment Area - No Warrant" → Screen: "4.4 Represent Smartcard" [User chooses preset cash option,
or if customer has correct amount,
taps the 'Cash' button.
]
- Decision: "Print Success?" → Screen: "8.5.2.1 Printing Failed - Card" [No]
- Screen: "2.3.1.1 Basket - Edit" → Screen: "22 - Sales - Select Product" [User taps
'Single'.
]
- Decision: "Valid top-up card?" → Decision: "Any products
available?" [Yes]
- Screen: "4.8 Transaction complete" → Decision: "Back to 'Sales' screen." [3 second timeout...]
- Decision: "Smartcard
Readable?" → Screen: "2.5.4.1 Critical Error" [No]
- Decision: "Connection Success?" → Screen: "2.5.3 View Basket/Reconnecting/Status Bar/Not Connected" [No]
- Screen: "2.3 Items in Basket" → Screen: "2.3.1 Basket Functionality - EditDuplicate" [User swipes right
on a Basket item.
]
- Decision: "Payment card used?" → Decision: "Back to 'Sales' screen." [No]
- Screen: "4.1.1 Critical Error - Incorrect Card" → Decision: "Back to 'Present Smartcard' screen." [User taps
'Retry' button.
]
- Decision: "Print Success?" → Screen: "27 Barcode Ticket - Printed?" [Yes]
- Screen: "2.4 Payment Area" → Decision: "Go to relevant 'Cash / Payment Card Print Flow' flow." [User taps 'Warrant'.]
- Screen: "2.3.1.1.1 Basket - Line Edited" → Screen: "2.3 Items in Basket" [User taps
'Confirm Edit'.
]
- Decision: "Payment card used?" → Decision: "Back to 'Sales' screen." [No]
- Decision: "Tries Remaining?" → Screen: "2.5.3.1 View Basket/Reconnecting/Status Bar/Not Connected/Contact Supervisor" [No]
- Decision: "Print success?" → Screen: "7.2 Print Failed" [No]
- Screen: "2.4.2 Payment/Card/User to Present Card" → Decision: "Amount too large?" [Operator hands payment device over to
customer to insert or swipe their card.
If it's contactless, the customer can present
their card to the device straight away.
]
- Screen: "2.6.6 Concessionary - Summary" → Decision: "Go back to Sales screen." [User taps 'Clear Basket'.]
- Decision: "Go to relevant 'Cash / Payment Card Print Flow' flow." → Screen: "2.0 Sales Screen" [On success...]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Payment card used?" [User taps
'Cancel' button.
]
- Decision: "Chip & PIN card?" → Decision: "Go to Chip & PIN flow." [Yes, Chip & PIN
available.
]
- Screen: "2.6.6 Concessionary - Summary" → Decision: "Go to 'Concessionary Print' flow." [User taps 'Issue Ticket'.]
- Decision: "Customer Attempting
PIN Entry" → Screen: "2.4.2.8 Payment/Card/Declined" [Failed set amount of times]
- Decision: "Transaction Success?" → Screen: "2.4.2.6 Payment/Card/Transaction Success" [Yes]
- Screen: "8.5.1 Print Receipt?" → Screen: "8.5.1.1 Printing Receipt - Card" [Yes - Print]
- Decision: "Valid top-up card?" → Screen: "4.1.1 Critical Error - Incorrect Card" [No]
- Screen: "2.4 Payment Area" → Decision: "Back to 'Sales' screen." [User taps
'Cancel'.
]
- Decision: "Print success?" → Screen: "2.4.3.2.1 Print Failed - Card" [No]
- Screen: "2.4.2.5 Payment/Card/Processing Transaction" → Screen: "2.4.2.3 Payment/Card/PIN Entry"
- Screen: "4.2.1 Top Up - No products available" → Decision: "Back to 'Present Smartcard' screen." [User presses
the back
button on HHD.
]
- Decision: "Smartcard
Readable?" → Decision: "Valid top-up card?" [Yes]
- Screen: "8.5.2.1 Printing Failed - Card" → Decision: "Go back to 'Printing Waybill' screen." [User taps
'Retry'.
]
- Decision: "Print Success?" → Screen: "2.4.3.2 Print Failed" [No]
- Decision: "Print success?" → Screen: "8.5.2.1 Printing Failed - Card" [No]
- Decision: "Transaction Success?" → Screen: "2.4.2.8 Payment/Card/Declined" [No]
- Screen: "2.4.1 Payment Area/Cash/Keyboard" → Screen: "2.4.1.1 Payment Area/Cash/Keyboard/Specific Amount" [User enters amount using
numerical pad. User tapping
the tick would close the keypad.
]
- Decision: "Print Success?" → Screen: "7.1 Transaction complete" [Yes]
- Screen: "8.5.2.1 Printing Failed - Card" → Decision: "Go to 'Printing Ticket - No Header' screen." [User taps
'Retry'.
]
- Screen: "8.5.2.1 Printing Failed - Card" → Decision: "Back to 'Sales' screen." [User taps
'Cancel'.
]
- Screen: "2.6.2.1 Discount - Summary - Rail" → Screen: "2.4 Payment Area" [User taps
'Pay'.
]
- Screen: "22.4 - Sales - 3 Day Travel Chosen - Third Date Chosen" → Decision: "Back to 'Sales' screen." [User taps
'Cancel'.
]
- Screen: "2.4.2.6 Payment/Card/Transaction Success" → Decision: "Continue back to relevant flow."
- Screen: "8.5.2.1 Printing Failed - Card" → Decision: "Go back to 'Waybill' screen." [User taps
'Cancel'.
]
- Screen: "4.6 Voiding Last Card Transaction" → Decision: "Go to 'Card Payment Receipt Print' Flow"
- Decision: "Payment Type?" → Screen: "2.4.2.4 Payment/Card/User to Confirm Amount" [Customer inserts card to trigger Chip & PIN flow.]
- Screen: "2.4 Payment Area" → Decision: "Go to relevant 'Cash / Payment Card Print Flow' flow." [User chooses preset cash option,
or if customer has correct amount,
taps the 'Cash' button, or taps Warrant if applicable.
]
- Screen: "8.5.1 Print Receipt?" → Decision: "Back to 'Sales' screen or previous flow if applicable." [User taps 'No'.]
- Screen: "2.5 View Basket/Reconnect Card Reader" → Screen: "2.5.3.2 View Basket/Reconnecting/Status Bar/Connecting" [User taps
'Card' button.
]
- Decision: "Print success?" → Screen: "Print Success" [Yes]
- Screen: "2.5.4.1 Critical Error" → Decision: "Back to 'Represent Smartcard' screen." [User taps
'Retry' button.
]
- Screen: "2.3.1 Basket Functionality - EditDuplicate" → Screen: "2.3.1.2 Item in Basket
Duplicated" [User taps
'Duplicate'.
]
- Screen: "7. Printing Waybill" → Decision: "Print Success?"
- Screen: "2.3 Items in Basket" → Screen: "2.4 Payment Area" [User taps 'Pay'.]
- Screen: "22.1 - Sales - 3 Day Travel Chosen" → Screen: "22.2 - Sales - 3 Day Travel Chosen - First Date Chosen" [User taps
Saturday 31st.
]
- Screen: "Print Success" → Decision: "Back to 'Menu' screen or previous flow if applicable." [3 second timeout
or user taps Tick.
]
- Screen: "2.3.1 Basket Functionality - EditDuplicate" → Screen: "2.3.1.1 Basket - Edit" [User taps 'Edit'.]
- Decision: "Valid top-up card?" → Screen: "4.1.2 Critical Error - Invalid Card" [No]
- Screen: "2.0 Sales Screen" → Screen: "4.1 Present Smart Card" [User taps
Smartcard
top up icon.
]
- Decision: "See Card Payment flow." → Decision: "Go to relevant 'Cash / Payment Card Print Flow' flow." [Card payment success...]
- Screen: "2.5.4.1 Critical Error" → Decision: "Payment card used?" [User taps
'Cancel' button.
]
- Screen: "2.0.8 Select Alighting - List - Search Tapped - Search Entered - No Matches" → Screen: "2.0.4 Select Alighting - List - Search Tapped - Search Entered" [User clears search
using delete key
on keypad, types new
search and presses tick.
]
- Screen: "8.5.2.1 Printing Failed - Card" → Decision: "Print Mini Statement" [User taps
'Retry'.
]
- Decision: "Print success?" → Screen: "8.5.1 Print Receipt?" [Yes]
- Screen: "22.4 - Sales - 3 Day Travel Chosen - Third Date Chosen" → Decision: "Back to 'Sales'  with Three-Day Product selected and price displayed. From here it can be added to the basket." [User taps
'Continue'.
]
- Screen: "2.0 Sales Screen" → Screen: "22 - Sales - Select Product - Glider" [User taps 
'Single'.
]
- Decision: "See Card Payment flow." → Decision: "Go to relevant 'Cash / Payment Card Print Flow' flow." [Successful card
payment.
]
- Screen: "7.1 Transaction complete" → Decision: "Go to 'Login' flow."
- Screen: "2.0 Sales Screen" → Screen: "2.0.2 Select Alighting - List - HHD Screen Size" [User taps an
Alighting Stage
]
- Screen: "11.3 Printing Waybill" → Decision: "Print Success?"
- Screen: "2.4.3.1 Printing Ticket - No Header" → Decision: "Print Success?"
- Decision: "Smartcard not previously Presented & Validated?" → Decision: "Valid Smartcard?" [Yes]
- Screen: "2.6.5.2 Concessionary Card - Sales mode - Rail - Return Chosen" → Screen: "2.6.6 Concessionary - Summary" [User taps
Action Bar.
]
- Screen: "2.4.2.5 Payment/Card/Processing Transaction" → Decision: "Transaction Success?"
- Screen: "2.4.2.5 Payment/Card/Processing Transaction" → Decision: "Transaction Success?"
- Decision: "Any products
available?" → Screen: "4.2.1 Top Up - No products available" [No]
- Decision: "Connection Success?" → Decision: "Go to Card Payment flow." [Yes]
- Decision: "Amount too large?" → Decision: "Payment Type?" [No]
- Screen: "2.5.3.2 View Basket/Reconnecting/Status Bar/Connecting" → Decision: "Connection Success?"
- Screen: "12.2 Printing Receipt" → Decision: "Print Success?"
- Screen: "26.2 Print Mini Statement" → Decision: "Print success?"
- Screen: "2.4.2.4 Payment/Card/User to Confirm Amount" → Screen: "2.4.2.1 Payment/Card/User Cancelled Transaction" [Customer cancels transaction
on the payment device.
]
- Decision: "Payment card used?" → Screen: "4.6 Voiding Last Card Transaction" [Yes]
- Decision: "Any products
available?" → Screen: "4.2 Top Up - Select Amount" [Yes]
- Screen: "2.4.2.7 Payment/Card/Signature Okay?" → Screen: "4.6 Voiding Last Card Transaction" [User taps 'No' because the signature
didn't match the payment card.
]
- Screen: "2.4.3.3 Printing Ticket - Card" → Decision: "Print success?"
- Decision: "Smartcard not previously Presented & Validated?" → Screen: "2.5.4.2 Error - Passback" [No]
- Screen: "8.5.1.1 Printing Receipt - Card" → Decision: "Print success?"
- Screen: "4.6 Voiding Last Card Transaction" → Decision: "Go to 'Card Payment Receipt Print' Flow"
- Screen: "2.2 Add To Basket" → Screen: "2.2.1 Add Another to Basket" [User taps
'Add to Basket'
icon to add
another to the
basket.
]
- Screen: "22 - Sales - Select Product - Glider" → Screen: "2.0.10 Sales Screen - Different Ticket Type Selected" [User taps
'Adult Return'.
]
- Decision: "Print success?" → Screen: "7.2.1 Print Failed Card Payment" [No]
- Screen: "2.2.1 Add Another to Basket" → Screen: "2.3 Items in Basket" [User taps
basket icon.
]
- Decision: "Chip & PIN card?" → Screen: "2.4.2.4 Payment/Card/User to Confirm Amount" [No Chip & PIN
available.
]
- Screen: "8.5.2.1 Printing Failed - Card" → Decision: "Back to 'Printing Ticket - No Header' screen." [User taps
'Retry'.
]
- Screen: "2.0 Sales Screen" → Screen: "2.0.12 Sales Screen - Paper Ticket Inspect" [User swipes from the right
inwards on the action bar to
do a paper ticket inspection.
]
- Screen: "4.2 Top Up - Select Amount" → Screen: "2.4.0.1 Payment Area - No Warrant" [Journey
amount selected.
]
- Screen: "2.6.1 - Discount - Sales mode - Select Product" → Screen: "2.6.1.1 Discount - Sales mode - Return Chosen" [User taps
'Return'.
]
- Decision: "Payment Type?" → Decision: "Chip & PIN card?" [Customer Swipes card.]
- Decision: "Payment card used?" → Screen: "4.6 Voiding Last Card Transaction" [Yes]
- Screen: "2.0 Sales Screen" → Screen: "2.0.7 Select Boarding - List - HHD Screen Size" [User taps a
Boarding Stage.
]
- Screen: "2.6.1.1 Discount - Sales mode - Return Chosen" → Screen: "2.6.2.1 Discount - Summary - Rail" [User taps
'Print' icon.
]
- Screen: "4.4 Represent Smartcard" → Decision: "Smartcard
Readable?" [Customer represents smartcard.]
- Decision: "Continue back to relevant flow." → Decision: "Back to Sales." [Once print is finished...]
- Decision: "Print Success?" → Screen: "8.5.2.1 Printing Failed - Card" [No]
- Screen: "2.0.14 Error - No Valid Tickets Available" → Screen: "2.0.14.1 Error - No Valid Tickets - Sales" [3 second timeout.]
- Screen: "27 Barcode Ticket - Printed?" → Screen: "7.1 Transaction complete" [User
taps 'Yes'.
]
- Decision: "Smartcard not previously Presented & Validated?" → Screen: "2.5.4.2 Error - Passback" [No]
- Screen: "2.4.3.1 Transaction complete" → Decision: "Back to 'Sales' screen." [3 second timeout
or user taps Tick.
]
- Decision: "Print success?" → Decision: "Back to 'Sales' screen or previous flow if applicable." [Yes]
- Screen: "2.4 Payment Area" → Decision: "See Card Payment flow." [User taps 'Card'
button.
]
- Screen: "2.6.1 Discount - Sales mode - Rail" → Screen: "2.6.1 - Discount - Sales mode - Select Product" [User taps 'Single'
to select
a ticket type.
]
- Screen: "2.5.3 View Basket/Reconnecting/Status Bar/Not Connected" → Decision: "Tries Remaining?" [User taps 'Retry'.]
- Screen: "2.1.1.2 Issue Ticket - Advanced Ticket - Calendar 3" → Screen: "2.1.3 Issue Advanced Ticket" [User taps
'Confirm'.
]
- Screen: "22 - Sales - Select Product" → Screen: "2.3.1.1.1 Basket - Line Edited" [User taps
'Adult Return'.
]
- Screen: "2.0.3 Select Alighting - List - Search Tapped" → Screen: "2.0.8 Select Alighting - List - Search Tapped - Search Entered - No Matches" [User enters stage
name incorrectly 
and presses tick
on keypad.
]
- Decision: "Accessed Waybill
when Signing Off
or in a menu?" → Screen: "7. Printing Waybill" [Signing Off.]
- Screen: "22.2 - Sales - 3 Day Travel Chosen - First Date Chosen" → Screen: "22.3 - Sales - 3 Day Travel Chosen - First & Second Dates Chosen" [User taps
Wednesday 4th.
]
- Decision: "Print Success?" → Screen: "2.4.3.1 Transaction complete" [Yes]
- Decision: "From Sales screen user selects 'Three-Day Travel' in the Ticket Type list..." → Screen: "22.1 - Sales - 3 Day Travel Chosen"
- Screen: "Print Success" → Decision: "Back to 'Sales' screen or previous flow if applicable." [3 second timeout
or user taps Tick.
]
- Screen: "2.1.1 Issue Ticket - Advanced Ticket" → Screen: "2.1.1.1 Issue Ticket - Advanced Ticket - Calendar 2" [User swipes
on the calendar.
]
- Decision: "Smartcard
Readable?" → Decision: "Valid top-up card?" [Yes]
- Decision: "See Card Payment flow." → Screen: "4.4 Represent Smartcard" [Successful card
payment.
]
- Screen: "2.5.3.1 View Basket/Reconnecting/Status Bar/Not Connected/Contact Supervisor" → Screen: "2.5 View Basket/Reconnect Card Reader" [User taps
'Back to
Payment'.
]
- Screen: "7.1 Transaction complete" → Decision: "Back to Supervisor menu." [User taps green tick or
timeout of 2 seconds.
]
- Decision: "Print a receipt for customer to sign. Print will go through same checks - if you cannot print the user will need to annul the transaction." → Screen: "2.4.2.7 Payment/Card/Signature Okay?" [Once the receipt
is printed...
]
- Decision: "Amount too large?" → Screen: "2.4.2.8 Payment/Card/Declined" [Yes - limitation reached.]
- Decision: "Print Success?" → Screen: "7.1 Transaction complete" [Yes]
- Screen: "2.4.2.5 Payment/Card/Processing Transaction" → Screen: "2.4.2.6 Payment/Card/Transaction Success"
- Decision: "Print Success?" → Screen: "7.2 Print Failed" [No]
- Screen: "2.4.0.1 Payment Area - No Warrant" → Screen: "2.4.2.2 Payment/Card/Initialising Transaction" [User taps 'Card'.]
- Decision: "Valid Smartcard?" → Screen: "2.6.1 Discount - Sales mode - Rail" [Yes]
- Screen: "2.1.1.1 Issue Ticket - Advanced Ticket - Calendar 2" → Screen: "2.1.1.2 Issue Ticket - Advanced Ticket - Calendar 3" [User chooses a date in the
calendar. This can be
navigated by swiping up
or down.
]
- Screen: "2.0 Sales Screen" → Screen: "2.2 Add To Basket" [User taps
'Add to Basket'
icon.
]
- Decision: "Transaction Success?" → Screen: "2.4.2.6 Payment/Card/Transaction Success" [Yes]
- Screen: "8.5.2.1 Printing Failed - Card" → Decision: "Go back to Sales screen." [User taps
'Cancel'.
]
- Screen: "2.0.12 Sales Screen - Paper Ticket Inspect" → Screen: "2.0.13 Sales Screen - Paper Ticket Inspect - Confirmed" [Green confirms
the Back Office
has been sent
the notification
of a paper ticket
inspectoon.
]
- Decision: "See Card Payment flow." → Decision: "Back to '2.4 - Payment Area'." [Card payment failure...]
- Screen: "4.1 Present Smart Card" → Decision: "Smartcard
Readable?" [Smartcard presented.]
- Decision: "Accessed Waybill
when Signing Off
or in a menu?" → Screen: "11.3 Printing Waybill" [From a Menu.]
- Screen: "27 Barcode Ticket - Printed?" → Decision: "Go to 'Printing Ticket' screen." [User
taps 'No'.
]
- Decision: "Print success?" → Screen: "Print Success" [Yes]
- Decision: "Print success?" → Screen: "2.4.3.4 Transaction complete - Card" [Yes]
- Screen: "2.4.3.4 Transaction complete - Card" → Decision: "Go back to Sales screen." [3 second timeout
or user taps Tick.
]
- Screen: "8.5.1.1 Printing Receipt - Card" → Decision: "Print success?"
- Decision: "Print success?" → Screen: "2.4.3.4 Transaction complete - Card" [Yes]
- Screen: "2.4.3.1 Printing Ticket - No Header" → Decision: "Print success?"
- Screen: "2.4.2.7 Payment/Card/Signature Okay?" → Decision: "Continue back to relevant flow." [User taps 'Yes'.]
- Screen: "2.3 Items in Basket" → Screen: "2.3.2 Basket Functionality - Delete" [User swipes left
on Basket item
]
- Screen: "2.4 Payment Area" → Screen: "2.6.2.1 - Payment - Details Swiped Down" [User taps 'Details'.
]
- Screen: "8.5.2.1 Printing Failed - Card" → Decision: "Go back to 'Mini Statement' screen." [User taps
'Cancel'.
]
- Screen: "2.4.2.4 Payment/Card/User to Confirm Amount" → Screen: "2.4.2.5 Payment/Card/Processing Transaction"
- Screen: "2.0 Sales Screen" → Decision: "Smartcard not previously Presented & Validated?" [User presents
a smartcard.
]
- Decision: "Tries Remaining?" → Decision: "Go back to 'View Basket/Reconnecting/Status Bar/Connecting' screen." [Yes]
- Screen: "2.4.3.4 Transaction complete - Card" → Decision: "Back to 'Sales' screen or previous flow if applicable." [3 second timeout
or user taps Tick.
]
- Screen: "2.0.4 Select Alighting - List - Search Tapped - Search Entered" → Decision: "Once stage is selected, back to 'Sales' screen."
- Decision: "Over £45, customer decides
Chip & PIN, or payment device
asks customer to insert their card?" → Screen: "2.4.2.5 Payment/Card/Processing Transaction" [No - Customer
uses contactless.
]
- Screen: "2.0.9.1 Select Boarding - List - Number Entered" → Screen: "2.0.9.2 Select Boarding - List - Number Entered - Tick Pressed" [User presses
tick on keypad.
]
- Decision: "Valid top-up card?" → Screen: "8.5.1.1 Printing Receipt - Card" [Yes]
- Screen: "2.3.2 Basket Functionality - Delete" → Screen: "2.1 Issue Ticket" [User taps
'Delete'.
]
- Screen: "8.5.1.1 Printing Receipt - Card" → Screen: "4.8 Transaction complete" [Once receipt prints...]
- Decision: "Smartcard
Readable?" → Screen: "2.5.4.1 Critical Error" [No]
- Screen: "2.5.4.1 Critical Error" → Decision: "Back to 'Sales' screen." [User taps
'Cancel'
button.
]
- Screen: "22.3 - Sales - 3 Day Travel Chosen - First & Second Dates Chosen" → Screen: "22.4 - Sales - 3 Day Travel Chosen - Third Date Chosen" [User taps
Friday 6th.
]
- Screen: "2.4 Payment Area" → Screen: "2.4.1 Payment Area/Cash/Keyboard" [User taps
'Price' field.
]
- Screen: "2.0.13 Sales Screen - Paper Ticket Inspect - Confirmed" → Decision: "Once confirmed, banner will fade out so back to 'Sales' screen."
- Screen: "2.0 Sales Screen" → Screen: "2.8.1 Tabbed Navigation - Tickets - Edit Passengers - Rail" [User taps
'1 Adult'.
]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Back to 'Represent Smartcard' screen." [User taps 'Retry' button.]
- Screen: "2.4.2.6 Payment/Card/Transaction Success" → Decision: "Print a receipt for customer to sign. Print will go through same checks - if you cannot print the user will need to annul the transaction."
- Screen: "2.6.2.1 Discount - Summary - Rail" → Decision: "Go back to Sales screen." [User taps
'Clear Basket'
button.
]
- Screen: "2.0.9 Select Boarding - List - Numerical Search" → Screen: "2.0.9.1 Select Boarding - List - Number Entered" [User inputs
a number.
]
- Screen: "7.1 Transaction complete" → Decision: "Back to relevant menu."
- Screen: "2.5.4.1 Critical Error" → Decision: "Back to 'Present Smartcard' screen." [User taps
'Retry'
button.
]
- Screen: "2.6.5.1 Concessionary Card - Sales mode - Rail" → Screen: "2.6.1.1 - Concession - Sales mode - Select Product" [User taps 'Single'
to select
a ticket type.
]
- Screen: "2.4 Payment Area" → Decision: "See Card Payment flow." [User taps 'Card'.]
- Decision: "Print Success?" → Screen: "11.4 Printing Failed" [No]
- Screen: "2.4.3 Printing Ticket" → Decision: "Print Success?"
- Screen: "2.6.2.1 - Payment - Details Swiped Down" → Decision: "Back to 'Payment Area' screen." [User taps 'Details'.]
- Screen: "2.0 Sales Screen" → Screen: "2.0.9 Select Boarding - List - Numerical Search" [User taps a
Boarding Number
]
- Screen: "2.4.2.2 Payment/Card/Initialising Transaction" → Screen: "2.4.2 Payment/Card/User to Present Card"
- Decision: "Transaction Success?" → Screen: "2.4.2.8 Payment/Card/Declined" [No]
- Screen: "2.0.9.2 Select Boarding - List - Number Entered - Tick Pressed" → Decision: "Once stage is selected, back to 'Sales' screen."
- Screen: "2.0 Sales Screen" → Decision: "Smartcard not previously Presented & Validated?" [User presents
a smartcard.
]
- Screen: "4.1.1 Critical Error - Incorrect Card" → Decision: "Back to 'Sales' screen." [User taps
'Cancel' button.
]
- Screen: "2.0.2 Select Alighting - List - HHD Screen Size" → Screen: "2.0.3 Select Alighting - List - Search Tapped" [User taps a
Search bar.
]
- Screen: "2.1.3 Issue Advanced Ticket" → Screen: "2.1.4 Issue Advanced Ticket - Are you sure?" [User taps 'Add
More to Basket'.
]
- Decision: "Customer Attempting
PIN Entry" → Screen: "2.4.2.5 Payment/Card/Processing Transaction" [PIN Entry success]
- Decision: "Print Success?" → Screen: "7.1 Transaction complete" [Yes]
- Screen: "2.4.2.6 Payment/Card/Transaction Success" → Decision: "Continue back to relevant flow."
- Screen: "7.2 Print Failed" → Decision: "Go to 'Login' flow." [User taps
'Continue Without Printing'.
]
- Screen: "7.2 Print Failed" → Decision: "Go to 'Printing Waybill' screen." [User taps
'Retry'.
]
- Screen: "7.2.1 Print Failed Card Payment" → Decision: "Back to 'Printing Receipt' screen." [User taps
'Retry'.
]
- Screen: "7.2.1 Print Failed Card Payment" → Decision: "Go back to Sales screen." [User taps
'Continue Without
Printing'.
]
- Screen: "2.0 Sales Screen" → Screen: "2.8.2 Tabbed Navigation - Tickets - Edit Passengers Glider" [User taps
'1 Adult'.]
- Screen: "2.8.2 Tabbed Navigation - Tickets - Edit Passengers Glider" → Screen: "2.8.2.2 Tabbed Navigation - Tickets - Edit Passengers - 1 Selected Glider" [User taps '-' on Adult
and '+' on Child]
- Screen: "2.8.2.2 Tabbed Navigation - Tickets - Edit Passengers - 1 Selected Glider" → Screen: "22.5 - Sales - Child Selected Glider" [User taps
'Confirm'
button.]
- Screen: "2.1.3 Issue Advanced Ticket" → Screen: "2.1.5 Issue Advanced Ticket - Are you sure?" [User attempts to
duplicate a product.]
- Screen: "2.1.3 Issue Advanced Ticket" → Screen: "2.1.6 Issue Advanced Ticket - Are you sure?" [User attempts to
edit a product.]
- Screen: "2.4.3.2.1 Print Failed - Card" → Decision: "Go to Annulment flow seen in 'Driver Menu Functionality'."
- Screen: "4.6 Voiding Last Card Transaction" → Decision: "Go to the 'Receipt Print' flow."
- Screen: "2.4.3.4 Transaction complete - Card" → Screen: "2.4.3.3 Printing Ticket - Card"
- Screen: "7.2 Print Failed" → Decision: "Go back to Sales screen."
- Screen: "7.2 Print Failed" → Decision: "Back to 'Printing Receipt' screen."
- Screen: "2.4.3.1 Printing Ticket - No Header" → Decision: "Print success?"
- Screen: "7.1 Transaction complete" → Decision: "Back to 'Sales' screen."
- Screen: "2.4.2.3 Payment/Card/PIN Entry" → Decision: "Customer Attempting
PIN Entry"
- Decision: "Over £45, customer decides
Chip & PIN, or payment device
asks customer to insert their card?" → Decision: "Go Back to 'User to Present Card' then follow Chip & PIN Flow." [Yes]
- Screen: "2.4.2.4 Payment/Card/User to Confirm Amount" → Screen: "2.4.2.5 Payment/Card/Processing Transaction"
- Decision: "Print success?" → Screen: "2.4.3.4 Transaction complete - Card" [Yes]
- Screen: "8.5.1.1 Printing Receipt - Card" → Decision: "Print success?"
- Screen: "2.4.3.4 Transaction complete - Card" → Decision: "Back to 'Sales' screen or previous flow if applicable." [3 second timeout
or user taps Tick.
]
- Screen: "7.2 Print Failed" → Decision: "Back to 'Printing Receipt' screen." [User taps
'Retry'.
]
- Screen: "7.2 Print Failed" → Decision: "Go back to Sales screen." [User taps
'Continue Without
Printing'.
]
- Decision: "Print success?" → Screen: "7.2 Print Failed" [No]
- Decision: "Print success?" → Screen: "2.4.3.2.1 Print Failed - Card" [No]
- Screen: "2.6.1.1 - Concession - Sales mode - Select Product" → Screen: "2.6.5.2 Concessionary Card - Sales mode - Rail - Return Chosen" [User taps
'Return'.]
- Screen: "2.4.1.1 Payment Area/Cash/Keyboard/Specific Amount" → Decision: "Go to relevant 'Cash / Payment Card Print Flow' flow." [User taps a payment option...]
- Screen: "2.4.0.1 Payment Area - No Warrant" → Decision: "See Card Payment flow." [User chooses 'Card' option]
- Screen: "2.8.1 Tabbed Navigation - Tickets - Edit Passengers - Rail" → Screen: "22.5 - Sales - Family & Friends Selected" [User taps on 'Family']
- Screen: "22.5 - Sales - Family & Friends Selected" → Screen: "22.6 - Sales - Select Product - Rail" [User taps
'Family & Friends'.]
- Decision: "Back to 'Sales'  with Three-Day Product selected and price displayed. From here it can be added to the basket." → Screen: "2.3.0.1 Items in Basket - 3 Dates" [Item added to Basket...]
- Screen: "4.1.3 Critical Error - Invalid Card - Generic Error" → Decision: "Go to 'Concessionary Card - Sales mode' screen." [User taps
'Retry' button.
]
- Screen: "4.1.3 Critical Error - Invalid Card - Generic Error" → Decision: "Go back to Sales screen." [User taps
'Cancel' button.
]
- Decision: "Valid Smartcard?" → Screen: "2.6.5.1 Concessionary Card - Sales mode - Rail" [Yes]
- Decision: "Valid Smartcard?" → Screen: "4.1.3 Critical Error - Invalid Card - Generic Error" [No, error]
- Screen: "4.1.3 Critical Error - Invalid Card - Generic Error" → Decision: "Go to 'Sales mode' screen." [User taps
'Retry' button.
]
- Screen: "4.1.3 Critical Error - Invalid Card - Generic Error" → Decision: "Go back to Sales screen." [User taps
'Cancel' button.
]
- Decision: "Valid Smartcard?" → Screen: "4.1.3 Critical Error - Invalid Card - Generic Error" [No, error]
- Decision: "Smartcard not previously Presented & Validated?" → Decision: "Valid Smartcard?" [Yes]
- Screen: "2.5 View Basket/Reconnect Card Reader" → Screen: "2.5.3.1 View Basket/Reconnecting/Status Bar/Not Connected/Contact Supervisor" [User taps 'Card' button.]
- Decision: "Go to 'Top Up Receipt Print' flow." → Decision: "Back to Sales screen." [Once Print flow is complete...]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Top Up Receipt Print' flow." [User taps
'Faulty Smartpass'.]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Card validation success?' check above." [User taps 'Retry'.]
- Decision: "Valid Smartcard?" → Screen: "3.3 Error - Read/Write Fail" [Read/Write Error]
- Decision: "Go to 'Top Up Receipt Print' flow." → Decision: "Back to Sales screen." [Once Print flow is complete...]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Top Up Receipt Print' flow." [User taps
'Faulty Smartpass'.]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Card validation success?' check above." [User taps 'Retry'.]
- Decision: "Valid Smartcard?" → Screen: "3.3 Error - Read/Write Fail" [Read/Write Error]
- Screen: "2.4.3.2 Print Failed" → Decision: "Go to Annulment flow seen in  'Driver Menu Functionality'." [User taps
'Annul Transaction'.
]
- Screen: "2.4.3.2.1 Print Failed - Card" → Decision: "Go to Annulment flow seen in 'Driver Menu Functionality'."


## 5. 5. Operator Menu Functionality

### Screens (45)
- 5. Operator Menu - Glider
- 4.1 Present Smart Card
- 9. View Totals
- 8.2.1 Annul Transaction
- 6.2 Break Mode - Glider
- 1.6 Login/Message of the Day - Loading
- 1.6.3 Login/Word of the Day - Loading
- 6. Break Mode
- 6.1 Break Mode - NIR
- 2.5.4.1 Critical Error
- 26. Mini Statement
- 26.1 Mini Statement - Shorter
- 8.4 Present Smart Card
- 1.6.5 Login/Word of the Day/Error
- 1.6.4 Login/Word of the Day
- 1.6.2 Login/Message of the Day/Error
- 1.6.1 Login/Message of the Day
- 2.5.4.1 Critical Error
- 4.1.2 Critical Error - Invalid Card
- 5.2 Operator Menu - Rail
- 4.1.4 Critical Error - Last Operation Not Top-Up
- 8.2 Annul - List of Transactions
- 5.3 Operator Menu - Rail - Nothing to Annul
- 8.2.3 Annul - List of Transactions - Search
- 8.2.4 Annul - List of Transactions - Search Entered
- 8.2.5 Annul - List of Transactions - Search Done
- 8.2.1.1 Annul Transaction - Rail
- 8.2.2 Critical Error - Invalid Transaction Selected
- 8.4 Present Smart Card
- 2.5.4.1 Critical Error
- 4.1.2 Critical Error - Invalid Card
- 4.1.4 Critical Error - Last Operation Not Top-Up
- 8.5.1.2 Printing Refund
- 8.5.1.3 Performing Card Refund
- 8.5.1.2 Printing Refund
- 8.5.2 Printing Failed - Annulment
- 8.5.1.4 Printing Refund - Confirm
- 8.5.2 Printing Failed - Annulment
- 8.5.1.5 Print EMV Receipt?
- 8.5.3 Print Failed - Annulment - Continue without Print
- 8.5.1.3 Printing Refund - Card Payment Receipt
- 8.5.3 Print Failed - Annulment - Continue without Print
- 8.5.4 Contact Ticket Office
- 8.5.4 Contact Ticket Office
- 8.5.3.1 Print Failed - Card Receipt

### Decision Points (50)
- HHD - Operator Menu Functionality
- Go to 'Connect Printer', in the Supervisor Menu flow.
- Go to 'Pair Payment Device', in the Supervisor Menu flow.
- User chooses to issue a penalty fare and third party app opens. A Penalty Fare ticket also prints.
- Go to 'Penalty Fare Warning' print flow.
- Go to 'Waybill Print Flow'.
- Is the card valid?
- Back to 'Operator Menu - Glider' screen.
- Transaction type
- Message of the Day available?
- Word and Colour of the Day available?
- Go to relevant print annulment flow.
- Back to 'Operator Menu' screen.
- Go to 'Mini Statement Print Flow'.
- Can the card be read?
- Back to 'Present Smart Card' screen.
- Is the card valid?
- Was the last operation a discount card validation?
- Go to 'Operator Menu'.
- Go to 'Operator Menu'.
- Was the last operation a top-up?
- Back to 'Operator Menu' screen.
- Go to 'Receipt Print' flow.
- Back to 'Present Smart Card' screen.
- Go to relevant print annulment flow.
- Go back to 'Annul - List of Transactions'.
- Transaction type
- Is this transaction for the last top-up?
- Go to relevant print annulment flow.
- Can the card be read?
- Is the card valid?
- Was the last operation a discount card validation?
- Was the last operation a top-up?
- Back to 'Operator Menu' screen.
- Back to 'Present Smart Card' screen.
- Go to relevant print annulment flow.
- HHD - Print Flow - Annulment
- Print success?
- Print success?
- Back to 'Sales' screen.
- Third print attempt?
- Third print attempt?
- Go to 'Printing Refund' screen.
- Go to 'Printing Refund' screen.
- Print success?
- Back to 'Sales' screen.
- Back to 'Sales' screen.
- Back to 'Sales' screen.
- Go to 'Printing Refund - Card Payment Receipt' screen.
- Back to 'Operator Menu' screen.

### Annotations / Spec Notes (22)
- Annulment Rules
- Product
- Glider
- Rail
- Top up
- Can annul only last ticket within 60 secs, provided it is done before validation of the card
- Any top up ticket can be annulled, provided it is done before validation of the card and within 60 minutes
- Paper Tickets
- Can annul only last ticket within 60 secs
- Any ticket can be annulled within the last 60 minutes
- Any ticket can be annulled, provided it is done before validation of the card and within the last 60 minutes
- Concessionary cards, discount cards
- Can annul only last ticket within 60 secs
- Note:  Once a card is validated you cannot annul any ticket on that card.
- Word and Colour of the Day from the Operator Menu will not be available until after R1.1 Go Live.
- The smartcard needs to be presented for every transaction done with the smartcard i.e. every write to a smartcard needs the smartcard to be presented whether be it annulling a transaction or topping up. The same applies for concession cards.
- If the user types a number that doesn't exist, the results will be empty.
- This screen will show if the transaction selected is a top-up, but not the most recent top-up; only the most recent top-up on a smartcard can be annulled, not one before, in case the smartcard has been used since an earlier top-up.
- Cash Print Flow - Annulment
- Card Print Flow - Annulment
- Unsuccessful prints will now take user to 'Print Failed - Annulment - Continue without Print'.
- Unsuccessful prints will now take user to 'Print Failed - Annulment - Continue without Print'.

### Connections / Flow (92)
- Decision: "Is this transaction for
the last top-up?" → Screen: "8.2.2 Critical Error - Invalid Transaction Selected" [No, this transaction is not the
most recent top-up associated
with the smartcard.
]
- Decision: "Was the last operation
a discount card
validation?" → Decision: "Go to relevant print annulment flow." [Yes]
- Screen: "8.2.1 Annul Transaction" → Decision: "Transaction type" [User taps 'Annul'.]
- Screen: "8.5.4 Contact Ticket Office" → Decision: "Back to 'Sales' screen." [3 second timeout...]
- Decision: "Was the last operation
a top-up?" → Screen: "4.1.4 Critical Error - Last Operation Not Top-Up" [No]
- Decision: "Print success?" → Screen: "8.5.2 Printing Failed - Annulment" [No]
- Screen: "8.4 Present Smart Card" → Decision: "Can the card
be read?" [Smartcard presented.]
- Decision: "Is the card valid?" → Decision: "Was the last operation
a discount card
validation?" [Yes]
- Screen: "2.5.4.1 Critical Error" → Decision: "Back to 'Operator Menu' screen." [User presses
'Cancel' button.
]
- Decision: "Was the last operation
a top-up?" → Screen: "4.1.4 Critical Error - Last Operation Not Top-Up" [No]
- Screen: "8.5.1.5 Print EMV Receipt?" → Screen: "8.5.1.3 Printing Refund - Card Payment Receipt" [Yes
]
- Screen: "5. Operator Menu - Glider" → Screen: "8.2.1 Annul Transaction" [User taps Annul
Previous Ticket
]
- Decision: "Is the card valid?" → Screen: "2.5.4.1 Critical Error" [No]
- Screen: "26.1 Mini Statement - Shorter" → Decision: "Go to 'Mini Statement Print Flow'." [User taps 'Print'.]
- Decision: "Was the last operation
a top-up?" → Decision: "Go to relevant print annulment flow." [Yes]
- Screen: "8.5.3 Print Failed - Annulment - Continue without Print" → Screen: "8.5.4 Contact Ticket Office" [User taps 'Continue
Without Printing'.
]
- Screen: "8.5.2 Printing Failed - Annulment" → Decision: "Third print
attempt?"
- Decision: "Third print
attempt?" → Screen: "8.5.1.2 Printing Refund" [No]
- Decision: "Print success?" → Screen: "8.5.1.5 Print EMV Receipt?" [Yes]
- Screen: "2.5.4.1 Critical Error" → Decision: "Back to 'Present Smart Card' screen." [User presses 'Retry'.]
- Decision: "Third print
attempt?" → Screen: "8.5.1.2 Printing Refund" [No]
- Screen: "5.2 Operator Menu - Rail" → Screen: "8.2 Annul - List of Transactions" [User taps 
'Annul Ticket'.
]
- Decision: "Was the last operation
a top-up?" → Decision: "Go to relevant print annulment flow." [Yes]
- Screen: "8.2 Annul - List of Transactions" → Screen: "8.2.3 Annul - List of Transactions - Search" [User taps
search bar.
]
- Decision: "Was the last operation
a discount card
validation?" → Decision: "Was the last operation
a top-up?" [No]
- Decision: "Is the card valid?" → Decision: "Was the last operation
a discount card
validation?" [Yes]
- Screen: "2.5.4.1 Critical Error" → Decision: "Back to 'Operator Menu' screen." [User presses
'Cancel' button.
]
- Decision: "Third print
attempt?" → Screen: "8.5.3 Print Failed - Annulment - Continue without Print" [Yes]
- Decision: "Transaction type" → Screen: "8.4 Present Smart Card" [Top Ups and Discount
smartcard validations.
]
- Decision: "Print success?" → Decision: "Back to 'Sales' screen." [Yes]
- Screen: "8.2.5 Annul - List of Transactions - Search Done" → Screen: "8.2.1.1 Annul Transaction - Rail" [User selects ticket
to annul.
]
- Decision: "Is this transaction for
the last top-up?" → Screen: "8.4 Present Smart Card" [Yes, or a discount card
so not applicable.
]
- Decision: "Is the card valid?" → Screen: "4.1.2 Critical Error - Invalid Card" [No]
- Decision: "Was the last operation
a discount card
validation?" → Decision: "Go to relevant print annulment flow." [Yes]
- Decision: "Print success?" → Screen: "8.5.2 Printing Failed - Annulment" [No]
- Decision: "Print success?" → Screen: "8.5.1.4 Printing Refund - Confirm" [Yes]
- Screen: "8.2.1.1 Annul Transaction - Rail" → Decision: "Transaction type" [User taps 'Annul'.]
- Screen: "8.5.3 Print Failed - Annulment - Continue without Print" → Screen: "8.5.4 Contact Ticket Office" [User taps 'Continue
Without Printing'.
]
- Screen: "8.4 Present Smart Card" → Decision: "Can the card
be read?" [Smartcard presented.]
- Screen: "8.5.3.1 Print Failed - Card Receipt" → Decision: "Back to 'Operator Menu' screen." [User taps 'Continue
without Printing'.
]
- Decision: "Transaction type" → Decision: "Go to relevant print annulment flow." [Paper ticket.]
- Screen: "8.5.2 Printing Failed - Annulment" → Decision: "Third print
attempt?"
- Decision: "Transaction type" → Decision: "Is this transaction for
the last top-up?" [Top Ups and Discount
smartcard validations.
]
- Screen: "8.5.1.4 Printing Refund - Confirm" → Decision: "Back to 'Sales' screen."
- Screen: "5. Operator Menu - Glider" → Screen: "4.1 Present Smart Card" [User taps 'Mini Statement'.]
- Screen: "8.5.3.1 Print Failed - Card Receipt" → Decision: "Go to 'Printing Refund - Card Payment Receipt' screen." [User taps 'Retry'.]
- Screen: "2.5.4.1 Critical Error" → Decision: "Back to 'Operator Menu' screen." [User taps 'Cancel'.]
- Decision: "Can the card
be read?" → Screen: "2.5.4.1 Critical Error" [No]
- Screen: "5. Operator Menu - Glider" → Decision: "Go to 'Waybill Print Flow'." [User taps 'Sign Off'.]
- Screen: "5. Operator Menu - Glider" → Screen: "6.2 Break Mode - Glider" [User taps
'Break Mode'.
]
- Screen: "5. Operator Menu - Glider" → Decision: "User chooses to issue a penalty fare and third party app opens.
A Penalty Fare ticket also prints." [User taps 'Issue Penalty Fare'.]
- Screen: "5. Operator Menu - Glider" → Screen: "9. View Totals" [User taps 'Totals'.]
- Decision: "Can the card
be read?" → Decision: "Is the card valid?" [Yes]
- Screen: "8.2.3 Annul - List of Transactions - Search" → Screen: "8.2.4 Annul - List of Transactions - Search Entered" [User enters
ticket number.
]
- Screen: "2.5.4.1 Critical Error" → Decision: "Back to 'Present Smart Card' screen." [User presses 'Retry'.]
- Decision: "Is the card valid?" → Screen: "4.1.2 Critical Error - Invalid Card" [No]
- Screen: "5. Operator Menu - Glider" → Decision: "Go to 'Penalty Fare Warning' print flow." [User taps 'Issue Penalty Warning'.
]
- Decision: "Is the card valid?" → Screen: "26.1 Mini Statement - Shorter" [Yes]
- Screen: "8.5.3 Print Failed - Annulment - Continue without Print" → Decision: "Go to 'Printing Refund' screen." [User taps 'Retry'.]
- Screen: "2.5.4.1 Critical Error" → Decision: "Back to 'Present Smart Card' screen." [User taps 'Retry'.]
- Screen: "8.5.3 Print Failed - Annulment - Continue without Print" → Decision: "Go to 'Printing Refund' screen." [User taps 'Retry'.]
- Decision: "Can the card
be read?" → Decision: "Is the card valid?" [Yes]
- Screen: "8.5.4 Contact Ticket Office" → Decision: "Back to 'Sales' screen." [5 second timeout...]
- Decision: "Can the card
be read?" → Screen: "2.5.4.1 Critical Error" [No]
- Decision: "Was the last operation
a discount card
validation?" → Decision: "Was the last operation
a top-up?" [No]
- Screen: "8.5.1.3 Printing Refund - Card Payment Receipt" → Decision: "Print success?"
- Screen: "8.5.1.2 Printing Refund" → Decision: "Print success?"
- Screen: "5.2 Operator Menu - Rail" → Decision: "Go to 'Receipt Print' flow." [User taps
'Receipt'.
]
- Screen: "8.2.4 Annul - List of Transactions - Search Entered" → Screen: "8.2.5 Annul - List of Transactions - Search Done" [User taps tick
on numerical
keypad.
]
- Decision: "Transaction type" → Decision: "Go to relevant print annulment flow." [Paper ticket.]
- Decision: "Print success?" → Screen: "8.5.3.1 Print Failed - Card Receipt" [No]
- Screen: "4.1 Present Smart Card" → Decision: "Is the card valid?"
- Decision: "Third print
attempt?" → Screen: "8.5.3 Print Failed - Annulment - Continue without Print" [Yes]
- Screen: "8.5.1.5 Print EMV Receipt?" → Decision: "Back to 'Sales' screen." [No]
- Screen: "8.5.1.3 Performing Card Refund" → Screen: "8.5.1.2 Printing Refund"
- Screen: "8.5.1.2 Printing Refund" → Decision: "Print success?"
- Decision: "Message of the Day available?" → Screen: "1.6.2 Login/Message of the Day/Error" [No]
- Decision: "Message of the Day available?" → Screen: "1.6.1 Login/Message of the Day" [Yes]
- Screen: "1.6.1 Login/Message of the Day" → Decision: "Go to 'Operator Menu'." [User taps
'Okay' button.
]
- Screen: "1.6.3 Login/Word of the Day - Loading" → Decision: "Word and Colour of the Day available?"
- Decision: "Word and Colour of the Day available?" → Screen: "1.6.5 Login/Word of the Day/Error" [No]
- Screen: "1.6.2 Login/Message of the Day/Error" → Decision: "Go to 'Operator Menu'." [Timeout of 3 seconds or the
user taps 'Okay' button.
]
- Decision: "Word and Colour of the Day available?" → Screen: "1.6.4 Login/Word of the Day" [Yes]
- Screen: "5. Operator Menu - Glider" → Screen: "1.6 Login/Message of the Day - Loading" [User taps 'Message of the Day'.]
- Screen: "1.6 Login/Message of the Day - Loading" → Decision: "Message of the Day available?"
- Screen: "5. Operator Menu - Glider" → Screen: "1.6.3 Login/Word of the Day - Loading" [User taps 'Word and Colours of the Day'.]
- Screen: "1.6.4 Login/Word of the Day" → Decision: "Go to 'Operator Menu'." [User taps
'Okay' button.]
- Screen: "1.6.5 Login/Word of the Day/Error" → Decision: "Go to 'Operator Menu'." [Timeout of 3 seconds or the
user taps 'Okay' button.]
- Screen: "8.2.1 Annul Transaction" → Decision: "Back to 'Operator Menu - Glider' screen."
- Screen: "8.2.1.1 Annul Transaction - Rail" → Decision: "Go back to 'Annul - List of Transactions'." ['Cancel' tapped.]
- Screen: "5. Operator Menu - Glider" → Decision: "Go to 'Connect Printer', in the Supervisor Menu flow." [Connect Printer]
- Screen: "5. Operator Menu - Glider" → Decision: "Go to 'Pair Payment Device', in the Supervisor Menu flow." [Pair Payment Device]


## 6. 6. Supervisor / Technician Functionality

### Screens (44)
- 19.2 Supervisor Menu - Signed in On Duty - Rail
- 19.3 Supervisor Menu - Signed in On Duty - Rail - Full
- 11.1.1 View All Waybills - Rail
- 11.3 View Waybill - Rail
- 1.8 - Supervisor Menu
- 11.1 View All Waybills
- 12.1 View/Print Versions - Full
- 12.1 View/Print Versions
- 10.5 Connecting to card_reader - Connect via Bluetooth
- 10 Enter MAC Address
- 19.1 Supervisor Menu - Signed in On Duty - Glider
- 1.6 Login/Message of the Day - Loading
- 1.6.3 Login/Word of the Day - Loading
- 10.6 Connecting to card_reader
- 11.2.1 View Waybill - Full
- 11.2 View Waybill
- 19 Supervisor Menu - Signed in On Duty
- 1.6.5 Login/Word of the Day/Error
- 1.6.4 Login/Word of the Day
- 1.6.2 Login/Message of the Day/Error
- 1.6.1 Login/Message of the Day
- 10.1 Enter MAC Address - field tapped
- 10.8 Card_Reader_Not_Connected
- 10.6.1 Configuring Payment Device
- 10.1.1 MAC Address entered
- 10.9 MAC Address Invalid
- 10.2 Connecting to printer
- 10.7 Card_Reader_Connected
- 10.4 Unable to Connect
- 10.2.1 Waiting for Printer
- 10.3 Printer Connected
- 1.9 Technician Mode
- 15 Transferring Data to Back Office
- 13.1 Payment Terminal - Blank
- 14 Printer Firmware - Applying
- 14.1 Printer Firmware - Applied
- 13.2 Payment Terminal - Terminal ID Selected
- 15.1 Back Office Not Available
- 21 Set Home Location
- 13.3 Payment Terminal - Terminal ID Entered
- 21.1 - Setting Home Location
- 13.4 Payment Terminal - Transaction Key Entered
- 21.2 New Home Location
- 13.5 Payment Terminal - Details Saved

### Decision Points (30)
- HHD - Supervisor Menu Functions
- Go to 'Login' flow.
- Go to 'Versioning Print' flow.
- See 'Operator Menu Functionality' flow.
- Go to 'Waybill Print' flow.
- Message of the Day available?
- Word and Colour of the Day available?
- Manual Entry or scan barcode?
- Go to 'Waybill Print' flow.
- Pairing  Success?
- Barcode scanned?
- Back to 'Connecting to card_reader - Connect via Bluetooth' screen.
- Go to 'Operator Menu'.
- Go to 'Operator Menu'.
- Back to 'Enter MAC Address' screen.
- Back to 'Supervisor Menu'.
- Connection Success?
- Back to 'Enter MAC Address' screen.
- Back to 'Supervisor Menu'.
- HHD - Technician Menu Functions
- Same as 'Supervisor Menu' flow.
- Opens third party app.
- Same as 'Supervisor Menu' flow.
- Same as 'Supervisor Menu' flow.
- Go to 'Login' flow.
- Is the Back Office available?
- Back to 'Technician Menu'.
- Back to 'Technician Menu'.
- Back to 'Technician Menu'.
- Back to 'Technician Menu'.

### Annotations / Spec Notes (5)
- Supervisor Menu - On Duty - Rail
- Supervisor - Rail - Waybills
- The menu for rail will show the option of 'Annul Ticket' because any ticket issued on this duty can be annulled.
- Once the user taps 'Continue' and the pairing begins, the device will display a code, which should be the same as the Payment Device. This is a built in Android feature.  The user should press 'Pair'. Once they press 'Pair' the 'Pairing with payment device' screen will display.
- The menu is full but will scroll.  The screen above shows all items available.

### Connections / Flow (67)
- Screen: "1.8 - Supervisor Menu" → Screen: "11.1 View All Waybills" [User taps
'View Waybills'.
]
- Decision: "Connection
Success?" → Screen: "10.4 Unable to Connect" [No]
- Screen: "10.9 MAC Address Invalid" → Decision: "Back to 'Enter MAC Address' screen." [3 second timeout...]
- Screen: "1.9 Technician Mode" → Decision: "Same as 'Supervisor Menu' flow." [User taps 'Versioning'.]
- Decision: "Barcode scanned?" → Screen: "10.2 Connecting to printer" [Valid address scanned.]
- Screen: "1.9 Technician Mode" → Decision: "Same as 'Supervisor Menu' flow." [User taps
'Connect Printer'.
]
- Screen: "19.1 Supervisor Menu - Signed in On Duty - Glider" → Decision: "See 'Operator Menu Functionality' flow." [User taps
'Break Mode',
'Annul Previous Ticket',
'Issue Penalty Fare',
'Issue Penalty Warning',
'Mini Statement' or
'Totals'.
]
- Screen: "15 Transferring Data to Back Office" → Decision: "Is the Back Office
available?"
- Screen: "1.8 - Supervisor Menu" → Screen: "19.1 Supervisor Menu - Signed in On Duty - Glider" [User taps 'Start Duty'.

Go through 'Duty Selection' flow
seen in the 'Login' flow,
then go to Sales Screen.
Menu includes extra options.
]
- Screen: "13.2 Payment Terminal - Terminal ID Selected" → Screen: "13.3 Payment Terminal - Terminal ID Entered" [User inputs ID using
numerical pad
and taps tick.
]
- Screen: "1.9 Technician Mode" → Screen: "13.1 Payment Terminal - Blank" [User taps 'Payment
Terminal'.
]
- Screen: "10.2 Connecting to printer" → Decision: "Connection
Success?"
- Decision: "Manual Entry or scan barcode?" → Decision: "Barcode scanned?" [Scanned barcode.]
- Screen: "14.1 Printer Firmware - Applied" → Decision: "Back to 'Technician Menu'." [User taps green tick or
timeout of 2 seconds.
]
- Decision: "Is the Back Office
available?" → Screen: "21 Set Home Location" [Yes]
- Screen: "10.2.1 Waiting for Printer" → Screen: "10.3 Printer Connected"
- Screen: "1.9 Technician Mode" → Decision: "Go to 'Login' flow." [User taps 'Sign Off'.]
- Screen: "1.8 - Supervisor Menu" → Decision: "Go to 'Login' flow." [User taps
'Sign Off'.
]
- Screen: "14 Printer Firmware - Applying" → Screen: "14.1 Printer Firmware - Applied"
- Decision: "Manual Entry or scan barcode?" → Screen: "10.1 Enter MAC Address - field tapped" [User taps the
'MAC Address'
field.]
- Decision: "Connection
Success?" → Screen: "10.2.1 Waiting for Printer" [Yes]
- Screen: "21.2 New Home Location" → Decision: "Back to 'Technician Menu'." [User taps green tick or
timeout of 2 seconds.
]
- Screen: "1.9 Technician Mode" → Screen: "15 Transferring Data to Back Office" [User taps
'Home Location'.
]
- Screen: "21.1 - Setting Home Location" → Screen: "21.2 New Home Location" [New Home Location
is set.
]
- Screen: "10.7 Card_Reader_Connected" → Decision: "Back to 'Supervisor Menu'." [User taps green tick or
timeout of 2 seconds.
]
- Decision: "Pairing 
Success?" → Screen: "10.8 Card_Reader_Not_Connected" [No]
- Screen: "10.3 Printer Connected" → Decision: "Back to 'Supervisor Menu'." [User taps green tick or
timeout of 2 seconds.
]
- Screen: "10.1.1 MAC Address entered" → Screen: "10.2 Connecting to printer" [User taps
'Connect' button.
]
- Decision: "Barcode scanned?" → Screen: "10.9 MAC Address Invalid" [Invalid address scanned.]
- Screen: "1.8 - Supervisor Menu" → Screen: "12.1 View/Print Versions" [User taps
'Versioning'.
]
- Screen: "10.8 Card_Reader_Not_Connected" → Decision: "Back to 'Connecting to card_reader - Connect via Bluetooth' screen." [User taps red cross or
timeout of 2 seconds.
]
- Screen: "12.1 View/Print Versions" → Decision: "Go to 'Versioning Print' flow." [User taps 'print' button.]
- Screen: "13.5 Payment Terminal - Details Saved" → Decision: "Back to 'Technician Menu'." [User taps green tick or
timeout of 2 seconds.
]
- Screen: "10.1 Enter MAC Address - field tapped" → Screen: "10.1.1 MAC Address entered" [User inputs
MAC Address.
]
- Screen: "21 Set Home Location" → Screen: "21.1 - Setting Home Location" [User taps a different
Home Location.
]
- Screen: "1.9 Technician Mode" → Decision: "Same as 'Supervisor Menu' flow." [User taps 'Pair with
Payment Device'.
]
- Screen: "13.3 Payment Terminal - Terminal ID Entered" → Screen: "13.4 Payment Terminal - Transaction Key Entered" [User inputs
Transaction Key
and taps off
alphanumeric keypad.
]
- Decision: "Is the Back Office
available?" → Screen: "15.1 Back Office Not Available" [No]
- Screen: "1.8 - Supervisor Menu" → Screen: "10 Enter MAC Address" [User taps
'Connect Printer'.
]
- Screen: "19.1 Supervisor Menu - Signed in On Duty - Glider" → Decision: "Go to 'Waybill Print' flow." [User taps 'End Duty'.]
- Screen: "15.1 Back Office Not Available" → Decision: "Back to 'Technician Menu'." [2 second timeout.]
- Decision: "Pairing 
Success?" → Screen: "10.6.1 Configuring Payment Device" [After the device pairs,
there is a back office
update to the device.
]
- Screen: "10.6.1 Configuring Payment Device" → Screen: "10.7 Card_Reader_Connected" [Once the update is completed...]
- Screen: "10.5 Connecting to card_reader - Connect via Bluetooth" → Screen: "10.6 Connecting to card_reader" [User taps
'Continue'.
]
- Screen: "11.2 View Waybill" → Decision: "Go to 'Waybill Print' flow." [User taps 'Print' button.]
- Screen: "1.8 - Supervisor Menu" → Screen: "10.5 Connecting to card_reader - Connect via Bluetooth" [User taps 'Pair with
Payment Device'.
]
- Screen: "11.1 View All Waybills" → Screen: "11.2 View Waybill" [User taps
a Waybill.
]
- Screen: "1.9 Technician Mode" → Decision: "Opens third party app." [User taps 'Configure Penalty
Fare Application'.
]
- Screen: "13.1 Payment Terminal - Blank" → Screen: "13.2 Payment Terminal - Terminal ID Selected" [User taps
'Terminal ID' field.
]
- Screen: "13.4 Payment Terminal - Transaction Key Entered" → Screen: "13.5 Payment Terminal - Details Saved" [User taps
'Continue' button.
]
- Screen: "1.9 Technician Mode" → Screen: "14 Printer Firmware - Applying" [User taps 'Apply
Printer Firmware'.
]
- Screen: "10 Enter MAC Address" → Decision: "Manual Entry or scan barcode?"
- Screen: "10.6 Connecting to card_reader" → Decision: "Pairing 
Success?"
- Decision: "Pairing 
Success?" → Screen: "10.6.1 Configuring Payment Device" [Yes]
- Screen: "10.4 Unable to Connect" → Decision: "Back to 'Enter MAC Address' screen." [3 second timeout or user taps the cross...]
- Decision: "Message of the Day available?" → Screen: "1.6.2 Login/Message of the Day/Error" [No]
- Decision: "Message of the Day available?" → Screen: "1.6.1 Login/Message of the Day" [Yes]
- Screen: "1.6.1 Login/Message of the Day" → Decision: "Go to 'Operator Menu'." [User taps
'Okay' button.
]
- Screen: "1.6.3 Login/Word of the Day - Loading" → Decision: "Word and Colour of the Day available?"
- Decision: "Word and Colour of the Day available?" → Screen: "1.6.5 Login/Word of the Day/Error" [No]
- Screen: "1.6.2 Login/Message of the Day/Error" → Decision: "Go to 'Operator Menu'." [Timeout of 3 seconds or the
user taps 'Okay' button.
]
- Decision: "Word and Colour of the Day available?" → Screen: "1.6.4 Login/Word of the Day" [Yes]
- Screen: "1.6 Login/Message of the Day - Loading" → Decision: "Message of the Day available?"
- Screen: "1.6.4 Login/Word of the Day" → Decision: "Go to 'Operator Menu'." [User taps
'Okay' button.]
- Screen: "1.6.5 Login/Word of the Day/Error" → Decision: "Go to 'Operator Menu'." [Timeout of 3 seconds or the
user taps 'Okay' button.]
- Screen: "1.8 - Supervisor Menu" → Screen: "1.6 Login/Message of the Day - Loading" [User taps 'Message of the Day'.]
- Screen: "1.8 - Supervisor Menu" → Screen: "1.6.3 Login/Word of the Day - Loading" [User taps 'Word and Colours of the Day'.]


## 7. 7. Barcode and mLink Scan

### Screens (34)
- 25.1.1 - Barcode Multi-use - Validation - Adult P2P
- 25.1.9 - Barcode Multi-use - Query - Adult P2P
- Barcode Reference 01 - Point-to-point rail
- 2.0 Sales Screen
- 25.2.1 - Barcode Multi-use - Validation - Child P2P
- 25.2.9 - Barcode Multi-use - Query - Child P2P
- Barcode Reference 02 - Point-to-Point Bus
- Barcode Reference 03 - Point-to-Point 3 Day Select
- 25.9.1 - Barcode Multi-Use - Failure - Passback
- 25.9.3 - Barcode Multi-Use - Failure - Invalid Time
- 25.9.5 - Barcode Multi-Use - Failure - Invalid Time
- 25.9.4 - Barcode Multi-Use - Failure - Invalid Location
- 25.3.1 - Barcode Multi-use - Validation - Conc P2P
- 25.4.9 - Barcode Multi-use - Query - Other P2P
- 25.9.2 - Barcode Multi-Use - Failure - Invalid Service
- 25.4.1 - Barcode Multi-use - Validation - Other P2P
- 25.3.9 - Barcode Multi-use - Query - Conc P2P
- 24.4.1 - Barcode Scan - Ticket Valid inc. Date and Depart Time
- 24.3 Barcode Scan - Validating Details
- 24.2.2 Barcode Scan - Transaction Cancelled - Ticket Not Valid
- 24.4.2 - Barcode Scan - Ticket Valid inc. Date with Expiry and Depart Time
- 24.4.4 - Barcode Scan - Ticket Valid inc. 3 Use Times
- 24.2.2 Barcode Scan - Transaction Cancelled - Ticket Not Valid
- 24.2.2 Barcode Scan - Transaction Cancelled - Ticket Not Valid
- 24.3.3 Barcode Scan - Redeeming
- 24.4.3 - Barcode Scan - Ticket Valid inc. Outbound ands Return
- 24.3.2 Barcode Scan - Offline Check
- 24 - Barcode Reference Entry
- 24.2.6 Barcode Scan - Transaction Cancelled - Ticket Not Passed Visual Inspection
- 24.2.2 Barcode Scan - Transaction Cancelled - Ticket Not Valid
- 24.2 Barcode Scan - Validation Failed
- 5.3 Operator Menu - Rail - Nothing to Annul
- 24.1 - Barcode Reference Entry - Field Tapped
- 24.1.1 - Barcode Reference Entry - Field Tapped - Number Entered

### Decision Points (44)
- Current location selected on HHD
- Barcode Display Description
- Barcode product vehicle type Will display either a Bus or Train symbol. (See variants)
- FLU Screen
- Barcode travel type - Zonal Variant Please see other variants for how P2P is displayed
- Barcode Expiry Displayed when present in the barcode and not 00:00. Please see also the 3 Day select variant.
- Barcode validation result icon
- Confirmation button to clear the screen and perform another function
- The product types represented within this flow are to demonstrate how certain products affect the colour profile of the screens.    Please see variant layouts to the right for other layouts that may occur.
- Is  Boarding/Alighting encoded in the Barcode?
- Product Type?
- Vehicle Type is checked.
- Current date/time is  >= "Start Date Time"  of barcode?
- Current date/time is  <= "End Date Time"  of barcode?
- Barcode is detected and scanned successfully
- Barcode is decrypted  and matches the 'Multi-Use' format?
- Check Unique ID field  is not within the configurable PassBacktime?
- Is barcode  product a 3 Day select?
- Is current date equal  to either Start/Additional/End  Date?
- Is product  valid on the current route?
- Is a Zone encoded in the Barcode?
- Is the current location the  same as or between the Boarding / Alighting locations?
- Does the current Zone match?
- Is the vehicle type valid  for the current route?
- Is current route Bus/Rail
- Is product value >=£90?
- Product Type?
- Back to 'Barcode Decryption check'
- Back to 'Sales' screen.
- Barcode is decrypted  and matches the 'Single-Use' format?
- Does the  Departure and Expiry date match?
- Is the barcode already offline validated?
- Online check available?
- Valid Barcode?
- Barcode Type U?
- Barcode Type B or E?
- Barcode Type D
- Is online validation still available?
- Redemption Successful?
- Go to 'Barcode Travel Ticket Print' Flow.
- Ticket value less than or equal to the configurable limit & the product is valid?
- Go to 'Barcode Travel Ticket Print' Flow.
- Operator Menu
- Back to 'Sales' screen.

### Annotations / Spec Notes (5)
- When a HHD loses internet connection and operator scans a barcode, the barcode number will be put on a list of offline validated barcodes so that it can't be validated offline again on that device. The list gets cleared as soon as the HHD device retrieves the connection and barcode records are sent to Cloudfare and CoreThree.
- Error could be: - The ticket is not valid - The ticket has already been used - The ticket is not valid on this date - The ticket has expired.
- Error could be:  - The ticket has already been offline validated
- Error will be: - Barcode decryption has failed
- Error could be: - The ticket value exceeds offline validation limit

### Connections / Flow (141)
- Screen: "2.0 Sales Screen" → Decision: "Barcode is detected and scanned successfully" [User press the 'Scan' button]
- Decision: "Barcode is detected and scanned successfully" → Decision: "Barcode is decrypted
 and matches the 'Multi-Use' format?" [Yes]
- Decision: "Barcode is detected and scanned successfully" → Screen: "2.0 Sales Screen" [No]
- Decision: "Barcode is decrypted
 and matches the 'Multi-Use' format?" → Decision: "Check Unique ID field 
is not within the configurable PassBacktime?" [Yes]
- Decision: "Check Unique ID field 
is not within the configurable PassBacktime?" → Screen: "25.9.1 - Barcode Multi-Use - Failure - Passback" [Unique ID is within 
the passback period
 the pasback period]
- Decision: "Check Unique ID field 
is not within the configurable PassBacktime?" → Decision: "Vehicle Type is checked." [Unique ID is not within
 the pasback period]
- Decision: "Vehicle Type is checked." → Decision: "Current date/time is 
>= "Start Date Time"
 of barcode?" [All]
- Decision: "Vehicle Type is checked." → Decision: "Is the vehicle type valid
 for the current route?" [Rail]
- Decision: "Vehicle Type is checked." → Decision: "Is the vehicle type valid
 for the current route?" [Bus]
- Decision: "Is the vehicle type valid
 for the current route?" → Decision: "Current date/time is 
>= "Start Date Time"
 of barcode?" [Yes]
- Decision: "Is the vehicle type valid
 for the current route?" → Screen: "25.9.2 - Barcode Multi-Use - Failure - Invalid Service" [No
]
- Decision: "Current date/time is 
>= "Start Date Time"
 of barcode?" → Screen: "25.9.3 - Barcode Multi-Use - Failure - Invalid Time" [No]
- Decision: "Current date/time is 
>= "Start Date Time"
 of barcode?" → Decision: "Current date/time is 
<= "End Date Time"
 of barcode?" [Yes]
- Decision: "Current date/time is 
<= "End Date Time"
 of barcode?" → Screen: "25.9.5 - Barcode Multi-Use - Failure - Invalid Time" [No]
- Decision: "Current date/time is 
<= "End Date Time"
 of barcode?" → Decision: "Is barcode
 product a 3 Day select?" [Yes]
- Decision: "Is current date equal 
to either Start/Additional/End 
Date?" → Screen: "25.9.3 - Barcode Multi-Use - Failure - Invalid Time" [No]
- Decision: "Is current date equal 
to either Start/Additional/End 
Date?" → Decision: "Is product 
valid on the current route?" [Yes]
- Decision: "Is product 
valid on the current route?" → Screen: "25.9.2 - Barcode Multi-Use - Failure - Invalid Service" [No]
- Decision: "Is product 
valid on the current route?" → Decision: "Is a Zone encoded in the Barcode?" [Yes]
- Decision: "Is a Zone encoded in the Barcode?" → Decision: "Does the current Zone match?" [Yes]
- Decision: "Is a Zone encoded in the Barcode?" → Decision: "Is 
Boarding/Alighting encoded in the Barcode?" [No]
- Decision: "Does the current Zone match?" → Decision: "Is 
Boarding/Alighting encoded in the Barcode?" [Yes]
- Decision: "Does the current Zone match?" → Screen: "25.9.4 - Barcode Multi-Use - Failure - Invalid Location" [No]
- Decision: "Is 
Boarding/Alighting encoded in the Barcode?" → Decision: "Is the current location the 
same as or between the Boarding / Alighting locations?" [Yes]
- Decision: "Is 
Boarding/Alighting encoded in the Barcode?" → Decision: "Product Type?" [No]
- Decision: "Is the current location the 
same as or between the Boarding / Alighting locations?" → Decision: "Is current route Bus/Rail" [No]
- Decision: "Is the current location the 
same as or between the Boarding / Alighting locations?" → Decision: "Product Type?" [Yes]
- Decision: "Is current route Bus/Rail" → Decision: "Is product value >=£90?" [CR105]
- Decision: "Is current route Bus/Rail" → Decision: "Product Type?" [Bus
]
- Decision: "Is current route Bus/Rail" → Screen: "25.9.4 - Barcode Multi-Use - Failure - Invalid Location" [Rail]
- Decision: "Is product value >=£90?" → Decision: "Product Type?" [Yes]
- Decision: "Product Type?" → Screen: "25.1.1 - Barcode Multi-use - Validation - Adult P2P" [Adult]
- Decision: "Product Type?" → Screen: "25.2.1 - Barcode Multi-use - Validation - Child P2P" [Child]
- Decision: "Product Type?" → Screen: "25.3.1 - Barcode Multi-use - Validation - Conc P2P" [Other]
- Decision: "Product Type?" → Screen: "25.4.1 - Barcode Multi-use - Validation - Other P2P" [Concession]
- Screen: "25.9.1 - Barcode Multi-Use - Failure - Passback" → Decision: "Back to 'Barcode Decryption check'" [User presses the
  'Scan' button]
- Screen: "25.9.3 - Barcode Multi-Use - Failure - Invalid Time" → Decision: "Back to 'Barcode Decryption check'" [User presses the
  'Scan' button]
- Screen: "25.9.2 - Barcode Multi-Use - Failure - Invalid Service" → Decision: "Back to 'Barcode Decryption check'" [User presses the
  'Scan' button]
- Screen: "25.9.4 - Barcode Multi-Use - Failure - Invalid Location" → Decision: "Back to 'Barcode Decryption check'" [User presses the
  'Scan' button]
- Screen: "25.9.1 - Barcode Multi-Use - Failure - Passback" → Decision: "Back to 'Sales' screen." [3 second
timeout]
- Screen: "25.9.3 - Barcode Multi-Use - Failure - Invalid Time" → Decision: "Back to 'Sales' screen." [3 second
timeout]
- Screen: "25.9.2 - Barcode Multi-Use - Failure - Invalid Service" → Decision: "Back to 'Sales' screen." [3 second
timeout]
- Screen: "25.9.4 - Barcode Multi-Use - Failure - Invalid Location" → Decision: "Back to 'Sales' screen." [3 second
timeout]
- Screen: "25.1.1 - Barcode Multi-use - Validation - Adult P2P" → Decision: "Back to 'Barcode Decryption check'" [User presses the
  'Scan' button]
- Screen: "25.2.1 - Barcode Multi-use - Validation - Child P2P" → Decision: "Back to 'Barcode Decryption check'" [User presses the
  'Scan' button]
- Screen: "25.3.1 - Barcode Multi-use - Validation - Conc P2P" → Decision: "Back to 'Barcode Decryption check'" [User presses the
  'Scan' button]
- Screen: "25.4.1 - Barcode Multi-use - Validation - Other P2P" → Decision: "Back to 'Barcode Decryption check'" [User presses the
  'Scan' button]
- Decision: "Barcode is decrypted
 and matches the 'Multi-Use' format?" → Decision: "Barcode is decrypted
 and matches the 'Single-Use' format?" [No]
- Screen: "24.1.1 - Barcode Reference Entry - Field Tapped - Number Entered" → Screen: "24.3 Barcode Scan - Validating Details" [User taps
'Confirm'.
]
- Screen: "24.4.1 - Barcode Scan - Ticket Valid inc. Date and Depart Time" → Decision: "Is online validation still available?" [Ticket passes visual 
inspection so the 
operator selects 'Valid']
- Decision: "Valid Barcode?" → Screen: "24.2.2 Barcode Scan - Transaction Cancelled - Ticket Not Valid" [No]
- Screen: "24.1 - Barcode Reference Entry - Field Tapped" → Screen: "24.1.1 - Barcode Reference Entry - Field Tapped - Number Entered" [User inputs
reference.
]
- Decision: "Online check available?" → Screen: "24.3.2 Barcode Scan - Offline Check" [No]
- Screen: "24.3 Barcode Scan - Validating Details" → Decision: "Is the barcode already
offline validated?"
- Decision: "Ticket value less than or
equal to the configurable limit & the product is valid?" → Screen: "24.2 Barcode Scan - Validation Failed" [No]
- Decision: "Is online validation still available?" → Screen: "24.3.3 Barcode Scan - Redeeming" [Yes
]
- Decision: "Is online validation still available?" → Decision: "Go to 'Barcode Travel Ticket Print' Flow." [No - store offline validation
in the background.
]
- Screen: "24.3.2 Barcode Scan - Offline Check" → Decision: "Ticket value less than or
equal to the configurable limit & the product is valid?"
- Screen: "24.2 Barcode Scan - Validation Failed" → Screen: "24.3 Barcode Scan - Validating Details" [Userselectss
'Retry'
]
- Decision: "Is the barcode already
offline validated?" → Decision: "Online check available?" [No]
- Decision: "Online check available?" → Decision: "Valid Barcode?" [Yes]
- Decision: "Ticket value less than or
equal to the configurable limit & the product is valid?" → Decision: "Valid Barcode?" [Yes]
- Decision: "Valid Barcode?" → Decision: "Barcode Type U?" [Yes]
- Screen: "24.4.1 - Barcode Scan - Ticket Valid inc. Date and Depart Time" → Screen: "24.2.6 Barcode Scan - Transaction Cancelled - Ticket Not Passed Visual Inspection" [Ticket does not pass visual 
inspection so the 
operator selects 'Not Valid']
- Decision: "Barcode is decrypted
 and matches the 'Single-Use' format?" → Screen: "24.2.2 Barcode Scan - Transaction Cancelled - Ticket Not Valid" [No]
- Decision: "Barcode is decrypted
 and matches the 'Single-Use' format?" → Screen: "24.3 Barcode Scan - Validating Details" [Yes]
- Screen: "24.2.2 Barcode Scan - Transaction Cancelled - Ticket Not Valid" → Decision: "Back to 'Sales' screen." [Timeout 3 seconds]
- Decision: "Back to 'Sales' screen." → Screen: "2.0 Sales Screen"
- Screen: "25.9.5 - Barcode Multi-Use - Failure - Invalid Time" → Decision: "Back to 'Sales' screen." [3 second
timeout]
- Decision: "Is the barcode already
offline validated?" → Screen: "24.2.2 Barcode Scan - Transaction Cancelled - Ticket Not Valid" [Yes]
- Screen: "24.2.2 Barcode Scan - Transaction Cancelled - Ticket Not Valid" → Decision: "Back to 'Sales' screen." [3 Second Timeout]
- Screen: "24.2 Barcode Scan - Validation Failed" → Decision: "Back to 'Sales' screen." [User selects Cancel]
- Screen: "24.2.6 Barcode Scan - Transaction Cancelled - Ticket Not Passed Visual Inspection" → Decision: "Back to 'Sales' screen." [3 second timeout.]
- Decision: "Barcode Type U?" → Decision: "Does the
 Departure and Expiry date match?" [Yes]
- Decision: "Does the
 Departure and Expiry date match?" → Screen: "24.4.1 - Barcode Scan - Ticket Valid inc. Date and Depart Time" [Yes]
- Decision: "Does the
 Departure and Expiry date match?" → Screen: "24.4.2 - Barcode Scan - Ticket Valid inc. Date with Expiry and Depart Time" [No]
- Screen: "24.4.2 - Barcode Scan - Ticket Valid inc. Date with Expiry and Depart Time" → Decision: "Is online validation still available?" [Ticket passes visual 
inspection so the 
operator selects 'Valid']
- Decision: "Barcode Type U?" → Decision: "Barcode Type B or E?" [No]
- Decision: "Barcode Type B or E?" → Screen: "24.4.1 - Barcode Scan - Ticket Valid inc. Date and Depart Time" [Yes]
- Decision: "Barcode Type D" → Screen: "24.4.4 - Barcode Scan - Ticket Valid inc. 3 Use Times" [Yes]
- Decision: "Barcode Type B or E?" → Decision: "Barcode Type D" [No]
- Decision: "Barcode Type D" → Screen: "24.4.3 - Barcode Scan - Ticket Valid inc. Outbound ands Return" [Barcode Type is H or S]
- Screen: "24.4.4 - Barcode Scan - Ticket Valid inc. 3 Use Times" → Decision: "Is online validation still available?" [Ticket passes visual 
inspection so the 
operator selects 'Valid']
- Screen: "24.4.4 - Barcode Scan - Ticket Valid inc. 3 Use Times" → Screen: "24.2.6 Barcode Scan - Transaction Cancelled - Ticket Not Passed Visual Inspection" [Ticket does not pass visual 
inspection so the 
operator selects 'Not Valid']
- Screen: "24.4.3 - Barcode Scan - Ticket Valid inc. Outbound ands Return" → Decision: "Is online validation still available?" [Ticket passes visual 
inspection so the 
operator selects 'Valid']
- Screen: "24.4.3 - Barcode Scan - Ticket Valid inc. Outbound ands Return" → Screen: "24.2.6 Barcode Scan - Transaction Cancelled - Ticket Not Passed Visual Inspection" [Ticket does not pass visual 
inspection so the 
operator selects 'Not Valid']
- Screen: "24.4.2 - Barcode Scan - Ticket Valid inc. Date with Expiry and Depart Time" → Screen: "24.2.6 Barcode Scan - Transaction Cancelled - Ticket Not Passed Visual Inspection" [Ticket does not pass visual 
inspection so the 
operator selects 'Not Valid']
- Screen: "24.2.2 Barcode Scan - Transaction Cancelled - Ticket Not Valid" → Decision: "Back to 'Sales' screen." [3 second timeout.]
- Decision: "Back to 'Sales' screen." → Screen: "2.0 Sales Screen"
- Screen: "24.1.1 - Barcode Reference Entry - Field Tapped - Number Entered" → Decision: "Back to 'Sales' screen." [User taps 'Cancel' button.]
- Decision: "Product Type?" → Screen: "25.1.9 - Barcode Multi-use - Query - Adult P2P" [Adult]
- Decision: "Product Type?" → Screen: "25.2.9 - Barcode Multi-use - Query - Child P2P" [Child]
- Decision: "Product Type?" → Screen: "25.4.9 - Barcode Multi-use - Query - Other P2P" [Pink]
- Decision: "Product Type?" → Screen: "25.3.9 - Barcode Multi-use - Query - Conc P2P" [Purple]
- Screen: "25.1.9 - Barcode Multi-use - Query - Adult P2P" → Decision: "Back to 'Barcode Decryption check'" [User presses the
  'Scan' button]
- Screen: "25.2.9 - Barcode Multi-use - Query - Child P2P" → Decision: "Back to 'Barcode Decryption check'" [User presses the
  'Scan' button]
- Screen: "25.4.9 - Barcode Multi-use - Query - Other P2P" → Decision: "Back to 'Barcode Decryption check'" [User presses the
  'Scan' button]
- Screen: "25.3.9 - Barcode Multi-use - Query - Conc P2P" → Decision: "Back to 'Barcode Decryption check'" [User presses the
  'Scan' button]
- Screen: "25.1.1 - Barcode Multi-use - Validation - Adult P2P" → Decision: "Back to 'Sales' screen." [2 second
timeout]
- Screen: "25.2.1 - Barcode Multi-use - Validation - Child P2P" → Decision: "Back to 'Sales' screen." [2 second
timeout]
- Screen: "25.3.1 - Barcode Multi-use - Validation - Conc P2P" → Decision: "Back to 'Sales' screen." [2 second
timeout]
- Screen: "25.4.1 - Barcode Multi-use - Validation - Other P2P" → Decision: "Back to 'Sales' screen." [2 second
timeout]
- Screen: "25.1.9 - Barcode Multi-use - Query - Adult P2P" → Decision: "Back to 'Sales' screen." [3 second
timeout]
- Screen: "25.2.9 - Barcode Multi-use - Query - Child P2P" → Decision: "Back to 'Sales' screen." [3 second
timeout]
- Screen: "25.4.9 - Barcode Multi-use - Query - Other P2P" → Decision: "Back to 'Sales' screen." [3 second
timeout]
- Screen: "25.3.9 - Barcode Multi-use - Query - Conc P2P" → Decision: "Back to 'Sales' screen." [3 second
timeout]
- Screen: "25.9.1 - Barcode Multi-Use - Failure - Passback" → Decision: "Back to 'Sales' screen." [User selects
 'Confirm']
- Screen: "25.9.3 - Barcode Multi-Use - Failure - Invalid Time" → Decision: "Back to 'Sales' screen." [User selects
 'Confirm']
- Screen: "25.9.2 - Barcode Multi-Use - Failure - Invalid Service" → Decision: "Back to 'Sales' screen." [User selects
 'Confirm']
- Screen: "25.9.5 - Barcode Multi-Use - Failure - Invalid Time" → Decision: "Back to 'Sales' screen." [User selects
 'Confirm']
- Screen: "25.9.4 - Barcode Multi-Use - Failure - Invalid Location" → Decision: "Back to 'Sales' screen." [User selects
 'Confirm']
- Screen: "25.4.1 - Barcode Multi-use - Validation - Other P2P" → Decision: "Back to 'Sales' screen."
- Screen: "25.3.9 - Barcode Multi-use - Query - Conc P2P" → Decision: "Back to 'Sales' screen." [User selects
 'Confirm']
- Screen: "25.4.9 - Barcode Multi-use - Query - Other P2P" → Decision: "Back to 'Sales' screen." [User selects
 'Confirm']
- Screen: "25.3.1 - Barcode Multi-use - Validation - Conc P2P" → Decision: "Back to 'Sales' screen."
- Screen: "25.2.1 - Barcode Multi-use - Validation - Child P2P" → Decision: "Back to 'Sales' screen."
- Screen: "25.2.9 - Barcode Multi-use - Query - Child P2P" → Decision: "Back to 'Sales' screen." [User selects
 'Confirm']
- Screen: "25.1.1 - Barcode Multi-use - Validation - Adult P2P" → Decision: "Back to 'Sales' screen."
- Screen: "25.1.9 - Barcode Multi-use - Query - Adult P2P" → Decision: "Back to 'Sales' screen." [User selects
 'Confirm']
- Decision: "Is barcode
 product a 3 Day select?" → Decision: "Is current date equal 
to either Start/Additional/End 
Date?" [Yes]
- Decision: "Is barcode
 product a 3 Day select?" → Decision: "Is product 
valid on the current route?" [No]
- Decision: "Back to 'Barcode Decryption check'" → Decision: "Barcode is detected and scanned successfully"
- Screen: "25.9.5 - Barcode Multi-Use - Failure - Invalid Time" → Decision: "Back to 'Barcode Decryption check'" [User presses the
  'Scan' button]
- Decision: "Is product value >=£90?" → Screen: "25.9.4 - Barcode Multi-Use - Failure - Invalid Location" [No]
- Screen: "5.3 Operator Menu - Rail - Nothing to Annul" → Screen: "24.1 - Barcode Reference Entry - Field Tapped"
- Screen: "24 - Barcode Reference Entry" → Decision: "e2b1abf5-7303-406f-bca1-e3312a518647" [User selects the 
Cancel option]
- Screen: "24.1 - Barcode Reference Entry - Field Tapped" → Screen: "24 - Barcode Reference Entry" [User selects the
 background or 
presses the 'Back' button
to hide the keyboard]
- Screen: "24 - Barcode Reference Entry" → Screen: "24.1 - Barcode Reference Entry - Field Tapped" [User selects the entry 
field or presses the 'Back'
button ]
- Screen: "Barcode Reference 01 - Point-to-point rail" → Decision: "Current location selected on HHD"
- Screen: "Barcode Reference 01 - Point-to-point rail" → Decision: "Barcode Display Description"
- Screen: "Barcode Reference 01 - Point-to-point rail" → Decision: "Barcode travel type - Zonal Variant
Please see other variants for how P2P is displayed"
- Screen: "Barcode Reference 01 - Point-to-point rail" → Decision: "Barcode Expiry
Displayed when present in the barcode and not 00:00.
Please see also the 3 Day select variant."
- Screen: "Barcode Reference 01 - Point-to-point rail" → Decision: "Barcode validation result icon"
- Screen: "Barcode Reference 01 - Point-to-point rail" → Decision: "Barcode product vehicle type
Will display either a Bus or Train symbol. (See variants)"
- Screen: "Barcode Reference 01 - Point-to-point rail" → Decision: "Confirmation button to clear the screen and perform another function"
- Decision: "Barcode Expiry
Displayed when present in the barcode and not 00:00.
Please see also the 3 Day select variant." → Screen: "Barcode Reference 03 - Point-to-Point 3 Day Select"
- Decision: "Barcode product vehicle type
Will display either a Bus or Train symbol. (See variants)" → Screen: "Barcode Reference 02 - Point-to-Point Bus"
- Screen: "24.3.3 Barcode Scan - Redeeming" → Decision: "Redemption Successful?"
- Decision: "Redemption Successful?" → Decision: "Go to 'Barcode Travel Ticket Print' Flow." [Yes]
- Decision: "Redemption Successful?" → Screen: "24.2.2 Barcode Scan - Transaction Cancelled - Ticket Not Valid" [No]
- Screen: "24.2.2 Barcode Scan - Transaction Cancelled - Ticket Not Valid" → Decision: "Back to 'Sales' screen." [3 second timeout.]


## 8. 8. Additional Features

### Screens (10)
- 27. Updating Payment Device
- 1.1.2 Login/Device Out of Service
- 18.1 Remotely Locked
- 1.4.3 Login/Communications Locked
- 18 Remotely Out of Service
- 15.1 Limit Approaching
- 15.1.1 Limit Approaching - Rail
- 15.2 Limit Reached
- 16 Device Docked
- 23 Fares Updating

### Decision Points (9)
- HHD - Out of Service
- HHD - Remotely Locked
- HHD - Comms Locked
- HHD - Device Remotely Out of Service
- HHD - Payment Device Updating
- HHD - Device Docked
- HHD - Limit Approaching and Reached
- HHD - Fares Updating
- HHD - Dual Inspection/Validation support

### Annotations / Spec Notes (7)
- The payment device can update at any time, so while this occurs there will be a fullscreen update.  The operator will be able to perform actions on the HHD device, however will not be able to use the payment device until the update is completed.
- If the HHD runs into a critical issue, either on start-up or during use, it will default to this screen and become unusable until a technician or some other stated action has fixed the issue.
- Notification at the bottom is presented when a pre-configured amount is reached. The amount remaining until the revenue limit is reached is presented on the left.
- Once the revenue limit is reached, the operator will be singed off and a waybill will  be printed. To unlock the device, the device will have to be docked and Back Office connection using ethernet will have to be established.
- When the device is docked, this screen is displayed. If it needs to do an update, the update icon is shown; otherwise it will just be the 'Device Docked' message.  This screen is displayed in 2 cases;  1) when the software is scheduled for an immediate download & update and device is on the docking station   and  2) when the software was scheduled for an update in the future.   In the second case the device does not have to be docked during the update.  The screen will disappear once the software is updated and Idle (Log in) screen will be displayed
- This screen is required for transition from current to future fares. This will only happen if device on LogOn screen.
- Communications are locked after x amount of hours of HHD not communicating with CloudFare

### Connections / Flow (0)


## 9. 9. Inspection & Validation V2

### Screens (47)
- 2.0.6 Sales Screen - Rail- Inspection - Device View
- 2.0 Sales Screen - Inspection - Device View
- 2.0.6 Sales Screen - Rail- Validation - Device View
- 3.4.2-Revenue Inspect - Success
- 3.3 Error - Read/Write Fail
- 3.4.1.2 Revenue Inspect - Connecting
- 3.4 Revenue Inspect - Card Prompt
- 3.3 Error - Read/Write Fail
- 2.0.9 Select Boarding - List - Numerical Search
- 2.0.7 Select Boarding - List - HHD Screen Size
- 3.4.1-Revenue Inspect - Processing
- 3.4.4.1-Revenue Inspect - Failure - Denylist
- 3.4.4.2-Revenue Inspect - Failure - Declined
- 3.4.3-Revenue Inspect - Failure - Disconnected
- 2.5.4.2 Error - Passback
- 2.5.4.2 Error - Passback
- 3.3.1 Error
- 3.3.1 Error
- 3.2.3 Smartcard Not Valid - No Travel Remaining
- 4.2.2 Top Up - iLink - Select Product
- 2.4.0.1 Payment Area - No Warrant
- 8.4 Present Smart Card
- 3.2.1 Inspection - Invalid - Warning
- 3.1 Inspection - Valid
- 2.6.7 Validation - Success
- 3.2 Inspection - Invalid
- 2.6 Discount - Sales mode (yLink)
- 2.6.0.1 Discount - Sales mode - Alighting Selected (yLink)
- 2.4 Payment Area (Glider)
- 2.6.2 Discount - Summary (yLink)
- 2.6.1 - Discount - Sales mode - Select Product - Rail - yLink
- 2.6.1 Discount - Sales mode - Rail
- 2.6.2 Discount - Summary (yLink)
- 2.4 Payment Area
- 4.4 Represent Smartcard
- 2.5.4.1 Critical Error
- 4.6 Voiding Last Card Transaction
- 2.6.5 Concessionary Card - Sales mode
- 8.5 Printing Receipt - Cash
- 2.4.3.1 Transaction complete
- 3.2.2 Successful Validation
- 2.6.7 Validation - Success
- 7.2 Print Failed
- 4.1.2 Critical Error - Invalid Card
- 4.6 Voiding Last Card Transaction
- 2.6.1 - Discount - Sales mode - Select Product - SeniorXB
- 2.6.5.1 Concessionary Card - Sales mode - Rail

### Decision Points (73)
- HHD remains in inspection mode
- Revenue Inspection can be triggered by pressing the square button. Note: This function is only available via the Sales Mode screen. The button will be unresponsive on any other screen.
- HHD - Revenue Inspection
- HHD - Validation Mode & Expired Card Top Up
- HHD - Inspection Mode & Card Validation
- Smartcard Readable?
- Smartcard Readable?
- Back to Sales screen.
- Back to Sales screen.
- Back to Sales screen.
- Back to Sales screen.
- Go back to previous screen.
- Go to 'Top Up Receipt Print' flow.
- Go to 'Top Up Receipt Print' flow.
- Back to Sales screen.
- Payment Device has  BOS connectivity?
- Inspection Success?
- Back to Sales screen.
- Is passback configured?
- Is passback configured?
- Back to Sales screen.
- Smartcard Last Used  within passback period?
- Smartcard Last Used  within passback period?
- Back to 'Sales' screen.
- Back to 'Sales' screen.
- Back to Sales screen.
- Back to Sales screen.
- Go to Penalty Warning print flow.
- Passed pre-validation checks?
- Smartcard Valid?
- A third party app opens. A Penalty Fare ticket also prints.
- Back to Sales screen.
- Back to 'Sales' screen.
- Back to Sales screen.
- User chooses to issue a penalty fare and third party app opens. A Penalty Fare ticket also prints.
- Go to Penalty Warning print flow.
- Back to 'Sales' screen.
- Back to Sales screen.
- Back to Sales screen.
- See Card Payment flow.
- Has the smartcard been previously  validated?
- Does the direction  of travel match the current route?
- Is 'Last Use'  within the transfer period? (<90 minutes)
- Does the direction  of travel match the current route?
- Glider/Rail?
- Back to Sales screen.
- Smartcard Type Commercial/Staff/EA?
- Glider/Rail?
- Back to 'Sales' screen.
- Smartcard Type Discounted Fare  Validation?
- Half-Fare?
- yLink Validation?
- Glider/Rail?
- See Card Payment flow.
- Go to relevant 'Cash / Payment Card Print Flow' flow.
- See Card Payment flow.
- Glider/Rail?
- Smartcard Readable?
- Go to the 'Card Payment Receipt Print' flow.
- Payment card used?
- Back to 'Sales' screen.
- Back to 'Represent Smartcard' screen.
- Smartcard Type Concession Fare  Validation
- Glider/Rail?
- Valid top-up card?
- Able to print?
- Back to 'Sales' screen.
- Go to the 'Card Payment Receipt Print' flow.
- Cross Border?
- Back to 'Represent Smartcard' screen.
- If no other Ticket Types are available the HHD will remain on the current screen
- Payment card used?
- Back to 'Sales' screen.

### Annotations / Spec Notes (21)
- Top-up is iLink only. Validation includes iLink, Staff, Spouse, Retired, External and aLink.
- Revenue inspection is available only from the Sales Mode screen.  Once Revenue Inspection mode is initiated the payment device needs to be woken up and connected to the HHD. Once connected the payment device needs to be kept awake for as long as the Inspection prompt and/or Revenue Inspection result  screens are displayed. This is to allow for sequential inspections.  Whilst Revenue Inspection mode is inititiated barcode scanning and smartcard validation will be disabled until returning to Sales Mode.
- Screen will timeout after 2s before  returning to card prompt screen.
- At any time the HHD needs to connect to the  card reading device this screen will be displayed untill the connection has been established.  Screen will timeout after 60s before returning  to Sales screen.
- In revenue inspection mode the inspector  may choose to change their boarding location  by selecting either the stage number or name.  The stage can also be changed by swiping the  name left or right to go forward or back on  the route respectively.  The route can not be changed from this screen.  Screen will timeout after 30s before  returning to Sales screen.
- Whilst changing boarding location the HHD is still functionally in revenue inspection mode at the currently selected location if a card is presented to the payment device.  Barcode/smartcard functionally will remain unavailable and the 30 second timeout will still return to sales screen.
- Previous screens may be:   * 2.0 Sales Screen - Inspection   * 2.0.6 Sales Screen - Rail - Inspection   * 2.6.5 Concessionary Card - Sales mode
- Screen will timeout after 3s before  returning to card prompt screen.  If a reason for failure is not due to a  Denylist the same layout will be used with an appropriate message displayed. (see generic example)
- Screen will timeout after 3s before  returning to card prompt screen.
- N.B. Error message could read: - Not valid at this location - Hotlisted Card - Product Expired
- 'Error Message' will read:  - Product Expired - Pass Expired - No Journeys Left - No Balance Left - Hotlisted Card - Visual Rejection
- 'Penalty Fare' option may be disabled if the Penalty Fare App is not available, the printer is disconnected or the Smartcard product is valid for free travel.
- Expiry, Last Used Dates and Direction may show as N/A when not available/applicable.
- On validation, a Transaction Record is sent to the back office.
- Expiry, Last Used Dates and Direction may show as N/A when not available/applicable.
- Warrant is used for paper tickets only, not top-ups. They will appear on Waybills and are available on Rail only.
- N.B. '£Price change' header will only show if cash was the payment method, otherwise card payment screen will display instead - this will be 1 of 2 for print due to additional receipts for card payment.  Print will still go through same checks seen in Print flows.
- For a card payment, there will be a check to see if you also want to print the customer receipt as seen in the 'Payment Card Print' flow.
- Other cards will display the tick and then        [PRODUCT NAME]              Validated  below the tick.  See 'Validation Successful' screen on the Rail flow for reference.
- On validation, a Transaction Record is sent to the back office.
- 1. For Dependants Pass, Senior, Blind, War Pensioner, 60+ and ROI Senior single is the only product option for local travel i.e. where boarding station and alighting station are both 61 or less.    2. For Senior, Blind, War Pensioner and ROI Senior XB single, XB day return and XB 1 month return are the product options for Cross border travel i.e. where boarding station or alighting station are greater than 61.

### Connections / Flow (149)
- Screen: "2.4.0.1 Payment Area - No Warrant" → Screen: "4.4 Represent Smartcard" [User selects a Cash value]
- Screen: "3.3.1 Error" → Decision: "Go to Penalty Warning print flow." [User taps
'Penalty Warning'.
A Penalty Warning ticket prints.
]
- Screen: "3.3.1 Error" → Decision: "A third party app opens.
A Penalty Fare ticket also prints." [User taps 'Penalty Fare'.]
- Decision: "Payment card used?" → Decision: "Back to 'Sales' screen." [No]
- Decision: "Valid top-up card?" → Screen: "4.1.2 Critical Error - Invalid Card" [No
]
- Screen: "2.6.7 Validation - Success" → Decision: "Back to 'Sales' screen."
- Decision: "See Card Payment flow." → Screen: "4.4 Represent Smartcard" [Successful card
payment.
]
- Decision: "Able to print?" → Screen: "7.2 Print Failed" [No]
- Decision: "Payment card used?" → Screen: "4.6 Voiding Last Card Transaction" [Yes]
- Screen: "3.2.3 Smartcard Not Valid - No Travel Remaining" → Screen: "4.2.2 Top Up - iLink - Select Product" [User taps 'Top-Up'.]
- Decision: "Smartcard Valid?" → Screen: "3.3.1 Error" [No - Travel is prohibited]
- Decision: "Smartcard Valid?" → Decision: "Smartcard Type
Commercial/Staff/EA?" [Yes - valid.]
- Decision: "Valid top-up card?" → Screen: "8.5 Printing Receipt - Cash" [Yes]
- Decision: "A third party app opens.
A Penalty Fare ticket also prints." → Decision: "Back to 'Sales' screen."
- Screen: "2.4.0.1 Payment Area - No Warrant" → Decision: "See Card Payment flow." [User taps
'Card' button.
]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Payment card used?" [User taps
'Cancel' button.
]
- Decision: "Go to Penalty Warning print flow." → Decision: "Back to Sales screen." [Once the Print
flow is complete...
]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Back to 'Represent Smartcard' screen." [User taps 'Retry' button.]
- Decision: "Able to print?" → Screen: "2.4.3.1 Transaction complete" [Yes]
- Screen: "2.5.4.1 Critical Error" → Decision: "Payment card used?" [User taps 'Cancel' button.]
- Screen: "2.5.4.1 Critical Error" → Decision: "Back to 'Represent Smartcard' screen." [User taps 'Retry' button.]
- Screen: "3.3.1 Error" → Decision: "Back to Sales screen."
- Screen: "4.6 Voiding Last Card Transaction" → Decision: "Go to the 'Card Payment Receipt Print' flow."
- Decision: "Payment card used?" → Screen: "4.6 Voiding Last Card Transaction" [Yes]
- Decision: "Go to 'Top Up Receipt Print' flow." → Decision: "Back to Sales screen." [Once the Print flow is complete...]
- Screen: "3.2.3 Smartcard Not Valid - No Travel Remaining" → Decision: "Back to Sales screen." [User taps 'Cancel'.]
- Decision: "Smartcard
Readable?" → Screen: "2.5.4.1 Critical Error" [No]
- Screen: "8.5 Printing Receipt - Cash" → Decision: "Able to print?"
- Decision: "Payment card used?" → Decision: "Back to 'Sales' screen." [No]
- Screen: "4.2.2 Top Up - iLink - Select Product" → Screen: "2.4.0.1 Payment Area - No Warrant" [iLink product
selected.
]
- Decision: "Smartcard
Readable?" → Decision: "Valid top-up card?" [Yes]
- Screen: "4.6 Voiding Last Card Transaction" → Decision: "Go to the 'Card Payment Receipt Print' flow."
- Screen: "2.6.7 Validation - Success" → Decision: "Back to 'Sales' screen."
- Decision: "Smartcard Valid?" → Screen: "3.2.3 Smartcard Not Valid - No Travel Remaining" [No - No travel
remaining.
]
- Decision: "Smartcard Readable?" → Screen: "3.3 Error - Read/Write Fail" [No]
- Screen: "2.4.3.1 Transaction complete" → Screen: "3.2.2 Successful Validation" [3 second
timeout...
]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go back to previous screen." [User taps 'Retry'.]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Top Up Receipt Print' flow." [User taps 'Faulty Smartpass'.]
- Screen: "7.2 Print Failed" → Screen: "3.2.2 Successful Validation" [User taps
'Continue Without
Printing' button.
]
- Screen: "3.2.2 Successful Validation" → Screen: "2.6.7 Validation - Success"
- Screen: "2.0 Sales Screen - Inspection - Device View" → Decision: "HHD remains in inspection mode" [User swipes Inspection 
to change mode]
- Screen: "2.0.6 Sales Screen - Rail- Inspection - Device View" → Screen: "2.0.6 Sales Screen - Rail- Validation - Device View" [User swipes Inspection 
to engage Validation mode]
- Screen: "2.0.6 Sales Screen - Rail- Validation - Device View" → Screen: "2.0.6 Sales Screen - Rail- Inspection - Device View" [User swipes Validation 
to engage Inspection mode]
- Screen: "2.0 Sales Screen - Inspection - Device View" → Decision: "Smartcard Readable?" [User presents a smartcard]
- Screen: "2.0.6 Sales Screen - Rail- Inspection - Device View" → Decision: "Smartcard Readable?" [User presents a smartcard]
- Decision: "Smartcard Readable?" → Decision: "Is passback configured?" [Yes]
- Decision: "Smartcard Last Used 
within passback period?" → Decision: "Passed pre-validation
checks?" [No]
- Decision: "Passed pre-validation
checks?" → Decision: "Has the smartcard
been previously 
validated?" [Yes]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Back to Sales screen." [User taps Cancel]
- Decision: "User chooses to issue a penalty fare and third party app opens.
A Penalty Fare ticket also prints." → Decision: "Back to 'Sales' screen."
- Decision: "Go to Penalty Warning print flow." → Decision: "Back to Sales screen." [Once the Print
flow is complete...
]
- Decision: "Passed pre-validation
checks?" → Screen: "3.3.1 Error" [No]
- Decision: "Smartcard Last Used 
within passback period?" → Screen: "2.5.4.2 Error - Passback" [Yes]
- Screen: "2.5.4.2 Error - Passback" → Decision: "Back to 'Sales' screen."
- Decision: "Has the smartcard
been previously 
validated?" → Screen: "3.2 Inspection - Invalid" [No]
- Decision: "Does the direction 
of travel match the current route?" → Screen: "3.1 Inspection - Valid" [Yes]
- Screen: "3.1 Inspection - Valid" → Decision: "Back to Sales screen."
- Screen: "3.1 Inspection - Valid" → Screen: "3.3.1 Error" [User selects
 'Not Valid']
- Screen: "3.2 Inspection - Invalid" → Decision: "Glider/Rail?" [User taps 'Validate'.]
- Screen: "8.4 Present Smart Card" → Decision: "Smartcard Readable?" [User presents 
smartcard]
- Decision: "Smartcard Readable?" → Screen: "3.3 Error - Read/Write Fail" [No - not
readable.
]
- Decision: "Go to 'Top Up Receipt Print' flow." → Decision: "Back to Sales screen." [Once the Print flow is complete...]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Top Up Receipt Print' flow." [User taps 'Faulty Smartpass'.]
- Decision: "Smartcard Readable?" → Decision: "Is passback configured?" [Yes -Readable]
- Decision: "Is passback configured?" → Decision: "Smartcard Valid?" [No]
- Screen: "3.3.1 Error" → Decision: "User chooses to issue a penalty fare and third party app opens.
A Penalty Fare ticket also prints." [User selects
 'Penalty Fare']
- Screen: "3.3.1 Error" → Decision: "Back to Sales screen."
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Back to Sales screen."
- Screen: "2.5.4.2 Error - Passback" → Decision: "Back to 'Sales' screen."
- Decision: "Smartcard Last Used 
within passback period?" → Screen: "2.5.4.2 Error - Passback" [Yes]
- Screen: "3.3.1 Error" → Decision: "Go to Penalty Warning print flow." [User selects 
'Penalty Warning']
- Screen: "2.0.6 Sales Screen - Rail- Validation - Device View" → Decision: "Smartcard Readable?" [User presents a smartcard]
- Decision: "Is passback configured?" → Decision: "Passed pre-validation
checks?" [No
]
- Decision: "Is passback configured?" → Decision: "Smartcard Last Used 
within passback period?" [Yes
]
- Decision: "Has the smartcard
been previously 
validated?" → Decision: "Is 'Last Use' 
within the transfer period?
(<90 minutes)" [Yes]
- Decision: "Is 'Last Use' 
within the transfer period?
(<90 minutes)" → Decision: "Does the direction 
of travel match the current route?" [Yes]
- Decision: "Does the direction 
of travel match the current route?" → Screen: "3.2 Inspection - Invalid" [No]
- Decision: "Is 'Last Use' 
within the transfer period?
(<90 minutes)" → Decision: "Does the direction 
of travel match the current route?" [No]
- Decision: "Does the direction 
of travel match the current route?" → Screen: "3.2.1 Inspection - Invalid - Warning" [Yes]
- Decision: "Does the direction 
of travel match the current route?" → Screen: "3.2 Inspection - Invalid" [No]
- Screen: "3.2.1 Inspection - Invalid - Warning" → Decision: "Glider/Rail?" [User taps 'Validate']
- Screen: "3.2.1 Inspection - Invalid - Warning" → Screen: "3.3.1 Error" [User selects
 'Penalty Fare']
- Screen: "3.2 Inspection - Invalid" → Screen: "3.3.1 Error" [User selects
 'Penalty Fare']
- Decision: "Is passback configured?" → Decision: "Smartcard Last Used 
within passback period?" [Yes]
- Decision: "Smartcard Last Used 
within passback period?" → Decision: "Smartcard Valid?" [No]
- Screen: "2.4 Payment Area" → Decision: "See Card Payment flow." [User taps 'Card'
button.
]
- Decision: "Smartcard Type
Commercial/Staff/EA?" → Decision: "Glider/Rail?" [Yes]
- Decision: "Smartcard Type
Discounted Fare
 Validation?" → Decision: "Half-Fare?" [Yes]
- Decision: "Smartcard Type
Concession Fare
 Validation" → Decision: "Glider/Rail?" [Concession Fare Validation]
- Decision: "Glider/Rail?" → Screen: "2.6.1 Discount - Sales mode - Rail" [Rail]
- Decision: "yLink Validation?" → Decision: "Glider/Rail?" [Yes]
- Decision: "Glider/Rail?" → Screen: "2.6 Discount - Sales mode (yLink)" [Glider]
- Screen: "2.6 Discount - Sales mode (yLink)" → Screen: "2.6.0.1 Discount - Sales mode - Alighting Selected (yLink)"
- Screen: "2.6.0.1 Discount - Sales mode - Alighting Selected (yLink)" → Screen: "2.6.2 Discount - Summary (yLink)"
- Screen: "2.6.1 Discount - Sales mode - Rail" → Screen: "2.6.2 Discount - Summary (yLink)"
- Screen: "2.6.2 Discount - Summary (yLink)" → Screen: "2.4 Payment Area"
- Screen: "2.6.1 Discount - Sales mode - Rail" → Screen: "2.6.1 - Discount - Sales mode - Select Product - Rail - yLink"
- Screen: "2.6.1 - Discount - Sales mode - Select Product - Rail - yLink" → Screen: "2.6.1 Discount - Sales mode - Rail"
- Screen: "2.6.5.1 Concessionary Card - Sales mode - Rail" → Decision: "Cross Border?"
- Decision: "Cross Border?" → Decision: "If no other Ticket Types are available the HHD will remain on the current screen" [No]
- Decision: "Cross Border?" → Screen: "2.6.1 - Discount - Sales mode - Select Product - SeniorXB" [Yes]
- Screen: "2.4 Payment Area" → Decision: "Go to relevant 'Cash / Payment Card Print Flow' flow." [User chooses preset cash option,
or if customer has correct amount,
taps the 'Cash' button, or taps Warrant if applicable.]
- Screen: "2.4 Payment Area" → Decision: "Go to relevant 'Cash / Payment Card Print Flow' flow."
- Screen: "2.4 Payment Area" → Decision: "Go to relevant 'Cash / Payment Card Print Flow' flow."
- Screen: "2.4 Payment Area" → Decision: "Go to relevant 'Cash / Payment Card Print Flow' flow."
- Screen: "2.4 Payment Area (Glider)" → Decision: "See Card Payment flow." [User taps 'Card'
button.
]
- Screen: "2.4 Payment Area (Glider)" → Screen: "4.4 Represent Smartcard" [User chooses preset cash option,
or if customer has correct amount,
taps the 'Cash' button, or taps Warrant if applicable.]
- Decision: "See Card Payment flow." → Screen: "4.4 Represent Smartcard" [Successful 
Card Payment]
- Screen: "4.4 Represent Smartcard" → Decision: "Smartcard
Readable?"
- Screen: "2.6.2 Discount - Summary (yLink)" → Screen: "2.4 Payment Area (Glider)"
- Screen: "2.6.1 - Discount - Sales mode - Select Product - SeniorXB" → Screen: "2.6.5.1 Concessionary Card - Sales mode - Rail" [User selects
 a Ticket Type]
- Screen: "2.6.5.1 Concessionary Card - Sales mode - Rail" → Screen: "4.4 Represent Smartcard"
- Screen: "2.6.5 Concessionary Card - Sales mode" → Decision: "Smartcard
Readable?"
- Decision: "Glider/Rail?" → Screen: "2.6.5.1 Concessionary Card - Sales mode - Rail" [Rail]
- Decision: "Glider/Rail?" → Screen: "2.6.5 Concessionary Card - Sales mode" [Glider]
- Screen: "2.0 Sales Screen - Inspection - Device View" → Screen: "3.4.1.2 Revenue Inspect - Connecting"
- Screen: "2.0.6 Sales Screen - Rail- Inspection - Device View" → Screen: "3.4.1.2 Revenue Inspect - Connecting"
- Screen: "2.0.6 Sales Screen - Rail- Validation - Device View" → Screen: "3.4.1.2 Revenue Inspect - Connecting" [User selects the square button to initiate a Revenue Inspection]
- Screen: "3.4.1-Revenue Inspect - Processing" → Decision: "Payment Device has 
BOS connectivity?"
- Decision: "Inspection Success?" → Screen: "3.4.2-Revenue Inspect - Success" [Yes]
- Decision: "Inspection Success?" → Screen: "3.4.4.1-Revenue Inspect - Failure - Denylist" [No
]
- Screen: "3.4 Revenue Inspect - Card Prompt" → Decision: "Back to Sales screen."
- Screen: "3.4 Revenue Inspect - Card Prompt" → Screen: "3.4.1-Revenue Inspect - Processing" [User presents an EMV card to M020]
- Screen: "3.4.2-Revenue Inspect - Success" → Decision: "Back to Sales screen."
- Screen: "3.4.4.1-Revenue Inspect - Failure - Denylist" → Decision: "Back to Sales screen."
- Screen: "3.4.2-Revenue Inspect - Success" → Screen: "3.4 Revenue Inspect - Card Prompt"
- Screen: "3.4.4.1-Revenue Inspect - Failure - Denylist" → Screen: "3.4 Revenue Inspect - Card Prompt"
- Screen: "3.4 Revenue Inspect - Card Prompt" → Screen: "2.0.9 Select Boarding - List - Numerical Search" [User selects the stage number]
- Screen: "3.4 Revenue Inspect - Card Prompt" → Screen: "2.0.7 Select Boarding - List - HHD Screen Size"
- Screen: "2.0.9 Select Boarding - List - Numerical Search" → Screen: "3.4 Revenue Inspect - Card Prompt" [User selects a new
 boarding location]
- Screen: "2.0.7 Select Boarding - List - HHD Screen Size" → Screen: "3.4 Revenue Inspect - Card Prompt" [User selects a new 
boarding location]
- Screen: "2.0.9 Select Boarding - List - Numerical Search" → Screen: "2.0.7 Select Boarding - List - HHD Screen Size" [User confirms the
 entered search value]
- Decision: "Payment Device has 
BOS connectivity?" → Decision: "Inspection Success?" [Yes]
- Decision: "Payment Device has 
BOS connectivity?" → Screen: "3.4.3-Revenue Inspect - Failure - Disconnected" [No]
- Screen: "3.4.3-Revenue Inspect - Failure - Disconnected" → Screen: "3.4 Revenue Inspect - Card Prompt"
- Screen: "3.4.3-Revenue Inspect - Failure - Disconnected" → Decision: "Back to Sales screen."
- Decision: "Glider/Rail?" → Screen: "8.4 Present Smart Card" [Rail]
- Decision: "Glider/Rail?" → Decision: "Smartcard Type
Commercial/Staff/EA?"
- Decision: "Smartcard Type
Commercial/Staff/EA?" → Decision: "Smartcard Type
Discounted Fare
 Validation?"
- Decision: "Smartcard Type
Discounted Fare
 Validation?" → Decision: "Smartcard Type
Concession Fare
 Validation"
- Decision: "yLink Validation?" → Screen: "2.6.1 Discount - Sales mode - Rail" [No]
- Decision: "Half-Fare?" → Decision: "Glider/Rail?" [Yes]
- Decision: "Half-Fare?" → Decision: "yLink Validation?" [No]
- Decision: "Glider/Rail?" → Screen: "2.6.1 Discount - Sales mode - Rail" [Rail]
- Decision: "Glider/Rail?" → Screen: "2.6.5 Concessionary Card - Sales mode" [Glider]
- Decision: "Glider/Rail?" → Screen: "2.6.7 Validation - Success" [Rail]
- Decision: "Glider/Rail?" → Screen: "2.6.5 Concessionary Card - Sales mode" [Glider]
- Screen: "3.4.1.2 Revenue Inspect - Connecting" → Screen: "3.4 Revenue Inspect - Card Prompt"
- Screen: "3.4.1.2 Revenue Inspect - Connecting" → Decision: "Back to Sales screen."


## 10. 10. Panic Mode Function

### Screens (3)
- 2.0 Sales Screen
- 6.10 - Panic Message
- 6.1 Break Mode - NIR

### Decision Points (1)
- Timeout (3s)

### Annotations / Spec Notes (1)
- Device will disable operator software functions temporarily whilst displaying a status message indicating that an alert is being sent to the backoffice. (Event Code 1127)   On timeout the device will transition to Driver Break.

### Connections / Flow (3)
- Screen: "2.0 Sales Screen" → Screen: "6.10 - Panic Message" [User presses button 
3 times in quick succession]
- Screen: "6.10 - Panic Message" → Decision: "Timeout
(3s)"
- Decision: "Timeout
(3s)" → Screen: "6.1 Break Mode - NIR"


---

# Additional Boards (not in main navigation list — old/archived versions)


## Inspection and Validation (extra/archived board)

### Screens (33)
- 2.0 Sales Screen - Inspection
- 2.0 Sales Screen - Validation
- 3.3.2 Error - Critical Error
- 2.0.6 Sales Screen - Rail- Inspection
- 2.0.6 Sales Screen - Rail- Validation
- 2.5.4.2 Error - Passback
- 2.5.4.2 Error - Passback
- 3.3 Error - Read/Write Fail
- 3.3 Error - Read/Write Fail
- 2.6.7 Validation - Success
- 3.1 Inspection - Valid
- 3.3.1 Error
- 3.2 Inspection - Invalid
- 3.3.1 Error
- 3.2.3 Smartcard Not Valid - No Travel Remaining
- 2.6.5 Concessionary Card - Sales mode
- 3.3.1 Error
- 4.4 Represent Smartcard
- 3.2.2 Successful Validation
- 2.4.0.1 Payment Area - No Warrant
- 4.2.2 Top Up - iLink - Select Product
- 8.5 Printing Receipt - Cash
- 3.3 Error - Read/Write Fail
- 2.5.4.1 Critical Error
- 4.1.2 Critical Error - Invalid Card
- 3.3 Error - Read/Write Fail
- 2.4.3.1 Transaction complete
- 4.1.2 Critical Error - Invalid Card
- 2.6.7 Validation - Success
- 7.2 Print Failed
- 4.6 Voiding Last Card Transaction
- 4.6 Voiding Last Card Transaction
- 3.2.2 Successful Validation

### Decision Points (63)
- HHD Rail - Validation & Expired Card Top Up
- HHD Glider - Inspection & Validation
- Smartcard Readable?
- Smartcard Readable?
- Smartcard Already Presented & Validated previously?
- Back to 'Sales' screen.
- Smartcard Already Presented & Validated previously?
- Back to 'Sales' screen.
- Smartcard Valid?
- Back to Sales screen.
- Passed pre-validation checks?
- Back to 'Sales' screen.
- Back to Sales screen.
- Has the Smartcard been validated?
- Go to 'Smartcard Readable?' check above.
- Go to 'Top Up Receipt Print' flow.
- Go to 'Top Up Receipt Print' flow.
- Back to Sales screen.
- Back to Sales screen.
- Back to Sales screen.
- Back to Sales screen.
- Back to Sales screen.
- Back to Sales screen.
- User chooses to issue a penalty fare and third party app opens. A Penalty Fare ticket also prints.
- Go to Penalty Warning print flow.
- Go to Penalty Warning print flow.
- A third party app opens. A Penalty Fare ticket also prints.
- Back to 'Sales' screen.
- Back to Sales screen.
- Card Type?
- Back to Sales screen.
- Back to 'Sales' screen.
- Go to 'Discount Card Sales' flow.
- Back to Sales screen.
- Back to 'Sales' screen.
- Smartcard readable?
- Card validation success?
- User chooses to issue a penalty fare and third party app opens. A Penalty Fare ticket also prints.
- Valid top-up card?
- Go to Penalty Warning print flow.
- Smartcard Readable?
- See Card Payment flow.
- Back to Sales screen.
- Back to 'Sales' screen.
- Correct Card presented?
- Payment card used?
- Go to 'Smartcard Readable?' check above.
- Able to print?
- Go to 'Top Up Receipt Print' flow.
- Back to Sales screen.
- Back to 'Sales' screen.
- Back to 'Represent Smartcard' screen.
- Back to 'Represent Smartcard' screen.
- Payment card used?
- Go to the 'Card Payment Receipt Print' flow.
- Back to 'Sales' screen.
- Go to 'Card validation success?' check above.
- Go to 'Top Up Receipt Print' flow.
- Back to Sales screen.
- Back to 'Sales' screen.
- Go to the 'Card Payment Receipt Print' flow.
- Back to 'Sales' screen.
- Back to 'Represent Smartcard' screen.

### Annotations / Spec Notes (9)
- Top-up is iLink only. Validation includes iLink, Staff, Spouse, Retired, External and aLink.
- On validation, a Transaction Record is sent to the back office.
- 'Error Message' will read:  - Product Expired - Pass Expired - No Journeys Left - No Balance Left - Hotlisted Card
- N.B. Error message could read: - Not valid at this location - Hotlisted Card - Product Expired
- N.B. '£Price change' header will only show if cash was the payment method, otherwise card payment screen will display instead - this will be 1 of 2 for print due to additional receipts for card payment.  Print will still go through same checks seen in Print flows.
- Other cards will display the tick and then        [PRODUCT NAME]              Validated  below the tick.  See 'Validation Successful' screen on the Rail flow for reference.
- For a card payment, there will be a check to see if you also want to print the customer receipt as seen in the 'Payment Card Print' flow.
- On validation, a Transaction Record is sent to the back office.
- Other cards will display the tick and then        [PRODUCT NAME]              Validated  below the tick.  See 'Validation Successful' screen on the Rail flow for reference.

### Connections / Flow (97)
- Decision: "Go to Penalty Warning print flow." → Decision: "Back to Sales screen." [Once the Print
flow is complete...
]
- Screen: "2.4.0.1 Payment Area - No Warrant" → Screen: "4.4 Represent Smartcard" [User chooses preset cash option,
or if customer has correct amount,
taps the 'Cash' button.
]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Back to 'Represent Smartcard' screen." [User taps 'Retry' button.]
- Screen: "3.3.1 Error" → Decision: "Go to Penalty Warning print flow." [User taps
'Penalty Warning'.
A Penalty Warning ticket prints.
]
- Decision: "Go to 'Top Up Receipt Print' flow." → Decision: "Back to Sales screen." [Once Print flow is complete...]
- Screen: "3.3.1 Error" → Decision: "A third party app opens.
A Penalty Fare ticket also prints." [User taps 'Penalty Fare'.]
- Screen: "3.2 Inspection - Invalid" → Screen: "3.3.1 Error" [User taps
'Penalty Fare'.
]
- Decision: "Payment card used?" → Decision: "Back to 'Sales' screen." [No]
- Decision: "Valid top-up card?" → Screen: "4.1.2 Critical Error - Invalid Card" [No
]
- Screen: "2.6.7 Validation - Success" → Decision: "Back to 'Sales' screen."
- Decision: "See Card Payment flow." → Screen: "4.4 Represent Smartcard" [Successful card
payment.
]
- Decision: "Able to print?" → Screen: "7.2 Print Failed" [No]
- Decision: "Payment card used?" → Screen: "4.6 Voiding Last Card Transaction" [Yes]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Back to 'Sales' screen." [User taps 'Cancel' button.]
- Screen: "3.2.3 Smartcard Not Valid - No Travel Remaining" → Screen: "4.2.2 Top Up - iLink - Select Product" [User taps 'Top-Up'.]
- Decision: "Go to 'Top Up Receipt Print' flow." → Decision: "Back to Sales screen." [Once Print flow is complete...]
- Decision: "Smartcard Valid?" → Screen: "3.3.1 Error" [No - Travel is prohibited]
- Decision: "Smartcard Valid?" → Screen: "2.6.7 Validation - Success" [Yes - valid.]
- Decision: "Valid top-up card?" → Screen: "8.5 Printing Receipt - Cash" [Yes]
- Decision: "A third party app opens.
A Penalty Fare ticket also prints." → Decision: "Back to 'Sales' screen."
- Screen: "2.4.0.1 Payment Area - No Warrant" → Decision: "See Card Payment flow." [User taps
'Card' button.
]
- Decision: "Correct Card
presented?" → Screen: "4.1.2 Critical Error - Invalid Card"
- Screen: "4.4 Represent Smartcard" → Decision: "Smartcard
Readable?" [Customer represents smartcard.]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Payment card used?" [User taps
'Cancel' button.
]
- Decision: "Go to Penalty Warning print flow." → Decision: "Back to Sales screen." [Once the Print
flow is complete...
]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Back to 'Represent Smartcard' screen." [User taps 'Retry' button.]
- Decision: "Able to print?" → Screen: "2.4.3.1 Transaction complete" [Yes]
- Decision: "Card validation
success?" → Screen: "3.2.2 Successful Validation" [Yes]
- Screen: "2.5.4.1 Critical Error" → Decision: "Payment card used?" [User taps 'Cancel' button.]
- Screen: "2.5.4.1 Critical Error" → Decision: "Back to 'Represent Smartcard' screen." [User taps 'Retry' button.]
- Screen: "3.3.1 Error" → Decision: "Back to Sales screen."
- Decision: "Card validation
success?" → Decision: "Correct Card
presented?" [No]
- Screen: "4.6 Voiding Last Card Transaction" → Decision: "Go to the 'Card Payment Receipt Print' flow."
- Decision: "Smartcard readable?" → Decision: "Card validation
success?" [Yes]
- Decision: "Payment card used?" → Screen: "4.6 Voiding Last Card Transaction" [Yes]
- Decision: "Correct Card
presented?" → Screen: "3.3 Error - Read/Write Fail" [Yes]
- Decision: "Go to 'Top Up Receipt Print' flow." → Decision: "Back to Sales screen." [Once the Print flow is complete...]
- Screen: "3.2.3 Smartcard Not Valid - No Travel Remaining" → Decision: "Back to Sales screen." [User taps 'Cancel'.]
- Decision: "Smartcard
Readable?" → Screen: "2.5.4.1 Critical Error" [No]
- Screen: "8.5 Printing Receipt - Cash" → Decision: "Able to print?"
- Decision: "Payment card used?" → Decision: "Back to 'Sales' screen." [No]
- Screen: "3.3.1 Error" → Decision: "User chooses to issue a penalty fare and third party app opens.
A Penalty Fare ticket also prints." [User taps
'Penalty Fare'.
]
- Screen: "3.2.2 Successful Validation" → Decision: "Back to 'Sales' screen." [3 second timeout or the user
taps the Tick.
]
- Screen: "4.2.2 Top Up - iLink - Select Product" → Screen: "2.4.0.1 Payment Area - No Warrant" [iLink product
selected.
]
- Decision: "Smartcard
Readable?" → Decision: "Valid top-up card?" [Yes]
- Decision: "Smartcard readable?" → Screen: "3.3 Error - Read/Write Fail" [No]
- Screen: "4.6 Voiding Last Card Transaction" → Decision: "Go to the 'Card Payment Receipt Print' flow."
- Screen: "2.6.7 Validation - Success" → Decision: "Back to 'Sales' screen."
- Decision: "Smartcard Valid?" → Screen: "3.2.3 Smartcard Not Valid - No Travel Remaining" [No - No travel
remaining.
]
- Decision: "Smartcard Readable?" → Screen: "3.3 Error - Read/Write Fail" [No]
- Decision: "User chooses to issue a penalty fare and third party app opens.
A Penalty Fare ticket also prints." → Decision: "Back to 'Sales' screen."
- Screen: "2.4.3.1 Transaction complete" → Screen: "3.2.2 Successful Validation" [3 second
timeout...
]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Smartcard Readable?' check above." [User taps 'Retry'.]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Top Up Receipt Print' flow." [User taps 'Faulty Smartpass'.]
- Screen: "7.2 Print Failed" → Screen: "3.2.2 Successful Validation" [User taps
'Continue Without
Printing' button.
]
- Screen: "3.2.2 Successful Validation" → Screen: "2.6.7 Validation - Success"
- Screen: "2.0 Sales Screen - Inspection" → Screen: "2.0 Sales Screen - Validation" [User swipes Inspection 
to engage Validation mode]
- Screen: "2.0.6 Sales Screen - Rail- Inspection" → Screen: "2.0.6 Sales Screen - Rail- Validation" [User swipes Inspection 
to engage Validation mode]
- Screen: "2.0.6 Sales Screen - Rail- Validation" → Screen: "2.0.6 Sales Screen - Rail- Inspection" [User swipes Validation 
to engage Inspection mode]
- Screen: "2.0 Sales Screen - Validation" → Screen: "2.0 Sales Screen - Inspection" [User swipes Validation 
to engage Inspection mode]
- Screen: "2.0 Sales Screen - Inspection" → Decision: "Smartcard Readable?"
- Screen: "2.0.6 Sales Screen - Rail- Inspection" → Decision: "Smartcard Readable?"
- Decision: "Smartcard Readable?" → Decision: "Smartcard Already Presented & Validated previously?" [Yes]
- Decision: "Smartcard Already Presented & Validated previously?" → Decision: "Passed pre-validation
checks?"
- Decision: "Passed pre-validation
checks?" → Decision: "Has the Smartcard
been validated?"
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Back to Sales screen." [User taps Cancel]
- Decision: "User chooses to issue a penalty fare and third party app opens.
A Penalty Fare ticket also prints." → Decision: "Back to 'Sales' screen."
- Decision: "Go to Penalty Warning print flow." → Decision: "Back to Sales screen." [Once the Print
flow is complete...
]
- Decision: "Passed pre-validation
checks?" → Screen: "3.3.1 Error" [No]
- Decision: "Smartcard Already Presented & Validated previously?" → Screen: "2.5.4.2 Error - Passback" [Yes]
- Screen: "2.5.4.2 Error - Passback" → Decision: "Back to 'Sales' screen."
- Decision: "Has the Smartcard
been validated?" → Screen: "3.2 Inspection - Invalid"
- Decision: "Has the Smartcard
been validated?" → Screen: "3.1 Inspection - Valid"
- Screen: "3.3.1 Error" → Decision: "Back to Sales screen."
- Screen: "3.1 Inspection - Valid" → Decision: "Back to Sales screen."
- Screen: "3.1 Inspection - Valid" → Screen: "3.3.1 Error"
- Decision: "Card Type?" → Decision: "Go to 'Discount Card Sales' flow." [yLink - user decides to validate smartcard
   (discounted smart cards)
]
- Screen: "3.2 Inspection - Invalid" → Decision: "Card Type?" [User taps 'Validate'.]
- Decision: "Card Type?" → Screen: "2.6.5 Concessionary Card - Sales mode" [User decides to validate smartcard
    (non-discounted smart cards)]
- Screen: "2.6.5 Concessionary Card - Sales mode" → Decision: "Smartcard readable?"
- Decision: "Smartcard Readable?" → Screen: "3.3 Error - Read/Write Fail" [No - not
readable.
]
- Decision: "Go to 'Top Up Receipt Print' flow." → Decision: "Back to Sales screen." [Once the Print flow is complete...]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Top Up Receipt Print' flow." [User taps 'Faulty Smartpass'.]
- Decision: "Smartcard Readable?" → Decision: "Smartcard Already Presented & Validated previously?" [Yes -Readable]
- Decision: "Smartcard Already Presented & Validated previously?" → Decision: "Smartcard Valid?" [No - this card has not been
presented previously.]
- Screen: "2.0 Sales Screen - Validation" → Decision: "Smartcard Readable?"
- Screen: "2.0.6 Sales Screen - Rail- Validation" → Decision: "Smartcard Readable?"
- Screen: "3.3.1 Error" → Decision: "User chooses to issue a penalty fare and third party app opens.
A Penalty Fare ticket also prints."
- Screen: "3.3.1 Error" → Decision: "Back to Sales screen."
- Screen: "3.3.1 Error" → Decision: "Go to Penalty Warning print flow."
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Back to Sales screen."
- Screen: "2.5.4.2 Error - Passback" → Decision: "Back to 'Sales' screen."
- Decision: "Smartcard Already Presented & Validated previously?" → Screen: "2.5.4.2 Error - Passback" [Yes]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Top Up Receipt Print' flow."
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Smartcard Readable?' check above."
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Top Up Receipt Print' flow."
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Card validation success?' check above."


## Inspection & Validation - Re-arrangement (extra/archived board)

### Screens (30)
- 2.0 Sales Screen - Inspection
- 2.0.6 Sales Screen - Rail- Inspection
- 2.0.6 Sales Screen - Rail- Validation
- 3.3 Error - Read/Write Fail
- 2.5.4.1 Critical Error
- 4.6 Voiding Last Card Transaction
- 3.3 Error - Read/Write Fail
- 8.5 Printing Receipt - Cash
- 2.4.3.1 Transaction complete
- 3.2.2 Successful Validation
- 2.6.7 Validation - Success
- 2.5.4.2 Error - Passback
- 2.5.4.2 Error - Passback
- 3.2.2 Successful Validation
- 7.2 Print Failed
- 4.1.2 Critical Error - Invalid Card
- 4.6 Voiding Last Card Transaction
- 3.2.3 Smartcard Not Valid - No Travel Remaining
- 2.6.7 Validation - Success
- 3.3.1 Error
- 3.3.1 Error
- 4.1.2 Critical Error - Invalid Card
- 3.2.1 Inspection - Invalid - Warning
- 4.2.2 Top Up - iLink - Select Product
- 2.4.0.1 Payment Area - No Warrant
- 4.4 Represent Smartcard
- 3.1 Inspection - Valid
- 8.4 Present Smart Card
- 2.6.5 Concessionary Card - Sales mode
- 3.2 Inspection - Invalid

### Decision Points (58)
- HHD remains in inspection mode
- HHD - Validation Mode & Expired Card Top Up
- HHD - Inspection Mode & Card Validation
- Smartcard readable?
- Smartcard Readable?
- Smartcard Readable?
- Smartcard Readable?
- Go to the 'Card Payment Receipt Print' flow.
- Back to Sales screen.
- Back to Sales screen.
- Payment card used?
- Back to 'Sales' screen.
- Go back to previous screen.
- Go to 'Top Up Receipt Print' flow.
- Back to 'Represent Smartcard' screen.
- Go to 'Top Up Receipt Print' flow.
- Back to Sales screen.
- Back to Sales screen.
- Is passback configured?
- Is passback configured?
- Smartcard Last Used  within passback period?
- Valid top-up card?
- Able to print?
- Back to 'Sales' screen.
- Back to 'Sales' screen.
- Smartcard Last Used  within passback period?
- Card validation success?
- Back to 'Sales' screen.
- Back to 'Sales' screen.
- Smartcard Valid?
- Go to the 'Card Payment Receipt Print' flow.
- Passed pre-validation checks?
- Correct Card presented?
- Back to 'Sales' screen.
- Back to Sales screen.
- Back to Sales screen.
- Back to 'Represent Smartcard' screen.
- Back to Sales screen.
- Back to 'Sales' screen.
- Back to 'Represent Smartcard' screen.
- Go to Penalty Warning print flow.
- A third party app opens. A Penalty Fare ticket also prints.
- Payment card used?
- User chooses to issue a penalty fare and third party app opens. A Penalty Fare ticket also prints.
- Go to Penalty Warning print flow.
- Back to 'Sales' screen.
- Back to Sales screen.
- Back to 'Sales' screen.
- Back to 'Sales' screen.
- Back to Sales screen.
- Has the smartcard been previously  validated?
- Does the direction  of travel match the current route?
- Is 'Last Use'  within the transfer period? (<90 minutes)
- Does the direction  of travel match the current route?
- See Card Payment flow.
- Back to Sales screen.
- Card Type?
- Go to 'Discount Card Sales' flow.

### Annotations / Spec Notes (13)
- Top-up is iLink only. Validation includes iLink, Staff, Spouse, Retired, External and aLink.
- Previous screens may be:   * 2.0 Sales Screen - Inspection   * 2.0.6 Sales Screen - Rail - Inspection   * 2.6.5 Concessionary Card - Sales mode
- N.B. '£Price change' header will only show if cash was the payment method, otherwise card payment screen will display instead - this will be 1 of 2 for print due to additional receipts for card payment.  Print will still go through same checks seen in Print flows.
- For a card payment, there will be a check to see if you also want to print the customer receipt as seen in the 'Payment Card Print' flow.
- Other cards will display the tick and then        [PRODUCT NAME]              Validated  below the tick.  See 'Validation Successful' screen on the Rail flow for reference.
- On validation, a Transaction Record is sent to the back office.
- Other cards will display the tick and then  [PRODUCT NAME] Validated   below the tick.  See 'Validation Successful' screen on the Rail flow for reference.
- 'Error Message' will read:  - Product Expired - Pass Expired - No Journeys Left - No Balance Left - Hotlisted Card - Visual Rejection
- On validation, a Transaction Record is sent to the back office.
- N.B. Error message could read: - Not valid at this location - Hotlisted Card - Product Expired
- 'Penalty Fare' option may be disabled if the Penalty Fare App is not available, the printer is disconnected or the Smartcard product is valid for free travel.
- Expiry, Last Used Dates and Direction may show as N/A when not available/applicable.
- Expiry, Last Used Dates and Direction may show as N/A when not available/applicable.

### Connections / Flow (98)
- Screen: "2.4.0.1 Payment Area - No Warrant" → Screen: "4.4 Represent Smartcard"
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Back to 'Represent Smartcard' screen." [User taps 'Retry' button.]
- Screen: "3.3.1 Error" → Decision: "Go to Penalty Warning print flow." [User taps
'Penalty Warning'.
A Penalty Warning ticket prints.
]
- Screen: "3.3.1 Error" → Decision: "A third party app opens.
A Penalty Fare ticket also prints." [User taps 'Penalty Fare'.]
- Decision: "Payment card used?" → Decision: "Back to 'Sales' screen." [No]
- Decision: "Valid top-up card?" → Screen: "4.1.2 Critical Error - Invalid Card" [No
]
- Screen: "2.6.7 Validation - Success" → Decision: "Back to 'Sales' screen."
- Decision: "See Card Payment flow." → Screen: "4.4 Represent Smartcard" [Successful card
payment.
]
- Decision: "Able to print?" → Screen: "7.2 Print Failed" [No]
- Decision: "Payment card used?" → Screen: "4.6 Voiding Last Card Transaction" [Yes]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Back to 'Sales' screen." [User taps 'Cancel' button.]
- Screen: "3.2.3 Smartcard Not Valid - No Travel Remaining" → Screen: "4.2.2 Top Up - iLink - Select Product" [User taps 'Top-Up'.]
- Decision: "Smartcard Valid?" → Screen: "3.3.1 Error" [No - Travel is prohibited]
- Decision: "Smartcard Valid?" → Screen: "2.6.7 Validation - Success" [Yes - valid.]
- Decision: "Valid top-up card?" → Screen: "8.5 Printing Receipt - Cash" [Yes]
- Decision: "A third party app opens.
A Penalty Fare ticket also prints." → Decision: "Back to 'Sales' screen."
- Screen: "2.4.0.1 Payment Area - No Warrant" → Decision: "See Card Payment flow." [User taps
'Card' button.
]
- Decision: "Correct Card
presented?" → Screen: "4.1.2 Critical Error - Invalid Card"
- Screen: "4.4 Represent Smartcard" → Decision: "Smartcard
Readable?" [Customer represents smartcard.]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Payment card used?" [User taps
'Cancel' button.
]
- Decision: "Go to Penalty Warning print flow." → Decision: "Back to Sales screen." [Once the Print
flow is complete...
]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Back to 'Represent Smartcard' screen." [User taps 'Retry' button.]
- Decision: "Able to print?" → Screen: "2.4.3.1 Transaction complete" [Yes]
- Decision: "Card validation
success?" → Screen: "3.2.2 Successful Validation" [Yes]
- Screen: "2.5.4.1 Critical Error" → Decision: "Payment card used?" [User taps 'Cancel' button.]
- Screen: "2.5.4.1 Critical Error" → Decision: "Back to 'Represent Smartcard' screen." [User taps 'Retry' button.]
- Screen: "3.3.1 Error" → Decision: "Back to Sales screen."
- Decision: "Card validation
success?" → Decision: "Correct Card
presented?" [No]
- Screen: "4.6 Voiding Last Card Transaction" → Decision: "Go to the 'Card Payment Receipt Print' flow."
- Decision: "Smartcard readable?" → Decision: "Card validation
success?" [Yes]
- Decision: "Payment card used?" → Screen: "4.6 Voiding Last Card Transaction" [Yes]
- Decision: "Correct Card
presented?" → Screen: "3.3 Error - Read/Write Fail" [Yes]
- Decision: "Go to 'Top Up Receipt Print' flow." → Decision: "Back to Sales screen." [Once the Print flow is complete...]
- Screen: "3.2.3 Smartcard Not Valid - No Travel Remaining" → Decision: "Back to Sales screen." [User taps 'Cancel'.]
- Decision: "Smartcard
Readable?" → Screen: "2.5.4.1 Critical Error" [No]
- Screen: "8.5 Printing Receipt - Cash" → Decision: "Able to print?"
- Decision: "Payment card used?" → Decision: "Back to 'Sales' screen." [No]
- Screen: "3.2.2 Successful Validation" → Decision: "Back to 'Sales' screen." [3 second timeout or the user
taps the Tick.
]
- Screen: "4.2.2 Top Up - iLink - Select Product" → Screen: "2.4.0.1 Payment Area - No Warrant" [iLink product
selected.
]
- Decision: "Smartcard
Readable?" → Decision: "Valid top-up card?" [Yes]
- Screen: "4.6 Voiding Last Card Transaction" → Decision: "Go to the 'Card Payment Receipt Print' flow."
- Screen: "2.6.7 Validation - Success" → Decision: "Back to 'Sales' screen."
- Decision: "Smartcard Valid?" → Screen: "3.2.3 Smartcard Not Valid - No Travel Remaining" [No - No travel
remaining.
]
- Decision: "Smartcard Readable?" → Screen: "3.3 Error - Read/Write Fail" [No]
- Screen: "2.4.3.1 Transaction complete" → Screen: "3.2.2 Successful Validation" [3 second
timeout...
]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go back to previous screen." [User taps 'Retry'.]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Top Up Receipt Print' flow." [User taps 'Faulty Smartpass'.]
- Screen: "7.2 Print Failed" → Screen: "3.2.2 Successful Validation" [User taps
'Continue Without
Printing' button.
]
- Screen: "3.2.2 Successful Validation" → Screen: "2.6.7 Validation - Success"
- Screen: "2.0 Sales Screen - Inspection" → Decision: "HHD remains in inspection mode" [User swipes Inspection 
to change mode]
- Screen: "2.0.6 Sales Screen - Rail- Inspection" → Screen: "2.0.6 Sales Screen - Rail- Validation" [User swipes Inspection 
to engage Validation mode]
- Screen: "2.0.6 Sales Screen - Rail- Validation" → Screen: "2.0.6 Sales Screen - Rail- Inspection" [User swipes Validation 
to engage Inspection mode]
- Screen: "2.0 Sales Screen - Inspection" → Decision: "Smartcard Readable?" [User presents a smartcard]
- Screen: "2.0.6 Sales Screen - Rail- Inspection" → Decision: "Smartcard Readable?" [User presents a smartcard]
- Decision: "Smartcard Readable?" → Decision: "Is passback configured?" [Yes]
- Decision: "Smartcard Last Used 
within passback period?" → Decision: "Passed pre-validation
checks?" [No]
- Decision: "Passed pre-validation
checks?" → Decision: "Has the smartcard
been previously 
validated?" [Yes]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Back to Sales screen." [User taps Cancel]
- Decision: "User chooses to issue a penalty fare and third party app opens.
A Penalty Fare ticket also prints." → Decision: "Back to 'Sales' screen."
- Decision: "Go to Penalty Warning print flow." → Decision: "Back to Sales screen." [Once the Print
flow is complete...
]
- Decision: "Passed pre-validation
checks?" → Screen: "3.3.1 Error" [No]
- Decision: "Smartcard Last Used 
within passback period?" → Screen: "2.5.4.2 Error - Passback" [Yes]
- Screen: "2.5.4.2 Error - Passback" → Decision: "Back to 'Sales' screen."
- Decision: "Has the smartcard
been previously 
validated?" → Screen: "3.2 Inspection - Invalid" [No]
- Decision: "Does the direction 
of travel match the current route?" → Screen: "3.1 Inspection - Valid" [Yes]
- Screen: "3.1 Inspection - Valid" → Decision: "Back to Sales screen."
- Screen: "3.1 Inspection - Valid" → Screen: "3.3.1 Error" [User selects
 'Not Valid']
- Decision: "Card Type?" → Decision: "Go to 'Discount Card Sales' flow." [Discounted smartcards
]
- Screen: "3.2 Inspection - Invalid" → Screen: "8.4 Present Smart Card" [User taps 'Validate'.]
- Decision: "Card Type?" → Screen: "2.6.5 Concessionary Card - Sales mode" [Non-discounted smartcards]
- Screen: "2.6.5 Concessionary Card - Sales mode" → Decision: "Smartcard readable?"
- Decision: "Smartcard Readable?" → Screen: "3.3 Error - Read/Write Fail" [No - not
readable.
]
- Decision: "Go to 'Top Up Receipt Print' flow." → Decision: "Back to Sales screen." [Once the Print flow is complete...]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Top Up Receipt Print' flow." [User taps 'Faulty Smartpass'.]
- Decision: "Smartcard Readable?" → Decision: "Is passback configured?" [Yes -Readable]
- Decision: "Is passback configured?" → Decision: "Smartcard Valid?" [No]
- Screen: "3.3.1 Error" → Decision: "User chooses to issue a penalty fare and third party app opens.
A Penalty Fare ticket also prints." [User selects
 'Penalty Fare']
- Screen: "3.3.1 Error" → Decision: "Back to Sales screen."
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Back to Sales screen."
- Screen: "2.5.4.2 Error - Passback" → Decision: "Back to 'Sales' screen."
- Decision: "Smartcard Last Used 
within passback period?" → Screen: "2.5.4.2 Error - Passback" [Yes]
- Screen: "3.3.1 Error" → Decision: "Go to Penalty Warning print flow." [User selects 
'Penalty Warning']
- Decision: "Smartcard readable?" → Screen: "3.3 Error - Read/Write Fail" [No]
- Screen: "2.0.6 Sales Screen - Rail- Validation" → Decision: "Smartcard Readable?" [User presents a smartcard]
- Decision: "Is passback configured?" → Decision: "Passed pre-validation
checks?" [No
]
- Decision: "Is passback configured?" → Decision: "Smartcard Last Used 
within passback period?" [Yes
]
- Decision: "Has the smartcard
been previously 
validated?" → Decision: "Is 'Last Use' 
within the transfer period?
(<90 minutes)" [Yes]
- Decision: "Is 'Last Use' 
within the transfer period?
(<90 minutes)" → Decision: "Does the direction 
of travel match the current route?" [Yes]
- Decision: "Does the direction 
of travel match the current route?" → Screen: "3.2 Inspection - Invalid" [No]
- Decision: "Is 'Last Use' 
within the transfer period?
(<90 minutes)" → Decision: "Does the direction 
of travel match the current route?" [No]
- Decision: "Does the direction 
of travel match the current route?" → Screen: "3.2.1 Inspection - Invalid - Warning" [Yes]
- Decision: "Does the direction 
of travel match the current route?" → Screen: "3.2 Inspection - Invalid" [No]
- Screen: "3.2.1 Inspection - Invalid - Warning" → Screen: "8.4 Present Smart Card" [User taps 'Validate']
- Screen: "3.2.1 Inspection - Invalid - Warning" → Screen: "3.3.1 Error" [User selects
 'Penalty Fare']
- Screen: "3.2 Inspection - Invalid" → Screen: "3.3.1 Error" [User selects
 'Penalty Fare']
- Decision: "Is passback configured?" → Decision: "Smartcard Last Used 
within passback period?"
- Decision: "Smartcard Last Used 
within passback period?" → Decision: "Smartcard Valid?" [No]
- Screen: "8.4 Present Smart Card" → Decision: "Card Type?" [User presents 
smartcard]


## [Archive] 4. Sales Mode (1) (extra/archived board)

### Screens (195)
- 2.0 Sales Screen
- 2.5 Basket Full
- 2.4.1.3 Payment Area/No Card Available 
- 2.0.9 Select Boarding - List - Numerical Search
- 2.0.7 Select Boarding - List - HHD Screen Size
- 2.0.2 Select Alighting - List - HHD Screen Size
- 2.8.1 Tabbed Navigation - Tickets - Edit Passengers - Rail
- 2.8.2 Tabbed Navigation - Tickets - Edit Passengers Glider
- 22 - Sales - Select Product - Glider
- 2.2 Add To Basket
- 2.0.12 Sales Screen - Paper Ticket Inspect
- 2.0.3 Select Alighting - List - Search Tapped
- 2.2.1 Add Another to Basket
- 2.0.13 Sales Screen - Paper Ticket Inspect - Confirmed
- 2.0.1 Select Alighting - List
- 2.0.10 Sales Screen - Different Ticket Type Selected
- 22.5 - Sales - Family & Friends Selected
- 2.8.2.2 Tabbed Navigation - Tickets - Edit Passengers - 1 Selected Glider
- 2.0.9.1 Select Boarding - List - Number Entered
- 2.0.8 Select Alighting - List - Search Tapped - Search Entered - No Matches
- 2.3 Items in Basket
- 22.5 - Sales - Child Selected Glider
- 22.6 - Sales - Select Product - Rail
- 2.0.9.2 Select Boarding - List - Number Entered - Tick Pressed
- 2.0.4 Select Alighting - List - Search Tapped - Search Entered
- 2.3.2 Basket Functionality - Delete
- 2.3.1 Basket Functionality - EditDuplicate
- 2.4 Payment Area
- 2.2.2 - Different Products
Selected - Rail
- 2.1 Issue Ticket
- 2.3.1.2 Item in Basket
Duplicated
- 2.3.1.1 Basket - Edit
- 2.4.1 Payment Area/Cash/Keyboard
- 2.6.2.1 - Payment - Details Swiped Down
- 22 - Sales - Select Product
- 2.4.1.1 Payment Area/Cash/Keyboard/Specific Amount
- 2.3.1.1.1 Basket - Line Edited
- 2.0 Sales Screen
- 2.3 Items in Basket
- 2.5 View Basket/Reconnect Card Reader
- 2.0.5 Sales Screen - Currency Switch Available
- 2.7 Tabbed Navigation - Tickets - Currency Switch
- 2.4.1.2 Payment Area/Cash/Currency Change
- 2.4.1.3 Payment Area/Cash/Currency Changed
- 2.0.14 Error - No Valid Tickets Available
- 22.1 - Sales - 3 Day Travel Chosen
- 2.5.3.2 View Basket/Reconnecting/Status Bar/Connecting
- 2.0.14.1 Error - No Valid Tickets - Sales
- 22.2 - Sales - 3 Day Travel Chosen - First Date Chosen
- 22.3 - Sales - 3 Day Travel Chosen - First & Second Dates Chosen
- 2.5.3 View Basket/Reconnecting/Status Bar/Not Connected
- 2.1.1 Issue Ticket - Advanced Ticket
- 22.4 - Sales - 3 Day Travel Chosen - Third Date Chosen
- 2.1.1.1 Issue Ticket - Advanced Ticket - Calendar 2
- 2.5.3.1 View Basket/Reconnecting/Status Bar/Not Connected/Contact Supervisor
- 2.3.0.1 Items in Basket - 3 Dates
- 2.1.1.2 Issue Ticket - Advanced Ticket - Calendar 3
- 2.5 View Basket/Reconnect Card Reader
- 2.1.3 Issue Advanced Ticket
- 2.1.4 Issue Advanced Ticket - Are you sure?
- 2.1.5 Issue Advanced Ticket - Are you sure?
- 2.1.6 Issue Advanced Ticket - Are you sure?
- 2.4.0.1 Payment Area - No Warrant
- 2.4.2.2 Payment/Card/Initialising Transaction
- 2.4.2 Payment/Card/User to Present Card
- 2.4.2.8 Payment/Card/Declined
- 2.4.2.4 Payment/Card/User to Confirm Amount
- 2.4.2.4 Payment/Card/User to Confirm Amount
- 2.4.2.5 Payment/Card/Processing Transaction
- 2.4.2.5 Payment/Card/Processing Transaction
- 2.4.2.1 Payment/Card/User Cancelled Transaction
- 2.4.2.5 Payment/Card/Processing Transaction
- 2.4.2.3 Payment/Card/PIN Entry
- 2.4.2.8 Payment/Card/Declined
- 2.4.2.6 Payment/Card/Transaction Success
- 2.4.2.6 Payment/Card/Transaction Success
- 2.4.2.7 Payment/Card/Signature Okay?
- 2.4.2.8 Payment/Card/Declined
- 2.4.2.5 Payment/Card/Processing Transaction
- 4.6 Voiding Last Card Transaction
- 2.4.2.8 Payment/Card/Declined
- 2.4.2.6 Payment/Card/Transaction Success
- 2.0 Sales Screen
- 2.6 Discount - Sales mode
- 2.0 Sales Screen
- 2.6.5 Concessionary Card - Sales mode
- 2.6.0.1 Discount - Sales mode - Alighting Selected
- 2.6.7 Validation - Success
- 4.1.2 Critical Error - Invalid Card
- 2.5.4.2 Error - Passback
- 2.5.4.2 Error - Passback
- 2.6.1 Discount - Sales mode - Rail
- 2.6.5.1 Concessionary Card - Sales mode - Rail
- 2.6.2 Discount - Summary
- 3.3 Error - Read/Write Fail
- 4.1.3 Critical Error - Invalid Card - Generic Error
- 4.1.3 Critical Error - Invalid Card - Generic Error
- 2.6.1.1 - Concession - Sales mode - Select Product
- 2.6.1 - Discount - Sales mode - Select Product
- 2.4 Payment Area
- 3.3 Error - Read/Write Fail
- 4.4 Represent Smartcard
- 3.3 Error - Read/Write Fail
- 2.6.5.2 Concessionary Card - Sales mode - Rail - Return Chosen
- 2.6.1.1 Discount - Sales mode - Return Chosen
- 4.1.2 Critical Error - Invalid Card
- 2.6.6 Concessionary - Summary
- 3.3 Error - Read/Write Fail
- 2.6.2.1 Discount - Summary - Rail
- 2.4 Payment Area
- 4.6 Voiding Last Card Transaction
- 8.5.1.1 Printing Receipt - Card
- 8.5.1.1 Printing Receipt - Card
- 2.4.3.1 Printing Ticket - No Header
- 26.2 Print Mini Statement
- 12.2 Printing Receipt
- 2.4.3 Printing Ticket
- 2.4.3.1 Printing Ticket - No Header
- 2.4.3.1 Printing Ticket - No Header
- 2.4.3.4 Transaction complete - Card
- 11.3 Printing Waybill
- 7. Printing Waybill
- 2.4.3.3 Printing Ticket - Card
- 7.2 Print Failed
- 2.4.3.4 Transaction complete - Card
- 2.4.3.2.1 Print Failed - Card
- 2.4.3.4 Transaction complete - Card
- 8.5.2.1 Printing Failed - Card
- Print Success
- Print Success
- 8.5.2.1 Printing Failed - Card
- 2.4.3.2 Print Failed
- 2.4.3.1 Transaction complete
- 11.4 Printing Failed
- 7.1 Transaction complete
- 7.2 Print Failed
- 2.4.3.4 Transaction complete - Card
- 8.5.2.1 Printing Failed - Card
- 27 Barcode Ticket - Printed?
- 8.5.2.1 Printing Failed - Card
- 7.1 Transaction complete
- 7.2 Print Failed
- 7.1 Transaction complete
- 2.4.3.2.1 Print Failed - Card
- 8.5.1 Print Receipt?
- 7.1 Transaction complete
- 8.5.1.1 Printing Receipt - Card
- 7.2.1 Print Failed Card Payment
- 4.2.2 Top Up - iLink - Expiry Date Set
- 4.2.2.2 Top Up - iLink - Expiry 1 Day from first use
- 2.0 Sales Screen
- 4.1 Present Smart Card
- 2.5.4.1 Critical Error
- 4.1.1 Critical Error - Incorrect Card
- 4.2.1 Top Up - No products available
- 4.2 Top Up - Select Amount
- 2.4.0.1 Payment Area - No Warrant
- 4.4 Represent Smartcard
- 2.5.4.1 Critical Error
- 4.1.2 Critical Error - Invalid Card
- 8.5.1.1 Printing Receipt - Card
- 4.8 Transaction complete
- 4.6 Voiding Last Card Transaction
- 4.6 Voiding Last Card Transaction
- 2.0.6 Sales Screen - Rail Login
- 3.3 Error - Read/Write Fail
- 2.5.4.2 Error - Passback
- 3.2.3 Smartcard Not Valid - No Travel Remaining
- 3.3.1 Error
- 2.6.7 Validation - Success
- 4.2.2 Top Up - iLink - Select Product
- 2.4.0.1 Payment Area - No Warrant
- 4.4 Represent Smartcard
- 4.1.2 Critical Error - Invalid Card
- 2.5.4.1 Critical Error
- 8.5 Printing Receipt - Cash
- 4.6 Voiding Last Card Transaction
- 4.6 Voiding Last Card Transaction
- 7.2 Print Failed
- 2.4.3.1 Transaction complete
- 3.2.2 Successful Validation
- 2.6.7 Validation - Success
- 2.0 Sales Screen
- 3.3 Error - Read/Write Fail
- 2.5.4.2 Error - Passback
- 3.1 Inspection - Valid
- 3.3.1 Error
- 3.2 Inspection - Invalid
- 3.3.1 Error
- 3.3.1 Error
- 2.6.5 Concessionary Card - Sales mode
- 3.2.2 Successful Validation
- 3.3 Error - Read/Write Fail
- 4.1.2 Critical Error - Invalid Card
- 3.3 Error - Read/Write Fail

### Decision Points (205)
- HHD - Sales Mode, Boarding/Alighting Stage Selection, Basket and Payment Area
- Once confirmed, banner will fade out so back to 'Sales' screen.
- Back to 'Sales' screen.
- Once stage is selected, back to 'Sales' screen.
- Once stage is selected, back to 'Sales' screen.
- See Card Payment flow.
- Back to '2.4 - Payment Area'.
- Back to 'Payment Area' screen.
- Go to relevant 'Cash / Payment Card Print Flow' flow.
- HHD - Payment Device Re-Connection
- HHD Rail - Additional Functionality
- From Sales screen user selects 'Three-Day Travel' in the Ticket Type list...
- Connection Success?
- Go to Card Payment flow.
- Tries Remaining?
- Back to 'Sales'  with Three-Day Product selected and price displayed. From here it can be added to the basket.
- Back to 'Sales' screen.
- Go back to 'View Basket/Reconnecting/Status Bar/Connecting' screen.
- HHD - Payment with Card
- Amount too large?
- Payment Type?
- Chip & PIN card?
- Over £45, customer decides Chip & PIN, or payment device asks customer to insert their card?
- Go to Chip & PIN flow.
- Go Back to 'User to Present Card' then follow Chip & PIN Flow.
- Transaction Success?
- Print a receipt for customer to sign. Print will go through same checks - if you cannot print the user will need to annul the transaction.
- Customer Attempting PIN Entry
- Continue back to relevant flow.
- Continue back to relevant flow.
- Back to Sales.
- Transaction Success?
- Go to the 'Receipt Print' flow.
- Continue back to relevant flow.
- HHD Rail - Smartcard Sales Mode
- HHD Glider - Smartcard Sales Mode
- Following on from 'Inspection - Invalid' screen and pressing the 'Validate' button...
- Following on from 'Inspection - Invalid' screen and pressing the 'Validate' button...
- Smartcard not previously Presented & Validated?
- Go back to Sales screen.
- Smartcard not previously Presented & Validated?
- Go to 'Concessionary Card - Sales mode' screen.
- Go back to Sales screen.
- Valid Smartcard?
- Valid Smartcard?
- Go back to Sales screen.
- Go to 'Sales mode' screen.
- Go back to Sales screen.
- Go to 'Concessionary Card - Sales mode' screen.
- Go to 'Top Up Receipt Print' flow.
- Go to 'Card validation success?' check above.
- Go back to Sales screen.
- Go back to Sales screen.
- Back to Sales screen.
- See Card Payment flow.
- Go to 'Top Up Receipt Print' flow.
- Go to 'Card validation success?' check above.
- Go to 'Top Up Receipt Print' flow.
- Go to 'Card validation success?' check above.
- Go to relevant 'Cash / Payment Card Print Flow' flow.
- Go to 'Represent Smartcard' screen.
- Go to 'Concessionary Print' flow.
- Back to Sales screen.
- Go back to Sales screen.
- Go back to Sales screen.
- Back to Sales screen.
- Payment card used?
- Go to 'Top Up Receipt Print' flow.
- Go to 'Card validation success?' check above.
- Go to relevant 'Cash / Payment Card Print Flow' flow.
- Back to Sales screen.
- See Card Payment flow.
- Go to the 'Payment Card Receipt Print' flow.
- Back to 'Sales' screen.
- HHD - Print Flow
- Accessed Waybill when Signing Off or in a menu?
- Print success?
- Print success?
- Print success?
- Print success?
- Print Success?
- Print Success?
- Print success?
- Print Success?
- Back to 'Sales' screen or previous flow if applicable.
- Back to 'Sales' screen or previous flow if applicable.
- Back to 'Menu' screen or previous flow if applicable.
- Back to 'Sales' screen or previous flow if applicable.
- Back to 'Sales' screen.
- Back to Supervisor menu.
- Back to 'Printing Receipt' screen.
- Go back to Sales screen.
- Go to Annulment flow seen in 'Driver Menu Functionality'.
- Print Success?
- Print Mini Statement
- Go back to 'Mini Statement' screen.
- Print Success?
- Back to 'Printing Ticket - No Header' screen.
- Go back to Sales screen.
- Print success?
- Go to Annulment flow seen in  'Driver Menu Functionality'.
- Go back to Sales screen.
- Back to 'Printing Receipt' screen.
- Go back to Sales screen.
- Back to 'Sales' screen.
- Go to 'Printing Ticket - No Header' screen.
- Go to 'Printing Ticket' screen.
- Back to relevant menu.
- Go to 'Login' flow.
- Back to 'Sales' screen.
- Go back to 'Printing Waybill' screen.
- Go back to 'Waybill' screen.
- Go to 'Login' flow.
- Go to 'Printing Waybill' screen.
- Back to 'Sales' screen or previous flow if applicable.
- Go to Annulment flow seen in 'Driver Menu Functionality'.
- Print success?
- Back to 'Printing Receipt' screen.
- Go back to Sales screen.
- Back to 'Sales' screen or previous flow if applicable.
- HHD Glider & Rail - Smartcard Top Up
- Smartcard Readable?
- Valid top-up card?
- Back to 'Present Smartcard' screen.
- Any products available?
- Back to 'Sales' screen.
- Back to 'Present Smartcard' screen.
- Back to 'Sales' screen.
- Back to 'Present Smartcard' screen.
- See Card Payment flow.
- Smartcard Readable?
- Valid top-up card?
- Back to 'Sales' screen.
- Payment card used?
- Payment card used?
- Back to 'Represent Smartcard' screen.
- Back to 'Represent Smartcard' screen.
- Go to 'Card Payment Receipt Print' Flow
- Back to 'Sales' screen.
- Go to 'Card Payment Receipt Print' Flow
- Back to 'Sales' screen.
- HHD Rail - Validation & Expired Card Top Up
- Smartcard Readable?
- Smartcard Already Presented & Validated previously?
- Smartcard Valid?
- Back to Sales screen.
- Back to 'Sales' screen.
- Go to 'Top Up Receipt Print' flow.
- Back to Sales screen.
- Back to 'Sales' screen.
- Back to Sales screen.
- Back to Sales screen.
- A third party app opens. A Penalty Fare ticket also prints.
- Go to Penalty Warning print flow.
- Back to 'Sales' screen.
- Back to Sales screen.
- See Card Payment flow.
- Smartcard Readable?
- Valid top-up card?
- Payment card used?
- Back to 'Represent Smartcard' screen.
- Back to 'Represent Smartcard' screen.
- Payment card used?
- Able to print?
- Go to the 'Card Payment Receipt Print' flow.
- Back to 'Sales' screen.
- Back to 'Sales' screen.
- Go to the 'Card Payment Receipt Print' flow.
- Back to 'Sales' screen.
- HHD Glider - Inspection & Validation
- Smartcard Readable?
- Smartcard Already Presented & Validated previously?
- Go to 'Smartcard Readable?' check above.
- Go to 'Top Up Receipt Print' flow.
- Back to Sales screen.
- Back to 'Sales' screen.
- Passed pre-validation checks?
- Has the Smartcard been validated?
- Back to 'Sales' screen.
- User chooses to issue a penalty fare and third party app opens. A Penalty Fare ticket also prints.
- Go to Penalty Warning print flow.
- Back to 'Sales' screen.
- Back to Sales screen.
- Go to Penalty Warning print flow.
- Back to Sales screen.
- User chooses to issue a penalty fare and third party app opens. A Penalty Fare ticket also prints.
- User chooses to issue a penalty fare and third party app opens. A Penalty Fare ticket also prints.
- Go to Penalty Warning print flow.
- Back to 'Sales' screen.
- Back to 'Sales' screen.
- Back to Sales screen.
- Card Type?
- Go to 'Discount Card Sales' flow.
- Smartcard readable?
- Card validation success?
- Back to 'Sales' screen.
- Correct Card presented?
- Go to 'Top Up Receipt Print' flow.
- Go to 'Smartcard Readable?' check above.
- Back to Sales screen.
- Back to 'Sales' screen.
- Back to 'Represent Smartcard' screen.
- Go to 'Top Up Receipt Print' flow.
- Go to 'Card validation success?' check above.
- Back to Sales screen.

### Annotations / Spec Notes (81)
- If no Card or Warrant option is available
- If the basket is full
- User can swipe Boarding & Alighting Stages, Passenger Type and Ticket Type to quickly go to the next option.  For example, swipe '1 Adult' to change to '1 Child'.  On Glider, 'Passenger Type' field cannot be swiped, for Rail, 'Ticket Type' cannot be swiped.
- This screen is only displayed when the operator attempts to add a favourite to a full basket.   If the operator attempts to add more tickets to the basket from the sales screen the Add To Basket button will grey out once the basket gets full.   If the basket is full and the user attempts to add a favourite, the 'Basket Full' screen will appear.  There will be a 3 second timeout, or the user can tap 'Back to Basket' to manage their basket, or issue the tickets in the basket.  The basket is full once there are 9 ticket lines.
- Pressing the ABC icon will change the view to alphanumeric.
- The current stage is highlighted in the middle of the screen.  Search and other functionality is the same as the Alighting Stage selection below. Tapping the number icon will change the view to numerical input.
- When on rail, the Passenger Types are not increased, just selected. The amount of tickets are based on Ticket Type numbers selected.
- When first arriving on 'Select Passenger Type' screen, the first product is set to 1.
- When on rail, the Ticket Types can be increased or decreased. Ticket Types are dependant on the Passenger Type selected.
- The price of the basket / ticket will be displayed in the header and in the £ Price field by default.  Warrant is used for paper tickets only, not top-ups. They will appear on Waybills and are available on Rail only.
- If different items are added to the basket they will be listed. The product area (1 Single | 1 Return etc.) will be scrollable if required. The monetary value on the left represents the currently selected product; the value on the right is the basket total.
- When cross border (XB) stations are set the operator can only view/select XB (not local) ticket types.  When local stations are set the operator can only view/select local (not XB) ticket types.
- 1. The operator can simply press the cash button to issue the ticket without having to enter amount given.  2. If the operator enters amount given and presses cash button HHD will calculate change due.  The operator can also use £5, £10 and £20 buttons for transaction below £20 without the need for pressing the cash button. HHD at that point will also calculate the change due.
- No Valid Tickets Available
- Three Day Product
- Currency Change Available
- User must choose a day within 4 days from today, and then the remaining 2 days within the next 7 days from the first date chosen.
- If a user chooses a Boarding and Alighting Stage that does not have a valid ticket, this error screen will display.  After 3 seconds, it will time out and take the user back to the Sales screen, with the Boarding and Alighting Stages that were selected shown, and Ticket Type & Passenger Type being disabled.
- From this screen tapping the back button on the device will take the operator to the Ticket Type Selection screen.   Tapping the 'Cancel' button from any other screen from this flow will take the operator to the Sales screen.
- Currency change is only available on cross border rail journeys i.e. :-   1. When the boarding station is between 1 and 61 AND the alighting station is between 62 and 96 then currency change is available but the default currency is in Sterling   2. When the boarding station is between 62 and 96 then currency change is available but the default currency is in Euro   If a currency change is available, the user will have the option to swipe right on the action bar in the Sales Area before adding items to the basket, or they can change currency in the Payment Area by tapping the 'To Pay' area above the Cash button.  Warrant is used for paper tickets only, not top-ups. They will appear on Waybills and are available on Rail only.
- If the user chooses to edit the first date after picking it anywhere in this flow, they will be taken back to the start of this flow ('3 Day Travel Chosen').  User will tap to select a date, and tap again to deselect the date.
- Advanced Ticket
- Users can purchase an advanced ticket if the option is available. Parameters for advanced tickets are set within CloudFare. The user must choose only one product, then navigate to the Basket. If they can book an advanced ticket, they will see the 'Advanced Ticket?' button in the basket. Tapping this will take them to a date picker where they can choose the date of travel, and tapping confirm will set the date.
- Reconnect attempt can be tried 3 times before advising to notify a Supervisor or Technician.
- The payment device has to be activated if in sleep mode.
- Only one advanced ticket can be added to the basket.
- This check only occurs on test transactions, not for commercial use.
- The sub-message will be 'Amount too large'. Timeout of 3 seconds and back to the Payment Area.
- Timeout of 3 seconds and back to Payment Area.
- Timeout of 3 seconds and back to Payment Area. The error message will be matched to the payment device.
- Timeout of 3 seconds and back to Payment Area.
- This flow is specifically for;  1. yLink Smartcards 2. 24+ Smartcards 3. Half Fare Smartcards (5 different types).
- Concession & Half Fare Card Presented
- Discount Card Presented
- Discount Card Presented (yLink Only)
- Concessionary Card Presented
- On validation, a Transaction Record is sent to the back office.
- All Half Fare Smartpass products will display the words "Half Fare Smartpass", and not the sub product name (PIPS, Disability Living allowance, Partially Sighted, No Driving Licence and Learning Disability).
- The error could be "Not valid at this Location", "Card Expired"
- 1. For Dependants Pass, Senior, Blind, War Pensioner, 60+ and ROI Senior single is the only product option for local travel i.e. where boarding station and alighting station are both 61 or less.    2. For Senior, Blind, War Pensioner and ROI Senior XB single, XB day return and XB 1 month return are the product options for Cross border travel i.e. where boarding station or alighting station are greater than 61.
- The error could be "Not valid at this Location", "Card Expired"
- 1. ylink and 24+ cards have single, return, weekly and monthly options for local stations only (there are no valid options for these products on cross border journeys)   2. Half fare Smartpasses have single and return options for local stations only (there are no valid options for these products on cross border journeys).  If any of these cards are presented for stages above stage 61, HHD will display "Not Valid at This Location" screen.
- Important to note that on Rail HHD:-  1. The selected alighting station chosen by the operator is recorded in the audit data for Free Concessionary smartpasses  2.  The fare foregone (i.e. what the Adult Single would have cost a fare paying customer) is captured in the audit data for this free transaction  3.  The operator must be able to change the boarding station and/or the alighting station after they have presented the Smartpass (as well as before)
- Free concession cards will display £0.00 in the price field.
- Warrant is used for paper tickets only, not top-ups. They will appear on Waybills and are available on Rail only.
- Payment Card Receipt Print Flow
- Top Up Receipt Flow
- Concessionary Print Flow
- Penalty Fare Warning Print Flow
- Versioning Print Flow
- Barcode Travel Ticket Print Flow
- Mini Statement Print Flow
- Waybill Print Flow
- Cash Print Flow
- Payment Card Print Flow
- If a merchant receipt is printed this will be 'printing 1 of 2'.
- The screen before this will be the 'Transaction Approved' screen as seen in the card payment flows. This flow covers printing only.
- If the user cannot print, they must annul the transaction.
- If the user cannot print, they must annul the transaction.
- Barcodes are only validated once the Operator confirms a ticket has successfully printed.
- Barcodes are only validated once the Operator confirms a ticket has successfully printed. Only one reprint attempt is allowed if a print fails.
- If a merchant receipt is printed it will go to receipt printing screen (1 of 1).  If 'No' is selected, the merchant receipt will still print if it's configured to do so in the back office. If yes, both will print. It will follow the Payment card receipt flow.
- If the user cannot print, they must annul the transaction.
- If the smartcard has an expiry date set, this screen will display.
- If the smartcard has a product added, you can only add the same period type.
- For DayLink this will display days and for period cards this will display periods.
- If the smartcard has too many journeys, the user cannot add more. The minimum amount of journeys a user can add is 5.
- If the 'Card' option was selected, the banner will read 'Card Payment' instead.
- At this point the card top up receipt should be printed. If the transaction was paid for by an EMV card then Card Payment should be displayed at the top of the screen as per Card Payment Print flow screen 2.4.3.3.   If cash was used, the screen should display £x.xx change.  N.B. 'Card Payment Receipt' header will only show if card was the payment method, otherwise it will be replaced with '£Price Change' if applicable. This also applies to the Transaction Complete screen.  The Transaction Complete screen displays 'days left' for DayLink cards, 'journeys left' for Multi Journey cards. Period Passes show the new expiry date.  Print will still go through same checks seen in Print flows.
- Top-up is iLink only. Validation includes iLink, Staff, Spouse, Retired, External and aLink.
- N.B. Error message could read: - Not valid at this location - Hotlisted Card - Product Expired
- On validation, a Transaction Record is sent to the back office.
- N.B. '£Price change' header will only show if cash was the payment method, otherwise card payment screen will display instead - this will be 1 of 2 for print due to additional receipts for card payment.  Print will still go through same checks seen in Print flows.
- For a card payment, there will be a check to see if you also want to print the customer receipt as seen in the 'Payment Card Print' flow.
- On validation, a Transaction Record is sent to the back office.
- Other cards will display the tick and then        [PRODUCT NAME]              Validated  below the tick.  See 'Validation Successful' screen on the Rail flow for reference.
- Message will read:  - Product Expired - Pass Expired - No Journeys Left - No Balance Left - Hotlisted Card
- Expiry & Last Used Dates show as N/A when not required.
- Expiry & Last Used Dates show as N/A when not required.
- N.B. Error message will read: Visual Rejection
- Other cards will display the tick and then        [PRODUCT NAME]              Validated  below the tick.  See 'Validation Successful' screen on the Rail flow for reference.

### Connections / Flow (365)
- Decision: "Payment Type?" → Decision: "Over £45, customer decides
Chip & PIN, or payment device
asks customer to insert their card?" [Contactless
]
- Decision: "Print success?" → Screen: "8.5.2.1 Printing Failed - Card" [No]
- Screen: "2.4.0.1 Payment Area - No Warrant" → Screen: "4.4 Represent Smartcard" [User chooses preset cash option,
or if customer has correct amount,
taps the 'Cash' button.
]
- Decision: "Print Success?" → Screen: "8.5.2.1 Printing Failed - Card" [No]
- Screen: "2.6.7 Validation - Success" → Decision: "Go back to Sales screen." [1 second timeout...]
- Decision: "Go to Penalty Warning print flow." → Decision: "Back to Sales screen." [Once the Print
flow is complete...
]
- Screen: "2.3.1.1 Basket - Edit" → Screen: "22 - Sales - Select Product" [User taps
'Single'.
]
- Decision: "Valid top-up card?" → Decision: "Any products
available?" [Yes]
- Screen: "4.8 Transaction complete" → Decision: "Back to 'Sales' screen." [3 second timeout...]
- Decision: "Smartcard
Readable?" → Screen: "2.5.4.1 Critical Error" [No]
- Screen: "3.3.1 Error" → Decision: "Go to Penalty Warning print flow." [User taps
'Penalty Warning'.
Penalty Warning
ticket prints.
]
- Decision: "Connection Success?" → Screen: "2.5.3 View Basket/Reconnecting/Status Bar/Not Connected" [No]
- Screen: "2.4.0.1 Payment Area - No Warrant" → Screen: "4.4 Represent Smartcard" [User chooses preset cash option,
or if customer has correct amount,
taps the 'Cash' button.
]
- Screen: "2.3 Items in Basket" → Screen: "2.3.1 Basket Functionality - EditDuplicate" [User swipes right
on a Basket item.
]
- Decision: "Payment card used?" → Decision: "Back to 'Sales' screen." [No]
- Decision: "Has the Smartcard
been validated?" → Screen: "3.1 Inspection - Valid" [Yes]
- Screen: "4.1.1 Critical Error - Incorrect Card" → Decision: "Back to 'Present Smartcard' screen." [User taps
'Retry' button.
]
- Decision: "Print Success?" → Screen: "27 Barcode Ticket - Printed?" [Yes]
- Screen: "2.4 Payment Area" → Decision: "Go to relevant 'Cash / Payment Card Print Flow' flow." [User taps 'Warrant'.]
- Screen: "2.3.1.1.1 Basket - Line Edited" → Screen: "2.3 Items in Basket" [User taps
'Confirm Edit'.
]
- Screen: "3.3.1 Error" → Decision: "Go to Penalty Warning print flow." [User taps
'Penalty Warning'.
Penalty Warning
ticket prints.
]
- Decision: "Following on from 'Inspection - Invalid' screen and pressing the 'Validate' button..." → Screen: "2.6.5 Concessionary Card - Sales mode"
- Decision: "Payment card used?" → Decision: "Back to 'Sales' screen." [No]
- Decision: "Tries Remaining?" → Screen: "2.5.3.1 View Basket/Reconnecting/Status Bar/Not Connected/Contact Supervisor" [No]
- Decision: "User chooses to issue a penalty fare and third party app opens.
A Penalty Fare ticket also prints." → Decision: "Back to 'Sales' screen."
- Screen: "3.1 Inspection - Valid" → Decision: "Back to 'Sales' screen." [User taps 'Valid'.]
- Decision: "Print success?" → Screen: "7.2 Print Failed" [No]
- Screen: "2.4.2 Payment/Card/User to Present Card" → Decision: "Amount too large?" [Operator hands payment device over to
customer to insert or swipe their card.
If it's contactless, the customer can present
their card to the device straight away.
]
- Screen: "2.6.2 Discount - Summary" → Screen: "2.4 Payment Area" [User taps
'Pay' button.
]
- Screen: "2.6.6 Concessionary - Summary" → Decision: "Go back to Sales screen." [User taps 'Clear Basket'.]
- Decision: "Go to relevant 'Cash / Payment Card Print Flow' flow." → Screen: "2.0 Sales Screen" [On success...]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Payment card used?" [User taps
'Cancel' button.
]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Back to 'Represent Smartcard' screen." [User taps 'Retry' button.]
- Decision: "Chip & PIN card?" → Decision: "Go to Chip & PIN flow." [Yes, Chip & PIN
available.
]
- Screen: "3.3.1 Error" → Decision: "Go to Penalty Warning print flow." [User taps
'Penalty Warning'.
A Penalty Warning ticket prints.
]
- Screen: "2.6.6 Concessionary - Summary" → Decision: "Go to 'Concessionary Print' flow." [User taps 'Issue Ticket'.]
- Decision: "Go to 'Top Up Receipt Print' flow." → Decision: "Back to Sales screen." [Once Print flow is complete...]
- Decision: "Customer Attempting
PIN Entry" → Screen: "2.4.2.8 Payment/Card/Declined" [Failed set amount of times]
- Screen: "3.3.1 Error" → Decision: "User chooses to issue a penalty fare and third party app opens.
A Penalty Fare ticket also prints."
- Screen: "2.0.6 Sales Screen - Rail Login" → Decision: "Smartcard Readable?" [User presents smartcard...]
- Decision: "Transaction Success?" → Screen: "2.4.2.6 Payment/Card/Transaction Success" [Yes]
- Screen: "3.3.1 Error" → Decision: "A third party app opens.
A Penalty Fare ticket also prints." [User taps 'Penalty Fare'.]
- Screen: "8.5.1 Print Receipt?" → Screen: "8.5.1.1 Printing Receipt - Card" [Yes - Print]
- Screen: "3.2 Inspection - Invalid" → Screen: "3.3.1 Error" [User taps
'Penalty Fare'.
]
- Decision: "Valid top-up card?" → Screen: "4.1.1 Critical Error - Incorrect Card" [No]
- Screen: "2.4 Payment Area" → Decision: "Back to 'Sales' screen." [User taps
'Cancel'.
]
- Decision: "Print success?" → Screen: "2.4.3.2.1 Print Failed - Card" [No]
- Decision: "Card Type?" → Screen: "2.6.5 Concessionary Card - Sales mode" [User decides to validate smartcard
    (non-discounted smart cards)
]
- Decision: "Payment card used?" → Decision: "Back to 'Sales' screen." [No]
- Screen: "2.4.2.5 Payment/Card/Processing Transaction" → Screen: "2.4.2.3 Payment/Card/PIN Entry"
- Screen: "4.2.1 Top Up - No products available" → Decision: "Back to 'Present Smartcard' screen." [User presses
the back
button on HHD.
]
- Decision: "Smartcard
Readable?" → Decision: "Valid top-up card?" [Yes]
- Decision: "Go to Penalty Warning print flow." → Decision: "Back to Sales screen." [Once the Print flow is complete...]
- Screen: "8.5.2.1 Printing Failed - Card" → Decision: "Go back to 'Printing Waybill' screen." [User taps
'Retry'.
]
- Decision: "Print Success?" → Screen: "2.4.3.2 Print Failed" [No]
- Decision: "Print success?" → Screen: "8.5.2.1 Printing Failed - Card" [No]
- Decision: "Transaction Success?" → Screen: "2.4.2.8 Payment/Card/Declined" [No]
- Decision: "See Card Payment flow." → Screen: "4.4 Represent Smartcard" [Successful card
payment.
]
- Decision: "Valid top-up card?" → Screen: "4.1.2 Critical Error - Invalid Card" [No
]
- Screen: "2.6.7 Validation - Success" → Decision: "Back to 'Sales' screen."
- Screen: "2.4.1 Payment Area/Cash/Keyboard" → Screen: "2.4.1.1 Payment Area/Cash/Keyboard/Specific Amount" [User enters amount using
numerical pad. User tapping
the tick would close the keypad.
]
- Decision: "Print Success?" → Screen: "7.1 Transaction complete" [Yes]
- Decision: "See Card Payment flow." → Screen: "4.4 Represent Smartcard" [Successful card
payment.
]
- Screen: "8.5.2.1 Printing Failed - Card" → Decision: "Go to 'Printing Ticket - No Header' screen." [User taps
'Retry'.
]
- Screen: "8.5.2.1 Printing Failed - Card" → Decision: "Back to 'Sales' screen." [User taps
'Cancel'.
]
- Decision: "Able to print?" → Screen: "7.2 Print Failed" [No]
- Screen: "2.6.2.1 Discount - Summary - Rail" → Screen: "2.4 Payment Area" [User taps
'Pay'.
]
- Decision: "Payment card used?" → Screen: "4.6 Voiding Last Card Transaction" [Yes]
- Screen: "22.4 - Sales - 3 Day Travel Chosen - Third Date Chosen" → Decision: "Back to 'Sales' screen." [User taps
'Cancel'.
]
- Decision: "Smartcard Already Presented & Validated previously?" → Screen: "2.5.4.2 Error - Passback" [Yes]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Back to 'Sales' screen." [User taps 'Cancel' button.]
- Screen: "2.4.2.6 Payment/Card/Transaction Success" → Decision: "Continue back to relevant flow."
- Screen: "3.2.3 Smartcard Not Valid - No Travel Remaining" → Screen: "4.2.2 Top Up - iLink - Select Product" [User taps 'Top-Up'.]
- Screen: "8.5.2.1 Printing Failed - Card" → Decision: "Go back to 'Waybill' screen." [User taps
'Cancel'.
]
- Screen: "4.6 Voiding Last Card Transaction" → Decision: "Go to 'Card Payment Receipt Print' Flow"
- Decision: "Payment Type?" → Screen: "2.4.2.4 Payment/Card/User to Confirm Amount" [Customer inserts card to trigger Chip & PIN flow.]
- Decision: "Payment card used?" → Screen: "4.6 Voiding Last Card Transaction" [Yes]
- Decision: "Go to 'Top Up Receipt Print' flow." → Decision: "Back to Sales screen." [Once Print flow is complete...]
- Screen: "2.0 Sales Screen" → Decision: "Smartcard
Readable?" [Smartcard presented and pre-validation
         are checks carried out
]
- Screen: "2.4 Payment Area" → Decision: "Go to relevant 'Cash / Payment Card Print Flow' flow." [User chooses preset cash option,
or if customer has correct amount,
taps the 'Cash' button, or taps Warrant if applicable.
]
- Screen: "8.5.1 Print Receipt?" → Decision: "Back to 'Sales' screen or previous flow if applicable." [User taps 'No'.]
- Screen: "2.5 View Basket/Reconnect Card Reader" → Screen: "2.5.3.2 View Basket/Reconnecting/Status Bar/Connecting" [User taps
'Card' button.
]
- Decision: "Print success?" → Screen: "Print Success" [Yes]
- Decision: "Smartcard Valid?" → Screen: "3.3.1 Error" [No - Other Issue]
- Decision: "Smartcard Valid?" → Screen: "2.6.7 Validation - Success" [Yes - valid.]
- Decision: "Valid top-up card?" → Screen: "8.5 Printing Receipt - Cash" [Yes]
- Screen: "2.5.4.1 Critical Error" → Decision: "Back to 'Represent Smartcard' screen." [User taps
'Retry' button.
]
- Screen: "2.3.1 Basket Functionality - EditDuplicate" → Screen: "2.3.1.2 Item in Basket
Duplicated" [User taps
'Duplicate'.
]
- Decision: "A third party app opens.
A Penalty Fare ticket also prints." → Decision: "Back to 'Sales' screen."
- Decision: "Payment card used?" → Decision: "Back to 'Sales' screen." [No]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Payment card used?" [User taps
'Cancel' button.
]
- Screen: "7. Printing Waybill" → Decision: "Print Success?"
- Screen: "2.3 Items in Basket" → Screen: "2.4 Payment Area" [User taps 'Pay'.]
- Screen: "22.1 - Sales - 3 Day Travel Chosen" → Screen: "22.2 - Sales - 3 Day Travel Chosen - First Date Chosen" [User taps
Saturday 31st.
]
- Screen: "Print Success" → Decision: "Back to 'Menu' screen or previous flow if applicable." [3 second timeout
or user taps Tick.
]
- Screen: "2.3.1 Basket Functionality - EditDuplicate" → Screen: "2.3.1.1 Basket - Edit" [User taps 'Edit'.]
- Decision: "Valid top-up card?" → Screen: "4.1.2 Critical Error - Invalid Card" [No]
- Screen: "2.0 Sales Screen" → Screen: "4.1 Present Smart Card" [User taps
Smartcard
top up icon.
]
- Decision: "See Card Payment flow." → Decision: "Go to relevant 'Cash / Payment Card Print Flow' flow." [Card payment success...]
- Screen: "3.1 Inspection - Valid" → Screen: "3.3.1 Error" [User taps 'Not Valid'.]
- Screen: "2.5.4.1 Critical Error" → Decision: "Payment card used?" [User taps
'Cancel' button.
]
- Decision: "Card Type?" → Decision: "Go to 'Discount Card Sales' flow." [yLink - user decides to validate smartcard
   (discounted smart cards)
]
- Screen: "2.0.8 Select Alighting - List - Search Tapped - Search Entered - No Matches" → Screen: "2.0.4 Select Alighting - List - Search Tapped - Search Entered" [User clears search
using delete key
on keypad, types new
search and presses tick.
]
- Screen: "2.6.2 Discount - Summary" → Decision: "Go back to Sales screen." [User taps
'Clear Basket'.
]
- Screen: "8.5.2.1 Printing Failed - Card" → Decision: "Print Mini Statement" [User taps
'Retry'.
]
- Decision: "Print success?" → Screen: "8.5.1 Print Receipt?" [Yes]
- Screen: "22.4 - Sales - 3 Day Travel Chosen - Third Date Chosen" → Decision: "Back to 'Sales'  with Three-Day Product selected and price displayed. From here it can be added to the basket." [User taps
'Continue'.
]
- Screen: "2.4.0.1 Payment Area - No Warrant" → Decision: "See Card Payment flow." [User taps
'Card' button.
]
- Screen: "2.0 Sales Screen" → Screen: "22 - Sales - Select Product - Glider" [User taps 
'Single'.
]
- Decision: "See Card Payment flow." → Decision: "Go to relevant 'Cash / Payment Card Print Flow' flow." [Successful card
payment.
]
- Decision: "Correct Card
presented?" → Screen: "4.1.2 Critical Error - Invalid Card" [No]
- Screen: "7.1 Transaction complete" → Decision: "Go to 'Login' flow."
- Screen: "2.0 Sales Screen" → Screen: "2.0.2 Select Alighting - List - HHD Screen Size" [User taps an
Alighting Stage
]
- Decision: "User chooses to issue a penalty fare and third party app opens.
A Penalty Fare ticket also prints." → Decision: "Back to 'Sales' screen."
- Screen: "11.3 Printing Waybill" → Decision: "Print Success?"
- Screen: "2.4.3.1 Printing Ticket - No Header" → Decision: "Print Success?"
- Decision: "Smartcard not previously Presented & Validated?" → Decision: "Valid Smartcard?" [Yes]
- Decision: "Smartcard
Readable?" → Decision: "Smartcard Already Presented & Validated previously?" [Yes]
- Screen: "2.6.5.2 Concessionary Card - Sales mode - Rail - Return Chosen" → Screen: "2.6.6 Concessionary - Summary" [User taps
Action Bar.
]
- Screen: "2.4.2.5 Payment/Card/Processing Transaction" → Decision: "Transaction Success?"
- Screen: "2.6.0.1 Discount - Sales mode - Alighting Selected" → Screen: "2.6.2 Discount - Summary" [User taps printer.]
- Screen: "2.4.2.5 Payment/Card/Processing Transaction" → Decision: "Transaction Success?"
- Decision: "Any products
available?" → Screen: "4.2.1 Top Up - No products available" [No]
- Screen: "4.4 Represent Smartcard" → Decision: "Smartcard
Readable?" [Customer represents smartcard.]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Payment card used?" [User taps
'Cancel' button.
]
- Screen: "2.4 Payment Area" → Screen: "4.4 Represent Smartcard" [User chooses preset cash option,
or if customer has correct amount,
taps the 'Cash' button, or user taps 'Warrant' if applicable.
]
- Decision: "Passed pre-validation
checks?" → Screen: "3.3.1 Error" [No]
- Decision: "Connection Success?" → Decision: "Go to Card Payment flow." [Yes]
- Screen: "3.3.1 Error" → Decision: "User chooses to issue a penalty fare and third party app opens.
A Penalty Fare ticket also prints."
- Decision: "Go to Penalty Warning print flow." → Decision: "Back to Sales screen." [Once the Print
flow is complete...
]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Back to 'Represent Smartcard' screen." [User taps 'Retry' button.]
- Screen: "2.6.5 Concessionary Card - Sales mode" → Decision: "Smartcard readable?" [Smartcard presented.]
- Decision: "Amount too large?" → Decision: "Payment Type?" [No]
- Screen: "2.5.3.2 View Basket/Reconnecting/Status Bar/Connecting" → Decision: "Connection Success?"
- Screen: "12.2 Printing Receipt" → Decision: "Print Success?"
- Decision: "Able to print?" → Screen: "2.4.3.1 Transaction complete" [Yes]
- Screen: "26.2 Print Mini Statement" → Decision: "Print success?"
- Screen: "2.4.2.4 Payment/Card/User to Confirm Amount" → Screen: "2.4.2.1 Payment/Card/User Cancelled Transaction" [Customer cancels transaction
on the payment device.
]
- Decision: "Payment card used?" → Screen: "4.6 Voiding Last Card Transaction" [Yes]
- Decision: "Any products
available?" → Screen: "4.2 Top Up - Select Amount" [Yes]
- Screen: "2.4.2.7 Payment/Card/Signature Okay?" → Screen: "4.6 Voiding Last Card Transaction" [User taps 'No' because the signature
didn't match the payment card.
]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Go to 'Concessionary Card - Sales mode' screen." [User taps
'Retry' button.
]
- Screen: "2.4.3.3 Printing Ticket - Card" → Decision: "Print success?"
- Screen: "2.5.4.2 Error - Passback" → Decision: "Back to 'Sales' screen."
- Decision: "Smartcard not previously Presented & Validated?" → Screen: "2.5.4.2 Error - Passback" [No]
- Screen: "8.5.1.1 Printing Receipt - Card" → Decision: "Print success?"
- Screen: "4.6 Voiding Last Card Transaction" → Decision: "Go to 'Card Payment Receipt Print' Flow"
- Screen: "2.2 Add To Basket" → Screen: "2.2.1 Add Another to Basket" [User taps
'Add to Basket'
icon to add
another to the
basket.
]
- Screen: "22 - Sales - Select Product - Glider" → Screen: "2.0.10 Sales Screen - Different Ticket Type Selected" [User taps
'Adult Return'.
]
- Decision: "Print success?" → Screen: "7.2.1 Print Failed Card Payment" [No]
- Screen: "2.2.1 Add Another to Basket" → Screen: "2.3 Items in Basket" [User taps
basket icon.
]
- Decision: "Chip & PIN card?" → Screen: "2.4.2.4 Payment/Card/User to Confirm Amount" [No Chip & PIN
available.
]
- Screen: "8.5.2.1 Printing Failed - Card" → Decision: "Back to 'Printing Ticket - No Header' screen." [User taps
'Retry'.
]
- Screen: "4.4 Represent Smartcard" → Decision: "Go to relevant 'Cash / Payment Card Print Flow' flow." [User represents
correct Smartcard.
]
- Screen: "3.3.1 Error" → Decision: "Go to Penalty Warning print flow." [User taps 'Penalty Warning'.
Penalty Warning ticket prints.
]
- Screen: "2.0 Sales Screen" → Screen: "2.0.12 Sales Screen - Paper Ticket Inspect" [User swipes from the right
inwards on the action bar to
do a paper ticket inspection.
]
- Screen: "4.2 Top Up - Select Amount" → Screen: "2.4.0.1 Payment Area - No Warrant" [Journey
amount selected.
]
- Screen: "2.6.1 - Discount - Sales mode - Select Product" → Screen: "2.6.1.1 Discount - Sales mode - Return Chosen" [User taps
'Return'.
]
- Decision: "Payment Type?" → Decision: "Chip & PIN card?" [Customer Swipes card.]
- Decision: "Payment card used?" → Screen: "4.6 Voiding Last Card Transaction" [Yes]
- Screen: "2.6.5 Concessionary Card - Sales mode" → Screen: "4.1.2 Critical Error - Invalid Card" [Incorrect Smartcard
presented.
]
- Screen: "2.0 Sales Screen" → Screen: "2.0.7 Select Boarding - List - HHD Screen Size" [User taps a
Boarding Stage.
]
- Screen: "2.6.1.1 Discount - Sales mode - Return Chosen" → Screen: "2.6.2.1 Discount - Summary - Rail" [User taps
'Print' icon.
]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Go back to Sales screen." [User taps
'Cancel' button.
]
- Screen: "4.4 Represent Smartcard" → Decision: "Smartcard
Readable?" [Customer represents smartcard.]
- Decision: "Continue back to relevant flow." → Decision: "Back to Sales." [Once print is finished...]
- Decision: "Card validation
success?" → Screen: "3.2.2 Successful Validation" [Yes]
- Decision: "Print Success?" → Screen: "8.5.2.1 Printing Failed - Card" [No]
- Screen: "2.0.14 Error - No Valid Tickets Available" → Screen: "2.0.14.1 Error - No Valid Tickets - Sales" [3 second timeout.]
- Decision: "Has the Smartcard
been validated?" → Screen: "3.2 Inspection - Invalid" [No]
- Screen: "27 Barcode Ticket - Printed?" → Screen: "7.1 Transaction complete" [User
taps 'Yes'.
]
- Decision: "Smartcard not previously Presented & Validated?" → Screen: "2.5.4.2 Error - Passback" [No]
- Decision: "Smartcard Readable?" → Screen: "3.3 Error - Read/Write Fail" [No - not
readable.
]
- Screen: "2.5.4.1 Critical Error" → Decision: "Payment card used?" [User taps 'Cancel' button.]
- Screen: "4.4 Represent Smartcard" → Screen: "4.1.2 Critical Error - Invalid Card" [Incorrect Smartcard
presented.
]
- Decision: "Go to 'Top Up Receipt Print' flow." → Decision: "Back to Sales screen." [Once the Print flow is complete...]
- Screen: "2.4.3.1 Transaction complete" → Decision: "Back to 'Sales' screen." [3 second timeout
or user taps Tick.
]
- Decision: "Print success?" → Decision: "Back to 'Sales' screen or previous flow if applicable." [Yes]
- Screen: "2.4 Payment Area" → Decision: "See Card Payment flow." [User taps 'Card'
button.
]
- Screen: "2.6.1 Discount - Sales mode - Rail" → Screen: "2.6.1 - Discount - Sales mode - Select Product" [User taps 'Single'
to select
a ticket type.
]
- Screen: "2.5.4.1 Critical Error" → Decision: "Back to 'Represent Smartcard' screen." [User taps 'Retry' button.]
- Screen: "2.5.3 View Basket/Reconnecting/Status Bar/Not Connected" → Decision: "Tries Remaining?" [User taps 'Retry'.]
- Screen: "3.3.1 Error" → Decision: "Back to Sales screen."
- Screen: "2.1.1.2 Issue Ticket - Advanced Ticket - Calendar 3" → Screen: "2.1.3 Issue Advanced Ticket" [User taps
'Confirm'.
]
- Screen: "22 - Sales - Select Product" → Screen: "2.3.1.1.1 Basket - Line Edited" [User taps
'Adult Return'.
]
- Screen: "2.0.3 Select Alighting - List - Search Tapped" → Screen: "2.0.8 Select Alighting - List - Search Tapped - Search Entered - No Matches" [User enters stage
name incorrectly 
and presses tick
on keypad.
]
- Decision: "Accessed Waybill
when Signing Off
or in a menu?" → Screen: "7. Printing Waybill" [Signing Off.]
- Screen: "22.2 - Sales - 3 Day Travel Chosen - First Date Chosen" → Screen: "22.3 - Sales - 3 Day Travel Chosen - First & Second Dates Chosen" [User taps
Wednesday 4th.
]
- Decision: "Print Success?" → Screen: "2.4.3.1 Transaction complete" [Yes]
- Decision: "Card validation
success?" → Decision: "Correct Card
presented?" [No]
- Decision: "From Sales screen user selects 'Three-Day Travel' in the Ticket Type list..." → Screen: "22.1 - Sales - 3 Day Travel Chosen"
- Screen: "Print Success" → Decision: "Back to 'Sales' screen or previous flow if applicable." [3 second timeout
or user taps Tick.
]
- Decision: "Smartcard Readable?" → Decision: "Smartcard Already Presented & Validated previously?" [Yes - readable.]
- Screen: "2.1.1 Issue Ticket - Advanced Ticket" → Screen: "2.1.1.1 Issue Ticket - Advanced Ticket - Calendar 2" [User swipes
on the calendar.
]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Go to 'Represent Smartcard' screen." [User taps
'Retry' button.
]
- Decision: "Smartcard
Readable?" → Decision: "Valid top-up card?" [Yes]
- Decision: "See Card Payment flow." → Screen: "4.4 Represent Smartcard" [Successful card
payment.
]
- Screen: "2.5.3.1 View Basket/Reconnecting/Status Bar/Not Connected/Contact Supervisor" → Screen: "2.5 View Basket/Reconnect Card Reader" [User taps
'Back to
Payment'.
]
- Screen: "7.1 Transaction complete" → Decision: "Back to Supervisor menu." [User taps green tick or
timeout of 2 seconds.
]
- Decision: "Print a receipt for customer to sign. Print will go through same checks - if you cannot print the user will need to annul the transaction." → Screen: "2.4.2.7 Payment/Card/Signature Okay?" [Once the receipt
is printed...
]
- Decision: "Amount too large?" → Screen: "2.4.2.8 Payment/Card/Declined" [Yes - limitation reached.]
- Decision: "Print Success?" → Screen: "7.1 Transaction complete" [Yes]
- Screen: "2.4.2.5 Payment/Card/Processing Transaction" → Screen: "2.4.2.6 Payment/Card/Transaction Success"
- Decision: "Print Success?" → Screen: "7.2 Print Failed" [No]
- Screen: "4.6 Voiding Last Card Transaction" → Decision: "Go to the 'Card Payment Receipt Print' flow."
- Decision: "Smartcard readable?" → Decision: "Card validation
success?" [Yes]
- Decision: "Payment card used?" → Screen: "4.6 Voiding Last Card Transaction" [Yes]
- Screen: "2.4.0.1 Payment Area - No Warrant" → Screen: "2.4.2.2 Payment/Card/Initialising Transaction" [User taps 'Card'.]
- Decision: "Correct Card
presented?" → Screen: "3.3 Error - Read/Write Fail" [Yes]
- Decision: "Valid Smartcard?" → Screen: "2.6.1 Discount - Sales mode - Rail" [Yes]
- Screen: "2.1.1.1 Issue Ticket - Advanced Ticket - Calendar 2" → Screen: "2.1.1.2 Issue Ticket - Advanced Ticket - Calendar 3" [User chooses a date in the
calendar. This can be
navigated by swiping up
or down.
]
- Decision: "Go to 'Top Up Receipt Print' flow." → Decision: "Back to Sales screen." [Once the Print flow is complete...]
- Screen: "2.0 Sales Screen" → Screen: "2.2 Add To Basket" [User taps
'Add to Basket'
icon.
]
- Screen: "3.2.3 Smartcard Not Valid - No Travel Remaining" → Decision: "Back to Sales screen." [User taps 'Cancel'.]
- Decision: "Smartcard Already Presented & Validated previously?" → Decision: "Smartcard Valid?" [No - this card has not been
presented previously.
]
- Decision: "Smartcard
Readable?" → Screen: "2.5.4.1 Critical Error" [No]
- Decision: "Transaction Success?" → Screen: "2.4.2.6 Payment/Card/Transaction Success" [Yes]
- Screen: "8.5.2.1 Printing Failed - Card" → Decision: "Go back to Sales screen." [User taps
'Cancel'.
]
- Screen: "2.4 Payment Area" → Decision: "See Card Payment flow." [User taps 'Card' button.]
- Screen: "8.5 Printing Receipt - Cash" → Decision: "Able to print?"
- Screen: "2.0.12 Sales Screen - Paper Ticket Inspect" → Screen: "2.0.13 Sales Screen - Paper Ticket Inspect - Confirmed" [Green confirms
the Back Office
has been sent
the notification
of a paper ticket
inspectoon.
]
- Decision: "See Card Payment flow." → Decision: "Back to '2.4 - Payment Area'." [Card payment failure...]
- Screen: "4.1 Present Smart Card" → Decision: "Smartcard
Readable?" [Smartcard presented.]
- Decision: "Payment card used?" → Decision: "Back to 'Sales' screen." [No]
- Screen: "3.3.1 Error" → Decision: "User chooses to issue a penalty fare and third party app opens.
A Penalty Fare ticket also prints." [User taps
'Penalty Fare'.
]
- Decision: "Accessed Waybill
when Signing Off
or in a menu?" → Screen: "11.3 Printing Waybill" [From a Menu.]
- Screen: "27 Barcode Ticket - Printed?" → Decision: "Go to 'Printing Ticket' screen." [User
taps 'No'.
]
- Decision: "Print success?" → Screen: "Print Success" [Yes]
- Decision: "Print success?" → Screen: "2.4.3.4 Transaction complete - Card" [Yes]
- Screen: "2.4.3.4 Transaction complete - Card" → Decision: "Go back to Sales screen." [3 second timeout
or user taps Tick.
]
- Screen: "8.5.1.1 Printing Receipt - Card" → Decision: "Print success?"
- Decision: "Print success?" → Screen: "2.4.3.4 Transaction complete - Card" [Yes]
- Screen: "2.4.3.1 Printing Ticket - No Header" → Decision: "Print success?"
- Screen: "2.6.5 Concessionary Card - Sales mode" → Screen: "2.6.7 Validation - Success" [User represents
correct Smartcard.
]
- Screen: "2.4.2.7 Payment/Card/Signature Okay?" → Decision: "Continue back to relevant flow." [User taps 'Yes'.]
- Screen: "2.3 Items in Basket" → Screen: "2.3.2 Basket Functionality - Delete" [User swipes left
on Basket item
]
- Screen: "2.4 Payment Area" → Screen: "2.6.2.1 - Payment - Details Swiped Down" [User taps 'Details'.
]
- Screen: "8.5.2.1 Printing Failed - Card" → Decision: "Go back to 'Mini Statement' screen." [User taps
'Cancel'.
]
- Screen: "3.2.2 Successful Validation" → Decision: "Back to 'Sales' screen." [3 second timeout or the user
taps the Tick.
]
- Screen: "4.6 Voiding Last Card Transaction" → Decision: "Go to the 'Payment Card Receipt Print' flow."
- Screen: "2.4.2.4 Payment/Card/User to Confirm Amount" → Screen: "2.4.2.5 Payment/Card/Processing Transaction"
- Screen: "2.0 Sales Screen" → Decision: "Smartcard not previously Presented & Validated?" [User presents
a smartcard.
]
- Screen: "4.2.2 Top Up - iLink - Select Product" → Screen: "2.4.0.1 Payment Area - No Warrant" [iLink product
selected.
]
- Decision: "Tries Remaining?" → Decision: "Go back to 'View Basket/Reconnecting/Status Bar/Connecting' screen." [Yes]
- Screen: "2.4.3.4 Transaction complete - Card" → Decision: "Back to 'Sales' screen or previous flow if applicable." [3 second timeout
or user taps Tick.
]
- Screen: "2.0.4 Select Alighting - List - Search Tapped - Search Entered" → Decision: "Once stage is selected, back to 'Sales' screen."
- Decision: "Over £45, customer decides
Chip & PIN, or payment device
asks customer to insert their card?" → Screen: "2.4.2.5 Payment/Card/Processing Transaction" [No - Customer
uses contactless.
]
- Screen: "2.0.9.1 Select Boarding - List - Number Entered" → Screen: "2.0.9.2 Select Boarding - List - Number Entered - Tick Pressed" [User presses
tick on keypad.
]
- Decision: "Valid top-up card?" → Screen: "8.5.1.1 Printing Receipt - Card" [Yes]
- Decision: "Following on from 'Inspection - Invalid' screen and pressing the 'Validate' button..." → Screen: "2.6 Discount - Sales mode"
- Decision: "Passed pre-validation
checks?" → Decision: "Has the Smartcard
been validated?" [Yes]
- Decision: "Smartcard
Readable?" → Decision: "Valid top-up card?" [Yes]
- Screen: "2.6.5 Concessionary Card - Sales mode" → Decision: "Go back to Sales screen." [User taps 'Cancel'
button.
]
- Screen: "2.3.2 Basket Functionality - Delete" → Screen: "2.1 Issue Ticket" [User taps
'Delete'.
]
- Screen: "8.5.1.1 Printing Receipt - Card" → Screen: "4.8 Transaction complete" [Once receipt prints...]
- Decision: "Smartcard
Readable?" → Screen: "2.5.4.1 Critical Error" [No]
- Decision: "Smartcard readable?" → Screen: "3.3 Error - Read/Write Fail" [No]
- Screen: "2.5.4.1 Critical Error" → Decision: "Back to 'Sales' screen." [User taps
'Cancel'
button.
]
- Screen: "22.3 - Sales - 3 Day Travel Chosen - First & Second Dates Chosen" → Screen: "22.4 - Sales - 3 Day Travel Chosen - Third Date Chosen" [User taps
Friday 6th.
]
- Screen: "2.4 Payment Area" → Screen: "2.4.1 Payment Area/Cash/Keyboard" [User taps
'Price' field.
]
- Screen: "2.0.13 Sales Screen - Paper Ticket Inspect - Confirmed" → Decision: "Once confirmed, banner will fade out so back to 'Sales' screen."
- Screen: "2.0 Sales Screen" → Screen: "2.8.1 Tabbed Navigation - Tickets - Edit Passengers - Rail" [User taps
'1 Adult'.
]
- Screen: "4.1.2 Critical Error - Invalid Card" → Decision: "Back to 'Represent Smartcard' screen." [User taps 'Retry' button.]
- Screen: "4.6 Voiding Last Card Transaction" → Decision: "Go to the 'Card Payment Receipt Print' flow."
- Screen: "2.4.2.6 Payment/Card/Transaction Success" → Decision: "Print a receipt for customer to sign. Print will go through same checks - if you cannot print the user will need to annul the transaction."
- Screen: "2.6.2.1 Discount - Summary - Rail" → Decision: "Go back to Sales screen." [User taps
'Clear Basket'
button.
]
- Screen: "2.0.9 Select Boarding - List - Numerical Search" → Screen: "2.0.9.1 Select Boarding - List - Number Entered" [User inputs
a number.
]
- Screen: "3.2 Inspection - Invalid" → Decision: "Card Type?" [User taps 'Validate'.]
- Screen: "7.1 Transaction complete" → Decision: "Back to relevant menu."
- Screen: "2.5.4.1 Critical Error" → Decision: "Back to 'Present Smartcard' screen." [User taps
'Retry'
button.
]
- Screen: "2.6.5.1 Concessionary Card - Sales mode - Rail" → Screen: "2.6.1.1 - Concession - Sales mode - Select Product" [User taps 'Single'
to select
a ticket type.
]
- Screen: "2.6.7 Validation - Success" → Decision: "Back to 'Sales' screen."
- Screen: "2.4 Payment Area" → Decision: "See Card Payment flow." [User taps 'Card'.]
- Decision: "Print Success?" → Screen: "11.4 Printing Failed" [No]
- Screen: "2.4.3 Printing Ticket" → Decision: "Print Success?"
- Decision: "Go to Penalty Warning print flow." → Decision: "Back to Sales screen." [Once the Print
flow is complete...
]
- Decision: "Smartcard Valid?" → Screen: "3.2.3 Smartcard Not Valid - No Travel Remaining" [No - No travel
remaining.
]
- Decision: "Smartcard
Readable?" → Screen: "3.3 Error - Read/Write Fail" [No]
- Decision: "User chooses to issue a penalty fare and third party app opens.
A Penalty Fare ticket also prints." → Decision: "Back to 'Sales' screen."
- Screen: "2.6.2.1 - Payment - Details Swiped Down" → Decision: "Back to 'Payment Area' screen." [User taps 'Details'.]
- Screen: "2.0 Sales Screen" → Screen: "2.0.9 Select Boarding - List - Numerical Search" [User taps a
Boarding Number
]
- Screen: "2.4.3.1 Transaction complete" → Screen: "3.2.2 Successful Validation" [3 second
timeout...
]
- Screen: "2.4.2.2 Payment/Card/Initialising Transaction" → Screen: "2.4.2 Payment/Card/User to Present Card"
- Decision: "Transaction Success?" → Screen: "2.4.2.8 Payment/Card/Declined" [No]
- Screen: "2.0.9.2 Select Boarding - List - Number Entered - Tick Pressed" → Decision: "Once stage is selected, back to 'Sales' screen."
- Screen: "2.0 Sales Screen" → Decision: "Smartcard not previously Presented & Validated?" [User presents
a smartcard.
]
- Screen: "4.1.1 Critical Error - Incorrect Card" → Decision: "Back to 'Sales' screen." [User taps
'Cancel' button.
]
- Screen: "2.0.2 Select Alighting - List - HHD Screen Size" → Screen: "2.0.3 Select Alighting - List - Search Tapped" [User taps a
Search bar.
]
- Screen: "2.1.3 Issue Advanced Ticket" → Screen: "2.1.4 Issue Advanced Ticket - Are you sure?" [User taps 'Add
More to Basket'.
]
- Decision: "Customer Attempting
PIN Entry" → Screen: "2.4.2.5 Payment/Card/Processing Transaction" [PIN Entry success]
- Decision: "Print Success?" → Screen: "7.1 Transaction complete" [Yes]
- Screen: "2.4.2.6 Payment/Card/Transaction Success" → Decision: "Continue back to relevant flow."
- Screen: "7.2 Print Failed" → Decision: "Go to 'Login' flow." [User taps
'Continue Without Printing'.
]
- Screen: "7.2 Print Failed" → Decision: "Go to 'Printing Waybill' screen." [User taps
'Retry'.
]
- Screen: "7.2.1 Print Failed Card Payment" → Decision: "Back to 'Printing Receipt' screen." [User taps
'Retry'.
]
- Screen: "7.2.1 Print Failed Card Payment" → Decision: "Go back to Sales screen." [User taps
'Continue Without
Printing'.
]
- Screen: "2.0 Sales Screen" → Screen: "2.8.2 Tabbed Navigation - Tickets - Edit Passengers Glider" [User taps
'1 Adult'.]
- Screen: "2.8.2 Tabbed Navigation - Tickets - Edit Passengers Glider" → Screen: "2.8.2.2 Tabbed Navigation - Tickets - Edit Passengers - 1 Selected Glider" [User taps '-' on Adult
and '+' on Child]
- Screen: "2.8.2.2 Tabbed Navigation - Tickets - Edit Passengers - 1 Selected Glider" → Screen: "22.5 - Sales - Child Selected Glider" [User taps
'Confirm'
button.]
- Screen: "2.1.3 Issue Advanced Ticket" → Screen: "2.1.5 Issue Advanced Ticket - Are you sure?" [User attempts to
duplicate a product.]
- Screen: "2.1.3 Issue Advanced Ticket" → Screen: "2.1.6 Issue Advanced Ticket - Are you sure?" [User attempts to
edit a product.]
- Screen: "2.4.3.2.1 Print Failed - Card" → Decision: "Go to Annulment flow seen in 'Driver Menu Functionality'."
- Screen: "2.6 Discount - Sales mode" → Screen: "2.6.0.1 Discount - Sales mode - Alighting Selected" [User selects an 
Alighting Stage.]
- Screen: "4.6 Voiding Last Card Transaction" → Decision: "Go to the 'Receipt Print' flow."
- Screen: "2.4.3.4 Transaction complete - Card" → Screen: "2.4.3.3 Printing Ticket - Card"
- Screen: "7.2 Print Failed" → Decision: "Go back to Sales screen."
- Screen: "7.2 Print Failed" → Decision: "Back to 'Printing Receipt' screen."
- Screen: "2.4.3.1 Printing Ticket - No Header" → Decision: "Print success?"
- Screen: "7.1 Transaction complete" → Decision: "Back to 'Sales' screen."
- Screen: "2.4.2.3 Payment/Card/PIN Entry" → Decision: "Customer Attempting
PIN Entry"
- Decision: "Over £45, customer decides
Chip & PIN, or payment device
asks customer to insert their card?" → Decision: "Go Back to 'User to Present Card' then follow Chip & PIN Flow." [Yes]
- Screen: "2.4.2.4 Payment/Card/User to Confirm Amount" → Screen: "2.4.2.5 Payment/Card/Processing Transaction"
- Decision: "Print success?" → Screen: "2.4.3.4 Transaction complete - Card" [Yes]
- Screen: "8.5.1.1 Printing Receipt - Card" → Decision: "Print success?"
- Screen: "2.4.3.4 Transaction complete - Card" → Decision: "Back to 'Sales' screen or previous flow if applicable." [3 second timeout
or user taps Tick.
]
- Screen: "7.2 Print Failed" → Decision: "Back to 'Printing Receipt' screen." [User taps
'Retry'.
]
- Screen: "7.2 Print Failed" → Decision: "Go back to Sales screen." [User taps
'Continue Without
Printing'.
]
- Decision: "Print success?" → Screen: "7.2 Print Failed" [No]
- Decision: "Print success?" → Screen: "2.4.3.2.1 Print Failed - Card" [No]
- Decision: "Smartcard Already Presented & Validated previously?" → Screen: "2.5.4.2 Error - Passback" [Yes]
- Decision: "Smartcard Already Presented & Validated previously?" → Decision: "Passed pre-validation
checks?" [No - this card has not been
presented previously.
]
- Screen: "2.5.4.2 Error - Passback" → Decision: "Back to 'Sales' screen."
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Top Up Receipt Print' flow." [User taps
'Faulty Smartpass'.]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Card validation success?' check above." [User taps 'Retry'.]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Top Up Receipt Print' flow." [User taps
'Faulty Smartpass'.]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Smartcard Readable?' check above." [User taps 'Retry'.]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Back to Sales screen." [User taps
'Retry'.]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Top Up Receipt Print' flow." [User taps 'Faulty Smartpass'.]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Smartcard Readable?' check above." [User taps 'Retry'.]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Top Up Receipt Print' flow." [User taps 'Free Smartpass'.]
- Screen: "7.2 Print Failed" → Screen: "3.2.2 Successful Validation" [User taps
'Continue Without
Printing' button.
]
- Screen: "2.6.1.1 - Concession - Sales mode - Select Product" → Screen: "2.6.5.2 Concessionary Card - Sales mode - Rail - Return Chosen" [User taps
'Return'.]
- Screen: "2.4.1.1 Payment Area/Cash/Keyboard/Specific Amount" → Decision: "Go to relevant 'Cash / Payment Card Print Flow' flow." [User taps a payment option...]
- Screen: "2.4.0.1 Payment Area - No Warrant" → Decision: "See Card Payment flow." [User chooses 'Card' option]
- Screen: "3.2.2 Successful Validation" → Screen: "2.6.7 Validation - Success"
- Screen: "2.8.1 Tabbed Navigation - Tickets - Edit Passengers - Rail" → Screen: "22.5 - Sales - Family & Friends Selected" [User taps on 'Family']
- Screen: "22.5 - Sales - Family & Friends Selected" → Screen: "22.6 - Sales - Select Product - Rail" [User taps
'Family & Friends'.]
- Decision: "Back to 'Sales'  with Three-Day Product selected and price displayed. From here it can be added to the basket." → Screen: "2.3.0.1 Items in Basket - 3 Dates" [Item added to Basket...]
- Screen: "4.1.3 Critical Error - Invalid Card - Generic Error" → Decision: "Go to 'Concessionary Card - Sales mode' screen." [User taps
'Retry' button.
]
- Screen: "4.1.3 Critical Error - Invalid Card - Generic Error" → Decision: "Go back to Sales screen." [User taps
'Cancel' button.
]
- Decision: "Valid Smartcard?" → Screen: "2.6.5.1 Concessionary Card - Sales mode - Rail" [Yes]
- Decision: "Valid Smartcard?" → Screen: "4.1.3 Critical Error - Invalid Card - Generic Error" [No, error]
- Screen: "4.1.3 Critical Error - Invalid Card - Generic Error" → Decision: "Go to 'Sales mode' screen." [User taps
'Retry' button.
]
- Screen: "4.1.3 Critical Error - Invalid Card - Generic Error" → Decision: "Go back to Sales screen." [User taps
'Cancel' button.
]
- Decision: "Valid Smartcard?" → Screen: "4.1.3 Critical Error - Invalid Card - Generic Error" [No, error]
- Decision: "Smartcard not previously Presented & Validated?" → Decision: "Valid Smartcard?" [Yes]
- Screen: "2.5 View Basket/Reconnect Card Reader" → Screen: "2.5.3.1 View Basket/Reconnecting/Status Bar/Not Connected/Contact Supervisor" [User taps 'Card' button.]
- Decision: "Go to 'Top Up Receipt Print' flow." → Decision: "Back to Sales screen." [Once Print flow is complete...]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Top Up Receipt Print' flow." [User taps
'Faulty Smartpass'.]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Card validation success?' check above." [User taps 'Retry'.]
- Decision: "Valid Smartcard?" → Screen: "3.3 Error - Read/Write Fail" [Read/Write Error]
- Decision: "Go to 'Top Up Receipt Print' flow." → Decision: "Back to Sales screen." [Once Print flow is complete...]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Top Up Receipt Print' flow." [User taps
'Faulty Smartpass'.]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Card validation success?' check above." [User taps 'Retry'.]
- Decision: "Valid Smartcard?" → Screen: "3.3 Error - Read/Write Fail" [Read/Write Error]
- Decision: "Go to 'Top Up Receipt Print' flow." → Decision: "Back to Sales screen." [Once Print flow is complete...]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Top Up Receipt Print' flow." [User taps
'Faulty Smartpass'.]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Card validation success?' check above." [User taps 'Retry'.]
- Screen: "2.6.5 Concessionary Card - Sales mode" → Screen: "3.3 Error - Read/Write Fail" [Read/Write Error]
- Decision: "Go to 'Top Up Receipt Print' flow." → Decision: "Back to Sales screen." [Once Print flow is complete...]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Top Up Receipt Print' flow." [User taps
'Faulty Smartpass'.]
- Screen: "3.3 Error - Read/Write Fail" → Decision: "Go to 'Card validation success?' check above." [User taps 'Retry'.]
- Screen: "4.4 Represent Smartcard" → Screen: "3.3 Error - Read/Write Fail" [Read/Write Error
]
- Screen: "2.4.3.2 Print Failed" → Decision: "Go to Annulment flow seen in  'Driver Menu Functionality'." [User taps
'Annul Transaction'.
]
- Screen: "2.4.3.2.1 Print Failed - Card" → Decision: "Go to Annulment flow seen in 'Driver Menu Functionality'."
