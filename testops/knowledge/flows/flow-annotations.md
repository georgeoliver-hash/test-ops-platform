# Flow annotations — extracted from Overflow (overflow_data.json)

## 1.0 Sign On
_13 note(s); branch labels: NO, Sign On, YES_

- If Message of the Day is available, The specific Page will be displayed.
- Presenting Card will redirect User to Sign On Page with the ID automatically entered and Pin field active.
- If the Device cannot establish a correct Communication it will be locked and present a screen with an Error Message and "Please Notify a Supervisor or Technician".
- If Message of the Day is not Available, User will be taken to an error screen.
- User will be redirected to ID field active (if he tried to Sign On manually entering ID) or PIN field active accordingly (if he tried to Sign On automatically presenting Card) after 3 seconds or by pressing Enter button.
- If Word and Coulour of the Day is available, The specific Page will be displayed.
- Pressing 'C' button will delete 1 character at a time. If the field is empty it will switch to the previous field.
- If User enters an incorrect Pin for more than the allowed number of attempts, the Device will become locked and will require a Supervisor Card to unlock.
- If Word and Colour of the Day is not Available, User will be taken to an error screen.
- If User doesn't present Card, he has to Press Any Key to progress to Sign On Page with ID field active.
- POS will display this screen whilst it is loading. In normal operating conditions with a good network connection this screen will be shown for a minimal period.
- Pressing any key will send operator to main screen.
- Metro Operator will go to this screen after Sign On.

## 10.0 Supervisor
_17 note(s); branch labels: No, Supervisor, User enters ID., User enters PIN., User presses Enter., Yes_

- Day information details are displayed with an option to print. The duty numbers will be sequential and increase by 1 each duty.
- User is able to select any of the duties by pressing corresponding button.
- Pressing the force comms button would trigger a check of the manifest in the back office and attempt to send audit files if they exist on the device. This would update the pending configuration files count and the pending audit files count. Refreshing the page will then update the count of these types of files to show how many of these items have been uploaded/downloaded.
- Shown while the POS is performing sign on activities.
- Selected any of the options will print the sales breakdown report.
- User is able to navigate to the specific items in the menu by pressing the corresponding button.
- User is able to use the arrows buttons to scroll the list.
- User will be redirected to ID field active (if he tried to Sign On manually entering ID) or PIN field active accordingly (if he tried to Sign On automatically presenting Card) after 3 seconds or by pressing Enter button.
- Pressing any key will require to enter both ID and PIN to Sign On.
- After forcing communication, user will return to the updated Force Comms screen.
- Presenting an Supervisor card will redirect user to Sign on page with the ID automatically entered and PIN field active.
- Details will be displayed, with print option.
- Presenting an Supervisor card when a operator is signed in will automatically sign off the operator and unlock the device, if needed. After sign on, POS will display Supervisor Menu screen
- The ‘Print and Zero Totals’ and ‘Print and Zero Accummulated’ options will initially come up with a screen asking whether you really want to zero the totals after the print. If ‘Yes’ is selected, then the totals will be zeroed. All printouts will contain the following information: - Operator number - POS number - Sign-on date and time - Sign-off date and time - No of tickets sold - Revenue collected - Miscellaneous revenue - No of smartcard validations - No of annulled tickets - First ticket number - Last ticket number - Individual detail (i.e. ticket type and prices) of all tickets and passes issued on that journey - Individual ticket numbers of any annulled tickets on that journey.
- Versions will show specific options.
- User will be able to print the details presented in the specific screen.
- Unless otherwise specified, the back button will take you back to the previous screen.

## 11.0 Technician
_31 note(s); branch labels: No, Technician, User enters ID., User enters PIN., User presses Enter., Yes_

- User will be redirected to ID field active (if he tried to Sign On manually entering ID) or PIN field active accordingly (if he tried to Sign On automatically presenting Card) after 3 seconds or by pressing Enter button.
- User will be able to incrementaly set brightness and volume and restore defaults.
- Other diagnostic information will appear on this screen depending on what is available from the interface.
- If the Device cannot establish a correct Communication it will become locked and present a screen with an Error Message and "Please Notify a Supervisor or Technician".
- User is able to navigate to the specific items in the menu by pressing the corresponding button.
- Pressing "Sign Off" will show user another screen that will require confirmation, before actually signing off.
- User will be able to test cards, a card status page will be displayed.
- Shown while the POS is performing sign on activities.
- After forcing communication, user will return to the updated Force Comms screen.
- After reboot, Idle screen will be presented.
- Pressing any key will require to enter both ID and PIN to Sign On.
- Pressing refresh will retrieve information from the server and update information to the latest values.
- Device Status will show specific options.
- Choosing Device Settings will show a menu page.
- User will be able to print the details presented in the specific screen.
- Locations will be available as a list and user will be able to see next or previous 10 locations using the arrow buttons.
- A information screen will be displayed.
- Presenting an Technician card will redirect user to Sign on page with the ID automatically entered and PIN field active.
- User will see a percentage for remaining paper and some average details. User will be able to print a test ticket and reverse paper feed.
- Versions will show specific options.
- User will be able to see which devices are currently connected or were previously connected. The fields on this screen don't update automatically so would need a refresh. Either refresh or go back (has the same effect). This will list devices such as:- - Payment Card Reader - Barcode Reader - Customer Information Display
- Shown while the POS is performing Soft Reboot activities.
- If the smartcard test is successful POS will show a ministatement.
- Device will be configured to connect to Ethernet if available and fall back to cellular if not. User can see whether Ethernet is connected or not. If it is then that is the communications method that will be used. If it's not then it will be cellular.
- Pressing the force comms button would trigger a check of the manifest in the back office and attempt to send audit files if they exist on the device. This would update the pending configuration files count and the pending audit files count. Refreshing the page will then update the count of these types of files to show how many of these items have been uploaded/downloaded.
- Pressing the 'Enter' key will take the user back to the 'Device Settings' screen with the Default Location updated according to the selection and pending confirmation. Pressing 'C' will take the user back with no proposed changes.
- Unless otherwise specified, the back button will take you back to the previous screen.
- Selecting an option will navigate back to the previous screen with the field updated. Pressing 'Back' or 'C' will return with no updates to the fields.
- Page displays the current configuration for the device. A confirmation button will only be available when a change has been made.
- When the field is highlighted the number keys can be pressed to enter a numerical value. Selecting 'Back' deselect the field and the previous setting will not be changed. Pressing 'C' will delete characters. (Note: The same behaviour occurs with TrayID)
- When changes have been made that need to be confirmed the relevant fields will be highlighted and the 'Confirm' button will be available. Selecting 'Back' will cancel all proposed changes. Selecting 'Confirm' will trigger a device reboot.

## 12.0 Administrator
_26 note(s); branch labels: Administrator, No, User enters ID., User enters PIN., User presses Enter., Yes_

