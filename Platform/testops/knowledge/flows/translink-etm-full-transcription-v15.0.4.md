# ETM-TFTS-V15.0.4 — Translink ETM UX — Full Flow Transcription

Source: Overflow.io project "ETM-TFTS-V15.0.4" (https://overflow.io/s/NDLGF6NF/)
Extracted: full text content of all boards — screen titles, decision points, annotations/spec notes, and screen-to-screen connections.
Note: This document captures TEXT content and FLOW STRUCTURE only. It does not include the actual visual mockup images (screens are referenced by their title/ID only).

## Board Index (main navigation order)
1. Title Board
2. Board 1
3. Startup
4. Driver Sign On
5. FLU
6. FLU 2.0 Navigation
7. FLU - Basket Mode
8. Driver Menu / Options
9. Supervisor
10. Technician
11. Displays LEDs and Audio Tones
12. Barcode Scanning
13. Power Interruption
14. Revenue Limit

---


## 1. Title Board

### Screens (0)

### Decision Points (0)

### Annotations / Spec Notes (1)
- ETM UX

### Connections / Flow (0)


## 2. Board 1

### Screens (2)
- 02.6 | EMV Validated
- 02.6.1 | EMV Validation Failure

### Decision Points (0)

### Annotations / Spec Notes (0)

### Connections / Flow (0)


## 3. Startup

### Screens (5)
- 0.0.0 - Screen Off
- 0.1.0.1 - Splash Screen
- 01.0.0 - Idle Screen
- 11.2.0 - Charging
- 01.0.2 - Device not Commissioned

### Decision Points (4)
- Software starts in less than 2 minutes?
- Device is commissioned?
- ETM is powered
- Back to the FLU screen

### Annotations / Spec Notes (5)
- Startup
- .
- The device may cycle through various BIOS/OS loading/maintenance screens immediately after powering but then shoudl settle ont he Software startup Splashscreen.
- ==================
- This screen appears on boot to ensure the device has enough charge to successfully allow the state to be saved in the event of a power interruption.

### Connections / Flow (7)
- Screen: "0.0.0 - Screen Off" → Decision: "ETM is powered"
- Decision: "ETM is powered" → Screen: "0.1.0.1 - Splash Screen"
- Screen: "0.1.0.1 - Splash Screen" → Decision: "Software starts in less than 2 minutes?"
- Decision: "Software starts in less than 2 minutes?" → Screen: "11.2.0 - Charging"
- Decision: "Software starts in less than 2 minutes?" → Decision: "Device is commissioned?"
- Screen: "11.2.0 - Charging" → Decision: "Device is commissioned?"
- Decision: "Device is commissioned?" → Screen: "01.0.2 - Device not Commissioned"


## 4. Driver Sign On

### Screens (37)
- 01.9 - Please Wait...
- 01.0.0 - Idle Screen
- 01.4.2 - Type Route - With Letters - Hiddent - 10 Typed
- 01.1.6 - Sign Off
- 01.0.0.1 - Idle Screen - Bad Comms
- 01.0.1 - Communications Locked
- 01.4.0 - Type Route - With Letters - Hidden
- 01.1.0 - Sign On - Empty Fields
- 01.1.1 - Sign On - ID Entered
- 01.1.2 - Sign On - PIN Entry
- 01.1.3 - Sign On - PIN Entry - 4*
- 01.1.5 - Sign On - Device Locked
- 01.1.4 - Sign On - Incorrect Details
- 01.2.1 - Sign on Details Entered - First Use Safety Check On Board
- 01.2.0 - Sign On Details Entered - First Use Safety Check
- 01.2.3 - Sign on Details Entered - Bus Check - Any Defects
- 01.2.2 - Sign on Details Entered - There Must be a First Use Safety Check
- 01.3.0 - Select Duty
- 01.3.1 - Select Duty - 4 Typed
- 01.3.2 - Select Duty - Incorrect
- 01.5.0 - Journey Selection
- 01.4.1 - Type Route - With Letters - Shown
- 01.4.3 - Type Route - With Number
- 01.4.3.1 - Type Route - With Number - Selected
- 01.4.6 - Type Route - Incorrect
- 01.4.4 - Type Route - With Number - Inbound Filtered
- 01.4.5 - Type Route - With Number - Outbound Filtered
- 01.5.1 - Journey Number
- 01.5.2 - Journey Number - 4 Typed
- 01.5.3 - Journey Number - Incorrect
- 01.6.0 - Route Summary
- 01.7.1 - Message of the Day - Unavailable
- 01.7.0 - Message of the Day
- 01.8.1 - Word and Colour of the Day - Unavailable
- 01.8.0 - Word and Colour of the Day - Simpler UI
- 01.9 - Please Wait...
- 02.0.0 | FLU Home

### Decision Points (28)
- Go back to: 01.0.0 - Idle Screen If a Duty number has been entered a way bill will be printed.
- Go back to previous screen
- Incorrect details entered more  than 3 times?
- Correct Login Details?
- Go to: '10.0.0 - Technician Menu'
- Is the Staff ID for a Driver?
- Go to the Supervisor Menu Flow
- Go to: '11.0.0 - Supervisor Menu'
- On screen timeout (3 seconds)
- Was sign-on  initiated  with smartcard?
- Go back to: 01.1.0 - Sign On - Empty Fields
- Go back to: 01.1.2 - Sign On - PIN Entry
- First Sign On of the day?
- Scheduling?
- Duty Number correct?
- Go to: 01.4.1 - Type Route - With Letters - Shown
- Go back to: 01.3.1 - Select Duty - 4 Typed
- Go back to: '01.3.0 - Select Duty'
- Go back to: '01.1.6 - Sign Off'
- Does this Route Exist?
- Does the Journey Number  match a valid 24hr time format? (Eg, 2115)
- Go back to: 01.5.1 - Journey Number
- Scheduling?
- Go back to: 01.5.0 - Journey Selection
- Message of the day Available?
- Words & Colours of the Day available?
- Go back to: '01.7.0 - Message of the Day'
- Go back to: '01.7.0 - Message of the Day'

### Annotations / Spec Notes (21)
- Driver Sign On
- Throughout the Driver Sign-On flow the following is true, unless otherwise stated: - If no button is pressed, there is a timeout of 30 seconds after which the ETM will return to Idle Screen. If the Driver is signed in, they will be signed out. - Pressing the 'C' key will take a user back one screen. - Pressing the 'P' key takes the user to the '1.1.6 - Sign Off?' screen.  - If you sign off after Duty Selection, a Waybill will be printed.
- Archived
- Abandon Sign On
- Idle Mode
- Communications are locked on the device if it has not communicated with CloudFare after x amount of hours.
- Sign On
- Pressing 'C' clears one character at a time
- Pressing 'C' clears one character at a time.  If all characters are cleared, go back to '01.1.1 - Sign On - ID Entered' screen. However the user cannot amend an ID if using a smartcard, so 'C' would go back to '01.0.0 - Idle Screen'
- Safety Check
- Duty Number entry
- Pressing 'C' clears one character at a time
- Scheduling/Route Selection
- The closest future journey to the current time is suggested to the driver. If they press the 'Enter' key they will progress to the next step. Pressing the 'C' key will take the driver back to the 'Select Duty' screen.
- If no journeys are available, or if the correct journey isn't available, the user can manually override scheduling and input a specific route number.  The 'Manual Override' key will take the user to the Route Selection screen.  The up and down arrows will allow the user to view more Journeys.
- Pressing L1-6 or R1-6 keys allows the user to input a letter into the Route Code field.  Users can navigate to the next set of letters using the up and down keys.   Pressing 'C' (on the physical buttons) clears the input field one letter at a time. Or, if the input field is empty, pressing 'C' will go to the '01.1.6 - Sign off' prompt screen.
- The up and down arrows will allow the user to view more Routes
- Pressing 'C' clears one character at a time
- Word, Colour and Messages of the day
- There will be a timeout of 5 seconds  to see if the Message of the Day can  be retrieved.
- There will be a timeout of 5 seconds  to see if the Words and Colours of the  Day can be retrieved.

### Connections / Flow (92)
- Screen: "01.0.0 - Idle Screen" → Screen: "01.1.0 - Sign On - Empty Fields" [User presses the 'Enter' key.]
- Screen: "01.1.0 - Sign On - Empty Fields" → Screen: "01.1.1 - Sign On - ID Entered" [User inputs ID using Numerical pad.]
- Screen: "01.1.1 - Sign On - ID Entered" → Screen: "01.1.2 - Sign On - PIN Entry" [User press 'Enter' key to advance.]
- Screen: "01.1.2 - Sign On - PIN Entry" → Screen: "01.1.3 - Sign On - PIN Entry - 4*" [User inputs PIN using numberpad]
- Screen: "01.0.0 - Idle Screen" → Screen: "01.1.2 - Sign On - PIN Entry" [User presents a valid smartcard.]
- Screen: "01.1.3 - Sign On - PIN Entry - 4*" → Decision: "Correct Login Details?" [User presses 'Enter' key.]
- Decision: "Correct Login Details?" → Decision: "Incorrect details entered more
 than 3 times?" [No]
- Decision: "Incorrect details entered more
 than 3 times?" → Screen: "01.1.5 - Sign On - Device Locked" [Yes]
- Decision: "Incorrect details entered more
 than 3 times?" → Screen: "01.1.4 - Sign On - Incorrect Details" [No]
- Screen: "01.1.4 - Sign On - Incorrect Details" → Screen: "01.0.0 - Idle Screen"
- Screen: "01.1.4 - Sign On - Incorrect Details" → Decision: "On screen timeout
(3 seconds)"
- Decision: "On screen timeout
(3 seconds)" → Decision: "Was sign-on  initiated 
with smartcard?"
- Decision: "Was sign-on  initiated 
with smartcard?" → Decision: "Go back to:
01.1.0 - Sign On - Empty Fields" [No
]
- Decision: "Was sign-on  initiated 
with smartcard?" → Decision: "Go back to:
01.1.2 - Sign On - PIN Entry" [Yes]
- Decision: "Go back to:
01.1.0 - Sign On - Empty Fields" → Screen: "01.1.0 - Sign On - Empty Fields"
- Decision: "Correct Login Details?" → Decision: "Is the Staff ID for a Driver?" [Yes]
- Decision: "First Sign On of the day?" → Screen: "01.2.1 - Sign on Details Entered - First Use Safety Check On Board" [No
]
- Decision: "First Sign On of the day?" → Screen: "01.2.0 - Sign On Details Entered - First Use Safety Check" [Yes]
- Screen: "01.2.0 - Sign On Details Entered - First Use Safety Check" → Screen: "01.2.1 - Sign on Details Entered - First Use Safety Check On Board" [User presses 'No' key.]
- Screen: "01.2.1 - Sign on Details Entered - First Use Safety Check On Board" → Screen: "01.2.2 - Sign on Details Entered - There Must be a First Use Safety Check" [User presses 'No' key.]
- Screen: "01.2.0 - Sign On Details Entered - First Use Safety Check" → Screen: "01.2.3 - Sign on Details Entered - Bus Check - Any Defects" [User presses 'Yes' key.]
- Screen: "01.2.2 - Sign on Details Entered - There Must be a First Use Safety Check" → Screen: "01.3.0 - Select Duty" [User presses 'Continue' key.]
- Screen: "01.2.1 - Sign on Details Entered - First Use Safety Check On Board" → Screen: "01.3.0 - Select Duty" [User press Yes' key.]
- Screen: "01.2.3 - Sign on Details Entered - Bus Check - Any Defects" → Screen: "01.3.0 - Select Duty" [User presses 'Yes' key.]
- Screen: "01.2.3 - Sign on Details Entered - Bus Check - Any Defects" → Screen: "01.3.0 - Select Duty" [User presses 'No' key.]
- Screen: "01.3.0 - Select Duty" → Screen: "01.3.1 - Select Duty - 4 Typed" [User Inputs a Duty Number
using the numerical keypad.]
- Screen: "01.3.1 - Select Duty - 4 Typed" → Decision: "Scheduling?" [User presses the 'Enter' key.]
- Decision: "Scheduling?" → Screen: "01.4.1 - Type Route - With Letters - Shown" [No]
- Decision: "Scheduling?" → Decision: "Duty Number correct?" [Yes
]
- Decision: "Duty Number correct?" → Screen: "01.3.2 - Select Duty - Incorrect" [No]
- Decision: "Duty Number correct?" → Screen: "01.5.0 - Journey Selection" [Yes]
- Screen: "01.4.1 - Type Route - With Letters - Shown" → Decision: "Does this Route Exist?" [User enters numbers 
and letters and presses 
the 'Enter' key.]
- Decision: "Does this Route Exist?" → Screen: "01.4.6 - Type Route - Incorrect" [No]
- Decision: "Does this Route Exist?" → Screen: "01.4.3 - Type Route - With Number" [Yes]
- Screen: "01.4.6 - Type Route - Incorrect" → Screen: "01.4.1 - Type Route - With Letters - Shown" [User presses 'C' key to go back.]
- Screen: "01.4.6 - Type Route - Incorrect" → Screen: "01.4.1 - Type Route - With Letters - Shown" [If no button is pressed, timeout is 3 seconds]
- Screen: "01.4.3 - Type Route - With Number" → Screen: "01.4.4 - Type Route - With Number - Inbound Filtered" [Pressing R6 toggles to 
Inbound only routes.]
- Screen: "01.4.4 - Type Route - With Number - Inbound Filtered" → Screen: "01.4.5 - Type Route - With Number - Outbound Filtered" [Pressing R6 again toggles
to Outbound only routes.]
- Screen: "01.4.5 - Type Route - With Number - Outbound Filtered" → Screen: "01.4.3 - Type Route - With Number" [Pressing R6 again toggles
to display both Inbound and 
Outbound routes.]
- Screen: "01.4.3 - Type Route - With Number" → Screen: "01.4.3.1 - Type Route - With Number - Selected" [User presses R2 to select a route.]
- Screen: "01.4.3.1 - Type Route - With Number - Selected" → Screen: "01.5.1 - Journey Number" [User presses 'Enter' key.]
- Screen: "01.5.1 - Journey Number" → Screen: "01.5.2 - Journey Number - 4 Typed" [User inputs a Journey Number
using the numerical keypad]
- Screen: "01.5.1 - Journey Number" → Decision: "Does the Journey Number 
match a valid 24hr time format?
(Eg, 2115)"
- Screen: "01.5.2 - Journey Number - 4 Typed" → Decision: "Does the Journey Number 
match a valid 24hr time format?
(Eg, 2115)" [User presses the 'Enter' key]
- Decision: "Does the Journey Number 
match a valid 24hr time format?
(Eg, 2115)" → Screen: "01.5.3 - Journey Number - Incorrect" [No]
- Decision: "Does the Journey Number 
match a valid 24hr time format?
(Eg, 2115)" → Screen: "01.6.0 - Route Summary" [Yes]
- Screen: "01.6.0 - Route Summary" → Decision: "Scheduling?" [User presses the 'C' key.]
- Screen: "01.6.0 - Route Summary" → Decision: "Message of the day Available?" [User presses 'Enter' key.]
- Decision: "Message of the day Available?" → Screen: "01.7.1 - Message of the Day - Unavailable" [No]
- Decision: "Message of the day Available?" → Screen: "01.7.0 - Message of the Day" [Yes]
- Decision: "Words & Colours of the Day
available?" → Screen: "01.8.1 - Word and Colour of the Day - Unavailable" [No]
- Decision: "Words & Colours of the Day
available?" → Screen: "01.8.0 - Word and Colour of the Day - Simpler UI" [Yes]
- Screen: "01.7.1 - Message of the Day - Unavailable" → Decision: "Words & Colours of the Day
available?" [User presses 'Enter' key.]
- Screen: "01.7.0 - Message of the Day" → Decision: "Words & Colours of the Day
available?"
- Screen: "01.8.1 - Word and Colour of the Day - Unavailable" → Screen: "01.9 - Please Wait..." [User press 'Enter' key.]
- Screen: "01.8.0 - Word and Colour of the Day - Simpler UI" → Screen: "01.9 - Please Wait..."
- Screen: "01.0.0 - Idle Screen" → Screen: "01.0.0.1 - Idle Screen - Bad Comms" [Comms Fails]
- Screen: "01.0.0.1 - Idle Screen - Bad Comms" → Screen: "01.0.0 - Idle Screen" [Comms is restored]
- Screen: "01.0.0.1 - Idle Screen - Bad Comms" → Screen: "01.0.1 - Communications Locked" [Comms Failure persists]
- Screen: "01.0.1 - Communications Locked" → Screen: "01.0.0 - Idle Screen"
- Screen: "01.1.6 - Sign Off" → Decision: "Go back to:
01.0.0 - Idle Screen
If a Duty number has been entered a way bill will be printed." [User presses Enter' key.]
- Screen: "01.1.6 - Sign Off" → Decision: "Go back to previous screen" [User presses 'Cancel' key.]
- Screen: "01.1.5 - Sign On - Device Locked" → Decision: "Go to the Supervisor Menu Flow" [Supervisor presents smartcard to unlock ETM.]
- Screen: "01.1.0 - Sign On - Empty Fields" → Screen: "01.0.0 - Idle Screen"
- Screen: "01.1.1 - Sign On - ID Entered" → Screen: "01.1.0 - Sign On - Empty Fields" [User presses 'C' when all characters have been removed]
- Screen: "01.1.2 - Sign On - PIN Entry" → Screen: "01.1.1 - Sign On - ID Entered"
- Decision: "Scheduling?" → Screen: "01.4.1 - Type Route - With Letters - Shown" [No]
- Decision: "Scheduling?" → Decision: "Go back to:
01.5.0 - Journey Selection" [Yes]
- Screen: "01.9 - Please Wait..." → Screen: "02.0.0 | FLU Home"
- Decision: "Go back to:
01.0.0 - Idle Screen
If a Duty number has been entered a way bill will be printed." → Screen: "01.0.0 - Idle Screen"
- Screen: "01.1.6 - Sign Off" → Decision: "Go back to previous screen" [User presses 'C' key.]
- Decision: "Is the Staff ID for a Driver?" → Decision: "First Sign On of the day?" [Yes]
- Decision: "Is the Staff ID for a Driver?" → Decision: "Go to:
'10.0.0 - Technician Menu'" [No Technician]
- Decision: "Is the Staff ID for a Driver?" → Decision: "Go to:
'11.0.0 - Supervisor Menu'" [No Supervisor]
- Screen: "01.2.2 - Sign on Details Entered - There Must be a First Use Safety Check" → Screen: "01.2.1 - Sign on Details Entered - First Use Safety Check On Board" [User presses 'Go Back' key.]
- Screen: "01.3.2 - Select Duty - Incorrect" → Decision: "Go back to:
'01.3.0 - Select Duty'" [User presses 'C' key.]
- Screen: "01.3.2 - Select Duty - Incorrect" → Decision: "Go back to:
'01.3.0 - Select Duty'" [If no button is pressed, 
timeout is 3 seconds]
- Screen: "01.5.0 - Journey Selection" → Screen: "01.6.0 - Route Summary" [User presses 'Enter' key.]
- Screen: "01.5.0 - Journey Selection" → Decision: "Go back to:
01.3.1 - Select Duty - 4 Typed" [User presses 'C' key.]
- Screen: "01.5.0 - Journey Selection" → Decision: "Go to:
01.4.1 - Type Route - With Letters - Shown" [User presses 'Manual Override' key.]
- Screen: "01.4.1 - Type Route - With Letters - Shown" → Decision: "Go back to:
'01.1.6 - Sign Off'" [User presses 'C' when no text is in the field.]
- Screen: "01.3.1 - Select Duty - 4 Typed" → Screen: "01.2.0 - Sign On Details Entered - First Use Safety Check" [User presses 'C' key 
when 'Duty Number' field is empty.]
- Screen: "01.3.0 - Select Duty" → Screen: "01.2.0 - Sign On Details Entered - First Use Safety Check"
- Screen: "01.5.1 - Journey Number" → Screen: "01.4.3 - Type Route - With Number" [User presses 'C' key]
- Screen: "01.5.3 - Journey Number - Incorrect" → Decision: "Go back to:
01.5.1 - Journey Number" [User presses 'C' key.]
- Screen: "01.5.3 - Journey Number - Incorrect" → Decision: "Go back to:
01.5.1 - Journey Number" [If no button is pressed, 
timeout is 3 seconds]
- Screen: "01.7.1 - Message of the Day - Unavailable" → Decision: "Words & Colours of the Day
available?" [On page timeout
(10 seconds)]
- Screen: "01.7.0 - Message of the Day" → Decision: "Words & Colours of the Day
available?" [On page timeout
(10 seconds)]
- Screen: "01.8.1 - Word and Colour of the Day - Unavailable" → Screen: "01.9 - Please Wait..." [On page timeout
(10 seconds)]
- Screen: "01.8.0 - Word and Colour of the Day - Simpler UI" → Screen: "01.9 - Please Wait..." [On page timeout
(10 seconds)]
- Screen: "01.8.0 - Word and Colour of the Day - Simpler UI" → Decision: "Go back to:
'01.7.0 - Message of the Day'" [User presses 'C' key.]
- Screen: "01.8.1 - Word and Colour of the Day - Unavailable" → Decision: "Go back to:
'01.7.0 - Message of the Day'" [User presses 'C' key.]


