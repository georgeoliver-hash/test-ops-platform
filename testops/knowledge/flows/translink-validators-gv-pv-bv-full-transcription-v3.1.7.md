# Translink Validators v3.1.7 (GV / PV / BV) — Full Flow Transcription

Source: Overflow.io project "Translink Validators 3.1.7" (https://overflow.io/s/9LR2K30N/)
Covers: Gate Validator (GV), Platform Validator (PV), and Bus Validator (BV, in an older/extra board).
Extracted: full text content of all boards — screen titles, decision points, annotations/spec notes, and screen-to-screen connections.
Note: This document captures TEXT content and FLOW STRUCTURE only. It does not include the actual visual mockup images (screens are referenced by their title/ID only).

## Board Index (main navigation order)
1. Welcome Page
2. Gate Validator Flows
3. Technician Menu - Gate
4. Platform Validator-Barcode
5. Technician Menu - Platform Validator

---


## 1. Welcome Page

### Screens (0)

### Decision Points (0)

### Annotations / Spec Notes (6)
- Welcome Page
- Version: 3.1.7
- Validators Figma Project
- Please see Figma project for the individual screens: Link
- Validators User Flows Contents
- 1. Welcome Page 2. Gate Validator Flows 3. Technician Menu - Gate 4. Platform Validator - Barcode Flow 5. Technician Menu - Platform Validator

### Connections / Flow (0)


## 2. Gate Validator Flows

### Screens (57)
- Initialisation
- Template -Validator Prompt
- Template - Validator Response
- Icons
- Status-Colours
- BiDirectionalMode/Validation/Entry
- BiDirectionalMode/InService
- 1.1.0 Present SmartCard no Tickets
- BiDirectionalMode/Error/Entry
- 0.0 Loading
- 1.0.1 Present SmartCard or Barcode
- 1.1.1 Present Ticket no SmartCard
- 1.2.8 Machine Not in Service (Gate)
- 1.2.10 Machine Not Commissioned (Gate)
- 1.6.1.1 ABT Tag successful
- BiDirectionalMode/InService/Card Only
- 1.6.3 ABT Error reading card
- 1.6.2 ABT deny list/negative list
- 1.4.9 Passback - No Entry
- BiDirectionalMode/Validation/Exit
- 1.2.5 Please Proceed
- 1.2.4 Emergency Exit
- 1.2.5 Please Proceed
- 1.2.6 No Entry
- 1.2.9 Bi-directional screen
- 1.5.0 Tag successful
- 1.6.4 ABT Hot listed card
- 1.3.7 Not Valid At This Location
- 1.3.8 Invalid Time Of Day
- 1.3.9 Product Expired
- 1.3.1 Represent Card
- 1.7.1.1 Barcode Validation Successful - Adult
- BiDirectionalMode/Error/Exit
- BiDirectionalMode/InService/Code Only
- 1.3.16 Unable to Validate
- 1.7.99.3 Barcode Validation Fail - Time
- 1.7.99.2 Barcode Validation Fail - Service
- 1.7.99.4 Barcode Validation Fail - Location
- 1.7.99.5 Barcode Validation Fail - Expired
- 1.7.99.1 Barcode Validation Fail - Passback
- EntryMode/Validation/Success
- EntryMode/InService
- EntryMode/Validation/Fail
- EntryMode/InService/CardOnly
- EntryMode/InService/Code Only
- ExitMode/InService
- ExitMode/Validation/Success
- ExitMode/Validation/Fail
- ExitMode/InService/CardOnly
- ExitMode/InService/Code Only
- EmergencyMode
- FullyFree/Idle
- FullyFree/Traverse
- ClosedMode/NotInService
- TechMode/Primary
- TechMode/Secondary
- TechMode/Both

### Decision Points (131)
- Location ID
- Company Logo
- Status Icon
- Status Bar as above
- Time (24 hour clock)
- PlinthID / DeviceID / Sublocation ID
- Device boots into mode X
- Bi-Directional
- Date
- Zone Name
- Background colour representing the response communicated.  Eg, Green:Success / Red:Failure / Amber:Warning
- Powered Off
- Main update message.  Eg. Validation Success /Failure
- Icon indicating where the card/barcode readers are.
- Prompt to present media type. Can be either/or both Card/Barcode depending on reader availability
- Loading
- Optional sub-message Up to two lines of text often providing directions or further information.
- Degraded Message
- Primary Path
- In-Service/Awaiting Validation
- Ingress Permitted
- Secondary Path
- Please Wait
- Error Path
- Ingress/Validation Declined
- Techncian Mode
- Timeout
- Card or Barcode is valid?
- No Response
- Fault is corrected
- Is device commissioned  and fully operational?
- A device fault has occurred
- Device is powered on
- Travel Card or Barcode presented to Primary Reader
- Device reboots in an attempt to recover the reader
- Is Validator/Plinth Commissioned?
- Card Type
- Sub-Product Type
- Local Rail
- Cross Border
- Free Smartpass
- Blind Smartpass
- Blind Single
- Blind XB Single Blind XB Day Return Blind XB 1 Mth Return
- Travel Card or Barcode presented to Secondary Reader
- Reader becomes  unavailable?
- Half-Fare Smartpass
- Partially Sighted
- Part Sight Single Part Sight Return
- N/A – not accepted for Rail Cross Border travel
- Smartcard or Barcode is presented to reader
- Is presented card readable?
- Is the presented  smartcarda Legacy miFare or  ABT EMV?
- ABT Valid AID?
- ABT Card is Expired?
- ABT ODA Valid?
- ABT Is PAN  on BIN list?
- ABT PAN on Deny List?
- ABT Has PAN been used within Passback Period?
- Card or Barcode is valid?
- Gate has been  remotely change to  "Fully Free" mode?
- Gate has changed  to Emergency mode
- Gate has changed  to Entry Mode
- Gate has changed  to Exit Mode
- Gate has changed  to Locked Mode
- Gate has opened due to passenger activity?
- Has device been put out of service?
- No Response
- Device is Primary? (Unsecured side)
- Device is Primary? (Unsecured side)
- Device is Primary? (Unsecured side)
- Is Gate Bi-Directional?
- Which direction is Gate opening?
- Smartcard Is smartcard an  operator card?
- Does Operator ID match a Technician ID in Stafflist?
- See "Technician Menu - Gate" board for Technician Sign-on.
- Device will not respond
- Smartcard Is card blocked?
- Smartcard Is card on the Actionlist?
- Smartcard Is smartcard product valid for current location?
- Smartcard Is smartcard valid at current time/date?
- Smartcard Is smartcard expired?
- Smartcard Is smartcard within Passback period?
- Smartcard Is smartcard within transfer period?
- Smartcard Was Smartcard validation record successfully updated?
- No Response
- Barcode Is barcode readable?
- Barcode Is barcode valid on current route/service?
- Barcode Is barcode valid at current date/time
- Barcode Is barcode valid at current location?
- Barcode Is barcode expired?
- Barcode Has Barcode been used within Passback Period?
- No Response
- Entry Mode
- Card or Barcode is valid?
- Travel Card or Barcode presented to Primary Reader
- No Response
- Travel Card or Barcode presented to Secondary Reader
- Reader becomes  unavailable?
- No Response
- No Response
- Exit Mode
- Travel Card or Barcode presented to Primary Reader
- No Response
- No Response
- Card or Barcode is valid?
- Reader becomes  unavailable?
- Travel Card or Barcode presented to Secondary Reader
- No Response
- Emergency Mode
- Passenger ingress is detected on either  Side A or Side B
- No Response
- Travel Card or Barcode presented to Either Reader
- Free Entry Mode
- Passenger has been detected to have degressed
- Passenger ingress is detected on either  Side A or Side B
- Travel Card or Barcode presented to Either Reader
- No Response
- No Response
- No Response
- Closed Mode
- Unexpected passenger ingress is detected on Side A
- unexpected passenger ingress is detected on Side B
- Travel Card or Barcode presented to Either Reader
- No Response
- No Response
- Technician Mode
- Valid Technician Card is Presented to Primary Validator
- For sign-on and Technician menus see "Technician Menu gate" board
- Valid Technician Card is Presented to Secondary Validator
- Valid Technician Card is Presented to both validators

### Annotations / Spec Notes (19)
- Gate and Validators
- LEDs
- Screen Templates
- Axio4-PMV LED
- Card-Reader LEDs
- The Axio4-PMV LED is positioned above the main display and can display appropriate colours depending on the activity of the device. These are as  follows:
- The FEIG card reader can display a number of different configurations of illuminated LED according to the FEIG documentation: (SEE LINK)  General rule though is that: * Any configuration of only-green LEDs means the reader is available for validation * Any configuration inlcuding an Amber LED means the device is "Not Ready" * Any configuration including a RED LED means a fault has occurred.
- Line Legend
- Validator Present X Template  The default layout used for a validator that is in-service and actively validating presented media.
- Validator Response Template  This basic layout is used for all status updates inclusive of gate mode changes, validation results and faults
- ...
- ...
- Audio Tones
- Validator - Validation Audio Tones
- The gate validators will typically play one of two audible tones in response to a validation:  - Success.wav                                                       - Played on a successful validation of either Card or Barcode  - Error.wav                                                            - Played on a validation failure The validator will also play a "timeout.wav" tone when Technician mode timeouts occur.  The gate itself will play some audio tones to alert of obstructions or to warn that the gates are closing.
- Validator - Audio Messages
- In addition to the above the following Audio Messages can be played: - Please_Proceed.wav                                          - Played on a validation success/passback of either card or barcode - Please_try_again_or_seek_assistance.wav    - Played on a "Please Try Again" screen - Please_Seek_assistance.wave                         - Played on a validation failure. (Eg. Hotlisted/Faulty/Product Expired)  Audible messages will only play for the following:
- Typically an uncommissioned device will have an unprogrammed Plinth-ID so it would be expected that the Status Bar may not have programmed values to display for Gate ID / Device ID / Sub Location or the Location.  Device will require comms and a Technician to sign-in and program the Location details
- For all barcodes that have an expiry time between 00:00 and 04:00 the PV will need to display the previous day (as the expiry date) on the MUB barcode validation screen (success).

### Connections / Flow (236)
- Screen: "Initialisation" → Decision: "Device boots into mode X"
- Decision: "Device boots into mode X" → Decision: "Bi-Directional"
- Screen: "BiDirectionalMode/InService" → Decision: "Travel Card or Barcode presented to Primary Reader"
- Screen: "BiDirectionalMode/InService" → Decision: "Travel Card or Barcode presented to Secondary Reader"
- Screen: "BiDirectionalMode/InService/Card Only" → Decision: "Travel Card or Barcode presented to Primary Reader"
- Screen: "BiDirectionalMode/InService/Card Only" → Decision: "Travel Card or Barcode presented to Secondary Reader"
- Screen: "BiDirectionalMode/InService/Code Only" → Decision: "Travel Card or Barcode presented to Primary Reader"
- Screen: "BiDirectionalMode/InService/Code Only" → Decision: "Travel Card or Barcode presented to Secondary Reader"
- Decision: "Travel Card or Barcode presented to Primary Reader" → Decision: "Card or Barcode is valid?"
- Decision: "Card or Barcode is valid?" → Screen: "BiDirectionalMode/Validation/Entry" [Yes]
- Decision: "Card or Barcode is valid?" → Screen: "BiDirectionalMode/Error/Entry" [No]
- Decision: "Travel Card or Barcode presented to Secondary Reader" → Decision: "Card or Barcode is valid?"
- Decision: "Card or Barcode is valid?" → Screen: "BiDirectionalMode/Validation/Exit" [Yes]
- Decision: "Card or Barcode is valid?" → Screen: "BiDirectionalMode/Error/Exit" [No]
- Screen: "BiDirectionalMode/InService" → Decision: "Reader becomes 
unavailable?"
- Decision: "Reader becomes 
unavailable?" → Screen: "BiDirectionalMode/InService/Card Only" [Barcode Reader
 unavailable]
- Decision: "Reader becomes 
unavailable?" → Screen: "BiDirectionalMode/InService/Code Only" [Card Reader
 unavailable]