- If the Card Dump data is unsuccessful in downloading, the user will be able to retry - this will take the user to the 'Please Wait - Downloading' screen above, or return to the Admin menu.
- If the Card Dump data is successful in downloading, the user will be returned to the Admin menu after removing the smartcard.
- If the Clear Card attempt is unsuccessful, the user will be able to retry - this will take them to the 'Clear Card' screen as long as the card has not been removed, or return to the Admin menu.
- If the Clear Card attempt is successful, the user will have to remove the smartcard to be returned to the Admin menu.
- Pressing the 'Cancel' key will take the user to the Admin menu.
- Pressing the 'Back' key will take the user to the Admin menu.
- Pressing the 'Back' key will take the user to the 'Establish Comms' screen.
- Pressing the 'Back' key will take the user to the 'Establish Comms' screen.
- Pressing the 'Back' key will take the user to the Admin menu.
- Pressing the 'Back' key will take the user to the Admin menu.
- Pressing the 'Back' key will take the user to the 'Device Settings' screen. Pressing one of the Location keys will take the user back to the 'Device Settings' screen. It will be possible to distinguish between locations that have the same name but a different mode. The mechanism to achieve this will be explained at a later date.
- Pressing the 'Back' key will take the user to the 'Device Settings' screen. Pressing the 'Enter' key will take the user back to the 'Device Settings' screen.
- Pressing the '*' key will take the user to the 'Tray ID' screen. Pressing the 'Enter' key will take the user back to the 'Device Settings' screen.
- Pressing the 'Enter' key will take the user back to the 'Device Settings' screen.
- Pressing the 'Enter' key will take the user back to the 'Device Settings' screen.
- Other diagnostic information will appear on this screen depending on what is available from the interface.
- The card data is sent directly to the back office.
- Presenting an Administrator card will redirect user to Sign on page with the ID automatically entered and PIN field active.
- If the Device cannot establish a correct Communication it will become locked and present a screen with an Error Message and "Please Notify a Supervisor or Technician".
- Shown while the POS is performing sign on activities.
- Pressing any key will require to enter both ID and PIN to Sign On.
- User will be redirected to ID field active (if he tried to Sign On manually entering ID) or PIN field active accordingly (if he tried to Sign On automatically presenting Card) after 3 seconds or by pressing Enter button.
- Translink no longer require the feature to commission a smartcard on the POS. As per email "POS CR Exchange" dated 20.07.20 12:36, this functionality has been exchanged, together with POS card reader reboot requirement removal, for CR034, the use of up and down arrows on the POS bus route selection screen and the addition of version screens in administrator mode.
- User will be able to print the details presented in the specific screen.
- 'Versions' screens and flow will match Technician menu, hen ce the screen names being 'Technician'.
- if a boarding location has already been configured then when the page is loaded the currently configured boarding location will be prepopulated

## 13.0 Customer Displays
_0 note(s); branch labels: Customer Displays_


## 14.0 Barcode Scanning
_7 note(s); branch labels: Barcode Scan Validation, No, Yes_

- The ticket will be visually checked by the operator. All the necessary information for each type depending on which barcode type has been scanned.
- User may press any key to go back to FLU screen or timeout of 3 seconds.
- Accessing Barcode Ref. via Operator Menu
- Ticket Validation Screen Examples
- Operator can navigate to the Barcode Reference Entry option on the Operator Menu. See 'Accessing Barcode Ref. via Operator Menu' below.
- Barcodes that have been validated offline will be stored in a list until a connection with Cloudfare and Corethree is re-established?
- On this particular barcode type there can be Notes as well.

## 15.0 Printer Errors
_2 note(s); branch labels: Printing errors_

- If the printer paper is low, the user will get a temporary notification (3 seconds timeout).
- These errors may occur when the following conditions are being met: - Paper level is low - Printer is malfunctioning due to hardware or software errors. - There is no paper in the feeder and user is trying to print. The device will send an event when a print fails, when a partial print occurs due to power loss and when a ticket resumes printing after power loss.

## 16.0 Power Interruption & Audio Tones
_6 note(s); branch labels: Audio Tones, Auto sign off, Power Interruption_

- This screen appears when power is interrupted. If the power is interrupted temporarily, the device will take the user to the screen they were originally on.
- If the power is interrupted for a longer time, this screen will display. The system is shutting down once this state is reached. If the power is off for shorter amount of time than the configured Auto Sign Off time then upon resuming power the POS will go to the Operator Break screen. If the power is off for longer than the configured Auto Sign Off time then upon resuming power the POS will go to the Idle screen with no waybill printed.
- This screen appears on boot to ensure the device has enough charge to successfully allow the state to be saved in the event of a power interruption.
- Power interruption occurs when the device loses power. It does have backup power, but only for a very small period of time. Care has been taken to ensure that any timeouts before shutting down will be enough to save the system state safely.
- Success Tone - Top Ups, Card Issues, Ticket Issues Error Tone - Any failure Frequent beep - Smartcard left on reader
- - If the device is inactive on any of the FLU screens for the configured Auto Sign Off period then the POS will revert to the Idle screen with no waybill printed - If the device is inactive on the Idle screen for the configured Auto Suspend period then the POS will turn the screen off and go into suspend mode - If the device is in suspend mode for the configured Suspend Duration period then the POS will automatically reboot and go to the Idle screen - If the device is in suspend mode then a key press will trigger the POS to reboot and go to the Idle screen

## 2.0 FLU - Bus
_49 note(s); branch labels: Bus Ticket Flow, Cash Limit, No, Payment, Ticket type changed, Tone sounds, Yes_

