*** Settings ***
Documentation    Operator Break mode — enter and leave.
...
...              Navigation path (NIR mode):
...                sign on -> MENU key (KEY_F12) -> Operator Menu ->
...                "Operator Break"
...                break mode -> "Break End Sign On" (re-enter credentials) ->
...                main screen
...
...              Strings used:
...                OperatorMenu.Title      = 'Operator Menu'
...                OperatorMenu.Break      = 'Operator Break'
...                Driver.DriverOnBreak    = 'On break'
...                Driver.BreakEndSignOn   = 'Break End Sign On'
...
...              refs: C4099939, C4099940
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:options

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Enter Break Mode Shows On Break
    [Documentation]    Tapping Operator Break puts the device into break mode.
    ...
    ...    After entering break mode the device displays the break status
    ...    indicator ('On break') and the sign-on prompt for break-end
    ...    re-authentication ('Break End Sign On').
    ...
    ...    ref: C4099939
    ${creds_id}=    Get Device Metadata Value    operator_id
    ${creds_pin}=    Get Device Metadata Value    operator_pin
    Skip If    not $creds_id or not $creds_pin
    ...    Operator credentials not seeded in devices.yaml metadata
    Ensure Signed Off
    ${signed_on}=    Sign On    ${creds_id}    ${creds_pin}    timeout=20.0
    Should Be True    ${signed_on}    Could not sign on with seeded credentials
    Sleep    1s
    ${opened}=    Open Operator Menu
    Should Be True    ${opened}
    ...    Operator Menu did not appear after pressing the MENU key
    ${tapped}=    Tap Text    Operator Break
    Should Be True    ${tapped}
    ...    Could not tap 'Operator Break' in the Operator Menu
    # Break mode can show either 'On break' (Driver.DriverOnBreak) or the
    # re-authentication prompt 'Break End Sign On' (Driver.BreakEndSignOn).
    ${reached}=    Wait For Any Text    On break    Break End Sign On    timeout=10.0
    ${visible}=    Visible Texts
    Should Be True    ${reached}
    ...    Device did not enter break mode after tapping 'Operator Break'. Visible: ${visible}

Leave Break Mode Returns To Main
    [Documentation]    Signing back in from break mode returns to the main
    ...    FLU screen.
    ...
    ...    After entering break mode the operator authenticates via
    ...    'Break End Sign On', which should return the device to the normal
    ...    signed-on state.
    ...
    ...    ref: C4099940
    ${creds_id}=    Get Device Metadata Value    operator_id
    ${creds_pin}=    Get Device Metadata Value    operator_pin
    Skip If    not $creds_id or not $creds_pin
    ...    Operator credentials not seeded in devices.yaml metadata
    Ensure Signed Off
    ${signed_on}=    Sign On    ${creds_id}    ${creds_pin}    timeout=20.0
    Should Be True    ${signed_on}    Could not sign on with seeded credentials
    Sleep    1s
    ${opened}=    Open Operator Menu
    Should Be True    ${opened}
    ...    Operator Menu did not appear after pressing the MENU key
    ${tapped}=    Tap Text    Operator Break
    Should Be True    ${tapped}
    ...    Could not tap 'Operator Break' in the Operator Menu
    ${reached}=    Wait For Any Text    On break    Break End Sign On    timeout=10.0
    Should Be True    ${reached}    Device did not enter break mode
    # Sign back in from break mode using the same credentials.
    ${signed_back_on}=    Sign On    ${creds_id}    ${creds_pin}    timeout=20.0
    Should Be True    ${signed_back_on}
    ...    Could not sign back in from break mode with seeded credentials
    # Should land back at the main menu — any of these texts confirms it.
    ${back}=    Wait For Any Text    Rail FLU    Rail    Ulsterbus    Basket
    ...    Operator Menu    timeout=15.0
    ${visible}=    Visible Texts
    Should Be True    ${back}
    ...    Did not return to the main/operator menu after break-end sign-on. Visible: ${visible}

*** Keywords ***
Open Operator Menu
    [Documentation]    Press the MENU key and wait for the Operator Menu
    ...    title. Returns True if the Operator Menu became visible within 5s.
    Press Menu Key
    ${reached}=    Wait For Text    Operator Menu    timeout=5.0
    RETURN    ${reached}