- Screen: "BiDirectionalMode/Validation/Entry" → Screen: "BiDirectionalMode/InService"
- Screen: "BiDirectionalMode/Error/Entry" → Screen: "BiDirectionalMode/InService"
- Screen: "BiDirectionalMode/Validation/Exit" → Screen: "BiDirectionalMode/InService"
- Screen: "BiDirectionalMode/Error/Exit" → Screen: "BiDirectionalMode/InService"
- Screen: "BiDirectionalMode/Error/Entry" → Decision: "No Response"
- Screen: "BiDirectionalMode/Error/Entry" → Decision: "No Response"
- Screen: "BiDirectionalMode/Validation/Entry" → Decision: "No Response"
- Screen: "BiDirectionalMode/Validation/Exit" → Decision: "No Response"
- Screen: "BiDirectionalMode/Validation/Entry" → Decision: "Card or Barcode is valid?"
- Screen: "BiDirectionalMode/Error/Exit" → Decision: "No Response"
- Screen: "BiDirectionalMode/Error/Exit" → Decision: "No Response"
- Screen: "BiDirectionalMode/Validation/Exit" → Decision: "Card or Barcode is valid?"
- Decision: "Travel Card or Barcode presented to Primary Reader" → Decision: "Card or Barcode is valid?"
- Decision: "Travel Card or Barcode presented to Secondary Reader" → Decision: "No Response"
- Screen: "EntryMode/InService" → Decision: "Travel Card or Barcode presented to Secondary Reader"
- Screen: "EntryMode/InService" → Decision: "Travel Card or Barcode presented to Secondary Reader"
- Screen: "EntryMode/InService/CardOnly" → Decision: "Travel Card or Barcode presented to Secondary Reader"
- Screen: "EntryMode/InService/CardOnly" → Decision: "Travel Card or Barcode presented to Secondary Reader"
- Screen: "EntryMode/InService/Code Only" → Decision: "Travel Card or Barcode presented to Secondary Reader"
- Screen: "EntryMode/InService/Code Only" → Decision: "Travel Card or Barcode presented to Secondary Reader"
- Screen: "EntryMode/InService" → Decision: "Travel Card or Barcode presented to Primary Reader"
- Screen: "EntryMode/InService" → Decision: "Travel Card or Barcode presented to Primary Reader"
- Screen: "EntryMode/InService/CardOnly" → Decision: "Travel Card or Barcode presented to Primary Reader"
- Screen: "EntryMode/InService/Code Only" → Decision: "Travel Card or Barcode presented to Primary Reader"
- Decision: "Card or Barcode is valid?" → Screen: "EntryMode/Validation/Fail" [No
]
- Decision: "Card or Barcode is valid?" → Screen: "EntryMode/Validation/Success" [Yes]
- Screen: "EntryMode/Validation/Success" → Screen: "EntryMode/InService"
- Screen: "EntryMode/Validation/Fail" → Screen: "EntryMode/InService"
- Screen: "EntryMode/Validation/Fail" → Decision: "No Response"
- Screen: "EntryMode/Validation/Fail" → Decision: "No Response"
- Screen: "EntryMode/Validation/Fail" → Decision: "No Response"
- Screen: "EntryMode/Validation/Fail" → Decision: "No Response"
- Screen: "EntryMode/InService" → Decision: "Reader becomes 
unavailable?"
- Decision: "Reader becomes 
unavailable?" → Screen: "EntryMode/InService/CardOnly"
- Decision: "Reader becomes 
unavailable?" → Screen: "EntryMode/InService/Code Only"
- Screen: "EntryMode/Validation/Success" → Decision: "Travel Card or Barcode presented to Primary Reader"
- Screen: "EntryMode/Validation/Success" → Decision: "Travel Card or Barcode presented to Primary Reader"
- Screen: "EntryMode/Validation/Success" → Decision: "No Response"
- Screen: "EntryMode/Validation/Success" → Decision: "No Response"
- Decision: "Device boots into mode X" → Decision: "Entry Mode"
- Decision: "Travel Card or Barcode presented to Primary Reader" → Decision: "No Response"
- Decision: "Travel Card or Barcode presented to Secondary Reader" → Decision: "Card or Barcode is valid?"
- Decision: "Card or Barcode is valid?" → Screen: "ExitMode/Validation/Success" [Yes]
- Decision: "Card or Barcode is valid?" → Screen: "ExitMode/Validation/Fail" [No]
- Screen: "ExitMode/Validation/Success" → Decision: "No Response"
- Screen: "ExitMode/Validation/Success" → Decision: "No Response"
- Screen: "ExitMode/Validation/Fail" → Decision: "No Response"
- Screen: "ExitMode/Validation/Fail" → Decision: "No Response"
- Screen: "ExitMode/Validation/Fail" → Decision: "No Response"
- Screen: "ExitMode/Validation/Fail" → Decision: "No Response"
- Screen: "ExitMode/Validation/Success" → Decision: "Travel Card or Barcode presented to Secondary Reader"
- Screen: "ExitMode/Validation/Success" → Decision: "Travel Card or Barcode presented to Secondary Reader"
- Screen: "ExitMode/InService" → Decision: "Travel Card or Barcode presented to Secondary Reader"
- Screen: "ExitMode/InService" → Decision: "Travel Card or Barcode presented to Secondary Reader"
- Screen: "ExitMode/InService" → Decision: "Reader becomes 
unavailable?"
- Decision: "Reader becomes 
unavailable?" → Screen: "ExitMode/InService/CardOnly"
- Decision: "Reader becomes 
unavailable?" → Screen: "ExitMode/InService/Code Only"
- Screen: "ExitMode/InService" → Decision: "Travel Card or Barcode presented to Primary Reader"
- Screen: "ExitMode/InService" → Decision: "Travel Card or Barcode presented to Primary Reader"
- Screen: "ExitMode/Validation/Success" → Screen: "ExitMode/InService"
- Screen: "ExitMode/Validation/Fail" → Screen: "ExitMode/InService"
- Decision: "Device boots into mode X" → Decision: "Exit Mode"
- Decision: "Device boots into mode X" → Decision: "Emergency Mode"
- Decision: "Device boots into mode X" → Decision: "Free Entry Mode"
- Decision: "Device boots into mode X" → Decision: "Closed Mode"
- Screen: "ExitMode/InService/CardOnly" → Decision: "Travel Card or Barcode presented to Secondary Reader"
- Screen: "ExitMode/InService/Code Only" → Decision: "Travel Card or Barcode presented to Secondary Reader"
- Screen: "ExitMode/InService/CardOnly" → Decision: "Travel Card or Barcode presented to Primary Reader"
- Screen: "ExitMode/InService/Code Only" → Decision: "Travel Card or Barcode presented to Primary Reader"
- Screen: "ExitMode/InService/CardOnly" → Decision: "Travel Card or Barcode presented to Primary Reader"
- Screen: "ExitMode/InService/Code Only" → Decision: "Travel Card or Barcode presented to Primary Reader"
- Screen: "EmergencyMode" → Decision: "Travel Card or Barcode presented to Either Reader"
- Screen: "EmergencyMode" → Decision: "Travel Card or Barcode presented to Either Reader"
- Screen: "EmergencyMode" → Decision: "Travel Card or Barcode presented to Either Reader"
- Screen: "EmergencyMode" → Decision: "Travel Card or Barcode presented to Either Reader"
- Decision: "Travel Card or Barcode presented to Either Reader" → Decision: "No Response"
- Decision: "Travel Card or Barcode presented to Either Reader" → Decision: "No Response"
- Decision: "Travel Card or Barcode presented to Either Reader" → Decision: "No Response"
- Decision: "Travel Card or Barcode presented to Either Reader" → Decision: "No Response"
- Decision: "Travel Card or Barcode presented to Either Reader" → Decision: "No Response"
- Decision: "Travel Card or Barcode presented to Either Reader" → Decision: "No Response"
- Decision: "Travel Card or Barcode presented to Either Reader" → Decision: "No Response"
- Decision: "Travel Card or Barcode presented to Either Reader" → Decision: "No Response"
- Decision: "Travel Card or Barcode presented to Either Reader" → Decision: "No Response"
- Decision: "Travel Card or Barcode presented to Either Reader" → Decision: "No Response"
- Screen: "ClosedMode/NotInService" → Decision: "Travel Card or Barcode presented to Either Reader"
- Screen: "ClosedMode/NotInService" → Decision: "Travel Card or Barcode presented to Either Reader"
- Screen: "ClosedMode/NotInService" → Decision: "Travel Card or Barcode presented to Either Reader"
- Screen: "ClosedMode/NotInService" → Decision: "Travel Card or Barcode presented to Either Reader"
- Screen: "FullyFree/Idle" → Decision: "Travel Card or Barcode presented to Either Reader"
- Screen: "FullyFree/Idle" → Decision: "Travel Card or Barcode presented to Either Reader"
- Screen: "FullyFree/Idle" → Decision: "Travel Card or Barcode presented to Either Reader"
- Screen: "FullyFree/Idle" → Decision: "Travel Card or Barcode presented to Either Reader"
- Screen: "FullyFree/Idle" → Decision: "Passenger ingress is detected on either 
Side A or Side B"
- Decision: "Passenger ingress is detected on either 
Side A or Side B" → Screen: "FullyFree/Traverse" [Gate Opens in the opposing direction 
to which the passenger entered by]
- Screen: "FullyFree/Traverse" → Decision: "Passenger has been detected to have degressed"
- Screen: "FullyFree/Traverse" → Decision: "No Response"
- Screen: "FullyFree/Traverse" → Decision: "No Response"
- Screen: "FullyFree/Traverse" → Decision: "No Response"
- Screen: "FullyFree/Traverse" → Decision: "No Response"
- Decision: "Passenger has been detected to have degressed" → Screen: "FullyFree/Idle"
- Screen: "EmergencyMode" → Decision: "Passenger ingress is detected on either 
Side A or Side B"
- Decision: "Passenger ingress is detected on either 
Side A or Side B" → Decision: "No Response"
- Screen: "ClosedMode/NotInService" → Decision: "Unexpected passenger ingress is detected on Side A"
- Screen: "ClosedMode/NotInService" → Decision: "unexpected passenger ingress is detected on Side B"
- Decision: "Valid Technician Card is Presented to Primary Validator" → Screen: "TechMode/Primary"
- Decision: "Valid Technician Card is Presented to Secondary Validator" → Screen: "TechMode/Secondary"
- Decision: "Valid Technician Card is Presented to both validators" → Screen: "TechMode/Both"
- Screen: "TechMode/Primary" → Decision: "For sign-on and Technician menus see "Technician Menu gate" board"
- Screen: "TechMode/Secondary" → Decision: "For sign-on and Technician menus see "Technician Menu gate" board"
- Screen: "TechMode/Both" → Decision: "For sign-on and Technician menus see "Technician Menu gate" board"
- Decision: "Device boots into mode X" → Decision: "Technician Mode"
- Decision: "Device is powered on" → Screen: "0.0 Loading"
- Screen: "0.0 Loading" → Decision: "Is device commissioned 
and fully operational?"
- Decision: "Is device commissioned 
and fully operational?" → Screen: "1.0.1 Present SmartCard or Barcode" [Yes]
- Decision: "Is device commissioned 
and fully operational?" → Decision: "Is Validator/Plinth Commissioned?" [No]
- Decision: "A device fault has occurred" → Screen: "1.1.0 Present SmartCard no Tickets" [Barcode Reader has
 become unavailable]
- Decision: "A device fault has occurred" → Screen: "1.1.1 Present Ticket no SmartCard" [Smartcard Reader
 has become unavailable]