- POS will display the FLU screen for bus, containing products which can be selected using L1-L5 keys and stages which can be selected using R1-R5 keys. After signing on and route selection, the POS will check the default boarding stage text (available for setting in Technician Mode) against the list of boarding stage names on the route and if any contain the text of the default stage then that boarding stage will be used as the default for that route. L1 - L5 buttons can be configured to result in a sub-menu or a list of products with fares. Products with a £0.00 fare will display as "Invalid".
- End of stages list
- Operator will be able to enter Route Number in numerical keyboard.
- Pressing "*" button here does the following:- - Press once shows the fare breaks - Press twice shows the favourites that have been selected in Cloudfare - Press again and it goes back to normal display
- Pressing "+" button when a toggle button is selected will show a menu with all items (ticket types)
- The error message will have a 2 seconds timeout.
- After selecting alighting stage, the operator will be able to add the product in the basket pressing R6 key.
- Pressing 'C' button from any FLU screen will take operator to Route Selection screen.
- Pressing '*' key again will take operator back to Main screen with the entered route available.
- After selecting, user will see ticket type in bottom bar.
- Pressing 'C' button will take operator back to main screen.
- Operator can use "⌃" and "⌵" buttons to load next or previous 4 stages. Boarding stage change or ticket type change will deselect the alighting stage.
- User can use "⌃" and "⌵" buttons to load next or previous 4 stages.
- User can change boarding stage using "<" and ">" buttons.
- Operator will be able to access letters pressing '*' key.
- The operator will be able to choose the direction of the route pressing R2 key. Pressing R6 or enter key will confirm the Route entered.
- POS will display the first boarding stage and last alighting stage of the selected route. Operator will be able to use "⌃" and "⌵" keys to scroll between routes.
- Operator will be able to access letters pressing '*' key.
- Pressing Enter will confirm the route entered.
- After Payment POS will print the ticket(s) and will return to FLU screen defaulting to Adult Single and deselect alighting stage, while displaying a confirmation message in the top bar with a configurable timeout of 2 seconds.
- Pressing Enter on FLU screen when the basket is empty will take operator directly to the payment screen.
- Pressing Enter on FLU screen when the basket is not empty will take operator to the basket.
- The unused buttons that have been left blank (L4-L5) may be used by Translink at a later date if required. User is able to select Bus from this screen pressing L1 key.
- Pressing the 'Back' key will take the user to the main screen. The list of products on this screen will depend on the day tour that has been selected. To keep compatibility with the legacy system, the user will only be able to issue one ticket/seat per transaction.
- Pressing the 'Back' key will take the user to the 'Day Tour Product' screen. The input is numbers-only.
- Pressing the 'Back' key will take the user to the 'Day Tour Product' screen. Pressing the 'C' key will clear one character at a time in the input field. If the input field is empty, the user will be taken back one screen.
- The input field will default to today's date. The up and down arrows will increment the date. The user will not be able to go behind today's date. Pressing the 'Back' key will take the user to the 'Seat Number Entry' screen. Pressing the 'C' key will go back to today's date.
- Pressing the 'Back' key will take the user to the 'Seat Number Entry' screen. Pressing the 'C' key will go back to today's date.
- Pressing the 'Back' key will take the user to the 'Date Entry' screen. This will follow the usual payment flow.
- User Selects Day Tour product from the list
- If a preconfigured amount is approaching a notification will be displayed. This will appear after ticket confirmation is displayed and will have a timeout of 3 seconds.
- If the maximum revenue is reached, the POS machine will lock and a Supervisor or Technician will need to be notified. The POS needs to retrieve the connection with the back office, operation that will be done in the background.
- Whenever an error screen is displayed on POS, an error tone will be played: https://sndup.net/29yg/Error.wav
- Whenever an success screen is displayed on POS, an success tone will be played: https://sndup.net/6n62/Success.wav
- Whenever a screen times out on POS, a time out tone will be played: https://sndup.net/3ckg/Timeout.wav
- Selecting one of the misc products available will require operator to type in an open fare for the selected product.
- Operator is able to confirm value pressing R6 or Enter.
- If operator eneters an invalid value (minimum and maximum values to be determined), an error banner will be displayed.
- If links for the sounds below don't work, please use the following link and download the sound on your computer: https://drive.google.com/drive/folders/1GeCT1YdpNuqKTRN1C_swZw4rdAD_vkat
- Pressing 'C' button will take operator back to main screen.
- Operator will be able to enter Route Number in numerical keyboard.
- Pressing '*' key again will take operator back to previous screen with the entered route available.
- Operator will be able to access letters pressing '*' key.
- POS will display the Day Tour product name for the selected route. Operator will be able to use "⌃" and "⌵" keys to scroll between routes.
- Operator will be able to access letters pressing '*' key.
- Pressing Enter will confirm the route entered.
- The error message will have a 2 seconds timeout.
- Pressing the Alighting Stage again will allow the user to change Currency. If they press the Alighting Stage button again, this will change the currency back to GBP.
- If the POS reaches the configured time out on the FLU screens, the user is signed out and break mode is skipped.

## 3.0 FLU - Rail
_28 note(s); branch labels: Cash Limit, NO, Payment, Rail Ticket Flow, YES_

- Choosing 'Rail FLU' will show the specific Rail FLU page.
- User will receive a scrollable list with stations. Selecting any will return to the previous screen keeping the selection. Other method is to use Numerical input from previous screen.
- Pressing 'C' button from any FLU screen would take user to Main Screen.
- User will receive a scrollable list with stations. Selecting any will return to the main screen keeping the selection. Other method is to use Numerical input from previous screen.
- User will receive a list with passenger types which can be ordered by Translink on Cloudfare. Selecting any will return to the previous screen keeping the selection. If more passengers types are added from Cloudfare and will not fit in the page, then the page will become scrollable and display in bottom navigation bar the afferent message for scrolling.
- The POS operator will only be able to see the ticket types which are available on the date in question. If the FLU has been advance dated it will show the ticket types which are available on that date.
- User has to choose available starting date.
- If a day selected, operator presses again the same button it will deselect that specific day. The days unavailable for selection will be greyed out. After confirming operator will return to FLU screen with the specific product selected. He will be able to press Enter to issue the ticket or to press 'Add to Basket button' from FLU screen.
- Operator has to enter date of the advance ticket. After confirming operator will return to FLU screen. He will be able to press Enter to issue the ticket or to press 'Add to Basket button' from FLU screen. "Pressing "C" will take the operator back to the date input screen.
- After Payment POS will print the ticket(s) and will return to FLU screen keeping the last ticket it issued and only changing ticket type to Adult Single default, if the operator changes the Boarding or Alighting Station. A confirmation beep sound is produced when ticket is issued. The confirmation banner will have a timeout of 2 seconds.
- An advance ticket can only be purchased as one ticket at a time. The advance ticket option will not be available if there are multiple products in the basket.
- Pressing Enter on FLU screen when the basket is empty will take operator directly to the payment screen.
- If a date for advance ticket is selected the information for the advance button will change to 'Ticket Date DD/MM/YY'. If operator will press this button will go back to date selection screen for advance ticket.
- Pressing the button corresponding the price will change currency to euro if cross border journey was selected. Pressing it again will change to default currency.
- The error will have a 3 seconds timeout for returning to the previous screen. User will be able to override pressing any key. This screen appears if the date entered is invalid or the advance date is valid but is outside the valid advance date range for that ticket type on Cloudfare.
- After sign on, Rail Flu will default to the last stations entered before sign-off.
- This screen shows cross border ticket types if the Boarding or Alighting station is a cross border station and local ticket types if neither Boarding nor Alighting station is a cross border station.
- Favourite Ticket Set Successfully
- Pressing + key in FLU screen will show a list with favourite tickets if set. If no favourite ticket was set, POS will display open slots items. Slots numbering will sort the order of the favourites displayed in the Main Menu screen.
- Choosing an already set favourite, operator will be able to see the complete information of the ticket to be overwritten and the information for their current selection on the Rail FLU screen.
- Choosing an available slot will directly set as favourite in that desired slot.
- After favourite ticket setting is finished, POS will return automatically to Rail FLU screen.
- If a preconfigured amount is approaching a notification will be displayed. This will appear after ticket confirmation is displayed and will have a timeout of 3 seconds.
- If the maximum revenue is reached, the POS machine will lock and a Supervisor or Technician will need to be notified. The POS needs to retrieve the connection with the back office, operation that will be done in the background.
- When the advance date is set the POS operator will have the ability to select a ticket type after this without the advance date defaulting back to current date. This means that the advance date will stay on screen until a) a ticket is issued or b) the operator changes the advance date. The Advanced Date, Passenger Type and Ticket Type will be reset if the POS is inactive for 1 minute.
- All products will be displayed (available for passenger type selection). The product list can be ordere by Translink on Cloudfare. Selecting any will populate the field on the main FLU screen.
- If operator choses for both boarding and alighting the same station, then the passenger and ticket types, along with the price, advance ticket option and basket will become unavailable.
- If the POS reaches the configured time out on the FLU screens, the user is signed out and break mode is skipped.

## 4.0 Basket & Payment
_54 note(s); branch labels: Advance Ticket, Basket Flow Bus, Basket Flow Rail, Card Payment, NO, No, Three Day Ticket, YES, Yes_

