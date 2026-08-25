*** Settings ***
Documentation     Screen Bindings
Library  Collections

Resource  SmartcardBindings.robot
Resource  ../Utility/ScreensUtility.robot
Resource  ../Utility/FunctionsUtility.robot
Resource  ../Utility/SimulatorUtility.robot
Resource  ../Utility/Platforms/WECFunctionsUtility.robot
Resource  ../../../Common/Utility/StaffUtility.robot
Resource  ../../ETM/Utility/ETMScreenUtility.robot
Resource  ../../Validators/Utility/ValidatorScreenUtility.robot

*** Keywords ***
### WHEN ###
the device is fully commissioned and started
    ${Restarting}    Run Keyword And Return Status    Device: Screen: Validate Screen    Restarting
    IF   ${Restarting}
         Sleep   120s
    END
    Device: Function: Set: Prepare and Start Device Services
    ${device_current_state}=    Device: Function: Gather Device State
    Should Not Be Equal As Strings    ${device_current_state}    UnCommissioned
    Should Not Be Equal As Strings    ${device_current_state}    ErrorOutOfService

Sign off the current device
    Device: Screen: Sign off the device

the device has ${device_screen_exp} screen within ${timeout} seconds
    Wait Until Keyword Succeeds  ${timeout} sec  1 sec  Device: Screen: Validate Screen  Idle  timeout=1
    Return From Keyword If    "${device_screen_exp}"=="Idle"
    ${StaffNumber}  ${Pin} =  Staff: Get Available Staff Member    Operator     ${current_device}[Type]     ${current_device}[operator_name]
    Device: Screen: Navigate to device screen with Variables          ${StaffNumber}    ${Pin}    ${device_screen_exp}

the ${screenName} screen is displayed
    the ${screenName} screen is displayed within 20 seconds

the ${screenName} screen is not displayed
    Run Keyword And Expect Error    Json tables do not match*    the ${screenName} screen is displayed within 1 seconds

the ${screenName} screen is not displayed within ${timeout} seconds
    Wait Until Keyword Succeeds    ${timeout} sec  1 sec  the ${screenName} screen is not displayed

the ${screenName} screen is displayed within ${timeout} seconds
	Wait Until Keyword Succeeds  ${timeout} sec  1 sec  Device: Screen: Validate Screen  ${screenName}  timeout=1

${r:(.* )?}sign on the device using ${r:(new|current|old|original)} staff member details and navigate to ${screen} screen
    Device: Screen: Sign On the device and Navigate     ${current_staff_number}    ${current_staff_pin}    ${screen}

${r:(.* )?}sign on the current device using edited staff member details and navigate to ${screen} screen
    Device: Screen: Sign On the device and Navigate     ${current_staff_number_edit}    ${current_staff_pin_edit}    ${screen}

${r:(.* )?}sign on the device using ${staffrole} credentials and navigate to ${screen} screen
    ${StaffNumber}  ${Pin} =  Staff: Get Available Staff Member    ${staffrole}     ${current_device}[Type]     ${current_device}[operator_name]
    Device: Screen: Sign On the device and Navigate     ${StaffNumber}    ${Pin}    ${screen}

${r:(.* )?}sign on the device as ${staffrole} and navigate to ${exp_screen} screen
    ${StaffNumber}  ${Pin} =  Staff: Get Available Staff Member    ${staffrole}     ${current_device}[Type]     ${current_device}[operator_name]
    Device: Screen: Sign On the device and Navigate     ${StaffNumber}    ${Pin}    ${exp_screen}

${r:(.* )?}navigate to ${exp_screen} screen as ${staffrole}
    ${StaffNumber}  ${Pin} =  Staff: Get Available Staff Member    ${staffrole}     ${current_device}[Type]     ${current_device}[operator_name]
    Device: Screen: Navigate to device screen with Variables          ${StaffNumber}    ${Pin}    ${exp_screen}

${r:(.* )?}presents ${card_tag} smartcard and move to ${exp_screen} screen as ${staffrole}
    Device: Screen: Sign On the device Using Smartcard     common     ${card_tag}    ${staffrole}    ${exp_screen}

${r:(.* )?}navigate to ${exp_screen} device screen
    wait until keyword succeeds  20 sec  1 sec  Device: Screen: Navigate to device screen    ${exp_screen}

${r:(.* )?}enters "${staffrole}" pin number
    ${StaffNumber}  ${Pin} =  Staff: Get Available Staff Member    ${staffrole}     ${current_device}[Type]     ${current_device}[operator_name]
    Device: Interactions: Press Button Sequence    ${Pin}
    ${layoutchk}    Run Keyword And Return Status    Device: Screen: Validate Screen Contains Text     OK
    IF   ${layoutchk}
        Device.click device ui button    OK    ${false}
    ELSE
        Device: Interactions: Press Key    ENTER
    END

${r:(.* )?}changes payment mode
    user presses the subtract

${r:(.* )?}enters basket confirmation screen
    When user presses the R6

${r:(.* )?}enters basket confirmation screen and selects confirm
    Run Keyword 2 times  When user presses the R6

${r:(.* )?}updates ${text_box_name} text entry value to ${exp_mounting_point} in device details screen
	${type}   Convert to String   ${current_device}[Type]
    IF   "${type}[-1]"=="V"
          ${type}   Use   Validator
    END
    Run keyword    ${type}ScreenUtility.Device: ${type}: Screen: Set Mounting point   ${exp_mounting_point}    ${text_box_name}