- Screen: "1.0.1 Present SmartCard or Barcode" → Decision: "A device fault has occurred"
- Decision: "A device fault has occurred" → Screen: "1.2.8 Machine Not in Service (Gate)" [Both readers become 
unavailable or "other" non-powerloss 
based fault has occurred]
- Screen: "1.1.1 Present Ticket no SmartCard" → Decision: "Device reboots in an attempt to recover the reader"
- Screen: "1.2.8 Machine Not in Service (Gate)" → Decision: "Device reboots in an attempt to recover the reader"
- Screen: "1.1.1 Present Ticket no SmartCard" → Decision: "Fault is corrected"
- Screen: "1.1.0 Present SmartCard no Tickets" → Decision: "Fault is corrected"
- Screen: "1.2.8 Machine Not in Service (Gate)" → Decision: "Fault is corrected"
- Decision: "Fault is corrected" → Screen: "1.0.1 Present SmartCard or Barcode"
- Decision: "Device reboots in an attempt to recover the reader" → Screen: "0.0 Loading"
- Screen: "1.0.1 Present SmartCard or Barcode" → Decision: "Smartcard or Barcode is presented to reader"
- Decision: "Smartcard or Barcode is presented to reader" → Decision: "Is presented card readable?"
- Decision: "ABT
Valid AID?" → Decision: "ABT
Card is Expired?" [Yes
(VISA, Mastercard, Maestro)]
- Decision: "ABT
Card is Expired?" → Decision: "ABT
ODA Valid?" [No]
- Decision: "ABT
ODA Valid?" → Decision: "ABT
Is PAN  on BIN list?" [Valid]
- Decision: "ABT
Is PAN  on BIN list?" → Decision: "ABT
PAN on Deny List?" [No]
- Decision: "ABT
PAN on Deny List?" → Decision: "ABT
Has PAN been used within Passback Period?" [No]
- Decision: "ABT
Valid AID?" → Screen: "1.6.2 ABT deny list/negative list" [No
(American Express, etc)]
- Decision: "ABT
Card is Expired?" → Screen: "1.6.2 ABT deny list/negative list" [Yes]
- Decision: "ABT
ODA Valid?" → Screen: "1.6.2 ABT deny list/negative list" [No]
- Decision: "ABT
Is PAN  on BIN list?" → Screen: "1.6.2 ABT deny list/negative list" [Yes]
- Decision: "ABT
PAN on Deny List?" → Screen: "1.6.2 ABT deny list/negative list" [Yes]
- Decision: "Is presented card readable?" → Decision: "Is the presented 
smartcarda Legacy miFare or 
ABT EMV?" [Yes]
- Decision: "Is presented card readable?" → Screen: "1.6.3 ABT Error reading card" [No]
- Decision: "Is the presented 
smartcarda Legacy miFare or 
ABT EMV?" → Decision: "ABT
Valid AID?" [ABT]
- Decision: "ABT
Has PAN been used within Passback Period?" → Screen: "1.6.1.1 ABT Tag successful" [No]
- Decision: "ABT
Has PAN been used within Passback Period?" → Screen: "1.4.9 Passback - No Entry" [Yes]
- Decision: "Smartcard
Was Smartcard validation record successfully updated?" → Screen: "1.3.1 Represent Card" [No]
- Decision: "Smartcard
Is card blocked?" → Decision: "Smartcard
Is card on the Actionlist?" [No
]
- Decision: "Smartcard
Is card on the Actionlist?" → Decision: "Smartcard
Is smartcard product valid for current location?" [No]
- Decision: "Smartcard
Is smartcard product valid for current location?" → Decision: "Smartcard
Is smartcard valid at current time/date?" [Yes]
- Decision: "Smartcard
Is smartcard valid at current time/date?" → Decision: "Smartcard
Is smartcard expired?" [Yes]
- Decision: "Smartcard
Is smartcard expired?" → Decision: "Smartcard
Is smartcard within Passback period?" [No]
- Decision: "Smartcard
Is smartcard within Passback period?" → Decision: "Smartcard
Is smartcard within transfer period?" [No]
- Decision: "Smartcard
Is card blocked?" → Screen: "1.6.4 ABT Hot listed card" [Yes]
- Decision: "Smartcard
Is card on the Actionlist?" → Screen: "1.6.4 ABT Hot listed card" [Yes]
- Decision: "Smartcard
Is smartcard product valid for current location?" → Screen: "1.3.7 Not Valid At This Location" [No]
- Decision: "Smartcard
Is smartcard valid at current time/date?" → Screen: "1.3.8 Invalid Time Of Day" [No]
- Decision: "Smartcard
Is smartcard expired?" → Screen: "1.3.9 Product Expired" [Yes]
- Decision: "Smartcard
Is smartcard within Passback period?" → Screen: "1.4.9 Passback - No Entry" [Yes]
- Decision: "Smartcard
Was Smartcard validation record successfully updated?" → Screen: "1.5.0 Tag successful" [Yes]
- Decision: "Is the presented 
smartcarda Legacy miFare or 
ABT EMV?" → Decision: "Smartcard
Is smartcard an
 operator card?" [Smartcard]
- Decision: "Barcode
Is barcode expired?" → Screen: "1.7.99.5 Barcode Validation Fail - Expired"
- Decision: "Barcode
Is barcode valid at current location?" → Screen: "1.7.99.4 Barcode Validation Fail - Location"
- Decision: "Barcode
Is barcode valid at current date/time" → Screen: "1.7.99.3 Barcode Validation Fail - Time"
- Decision: "Barcode
Is barcode valid on current route/service?" → Screen: "1.7.99.2 Barcode Validation Fail - Service"
- Decision: "Barcode
Is barcode valid on current route/service?" → Decision: "Barcode
Is barcode valid at current date/time"
- Decision: "Barcode
Is barcode valid at current date/time" → Decision: "Barcode
Is barcode valid at current location?"
- Decision: "Barcode
Is barcode valid at current location?" → Decision: "Barcode
Is barcode expired?"
- Decision: "Barcode
Is barcode expired?" → Decision: "Barcode
Has Barcode been used within Passback Period?"
- Decision: "Barcode
Has Barcode been used within Passback Period?" → Screen: "1.7.99.1 Barcode Validation Fail - Passback"
- Decision: "Barcode
Has Barcode been used within Passback Period?" → Screen: "1.7.1.1 Barcode Validation Successful - Adult"
- Decision: "Barcode
Is barcode readable?" → Decision: "Barcode
Is barcode valid on current route/service?"
- Decision: "Barcode
Is barcode readable?" → Screen: "1.3.16 Unable to Validate"
- Decision: "Smartcard or Barcode is presented to reader" → Decision: "Barcode
Is barcode readable?"
- Decision: "Is Validator/Plinth Commissioned?" → Screen: "1.2.10 Machine Not Commissioned (Gate)" [No]
- Decision: "Is Validator/Plinth Commissioned?" → Screen: "1.2.8 Machine Not in Service (Gate)" [Yes]
- Screen: "1.0.1 Present SmartCard or Barcode" → Decision: "Gate has been 
remotely change to
 "Fully Free" mode?" [GateMode or state has changed.
]
- Decision: "Gate has changed 
to Emergency mode" → Decision: "Device is Primary?
(Unsecured side)" [Yes]
- Decision: "Device is Primary?
(Unsecured side)" → Screen: "1.2.4 Emergency Exit" [No
(Secured Side)]
- Decision: "Device is Primary?
(Unsecured side)" → Screen: "1.2.6 No Entry" [Yes
(Secured Side)]
- Decision: "Gate has been 
remotely change to
 "Fully Free" mode?" → Screen: "1.2.5 Please Proceed" [Yes]
- Decision: "Gate has been 
remotely change to
 "Fully Free" mode?" → Decision: "Gate has changed 
to Emergency mode" [No]
- Decision: "Gate has changed 
to Entry Mode" → Decision: "Device is Primary?
(Unsecured side)" [Yes]
- Decision: "Gate has changed 
to Exit Mode" → Decision: "Device is Primary?
(Unsecured side)" [Yes]
- Decision: "Gate has changed 
to Emergency mode" → Decision: "Gate has changed 
to Entry Mode" [No]
- Decision: "Gate has changed 
to Entry Mode" → Decision: "Gate has changed 
to Exit Mode" [No]
- Decision: "Device is Primary?
(Unsecured side)" → Screen: "1.2.6 No Entry" [No]
- Decision: "Device is Primary?
(Unsecured side)" → Screen: "1.2.6 No Entry" [Yes]
- Decision: "Gate has changed 
to Locked Mode" → Screen: "1.2.6 No Entry" [Yes]
- Decision: "Device is Primary?
(Unsecured side)" → Decision: "Is device commissioned 
and fully operational?" [No]
- Decision: "Device is Primary?
(Unsecured side)" → Decision: "Is device commissioned 
and fully operational?" [No]
- Decision: "Gate has changed 
to Exit Mode" → Decision: "Gate has changed 
to Locked Mode" [No]
- Decision: "Gate has changed 
to Locked Mode" → Decision: "Gate has opened due to passenger activity?" [No]
- Decision: "Which direction is Gate opening?" → Screen: "1.2.9 Bi-directional screen" [Towards the validator]
- Decision: "Which direction is Gate opening?" → Screen: "1.2.5 Please Proceed" [Away from Validator]
- Decision: "Is Gate Bi-Directional?" → Decision: "Which direction is Gate opening?" [Yes]
- Decision: "Gate has opened due to passenger activity?" → Decision: "Is Gate Bi-Directional?" [Yes]
- Decision: "Is Gate Bi-Directional?" → Screen: "1.2.6 No Entry" [No]
- Decision: "Has device been put out of service?" → Decision: "Is device commissioned 
and fully operational?"
- Decision: "Gate has opened due to passenger activity?" → Decision: "Has device been put out of service?" [No]
- Decision: "Has device been put out of service?" → Screen: "1.2.8 Machine Not in Service (Gate)"
- Decision: "Smartcard
Is smartcard an
 operator card?" → Decision: "Smartcard
Is card blocked?" [No]
- Decision: "Smartcard
Is smartcard an
 operator card?" → Decision: "Does Operator ID match a Technician ID in Stafflist?" [Yes]
- Decision: "Does Operator ID match a Technician ID in Stafflist?" → Decision: "Device will not respond" [No]
- Decision: "Does Operator ID match a Technician ID in Stafflist?" → Decision: "See "Technician Menu - Gate" board
for Technician Sign-on." [Yes]
- Screen: "Template -Validator Prompt" → Decision: "Company Logo"
- Screen: "Template -Validator Prompt" → Decision: "PlinthID / DeviceID / Sublocation ID"
- Screen: "Template -Validator Prompt" → Decision: "Location ID"
- Screen: "Template -Validator Prompt" → Decision: "Date"
- Screen: "Template -Validator Prompt" → Decision: "Time (24 hour clock)"
- Screen: "Template -Validator Prompt" → Decision: "Prompt to present media type.
Can be either/or both Card/Barcode depending on reader availability"
- Screen: "Template -Validator Prompt" → Decision: "Degraded Message"
- Screen: "Template -Validator Prompt" → Decision: "Icon indicating where the card/barcode readers are."
- Screen: "Template - Validator Response" → Decision: "Status Bar as above"
- Screen: "Template - Validator Response" → Decision: "Status Icon"
- Screen: "Template - Validator Response" → Decision: "Background colour representing the response communicated.

Eg, Green:Success / Red:Failure / Amber:Warning"
- Screen: "Template - Validator Response" → Decision: "Main update message. 
Eg. Validation Success /Failure"
- Screen: "Template - Validator Response" → Decision: "Optional sub-message
Up to two lines of text often providing directions or further information."
- Screen: "Template -Validator Prompt" → Decision: "Zone Name"
- Decision: "Smartcard
Is smartcard within transfer period?" → Screen: "1.5.0 Tag successful" [Yes]
- Decision: "Smartcard
Is smartcard within transfer period?" → Decision: "Smartcard
Was Smartcard validation record successfully updated?" [No]


## 3. Technician Menu - Gate

### Screens (28)
- 1.0 Present SmartCard or Barcode
- 10.00.51 Technician Menu - Login Screen
- 10.00.52 Technician Menu -Enter PIN
- 11.00.50 Technician Menu - Home Screen
- 11.01.52 Technician Menu - Location Settings - Gate - Edit
- 10.00.53 Technician Menu - Incorrect Details
- 11.05.02 Technician Menu - Network interfaces - Details
- 10.02.02 Technician Menu - Please Wait
- 11.05.01 Technician Menu - Network Interfaces
- 11.01.51 Technician Menu - Location Settings - Gate
- 11.01.53 Technician Menu - Location Settings - Gate - Edit - Clear
- 10.02.01 Technician Menu - Sign Off
- 11.05.03 Technician Menu - Network interfaces - FecDetails
- 11.05.54 Technician Menu - Network interfaces - Gate - ChangeIP
- 11.05.05 Technician Menu - Network Routing Table
- 11.01.10 Technician Menu - Select Location
- 11.01.10 Technician Menu - Select Location - Selected
- 11.01.05 Technician Menu - Location Settings - Fail
- 10.02.03 Technician Menu - Rebooting
- 11.02.01 Technician Menu - Software Version
- 11.06.01 Technician Menu - Configuration Version
- 11.03.01 Technician Menu - Brightness
- 11.07.01 Technician Menu - Audio
- 11.08.10 Technician Menu - Tests Pass
- 10.02.02 Technician Menu - Please Wait
- 11.04.01 Technician Menu - Force communications
- 11.08.00 Technician Menu - Tests and Diagnostics
- 11.08.15 Technician Menu - Tests Fail