- Operator will choose passengers' choise of payment. Choosing Cash/Warrant options will imediately issue the ticket, Bank Card will follow the specific flow (5.0).
- User may select one of the popular rail tickets in main screen and will be taken to payment screen directly. This type of ticket cannot be sent to the basket or added to another tickets in the basket.
- Favourite tickets payment
- After payment a notification containing alighting station and price will be displyed in the top bar.
- Operator will choose passengers' choise of payment. Choosing Cash/Warrant options will imediately issue the ticket, Bank Card will follow the specific flow (5.0).
- Three Day Ticket was previously selected by the operator and data was updated in this screen.
- After payment a notification containing alighting station and price will be displyed in the top bar.
- Operator will choose passengers' choise of payment. Choosing Cash/Warrant options will imediately issue the ticket, Bank Card will follow the specific flow (5.0).
- When issuing an advanced ticket within the rail FLU straight to the basket or payment screen depending on the button selected as only one advanced ticket is allowed in the basket at a time.
- After payment a notification containing alighting station and price will be displyed in the top bar.
- If there isn't any PCD attached to the POS, Bank Card option will be unavailable.
- If there isn't any PCD attached to the POS, Bank Card option will be unavailable.
- If there isn't any PCD attached to the POS, Bank Card option will be unavailable.
- Senior Single (and all other smartcard pass types e.g. War Pensioner, Blind, yLink, 24+, Half-Fare etc) cannot be added to a basket as they require Smartcard validation per individual transaction.
- Senior Single (and all other smartcard pass types e.g. War Pensioner, Blind, yLink, 24+, Half-Fare etc) cannot be added to a basket as they require Smartcard validation per individual transaction.
- After Payment POS prints the ticket(s) and returns back to the default Rail screen once the confirmation banner has timed out.
- If there isn't any PCD attached to the POS, Bank Card option will be unavailable.
- Operator chooses boarding and alighting stages.
- Pressing Enter on FLU screen when the basket is not empty will take operator to the basket.
- After selecting alighting stage, the operator will be able to add the product in the basket pressing R6 key.
- Pressing back will take user back to basket. Add more will take user back to the specific FLU screen he started (if Bus with route selected, then route should be memorised).
- The error will have a 3 seconds timeout for returning to the previous screen. User will be able to override pressing any key.
- Pressing Add More button, user will go back to Main Screen, to add another ticket to the basket.
- User will follow Card Payment flow.
- Choosing 'Clear basket' will show a confirmation screen. If confirmed, the basket is cleared and user is taken back to Main Screen.
- User may select an item, pressing the corresponding L1-L3 / R1-R3 buttons. When selected, the 'Delete item'option will become available.
- After confirming, user will be able to select payment method. He will still be able to scroll ticket list or to add more tickets to basket, if the maximum amount is not reached.
- User is allowed to add a maximum of 9 tickets to the basket. If the maximum is reached the 'Add More' button becomes unavailable so the operator is unable to add any more tickets to the basket. If an item is deleted from the basket then the 'Add More' button will become available again.
- In basket screen, user may scroll between tickets if more then 3 tickets added, add more tickets, clear basket or remove tickets from the basket using R1-R3 buttons.
- User is allow to add maximum 9 tickets to basket. If trying to add more he will receive an error message and is able to press any key to go back.
- User is allow to add maximum 9 tickets to basket. If trying to add more he will receive an error message and is able to press any key to go back.
- In basket screen, user may scroll between tickets if more then 3 tickets added, add more tickets, clear basket or remove tickets from the basket using R1-R3 buttons.
- User is allowed to add a maximum of 9 tickets to the basket. If the maximum is reached the 'Add More' button becomes unavailable so the operator is unable to add any more tickets to the basket. If an item is deleted from the basket then the 'Add More' button will become available again
- After confirming, user will be able to select payment method. He will still be able to scroll ticket list or to add more tickets to basket, if the maximum amount is not reached.
- User may select an item, pressing the corresponding L1-L3 / R1-R3 buttons. When selected, the 'Delete item'option will become available.
- Choosing 'Clear basket' will show a confirmation screen. If confirmed, the basket is cleared and user is taken back to Main Screen.
- User will follow Card Payment flow.
- Pressing Add More button, user will go back to Main Screen, to add another ticket to the basket. On Bus Basket the operator cannot add tickets from 2 different routes. On Bus Basket the operator can add tickets with 2 different boarding stages on the same route.
- The error will have a 3 seconds timeout for returning to the previous screen. User will be able to override pressing any key.
- Pressing back will take user back to basket. Add more will take user back to the specific FLU screen he started (if Bus with route selected, then route should be memorised).
- After selecting alighting stage, the operator will be able to add the product in the basket pressing R6 key.
- Pressing Enter on FLU screen when the basket is not empty will take operator to the basket.
- Operator chooses boarding and alighting stages.
- If there isn't any PCD attached to the POS, Bank Card option will be unavailable.
- After Payment POS will print the ticket(s) and will return to FLU screen defaulting to Adult Single and deselect alighting stage, while displaying a confirmation message in the top bar with a configurable timeout of 2 seconds.
- Add More option will take user back to Rail FLU for adding more products to the basket.
- If a date for advance ticket is selected the information for the advance button will change to 'Ticket Date DD/MM/YY'. If operator will press this button will go back to date selection screen for advance ticket.
- The error will have a 3 seconds timeout for returning to the previous screen. User will be able to override pressing any key.
- Operator has to enter date of the advance ticket. After confirming the POS will display Payment screen. He will be able to press Enter to issue the ticket or to press 'Add to Basket button' from FLU screen. Pressing C will delete a character at a time.
- If a ticket is selected, operator may increase or decrease the number of passengers on that line using + and - keys. Maximum of passengers per line is 100. Each line will result in one printed ticket.
- If a ticket is selected, operator may increase or decrease the number of passengers on that line using + and - keys. Maximum of passengers per line is 100. Each line will result in one printed ticket.
- This screen appears if the date entered is invalid or the advance date is valid but is outside the valid advance date range for that ticket type on Cloudfare.
- After confirming the date for the advance ticket the bus operator will be taken to the basket automatically.
- Operator will be able to go to the date screen selection for changing the date of the advance ticket pressing L4.

## 5.0 Card Payment
_31 note(s); branch labels: Card Payment Flow, Chip & PIN, Contactless, No, Print Ticket, Swipe Card, Yes_