the device has default screen template
    Device: Screen: Validate Layout By Name

#THEN
###THEN###
the ${ScreenName} screen should be displayed
    Log To Console  \nWaiting for the "${ScreenName}" Screen to be displayed..
    wait until keyword succeeds  20 sec  1 sec  Device: Screen: Validate Screen  ${ScreenName}
    log to Console   Correct Screen displayed \n

the device remains on the ${ScreenName} screen for the next ${seconds} seconds
    Run Keyword And Expect Error    *did not occur.*    the ${ScreenName} screen is not displayed within ${seconds} seconds
    the ${ScreenName} screen should be displayed

the device state is no longer "${state}" within ${timeout} seconds
    Wait Until Keyword Succeeds   ${timeout} s   1 s   the device state is no longer "${state}"

the device state is no longer "${state}"
    ${device_current_state}=    Device: Function: Gather Device State
    Should Not Be Equal As Strings    ${device_current_state}    ${state}

the device should not be logged-in successfully
    ${device_current_state}=    Device: Function: Gather Device State
    Should Be Equal As Strings    ${device_current_state}    Idle

the device should be reached FLU Screen
    ${device_current_state}=    Device: Function: Gather Device State
    Should Be Equal As Strings    ${device_current_state}    InService

the device is fully Commissioned
    wait until keyword succeeds  120 sec  5 sec  Device: Screen: Validate Screen  Idle
    ${device_current_state}=    Device: Function: Gather Device State
    Should Not Be Equal As Strings    ${device_current_state}    UnCommissioned

the device ${r:(should be|is)} signed onto a Shift
    ${device_current_state}=    Device: Function: Gather Device State
    Should Be Equal As Strings    ${device_current_state}    InService

the device screen should contain ${exp_text} ${r:(.*)?}
    Device: Screen: Validate Screen Contains Text     ${exp_text}

the payment mode should be ${paymentlabel}
  ${vars} =  Create Dictionary  PaymentModeLabel=${paymentlabel}
  Device: Screen: Validate Screen With Variables  Flu  ${vars}

the ${ScreenName} screen should be displayed with "${exp_text_label}" label
    ${vars} =  Create Dictionary  DisplayLable=${exp_text_label}
    Device: Screen: Validate Screen With Variables  ${ScreenName}    ${vars}

the ${ScreenName} screen should be displayed with "${exp_text_label}" fare label
    ${exp_text_label_splited}    Split String    ${exp_text_label}    $
    ${exp_text_label}   Use   ${exp_text_label_splited}[0]
    ${vars} =  Create Dictionary  DisplayLable=${exp_text_label}
    Device: Screen: Validate Screen With Variables  ${ScreenName}    ${vars}

the ${ScreenName} screen should be displayed with "${exp_text_label}" label and "${exp_text_info}" info
    ${vars} =  Create Dictionary  DisplayLable=${exp_text_label}    DisplayInfo=${exp_text_info}
    Device: Screen: Validate Screen With Variables  ${ScreenName}    ${vars}

the ${ScreenName} screen should be displayed with "${exp_text_label}" fare label and "${exp_text_info}" fare info
    ${exp_text_label_splited}    Split String    ${exp_text_label}    $
    ${exp_text_label}   Use   ${exp_text_label_splited}[0]
    ${exp_text_info_splited}    Split String    ${exp_text_info}    $
    ${exp_text_info}   Use   ${exp_text_info_splited}[0]
    ${vars} =  Create Dictionary  DisplayLable=${exp_text_label}    DisplayInfo=${exp_text_info}
    Device: Screen: Validate Screen With Variables  ${ScreenName}    ${vars}

the current device details should be displayed in Device Settings screen
    ${vars} =  Create Dictionary
    ...        HomeLocationBox=${current_device}[homelocation_code]
    ...        MountingPointBox=${current_device}[mounting_point_id]
    ...        TrayIdBox=${current_device}[tray_id]
    ...        FleetNumberBox=${current_device}[bus_no]
    Device: Screen: Validate Screen With Variables    DeviceSettings    ${vars}

the following details should be displayed on the screen
    [Arguments]  ${screen}  &{screen_data}
    ${screen_data} =  Create Dictionary  &{screen_data}
    Device: Screen: Validate Screen With Variables     ${screen}    ${screen_data}

the ${screen_name} screen ${r:(is|should be)} displayed and ${element} is ${element_text}
    ${element}    Convert To String     ${element}
    ${element_text}    Convert To String     ${element_text}
    ${vars} =  Create Dictionary
    ...        ${element}=${element_text}
    Device: Screen: Validate Screen With Variables    ${screen_name}    ${vars}

the ${screen_name} screen ${r:(is|should be)} displayed with additional ${element_text} as a ${element}
    ${element}    Convert To String     ${element}
    ${element_text}    Convert To String     ${element_text}
    ${vars} =  Create Dictionary
    ...        ${element}=${element_text}
    Device: Screen: Validate Screen    ${screen_name}
    Device: Screen: Assert Element Values in layout     ${vars}

the DataView screen contains the follows amount of rows
    [Arguments]  ${rows_number}

    FOR  ${num}  IN RANGE  1  ${rows_number} + 1
       assert element in the device layout  {"Name": "Row${num}"}
       assert element in the device layout  {"Name": "Row${num}Label1"}
       assert element in the device layout  {"Name": "Row${num}Label2"}
       assert element in the device layout  {"Name": "Underline${num}"}
    END