### Decision Points (12)
- Is the PIN valid  for the provided ID?
- Has the  Home Location  changed?
- Is the  Home Location list available?
- 11.00.00 Technician Menu - Home Screen
- 1.0 Present SmartCard or Barcode
- 11.00.00 Technician Menu - Home Screen
- 11.00.00 Technician Menu - Home Screen
- 11.00.00 Technician Menu - Home Screen
- 11.00.00 Technician Menu - Home Screen
- 11.00.00 Technician Menu - Home Screen
- 11.00.00 Technician Menu - Home Screen
- 11.00.00 Technician Menu - Home Screen

### Annotations / Spec Notes (14)
- Presenting an Technician card will redirect user to Sign on page with the ID automatically entered and PIN field active.
- Location Settings
- Network Settings
- User will be able to enter/edit values by pressing the 'Change' button.  When in Edit mode the 'Stop Location', 'Install Point ID', 'Mount ID' and 'Zone' can be configured by selecting the relevant field and entering a number via the on-screen pin-pad.   To change the Home Location the user will press the 'Select' button and choose from a list of available Home Locations provided on request from the BackOffice.  When a new Home Location is selected a reboot will be necessary to perform the update.
- The error message will disapear as a new PIN is entered..
- Software Versions
- Configuration Versions
- Audio
- Brightness
- The Brightness page allows teh technician to make adjustments tot eh PV screen brightness. The 'Mode' displayed indicates whether the PV has been configured manually or is configured to automatically adapt to environmental light conditions as detected via the built-in light sensor.
- Tests and Diagnostics WIP
- Force Communications
- The Force Communications page will summarize the following details:     1. How many Audit Records are pending delivery to the back office.     2. The last date/time that an Audit Record was successfully sent     3. The last date/time a manifest download was attempted     4. The last date/time a manifest download was successful     5. A count of pending files to download for software/configuration updates.  Pressing the 'Call Now' button will trigger a check of the manifest in the back office and attempt to send any pending audit records.   Pressing the 'Refresh' button will update the values displayed with the most recent information.
- Section reserved for Gate Validators.

### Connections / Flow (57)
- Screen: "1.0 Present SmartCard or Barcode" → Screen: "10.00.51 Technician Menu - Login Screen" [Valid Technician Card 
is presented to the Validator]
- Decision: "Is the PIN valid 
for the provided ID?" → Screen: "11.00.50 Technician Menu - Home Screen" [Yes]
- Screen: "11.01.51 Technician Menu - Location Settings - Gate" → Screen: "11.01.52 Technician Menu - Location Settings - Gate - Edit"
- Screen: "10.00.51 Technician Menu - Login Screen" → Screen: "1.0 Present SmartCard or Barcode"
- Screen: "11.00.50 Technician Menu - Home Screen" → Screen: "10.02.01 Technician Menu - Sign Off"
- Screen: "10.02.01 Technician Menu - Sign Off" → Screen: "11.00.50 Technician Menu - Home Screen"
- Screen: "10.00.51 Technician Menu - Login Screen" → Screen: "10.00.52 Technician Menu -Enter PIN" [User Enters PIN]
- Screen: "10.00.52 Technician Menu -Enter PIN" → Screen: "1.0 Present SmartCard or Barcode"
- Screen: "10.00.52 Technician Menu -Enter PIN" → Decision: "Is the PIN valid 
for the provided ID?"
- Screen: "10.00.52 Technician Menu -Enter PIN" → Screen: "10.00.51 Technician Menu - Login Screen"
- Decision: "Is the PIN valid 
for the provided ID?" → Screen: "10.00.53 Technician Menu - Incorrect Details" [No]
- Screen: "10.00.53 Technician Menu - Incorrect Details" → Screen: "1.0 Present SmartCard or Barcode"
- Screen: "10.00.53 Technician Menu - Incorrect Details" → Decision: "Is the PIN valid 
for the provided ID?"
- Screen: "10.02.01 Technician Menu - Sign Off" → Screen: "1.0 Present SmartCard or Barcode"
- Screen: "11.00.50 Technician Menu - Home Screen" → Screen: "11.01.51 Technician Menu - Location Settings - Gate"
- Screen: "11.00.50 Technician Menu - Home Screen" → Screen: "11.02.01 Technician Menu - Software Version"
- Screen: "11.00.50 Technician Menu - Home Screen" → Screen: "11.03.01 Technician Menu - Brightness"
- Screen: "11.00.50 Technician Menu - Home Screen" → Screen: "11.04.01 Technician Menu - Force communications"
- Screen: "11.01.53 Technician Menu - Location Settings - Gate - Edit - Clear" → Screen: "11.01.52 Technician Menu - Location Settings - Gate - Edit" [User enters 
details into 
empty field]
- Screen: "11.02.01 Technician Menu - Software Version" → Decision: "11.00.00 Technician Menu - Home Screen"
- Screen: "11.00.50 Technician Menu - Home Screen" → Screen: "11.05.01 Technician Menu - Network Interfaces"
- Screen: "11.00.50 Technician Menu - Home Screen" → Screen: "11.06.01 Technician Menu - Configuration Version"
- Screen: "11.00.50 Technician Menu - Home Screen" → Screen: "11.07.01 Technician Menu - Audio"
- Screen: "11.00.50 Technician Menu - Home Screen" → Screen: "11.08.00 Technician Menu - Tests and Diagnostics"
- Screen: "11.01.51 Technician Menu - Location Settings - Gate" → Decision: "11.00.00 Technician Menu - Home Screen"
- Screen: "11.03.01 Technician Menu - Brightness" → Decision: "11.00.00 Technician Menu - Home Screen"
- Screen: "11.01.10 Technician Menu - Select Location" → Screen: "11.01.52 Technician Menu - Location Settings - Gate - Edit"
- Decision: "Is the 
Home Location list available?" → Screen: "11.01.10 Technician Menu - Select Location" [Yes]
- Decision: "Has the
 Home Location 
changed?" → Screen: "11.01.51 Technician Menu - Location Settings - Gate" [No]
- Screen: "10.02.02 Technician Menu - Please Wait" → Decision: "Has the
 Home Location 
changed?"
- Decision: "Has the
 Home Location 
changed?" → Screen: "10.02.03 Technician Menu - Rebooting" [Yes]
- Screen: "10.02.03 Technician Menu - Rebooting" → Decision: "1.0 Present SmartCard or Barcode" [Device will reboot]
- Screen: "11.04.01 Technician Menu - Force communications" → Screen: "10.02.02 Technician Menu - Please Wait"
- Screen: "10.02.02 Technician Menu - Please Wait" → Screen: "11.04.01 Technician Menu - Force communications"
- Screen: "11.05.01 Technician Menu - Network Interfaces" → Screen: "11.05.02 Technician Menu - Network interfaces - Details"
- Screen: "11.05.01 Technician Menu - Network Interfaces" → Screen: "11.05.03 Technician Menu - Network interfaces - FecDetails"
- Screen: "11.05.03 Technician Menu - Network interfaces - FecDetails" → Screen: "11.05.54 Technician Menu - Network interfaces - Gate - ChangeIP"
- Screen: "11.01.10 Technician Menu - Select Location" → Screen: "11.01.10 Technician Menu - Select Location - Selected"
- Screen: "11.01.10 Technician Menu - Select Location - Selected" → Screen: "11.01.52 Technician Menu - Location Settings - Gate - Edit"
- Decision: "Is the 
Home Location list available?" → Screen: "11.01.05 Technician Menu - Location Settings - Fail" [No]
- Screen: "11.01.05 Technician Menu - Location Settings - Fail" → Screen: "11.01.52 Technician Menu - Location Settings - Gate - Edit"
- Screen: "11.01.05 Technician Menu - Location Settings - Fail" → Decision: "Is the 
Home Location list available?"
- Screen: "11.01.10 Technician Menu - Select Location - Selected" → Screen: "11.01.53 Technician Menu - Location Settings - Gate - Edit - Clear"
- Screen: "11.05.01 Technician Menu - Network Interfaces" → Screen: "11.05.05 Technician Menu - Network Routing Table"
- Screen: "11.05.05 Technician Menu - Network Routing Table" → Screen: "11.05.01 Technician Menu - Network Interfaces"
- Screen: "11.05.03 Technician Menu - Network interfaces - FecDetails" → Screen: "11.05.01 Technician Menu - Network Interfaces"
- Screen: "11.05.02 Technician Menu - Network interfaces - Details" → Screen: "11.05.01 Technician Menu - Network Interfaces"
- Screen: "11.01.52 Technician Menu - Location Settings - Gate - Edit" → Screen: "10.02.02 Technician Menu - Please Wait" [User Selects Confirm]
- Screen: "11.01.53 Technician Menu - Location Settings - Gate - Edit - Clear" → Screen: "11.01.51 Technician Menu - Location Settings - Gate" [User Selects
Cancel]
- Screen: "11.01.52 Technician Menu - Location Settings - Gate - Edit" → Screen: "11.01.51 Technician Menu - Location Settings - Gate" [User Selects
Cancel]
- Screen: "11.01.52 Technician Menu - Location Settings - Gate - Edit" → Screen: "11.01.53 Technician Menu - Location Settings - Gate - Edit - Clear"
- Screen: "11.01.52 Technician Menu - Location Settings - Gate - Edit" → Screen: "10.02.02 Technician Menu - Please Wait"
- Screen: "11.04.01 Technician Menu - Force communications" → Decision: "11.00.00 Technician Menu - Home Screen"
- Screen: "11.05.01 Technician Menu - Network Interfaces" → Decision: "11.00.00 Technician Menu - Home Screen"
- Screen: "11.06.01 Technician Menu - Configuration Version" → Decision: "11.00.00 Technician Menu - Home Screen"
- Screen: "11.07.01 Technician Menu - Audio" → Decision: "11.00.00 Technician Menu - Home Screen"
- Screen: "11.08.00 Technician Menu - Tests and Diagnostics" → Decision: "11.00.00 Technician Menu - Home Screen"


## 4. Platform Validator-Barcode

### Screens (26)
- 1.1.0 Present SmartCard no Tickets
- 0.0 Loading
- 1.0.1 Present SmartCard or Barcode
- 1.1.1 Present Ticket no SmartCard
- 1.2.1 Machine Not in Service
- 1.2.1 Machine Not in Service
- 1.6.1.1 ABT Tag successful
- 1.6.1.1 ABT Tag successful - Rail
- 1.6.6 Passback - No Entry
- 1.6.3 ABT Error reading card
- 1.6.2 ABT deny list/negative list
- 1.4.3 Passback Journeys Left
- 1.4.4 Passback Days Left 
- 1.5.0 Tag successful
- 1.6.4 ABT Hot listed card
- 1.3.7 Not Valid At This Location
- 1.3.8 Invalid Time Of Day
- 1.3.9 Product Expired
- 1.3.1 Represent Card
- 1.7.1.1 Barcode Validation Successful - Adult
- 1.3.16 Unable to Validate
- 1.7.99.3 Barcode Validation Fail - Time
- 1.7.99.2 Barcode Validation Fail - Service
- 1.7.99.4 Barcode Validation Fail - Location
- 1.7.99.5 Barcode Validation Fail - Expired
- 1.7.99.6 Barcode Validation Fail - Passback PV