- Customer has to insert or swipe the card for initialising transaction. If it's a contactless card, the customer can present their card to the device straight away.
- Print a receipt for customer to sign.
- Timeout of 3 seconds or press any key will go back to Payment Screen.
- Customer cancels transaction on PIN pad.
- Timeout of 3 seconds or press any key will go back to Payment Screen.
- Timeout of 3 seconds or press any key will go back to Payment Screen.
- If transaction was declined then user will receive the appropriate error message.
- Customer cancels transaction on PIN pad.
- From payment screen, user chooses Bank Card.
- Timeout of 3 seconds or press any key will go back to Payment Screen.
- If the provided signature does not match the payment card, user wil receive an error screen with 'Sigature doesn't match payment card'
- Timeout of 3 seconds or press any key will go back to Payment Screen.
- Regardless of which option is chosen by the POS operator (i.e. Print receipt or Back to Main/No receipt) the POS will revert to screen 2.7.3 (Bus Flu) or 3.2 (Rail Flu) .
- The error messages displayed on the POS screen will be dependent on the error messages received from the M020.
- The value of transaction is too big for a card payment.
- Timeout of 3 seconds or press any key will go back to Payment Screen.
- Payment terminal is in the process of authorising transaction.
- Payment terminal is in the process of authorising transaction.
- Customer is confirming the transaction amount and inputting their PIN.
- Payment terminal is in the process of authorising transaction.
- The error messages displayed on the POS screen will be dependent on the error messages received from the M020.
- Waiting for customer to press green button on M020 to confirm the amount. The POS will be told the status by the card reader, and will reflect the status from this. Starting transaction > Event (Awaiting card) > Insert card into reader > Events back from card
- As soon as this screen appears the ticket is immediately printed. Only after the ticket prints does the customer have the option to print a payment card receipt (or not print a payment card receipt and go back to Main Screen).
- Once the customer presses Yes on this screen the ticket will be printed and the POS will revert to screen 2.7.3 (Bus Flu) or 3.2 (Rail Flu).
- Regardless of which option is chosen by the POS operator (i.e. Print receipt or Back to Main/No receipt) the POS will revert to screen 2.7.3 (Bus Flu) or 3.2 (Rail Flu) .
- As soon as this screen appears the ticket is immediately printed. Only after the ticket prints does the customer have the option to print a payment card receipt (or not print a payment card receipt and go back to Main Screen).
- the POS will be told the status by the card reader, and will reflect the status from this. Starting transaction > Event (Awaiting card) > Insert card into reader > Events back from card
- Timeout of 3 seconds or press any key will go back to Payment Screen.
- A declined card payment receipt will be printed when this screen is displayed. If the customer presses the red x on the M020 before entering the pin there is no cancelled payment receipt.
- If user enters PIN incorrectly more then the accepted amount of times, user will receive an error screen with 'Incorrect PIN entered too many times'.
- The user will be asked to insert their card to pay for the transaction.

## 6.0 Numerical Input
_14 note(s); branch labels: NO, No, Numerical Input Bus, Numerical Input Rail, YES, Yes_

- User enters a number at any given time in the main Bus FLU screen.
- User will receive an error notification if change couldn't be calculated. The Calculate Change option will not be available if: 1. entering too many digits 2. the amount entered is less than the ticket value 3. previous transaction had no value
- User may set alighting stage using ID number. This will automatically return to Main FLU screen with the entered ID station selected.
- User is able to issue a group ticket with the selected boarding and alighting stages multiplied with the number entered.
- According to amount entered, User will not be able to access some of the functionality. For example, group ticket has a limit of 100 tickets.
- User is able to calculate change.
- User may set boarding stage using Unique Farestage ID. This will automatically return to Main FLU screen with boarding stage changed.
- The machine will print a single group ticket receipt. Upon ticket issue a single transaction record will be sent to the back office that includes sub-elements for each passenger that is part of the group ticket
- Operator will be able to set an advance date ticket following the specific flow.
- There will be a setting within Cloudfare which allows Translink to configure which ticket types will be allowed to be issued as a Group Tickets and which will not.
- Timeout will not occur, 'Back or Main' keys must be pressed.
- If the number entered doesn't match any of the stages available, an error will be displayed.
- The POS will display an error banner if the amount entered cannot be used for a group ticket.
- The POS will display an error banner if the product selected is not available as a group ticket.

## 7.0 Top Up & Validation
_152 note(s); branch labels: Card payment flow, Faulty Cards Flow, No, Top Up, Yes_