## 5. FLU

### Screens (80)
- 02.0.0 | FLU Home
- 02.0.0 | FLU Home
- 05.0.0 - Hotlisted Error
- 02.0.2 | Main Screen - FLU - Change Boarding Stage
- 02.0.3 | FLU - Alighting Stages 06-09
- 02.0.1 | Product Page Example
- 02.0.4 | FLU - Fare-Based - Journeys
- 05.0.1 - FLU - Smartcard Top Up - No Journeys Left Error
- 02.0.3.1 | FLU - Alighting Stages 23 _ 24
- 02.0.4.1 | FLU - Fav Journeys
- 05.0.2 - FLU - DayLink Tap on - Success
- 02.0.4.2 FLU - Transfer Journeys
- 05.0.3 - FLU - Smartcard Already Validated
- 02.0.0 | FLU Home
- 02.1.0 | Toggle Group - Group
- 02.2 | Preset Product
- 02.3 | Menu Type
- 02.4 | FLU Product
- 02.0.0 | FLU Home
- 02.1.1 | Toggle Groups - List
- 02.3.1 | Menu Type - Product Selected
- 02.4.1 | FLU Product - Alighting Stage Selected
- 06.0.0 - Present Smartcard
- 02.1.2 Toggle Group - Flu Product Selected from Menu
- 06.0.1 - FLU - Smart Card - Menu
- 02.1.3 Flu Product Selected - Alighting Stage Selected
- 02.0.5 | Easibus
- 06.0.1.3 - FLU - Smartcard Top Up - Error - Remove Smartcard
- 06.0.1.1 - FLU - Smart Card - Mini Statement
- 06.0.1.2 - FLU - Smart Card - Top Up
- 06.0.1.4 - FLU - Smartcard - Outside Time Band
- 06.0.1.2.1 - FLU - Smart Card - Top Up - Payment
- 06.0.10.0 - FLU - ABT Presented
- 06.0.10.1 - FLU Product - Alighting Stage selected - ABT
- 06.0.1.2.3 - FLU - Smartcard - Top Up - Error
- 06.0.1.2.2 - FLU - Smartcard - Top Up - Confirmation
- 02.6.5 | EMV Validation Failure - Card already validated
- 06.1.0.0 | Pass Success
- 02.6 | EMV Validated
- 06.0.2.0 -  FLU - Smartcard - Faulty - Select Card Type
- 02.6.1 | EMV Validation Failure
- 06.0.3.0 -  FLU - Smartcard - Faulty - Charge Full Fare
- 06.0.4.0 -  FLU - Smartcard - Faulty - Issue Ticket
- 02.6.2 | EMV Validation Failure - Tap Error
- 02.6.3 | EMV Validation Failure - Card has Expired
- 02.6.4 | EMV Validation Failure - Card has been declined
- 2.5 | Main Screen - Last Transaction 200 - Success
- 2.5.2 | Main Screen - Last Transaction - Multiple Tickets in Basket - Success
- 2.5.1 | Main Screen - Last Transaction 200
- 07.0.0 - Printer Error

- 07.0.2 - Main Screen - FLU - Paper Low
- 07.0.6 -Main Screen - Travel Mode
- 07.0.6.2 - Main Screen - Travel Mode - Schedule Adherence - In Set Times
- 07.0.6.1 - Main Screen - Travel Mode - Schedule Adherence - Outside Set Times
- 07.0.1 - Printer Error - Paper Jam
- 07.0.3 - Out of Service Error
- 07.0.4 | Main Screen - Currency is Euro
- 02.0.0 | FLU Home
- 03.0.1.3 | Promo Menu Product Selected
- 03.0 | Promo Menu
- 03.0.1 | Promo Menu - Basket Mode
- 03.0.1.1 - Promo Menu - Ticket Purchased
- 03.0.2.2 | Promo Menu  - P&R Menu
- 06.0.5.0 -  Main Screen - FLU - yLink
- 06.0.6.0 -  Main Screen - FLU - Free Product
- 03.0.3 | Promo Menu - Basket Mode - Ticket Selected
- 03.0.2.1 | Promo Menu - Basket Mode - P&R Menu
- 03.0.1.2 - Promo Menu - Updated Last
- 06.0.7.0 -  Main Screen - FLU - Free Product - Notification
- 06.0.5.1 - FLU Product - Alighting Stage selected - yLink
- 03.0.2 | Promo Menu - Basket Mode - Ticket in Basket
- 06.1.0.0 | Pass Success
- 06.0.5.3 - FLU Product - Alighting Stage selected - yLink - Basket - Added
- 02.0.0 | FLU Home
- 04.0 | Numeric Entry - 9 - Change & Alighting
- 04.0.1 | Numeric Entry - 9017 - Change & Alighting
- 04.1 | FLU - Group Ticket - Payment
- 04.0.1.3 | Main Screen - FLU - 9017 Alighting Stage Chosen
- 04.0.1.1 | Numeric Entry - 500 - Change Calculated
- 04.0.1.2 | Numeric Entry - 9017 - Change & Alighting - Error Bar

### Decision Points (33)
- Is it a valid card?
- 'Numeric Input' Flow
- 'Basket Mode' Flow
- Has the card already been tapped today?
- Is there at least one day available on the card?
- Has this card already been tapped on this bus in the last x minutes?
- 02.0.0 Main FLU Screen
- 02.0.0 Main FLU Screen
- 02.0.0 Main FLU Screen
- 02.0.0 Main FLU Screen
- Payment Process
- Card write success?
- Card already validated  within passback period?
- Metro or  Ulsterbus TOO?
- Card is valid
- EMV/ABT Card is presented
- Once card is removed, go back to FLU
- Metro or  Ulsterbus TOO?
- 02.0.0 Main FLU Screen
- Go Back
- 02.0.0 Main FLU Screen
- Back to FLU
- Back to FLU
- User presses enter to confirm ticket selection
- Annulment flow
- Retry successful?
- Continue flow from 'Different Products, Alighting Stages and Fare based FLU"
- Discount smartcard presented and not faulty
- Discount smartcard presented and not faulty
- Go Back to 02.0.0 | FLU Home
- Issue ticket and go back to 02.0.0 | FLU Home
- 02.0.0 Main FLU Screen
- Printing flow

### Annotations / Spec Notes (67)
- DayLink Tap On
- Sales Mode
- Changing Boarding and Alighting Stages, Toggling the Product Page, Viewing Fare Based Products and viewing Favourite Stages.
- Removing the Smartcard during this flow will take the user back to 02.0.0 | FLU Home. iLink and Travelcards will follow this flow as well.
- The product pages are configurable.  The order can be configured in CloudFare and specific button options can be fixed within the device configuration.
- Example shown is for a Hotlisted card but could also be an expired card
- The last stage on the farelist is always displayed to the driver.
- User selects 'Top Up - 1 Day' once they've received payment. The dayLink card is then topped up by one day and also validated. This results in a receipt for the top up printing and a ticket for the validation printing.  Note: It is the day that was just loaded onto the card that is immediately validated. For example, the card is now valid for travel for the rest of the day, but does not hold any more days on it.  If the passenger would rather not top up and just get off the bus or buy a different ticket, they may remove the card to cancel.  If the user presses 'Top-up' (R6), they'll be taken to the 'Top-up' flow.
- If the GPS quality threshold is strong enough, the user will not be able to change the boarding stage manually.
- Note: This is not the only way to change the boarding stage. See the 'Numeric Input' flow to see how to change the boarding stage through it's ID.
- Once the smartcard is removed, the device will go back to FLU
- Pressing the star (*) key again will toggle the page back to the main FLU screen
- If a smartcard is attempted to be used twice in quick succession, this error appears.  If the smartcard has already been validated, the user can choose to override the validation and issue another ticket. This is useful for the user if they've accidentally selected the incorrect Alighting Stage. The previous transaction will need annuling as well.
- Sales Mode
- Different Products, Alighting Stages, Fare Based & Favourites FLU
- This screen is configurable in CloudFare and the options displayed are for example purposes.  The left hand buttons can be fixed to products/options.  L6 is reserved for Smartcard functionality.
- Smartcard Mini Statement and Top-up
- Removing the Smartcard during this flow will take the user back to 02.0.0 | FLU Home.
- Enter text....
- The amount of products you can toggle is a configurable amount but will only show the indicator as a maximum of 4. You can have as many products as you'd like in a product group but any more than 4 and it will be hidden behind an expandable menu (+).
- The user can press 'C' or the Go Back option (L6) to clear the menu and return to 02.0.0 Main FLU Screen. Alternatively, there is a timeout of 60 seconds which results in the same action.
- Enter text....
- Enter text....
- Enter text....
- Enter text....
- There is a timeout of 60 seconds to clear the current selection. This would take the user back to the default product as well. To select something else, press a different key.
- If the product selected is part of a product toggle group, the relevant dot is selected. If the product can only be found in the extended menu, the '+' is highlighted
- These are the Easibus products. The menu pops up immediately after a ticket is selected.  This screen is configurable for products displayed and is not hardcoded.
- For dayLink, the top up flow is identical except 'Days' are shown in place of 'Journeys' throughout.  For iLink and Metro Travelcard, the flow is the same except that the top up options on screen are related to periods of time like; 1 day, 1 week, 1 month.  'Go Back' option will take the user back to the 'Smartcard - Menu' screen.
- This screen is also displayed if a faulty smartcard is presented.
- ABT - Tap-On-Only
- Cancel (L6) will take the user back to the Smartcard Menu Screen
- If a customer presents a smartcard outside of a relevant time band, they will be unable to use it.
- When ABT taps are configured to be enabled they are typically expected to be inititiated when the ETM is in FLU mode.  ABT Taps will not be enabled when they may intefere with other operations or the device is not ready for them. (Eg. The ETM needs to be signed into a shift, other card handling functions are being interacted with or similar.)  Examples of when ABT taps are not available:  - Basket screens  - Basket mode enabled (item in basket)  - Driver Break  - Smartcard screens (top up/mini statement screens)  - Annul Previous Ticket screen  - The Start New Journey Flow     - Start New Journey > Select Route screen     - Start New Journey > Journey Number screen     - Start New Journey > Route Summary screen  - Travel Mode (when travelling above 5kph)
- When selecting an Alighting point for the TOO transaction the ETM will ignore other card presentations. (Smartcard and ABT)  The basket functionality will not be available on this screen.
- Removing the Smartcard will take the user back to 02.0.0 | FLU Home.
- For dayLink, iLink and Metro Travelcard, show the number of days left on the card in place of 'journeys' here.   After a successful top up, the card will be auto-validated (the same applied for iLink & Ulsterbus Town Service cards).
- Error Tone is played and will show "See Driver"
- A Success Tone is played and the passenger display will show "Success"
- A Success Tone is played and the passenger display will show "Success"
- This will typically be returning to 02.0.0 Main Flu unless the Tap occurred during  a screen flow that supports taps. Eg. Driver Menu.
- Example EMV Validation Failure screens
- The Error Tone is played, a declined receipt will be printed and the passenger display will show "See Driver" as a Tap Error is displayed.  Possible Scenarios: - Card has been declined (Bin List/Deny List/etc) - Card has expired - Tap Error (This will be displayed when the error is not well determined. Eg. A Card-tear or a mis-read.)  The customer needs to check their account for more information.
- Payment Process
- Printer Errors and Events
- Example of transaction success - this will timeout after 3 seconds
- An example showing post basket screen for mulitple issued tickets
- While driving, the device will change to a Travel Mode which displays the time and date to the driver to help minimise distraction. This triggers on a time out from FLU after 1 minute. Any button press takes the driver back to FLU.  Brightness will also be dimmed in Travel Mode.  When the bus stops the driver can press the enter key or a customer can present a smartcard to restore the brightness and return to FLU.  This screen also displays Schedule Adherence.  If the box is green, the operator is on time. If the box is orange, the operator is within a set parameter for early or late, and the times are +/-. If the box is red, the operator is outside of the set parameter and the times are +/-.
- Example of last transaction being updated in the bottom right hand corner of the UI. If the user wants to calculate change, see the Numeric Input flow.
- Annul Transaction is replaced by "Cancel" if error occurs while trying to print something other than a ticket. Such as Technician Menu and printing out the versions.
- If the paper is low, this error appears. It appears after printing a ticket if the paper is below a threshold value. it does not appear unless a ticket was printed.  Timeout is 5 seconds, and then goes back to 02.0.0 | FLU Home
- Promo Menu & Basket Tracker
- A printer error variation, for paper jams there is an option for Reverse Paper Feed. Reversing paper feed will not change this screen.
- The user can select an alighting stage. To change the currency, they can press the alighting stage key again, this will change the currency to €. To change back to £, the user can press the alighting stage key for a third time to toggle it back.  For basket mode, the user will need to follow the method above to change the currency to €, then enter the basket mode. This should keep the ETM in € mode and also unselect the selected alighting stage.
- If a product is currently selected when the user initiates basket mode, the selected product will be added to the basket as well. The previously selected product will also deselect upon it being added to the basket.
- yLink & Pass
- In the sub menus within the promo menu, the basket tracker remains and functions in the same way as in the promo menu and main screen.
- Example of a smartcard being presented for a free pass, for example, a senior pass.
- The customer only needs to tap their card to change the ETM into smartcard mode. The user can exit this state by pressing the 'C' key. If the cuatomer taps their card again, they'll put the ETM into passback mode.
- If the product is free, then pressing the associated button will automatically issue without having to press enter.
- The user is returned back to the menu they were on at purchase
- Only one smartcard ticket can be added per customer, so the menu on the left is reverted back to default.   It is possible to add other paper products (a child single for example) to the basket alongside a half fare or ylink product so that a single retail mode tap can be used as payment
- Numeric Input
- In the sub menus within the promo menu, the basket tracker remains and functions in the same way as in the promo menu and main screen.
- Pressing 'C' here will clear one character in the input field.  If this error screen displays, the input is automatically cleared.  The error message depends on what the user tried to do.  If 'Set Alighting Stage' could not be completed, the error message says "Unable to set Alighting Stage"  If 'Set Boarding Stage' could not be completed, the error message says "Unable to set Boarding Stage"  If change cannot be calculated due to the amount entered being less than the last transaction, the error message says "Unable to Calculate Change"
- By default, if the product is changed after selecting the alighting stage, the alighting stage is deselected.
- If the GPS threshold is strong enough, the user will not be able to manually change the boarding stage.

### Connections / Flow (103)
- Screen: "02.0.0 | FLU Home" → Screen: "02.0.1 | Product Page Example" [User presses the minus key to toggle through product pages]
- Screen: "02.0.0 | FLU Home" → Screen: "02.0.2 | Main Screen - FLU - Change Boarding Stage" [User presses the right arrow key to select the next boarding stage]
- Screen: "02.0.0 | FLU Home" → Screen: "02.0.3 | FLU - Alighting Stages 06-09" [User presses the down arrow key to view another more alighting stages]
- Screen: "02.0.0 | FLU Home" → Screen: "02.0.4 | FLU - Fare-Based - Journeys" [User presses star (*) key]
- Screen: "02.0.4 | FLU - Fare-Based - Journeys" → Screen: "02.0.4.1 | FLU - Fav Journeys" [User presses star (*) key to toggle to favourites]
- Screen: "02.0.4.1 | FLU - Fav Journeys" → Screen: "02.0.4.2 FLU - Transfer Journeys" [User presses star (*) key to toggle to transfer journeys]
- Screen: "02.0.3 | FLU - Alighting Stages 06-09" → Screen: "02.0.3.1 | FLU - Alighting Stages 23 _ 24" [User presses the down arrow key until the last page of alighting stages are left.
 The user can press the up arrow to navigate back through the alighting stages]
- Screen: "02.0.0 | FLU Home" → Decision: "'Numeric Input' Flow" [User presses a number key]
- Screen: "02.0.0 | FLU Home" → Decision: "'Basket Mode' Flow" [User presses R6 key]
- Screen: "02.0.0 | FLU Home" → Screen: "02.1.0 | Toggle Group - Group" [Pressing a button associated with a toggle 
group will select the next product in that group]
- Screen: "02.0.0 | FLU Home" → Screen: "02.2 | Preset Product" [Preset Product is Selected]
- Screen: "02.0.0 | FLU Home" → Screen: "02.3 | Menu Type" [Menu Type Selected]
- Screen: "02.1.0 | Toggle Group - Group" → Screen: "02.1.1 | Toggle Groups - List" [Pressing '+' expands the products within the toggle group 
to display them as a list on a seperate screen]
- Screen: "02.1.1 | Toggle Groups - List" → Screen: "02.1.2 Toggle Group - Flu Product Selected from Menu" [Once the desired product is selected, the user 
selects an alighting stage using R1 - R5]
- Screen: "02.1.2 Toggle Group - Flu Product Selected from Menu" → Screen: "02.1.3 Flu Product Selected - Alighting Stage Selected" [Once a product is selected, the user selects an alighting stage using R1 - R5 buttons]
- Screen: "02.0.0 | FLU Home" → Screen: "02.4 | FLU Product"
- Screen: "02.4 | FLU Product" → Screen: "02.4.1 | FLU Product - Alighting Stage Selected"
- Screen: "02.3 | Menu Type" → Screen: "02.3.1 | Menu Type - Product Selected"
- Screen: "02.1.0 | Toggle Group - Group" → Decision: "02.0.0 Main FLU Screen" [Pressing 'C' or a timeout of 60 seconds will take the user
 back to their first product in the toggle group]