### Decision Points (33)
- Fault is corrected
- Is device commissioned  and fully operational?
- A device fault has occurred
- Device is powered on
- Device reboots in an attempt to recover the reader
- Is Validator/Plinth Commissioned?
- Smartcard or Barcode is presented to reader
- Is presented card readable?
- Is the presented  smartcarda Legacy miFare or  ABT EMV?
- ABT Valid AID?
- ABT Card is Expired?
- ABT ODA Valid?
- ABT Is PAN  on BIN list?
- ABT PAN on Deny List?
- ABT Has PAN been used within Passback Period?
- Smartcard Is smartcard an  operator card?
- Does Operator ID match a Technician ID in Stafflist?
- See "Technician Menu" board for Technician Sign-on.
- Device will not respond
- Smartcard Is card blocked?
- Smartcard Is card on the Actionlist?
- Smartcard Is smartcard product valid for current location?
- Smartcard Is smartcard valid at current time/date?
- Smartcard Is smartcard expired?
- Smartcard Is smartcard within Passback period?
- Smartcard Is smartcard within transfer period?
- Smartcard Was Smartcard validation record successfully updated?
- Barcode Is barcode readable?
- Barcode Is barcode valid on current route/service?
- Barcode Is barcode valid at current date/time
- Barcode Is barcode valid at current location?
- Barcode Is barcode expired?
- Barcode Has Barcode been used within Passback Period?

### Annotations / Spec Notes (6)
- Platform Validator
- Platform Validator
- The following flow for the Platform Validator differs from the Gate Validator flow in that Passback validations are not considered a Failure response.
- Typically an uncommissioned device will have an unprogrammed Plinth-ID so it would be expected that the Status Bar may not have programmed values to display for Device ID / Sub Location or the Location.  Device will require comms and a Technician to sign-in and program the Location details
- '1.6.1.1 ABT Tag successful' screen can display an additional line of text. For NIR/Rail PVs this will state "Northern Ireland Travel Only".
- For all barcodes that have an expiry time between 00:00 and 04:00 the PV will need to display the previous day (as the expiry date) on the MUB barcode validation screen (success).

### Connections / Flow (69)
- Decision: "Device is powered on" → Screen: "0.0 Loading"
- Screen: "0.0 Loading" → Decision: "Is device commissioned 
and fully operational?"
- Decision: "Is device commissioned 
and fully operational?" → Screen: "1.0.1 Present SmartCard or Barcode" [Yes]
- Decision: "Is device commissioned 
and fully operational?" → Decision: "Is Validator/Plinth Commissioned?" [No]
- Decision: "A device fault has occurred" → Screen: "1.1.0 Present SmartCard no Tickets" [Barcode Reader has
 become unavailable]
- Decision: "A device fault has occurred" → Screen: "1.1.1 Present Ticket no SmartCard" [Smartcard Reader
 has become unavailable]
- Screen: "1.0.1 Present SmartCard or Barcode" → Decision: "A device fault has occurred"
- Decision: "A device fault has occurred" → Screen: "1.2.1 Machine Not in Service" [Both readers become 
unavailable or "other" non-powerloss 
based fault has occurred]
- Screen: "1.1.1 Present Ticket no SmartCard" → Decision: "Device reboots in an attempt to recover the reader"
- Screen: "1.2.1 Machine Not in Service" → Decision: "Device reboots in an attempt to recover the reader"
- Screen: "1.1.1 Present Ticket no SmartCard" → Decision: "Fault is corrected"
- Screen: "1.1.0 Present SmartCard no Tickets" → Decision: "Fault is corrected"
- Screen: "1.2.1 Machine Not in Service" → Decision: "Fault is corrected"
- Decision: "Fault is corrected" → Screen: "1.0.1 Present SmartCard or Barcode"
- Decision: "Device reboots in an attempt to recover the reader" → Screen: "0.0 Loading"
- Screen: "1.0.1 Present SmartCard or Barcode" → Decision: "Smartcard or Barcode is presented to reader"
- Decision: "Smartcard or Barcode is presented to reader" → Decision: "Is presented card readable?"
- Decision: "ABT
Valid AID?" → Decision: "ABT
Card is Expired?" [Yes
(VISA, Mastercard, Maestro)]
- Decision: "ABT
Card is Expired?" → Decision: "ABT
ODA Valid?" [No]
- Decision: "ABT
ODA Valid?" → Decision: "ABT
Is PAN  on BIN list?" [Valid]
- Decision: "ABT
Is PAN  on BIN list?" → Decision: "ABT
PAN on Deny List?" [No]
- Decision: "ABT
PAN on Deny List?" → Decision: "ABT
Has PAN been used within Passback Period?" [No]
- Decision: "ABT
Valid AID?" → Screen: "1.6.2 ABT deny list/negative list" [No
(American Express, etc)]
- Decision: "ABT
Card is Expired?" → Screen: "1.6.2 ABT deny list/negative list" [Yes]
- Decision: "ABT
ODA Valid?" → Screen: "1.6.2 ABT deny list/negative list" [No]
- Decision: "ABT
Is PAN  on BIN list?" → Screen: "1.6.2 ABT deny list/negative list" [Yes]
- Decision: "ABT
PAN on Deny List?" → Screen: "1.6.2 ABT deny list/negative list" [Yes]
- Decision: "Is presented card readable?" → Decision: "Is the presented 
smartcarda Legacy miFare or 
ABT EMV?" [Yes]
- Decision: "Is presented card readable?" → Screen: "1.6.3 ABT Error reading card" [No]
- Decision: "Is the presented 
smartcarda Legacy miFare or 
ABT EMV?" → Decision: "ABT
Valid AID?" [ABT]
- Decision: "ABT
Has PAN been used within Passback Period?" → Screen: "1.6.1.1 ABT Tag successful" [No]
- Decision: "ABT
Has PAN been used within Passback Period?" → Screen: "1.6.6 Passback - No Entry" [Yes]
- Decision: "Smartcard
Was Smartcard validation record successfully updated?" → Screen: "1.3.1 Represent Card" [No]
- Decision: "Smartcard
Is card blocked?" → Decision: "Smartcard
Is card on the Actionlist?" [No
]
- Decision: "Smartcard
Is card on the Actionlist?" → Decision: "Smartcard
Is smartcard product valid for current location?" [No]
- Decision: "Smartcard
Is smartcard product valid for current location?" → Decision: "Smartcard
Is smartcard valid at current time/date?" [Yes]
- Decision: "Smartcard
Is smartcard valid at current time/date?" → Decision: "Smartcard
Is smartcard expired?" [Yes]
- Decision: "Smartcard
Is smartcard expired?" → Decision: "Smartcard
Is smartcard within Passback period?" [No]
- Decision: "Smartcard
Is smartcard within Passback period?" → Decision: "Smartcard
Is smartcard within transfer period?" [No]
- Decision: "Smartcard
Is card blocked?" → Screen: "1.6.4 ABT Hot listed card" [Yes]
- Decision: "Smartcard
Is card on the Actionlist?" → Screen: "1.6.4 ABT Hot listed card" [Yes]
- Decision: "Smartcard
Is smartcard product valid for current location?" → Screen: "1.3.7 Not Valid At This Location" [No]
- Decision: "Smartcard
Is smartcard valid at current time/date?" → Screen: "1.3.8 Invalid Time Of Day" [No]
- Decision: "Smartcard
Is smartcard expired?" → Screen: "1.3.9 Product Expired" [Yes]
- Decision: "Smartcard
Is smartcard within Passback period?" → Screen: "1.4.3 Passback Journeys Left" [Yes]
- Decision: "Smartcard
Was Smartcard validation record successfully updated?" → Screen: "1.5.0 Tag successful" [Yes]
- Decision: "Is the presented 
smartcarda Legacy miFare or 
ABT EMV?" → Decision: "Smartcard
Is smartcard an
 operator card?" [Smartcard]
- Decision: "Barcode
Is barcode expired?" → Screen: "1.7.99.5 Barcode Validation Fail - Expired"
- Decision: "Barcode
Is barcode valid at current location?" → Screen: "1.7.99.4 Barcode Validation Fail - Location"
- Decision: "Barcode
Is barcode valid at current date/time" → Screen: "1.7.99.3 Barcode Validation Fail - Time"
- Decision: "Barcode
Is barcode valid on current route/service?" → Screen: "1.7.99.2 Barcode Validation Fail - Service"
- Decision: "Barcode
Is barcode valid on current route/service?" → Decision: "Barcode
Is barcode valid at current date/time"
- Decision: "Barcode
Is barcode valid at current date/time" → Decision: "Barcode
Is barcode valid at current location?"
- Decision: "Barcode
Is barcode valid at current location?" → Decision: "Barcode
Is barcode expired?"
- Decision: "Barcode
Is barcode expired?" → Decision: "Barcode
Has Barcode been used within Passback Period?"
- Decision: "Barcode
Has Barcode been used within Passback Period?" → Screen: "1.7.99.6 Barcode Validation Fail - Passback PV" [Yes]
- Decision: "Barcode
Has Barcode been used within Passback Period?" → Screen: "1.7.1.1 Barcode Validation Successful - Adult" [No]
- Decision: "Barcode
Is barcode readable?" → Decision: "Barcode
Is barcode valid on current route/service?"
- Decision: "Barcode
Is barcode readable?" → Screen: "1.3.16 Unable to Validate"
- Decision: "Smartcard or Barcode is presented to reader" → Decision: "Barcode
Is barcode readable?"
- Decision: "Is Validator/Plinth Commissioned?" → Screen: "1.2.1 Machine Not in Service" [No]
- Decision: "Is Validator/Plinth Commissioned?" → Screen: "1.2.1 Machine Not in Service" [Yes]
- Decision: "Smartcard
Is smartcard an
 operator card?" → Decision: "Smartcard
Is card blocked?" [No]
- Decision: "Smartcard
Is smartcard an
 operator card?" → Decision: "Does Operator ID match a Technician ID in Stafflist?" [Yes]
- Decision: "Does Operator ID match a Technician ID in Stafflist?" → Decision: "Device will not respond" [No]
- Decision: "Does Operator ID match a Technician ID in Stafflist?" → Decision: "See "Technician Menu" board
for Technician Sign-on." [Yes]
- Decision: "Smartcard
Is smartcard within transfer period?" → Screen: "1.5.0 Tag successful" [Yes]
- Decision: "Smartcard
Is smartcard within transfer period?" → Decision: "Smartcard
Was Smartcard validation record successfully updated?" [No]
- Decision: "Smartcard
Is smartcard within Passback period?" → Screen: "1.4.4 Passback Days Left "


## 5. Technician Menu - Platform Validator

### Screens (25)
- 1.0 Present SmartCard or Barcode
- 10.00.01 Technician Menu - Login Screen
- 10.00.02 Technician Menu -Enter PIN
- 11.00.00 Technician Menu - Home Screen
- 10.00.03 Technician Menu - Incorrect Details
- 11.05.02 Technician Menu - Network interfaces - Details
- 11.05.01 Technician Menu - Network Interfaces
- 11.01.01 Technician Menu - Location Settings
- 11.01.02 Technician Menu - Location Settings - Edit
- 11.01.03 Technician Menu - Location Settings - Edit - Clear
- 10.02.02 Technician Menu - Please Wait
- 10.02.01 Technician Menu - Sign Off
- 11.05.03 Technician Menu - Network interfaces - FecDetails
- 11.05.04 Technician Menu - Network interfaces -ChangeIP
- 11.05.05 Technician Menu - Network Routing Table
- 11.01.10 Technician Menu - Select Location
- 11.01.10 Technician Menu - Select Location - Selected
- 10.02.03 Technician Menu - Rebooting
- 11.01.05 Technician Menu - Location Settings - Fail
- 11.06.01 Technician Menu - Configuration Version
- 11.02.01 Technician Menu - Software Version
- 11.07.01 Technician Menu - Audio
- 11.03.01 Technician Menu - Brightness
- 10.02.02 Technician Menu - Please Wait
- 11.04.01 Technician Menu - Force communications

### Decision Points (11)
- Is the PIN valid  for the provided ID?
- Has the  Home Location  changed?
- Is the  Home Location list available?
- 11.00.00 Technician Menu - Home Screen
- 1.0 Present SmartCard or Barcode
- 11.00.00 Technician Menu - Home Screen
- 11.00.00 Technician Menu - Home Screen
- 11.00.00 Technician Menu - Home Screen
- 11.00.00 Technician Menu - Home Screen
- 11.00.00 Technician Menu - Home Screen
- 11.00.00 Technician Menu - Home Screen