- A Top Up Successful screen is presented and user has to remove Smartcard to continue.
- This is a catch all error screen for issues with the smartcard. For example, this could be a card that is not specific for Translink (anything not in a recognised format) . Timeout of 3 seconds or press any key will go back to Main Menu.
- User is able to choose a product pressing the corresponding buttons. If choosing a product will overcome the maximum amount allowed for that card, then that menu option will not be displayed.
- User will be prompted to present Smartcard.
- Timeout of 3 seconds or press any key will go back to the previous screen.
- User may choose 'Smartcard' at any given time on the Main Screen and both Bus or Rail FLU screens.
- User selects Smartcard from Main Menu.
- Pressing 'C' button will reset value and journeys number.
- If the Smartcard card is valid and not blank, user is presented the Smartcard menu.
- Discount/Entitlement Smartcards Validation
- User will be prompted to present Smartcard. This is the first screen Metro operator will be presented after sign on process.
- If the Smartcard card is valid and not blank, user is presented the Smartcard menu.
- This is a catch all error screen for issues with the smartcard. For example, this could be a card that is not specific for Translink (anything not in a recognised format). Timeout of 3 seconds or pressing any key will go back to previous screen.
- Pressing 'C' button will reset value and journeys number.
- User is able to choose a product pressing the corresponding buttons. If choosing a product will overcome the maximum amount allowed for that card, then that menu option will not be displayed.
- After printing process, user will automatically return to Top up menu.
- Metro Top Up Flow
- Ulsterbus Top Up Flow
- A Top Up Successful screen is presented and user has to remove Smartcard to continue.
- Timeout of 3 seconds or pressing any key will go back to the previous screen.
- If the card expired it will be stated in the screen. The user is able to choose a product pressing the corresponding buttons.
- ABT Top Up Flow
- User will be prompted to present Smartcard.
- If the Smartcard card is valid and not blank, user is presented the Smartcard menu.
- This is a catch all error screen for issues with the smartcard. For example, this could be a card that is not specific for Translink (anything not in a recognised format) . Timeout of 3 seconds or press any key will go back to Main Menu.
- User selects Smartcard from Main Menu.
- After printing process, user will automatically return to Top up menu.
- A Top Up Successful screen is presented and user has to remove Smartcard to continue.
- Timeout of 3 seconds or pressing any key will go back to the previous screen.
- A Top Up Successful screen is presented and user has to remove Smartcard to continue.
- Timeout of 3 seconds or pressing any key will go back to the previous screen.
- A Top Up Successful screen is presented and user has to remove Smartcard to continue.
- User is able to choose a product pressing the corresponding buttons. The expiry for the product is also shown.
- If the product is expired it will be stated in the screen.
- User will be prompted to present Smartcard.
- If the Smartcard card is valid and not blank, user is presented the Smartcard menu.
- This is a catch all error screen for issues with the smartcard. For example, this could be a card that is not specific for Translink (anything not in a recognised format) . Timeout of 3 seconds or press any key will go back to Main Menu.
- User selects Smartcard from Main Menu.
- After printing process, user will automatically return to Top up menu.
- User may choose 'Smartcard' at any given time on the Main Screen and both Bus or Rail FLU screens.
- DayLink Top Up Flow
- A Top Up Successful screen is presented and user has to remove Smartcard to continue.
- Timeout of 3 seconds or pressing any key will go back to the previous screen.
- User is able to choose a product pressing the corresponding buttons.
- User will be prompted to present Smartcard.
- If the Smartcard card is valid and not blank, user is presented the Smartcard menu.
- This is a catch all error screen for issues with the smartcard. For example, this could be a card that is not specific for Translink (anything not in a recognised format) . Timeout of 3 seconds or press any key will go back to Main Menu.
- User selects Smartcard from Main Menu.
- After printing process, user will automatically return to Top up menu.
- User may choose 'Smartcard' at any given time on the Main Screen and both Bus or Rail FLU screens.
- Belfast Visitor Pass Top Up Flow
- A Top Up Successful screen is presented and user has to remove Smartcard to continue.
- Timeout of 3 seconds or pressing any key will go back to the previous screen.
- User is able to choose a product pressing the corresponding buttons.
- User will be prompted to present Smartcard.
- If the Smartcard card is valid and not blank, user is presented the Smartcard menu.
- This is a catch all error screen for issues with the smartcard. For example, this could be a card that is not specific for Translink (anything not in a recognised format) . Timeout of 3 seconds or press any key will go back to Main Menu.
- User selects Smartcard from Main Menu.
- After printing process, user will automatically return to Top up menu.
- User may choose 'Smartcard' at any given time on the Main Screen and both Bus or Rail FLU screens.
- iLink Top Up Flow
- A Top Up Successful screen is presented and user has to remove Smartcard to continue.
- Timeout of 3 seconds or pressing any key will go back to the previous screen.
- User is able to choose a product pressing the corresponding buttons.
- If the card expired it will be stated in the screen.
- All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- After operator chooses alighting stage the ticket is printed automatically. No aditional action is needed.
- For rail operator has to confirm pressing Enter for the ticket to be issued.
- Similar to the Senior Smartpass. Ticket type will be displayed accordingly: 60+ Single.
- This ticket type will not be accepted for Rail Cross Border travel. Cross Border stations will not be displayed/available for numerical input.
- Similar to the Senior Smartpass. Ticket type will be displayed accordingly: RoI Senior Single. Cross Border tickets will be display as: RoI Senior XB Single RoI Senior XB Day Return RoI Senior XB 1 Mth Return and will be available to change using L4 toggle or R4 menu keys.
- Similar to the Senior Smartpass. Ticket type will be displayed accordingly: Blind Single. Cross Border tickets will be display as: Blind XB Single Blind XB Day Return Blind XB 1 Mth Return and will be available to change using L4 toggle or R4 menu keys.
- Similar to the Senior Smartpass. Ticket type will be displayed accordingly: War Pensioner Single. Cross Border tickets will be display as: War Pensioner XB Single War Pensioner XB Day Return War Pensioner XB 1 Mth Return and will be available to change using L4 toggle or R4 menu keys.
- For both rail and bus operator has to confirm pressing Enter to go to payment screen.
- Similar to the Senior Smartpass.
- This ticket types will not be accepted for Rail Cross Border travel. Cross Border stations will not be displayed/available for numerical input.
- Operator chooses alighting stage
- Rail operator can choose between Half Fare Single and Half Fare Return using L4 toggle key or R4 key and select from the list.
- This ticket type will not be accepted for Rail Cross Border travel. Cross Border stations will not be displayed/available for numerical input.
- Similar to the Senior Smartpass.
- This ticket types will not be accepted for Rail Cross Border travel. Cross Border stations will not be displayed/available for numerical input.
- Similar to the Senior Smartpass.
- This ticket types will not be accepted for Rail Cross Border travel. Cross Border stations will not be displayed/available for numerical input.
- Similar to the Senior Smartpass.
- This ticket types will not be accepted for Rail Cross Border travel. Cross Border stations will not be displayed/available for numerical input.
- For both rail and bus operator has to confirm pressing Enter to go to payment screen.
- Operator chooses alighting stage
- Rail operator can choose between yLink Single, yLink Return, yLink Weekly and yLink Monthly using L4 toggle key or R4 key and select from the list.
- This ticket type will not be accepted for Rail Cross Border travel. Cross Border stations will not be displayed/available for numerical input.
- Operator has to confirm pressing Enter to go to payment screen.
- Rail operator can choose between 24+ Single, 24+ Return, 24+ Weekly, and 24+ Monthly using L4 toggle key or R4 key and select from the list.
- This ticket type will not be accepted for Rail Cross Border travel. Cross Border stations will not be displayed/available for numerical input.
- This card type will only be accepted for rail.
- For Rail, operator has to confirm pressing enter for the ticket to be issued.
- This ticket type will not be accepted for Rail Cross Border travel. Cross Border stations will not be displayed/available for numerical input.
- Operator may choose to go back to previous screen or press Continue key to go to Main Screen or FLU screen (where initially started).
- Operator may choose to go back to previous screen or press Issue Receipt key to print receipt and go to Main Screen or FLU screen (where initially started).
- Customer will be unable to use the Smartcard if presented outside of a relevant time band. This error will have a timeout of 3 seconds and will send operator to Main Screen or FLU screen (where initially started).
- Customer will be unable to validate the card again if the last validation was made in less then X minutes prior to the second attempt (this time should be configured to TL demand). This error will have a timeout of 3 seconds and will send operator to Main Screen or FLU screen (where initially started).
- If the card presented is Hotlisted POS will show this error. If expired, it will state Expired Smartcard. This error will have a timeout of 3 seconds and will send operator to Main Screen or FLU screen (where initially started).
- When this screen is shown: 1) the Cash or Warrant payment is not recorded in the POS audit data (and a diagnostic/event is recorded to audit this error occured) 2) Any payment card transaction is automatically voided by the POS (and a diagnostic/event is recorded to audit this error occured)
- Timeout of 3 seconds or pressing any key will go back to the previous screen.
- If a Multi-Journey card is expired and journeys are added to it then all existing journeys are removed following the successful top-up (and a journey removal receipt is printed).
- If a Multi-Journey card is expired and journeys are added to it then all existing journeys are removed following the successful top-up (and a journey removal receipt is printed).
- All Ulsterbus cards can be topped up on any POS (i.e. Metro, Ulsterbus or Rail POS)
- All Metro cards can be topped up on any POS (i.e. Metro, Ulsterbus or Rail POS)
- All ABT cards (Adult or Child) can be topped up on any POS (i.e. Metro, Ulsterbus or Rail POS). The text 'ABT' on screens will be replaced by the ABT brand name
- All DayLink cards can be topped up on any POS (i.e. Metro, Ulsterbus or Rail POS)
- All iLink cards can be topped up on any POS (i.e. Metro, Ulsterbus or Rail POS)
- When Mini Statement is selected, the POS will display data for the smarcard previously presented.
- When Mini Statement is selected, the POS will display data for the smarcard previously presented.
- The operator will still be able to change boarding or alighting station at this point without removing the ticket type initiated by presenting the free Smartpass.
- The operator should still be able to change boarding or alighting station at this point without removing the ticket type initiated by presenting the Half Fare Smartpass
- The operator should still be able to change boarding or alighting station at this point without removing the ticket type initiated by presenting the yLink Smartpass.
- The operator should still be able to change boarding or alighting station at this point without removing the ticket type initiated by presenting the 24+ Smartpass.
- The operator should still be able to change boarding or alighting station at this point without removing the ticket type initiated by presenting the Dependants Smartpass.
- All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- All Belfast Visitor cards can be topped up on any POS (i.e. Metro, Ulsterbus or Rail POS)
- All XB ticket types are only available on Rail POS.
- After operator chooses alighting stage the ticket is printed automatically. No aditional action is needed.
- When this screen is shown: 1) the Cash or Warrant payment is not recorded in the POS audit data (and a diagnostic/event is recorded to audit this error occured) 2) Any payment card transaction is automatically voided by the POS (and a diagnostic/event is recorded to audit this error occured)
- When this screen is shown: 1) the Cash or Warrant payment is not recorded in the POS audit data (and a diagnostic/event is recorded to audit this error occured) 2) Any payment card transaction is automatically voided by the POS (and a diagnostic/event is recorded to audit this error occured)
- When this screen is shown: 1) the Cash or Warrant payment is not recorded in the POS audit data (and a diagnostic/event is recorded to audit this error occured) 2) Any payment card transaction is automatically voided by the POS (and a diagnostic/event is recorded to audit this error occured)
- When this screen is shown: 1) the Cash or Warrant payment is not recorded in the POS audit data (and a diagnostic/event is recorded to audit this error occured) 2) Any payment card transaction is automatically voided by the POS (and a diagnostic/event is recorded to audit this error occured)
- When this screen is shown: 1) the Cash or Warrant payment is not recorded in the POS audit data (and a diagnostic/event is recorded to audit this error occured) 2) Any payment card transaction is automatically voided by the POS (and a diagnostic/event is recorded to audit this error occured)
- When this screen is shown: 1) the Cash or Warrant payment is not recorded in the POS audit data (and a diagnostic/event is recorded to audit this error occured) 2) Any payment card transaction is automatically voided by the POS (and a diagnostic/event is recorded to audit this error occured)
- When this screen is shown: 1) the Cash or Warrant payment is not recorded in the POS audit data (and a diagnostic/event is recorded to audit this error occured) 2) Any payment card transaction is automatically voided by the POS (and a diagnostic/event is recorded to audit this error occured)
- In regards to Mini Statements, if the card does not have a card reference number then "N/A" will be displayed.
- Example of ABT card in negative list (variant of screen 7.4.6 ABT Smartcard/Top Up)
- Example of ABT card in negative list (variant of screen 7.2.2 Smartcard/Menu-ABT)
- *Enter button has no function on this screen*
- *Enter button has no function on this screen*
- *Enter button has no function on this screen*
- *Enter button has no function on this screen*
- *Enter button has no function on this screen*
- *Enter button has no function on this screen*
- *Enter button has no function on this screen*
- *Enter button has no function on this screen*
- There are no validations for Metro POS
- Return to beginning of the flow
- *Only the cash option is available to Metro users*
- *Only the cash option is available to Metro users*
- *Only the cash option is available to Metro users*
- *Only the cash option is available to Metro users*
- *Only the cash option is available to Metro users*
- *Only the cash option is available to Metro users*
- *Only the cash option is available to Metro users*
- Warrant and card is available for NIR and Ulsterbus