- Screen: "02.1.1 | Toggle Groups - List" → Decision: "02.0.0 Main FLU Screen" [User presses L6 (Go Back)]
- Screen: "02.1.3 Flu Product Selected - Alighting Stage Selected" → Decision: "Payment Process" [User presses enter to confirm selection, issuing the ticket]
- Decision: "Payment Process" → Decision: "02.0.0 Main FLU Screen" [Payment is successful and ticket is printed (if applicable)]
- Screen: "02.2 | Preset Product" → Decision: "02.0.0 Main FLU Screen" [Pass product selected]
- Decision: "User presses enter to confirm ticket selection" → Screen: "2.5 | Main Screen - Last Transaction 200 - Success" [Cash, user presses enter]
- Screen: "2.5 | Main Screen - Last Transaction 200 - Success" → Screen: "2.5.1 | Main Screen - Last Transaction 200" [Timeout of 3 seconds]
- Screen: "02.6.1 | EMV Validation Failure" → Decision: "02.0.0 Main FLU Screen" [2 second timeout,  card removal is detected, 
or L6 (Go Back) is pressed]
- Screen: "02.6 | EMV Validated" → Decision: "02.0.0 Main FLU Screen" [Card is removed or 2 seconds timeout]
- Screen: "02.0.0 | FLU Home" → Screen: "03.0 | Promo Menu" [User selects Promo option, which would appear on one of the
 right sided buttons. It can be configuted to be shown]
- Screen: "03.0 | Promo Menu" → Screen: "03.0.1 | Promo Menu - Basket Mode" [User presses R6 to change to basket mode]
- Screen: "03.0 | Promo Menu" → Screen: "03.0.1.3 | Promo Menu Product Selected" [User selects a product]
- Screen: "03.0 | Promo Menu" → Screen: "03.0.2.2 | Promo Menu  - P&R Menu" [User selects a product sub menu]
- Screen: "03.0.1 | Promo Menu - Basket Mode" → Screen: "03.0.3 | Promo Menu - Basket Mode - Ticket Selected" [User selects a product and is highlighted to the user]
- Screen: "03.0.1 | Promo Menu - Basket Mode" → Screen: "03.0.2.1 | Promo Menu - Basket Mode - P&R Menu" [User selects a sub menu to see further products]
- Screen: "03.0.1.1 - Promo Menu - Ticket Purchased" → Screen: "03.0.1.2 - Promo Menu - Updated Last" [Timeout of 3 seconds, green banner disappears]
- Screen: "03.0.3 | Promo Menu - Basket Mode - Ticket Selected" → Screen: "03.0.2 | Promo Menu - Basket Mode - Ticket in Basket" [User presses enter to confirm selection and add it to the basket]
- Screen: "03.0.1.3 | Promo Menu Product Selected" → Screen: "03.0.1.1 - Promo Menu - Ticket Purchased" [User presses enter to confirm selection]
- Screen: "04.0 | Numeric Entry - 9 - Change & Alighting" → Screen: "04.0.1 | Numeric Entry - 9017 - Change & Alighting" [
User can enter a number to represent the following;
- Group Ticket Amount
- Boarding Stage ID
- Alighting Stage ID
- or the amount of cash given, to calculate change

]
- Screen: "04.0.1 | Numeric Entry - 9017 - Change & Alighting" → Screen: "04.1 | FLU - Group Ticket - Payment" [User can enter a number between 2 and 100 and issue a group ticket]
- Screen: "04.0.1 | Numeric Entry - 9017 - Change & Alighting" → Screen: "04.0.1.1 | Numeric Entry - 500 - Change Calculated" [Calculate change based off the value entered]
- Screen: "04.0.1 | Numeric Entry - 9017 - Change & Alighting" → Screen: "04.0.1.2 | Numeric Entry - 9017 - Change & Alighting - Error Bar" [User enters an invalid number]
- Screen: "04.0.1 | Numeric Entry - 9017 - Change & Alighting" → Screen: "04.0.1.3 | Main Screen - FLU - 9017 Alighting Stage Chosen" [User selects alighting stage to the ID, in this case 9017]
- Screen: "02.0.0 | FLU Home" → Screen: "04.0 | Numeric Entry - 9 - Change & Alighting" [User uses the numeric keypad to start entering a number]
- Screen: "04.0.1 | Numeric Entry - 9017 - Change & Alighting" → Screen: "02.0.0 | FLU Home" [User cancels and is taken back to the Main FLU screen]
- Screen: "04.0.1.1 | Numeric Entry - 500 - Change Calculated" → Decision: "Printing flow" [An optional receipt is selected]
- Screen: "04.0.1.1 | Numeric Entry - 500 - Change Calculated" → Screen: "02.0.0 | FLU Home" [User selects 'Go Back' (L6)]
- Decision: "Is it a valid card?" → Screen: "05.0.0 - Hotlisted Error" [No]
- Screen: "02.0.0 | FLU Home" → Decision: "Is it a valid card?" [DayLink card is presented]
- Decision: "Is it a valid card?" → Decision: "Has the card already been tapped today?" [Yes]
- Decision: "Has the card already been tapped today?" → Decision: "Has this card already been tapped on this bus in the last x minutes?" [Yes]
- Decision: "Has the card already been tapped today?" → Decision: "Is there at least one day available on the card?" [No, first tap of the day]
- Decision: "Is there at least one day available on the card?" → Screen: "05.0.2 - FLU - DayLink Tap on - Success" [Yes, charge one day off the card]
- Decision: "Has this card already been tapped on this bus in the last x minutes?" → Screen: "05.0.2 - FLU - DayLink Tap on - Success" [No, continue and do not charge the card]
- Decision: "Has this card already been tapped on this bus in the last x minutes?" → Screen: "05.0.3 - FLU - Smartcard Already Validated" [Yes, passback]
- Decision: "Is there at least one day available on the card?" → Screen: "05.0.1 - FLU - Smartcard Top Up - No Journeys Left Error" [No, card presented does not have enough credit]
- Screen: "02.0.0 | FLU Home" → Screen: "06.0.0 - Present Smartcard" [Smartcard option selected]
- Screen: "06.0.0 - Present Smartcard" → Screen: "06.0.1 - FLU - Smart Card - Menu" [Smartcard presented]
- Screen: "06.0.1 - FLU - Smart Card - Menu" → Screen: "06.0.1.3 - FLU - Smartcard Top Up - Error - Remove Smartcard" [User presses Go Back and hasn't removed the smartcard]
- Screen: "06.0.1 - FLU - Smart Card - Menu" → Screen: "06.0.1.1 - FLU - Smart Card - Mini Statement" [Mini statement option selected]
- Screen: "06.0.1 - FLU - Smart Card - Menu" → Screen: "06.0.1.2 - FLU - Smart Card - Top Up" [Top up smartcard option selected]
- Screen: "06.0.1.2 - FLU - Smart Card - Top Up" → Screen: "06.0.1.2.1 - FLU - Smart Card - Top Up - Payment" [10 Journeys option selected]
- Screen: "06.0.1.2.1 - FLU - Smart Card - Top Up - Payment" → Decision: "Card write success?" [Issue top up]
- Decision: "Card write success?" → Screen: "06.0.1.2.3 - FLU - Smartcard - Top Up - Error" [No]
- Decision: "Card write success?" → Screen: "06.0.1.2.2 - FLU - Smartcard - Top Up - Confirmation" [Yes]
- Screen: "02.0.0 | FLU Home" → Screen: "06.0.2.0 -  FLU - Smartcard - Faulty - Select Card Type"
- Screen: "06.0.2.0 -  FLU - Smartcard - Faulty - Select Card Type" → Screen: "06.0.3.0 -  FLU - Smartcard - Faulty - Charge Full Fare" [Dependants Pass]
- Screen: "06.0.3.0 -  FLU - Smartcard - Faulty - Charge Full Fare" → Decision: "Back to FLU" [User continues (R6)]
- Screen: "06.0.3.0 -  FLU - Smartcard - Faulty - Charge Full Fare" → Screen: "06.0.2.0 -  FLU - Smartcard - Faulty - Select Card Type" [User presses Go Back (L6)]
- Screen: "06.0.4.0 -  FLU - Smartcard - Faulty - Issue Ticket" → Screen: "06.0.2.0 -  FLU - Smartcard - Faulty - Select Card Type" [User presses Go Back (L6)]
- Screen: "06.0.4.0 -  FLU - Smartcard - Faulty - Issue Ticket" → Decision: "Back to FLU" [User continues (R6)]
- Screen: "06.0.2.0 -  FLU - Smartcard - Faulty - Select Card Type" → Screen: "06.0.3.0 -  FLU - Smartcard - Faulty - Charge Full Fare" [Fare Paying Smartcard]
- Screen: "06.0.2.0 -  FLU - Smartcard - Faulty - Select Card Type" → Screen: "06.0.4.0 -  FLU - Smartcard - Faulty - Issue Ticket" [SmartPass]
- Screen: "06.0.0 - Present Smartcard" → Screen: "02.0.0 | FLU Home" [User cancels]
- Screen: "06.0.1.1 - FLU - Smart Card - Mini Statement" → Screen: "06.0.1 - FLU - Smart Card - Menu"
- Screen: "06.0.1.1 - FLU - Smart Card - Mini Statement" → Screen: "06.0.1 - FLU - Smart Card - Menu" [User presses Print and a receipt prints]
- Screen: "06.0.1.2.2 - FLU - Smartcard - Top Up - Confirmation" → Decision: "Once card is removed, go back to FLU"
- Screen: "07.0.0 - Printer Error
" → Decision: "Annulment flow" [User annuls transaction]
- Screen: "07.0.0 - Printer Error
" → Decision: "Retry successful?" [User retries]
- Decision: "Retry successful?" → Screen: "07.0.0 - Printer Error
" [No]
- Decision: "Retry successful?" → Decision: "Continue flow from 'Different Products, Alighting Stages and Fare based FLU"" [Yes]
- Screen: "06.0.5.0 -  Main Screen - FLU - yLink" → Screen: "06.0.5.1 - FLU Product - Alighting Stage selected - yLink" [An alighting stage is selected]
- Screen: "06.0.6.0 -  Main Screen - FLU - Free Product" → Screen: "06.0.7.0 -  Main Screen - FLU - Free Product - Notification" [When issuing a free pass, if the basket is enabled upon issuing the free pass, 
the basket is cleared and disabled. 
This notifies the user before completing the action.]
- Screen: "06.0.5.1 - FLU Product - Alighting Stage selected - yLink" → Screen: "06.0.5.3 - FLU Product - Alighting Stage selected - yLink - Basket - Added" [User presses R6 to initiate basket
 mode (R6) which adds the selected ticket to the basket]
- Decision: "Discount smartcard presented and not faulty" → Screen: "06.0.5.0 -  Main Screen - FLU - yLink"
- Decision: "Discount smartcard presented and not faulty" → Screen: "06.0.6.0 -  Main Screen - FLU - Free Product"
- Screen: "06.0.7.0 -  Main Screen - FLU - Free Product - Notification" → Decision: "Go Back to 02.0.0 | FLU Home"
- Screen: "06.0.7.0 -  Main Screen - FLU - Free Product - Notification" → Decision: "Issue ticket and go back to 02.0.0 | FLU Home"
- Screen: "06.0.10.0 - FLU - ABT Presented" → Screen: "06.0.10.1 - FLU Product - Alighting Stage selected - ABT" [An alighting stage is selected]
- Screen: "06.0.10.1 - FLU Product - Alighting Stage selected - ABT" → Screen: "06.1.0.0 | Pass Success" [Selected stage will be highlighted 
momentarily before issuing the ticket.]
- Screen: "06.0.5.1 - FLU Product - Alighting Stage selected - yLink" → Screen: "06.1.0.0 | Pass Success" [User presses enter to confirm selection]
- Screen: "06.1.0.0 | Pass Success" → Decision: "02.0.0 Main FLU Screen"
- Screen: "06.1.0.0 | Pass Success" → Decision: "Metro or 
Ulsterbus TOO?" [On removal of Smartcard
(If Smartcard was removed prior to
 this screen a 2 second timeout will 
also move the user forward)]
- Decision: "EMV/ABT Card is presented" → Decision: "Card is valid"
- Decision: "Card is valid" → Screen: "02.6.1 | EMV Validation Failure" [No]
- Decision: "Card is valid" → Decision: "Card already validated 
within passback period?" [Yes]
- Decision: "Metro or 
Ulsterbus TOO?" → Screen: "02.6 | EMV Validated" [Metro TOO]
- Decision: "Metro or 
Ulsterbus TOO?" → Screen: "06.0.10.0 - FLU - ABT Presented" [Ulsterbus TOO]
- Screen: "06.0.10.0 - FLU - ABT Presented" → Decision: "Metro or 
Ulsterbus TOO?" [The 'C' key is selected to abandon the transaction and return to FLU]
- Screen: "06.0.10.1 - FLU Product - Alighting Stage selected - ABT" → Decision: "Metro or 
Ulsterbus TOO?"
- Decision: "Metro or 
Ulsterbus TOO?" → Decision: "02.0.0 Main FLU Screen" [Ulsterbus]
- Decision: "Metro or 
Ulsterbus TOO?" → Decision: "Go Back" [Metro]
- Decision: "Card already validated 
within passback period?" → Decision: "Metro or 
Ulsterbus TOO?" [No]
- Decision: "Card already validated 
within passback period?" → Screen: "02.6.5 | EMV Validation Failure - Card already validated" [Yes]
- Screen: "02.6.5 | EMV Validation Failure - Card already validated" → Decision: "02.0.0 Main FLU Screen" [2 second timeout,  card removal is detected, 
or L6 (Go Back) is pressed]


## 6. FLU 2.0 Navigation

### Screens (27)
- Toggle Pips
- 02.0.0 | FLU Home
- 02.1.0 | Toggle Group - Flu Product 2
- 02.1.0.1 | Toggle Group - Flu Product 3
- 02.1.0.2 | Toggle Group - Flu Product 4
- 02.1.0.1 | Toggle Group - Group - Alighting Stage Selected
- 02.0.1 | Product Page Example
- 02.1.1.0 | Toggle Groups - List
- 02.1.2 Toggle Group - Flu Product Selected from Menu
- 02.1.3 Flu Product Selected - Alighting Stage Selected
- 02.4 | FLU Product
- 02.4.1 | FLU Product - Alighting Stage Selected
- 02.0.3 | FLU - Alighting Stages 06-09
- 02.0.3.1 | FLU - Alighting Stages 10_11
- 02.0.4 | FLU - Fare-Based - Journeys
- 02.0.4.1 | FLU - Fav Journeys
- 02.0.4.2 FLU - Transfer Journeys
- 02.0.2 | Main Screen - FLU - Change Boarding Stage
- 02.0.2.1 | Main Screen - FLU - Change Boarding Stage 2
- 02.0.2.2 | Main Screen - FLU - Last Boarding Stage
- 02.2 | Preset Product
- 02.2.1 | Preset Product Issued 01
- 02.2.1 | Preset Product Issued 02
- 02.3 | Menu Type
- 02.3.1 | Menu Type - Product Selected
- 07.0.4 | Main Screen - Currency is Euro
- 02.0.8 | FLU - Alighting Stages - Selected

### Decision Points (29)
- Comms Lock
- Barcode
- GPS Event
- Smartcard
- EMV/ABT Tap Event
- Printer Event
- Timeout: Auto End of Shift
- Remote Command
- Go to: '02.0.0 | FLU Home'
- 60 Timeout
- Go to: 'Payment Flow'
- Go to: 'Basket Flow'
- Go to: '02.0.0 | FLU Home'
- Fare based Journeys  configured for current route?
- Favourites configured  for current route?
- Transfers configured  for current route?
- Go to: '02.0.0 | FLU Home'
- Is current travel  Speed <20kph?
- Is the bus within  the GPS footprint of  the current stop?
- ETM is on first stop of the current route so an error tone will be played
- Device will remain on: '02.0.0 | FLU Home'
- Device will return to: '02.0.0 | FLU Home'
- ETM is on last stop of the current route so an error tone will be played
- Device will return to: '02.0.0 | FLU Home'
- Go to: 'Basket Flow'
- Go to: 'Payment Flow'
- Device will return to: '02.0.0 | FLU Home'
- Is the current route  enabled for  multi-currency?
- Go to: 'Basket Flow'

### Annotations / Spec Notes (13)
- FLU Toggle Groups
- The products that can be toggled via the FLU page will be the first four configured for the given Product Group.  Up to four 'toggle pips' will be displayed and only if there is more than 1 product in the group. If there is more than four products within a group the '+' icon will also be displayed.  Selecting any product other than the first four within the group will result in the '+' being highlighted.
- The following screens will represent a route with the following stages:  Route 10F (IN) 10115 Lagmore View 10102 Lagmore Dale 10862 Twinbrook Rd 10113 Bell Steele Road 10371 Pantridge Road 10110 Woodbourne Suffolk Rd 10111 Saint Teresa's 10112 Glen Parade 9041 City Cemetery 9037 Royal Hospitals 9034 Divis Tower 10867 Wellington Place (Queen St)
- Any selections or made whilst on FLU are subject to a 60 second timeout.  Ie. Alighting Stage Selection or  and alternate product type.  Upon the timeout expiring the ETM will return to the Default FLU page.
- FLU Alighting Stage Paging
- The FLU page will display up to five Alighting Stages.   The fifth Alighting Stage will always be the last stage of the given route unless it is already listed in the first four rows for a given page. In which case the row will be empty.  Each page will update the list from the next stage not previously displayed.  Note: There is no timeout associated with viewing alternate Alighting Stage pages.
- FLU Journey Type Toggle
- FLU Manually Change Boarding Stage
- Manual stage changing is available only when the Bus is both outside the GPS footprint of the current boarding stage and not travelling at a speed greater than 20kph.  If either of this conditions is true the ETM will be unresponsive.  Note: The boarding stage can also be changed manually via entering the Stage ID number. See 'Numeric Input' to see how to change boarding stage through its ID.
- FLU Preset/Pass menu
- FLU Menu Type Products
- FLU Menu - Alighting Stage selection and Currency Switch
- The user can select an Alighting Stage. To change the currency, they can press the Alighting Stage key again - this will change the currency to €. To change back to £, they'll press the Alighting Stage key for a third time.  For basket mode, the user will need to follow the method above to get into Euros, then enter basket mode. This should keep the ETM in Euro mode and also unselect a selected Alighting Stage.