### Annotations / Spec Notes (12)
- Presenting an Technician card will redirect user to Sign on page with the ID automatically entered and PIN field active.
- Location Settings
- Network Settings
- User will be able to enter/edit values by pressing the 'Change' button.  When in Edit mode the 'Stop Location', 'Install Point ID' and 'Mount ID' can be configured by selecting the relevant field and entering a number via the on-screen pin-pad.   To change the Home Location the user will press the 'Select' button and choose from a list of available Home Locations provided on request from the BackOffice.  When a new Home Location is selected a reboot will be necessary to perform the update.
- The error message will disapear after a short timeout.
- Configuration Versions
- Software Versions
- Audio
- Brightness
- The Brightness page allows teh technician to make adjustments tot eh PV screen brightness. The 'Mode' displayed indicates whether the PV has been configured manually or is configured to automatically adapt to environmental light conditions as detected via the built-in light sensor.
- Force Communications
- The Force Communications page will summarize the following details:     1. How many Audit Records are pending delivery to the back office.     2. The last date/time that an Audit Record was successfully sent     3. The last date/time a manifest download was attempted     4. The last date/time a manifest download was successful     5. A count of pending files to download for software/configuration updates.  Pressing the 'Call Now' button will trigger a check of the manifest in the back office and attempt to send any pending audit records.   Pressing the 'Refresh' button will update the values displayed with the most recent information.

### Connections / Flow (56)
- Screen: "1.0 Present SmartCard or Barcode" → Screen: "10.00.01 Technician Menu - Login Screen" [Valid Technician Card 
is presented to the Validator]
- Decision: "Is the PIN valid 
for the provided ID?" → Screen: "11.00.00 Technician Menu - Home Screen" [Yes]
- Screen: "11.01.01 Technician Menu - Location Settings" → Screen: "11.01.02 Technician Menu - Location Settings - Edit"
- Screen: "10.00.01 Technician Menu - Login Screen" → Screen: "1.0 Present SmartCard or Barcode"
- Screen: "11.00.00 Technician Menu - Home Screen" → Screen: "10.02.01 Technician Menu - Sign Off"
- Screen: "10.02.01 Technician Menu - Sign Off" → Screen: "11.00.00 Technician Menu - Home Screen"
- Screen: "10.00.01 Technician Menu - Login Screen" → Screen: "10.00.02 Technician Menu -Enter PIN" [User Enters PIN]
- Screen: "10.00.02 Technician Menu -Enter PIN" → Screen: "1.0 Present SmartCard or Barcode"
- Screen: "10.00.01 Technician Menu - Login Screen" → Decision: "Is the PIN valid 
for the provided ID?"
- Screen: "10.00.02 Technician Menu -Enter PIN" → Decision: "Is the PIN valid 
for the provided ID?"
- Screen: "10.00.02 Technician Menu -Enter PIN" → Screen: "10.00.01 Technician Menu - Login Screen"
- Decision: "Is the PIN valid 
for the provided ID?" → Screen: "10.00.03 Technician Menu - Incorrect Details" [No]
- Screen: "10.00.03 Technician Menu - Incorrect Details" → Screen: "1.0 Present SmartCard or Barcode"
- Screen: "10.00.03 Technician Menu - Incorrect Details" → Decision: "Is the PIN valid 
for the provided ID?"
- Screen: "10.02.01 Technician Menu - Sign Off" → Screen: "1.0 Present SmartCard or Barcode"
- Screen: "11.00.00 Technician Menu - Home Screen" → Screen: "11.01.01 Technician Menu - Location Settings"
- Screen: "11.00.00 Technician Menu - Home Screen" → Screen: "11.02.01 Technician Menu - Software Version"
- Screen: "11.00.00 Technician Menu - Home Screen" → Screen: "11.03.01 Technician Menu - Brightness"
- Screen: "11.00.00 Technician Menu - Home Screen" → Screen: "11.04.01 Technician Menu - Force communications"
- Screen: "11.01.02 Technician Menu - Location Settings - Edit" → Screen: "11.01.03 Technician Menu - Location Settings - Edit - Clear"
- Screen: "11.01.02 Technician Menu - Location Settings - Edit" → Screen: "11.01.01 Technician Menu - Location Settings"
- Screen: "11.01.03 Technician Menu - Location Settings - Edit - Clear" → Screen: "11.01.01 Technician Menu - Location Settings"
- Screen: "11.01.03 Technician Menu - Location Settings - Edit - Clear" → Decision: "Is the 
Home Location list available?"
- Screen: "11.02.01 Technician Menu - Software Version" → Decision: "11.00.00 Technician Menu - Home Screen"
- Screen: "11.00.00 Technician Menu - Home Screen" → Screen: "11.05.01 Technician Menu - Network Interfaces"
- Screen: "11.00.00 Technician Menu - Home Screen" → Screen: "11.06.01 Technician Menu - Configuration Version"
- Screen: "11.00.00 Technician Menu - Home Screen" → Screen: "11.07.01 Technician Menu - Audio"
- Screen: "11.01.01 Technician Menu - Location Settings" → Decision: "11.00.00 Technician Menu - Home Screen"
- Screen: "11.03.01 Technician Menu - Brightness" → Decision: "11.00.00 Technician Menu - Home Screen"
- Screen: "11.01.02 Technician Menu - Location Settings - Edit" → Decision: "Is the 
Home Location list available?"
- Screen: "11.01.10 Technician Menu - Select Location" → Screen: "11.01.02 Technician Menu - Location Settings - Edit"
- Decision: "Is the 
Home Location list available?" → Screen: "11.01.10 Technician Menu - Select Location" [Yes]
- Decision: "Has the
 Home Location 
changed?" → Screen: "11.01.01 Technician Menu - Location Settings" [No]
- Screen: "10.02.02 Technician Menu - Please Wait" → Decision: "Has the
 Home Location 
changed?"
- Decision: "Has the
 Home Location 
changed?" → Screen: "10.02.03 Technician Menu - Rebooting" [Yes]
- Screen: "10.02.03 Technician Menu - Rebooting" → Decision: "1.0 Present SmartCard or Barcode" [Device will reboot]
- Screen: "11.04.01 Technician Menu - Force communications" → Screen: "10.02.02 Technician Menu - Please Wait"
- Screen: "10.02.02 Technician Menu - Please Wait" → Screen: "11.04.01 Technician Menu - Force communications"
- Screen: "11.05.01 Technician Menu - Network Interfaces" → Screen: "11.05.02 Technician Menu - Network interfaces - Details"
- Screen: "11.05.01 Technician Menu - Network Interfaces" → Screen: "11.05.03 Technician Menu - Network interfaces - FecDetails"
- Screen: "11.05.03 Technician Menu - Network interfaces - FecDetails" → Screen: "11.05.04 Technician Menu - Network interfaces -ChangeIP"
- Screen: "11.01.10 Technician Menu - Select Location" → Screen: "11.01.10 Technician Menu - Select Location - Selected"
- Screen: "11.01.10 Technician Menu - Select Location - Selected" → Screen: "11.01.02 Technician Menu - Location Settings - Edit"
- Screen: "11.01.03 Technician Menu - Location Settings - Edit - Clear" → Screen: "10.02.02 Technician Menu - Please Wait"
- Decision: "Is the 
Home Location list available?" → Screen: "11.01.05 Technician Menu - Location Settings - Fail" [No]
- Screen: "11.01.05 Technician Menu - Location Settings - Fail" → Screen: "11.01.02 Technician Menu - Location Settings - Edit"
- Screen: "11.01.05 Technician Menu - Location Settings - Fail" → Decision: "Is the 
Home Location list available?"
- Screen: "11.01.10 Technician Menu - Select Location - Selected" → Screen: "11.01.03 Technician Menu - Location Settings - Edit - Clear"
- Screen: "11.05.01 Technician Menu - Network Interfaces" → Screen: "11.05.05 Technician Menu - Network Routing Table"
- Screen: "11.05.05 Technician Menu - Network Routing Table" → Screen: "11.05.01 Technician Menu - Network Interfaces"
- Screen: "11.05.03 Technician Menu - Network interfaces - FecDetails" → Screen: "11.05.01 Technician Menu - Network Interfaces"
- Screen: "11.05.02 Technician Menu - Network interfaces - Details" → Screen: "11.05.01 Technician Menu - Network Interfaces"
- Screen: "11.04.01 Technician Menu - Force communications" → Decision: "11.00.00 Technician Menu - Home Screen"
- Screen: "11.07.01 Technician Menu - Audio" → Decision: "11.00.00 Technician Menu - Home Screen"
- Screen: "11.06.01 Technician Menu - Configuration Version" → Decision: "11.00.00 Technician Menu - Home Screen"
- Screen: "11.05.01 Technician Menu - Network Interfaces" → Decision: "11.00.00 Technician Menu - Home Screen"


---

# Additional Boards (not in main navigation list — older/archived or draft versions)


## Platform Validator (extra/archived board)

### Screens (27)
- 1.0 Present SmartCard
- 1.1 Present SmartCard no Tickets
- 1.2 Present Ticket no SmartCard
- 1.2.1 Machine Not in Service
- 1.2.2 Entering Service
- 1.2.3 Entering Technician Menu
- 1.6.4 ABT Hot listed card
- 1.3.11 No Journeys Left
- 1.3.15 No Days Left 
- 1.3.1 Represent Card
- 1.3.2 Card Not Yet Valid
- 1.3.3 Invalid Card
- 1.3.5 Please Try Again
- 1.3.7 Not Valid At This Location
- 1.3.8 Invalid Time Of Day
- 1.3.9 Product Expired
- 1.3.13 Faulty card
- 1.4.1 Passback proceed
- 1.4.3 Passback Journeys Left
- 1.4.2 Passback Expires
- 1.4.4 Passback Days Left 
- 1.5.4 Tag successful expires
- 1.5.2 Tag successful travel limit
- 1.5.3 Tag successful days left
- 1.6.1.1 ABT Tag successful
- 1.6.2 ABT deny list/negative list
- 1.6.3 ABT Error reading card

### Decision Points (9)
- Main screen
- Error section
- Main screen
- Passback
- Main screen
- Successful Tag-On
- Main screen
- ABT Cards
- Main screen

### Annotations / Spec Notes (6)
- Platform Validator
- Barcode Specific screens: 1.0; 1.1; 1.2; 1.3.5; 1.3.7; 1.3.9; 1.3.16; 1.5.4
- Glider PV only screens
- Glider PV only screens
- Glider PV only screens
- Cases in which this screen will be displayed 1) Unsupported cEMV card e.g. AMEX 2) Card Clash 3) Expired cEMV card 4) BIN on cEMV card invalid 5) AID check invalid 6) ODA check not ok 7) Deny list 8) Negative list