## 8.0 Issue Card
_67 note(s); branch labels: Card payment flow, Issue Card, No, Yes_

- If the Smartcard presented is not valid, user will receive an Error Screen. Timeout of 3 seconds or press any key will go back to Main Menu.
- User selects Smartcard from Main Menu.
- User will be prompted to present Smartcard.
- If the Smartcard card is valid and blank (pre-encoded information only), user is able to select Issue Smartcard.
- User may choose 'Smartcard' at any given time on the Main Screen and both Bus or Rail FLU screens.
- User will see a confirmation screen with options for payment methods.
- "Pressing "C" button will take the operator back to select an alternative card reference number.
- A Card Issue Successful screen is presented and user has to remove Smartcard to`continue.
- A Card Issue Successful screen is presented and user has to remove Smartcard to`continue.
- User is able to choose a product pressing the corresponding buttons.
- Selection of adult or child will be done automatically by the POS according to the data on the card. All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- User will be prompted to present Smartcard. This is the first screen Metro operator will be presented after sign on process.
- This is a catch all error screen for issues with the smartcard. For example, this could be a card that is not specific for Translink (anything not in a recognised format). Timeout of 3 seconds or pressing any key will go back to previous screen.
- User will see a confirmation screen with options for payment methods.
- Pressing 'C' button will reset value and journeys number.
- Metro POS Card Issue Flow
- A Card Issue Successful screen is presented and user has to remove Smartcard to`continue.
- A Card Issue Successful screen is presented and user has to remove Smartcard to`continue.
- Selection of adult or child will be done automatically by the POS according to the data on the card. All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- User is able to choose a product pressing the corresponding buttons.
- A Card Issue Successful screen is presented and user has to remove Smartcard to`continue.
- A Card Issue Successful screen is presented and user has to remove Smartcard to`continue.
- User is able to choose a product pressing the corresponding buttons.
- Selection of adult or child will be done automatically by the POS according to the data on the card. All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- A Card Issue Successful screen is presented and user has to remove Smartcard to`continue.
- User is able to choose a product pressing the corresponding buttons.
- A Card Issue Successful screen is presented and user has to remove Smartcard to`continue.
- User is able to choose a product pressing the corresponding buttons.
- Selection of adult or child will be done automatically by the POS according to the data on the card. All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- Selection of adult or child will be done automatically by the POS according to the data on the card. All child user flows will be similar to the adult ones and will state Child instead of Adult where present, with the corresponding value of products retrieved from Cloudfare.
- The operator will be able to to try again to write information on the smartcard or to cancel the process which would void the transaction and return to the previous screen.
- The operator will be able to to try again to write information on the smartcard or to cancel the process which would void the transaction and return to the previous screen.
- The operator will be able to to try again to write information on the smartcard or to cancel the process which would void the transaction and return to the previous screen.
- The operator will be able to to try again to write information on the smartcard or to cancel the process which would void the transaction and return to the previous screen.
- The operator will be able to to try again to write information on the smartcard or to cancel the process which would void the transaction and return to the previous screen.
- The operator will be able to to try again to write information on the smartcard or to cancel the process which would void the transaction and return to the previous screen.
- The operator will be able to to try again to write information on the smartcard or to cancel the process which would void the transaction and return to the previous screen.
- The operator will be able to to try again to write information on the smartcard or to cancel the process which would void the transaction and return to the previous screen.
- When this screen is shown: 1) If payment was by card the card transaction is voided 2) No transaction record will have been recorded on the POS and subsequently no totals information would have been updated 3) Some data may have been written to the smartcard but it would have been written to a section of the smartcard that is not currently being used so will have no effect on smartcard operation 4) A diagnostic/event is recorded to audit this error occurred"
- The text 'ABT' on screens will be replaced by the ABT brand name. The flow after selecting Adult or Child will remain the same.
- Any Translink Smartcard can be issued from any Ulsterbus or NIR POS device.
- Customer access code is printed on the card issue receipt.
- The iLink zone is determined from the card encoding.
- Any Translink Smartcard can be issued from a Metro POS except for Ulsterbus Multi-Journey and Ulsterbus Town Services Travelcard
- The text 'ABT' on screens will be replaced by the ABT brand name.
- When this screen is shown: 1) If payment was by card the card transaction is voided 2) No transaction record will have been recorded on the POS and subsequently no totals information would have been updated 3) Some data may have been written to the smartcard but it would have been written to a section of the smartcard that is not currently being used so will have no effect on smartcard operation 4) A diagnostic/event is recorded to audit this error occurred"
- When this screen is shown: 1) If payment was by card the card transaction is voided 2) No transaction record will have been recorded on the POS and subsequently no totals information would have been updated 3) Some data may have been written to the smartcard but it would have been written to a section of the smartcard that is not currently being used so will have no effect on smartcard operation 4) A diagnostic/event is recorded to audit this error occurred"
- When this screen is shown: 1) If payment was by card the card transaction is voided 2) No transaction record will have been recorded on the POS and subsequently no totals information would have been updated 3) Some data may have been written to the smartcard but it would have been written to a section of the smartcard that is not currently being used so will have no effect on smartcard operation 4) A diagnostic/event is recorded to audit this error occurred"
- When this screen is shown: 1) If payment was by card the card transaction is voided 2) No transaction record will have been recorded on the POS and subsequently no totals information would have been updated 3) Some data may have been written to the smartcard but it would have been written to a section of the smartcard that is not currently being used so will have no effect on smartcard operation 4) A diagnostic/event is recorded to audit this error occurred"
- When this screen is shown: 1) If payment was by card the card transaction is voided 2) No transaction record will have been recorded on the POS and subsequently no totals information would have been updated 3) Some data may have been written to the smartcard but it would have been written to a section of the smartcard that is not currently being used so will have no effect on smartcard operation 4) A diagnostic/event is recorded to audit this error occurred"
- When this screen is shown: 1) If payment was by card the card transaction is voided 2) No transaction record will have been recorded on the POS and subsequently no totals information would have been updated 3) Some data may have been written to the smartcard but it would have been written to a section of the smartcard that is not currently being used so will have no effect on smartcard operation 4) A diagnostic/event is recorded to audit this error occurred"
- When this screen is shown: 1) If payment was by card the card transaction is voided 2) No transaction record will have been recorded on the POS and subsequently no totals information would have been updated 3) Some data may have been written to the smartcard but it would have been written to a section of the smartcard that is not currently being used so will have no effect on smartcard operation 4) A diagnostic/event is recorded to audit this error occurred"
- The text 'ABT' on screens will be replaced by the ABT brand name.
- *Enter button has no function on this screen*
- *Enter button has no function on this screen*
- *Enter button has no function on this screen*
- *Enter button has no function on this screen*
- *Enter button has no function on this screen*
- *Enter button has no function on this screen*
- *Enter button has no function on this screen*
- *Only the cash option is available to Metro users*
- *Only the cash option is available to Metro users*
- *Only the cash option is available to Metro users*
- *Only the cash option is available to Metro users*
- *Only the cash option is available to Metro users*
- *Only the cash option is available to Metro users*
- *Only the cash option is available to Metro users*