### Connections / Flow (76)
- Screen: "02.0.0 | FLU Home" → Screen: "02.1.0 | Toggle Group - Flu Product 2" [User toggles the default Product Group 
by selecting the 'L1' key]
- Screen: "02.0.0 | FLU Home" → Screen: "02.1.1.0 | Toggle Groups - List" [User wishes to select from the products within 
the Default Toggle group by selecting the '+' key]
- Screen: "02.1.1.0 | Toggle Groups - List" → Screen: "02.1.2 Toggle Group - Flu Product Selected from Menu" [User selects a product type by 
pressing the relevant L1-5 or R1-5 key]
- Screen: "02.1.2 Toggle Group - Flu Product Selected from Menu" → Screen: "02.1.3 Flu Product Selected - Alighting Stage Selected"
- Screen: "02.0.0 | FLU Home" → Screen: "02.0.1 | Product Page Example"
- Screen: "02.0.1 | Product Page Example" → Screen: "02.0.0 | FLU Home"
- Screen: "02.0.0 | FLU Home" → Screen: "02.0.3 | FLU - Alighting Stages 06-09" [User selects the 'Down' key
to view the following alighting stages]
- Screen: "02.0.3 | FLU - Alighting Stages 06-09" → Screen: "02.0.3.1 | FLU - Alighting Stages 10_11" [User selects the 'Down' key
to view the following alighting stages]
- Screen: "02.0.3.1 | FLU - Alighting Stages 10_11" → Screen: "02.0.3 | FLU - Alighting Stages 06-09" [User selects the 'Up' key
to view the previous alighting stages]
- Screen: "02.0.0 | FLU Home" → Decision: "Fare based Journeys 
configured for current route?" [User selects the '*' key
to change the Journey Type]
- Screen: "02.0.4 | FLU - Fare-Based - Journeys" → Decision: "Favourites configured 
for current route?" [User selects the '*' key
to change the Journey Type]
- Screen: "02.0.0 | FLU Home" → Decision: "Is current travel 
Speed <20kph?" [User selects 'Right' key
to manually stage change onwards]
- Screen: "02.0.2.2 | Main Screen - FLU - Last Boarding Stage" → Decision: "ETM is on last stop of the current route so an error tone will be played"
- Screen: "02.0.0 | FLU Home" → Screen: "02.2 | Preset Product" [User selects the 'Preset' key]
- Screen: "02.0.0 | FLU Home" → Screen: "02.3 | Menu Type" [User selects the 'Promo' key.]
- Screen: "02.3 | Menu Type" → Screen: "02.3.1 | Menu Type - Product Selected"
- Screen: "02.1.0 | Toggle Group - Flu Product 2" → Screen: "02.1.0.1 | Toggle Group - Flu Product 3" [User toggles the 
product type by pressing 'L1']
- Screen: "02.1.0.1 | Toggle Group - Flu Product 3" → Screen: "02.1.0.2 | Toggle Group - Flu Product 4" [User toggles the 
product type by pressing 'L1']
- Decision: "Fare based Journeys 
configured for current route?" → Screen: "02.0.4 | FLU - Fare-Based - Journeys" [Yes]
- Decision: "Fare based Journeys 
configured for current route?" → Decision: "Favourites configured 
for current route?" [No]
- Decision: "Favourites configured 
for current route?" → Screen: "02.0.4.1 | FLU - Fav Journeys" [Yes]
- Decision: "Favourites configured 
for current route?" → Decision: "Transfers configured 
for current route?" [No]
- Decision: "Transfers configured 
for current route?" → Screen: "02.0.4.2 FLU - Transfer Journeys" [Yes]
- Screen: "02.0.4.1 | FLU - Fav Journeys" → Decision: "Transfers configured 
for current route?" [User selects the '*' key
to change the Journey Type]
- Decision: "Transfers configured 
for current route?" → Decision: "Go to:
'02.0.0 | FLU Home'" [No]
- Screen: "02.0.4.2 FLU - Transfer Journeys" → Decision: "Go to:
'02.0.0 | FLU Home'" [User selects the '*' key
to change the Journey Type]
- Screen: "02.1.0.1 | Toggle Group - Flu Product 3" → Screen: "02.1.0.1 | Toggle Group - Group - Alighting Stage Selected" [User selects an alighting stage by select 'R1-5']
- Screen: "02.1.0.1 | Toggle Group - Group - Alighting Stage Selected" → Decision: "Go to:
'Payment Flow'"
- Screen: "02.1.3 Flu Product Selected - Alighting Stage Selected" → Decision: "Go to:
'Payment Flow'"
- Screen: "02.1.0.1 | Toggle Group - Group - Alighting Stage Selected" → Decision: "Go to:
'Basket Flow'"
- Screen: "02.1.3 Flu Product Selected - Alighting Stage Selected" → Decision: "Go to:
'Basket Flow'"
- Screen: "02.0.3 | FLU - Alighting Stages 06-09" → Decision: "Go to:
'02.0.0 | FLU Home'"
- Decision: "Is current travel 
Speed <20kph?" → Decision: "Is the bus within 
the GPS footprint of 
the current stop?" [Yes]
- Decision: "Is the bus within 
the GPS footprint of 
the current stop?" → Screen: "02.0.2 | Main Screen - FLU - Change Boarding Stage" [No
Moving back or forth to Stage 2]
- Decision: "Is current travel 
Speed <20kph?" → Decision: "Device will remain on:
'02.0.0 | FLU Home'" [No]
- Decision: "Is the bus within 
the GPS footprint of 
the current stop?" → Decision: "Device will remain on:
'02.0.0 | FLU Home'" [Yes]
- Screen: "02.0.0 | FLU Home" → Decision: "ETM is on first stop of the current route so an error tone will be played" [User selects 'Left' key
to manually stage change backwards]
- Decision: "ETM is on first stop of the current route so an error tone will be played" → Decision: "Device will remain on:
'02.0.0 | FLU Home'"
- Decision: "ETM is on last stop of the current route so an error tone will be played" → Screen: "02.0.2.2 | Main Screen - FLU - Last Boarding Stage"
- Screen: "02.0.2.1 | Main Screen - FLU - Change Boarding Stage 2" → Decision: "Is current travel 
Speed <20kph?"
- Screen: "02.2 | Preset Product" → Decision: "Device will return to:
'02.0.0 | FLU Home'"
- Screen: "02.3 | Menu Type" → Decision: "Device will return to:
'02.0.0 | FLU Home'"
- Screen: "02.3.1 | Menu Type - Product Selected" → Decision: "Device will return to:
'02.0.0 | FLU Home'"
- Screen: "02.3.1 | Menu Type - Product Selected" → Decision: "Go to:
'Basket Flow'"
- Screen: "02.3 | Menu Type" → Decision: "Go to:
'Basket Flow'"
- Screen: "02.3.1 | Menu Type - Product Selected" → Decision: "Go to:
'Payment Flow'"
- Screen: "02.3 | Menu Type" → Decision: "Device will return to:
'02.0.0 | FLU Home'"
- Screen: "02.3.1 | Menu Type - Product Selected" → Decision: "Device will return to:
'02.0.0 | FLU Home'"
- Screen: "02.0.0 | FLU Home" → Decision: "Barcode" [Barcode is presented to reader]
- Screen: "02.0.0 | FLU Home" → Decision: "GPS Event" [GPS invoked Stage Change]
- Screen: "02.0.0 | FLU Home" → Decision: "Smartcard" [miFare Smart card is presented]
- Screen: "02.0.0 | FLU Home" → Decision: "EMV/ABT Tap Event" [Open Payment Tap event occurs]
- Screen: "02.0.0 | FLU Home" → Decision: "Printer Event" [Printer Event is detected]
- Screen: "02.0.0 | FLU Home" → Decision: "Timeout:
Auto End of Shift" [Timeout: End of Shift]
- Screen: "02.0.2 | Main Screen - FLU - Change Boarding Stage" → Decision: "Is current travel 
Speed <20kph?"
- Screen: "02.0.2 | Main Screen - FLU - Change Boarding Stage" → Decision: "Is current travel 
Speed <20kph?"
- Decision: "Is the bus within 
the GPS footprint of 
the current stop?" → Screen: "02.0.2.1 | Main Screen - FLU - Change Boarding Stage 2" [No
Moving back or forth to Stage 11]
- Decision: "Is the bus within 
the GPS footprint of 
the current stop?" → Screen: "02.0.2.2 | Main Screen - FLU - Last Boarding Stage" [No
Moving forth to the final stage]
- Decision: "Is the bus within 
the GPS footprint of 
the current stop?" → Decision: "Device will return to:
'02.0.0 | FLU Home'" [No
Moving back to the first stage]
- Screen: "02.0.2.1 | Main Screen - FLU - Change Boarding Stage 2" → Decision: "Is current travel 
Speed <20kph?"
- Screen: "02.0.2.2 | Main Screen - FLU - Last Boarding Stage" → Decision: "Is current travel 
Speed <20kph?"
- Screen: "02.1.0 | Toggle Group - Flu Product 2" → Decision: "60 Timeout"
- Screen: "02.1.0.1 | Toggle Group - Flu Product 3" → Decision: "60 Timeout"
- Screen: "02.1.0.2 | Toggle Group - Flu Product 4" → Decision: "60 Timeout"
- Screen: "02.1.0.1 | Toggle Group - Group - Alighting Stage Selected" → Decision: "60 Timeout"
- Screen: "02.1.1.0 | Toggle Groups - List" → Decision: "60 Timeout"
- Screen: "02.1.2 Toggle Group - Flu Product Selected from Menu" → Decision: "60 Timeout"
- Screen: "02.1.3 Flu Product Selected - Alighting Stage Selected" → Decision: "60 Timeout"
- Decision: "60 Timeout" → Decision: "Go to:
'02.0.0 | FLU Home'"
- Screen: "02.1.0.2 | Toggle Group - Flu Product 4" → Decision: "Go to:
'02.0.0 | FLU Home'"
- Screen: "02.0.0 | FLU Home" → Screen: "02.4 | FLU Product"
- Screen: "02.0.0 | FLU Home" → Screen: "02.0.8 | FLU - Alighting Stages - Selected" [User selects R1-R5 for an alighting stage.
[R3}]
- Screen: "02.0.8 | FLU - Alighting Stages - Selected" → Decision: "Is the current route 
enabled for 
multi-currency?" [User selects the same Alighting Stage 
whilst the default currency [GBP]  is active]
- Screen: "07.0.4 | Main Screen - Currency is Euro" → Screen: "02.0.8 | FLU - Alighting Stages - Selected" [User selects the same Alighting Stage 
whilst the secondary currency is active ]
- Decision: "Is the current route 
enabled for 
multi-currency?" → Screen: "07.0.4 | Main Screen - Currency is Euro" [Yes]
- Screen: "07.0.4 | Main Screen - Currency is Euro" → Decision: "Go to:
'Basket Flow'"


## 7. FLU - Basket Mode

### Screens (17)
- 02.0.0 | FLU Home
- 02.7.8 | Main Screen - FLU - Multiple Items - Basket is Full
- 02.7.8.1 | Main Screen - FLU - Multiple Items - Basket Full - Error
- 02.7 | Main Screen - FLU - Multiple Items - Basket Mode Selected
- 02.7.1 | Main Screen - FLU - Multiple Items - 1 Ticket Chosen
- 02.7.2 | Main Screen - FLU - Multiple Items - Basket - Page 1
- 02.7.2.1 | Main Screen - FLU - Multiple Items - Basket - Euros
- 02.7.3 | Main Screen - FLU - Multiple Items - Basket - Page 2
- 02.7.3.1 | Main Screen - FLU - Multiple Items - Basket - Delete Item
- 02.7.3.2 | Main Screen - FLU - Multiple Items - Basket - Quantity Error
- 02.7.4 | Main Screen - FLU - Multiple Items - Basket - Item Deleted
- 02.7.5 | Main Screen - FLU - Multiple Items - Basket - Confirmed
- 05.4.2 | Above Threshold
- 01.9.1 - Please Wait... Printing
- 05.2.1 | FLU/Bank Card/Present
- 05.4.4 | FLU/Transaction Approved-Confirmation
- 05.4.1 | FLU/Bank Card/Transaction Declined

### Decision Points (6)
- Back to FLU screen with basket empty
- Back to FLU screen to add more products to basket
- Is the transaction above the retail threshold?
- Payment Process Flow
- 02.0.0 Main FLU Screen
- Payment Process

### Annotations / Spec Notes (9)
- Basket Mode
- The basket can only hold 9 items. Once it is full, users will be unable to add any more to the basket.  If they're on the FLU and try to add a product, the user will get the Basket Full error.  If they're on the Basket screen, they'll be unable to add more items to the basket.  If a user removes an item from the basket, they will be able to add a new item to the basket.
- Pressing the R6 button will put the user into the basket mode.  If a product/alighting stage is currently selected when the user initiates basket mode, the selected product/alighting stage will be added to the basket as well. The previously selected alighting stage will also deselect upon it being added to the basket.
- The 'Add More to Basket' option will take the user back to FLU so they can add more items.  The 'Clear Basket' button will take the user back to FLU and clear the basket.
- When a line item is selected, the user can increase or decrease the quantity by using the '+' and '-' keys.  If the quantity can't be changed then a relevant error message is shown for 2 seconds.
- On the FLU screen, the product will be returned to default and basket will be disabled but Fave/All will stay unchanged.
- Timeout of 30seconds if no card is presented, as per PCI compliance. The FEIG will send us a cancel message automatically causing the timeout. (Driven by FEIG not ETM and NOT Configurable).  This behaves in the same way as if the user had pressed the 'Cancel' button (L6)
- Need to add possible different errors
- There is no option for the user to select print receipt. However, a receipt will automatically be printed if it is mandatory.

### Connections / Flow (20)
- Screen: "02.7 | Main Screen - FLU - Multiple Items - Basket Mode Selected" → Screen: "02.7.1 | Main Screen - FLU - Multiple Items - 1 Ticket Chosen" [Once in basket mode, pressing a button associated with a product or alighting
 stage will add it to the basket and remain highlighed for 2 seconds to give indication]
- Screen: "02.7.1 | Main Screen - FLU - Multiple Items - 1 Ticket Chosen" → Screen: "02.7.2 | Main Screen - FLU - Multiple Items - Basket - Page 1" [When items are in the basket, pressing R6 (Basket key) 
will take the user to the View Basket screen]
- Screen: "02.7.2 | Main Screen - FLU - Multiple Items - Basket - Page 1" → Decision: "Back to FLU screen to add more products to basket" [Add More to Basket]
- Screen: "02.7.2 | Main Screen - FLU - Multiple Items - Basket - Page 1" → Decision: "Back to FLU screen with basket empty" [Clear Basket]
- Screen: "02.7.2 | Main Screen - FLU - Multiple Items - Basket - Page 1" → Screen: "02.7.3 | Main Screen - FLU - Multiple Items - Basket - Page 2" [By using the up and down arrow keys, the user can access more pages 
if the amount of products in the basket does not fit on one screen.]
- Screen: "02.7.2 | Main Screen - FLU - Multiple Items - Basket - Page 1" → Screen: "02.7.3.1 | Main Screen - FLU - Multiple Items - Basket - Delete Item" [User selects a line item in the basket (R1 - R3), which selects the 
chosen item and enables the 'Delete Item' function (L4)]
- Screen: "02.7.3.1 | Main Screen - FLU - Multiple Items - Basket - Delete Item" → Screen: "02.7.4 | Main Screen - FLU - Multiple Items - Basket - Item Deleted" [User presses 'Delete Item' (L4)]
- Screen: "02.7.4 | Main Screen - FLU - Multiple Items - Basket - Item Deleted" → Screen: "02.7.5 | Main Screen - FLU - Multiple Items - Basket - Confirmed" [User presses confirm (R6) to continue to the payment screen]
- Screen: "02.7.5 | Main Screen - FLU - Multiple Items - Basket - Confirmed" → Decision: "Payment Process Flow" [User presses Cash (L5)]
- Decision: "Payment Process Flow" → Screen: "01.9.1 - Please Wait... Printing"
- Screen: "01.9.1 - Please Wait... Printing" → Decision: "02.0.0 Main FLU Screen"
- Screen: "02.7.5 | Main Screen - FLU - Multiple Items - Basket - Confirmed" → Decision: "Is the transaction above the retail threshold?" [User presses Bank Card (R5)]
- Screen: "05.2.1 | FLU/Bank Card/Present" → Screen: "05.4.4 | FLU/Transaction Approved-Confirmation" [Contactless card presented]
- Screen: "05.2.1 | FLU/Bank Card/Present" → Screen: "05.4.1 | FLU/Bank Card/Transaction Declined" [Transaction Declined]
- Screen: "05.4.2 | Above Threshold" → Screen: "02.7.4 | Main Screen - FLU - Multiple Items - Basket - Item Deleted" [Type something]
- Decision: "Is the transaction above the retail threshold?" → Screen: "05.4.2 | Above Threshold" [Yes]
- Decision: "Is the transaction above the retail threshold?" → Screen: "05.2.1 | FLU/Bank Card/Present" [No]
- Screen: "02.7.5 | Main Screen - FLU - Multiple Items - Basket - Confirmed" → Screen: "02.7.4 | Main Screen - FLU - Multiple Items - Basket - Item Deleted" [User cancels (L6) and is taken back to the basket screen]
- Screen: "05.2.1 | FLU/Bank Card/Present" → Screen: "02.7.5 | Main Screen - FLU - Multiple Items - Basket - Confirmed" [User cancels transaction and is returned to the basket confirmation screen]
- Screen: "05.4.4 | FLU/Transaction Approved-Confirmation" → Decision: "Payment Process" [Once printed, the user is taken to the payment process, where the green banner is shown]


## 8. Driver Menu / Options

### Screens (60)
- 08.0.0 Driver Menu
- 08.1.0 - Driver Options
- 08.0.1 - Inspector - Present Smartcard
- 08.2.0 - Driver Menu - Ticket History
- 08.2.1 - Driver Menu - Ticket History - View Ticket - Annulled
- 08.0.1.1 - Inspector - Invalid Smartcard
- 06.0.1.3 - FLU - Smartcard Top Up - Error - Remove Smartcard
- 08.2.1 - Driver Menu - Ticket History - View Ticket
- 08.0.2 - Driver Menu - Annulment - Top Up
- 08.0.2.1 - Annulment - Present Smartcard
- 08.0.2.3 - Driver Menu - Annulment unsuccessful - Incorrect Card
- 08.3.0 - Driver Menu - Duty Totals
- 08.3.1 - Driver Menu - Journey Totals
- 08.0.2.2 - Driver Menu - Annulment Successful - Smartcard
- 08.9.6 - ETM Soft Reboot
- 11.1.0 - Restarting
- 08.0.4 - Driver Menu - Annulment - yLink
- 08.0.2.1 - Annulment - Present Smartcard
- 08.0.2.3 - Driver Menu - Annulment unsuccessful - Incorrect Card
- 08.0.2.2 - Driver Menu - Annulment Successful - Smartcard
- 08.9.7 -Card Reader Soft Reboot
- 01.9 - Please Wait...
- 08.0.3 - Driver Menu - Annulment - Tickets
- 08.0.3.2 - Driver Menu - Annulment Unsuccessful
- 08.0.3.1 - Driver Menu - Annulment Successful
- 08.10.1 - Report Faulty Device?
- 08.10.2 - Driver Menu - Driver Faulty Device
- 08.10.4 - Main Screen - FLU - Faulty Device
- 08.0.4.2 - Driver Menu - Annulment - ABT TOO
- 08.10.3 - Faulty Device Already Reported
- 08.4.0 - Driver Menu - Display Settings - Brightness and Volume
- 08.0.5 - Open Tickets
- 08.0.5.1 - Excess Ticket
- 08.0.5.2 - Excess Ticket - Error
- 08.5.0 - Driver Menu - Paper Status
- 08.0.7 - Idle Screen - On Break/Black
- 08.0.7.1 - Incorrect Smartcard
- 08.6.0 - Driver Menu - Word and Colour of the Day
- COTD Left/COTDL10
- COTD Left/COTDL11
- COTD Left/COTDL16
- COTD Left/COTDL15
- COTD Left/COTDL13
- COTD Left/COTDL9
- COTD Left/COTDL12
- COTD Left/COTDL14
- 01.1.2 - Sign On - PIN Entry
- 01.1.3 - Sign On - PIN Entry - 4*
- 08.6.1 - Driver Menu - Word and Colour of the Day - Unavailable
- 01.1.4 - Sign On - Incorrect Details
- 01.1.5 - Sign On - Device Locked
- 08.7.0 - Driver Menu - Messages
- 08.0.6 -New Trip - Select New Route
- 08.7.1 - Driver Menu - Messages - Unavailable
- 01.1.6 -Sign Off?
- 01.9 - Please Wait...
- 08.9.0 - Driver Menu - BV Devices
- 08.9.1 - BV Device Selected
- 08.9.2 - BV Device Selected - Reboot?
- 08.9.3 - BV Device Selected - Summary