### Connections / Flow (53)
- Screen: "1.3.1 Represent Card" → Decision: "Main screen"
- Screen: "1.2.3 Entering Technician Menu" → Decision: "Main screen"
- Screen: "1.0 Present SmartCard" → Screen: "1.3.9 Product Expired" [If the product on card expired]
- Screen: "1.0 Present SmartCard" → Screen: "1.2.2 Entering Service" [Validator entering service]
- Screen: "1.0 Present SmartCard" → Screen: "1.2.3 Entering Technician Menu" [When when technican presents smartcard to enter technician menu]
- Screen: "1.2.2 Entering Service" → Decision: "Main screen"
- Screen: "1.3.13 Faulty card" → Decision: "Main screen"
- Screen: "1.3.3 Invalid Card" → Decision: "Main screen"
- Screen: "1.0 Present SmartCard" → Screen: "1.3.2 Card Not Yet Valid" [If the card is not yet valid]
- Screen: "1.2.1 Machine Not in Service" → Decision: "Main screen"
- Screen: "1.3.8 Invalid Time Of Day" → Decision: "Main screen"
- Screen: "1.3.5 Please Try Again" → Decision: "Main screen"
- Screen: "1.0 Present SmartCard" → Screen: "1.3.1 Represent Card" [If the validator has detected an "unsafe transaction"]
- Screen: "1.0 Present SmartCard" → Screen: "1.3.13 Faulty card" [If the card is faulty]
- Screen: "1.3.2 Card Not Yet Valid" → Decision: "Main screen"
- Screen: "1.0 Present SmartCard" → Screen: "1.2.1 Machine Not in Service" [If the validator is not in service]
- Screen: "1.0 Present SmartCard" → Screen: "1.3.5 Please Try Again" [Card misread or Error Updating card]
- Screen: "1.0 Present SmartCard" → Screen: "1.3.8 Invalid Time Of Day"
- Screen: "1.3.7 Not Valid At This Location" → Decision: "Main screen"
- Screen: "1.0 Present SmartCard" → Screen: "1.3.7 Not Valid At This Location" [If not supported card is taged]
- Screen: "1.3.9 Product Expired" → Decision: "Main screen"
- Screen: "1.0 Present SmartCard" → Screen: "1.3.3 Invalid Card" [If the card is invalid
Customer presents a card to a BV which is not acEMV or ABT card]
- Screen: "1.0 Present SmartCard" → Screen: "1.6.2 ABT deny list/negative list" [Card on deny list/negative list]
- Screen: "1.6.1.1 ABT Tag successful" → Decision: "Main screen"
- Screen: "1.6.3 ABT Error reading card" → Decision: "Main screen"
- Screen: "1.0 Present SmartCard" → Screen: "1.6.1.1 ABT Tag successful" [Succesful Tag]
- Screen: "1.0 Present SmartCard" → Screen: "1.6.4 ABT Hot listed card" [Hot listed card ]
- Screen: "1.6.3 ABT Error reading card" → Decision: "Main screen"
- Screen: "1.0 Present SmartCard" → Screen: "1.6.3 ABT Error reading card" [Error reading ABT card]
- Screen: "1.0 Present SmartCard" → Screen: "1.4.2 Passback Expires" [Ilink, Smartlink Travelcards, aLink tag]
- Screen: "1.4.2 Passback Expires" → Decision: "Main screen"
- Screen: "1.0 Present SmartCard" → Screen: "1.5.4 Tag successful expires" [Ilink, Smartlink Travelcards, aLink tag]
- Screen: "1.5.4 Tag successful expires" → Decision: "Main screen"
- Screen: "1.0 Present SmartCard" → Screen: "1.4.1 Passback proceed" [ABT passback]
- Screen: "1.4.1 Passback proceed" → Decision: "Main screen"
- Screen: "1.6.2 ABT deny list/negative list" → Decision: "Main screen"
- Screen: "1.6.4 ABT Hot listed card" → Decision: "Main screen"
- Screen: "1.0 Present SmartCard" → Screen: "1.3.11 No Journeys Left" [If there are no journeys left]
- Screen: "1.0 Present SmartCard" → Screen: "1.3.15 No Days Left " [If there are no Days left]
- Screen: "1.3.11 No Journeys Left" → Decision: "Main screen"
- Screen: "1.3.15 No Days Left " → Decision: "Main screen"
- Screen: "1.0 Present SmartCard" → Screen: "1.4.3 Passback Journeys Left" [Smartlink Multi Journey cards tag ]
- Screen: "1.0 Present SmartCard" → Screen: "1.4.4 Passback Days Left " [DayLink Cards]
- Screen: "1.4.3 Passback Journeys Left" → Decision: "Main screen"
- Screen: "1.4.4 Passback Days Left " → Decision: "Main screen"
- Screen: "1.0 Present SmartCard" → Screen: "1.5.2 Tag successful travel limit" [Smartlink Multi Journey cards tag ]
- Screen: "1.0 Present SmartCard" → Screen: "1.5.3 Tag successful days left" [DayLink cards tag ]
- Screen: "1.5.2 Tag successful travel limit" → Decision: "Main screen"
- Screen: "1.5.3 Tag successful days left" → Decision: "Main screen"
- Screen: "1.0 Present SmartCard" → Screen: "1.1 Present SmartCard no Tickets" [If barcode reader is faulty / inoperable]
- Screen: "1.0 Present SmartCard" → Screen: "1.2 Present Ticket no SmartCard" [If card reader is faulty / inoperable]
- Screen: "1.1 Present SmartCard no Tickets" → Screen: "1.0 Present SmartCard"
- Screen: "1.2 Present Ticket no SmartCard" → Screen: "1.0 Present SmartCard"


## Gate Validator (extra/archived board)

### Screens (59)
- 1.0.1 Present SmartCard or Barcode
- 1.1 Present SmartCard no Tickets
- 1.2 Present Ticket no SmartCard
- 1.2.8 Machine Not in Service (Gate)
- 1.2.2 Entering Service
- 1.2.3 Entering Technician Menu
- 1.2.4 Emergency Exit
- 1.2.5 Please Proceed
- 1.2.6 No Entry
- 1.2.9 Bi-directional screen
- 1.3.1 Represent Card
- 1.3.3 Invalid Card
- 1.3.5 Please Try Again
- 1.3.7 Not Valid At This Location
- 1.3.8 Invalid Time Of Day
- 1.3.9 Product Expired
- 1.3.13 Faulty card
- 1.6.4 ABT Hot listed card
- 1.3.16 Unable to Validate
- 1.4.9 Passback - No Entry
- 1.5.4 Tag successful expires
- 1.6.1.1 ABT Tag successful
- 1.6.2 ABT deny list/negative list
- 1.6.3 ABT Error reading card
- 1.7.1.1 Barcode Validation Successful - Adult
- 1.7.99.1 Barcode Validation Fail - Passback
- 1.7.99.2 Barcode Validation Fail - Service
- 1.7.99.3 Barcode Validation Fail - Time
- 1.7.99.4 Barcode Validation Fail - Location
- 1.7.99.5 Barcode Validation Fail - Expired
- Validator  Copy 3
- Validator  Copy 3
- Validator  Copy 2
- Validator  Copy 4
- Validator  Copy 4
- Validator  Copy 2
- Validator  Copy 2
- Validator  Copy 3
- Validator  Copy 3
- Validator  Copy 2
- Validator  Copy 2
- 1.0.1 Present SmartCard or Barcode
- 1.2.6 No Entry
- 1.0.1 Present SmartCard or Barcode
- 1.0.1 Present SmartCard or Barcode
- 1.2.6 No Entry
- 1.2.6 No Entry
- 1.2.5 Please Proceed
- 1.2.5 Please Proceed
- 1.6.2 ABT deny list/negative list
- 1.2.9 Bi-directional screen
- Validator  Copy 3
- Validator  Copy 2
- 1.2.9 Bi-directional screen
- 1.5.4 Tag successful expires
- Validator  Copy 3
- Validator  Copy 2
- 1.2.4 Emergency Exit
- 1.2.6 No Entry

### Decision Points (10)
- Main screen
- Error section
- Main screen
- Passback
- Main screen
- Successful Tag-On
- Main screen
- ABT Cards
- Main screen
- Multi-Use Barcodes

### Annotations / Spec Notes (32)
- Gate Validator
- Audible Messages for Gate Validator
- Message 1 (Success message)  1.5.4 Successful Expires 1.4.2. Passback Expires   Message 2 (Retry or seek assistance message)  1.3.5 Please try again   Message 3 - (Seek Assistance message)  1.6.4 Hotlisted Card 1.3.13 Faulty Card 1.3.9 - Product Expired   Audible messages will only play for the following:
- Card Type
- Sub-Product Type
- Local Rail
- Cross Border
- Free Smartpass
- Blind Smartpass
- Blind Single
- Blind XB Single
- Blind XB Day Return
- Blind XB 1 Mth Return
- Part Sight Single
- N/A – not accepted for Rail Cross Border travel
- Half-Fare Smartpass
- Partially Sighted
- Part Sight Return
- Barcode Specific screens: 1.0; 1.1; 1.2; 1.3.5; 1.3.7; 1.3.9; 1.3.16; 1.5.4
- Cases in which this screen will be displayed 1) Unsupported cEMV card e.g. AMEX 2) Card Clash 3) Expired cEMV card 4) BIN on cEMV card invalid 5) AID check invalid 6) ODA check not ok 7) Deny list 8) Negative list
- Gate Validator Layout Description
- Screen Display
- If one of readers (Card Validator or Barcode Reader) is not working. Gate Validator will be still partially working. It will display appropriate screen: 1.1 or 1.2
- Card Validator
- Barcode Reader
- Pictogram
- Active Gates (Non Bi-Directional)
- Inactive Gates (Bi-Directional)
- Active Gates (Bi-Directional)
- Forced Open (Bi-Directional)
- One side gets an error screen (Bi-Directional)
- Gates are opened by external emergancy button

### Connections / Flow (55)
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.2.9 Bi-directional screen" [On a bi-directional gate when on one
gate user presents card
]
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.3.8 Invalid Time Of Day" [If the card is for different time of day]
- Screen: "1.6.2 ABT deny list/negative list" → Decision: "Main screen"
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.2.4 Emergency Exit" [Exit validator when in 'emergency exit'
mode
]
- Screen: "1.3.8 Invalid Time Of Day" → Decision: "Main screen"
- Screen: "1.2.9 Bi-directional screen" → Decision: "Main screen"
- Screen: "1.2 Present Ticket no SmartCard" → Screen: "1.0.1 Present SmartCard or Barcode"
- Screen: "1.2.6 No Entry" → Decision: "Main screen"
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.3.13 Faulty card" [If the card is faulty]
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.2.5 Please Proceed" [Validator when in 'Fully Free' mode]
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.2.8 Machine Not in Service (Gate)" [If the validator is not in service]
- Screen: "1.3.1 Represent Card" → Decision: "Main screen"
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.1 Present SmartCard no Tickets" [If barcode reader is faulty / inoperable
]
- Screen: "1.3.9 Product Expired" → Decision: "Main screen"
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.3.9 Product Expired" [If the product on card expired]
- Screen: "1.6.3 ABT Error reading card" → Decision: "Main screen"
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.3.5 Please Try Again" [Card misread or Error Updating card]
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.6.4 ABT Hot listed card" [Hot listed card ]
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.3.3 Invalid Card" [If the card is invalid
]
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.3.1 Represent Card" [If the validator has detected an "unsafe transaction"]
- Screen: "1.2.5 Please Proceed" → Decision: "Main screen"
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.2 Present Ticket no SmartCard" [If card reader is faulty / inoperable
]
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.6.1.1 ABT Tag successful" [Successful Tag-On]
- Screen: "1.2.8 Machine Not in Service (Gate)" → Decision: "Main screen"
- Screen: "1.2.3 Entering Technician Menu" → Decision: "Main screen"
- Screen: "1.2.4 Emergency Exit" → Decision: "Main screen"
- Screen: "Validator  Copy 4" → Screen: "Validator  Copy 3" [Card is presented by user]
- Screen: "1.6.1.1 ABT Tag successful" → Decision: "Main screen"
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.2.3 Entering Technician Menu" [When when technican presents smartcard to enter technician menu]
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.6.3 ABT Error reading card" [Error reading ABT card]
- Screen: "1.3.3 Invalid Card" → Decision: "Main screen"
- Screen: "1.3.5 Please Try Again" → Decision: "Main screen"
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.6.2 ABT deny list/negative list" [Card on deny list/negative list]
- Screen: "1.1 Present SmartCard no Tickets" → Screen: "1.0.1 Present SmartCard or Barcode"
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.2.6 No Entry" [When the aisle controlled by this validator is closed
(includes entry validator when gate is in 'emergency exit' mode)
]
- Screen: "1.3.7 Not Valid At This Location" → Decision: "Main screen"
- Screen: "1.2.2 Entering Service" → Decision: "Main screen"
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.2.2 Entering Service" [Validator entering service]
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.3.7 Not Valid At This Location" [If not supported card is taged]
- Screen: "1.3.13 Faulty card" → Decision: "Main screen"
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.4.9 Passback - No Entry" [Ilink, Smartlink Travelcards, aLink tag]
- Screen: "1.4.9 Passback - No Entry" → Decision: "Main screen"
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.5.4 Tag successful expires" [Ilink, Smartlink Travelcards, aLink tag]
- Screen: "1.5.4 Tag successful expires" → Decision: "Main screen"
- Screen: "Validator  Copy 4" → Screen: "Validator  Copy 2"
- Screen: "1.3.16 Unable to Validate" → Decision: "Main screen"
- Screen: "1.0.1 Present SmartCard or Barcode" → Screen: "1.3.16 Unable to Validate" [Barcode reader unable to validate]
- Screen: "1.6.4 ABT Hot listed card" → Decision: "Main screen"
- Screen: "1.0.1 Present SmartCard or Barcode" → Decision: "Multi-Use Barcodes"
- Decision: "Multi-Use Barcodes" → Screen: "1.7.1.1 Barcode Validation Successful - Adult" [Barcode Use
]
- Decision: "Multi-Use Barcodes" → Screen: "1.7.99.1 Barcode Validation Fail - Passback" [Barcode already validated
(passback)]
- Decision: "Multi-Use Barcodes" → Screen: "1.7.99.2 Barcode Validation Fail - Service" [Barcode is not valid on the 
current route/service]
- Decision: "Multi-Use Barcodes" → Screen: "1.7.99.3 Barcode Validation Fail - Time" [Barcode is not valid at 
current time]
- Decision: "Multi-Use Barcodes" → Screen: "1.7.99.4 Barcode Validation Fail - Location" [Barcode is not valid at 
current location]
- Decision: "Multi-Use Barcodes" → Screen: "1.7.99.5 Barcode Validation Fail - Expired" [Barcode has expired]