## 9.0 Operator
_40 note(s); branch labels: NO, Operator, Operator presents card., YES_

- Pressing 'Annul Rail/Misc Tickets' will show a list with transaction from current shift. If a product is issued in euros then it is presented in euros on the annulment screen.
- After signing off, the device will go automatically in idle mode.
- User will receive a confirmation screen and will be able to go back to operator menu, pressing any key.
- Choosing Totals will display a list which will be available for printing.
- Choosing a transaction will show full details and option to annul.
- Pressing "Break Mode" will show user another screen that will require confirmation, before actually going into break mode.
- User may press 'Wayfarer' button at any given time on the Main Screen and both Bus or Rail FLU screens.
- User will be given the possibility to retry or to sign off anyway. Operator can retry indefinitely.
- Device will enter break mode and display a similar screen to idle mode.
- Pressing "Sign Off" will show user another screen that will require confirmation, before actually signing off.
- Choosing 'Operator Options' will show a menu screen with specific options.
- User is able to access Operator Menu, pressing the 'Wayfarer' button.
- If a supervisor presents their card and enters a valid PIN then the Supervisor Menu is displayed and the current Operator is signed off. When the Supervisor signs off the Idle screen is displayed.
- User will be redirected to ID field active (if he tried to Sign On manually entering ID) or PIN field active accordingly (if he tried to Sign On automatically presenting Card) after 3 seconds or by pressing Enter button.
- If connection is slow, User might see a loading screen
- If Soft Reboot is chosen operator will have to press Confirm or Enter for rebooting the POS.
- If any of the following conditions have not been met then the "Annul Previous Transaction" option is not available: - The previous transaction was a bus ticket that was issued within the last 60 seconds - The previous transaction was a smartcard transaction.
- POS will display a list with tickets and transactions.
- Using L1-L5, operator can see details for the selected ticket/transaction.
- Usr will be able to press any key to go back to the previous screen.
- Usr will be able to press any key to go back to the previous screen.
- An annulled ticket receipt will be printed showing which ticket has been annulled so that the operator can use this annulled receipt along with the original ticket issued to reconcile his cash takings. If the transaction used a payment card then the card is automatically refunded and a payment card receipt is printed.
- User will see a percentage for remaining paper and some average details. User will be able to print a test ticket and reverse paper feed.
- POS will print a waybill if confimed. Shift and day totals will appear on the waybill.
- User will be return to the previous annulment screen pressing any key.
- Unless otherwise specified, the back button will take you back to the previous screen.
- As per the CONOPs Flowbird were committed to provide a facility to reboot the card reader. As per email "POS CR Exchange" dated 20.07.20 12:36, this functionality has been exchanged, together with administrator mode commission card functionality, for CR034, the use of up and down arrows on the POS bus route selection screen and the addition of version screens in administrator mode.
- The child flow will be the same as the Adult Excess Ticket flow.
- Pressing the 'Barcode Reference Entry' key will take the user to the 'Barcode Scanning' flow.
- The 'Issue Refund' flow will be agreed between Flowbird and Translink following further analysis.
- User will be return to the previous annulment screen pressing any key.
- Reporting a faulty device means the Payment Device will no longer be available to use. An event will be sent to CloudFare to notify back end users of a Faulty Device.
- If there is a faulty device, the Faulty Device icon is shown in the header.
- If most recent transaction was a smartcard transaction, then it can be annulled.
- Example of Metro POS Operator Menu.
- Example of Metro POS Operator Options Menu.
- If on break for a configured amount of time, the user will be signed out
- If on break for a configured amount of time, the POS will be put in suspend mode.
- If on break for a configured amount of time, the user will be signed out
- After a certain amount of time has passed on any screen (apart from FLU), the POS enters breakmode.

## Welcome Page
_3 note(s); branch labels: Available, Card Reader, Cellular, Dark background, Ethernet, Faulty Payment Device, Light background, Network, POS v4.0.3, Symbols, Unavailable, Welcome Page_

- Translink POS User Flows Contents
- 1.0 Sign On 2.0 FLU - Bus 3.0 FLU - Rail 4.0 Basket & Payment 5.0 Card Payment 6.0 Numerical Input 7.0 Top Up & Validation 8.0 Issue Card 9.0 Operator 10.0 Supervisor 11.0 Technician 12.0 Administrator 13.0 Customer Displays 14.0 Barcode Scanning 15.0 Printer Errors 16.0 Power Interruption & Audio Tones
- The following symbols showing the availablility of three features, being permanently positioned in the upper left side of the screen, as a part of the status bar. For accessibility reasons, the symbols may vary between two colors: blue on a light background and white on a dark background. The Faulty Device icon is used to remind the driver that they have already reported the device as faulty. It is technically a different state to Card Reader Unavailable.