### Decision Points (50)
- Valid Smartcard?
- Annulled ticket?
- Go back to: '02.0.0.0 FLU'
- Go back to: '08.1.0 - Driver Options'
- Type of annulment
- Annulment Successful?
- Go back to: '08.0.0 Driver Menu'
- Go back to: '08.1.0 - Driver Options'
- Go to: '08.0.7 - Idle Screen - On Break/Black'
- Annulment Successful?
- Go back to: '08.1.0 - Driver Options'
- Go back to: '08.0.0 Driver Menu'
- Go back to: '08.1.0 - Driver Options'
- Annulment Successful?
- Go back to: '08.1.0 - Driver Options'
- Go back to: '08.0.0 Driver Menu'
- Device already reported  as faulty?
- Go back to: '02.0.0.0 FLU'
- Go back to: '08.0.0 Driver Menu'
- Go back to: '08.1.0 - Driver Options'
- Is amount processable?
- Default settings are restored.
- Go back to: '08.1.0 - Driver Options'
- Go back to:  '08.0.0 Driver menu'
- An excess ticket will be printed. Go back to: '02.0.0.0 FLU'
- Go to: '12.0.0 Barcode Reference'
- A test ticket is printed and the ETM remains on:  '08.0.0 Driver menu'
- Go back to: '02.0.0.0 FLU'
- Go back to: '08.1.0 - Driver Options'
- Smartcard matches current  Driver Staff ID OR a valid Supervisor Staff ID
- Is Word and Colour of the Day available?
- Correct Login Details?
- Driver?
- Go back to: '02.0.0.0 FLU'
- Current Driver is Sign-Off Go back to: '02.0.0.0 FLU'
- Go to: '09.0.0 Supervisor Menu'
- Incorrect details entered more  than 3 times?
- Go back to: '08.1.0 - Driver Options'
- Go to: '09.0.0 Supervisor Menu'
- Is Message of the Day available?
- Scheduling enabled?
- Go to:  '01.5.0 - Journey Selection'
- Go to:  '01.4.1 - Type Route - With Letters - Shown'
- Go back to:  '08.0.0 Driver menu'
- Paper feed is reversed and the ETM remains on:  '08.0.0 Driver menu'
- Go back to: '08.1.0 - Driver Options'
- Go back to:  '01.0.0 - Idle Screen'
- Selected device will reboot.
- Go back to:  '08.0.0 Driver menu'
- Go back to: '08.1.0 - Driver Options'

### Annotations / Spec Notes (34)
- Inspector
- Ticket History
- On an incorrect smartcard being presented, use "Transaction Unsuccessful" screen which is a smartcard error screen. The text should be "invalid smartcard"
- The cross on the 'Ticket History screen means the transaction has been annulled.  The up and down arrows will allow the user to view more logs in the Ticket History.
- Annulment
- Annulment only available for the last transaction that occurred less than a minute ago.  If the last transaction was a basket transaction the whole basket will be annulled at once.  On a stage change, the annulment list clears.
- Totals
- If an incorrect card is presented the ETM should request that card to be presented on this screen and therefore not kick you out to FLU when the current card is removed.
- Soft Reboot
- Removal of Smartcard will take the user back to FLU.  An annulled ticket will be printed and follow print flows seen on the FLU board
- 'Soft Reboot' turns the ETM off and back on again. ETM starts on 'Driver on Break' screen. Driver is not logged out.
- Reboot Card Reader
- Removal of Smartcard will take the user back to FLU.  An annulled ticket will be printed and follow print flows seen on the FLU board
- Report Faulty Reader
- 'Cancel' option will take the user back to the Annulment screen.  'Retry' option will take the user back to the Annulment Success check.
- 3 second timeout and back to FLU.  Annulled ticket/s will also be printed and follow print flows seen on the FLU board.
- When the reader is reported as faulty, the Faulty Device Icon is shown in the header.   This icon will remain in this state until the ETM is rebooted.
- Reporting a faulty device will send a notification to the back office.
- Open Tickets
- Display Settings
- 'Cancel' option will take the user back to the Driver Menu  'C' key will clear the value of the input field.
- Paper Status
- Driver Break
- Word and Colour of the Day
- When 'On Break' only the operator who put the ETM 'On Break' is able to sign in, other operators can not sign in. However, a supervisor can still log in to override this.  A break lasts for as long as configured in TMS. After the time runs out, the driver is signed out, and every one else is able to sign in again. The screen will be 'Idle'.
- The possible colours that can be displayed are as shown above.
- User can press the 'Go Back' key, or wait for the timeout which is 10 seconds. This will return the user to the 'On Break' screen.
- Pressing 'C' clears one character at a time.
- User can press the 'Go Back' key, or wait for the timeout which is 10 seconds. This will return the user to the 'On Break' screen.
- Message of the Day
- Start New Journey
- Sign Off
- Other Devices
- A waybill is printed and the printing waybill flow will be followed for this.