## Bus Validator (extra/archived board)

### Screens (15)
- 1.0 Present SmartCard or Barcode
- 1.1.2 Wait for Stop
- 1.2.7 Machine Not in Service (Bus)
- 1.2.3 Entering Technician Menu
- 1.1.2.1 Invalid Wait for Stop
- 1.2.2 Entering Service
- 1.3.3 Invalid Card
- 1.3.1 Represent Card
- 1.3.5 Please Try Again
- 1.3.13 Faulty card
- 1.6.4 ABT Hot listed card
- 1.4.1 Passback proceed
- 1.6.3 ABT Error reading card
- 1.6.1.0 ABT Tag successful
- 1.6.2 ABT deny list/negative list

### Decision Points (8)
- Main screen
- Main screen
- Error section
- Main screen
- Passback
- Main screen
- ABT Cards
- Main screen

### Annotations / Spec Notes (2)
- Bus Validator
- Cases in which this screen will be displayed 1) Unsupported cEMV card e.g. AMEX 2) Card Clash 3) Expired cEMV card 4) BIN on cEMV card invalid 5) AID check invalid 6) ODA check not ok 7) Deny list 8) Negative list

### Connections / Flow (28)
- Screen: "1.3.1 Represent Card" → Decision: "Main screen"
- Screen: "1.0 Present SmartCard or Barcode" → Screen: "1.6.2 ABT deny list/negative list" [Card on deny list/negative list]
- Screen: "1.3.5 Please Try Again" → Decision: "Main screen"
- Screen: "1.2.7 Machine Not in Service (Bus)" → Decision: "Main screen" [Error resolved]
- Screen: "1.0 Present SmartCard or Barcode" → Screen: "1.3.1 Represent Card" [If the validator has detected an "unsafe transaction"]
- Screen: "1.0 Present SmartCard or Barcode" → Screen: "1.2.3 Entering Technician Menu" [When when technican presents smartcard to enter technician menu]
- Screen: "1.6.3 ABT Error reading card" → Decision: "Main screen"
- Screen: "1.0 Present SmartCard or Barcode" → Screen: "1.3.5 Please Try Again" [Card misread or Error Updating card]
- Screen: "1.0 Present SmartCard or Barcode" → Screen: "1.3.3 Invalid Card" [If the card is invalid
]
- Screen: "1.2.7 Machine Not in Service (Bus)" → Screen: "1.2.2 Entering Service" [Validator entering service]
- Screen: "1.1.2 Wait for Stop" → Decision: "Main screen" [Bus enters a bus stop footprint]
- Screen: "1.1.2.1 Invalid Wait for Stop" → Screen: "1.1.2 Wait for Stop"
- Screen: "1.1.2 Wait for Stop" → Screen: "1.1.2.1 Invalid Wait for Stop" [If a valid card is presented
to the BV the 'Invalid Wait for Stop' error
is shown
]
- Screen: "1.3.13 Faulty card" → Decision: "Main screen"
- Screen: "1.0 Present SmartCard or Barcode" → Screen: "1.1.2 Wait for Stop" [When the bus is not in a bus stop footprint
BV goes into a disabled mode
]
- Screen: "1.2.3 Entering Technician Menu" → Decision: "Main screen"
- Screen: "1.2.2 Entering Service" → Decision: "Main screen"
- Screen: "1.6.3 ABT Error reading card" → Decision: "Main screen"
- Screen: "1.0 Present SmartCard or Barcode" → Screen: "1.3.13 Faulty card" [If the card is faulty]
- Screen: "1.4.1 Passback proceed" → Decision: "Main screen"
- Screen: "1.0 Present SmartCard or Barcode" → Screen: "1.2.7 Machine Not in Service (Bus)" [If the validator is not in service]
- Screen: "1.0 Present SmartCard or Barcode" → Screen: "1.6.4 ABT Hot listed card" [Hot listed card ]
- Screen: "1.0 Present SmartCard or Barcode" → Screen: "1.6.1.0 ABT Tag successful" [Succesful Tag]
- Screen: "1.0 Present SmartCard or Barcode" → Screen: "1.4.1 Passback proceed" [ABT passback]
- Screen: "1.6.1.0 ABT Tag successful" → Decision: "Main screen"
- Screen: "1.3.3 Invalid Card" → Decision: "Main screen"
- Screen: "1.0 Present SmartCard or Barcode" → Screen: "1.6.3 ABT Error reading card" [Error reading ABT card]
- Screen: "1.6.4 ABT Hot listed card" → Decision: "Main screen"


## Audible Messages for Gate Validator (extra/archived board)

### Screens (0)

### Decision Points (0)

### Annotations / Spec Notes (17)
- Audible Messages
- Message 1 (Success message)  1.5.4 Successful Expires 1.4.2. Passback Expires   Message 2 (Retry or seek assistance message)  1.3.5 Please try again   Message 3 - (Seek Assistance message)  1.6.4 Hotlisted Card 1.3.13 Faulty Card 1.3.9 - Product Expired   Audible messages will only play for the following:
- Card Type
- Sub-Product Type
- Local Rail
- Cross Border
- Free Smartpass
- Blind Smartpass
- Blind Single
- Blind XB Single
- Blind XB Day Return
- Blind XB 1 Mth Return
- Part Sight Single
- N/A – not accepted for Rail Cross Border travel
- Half-Fare Smartpass
- Partially Sighted
- Part Sight Return

### Connections / Flow (0)


## Technician Menu (extra/archived board)

### Screens (22)
- 1.0 Present SmartCard or Barcode
- 0.0 Technician Menu - Login screen
- 0.1 Technician Menu - Enter PIN
- 1.0 Technician Menu - Home screen
- 1.7.1 Technician Menu - Incorrect Detiles
- 1.8.0 Technician Menu - Sign Off
- 1.1.1 Technician Menu - Location setting
- 1.2.1 Technician Menu - Network Interfaces
- 1.3.1 Technician Menu - Software Version
- 1.3.1 Technician Menu - Software Version Copy
- 1.4.1 Technician Menu - Force communications
- 1.0 Technician Menu - Home screen Copy
- 1.5.1 Technician Menu - Brightness
- 1.6.1 Technician Menu - Audio
- 1.0 Present SmartCard or Barcode
- 1.1.2 Technician Menu - Location setting - Edit
- 1.7.1 Technician Menu - Configuration Version
- 1.8.0 Technician Menu - Please Wait
- 1.1.2 Technician Menu - Location setting - Edit- selected
- 1.1.3 Technician Menu - Location setting - Edit- Clear
- 1.1.3 Technician Menu - Location setting - Edit- Input
- 1.1.4 Technician Menu - Location setting Edited

### Decision Points (1)
- Are the ID and PIN valid?

### Annotations / Spec Notes (17)
- Presenting an Technician card will redirect user to Sign on page with the ID automatically entered and PIN field active.
- User is able to navigate to the specific items in the menu by pressing the corresponding button.
- Unless otherwise specified, the back button will take you back to the previous screen.
- User presses Enter.
- User enters PIN.
- Pressing the call now button would trigger a check of the manifest in the back office and attempt to send audit files if they exist on the device. This would update the pending configuration files count and the pending audit files count. Refreshing the page will then update the count of these types of files to show how many of these items have been uploaded/downloaded.
- No
- Pressing "Sign Off" will show user another screen that will require confirmation, before actually signing off.
- User will be able to incrementaly set brightness
- User will be able to incrementaly set and volume and perform test of the volume loudness
- Options on this screen will depend on type of the device
- The fields on this screen don't update automatically so would need a refresh. Either refresh or go back (has the same effect).
- User will be redirected to PIN field active accordingly (if he tried to Sign On automatically presenting Card) after 3 seconds or by pressing Enter button.
- Pressing refresh will retrieve information from the server and update information to the latest values.
- User will be able to enter/edit values by pressing change button
- User can scroll row by row
- User will be able to enter/edit Tray ID using numerical buttons.

### Connections / Flow (27)
- Screen: "1.0 Present SmartCard or Barcode" → Screen: "0.0 Technician Menu - Login screen"
- Screen: "0.0 Technician Menu - Login screen" → Screen: "0.1 Technician Menu - Enter PIN"
- Screen: "0.1 Technician Menu - Enter PIN" → Decision: "Are the ID and
PIN valid?"
- Decision: "Are the ID and
PIN valid?" → Screen: "1.7.1 Technician Menu - Incorrect Detiles"
- Decision: "Are the ID and
PIN valid?" → Screen: "1.0 Technician Menu - Home screen"
- Screen: "1.1.1 Technician Menu - Location setting" → Screen: "1.1.2 Technician Menu - Location setting - Edit"
- Screen: "1.0 Technician Menu - Home screen" → Screen: "1.1.1 Technician Menu - Location setting"
- Screen: "1.1.2 Technician Menu - Location setting - Edit" → Screen: "1.1.2 Technician Menu - Location setting - Edit- selected"
- Screen: "1.1.2 Technician Menu - Location setting - Edit- selected" → Screen: "1.1.3 Technician Menu - Location setting - Edit- Clear"
- Screen: "1.1.3 Technician Menu - Location setting - Edit- Clear" → Screen: "1.1.3 Technician Menu - Location setting - Edit- Input"
- Screen: "1.1.3 Technician Menu - Location setting - Edit- Input" → Screen: "1.1.4 Technician Menu - Location setting Edited"
- Screen: "1.0 Technician Menu - Home screen" → Screen: "1.2.1 Technician Menu - Network Interfaces"
- Screen: "1.0 Technician Menu - Home screen" → Screen: "1.3.1 Technician Menu - Software Version"
- Screen: "1.0 Technician Menu - Home screen" → Screen: "1.3.1 Technician Menu - Software Version Copy"
- Screen: "1.0 Technician Menu - Home screen" → Screen: "1.4.1 Technician Menu - Force communications"
- Screen: "1.0 Technician Menu - Home screen" → Screen: "1.0 Technician Menu - Home screen Copy"
- Screen: "1.0 Technician Menu - Home screen" → Screen: "1.5.1 Technician Menu - Brightness"
- Screen: "1.0 Technician Menu - Home screen" → Screen: "1.6.1 Technician Menu - Audio"
- Screen: "0.0 Technician Menu - Login screen" → Screen: "1.0 Present SmartCard or Barcode"
- Screen: "0.1 Technician Menu - Enter PIN" → Screen: "1.0 Present SmartCard or Barcode"
- Screen: "1.0 Technician Menu - Home screen" → Screen: "1.8.0 Technician Menu - Sign Off"
- Screen: "1.8.0 Technician Menu - Sign Off" → Screen: "1.0 Present SmartCard or Barcode"
- Screen: "1.3.1 Technician Menu - Software Version" → Screen: "1.7.1 Technician Menu - Configuration Version"
- Screen: "1.8.0 Technician Menu - Sign Off" → Screen: "1.0 Technician Menu - Home screen"
- Screen: "1.4.1 Technician Menu - Force communications" → Screen: "1.8.0 Technician Menu - Please Wait"
- Screen: "1.4.1 Technician Menu - Force communications" → Screen: "1.8.0 Technician Menu - Please Wait"
- Screen: "1.8.0 Technician Menu - Please Wait" → Screen: "1.4.1 Technician Menu - Force communications"