### Connections / Flow (131)
- Screen: "08.0.0 Driver Menu" → Screen: "08.1.0 - Driver Options" [User presses 'Driver Options' key.]
- Decision: "Type of annulment" → Screen: "08.0.3 - Driver Menu - Annulment - Tickets" [Annul Ticket/Product Issue]
- Decision: "Type of annulment" → Screen: "08.0.2 - Driver Menu - Annulment - Top Up" [Annul Top-Up]
- Decision: "Type of annulment" → Screen: "08.0.4 - Driver Menu - Annulment - yLink" [Annul Discount Card]
- Screen: "08.0.2 - Driver Menu - Annulment - Top Up" → Screen: "08.0.2.1 - Annulment - Present Smartcard" [User press 
'Annul key.]
- Screen: "08.0.2.1 - Annulment - Present Smartcard" → Decision: "Annulment Successful?"
- Screen: "08.0.2.1 - Annulment - Present Smartcard" → Screen: "08.0.2 - Driver Menu - Annulment - Top Up" [User press 'Cancel' key.]
- Decision: "Annulment Successful?" → Screen: "08.0.2.3 - Driver Menu - Annulment unsuccessful - Incorrect Card" [No]
- Decision: "Annulment Successful?" → Screen: "08.0.2.2 - Driver Menu - Annulment Successful - Smartcard" [Yes]
- Screen: "08.0.3 - Driver Menu - Annulment - Tickets" → Decision: "Annulment Successful?" [User presses 'Annul' key.]
- Decision: "Annulment Successful?" → Screen: "08.0.3.2 - Driver Menu - Annulment Unsuccessful" [No]
- Decision: "Annulment Successful?" → Screen: "08.0.3.1 - Driver Menu - Annulment Successful" [Yes]
- Screen: "08.0.2.1 - Annulment - Present Smartcard" → Decision: "Annulment Successful?" [User presents Smartcard.]
- Decision: "Annulment Successful?" → Screen: "08.0.2.3 - Driver Menu - Annulment unsuccessful - Incorrect Card" [No]
- Decision: "Annulment Successful?" → Screen: "08.0.2.2 - Driver Menu - Annulment Successful - Smartcard" [Yes]
- Screen: "08.0.4 - Driver Menu - Annulment - yLink" → Screen: "08.0.2.1 - Annulment - Present Smartcard" [User presses 
'Annul' key.]
- Screen: "08.0.5 - Open Tickets" → Screen: "08.0.5.1 - Excess Ticket"
- Screen: "08.0.5.1 - Excess Ticket" → Screen: "08.0.5 - Open Tickets" [User press 'Cancel' key.]
- Screen: "08.0.5.2 - Excess Ticket - Error" → Screen: "08.0.5 - Open Tickets"
- Screen: "08.0.0 Driver Menu" → Screen: "08.0.7 - Idle Screen - On Break/Black" [User presses 'Driver Break' key.]
- Screen: "08.0.0 Driver Menu" → Screen: "08.0.6 -New Trip - Select New Route" [User presses 'Start New Journey' key.]
- Screen: "08.0.0 Driver Menu" → Screen: "01.1.6 -Sign Off?" [User presses 'Sign Off' key.]
- Screen: "08.0.0 Driver Menu" → Screen: "08.0.1 - Inspector - Present Smartcard" [User Presses 'Inspector' Key.]
- Screen: "08.0.0 Driver Menu" → Decision: "Type of annulment" [User presses 'Annul Previous Transaction' key.]
- Screen: "08.0.0 Driver Menu" → Screen: "08.0.5 - Open Tickets" [User presses 'Open Tickets' key.]
- Screen: "08.0.0 Driver Menu" → Decision: "Go to:
'12.0.0 Barcode Reference'" [User presses 'Barcode Reference Entry' key.]
- Screen: "08.0.0 Driver Menu" → Decision: "A test ticket is printed and the ETM remains on: 
'08.0.0 Driver menu'" [User presses 'Print Test Ticket' key.]
- Screen: "08.0.7 - Idle Screen - On Break/Black" → Screen: "01.1.2 - Sign On - PIN Entry" [User Presses 'Enter' key.]
- Screen: "01.1.2 - Sign On - PIN Entry" → Screen: "01.1.3 - Sign On - PIN Entry - 4*" [User inputs ID using 
Numerical pad.]
- Decision: "Smartcard matches current 
Driver Staff ID OR a
valid Supervisor Staff ID" → Screen: "01.1.2 - Sign On - PIN Entry" [Yes]
- Decision: "Smartcard matches current 
Driver Staff ID OR a
valid Supervisor Staff ID" → Screen: "08.0.7.1 - Incorrect Smartcard" [No]
- Screen: "08.0.7 - Idle Screen - On Break/Black" → Decision: "Smartcard matches current 
Driver Staff ID OR a
valid Supervisor Staff ID" [Smartcard Presented]
- Screen: "01.1.3 - Sign On - PIN Entry - 4*" → Screen: "01.1.2 - Sign On - PIN Entry" [User presses 'C' key
when data field is empty]
- Screen: "01.1.2 - Sign On - PIN Entry" → Screen: "08.0.7 - Idle Screen - On Break/Black" [User presses 'C' key.]
- Screen: "01.1.3 - Sign On - PIN Entry - 4*" → Decision: "Correct Login Details?" [User presses 'Enter' key.]
- Decision: "Correct Login Details?" → Decision: "Incorrect details entered more
 than 3 times?" [No]
- Decision: "Correct Login Details?" → Decision: "Driver?" [Yes]
- Decision: "Driver?" → Decision: "Go to:
'09.0.0 Supervisor Menu'" [No (Supervisor)]
- Screen: "01.1.4 - Sign On - Incorrect Details" → Screen: "08.0.7 - Idle Screen - On Break/Black" [On Timeout]
- Decision: "Incorrect details entered more
 than 3 times?" → Screen: "01.1.4 - Sign On - Incorrect Details" [No]
- Decision: "Incorrect details entered more
 than 3 times?" → Screen: "01.1.5 - Sign On - Device Locked" [Yes]
- Screen: "08.0.1 - Inspector - Present Smartcard" → Decision: "Go back to:
'02.0.0.0 FLU'"
- Screen: "08.0.1 - Inspector - Present Smartcard" → Decision: "Valid Smartcard?"
- Decision: "Valid Smartcard?" → Screen: "06.0.1.3 - FLU - Smartcard Top Up - Error - Remove Smartcard" [Yes]
- Decision: "Valid Smartcard?" → Screen: "08.0.1.1 - Inspector - Invalid Smartcard" [No]
- Screen: "08.0.1.1 - Inspector - Invalid Smartcard" → Decision: "Go back to:
'02.0.0.0 FLU'" [Card Removed]
- Screen: "06.0.1.3 - FLU - Smartcard Top Up - Error - Remove Smartcard" → Decision: "Go back to:
'02.0.0.0 FLU'" [Card Removed]
- Screen: "08.1.0 - Driver Options" → Screen: "08.2.0 - Driver Menu - Ticket History" [User presses 'Last Ticket Issued' key.]
- Screen: "08.1.0 - Driver Options" → Screen: "08.3.0 - Driver Menu - Duty Totals" [User presses 'Totals' key.]
- Screen: "08.1.0 - Driver Options" → Screen: "08.9.6 - ETM Soft Reboot" [User presses 'Soft Reboot' key.]
- Screen: "08.1.0 - Driver Options" → Screen: "08.9.7 -Card Reader Soft Reboot" [User presses 'Reboot Card Reader' key.]
- Screen: "08.1.0 - Driver Options" → Decision: "Device already reported 
as faulty?" [User presses 'Report Faulty Reader' key.]
- Screen: "08.1.0 - Driver Options" → Screen: "08.0.0 Driver Menu"
- Screen: "08.1.0 - Driver Options" → Screen: "08.4.0 - Driver Menu - Display Settings - Brightness and Volume" [User presses 'Display Settings' key.]
- Screen: "08.1.0 - Driver Options" → Screen: "08.5.0 - Driver Menu - Paper Status" [User presses 'Paper Status' key.]
- Screen: "08.1.0 - Driver Options" → Decision: "Is Word and Colour of the Day available?" [User presses Word and Colour' key.]
- Screen: "08.1.0 - Driver Options" → Decision: "Is Message of the Day available?" [User presses 'Messages' key.]
- Screen: "08.1.0 - Driver Options" → Screen: "08.9.0 - Driver Menu - BV Devices" [User presses 'Other Devices' key.]
- Screen: "08.0.0 Driver Menu" → Decision: "Go back to:
'02.0.0.0 FLU'" [User presses 'Go Back' key.]
- Screen: "08.0.0 Driver Menu" → Decision: "Paper feed is reversed and the ETM remains on: 
'08.0.0 Driver menu'" [User presses 'Reverse Paper Feed' key.]
- Decision: "Driver?" → Decision: "Go back to:
'02.0.0.0 FLU'" [Yes]
- Screen: "08.2.0 - Driver Menu - Ticket History" → Decision: "Annulled ticket?"
- Screen: "08.2.0 - Driver Menu - Ticket History" → Decision: "Annulled ticket?" [User selects a ticket via the L1-L5 or R1-R5 keys.]
- Decision: "Annulled ticket?" → Screen: "08.2.1 - Driver Menu - Ticket History - View Ticket - Annulled" [Yes]
- Decision: "Annulled ticket?" → Screen: "08.2.1 - Driver Menu - Ticket History - View Ticket" [No]
- Screen: "08.2.1 - Driver Menu - Ticket History - View Ticket - Annulled" → Screen: "08.2.0 - Driver Menu - Ticket History"
- Screen: "08.2.1 - Driver Menu - Ticket History - View Ticket" → Screen: "08.2.0 - Driver Menu - Ticket History" [User press the 'Go Back' key.]
- Screen: "08.2.0 - Driver Menu - Ticket History" → Decision: "Go back to:
'08.1.0 - Driver Options'"
- Screen: "08.3.0 - Driver Menu - Duty Totals" → Decision: "Go back to:
'08.1.0 - Driver Options'" [User presses 'Go Back' key.]
- Screen: "08.3.0 - Driver Menu - Duty Totals" → Screen: "08.3.1 - Driver Menu - Journey Totals" [User press the 
'Journey' key.]
- Screen: "08.3.1 - Driver Menu - Journey Totals" → Screen: "08.3.0 - Driver Menu - Duty Totals" [User presses the
 'Duty' key.]
- Screen: "08.3.1 - Driver Menu - Journey Totals" → Decision: "Go back to:
'08.1.0 - Driver Options'" [User presses 'Go Back' key.]
- Screen: "08.9.6 - ETM Soft Reboot" → Decision: "Go back to:
'08.1.0 - Driver Options'" [User presses 'Cancel' key.]
- Screen: "08.9.6 - ETM Soft Reboot" → Screen: "11.1.0 - Restarting" [User presses 'Reboot' key.]
- Screen: "11.1.0 - Restarting" → Decision: "Go to:
'08.0.7 - Idle Screen - On Break/Black'"
- Screen: "08.9.7 -Card Reader Soft Reboot" → Decision: "Go back to:
'08.1.0 - Driver Options'"
- Screen: "08.9.7 -Card Reader Soft Reboot" → Screen: "01.9 - Please Wait..." [User presses 'Reboot' key.]
- Screen: "01.9 - Please Wait..." → Decision: "Go back to:
'08.1.0 - Driver Options'" [Once card reader has rebooted.]
- Decision: "Device already reported 
as faulty?" → Screen: "08.10.1 - Report Faulty Device?" [No]
- Decision: "Device already reported 
as faulty?" → Screen: "08.10.3 - Faulty Device Already Reported" [Yes]
- Screen: "08.10.3 - Faulty Device Already Reported" → Decision: "Go back to:
'08.1.0 - Driver Options'" [User presses 'Cancel' key.]
- Screen: "08.10.1 - Report Faulty Device?" → Decision: "Go back to:
'08.1.0 - Driver Options'" [User presses 'Cancel' key.]
- Screen: "08.10.1 - Report Faulty Device?" → Screen: "08.10.2 - Driver Menu - Driver Faulty Device" [User presses 'Confirm' key.]
- Screen: "08.4.0 - Driver Menu - Display Settings - Brightness and Volume" → Decision: "Go back to:
'08.1.0 - Driver Options'" [User presses 'Go Back' key.]
- Screen: "08.4.0 - Driver Menu - Display Settings - Brightness and Volume" → Decision: "Default settings are restored." [User presses 'Restore Defaults' key.]
- Screen: "08.5.0 - Driver Menu - Paper Status" → Decision: "Go back to:
'08.1.0 - Driver Options'" [User presses 'Go Back' key.]
- Screen: "08.6.1 - Driver Menu - Word and Colour of the Day - Unavailable" → Decision: "Go back to:
'08.1.0 - Driver Options'" [User presses 'Go Back' key.]
- Decision: "Is Word and Colour of the Day available?" → Screen: "08.6.0 - Driver Menu - Word and Colour of the Day" [Yes]
- Decision: "Is Word and Colour of the Day available?" → Screen: "08.6.1 - Driver Menu - Word and Colour of the Day - Unavailable" [No]
- Screen: "08.6.0 - Driver Menu - Word and Colour of the Day" → Decision: "Go back to:
'08.1.0 - Driver Options'"
- Decision: "Is Message of the Day available?" → Screen: "08.7.0 - Driver Menu - Messages" [Yes]
- Decision: "Is Message of the Day available?" → Screen: "08.7.1 - Driver Menu - Messages - Unavailable" [No]
- Screen: "08.7.0 - Driver Menu - Messages" → Decision: "Go back to:
'08.1.0 - Driver Options'"
- Screen: "08.7.1 - Driver Menu - Messages - Unavailable" → Decision: "Go back to:
'08.1.0 - Driver Options'"
- Screen: "08.0.2 - Driver Menu - Annulment - Top Up" → Decision: "Go back to:
'08.0.0 Driver Menu'" [User press 'Cancel' key.]
- Screen: "08.0.2.3 - Driver Menu - Annulment unsuccessful - Incorrect Card" → Screen: "08.0.2 - Driver Menu - Annulment - Top Up" [User press 'Retry' key.]
- Screen: "08.0.2.2 - Driver Menu - Annulment Successful - Smartcard" → Decision: "Go back to:
'02.0.0.0 FLU'" [On Smartcard removal]
- Screen: "08.0.3.1 - Driver Menu - Annulment Successful" → Decision: "Go back to:
'02.0.0.0 FLU'" [On page timeout.]
- Screen: "08.0.2.2 - Driver Menu - Annulment Successful - Smartcard" → Decision: "Go back to:
'02.0.0.0 FLU'" [On Smartcard removal]
- Screen: "01.1.5 - Sign On - Device Locked" → Decision: "Go to:
'09.0.0 Supervisor Menu'" [Supervisor presents smartcard to unlock ETM.]
- Screen: "01.1.6 -Sign Off?" → Screen: "01.9 - Please Wait..." [User presses 'Enter' key.]
- Screen: "08.0.7 - Idle Screen - On Break/Black" → Decision: "Current Driver is Sign-Off
Go back to:
'02.0.0.0 FLU'" [On page timeout]
- Screen: "08.0.7.1 - Incorrect Smartcard" → Screen: "08.0.7 - Idle Screen - On Break/Black" [User presses 'Go Back' key.]
- Screen: "08.0.7.1 - Incorrect Smartcard" → Screen: "08.0.7 - Idle Screen - On Break/Black" [On page timeout]
- Screen: "08.0.6 -New Trip - Select New Route" → Decision: "Go back to: 
'08.0.0 Driver menu'"
- Screen: "08.0.6 -New Trip - Select New Route" → Decision: "Scheduling enabled?"
- Decision: "Scheduling enabled?" → Decision: "Go to: 
'01.4.1 - Type Route - With Letters - Shown'" [No]
- Decision: "Scheduling enabled?" → Decision: "Go to: 
'01.5.0 - Journey Selection'" [Yes]
- Screen: "08.0.5 - Open Tickets" → Decision: "Go back to: 
'08.0.0 Driver menu'" [User press 'Go Back key.]
- Screen: "08.0.5.1 - Excess Ticket" → Decision: "Is amount processable?" [User Presses 'Issue' key.]
- Decision: "Is amount processable?" → Screen: "08.0.5.2 - Excess Ticket - Error" [No]
- Screen: "08.0.5.2 - Excess Ticket - Error" → Decision: "Is amount processable?"
- Decision: "Is amount processable?" → Decision: "An excess ticket will be printed.
Go back to:
'02.0.0.0 FLU'" [Yes]
- Screen: "01.1.6 -Sign Off?" → Decision: "Go back to: 
'08.0.0 Driver menu'" [User presses 'Cancel' button]
- Screen: "08.0.4 - Driver Menu - Annulment - yLink" → Decision: "Go back to:
'08.0.0 Driver Menu'" [User presses 'Cancel' key.]
- Screen: "08.0.2.1 - Annulment - Present Smartcard" → Screen: "08.0.4 - Driver Menu - Annulment - yLink" [User presses 'Cancel' key.]
- Screen: "08.0.3 - Driver Menu - Annulment - Tickets" → Decision: "Go back to:
'08.0.0 Driver Menu'" [User presses 'Cancel' key.]
- Screen: "08.0.3.2 - Driver Menu - Annulment Unsuccessful" → Screen: "08.0.3 - Driver Menu - Annulment - Tickets" [User press 'Cancel' key.]
- Screen: "08.0.3.2 - Driver Menu - Annulment Unsuccessful" → Decision: "Annulment Successful?" [User Presses 'Retry' key.]
- Screen: "08.0.2.3 - Driver Menu - Annulment unsuccessful - Incorrect Card" → Decision: "Annulment Successful?" [User presses 'Retry' key.]
- Screen: "01.9 - Please Wait..." → Decision: "Go back to: 
'01.0.0 - Idle Screen'" [On successfully ending the shift...]
- Screen: "08.9.0 - Driver Menu - BV Devices" → Screen: "08.9.1 - BV Device Selected" [User presses 
'R1-R5' key]
- Screen: "08.9.1 - BV Device Selected" → Screen: "08.9.3 - BV Device Selected - Summary" [User presses 
'Summary' key.]
- Screen: "08.9.1 - BV Device Selected" → Screen: "08.9.2 - BV Device Selected - Reboot?" [User presses 
'Reboot' key.]
- Screen: "08.9.3 - BV Device Selected - Summary" → Screen: "08.9.1 - BV Device Selected" [User presses 'Cancel Key.]
- Screen: "08.9.2 - BV Device Selected - Reboot?" → Screen: "08.9.1 - BV Device Selected" [User presses 
'Cancel' key.]
- Screen: "08.9.2 - BV Device Selected - Reboot?" → Decision: "Selected device will reboot." [User presses 
'Reboot' key.]
- Screen: "08.9.0 - Driver Menu - BV Devices" → Decision: "Go back to:
'08.1.0 - Driver Options'" [User presses 
'Go back' key.]
- Decision: "Type of annulment" → Screen: "08.0.4.2 - Driver Menu - Annulment - ABT TOO" [Annul ABT TOO Product]
- Screen: "08.0.4.2 - Driver Menu - Annulment - ABT TOO" → Screen: "08.0.3.1 - Driver Menu - Annulment Successful" [User presses 'Annul' key.]
- Screen: "08.0.4.2 - Driver Menu - Annulment - ABT TOO" → Decision: "Go back to:
'08.0.0 Driver Menu'" [User presses 'Cancel' key.]


## 9. Supervisor

### Screens (19)
- 09.0.0 Supervisor Menu
- 09.5.0 Supervisor Menu - Versioning
- 09.5.1 Supervisor Menu - Serial Numbers
- 09.5.2 Supervisor Menu - Software Versions
- 09.5.3 Supervisor Menu - Configuration Versions
- 09.5.3.1 Supervisor Menu - Configuration Versions - Page 2
- 09.3.0 Supervisor Menu - Waybills - History
- 09.3.2 Supervisor Menu - Waybills - Detailed
- 09.3.1 Supervisor Menu - Waybills - History - Page 2
- 09.3.2.1 Supervisor Menu - Waybills - Detailed - Page 2
- 09.2.0 Supervisor Menu - GPS Information
- 09.2.1 Supervisor Menu - GPS Information - Error
- 09.1.0 Supervisor Menu - Force Communications
- 08.9.6 - ETM Soft Reboot
- 11.1.0 - Restarting
- 08.9.0 - Driver Menu - BV Devices
- 08.9.1 - BV Device Selected
- 08.9.2 - BV Device Selected - Reboot?
- 08.9.3 - BV Device Selected - Summary

### Decision Points (17)
- Was printing successful?
- Versions are printed. ETM remains on the same screen.
- 'Printer Error' screen in FLU section
- Go back to:  '09.0.0 Supervisor Menu'
- Was printing successful?
- Versions are printed. ETM remains on the same screen.
- 'Printer Error' screen in FLU section
- Go back to:  '09.0.0 Supervisor Menu'
- GPS Information available?
- Go back to:  '09.0.0 Supervisor Menu'
- Displayed information is updated.
- A manifest update check will be performed.
- Go back to:  '09.0.0 Supervisor Menu'
- Device will reboot and return to: '01.0.0 - Idle Screen'
- Selected device will reboot.
- Go back to: 09.0.0 Supervisor Menu'
- Go back to:  '01.0.0 - Idle Screen'

### Annotations / Spec Notes (19)
- Versions
- 'Go Back' key would be used to go back to the 'Supervisor Menu' screen.
- 'Go Back' key would be used to go back to the 'Versions' screen.
- 'Go Back' key would be used to go back to the 'Versions' screen.  The up and down arrow keys will allow the user to view more information in the Software Versions' list.
- 'Go Back' key would be used to go back to the 'Versions' screen.
- 'Go Back' key would be used to go back to the 'Versions' screen.
- Historic Waybills
- 'Go Back' key would be used to go back to the 'Supervisor Menu' screen.
- Once viewing a waybll, users can press the right and left arrow keys to view the next one.  'Go Back' key would be used to go back to the 'Waybills - History' screen.
- 'Go Back' key would be used to go back to the 'Supervisor Menu' screen.
- 'Go Back' key would be used to go back to the 'Waybills - History' screen.
- GPS Information
- 'Go Back' key would be used to go back to the 'Supervisor Menu' screen.
- 'Go Back' key would be used to go back to the 'Supervisor Menu' screen.
- Force Comms
- Pressing the 'Force Comms' button communicates with the back office for updates to download or data for the device to upload.   Pressing the 'Refresh' button updates the communication information if there were any errors obtaining it previously.  'Go Back' key would be used to go back to the 'Supervisor Menu' screen.
- Soft Reboot
- 'Cancel' key will take the user back to the 'Supervisor Menu' screen.
- Other Devices

### Connections / Flow (49)
- Decision: "Was printing successful?" → Decision: "Versions are printed.
ETM remains on the same screen." [Yes]
- Decision: "Was printing successful?" → Decision: "'Printer Error' screen in FLU section" [No]
- Screen: "09.5.3 Supervisor Menu - Configuration Versions" → Decision: "Was printing successful?" [User presses
 'Print' key.]
- Screen: "09.5.2 Supervisor Menu - Software Versions" → Decision: "Was printing successful?" [User presses
 'Print' key.]
- Screen: "09.5.1 Supervisor Menu - Serial Numbers" → Decision: "Was printing successful?" [User presses
 'Print' key.]
- Screen: "09.5.3.1 Supervisor Menu - Configuration Versions - Page 2" → Decision: "Was printing successful?" [User presses
 'Print' key.]
- Screen: "09.5.0 Supervisor Menu - Versioning" → Screen: "09.5.1 Supervisor Menu - Serial Numbers" [User presses
 'Serial Numbers' key.]
- Screen: "09.5.0 Supervisor Menu - Versioning" → Screen: "09.5.2 Supervisor Menu - Software Versions" [User presses 
'Software Versions' key.]
- Screen: "09.5.0 Supervisor Menu - Versioning" → Screen: "09.5.3 Supervisor Menu - Configuration Versions" [User presses 
'Configuration Versions' key.]
- Screen: "09.5.3.1 Supervisor Menu - Configuration Versions - Page 2" → Screen: "09.5.3 Supervisor Menu - Configuration Versions" [User presses
 'Up' key.]
- Screen: "09.5.3 Supervisor Menu - Configuration Versions" → Screen: "09.5.3.1 Supervisor Menu - Configuration Versions - Page 2" [User presses
 'Down' key.]
- Screen: "09.5.0 Supervisor Menu - Versioning" → Decision: "Go back to: 
'09.0.0 Supervisor Menu'" [User press
 'Go Back' key.]
- Screen: "09.5.1 Supervisor Menu - Serial Numbers" → Screen: "09.5.0 Supervisor Menu - Versioning" [User presses
 'Go Back' key.]
- Screen: "09.0.0 Supervisor Menu" → Screen: "09.5.0 Supervisor Menu - Versioning" [User presses 'Versions' key.]
- Screen: "09.0.0 Supervisor Menu" → Screen: "09.3.0 Supervisor Menu - Waybills - History" [User presses 'Historic Waybills' key.]
- Screen: "09.0.0 Supervisor Menu" → Decision: "GPS Information available?" [User presses 'GPS Information' key.]
- Screen: "09.0.0 Supervisor Menu" → Screen: "09.1.0 Supervisor Menu - Force Communications" [User presses 'Force Comms' key.]
- Screen: "09.0.0 Supervisor Menu" → Screen: "08.9.6 - ETM Soft Reboot" [User presses 'Soft Reboot' key.]
- Screen: "09.3.0 Supervisor Menu - Waybills - History" → Screen: "09.3.1 Supervisor Menu - Waybills - History - Page 2" [User presses 'Down' key.]
- Screen: "09.3.1 Supervisor Menu - Waybills - History - Page 2" → Screen: "09.3.0 Supervisor Menu - Waybills - History"
- Screen: "09.3.0 Supervisor Menu - Waybills - History" → Screen: "09.3.2 Supervisor Menu - Waybills - Detailed" [User presses L1-L5 
to select a Waybill to view.]
- Screen: "09.3.2 Supervisor Menu - Waybills - Detailed" → Screen: "09.3.2.1 Supervisor Menu - Waybills - Detailed - Page 2" [User presses
 'Down' key.]
- Screen: "09.3.2.1 Supervisor Menu - Waybills - Detailed - Page 2" → Screen: "09.3.2 Supervisor Menu - Waybills - Detailed" [User presess 
'Up' key.]
- Screen: "09.3.0 Supervisor Menu - Waybills - History" → Decision: "Go back to: 
'09.0.0 Supervisor Menu'" [User press
 'Go Back' key.]
- Screen: "09.3.1 Supervisor Menu - Waybills - History - Page 2" → Decision: "Go back to: 
'09.0.0 Supervisor Menu'" [User press
 'Go Back' key.]
- Screen: "09.3.2 Supervisor Menu - Waybills - Detailed" → Screen: "09.3.0 Supervisor Menu - Waybills - History" [User presses 
'Go Back' key.]
- Screen: "09.3.2.1 Supervisor Menu - Waybills - Detailed - Page 2" → Screen: "09.3.0 Supervisor Menu - Waybills - History" [User presess 
'Go Back' key.]
- Decision: "Was printing successful?" → Decision: "Versions are printed.
ETM remains on the same screen." [Yes]
- Decision: "Was printing successful?" → Decision: "'Printer Error' screen in FLU section" [No]
- Screen: "09.3.2 Supervisor Menu - Waybills - Detailed" → Decision: "Was printing successful?" [User presses 
'Print' key.]
- Screen: "09.3.2.1 Supervisor Menu - Waybills - Detailed - Page 2" → Decision: "Was printing successful?" [User presses 
'Print' key.]
- Screen: "08.9.0 - Driver Menu - BV Devices" → Screen: "08.9.1 - BV Device Selected" [User presses 
'R1-R5' key]
- Screen: "08.9.1 - BV Device Selected" → Screen: "08.9.3 - BV Device Selected - Summary" [User presses 
'Summary' key.]
- Screen: "08.9.1 - BV Device Selected" → Screen: "08.9.2 - BV Device Selected - Reboot?" [User presses 
'Reboot' key.]
- Screen: "08.9.3 - BV Device Selected - Summary" → Screen: "08.9.1 - BV Device Selected" [User presses 'Cancel Key.]
- Screen: "08.9.2 - BV Device Selected - Reboot?" → Screen: "08.9.1 - BV Device Selected" [User presses 
'Cancel' key.]
- Screen: "08.9.2 - BV Device Selected - Reboot?" → Decision: "Selected device will reboot." [User presses 
'Reboot' key.]
- Screen: "08.9.0 - Driver Menu - BV Devices" → Decision: "Go back to:
09.0.0 Supervisor Menu'" [User presses 
'Go back' key.]
- Screen: "09.0.0 Supervisor Menu" → Screen: "08.9.0 - Driver Menu - BV Devices" [User presses 'Other Devices' key.]
- Screen: "09.0.0 Supervisor Menu" → Decision: "Go back to: 
'01.0.0 - Idle Screen'" [User presses 'Sign Off' key.]
- Decision: "GPS Information available?" → Screen: "09.2.0 Supervisor Menu - GPS Information" [Yes]
- Decision: "GPS Information available?" → Screen: "09.2.1 Supervisor Menu - GPS Information - Error" [No]
- Screen: "09.2.1 Supervisor Menu - GPS Information - Error" → Decision: "Go back to: 
'09.0.0 Supervisor Menu'" [User presses 
'Go Back' key.]
- Screen: "09.2.0 Supervisor Menu - GPS Information" → Decision: "Go back to: 
'09.0.0 Supervisor Menu'" [User presses 
'Go Back' key.]
- Screen: "09.1.0 Supervisor Menu - Force Communications" → Decision: "Displayed information is updated." [User presses 
'Refresh' key.]
- Screen: "09.1.0 Supervisor Menu - Force Communications" → Decision: "A manifest update check will be performed." [User presses 
'Force Comms' key.]
- Screen: "09.1.0 Supervisor Menu - Force Communications" → Decision: "Go back to: 
'09.0.0 Supervisor Menu'" [User presses 
'Go Back' key.]
- Screen: "11.1.0 - Restarting" → Decision: "Device will reboot and return to:
'01.0.0 - Idle Screen'"
- Screen: "08.9.6 - ETM Soft Reboot" → Screen: "11.1.0 - Restarting" [User presses Reboot' key.]


## 10. Technician

### Screens (36)
- 10.0.0 - Technician Menu
- 10.1.0 - Technician - Device Settings
- 10.1.2 - Technician - Device Settings - Edit Home Location
- 10.1.3 - Technician - Device Settings - Home location not available
- 10.1.1 - Technician - Device Settings - Edit Input Field
- 10.1.1.2 - Technician - Device Settings -Confirm Input
- 01.9 - Please Wait...
- 10.2.0 - Technician - Display Settings
- 01.9 - Please Wait...
- 10.5.0 - Technician - Force Communications
- 08.9.6 - ETM Soft Reboot
- 11.1.0 - Restarting
- 10.8.0 - Technician Menu - Decommissioning
- 10.8.1 - Technician Menu - Decommissioning Warning
- 10.4.0 - Technician - Network Settings
- 10.4.2 - Technician - Cellular Modem
- 10.4.1 - Technician - FEC1
- 10.4.1.1 - Technician - Edit IP Addresses
- 10.4.1.2 - Technician - IP Address changed
- 10.6.0 - Technician - Network Routing Table
- 10.7.0 - Technician Menu - Versions
- 10.7.1 - Technician - Serial Numbers
- 10.7.2 - Technician Menu - Software Versions
- 10.7.3 - Technician Menu - Configuration Versions
- 10.7.3.1 - Technician Menu - Configuration Versions - Page 2
- 10.3.0 - Technician - Device Status
- 10.3.4 - Technician - Paper Status
- 10.3.3 - Technician - Card Reader
- 10.3.3.1 - Technician - Card Reader - Smartcard Details
- 06.0.1.3 - FLU - Smartcard Top Up - Error - Remove Smartcard
- 01.9 - Please Wait...
- 10.3.2 - Technician - GPS Information
- 10.3.1 - Technician - Other Devices
- 08.9.1 - BV Device Selected
- 08.9.2 - BV Device Selected - Reboot?
- 08.9.3 - BV Device Selected - Summary

### Decision Points (35)
- Home Locations available?
- Go back to:  '10.1.0 - Technician - Device Settings'
- Has a change been made?
- Changes are applied. Go back to:  10.0.0 - Technician Menu'
- Go back to:  '10.1.0 - Technician - Device Settings'
- Go back to:  '10.0.0 - Technician Menu'
- Default settings are restored.
- Go back to:  '10.0.0 - Technician Menu'
- Displayed information is updated.
- A manifest update check will be performed.
- Go back to:  '10.0.0 - Technician Menu'
- Device will reboot and return to: '01.0.0 - Idle Screen'
- Go back to:  '10.0.0 - Technician Menu'
- Device will reboot and return to: '01.0.0 - Idle Screen'
- Go back to:  '10.0.0 - Technician Menu'
- Displayed information is refreshed.
- Go back to:  '10.0.0 - Technician Menu'
- Displayed information is refreshed.
- Displayed information is updated.
- Displayed information is refreshed.
- Go back to:  '10.0.0 - Technician Menu'
- Go back to:  '10.7.0 - Technician Menu - Versions'
- Was printing successful?
- Versions are printed. ETM remains on the same screen.
- 'Printer Error' screen in FLU section
- Go back to:  '10.0.0 - Technician Menu'
- Go back to:  '10.3.0 - Technician - Device Status'
- Paper feed is reversed and the ETM remains on:  '10.3.4 - Technician - Paper Status'
- Was printing successful?
- Versions are printed. ETM remains on the same screen.
- 'Printer Error' screen in FLU section
- Go back to:  '10.0.0 - Technician Menu'
- Smartcard Valid?
- Selected device will reboot.
- Go back to:  '01.0.0 - Idle Screen'

### Annotations / Spec Notes (31)
- Device Settings
- Up and Down arrows will allow the user to view more locations.
- After field has been edited, the user can confirm by pressing the 'Enter' key.
- Pressing confirm or cancel takes the user back to the Technician Menu with changes saved or canceled.
- Display Settings
- Brightness can be adjusted through the L2 and R2 keys and VOlume can be adjusted through the L4 and R4 keys.  Defaults can be restored through pressing R6
- Force Communications
- The user can refresh the screen through pressing R5 and can force communications through pressing R6. This will not take the user to a different screen.  'Go Back' key would be used to go back to the 'Technician Menu' screen.
- A please wait screen willbe displayed whilst the current Communications status is identified.
- Soft Reboot
- Decommissioning
- ===This function is pending design===
- "Go back" takes user back to the Technician Menu
- "Cancel" takes user back to the Technician Menu
- Network Settings
- The user can refresh the screen by pressing R6.
- 'Go Back' key would be used to go back to the 'Network Settings screen.  The 'Refresh key will refresh the information on this list.
- 'Go Back' key would be used to go back to the 'Network Settings screen.  The 'Refresh key will refresh the information on this list.
- The user can use the arrow keys to navigate between the cells. When a new cell is selected, the previous entry remains until the user clears it by using the 'C' button.
- Network Routing
- The user can refresh the screen by pressing R6.  'Go Back' key would be used to go back to the 'Technician Menu' screen.
- Versions
- 'Go Back' key would be used to go back to the 'Technician Menu' screen.
- 'Go Back' key would be used to go back to the 'Versions' screen.
- 'Go Back' key would be used to go back to the 'Versions' screen.
- 'Go Back' key would be used to go back to the 'Versions' screen.  'Down Arrow' key goes to '10.7.3.1 - Technician Menu - Configuration Versions - Page 2'
- Device Status
- The 'Reverse Paper Feed' key is used to reverse the paper back into the roll. This is useful for any excess paper or for trying to resolve jams in some cases.
- When a card is presented, the card status (Mini Statement) screen is displayed.  The user can also reboot the card reader from this screen by pressing R6. (The user stays on the same screen).  'Go Back' key would be used to go back to the 'Device Status' screen.
- 'Go Back' key would be used to go back to the 'Device Status' screen.
- Pressing R2-4 in this example would take the user to the screens seen in the Driver Menu - Driver Options flow cvering BV Devices.  'Go Back' key would be used to go back to the 'Device Status' screen.

### Connections / Flow (101)
- Screen: "10.0.0 - Technician Menu" → Screen: "10.1.0 - Technician - Device Settings" [Use presses 'Device Settings' key.]
- Screen: "10.0.0 - Technician Menu" → Screen: "10.2.0 - Technician - Display Settings" [User presses 'Display Settings' key.]
- Screen: "10.0.0 - Technician Menu" → Screen: "01.9 - Please Wait..." [User presses 'Force Comms' key.]
- Screen: "10.0.0 - Technician Menu" → Screen: "10.8.0 - Technician Menu - Decommissioning" [User presses 'Decommissioning' key.]
- Screen: "10.0.0 - Technician Menu" → Screen: "10.4.0 - Technician - Network Settings" [User presses 'Network Settings' key.]
- Screen: "10.0.0 - Technician Menu" → Screen: "10.6.0 - Technician - Network Routing Table" [User presses 'Network Routing' key.]
- Screen: "10.0.0 - Technician Menu" → Screen: "10.7.0 - Technician Menu - Versions" [User presses 'Versions' key.]
- Screen: "10.0.0 - Technician Menu" → Screen: "10.3.0 - Technician - Device Status" [User presses Device Status' key.]
- Screen: "10.1.0 - Technician - Device Settings" → Decision: "Home Locations available?" [User presses R2 'Home Locations' key.]
- Screen: "10.1.0 - Technician - Device Settings" → Screen: "10.1.1 - Technician - Device Settings - Edit Input Field" [User presses R4 'Tray ID' key.]
- Screen: "10.1.0 - Technician - Device Settings" → Decision: "Go back to: 
'10.0.0 - Technician Menu'"
- Screen: "10.1.1 - Technician - Device Settings - Edit Input Field" → Decision: "Has a change been made?" [User presses
 'Enter' key.]
- Screen: "10.1.1.2 - Technician - Device Settings -Confirm Input" → Decision: "Go back to: 
'10.0.0 - Technician Menu'" [User press the 'Cancel' key.]
- Decision: "Home Locations available?" → Screen: "10.1.2 - Technician - Device Settings - Edit Home Location" [Yes]
- Decision: "Home Locations available?" → Screen: "10.1.3 - Technician - Device Settings - Home location not available" [No]
- Screen: "10.1.1.2 - Technician - Device Settings -Confirm Input" → Screen: "01.9 - Please Wait..." [User presses 'Confirm' key.]
- Screen: "01.9 - Please Wait..." → Decision: "Changes are applied.
Go back to: 
10.0.0 - Technician Menu'"
- Screen: "10.1.2 - Technician - Device Settings - Edit Home Location" → Screen: "10.1.0 - Technician - Device Settings" [User presses
 'Go Back' key.]
- Decision: "Has a change been made?" → Screen: "10.1.1.2 - Technician - Device Settings -Confirm Input" [Yes]
- Screen: "10.1.2 - Technician - Device Settings - Edit Home Location" → Decision: "Has a change been made?" [User presses 'L1-L5 or R1-R6' 
key to select a location.]
- Screen: "10.1.2 - Technician - Device Settings - Edit Home Location" → Decision: "Has a change been made?"
- Decision: "Has a change been made?" → Decision: "Go back to: 
'10.1.0 - Technician - Device Settings'"
- Screen: "10.1.1 - Technician - Device Settings - Edit Input Field" → Decision: "Go back to: 
'10.0.0 - Technician Menu'" [User presses 'Go Back' key.]
- Screen: "10.1.3 - Technician - Device Settings - Home location not available" → Decision: "Go back to: 
'10.1.0 - Technician - Device Settings'" [User presses 'Go Back' key.]
- Screen: "10.2.0 - Technician - Display Settings" → Decision: "Default settings are restored." [User presses 'Restore Defaults' key.]
- Screen: "10.2.0 - Technician - Display Settings" → Decision: "Go back to: 
'10.0.0 - Technician Menu'" [User presses 'Go Back' key.]
- Screen: "10.5.0 - Technician - Force Communications" → Decision: "Go back to: 
'10.0.0 - Technician Menu'" [User presses 'Go Back' key.]
- Screen: "10.5.0 - Technician - Force Communications" → Decision: "Displayed information is updated." [User presses 'Refresh' key.]
- Screen: "10.5.0 - Technician - Force Communications" → Decision: "A manifest update check will be performed." [User presses 'Force Comms' key.]
- Screen: "01.9 - Please Wait..." → Screen: "10.5.0 - Technician - Force Communications"
- Decision: "A manifest update check will be performed." → Screen: "01.9 - Please Wait..."
- Decision: "Displayed information is updated." → Screen: "01.9 - Please Wait..."
- Screen: "10.0.0 - Technician Menu" → Screen: "08.9.6 - ETM Soft Reboot" [User presses 'Soft Reboot' key.]
- Screen: "08.9.6 - ETM Soft Reboot" → Decision: "Go back to: 
'10.0.0 - Technician Menu'" [User presses 'Go Back' key.]
- Screen: "08.9.6 - ETM Soft Reboot" → Screen: "11.1.0 - Restarting" [User presses 'Reboot' key.]
- Screen: "11.1.0 - Restarting" → Decision: "Device will reboot and return to:
'01.0.0 - Idle Screen'"
- Screen: "10.8.0 - Technician Menu - Decommissioning" → Screen: "10.8.1 - Technician Menu - Decommissioning Warning" [User presses
 'Decommission Device' Ket.]
- Screen: "10.8.0 - Technician Menu - Decommissioning" → Decision: "Go back to: 
'10.0.0 - Technician Menu'" [User presses 
'Go Back' key.]
- Screen: "10.8.1 - Technician Menu - Decommissioning Warning" → Decision: "Go back to: 
'10.0.0 - Technician Menu'" [User presses
 'Cancel' key.]
- Screen: "10.8.1 - Technician Menu - Decommissioning Warning" → Decision: "Device will reboot and return to:
'01.0.0 - Idle Screen'" [User presses 
'Yes' key.]
- Screen: "10.4.0 - Technician - Network Settings" → Screen: "10.4.2 - Technician - Cellular Modem" [User presses
 R2 'Cellular' key.]
- Screen: "10.4.0 - Technician - Network Settings" → Screen: "10.4.1 - Technician - FEC1" [User presses
 R3 'FEC1' key.]
- Screen: "10.4.0 - Technician - Network Settings" → Decision: "Displayed information is refreshed." [User presses
 'Refresh' key.]
- Screen: "10.4.0 - Technician - Network Settings" → Decision: "Go back to: 
'10.0.0 - Technician Menu'" [User presses
 'Go Back' key.]
- Screen: "10.4.2 - Technician - Cellular Modem" → Screen: "10.4.0 - Technician - Network Settings" [User presses
 'Go Back' key.]
- Screen: "10.4.1 - Technician - FEC1" → Screen: "10.4.0 - Technician - Network Settings" [User presses
 'Go Back' key.]
- Screen: "10.4.1 - Technician - FEC1" → Screen: "10.4.1.1 - Technician - Edit IP Addresses" [User presses
 'Change' key.]
- Screen: "10.4.1.1 - Technician - Edit IP Addresses" → Screen: "10.4.1.2 - Technician - IP Address changed" [User presses
 'Confirm' key.]
- Screen: "10.4.1.2 - Technician - IP Address changed" → Screen: "10.4.0 - Technician - Network Settings" [User presses
 'Confirm' key.]
- Screen: "10.4.1.1 - Technician - Edit IP Addresses" → Screen: "10.4.1 - Technician - FEC1" [User presses
 'Cancel' key.]
- Screen: "10.4.1.2 - Technician - IP Address changed" → Screen: "10.4.1 - Technician - FEC1" [User presses
 'Cancel' key.]
- Screen: "10.4.1 - Technician - FEC1" → Decision: "Displayed information is updated." [User presses
 'Refresh' key.]
- Screen: "10.4.2 - Technician - Cellular Modem" → Decision: "Displayed information is refreshed." [User presses
 'Refresh' key.]
- Screen: "10.6.0 - Technician - Network Routing Table" → Decision: "Go back to: 
'10.0.0 - Technician Menu'" [User presses 
'Go Back' key.]
- Screen: "10.6.0 - Technician - Network Routing Table" → Decision: "Displayed information is refreshed." [User presses
 'Refresh' key.]
- Screen: "10.7.0 - Technician Menu - Versions" → Screen: "10.7.1 - Technician - Serial Numbers" [User presses
 'Serial Numbers' key.]
- Screen: "10.7.0 - Technician Menu - Versions" → Screen: "10.7.2 - Technician Menu - Software Versions" [User presses
 'Software Versions' key.]
- Screen: "10.7.0 - Technician Menu - Versions" → Screen: "10.7.3 - Technician Menu - Configuration Versions" [User presses
 'Configuration Versions' key.]
- Screen: "10.7.0 - Technician Menu - Versions" → Decision: "Go back to: 
'10.0.0 - Technician Menu'"
- Screen: "10.7.3 - Technician Menu - Configuration Versions" → Screen: "10.7.3.1 - Technician Menu - Configuration Versions - Page 2" [User presses 
'Down' key.]
- Screen: "10.7.3.1 - Technician Menu - Configuration Versions - Page 2" → Screen: "10.7.3 - Technician Menu - Configuration Versions" [User presses 
'Up' key.]
- Screen: "10.7.1 - Technician - Serial Numbers" → Decision: "Go back to: 
'10.7.0 - Technician Menu - Versions'" [User presses 
'Go Back' key.]
- Screen: "10.7.2 - Technician Menu - Software Versions" → Decision: "Go back to: 
'10.7.0 - Technician Menu - Versions'" [User presses 
'Go Back' key.]
- Screen: "10.7.3 - Technician Menu - Configuration Versions" → Decision: "Go back to: 
'10.7.0 - Technician Menu - Versions'" [User presses 'Go Back' key.]
- Decision: "Was printing successful?" → Decision: "Versions are printed.
ETM remains on the same screen." [Yes]
- Decision: "Was printing successful?" → Decision: "'Printer Error' screen in FLU section" [No]
- Screen: "10.7.2 - Technician Menu - Software Versions" → Decision: "Was printing successful?" [User presses
 'Print' key.]
- Screen: "10.7.3 - Technician Menu - Configuration Versions" → Decision: "Was printing successful?" [User presses
 'Print' key.]
- Screen: "10.7.1 - Technician - Serial Numbers" → Decision: "Was printing successful?" [User presses
 'Print' key.]
- Screen: "10.7.3.1 - Technician Menu - Configuration Versions - Page 2" → Decision: "Was printing successful?" [User presses
 'Print' key.]
- Decision: "Was printing successful?" → Decision: "Versions are printed.
ETM remains on the same screen." [Yes]
- Decision: "Was printing successful?" → Decision: "'Printer Error' screen in FLU section" [No]
- Screen: "10.3.0 - Technician - Device Status" → Screen: "10.3.4 - Technician - Paper Status" [User presses 
'Printer/Paper' key.]
- Screen: "10.3.0 - Technician - Device Status" → Screen: "10.3.3 - Technician - Card Reader" [User presses 
'Card Reader' key.]
- Screen: "10.3.0 - Technician - Device Status" → Screen: "10.3.2 - Technician - GPS Information" [User presses 
'GPS' key.]
- Screen: "10.3.0 - Technician - Device Status" → Screen: "10.3.1 - Technician - Other Devices" [User presses 
'Other Devices' key.]
- Screen: "10.3.4 - Technician - Paper Status" → Decision: "Paper feed is reversed and the ETM remains on: 
'10.3.4 - Technician - Paper Status'" [User presses 
'Reverse Paper Feed' key.]
- Screen: "10.3.4 - Technician - Paper Status" → Decision: "Was printing successful?" [User presses 
'Print Test Ticket' key.]
- Screen: "10.3.4 - Technician - Paper Status" → Decision: "Go back to: 
'10.3.0 - Technician - Device Status'"
- Screen: "10.3.3 - Technician - Card Reader" → Decision: "Go back to: 
'10.3.0 - Technician - Device Status'"
- Screen: "10.3.3 - Technician - Card Reader" → Screen: "01.9 - Please Wait..." [User presses 
'Reboot' key.]
- Screen: "01.9 - Please Wait..." → Decision: "Go back to: 
'10.3.0 - Technician - Device Status'"
- Screen: "10.3.3 - Technician - Card Reader" → Decision: "Smartcard Valid?" [User presents 
a smartcard.]
- Screen: "10.3.3.1 - Technician - Card Reader - Smartcard Details" → Screen: "06.0.1.3 - FLU - Smartcard Top Up - Error - Remove Smartcard" [User presses 
'Reboot' key.]
- Screen: "06.0.1.3 - FLU - Smartcard Top Up - Error - Remove Smartcard" → Decision: "Go back to: 
'10.3.0 - Technician - Device Status'" [User removes
 smartcard.]
- Screen: "10.3.3.1 - Technician - Card Reader - Smartcard Details" → Decision: "Go back to: 
'10.3.0 - Technician - Device Status'" [User removes
 smartcard.]
- Screen: "10.3.2 - Technician - GPS Information" → Decision: "Go back to: 
'10.3.0 - Technician - Device Status'" [User press
 'Go Back' key.]
- Screen: "08.9.1 - BV Device Selected" → Screen: "08.9.3 - BV Device Selected - Summary" [User presses 
'Summary' key.]
- Screen: "08.9.1 - BV Device Selected" → Screen: "08.9.2 - BV Device Selected - Reboot?" [User presses 
'Reboot' key.]
- Screen: "08.9.3 - BV Device Selected - Summary" → Screen: "08.9.1 - BV Device Selected" [User presses 'Cancel Key.]
- Screen: "08.9.2 - BV Device Selected - Reboot?" → Screen: "08.9.1 - BV Device Selected" [User presses 
'Cancel' key.]
- Screen: "08.9.2 - BV Device Selected - Reboot?" → Decision: "Selected device will reboot." [User presses 
'Reboot' key.]
- Screen: "10.3.1 - Technician - Other Devices" → Screen: "08.9.1 - BV Device Selected"
- Screen: "10.3.1 - Technician - Other Devices" → Screen: "08.9.1 - BV Device Selected" [User presses
'R2-4' key.]
- Screen: "10.3.1 - Technician - Other Devices" → Screen: "08.9.1 - BV Device Selected"
- Screen: "08.9.1 - BV Device Selected" → Screen: "10.3.1 - Technician - Other Devices" [User presses 
'Go Back' key.]
- Screen: "10.3.1 - Technician - Other Devices" → Screen: "10.3.0 - Technician - Device Status"
- Screen: "10.3.0 - Technician - Device Status" → Decision: "Go back to: 
'10.0.0 - Technician Menu'" [User presses
 'Go Back' key.]
- Decision: "Smartcard Valid?" → Screen: "10.3.3.1 - Technician - Card Reader - Smartcard Details" [Yes]
- Decision: "Smartcard Valid?" → Screen: "06.0.1.3 - FLU - Smartcard Top Up - Error - Remove Smartcard" [No]
- Screen: "10.0.0 - Technician Menu" → Decision: "Go back to: 
'01.0.0 - Idle Screen'"


## 11. Displays LEDs and Audio Tones

### Screens (29)
- 0.1.1.1 - Out of Service
- 0.1.1.2 - Please Wait
- 0.1.1.3 - See Driver
- 0.1.1.4 - Boarding
- 0.1.1.5 - Transaction Success
- PID/Info/Printer Firmware
- PID/Info/Out of Service
- PID/Info/Please Wait
- PID/Info/See Driver
- PID/FLU/Selection
- PID/FLU/TicketIssue
- PID/FLU/Product Issue
- PID/FLU/Pass Issue
- PID/FLU/Basket
- PID/FLU/Basket Issue
- PID/Smartcard/Present
- PID/Smartcard/Success
- PID/Smartcard/Single
- PID/Smartcard/Inspector
- PID/Smartcard/Operator
- PID/ABT/Success
- CardReader/Inactive
- CardReader/LEDGNNN
- CardReader/LEDGGNN
- CardReader/LEDGGGN
- CardReader/LEDGGGG
- CardReader/LEDNNAN
- CardReader/LEDGNAN
- CardReader/LEDNNNR

### Decision Points (0)

### Annotations / Spec Notes (0)

### Connections / Flow (0)


## 12. Barcode Scanning

### Screens (22)
- 02.0.0 | FLU Home
- 08.0.0 Driver Menu
- 12.0.0 - Barcode Reference
- 12.0.1 - Barcode Reference Entered
- 12.1.0 - Barcode Validation Failed
- 12.2.0 - Barcode - Validating Details
- 12.2.1 - Barcode - Offline Check
- 12.5.2 - Barcode Scan - Ticket Valid inc_ Date with Expiry and Depart Time
- 12.5.3 - Barcode Scan - Ticket Valid inc_ Outbound ands Return
- 12.5.4 - Barcode Scan - Ticket Valid inc_ 3 Use Times
- 12.5.1 - Barcode Scan - Ticket Valid inc. Date and Depart Time
- 12.5.3.1 - Barcode Scan - Ticket Valid inc_ Outbound ands Return - Page 2
- 12.5.4.1 - Barcode Scan - Ticket Valid inc_ 3 Use Times - Page 2
- 12.1.1 - Barcode Scan - Transaction Cancelled - Ticket Not Valid
- 12.1.2 - Barcode Scan - Transaction Cancelled - Ticket Not Passed Visual Inspection
- 12.4.1 - Barcode Ticket - Print Error
- 12.4.0 - Barcode Ticket - Printed?
- 12.1.0 - Barcode Validation Failed
- 12.1.1 - Barcode Scan - Transaction Cancelled - Ticket Not Valid
- 12.2.0 - Barcode - Validating Details
- 12.5.1 - Barcode Scan - Ticket Valid inc. Date and Depart Time
- 12.1.2 - Barcode Scan - Transaction Cancelled - Ticket Not Passed Visual Inspection

### Decision Points (19)
- Barcode Data successfully received?
- Barcode Reference  correct and/or valid?
- Decryption & parsing successful?
- Back to the FLU screen
- Back to the FLU screen
- Is the barcode already offline validated?
- Online check available?
- Valid Barcode?
- Ticket value less than or  equal to the configurable limit &  the product is valid?
- Passed additional  background checks?
- Online?
- Back to the FLU screen
- Successful Print?
- Customer presents mLink Ticket and Operator scans.
- Back to the FLU screen
- Offline validation possible  using encryption keys?
- Is the date valid?
- Back to the FLU screen
- Back to the FLU screen.

### Annotations / Spec Notes (6)
- Barcode Scan Validation
- This flow will be finalised upon reviewing the Corethree Barcode Approach post R2.0. Multi-use barcodes will also be reviewed post R2.0.
- Accessing Barcode Ref. via Driver menu
- Errors could be be: - Barcode decryption has failed. - The ticket is not valid - The ticket has already been used - The ticket is not valid on this date - The ticket has expired - The ticket value exceeds offline validation limit.  The operator can input a barcode reference by press the option in the Driver Menu.
- Ticket Validation screen examples
- mLink Scan Validation

### Connections / Flow (58)
- Decision: "Barcode Data successfully received?" → Screen: "12.2.0 - Barcode - Validating Details" [Yes]
- Screen: "02.0.0 | FLU Home" → Decision: "Barcode Data successfully received?" [Barcode is scanned]
- Decision: "Barcode Data successfully received?" → Screen: "12.1.0 - Barcode Validation Failed" [No]
- Screen: "12.2.0 - Barcode - Validating Details" → Decision: "Decryption & parsing successful?"
- Decision: "Decryption & parsing successful?" → Screen: "12.1.0 - Barcode Validation Failed" [No]
- Decision: "Is the barcode already offline validated?" → Screen: "12.1.0 - Barcode Validation Failed" [Barcode has already been validated offline]
- Decision: "Valid Barcode?" → Screen: "12.1.1 - Barcode Scan - Transaction Cancelled - Ticket Not Valid" [No]
- Decision: "Ticket value less than or 
equal to the configurable limit &
 the product is valid?" → Screen: "12.1.0 - Barcode Validation Failed" [No]
- Screen: "12.2.1 - Barcode - Offline Check" → Decision: "Ticket value less than or 
equal to the configurable limit &
 the product is valid?"
- Decision: "Online check available?" → Decision: "Valid Barcode?" [Yes]
- Decision: "Passed additional
 background checks?" → Screen: "12.1.1 - Barcode Scan - Transaction Cancelled - Ticket Not Valid" [No]
- Decision: "Passed additional
 background checks?" → Screen: "12.5.1 - Barcode Scan - Ticket Valid inc. Date and Depart Time" [Yes]
- Decision: "Valid Barcode?" → Decision: "Passed additional
 background checks?" [Yes]
- Screen: "12.5.1 - Barcode Scan - Ticket Valid inc. Date and Depart Time" → Screen: "12.1.2 - Barcode Scan - Transaction Cancelled - Ticket Not Passed Visual Inspection" [User press 
'Not Valid' key.]
- Screen: "12.5.1 - Barcode Scan - Ticket Valid inc. Date and Depart Time" → Decision: "Online?" [User press 
'Valid' key.]
- Decision: "Online?" → Decision: "Successful Print?" [No -Store offline validation in the background]
- Decision: "Online?" → Decision: "Successful Print?" [Yes - Operator prints a travel ticket.]
- Decision: "Successful Print?" → Screen: "12.4.1 - Barcode Ticket - Print Error" [No]
- Decision: "Successful Print?" → Screen: "12.4.0 - Barcode Ticket - Printed?" [Yes]
- Screen: "12.4.1 - Barcode Ticket - Print Error" → Screen: "12.5.1 - Barcode Scan - Ticket Valid inc. Date and Depart Time" [User presses 'Retry' key.]
- Screen: "12.1.2 - Barcode Scan - Transaction Cancelled - Ticket Not Passed Visual Inspection" → Decision: "Back to the FLU screen" [User press 'Go Back' key.]
- Screen: "12.4.1 - Barcode Ticket - Print Error" → Decision: "Back to the FLU screen" [User presses 'Cancel' key.]
- Screen: "12.4.0 - Barcode Ticket - Printed?" → Decision: "Successful Print?" [User presses
 'No' key.]
- Decision: "Decryption & parsing successful?" → Decision: "Is the barcode already offline validated?" [Yes]
- Decision: "Is the barcode already offline validated?" → Decision: "Online check available?" [Barcode has NOT already been validated offline]
- Screen: "12.1.0 - Barcode Validation Failed" → Screen: "12.2.0 - Barcode - Validating Details" [User presses 'Retry' key.]
- Screen: "12.1.0 - Barcode Validation Failed" → Decision: "Back to the FLU screen" [User presses 'Cancel' key.]
- Decision: "Online check available?" → Screen: "12.2.1 - Barcode - Offline Check" [No
]
- Screen: "08.0.0 Driver Menu" → Screen: "12.0.0 - Barcode Reference"
- Screen: "12.0.0 - Barcode Reference" → Screen: "12.0.1 - Barcode Reference Entered" [User  enters Barcode reference ID.]
- Screen: "12.0.1 - Barcode Reference Entered" → Decision: "Back to the FLU screen" [User presses
 'Cancel' key.]
- Screen: "12.0.1 - Barcode Reference Entered" → Decision: "Barcode Reference 
correct and/or valid?" [User presses
 'Continue' key.]
- Decision: "Barcode Reference 
correct and/or valid?" → Screen: "12.1.0 - Barcode Validation Failed" [No]
- Decision: "Barcode Reference 
correct and/or valid?" → Screen: "12.2.0 - Barcode - Validating Details" [Yes]
- Screen: "12.5.3 - Barcode Scan - Ticket Valid inc_ Outbound ands Return" → Screen: "12.5.3.1 - Barcode Scan - Ticket Valid inc_ Outbound ands Return - Page 2"
- Screen: "12.5.3.1 - Barcode Scan - Ticket Valid inc_ Outbound ands Return - Page 2" → Screen: "12.5.3 - Barcode Scan - Ticket Valid inc_ Outbound ands Return"
- Screen: "12.5.4 - Barcode Scan - Ticket Valid inc_ 3 Use Times" → Screen: "12.5.4.1 - Barcode Scan - Ticket Valid inc_ 3 Use Times - Page 2"
- Screen: "12.5.4.1 - Barcode Scan - Ticket Valid inc_ 3 Use Times - Page 2" → Screen: "12.5.4 - Barcode Scan - Ticket Valid inc_ 3 Use Times"
- Screen: "02.0.0 | FLU Home" → Screen: "08.0.0 Driver Menu"
- Screen: "08.0.0 Driver Menu" → Screen: "02.0.0 | FLU Home"
- Decision: "Ticket value less than or 
equal to the configurable limit &
 the product is valid?" → Screen: "12.5.1 - Barcode Scan - Ticket Valid inc. Date and Depart Time" [Yes]
- Screen: "12.1.1 - Barcode Scan - Transaction Cancelled - Ticket Not Valid" → Decision: "Back to the FLU screen" [User presses 'Cancel' key.]
- Screen: "12.0.0 - Barcode Reference" → Decision: "Back to the FLU screen" [User presses 
'Cancel' key.]
- Screen: "12.1.1 - Barcode Scan - Transaction Cancelled - Ticket Not Valid" → Decision: "Is the barcode already offline validated?" [User presses
 'Retry key.]
- Screen: "12.4.0 - Barcode Ticket - Printed?" → Decision: "Back to the FLU screen" [User presses
 'Yes' key.]
- Decision: "Offline validation possible 
using encryption keys?" → Screen: "12.1.0 - Barcode Validation Failed" [No]
- Decision: "Offline validation possible 
using encryption keys?" → Decision: "Is the date valid?" [Yes]
- Decision: "Is the date valid?" → Screen: "12.1.1 - Barcode Scan - Transaction Cancelled - Ticket Not Valid" [No]
- Decision: "Is the date valid?" → Screen: "12.2.0 - Barcode - Validating Details" [Yes]
- Screen: "12.2.0 - Barcode - Validating Details" → Screen: "12.5.1 - Barcode Scan - Ticket Valid inc. Date and Depart Time"
- Screen: "12.5.1 - Barcode Scan - Ticket Valid inc. Date and Depart Time" → Screen: "12.1.2 - Barcode Scan - Transaction Cancelled - Ticket Not Passed Visual Inspection" [User presses
'Not Valid' key.]
- Decision: "Customer presents mLink Ticket and Operator scans." → Decision: "Offline validation possible 
using encryption keys?"
- Screen: "12.1.0 - Barcode Validation Failed" → Decision: "Offline validation possible 
using encryption keys?" [User presess
 'Retry' key.]
- Screen: "12.1.0 - Barcode Validation Failed" → Decision: "Back to the FLU screen." [User presess
 'Cancel' key.]
- Screen: "12.1.1 - Barcode Scan - Transaction Cancelled - Ticket Not Valid" → Decision: "Back to the FLU screen." [User presess
 'Cancel' key.]
- Screen: "12.1.1 - Barcode Scan - Transaction Cancelled - Ticket Not Valid" → Decision: "Offline validation possible 
using encryption keys?" [User presess
 'Retry' key.]
- Screen: "12.1.2 - Barcode Scan - Transaction Cancelled - Ticket Not Passed Visual Inspection" → Decision: "Back to the FLU screen." [User presses 
'Go Back' key]
- Screen: "12.5.1 - Barcode Scan - Ticket Valid inc. Date and Depart Time" → Decision: "Back to the FLU screen." [User presses
'Valid' key.]


## 13. Power Interruption

### Screens (3)
- 11.0.0 - Power Interruption
- 11.1.0 - Restarting
- 11.2.0 - Charging

### Decision Points (0)

### Annotations / Spec Notes (5)
- Power Interruption
- Power Interruption occurs when the device loses power. It does have backup, but only for a very small period of time. Care has been taken t ensure that any timeouts before shutting down will be enough to save the system state safely.
- If the power is interrupted for a longer time, this screen wil display.  The system is shutting down once this state is reached.
- This screen appears on boot to ensure the device has enough charge to successfully allow the state to be saved in the event of a power interruption.
- This screen appears when power is interrupted.  If the power is interrupted temporarily, the device will take the user back to the screen they were originally on.

### Connections / Flow (0)


## 14. Revenue Limit

### Screens (2)
- 02.9 | Main Screen - Revenue Limit Approaching
- 02.9.1 - Main Screen - Revenue Limit Reached

### Decision Points (0)

### Annotations / Spec Notes (3)
- Revenue Limit
- Once max revenue is reached, the Driver will be automatically signed-off, a waybill will be printed and the ETM wil lock. A supervisor or Technician will need to be notified.  ETM will need to retrieve the connection with the back office. This is done in the background.
- Notification at the header is presented when a pre-configured amount is approaching.  The baner will appear after a 'Transaction Complete' banner disapears, then disapear after 3 seconds.

### Connections / Flow (0)


---

# Additional Boards (not in main navigation list — drafts/hidden)


## Driver Menu / Options (Old layout draft) (extra/draft board)

### Screens (38)
- 08.0.0 Driver Menu
- 08.0.1 - Inspector - Present Smartcard
- 08.0.2 - Driver Menu - Annulment - Top Up
- 08.0.3 - Driver Menu - Annulment - Tickets
- 08.0.4 - Driver Menu - Annulment - yLink
- 08.0.5 - Open Tickets
- 01.1.6 -Sign Off?
- 08.0.6 -New Trip - Select New Route
- 08.0.7 - Idle Screen - On Break/Black
- 08.0.1.1 - Inspector - Invalid Smartcard
- 08.0.2.1 - Annulment - Present Smartcard
- 08.0.3.1 - Driver Menu - Annulment Successful
- 08.0.3.2 - Driver Menu - Annulment Unsuccessful
- 08.0.5.1 - Excess Ticket
- 01.9 - Please Wait...
- 08.0.7.1 - Incorrect Smartcard
- 08.0.2.2 - Driver Menu - Annulment Successful - Smartcard
- 08.0.2.3 - Driver Menu - Annulment unsuccessful - Incorrect Card
- 08.0.5.2 - Excess Ticket - Error
- 08.1.0 - Driver Options
- 08.2.0 - Driver Menu - Ticket History
- 08.3.0 - Driver Menu - Duty Totals
- 08.4.0 - Driver Menu - Display Settings - Brightness and Volume
- 08.5.0 - Driver Menu - Paper Status
- 08.6.0 - Driver Menu - Word and Colour of the Day
- 08.7.0 - Driver Menu - Messages
- 08.9.0 - Driver Menu - BV Devices
- 08.9.6 - ETM Soft Reboot
- 08.9.7 - BV Device Selected - Reboot?
- 08.2.1 - Driver Menu - Ticket History - View Ticket
- 08.3.1 - Driver Menu - Journey Totals
- 08.9.1 - BV Device Selected
- 08.9.2 - BV Device Selected - Reboot?
- 08.9.3 - BV Device Selected - Summary
- 08.10.1 - Report Faulty Device?
- 08.10.3 - Faulty Device Already Reported
- 08.10.2 - Driver Menu - Driver Faulty Device
- 08.10.4 - Main Screen - FLU - Faulty Device

### Decision Points (0)

### Annotations / Spec Notes (0)

### Connections / Flow (0)


## FLU 2.0 Ticket Issuance (extra/draft board)

### Screens (6)
- 02.0.0 | FLU Home
- 00.0.0 | Adult Single - Issuance - Alighting Selected
- 2.5 | Main Screen - Last Transaction 200 - Success
- 2.5.1 | Main Screen - Last Transaction 200
- 02.0.5 | Easibus
- 00.0.0 | Child Single - Issuance - Alighting Selected

### Decision Points (5)
- Ticket Is Issued
- Transaction Success Tone played
- Easibus Route?
- Unexpected  Printer Event?
- Printer Error Flow

### Annotations / Spec Notes (1)
- The following screens will represent a route with the following stages:  Route 10F (IN) 10115 Lagmore View 10102 Lagmore Dale 10862 Twinbrook Rd 10113 Bell Steele Road 10371 Pantridge Road 10110 Woodbourne Suffolk Rd 10111 Saint Teresa's 10112 Glen Parade 9041 City Cemetery 9037 Royal Hospitals 9034 Divis Tower 10867 Wellington Place (Queen St)

### Connections / Flow (22)
- Screen: "02.0.0 | FLU Home" → Screen: "00.0.0 | Adult Single - Issuance - Alighting Selected"
- Screen: "00.0.0 | Adult Single - Issuance - Alighting Selected" → Decision: "Easibus Route?"
- Decision: "Easibus Route?" → Screen: "02.0.5 | Easibus" [Yes]
- Screen: "02.0.5 | Easibus" → Screen: "02.0.0 | FLU Home" [User selects 'Cancel']
- Decision: "Easibus Route?" → Decision: "Ticket Is Issued" [No]
- Screen: "02.0.5 | Easibus" → Decision: "Ticket Is Issued"
- Screen: "02.0.5 | Easibus" → Decision: "Ticket Is Issued"
- Screen: "02.0.5 | Easibus" → Decision: "Ticket Is Issued"
- Screen: "02.0.5 | Easibus" → Decision: "Ticket Is Issued"
- Screen: "02.0.5 | Easibus" → Decision: "Ticket Is Issued"
- Screen: "02.0.5 | Easibus" → Decision: "Ticket Is Issued"
- Screen: "02.0.5 | Easibus" → Decision: "Ticket Is Issued"
- Screen: "02.0.5 | Easibus" → Decision: "Ticket Is Issued" [User selects any available option]
- Screen: "00.0.0 | Adult Single - Issuance - Alighting Selected" → Screen: "02.0.0 | FLU Home" [Screen Timeouth]
- Decision: "Ticket Is Issued" → Decision: "Unexpected 
Printer Event?"
- Screen: "2.5 | Main Screen - Last Transaction 200 - Success" → Screen: "2.5.1 | Main Screen - Last Transaction 200" [X seconds timeout]
- Decision: "Unexpected 
Printer Event?" → Decision: "Transaction Success Tone played" [No]
- Decision: "Unexpected 
Printer Event?" → Decision: "Printer Error Flow" [Paper Slip]
- Decision: "Unexpected 
Printer Event?" → Decision: "Printer Error Flow" [Paper Out]
- Decision: "Unexpected 
Printer Event?" → Decision: "Printer Error Flow" [Paper Jam]
- Decision: "Unexpected 
Printer Event?" → Decision: "Printer Error Flow" [Printer Disconnect]
- Decision: "Transaction Success Tone played" → Screen: "2.5 | Main Screen - Last Transaction 200 - Success"
