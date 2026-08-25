*** Settings ***
Documentation    Operator Options sub-menu — cancel Soft Reset and Ticket
...              History.
...
...              Navigation path:
...                sign on -> MENU key -> Operator Menu -> "Operator Options"
...                -> Operator Options screen: Soft Reboot / Ticket History /
...                   Paper Status / Display Settings / Message of the Day /
...                   Word and Color of the Day
...
...              Strings used:
...                OperatorMenu.OperatorOptions   = 'Operator Options'
...                OperatorOptions.Title          = 'Operator Options'
...                OperatorOptions.SoftReboot     = 'Soft Reboot'
...                OperatorOptions.TicketHistory  = 'Ticket History'
...                TicketHistory.Title            = 'Ticket History'
...                TicketHistory.Product          = 'Product Name'
...                TicketHistory.Time             = 'Date and Time'
...                TicketHistory.Price            = 'Price'
...
...              refs: C4099937, C4099942
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:options

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Cancel Soft Reboot Stays On Options Screen
    [Documentation]    Cancelling the Soft Reboot confirmation stays on the
    ...    Operator Options screen.
    ...
    ...    Operator Options -> Soft Reboot -> cancel/back -> still on
    ...    Operator Options. The device must NOT reboot after a cancel action.
    ...
    ...    ref: C4099937
    ${creds_id}=    Get Device Metadata Value    operator_id
    ${creds_pin}=    Get Device Metadata Value    operator_pin
    Skip If    not $creds_id or not $creds_pin
    ...    Operator credentials not seeded in devices.yaml metadata
    Ensure Signed Off
    ${signed_on}=    Sign On    ${creds_id}    ${creds_pin}    timeout=20.0
    Should Be True    ${signed_on}    Could not sign on with seeded credentials
    Sleep    1s
    ${navigated}=    Navigate To Operator Options
    Should Be True    ${navigated}
    ...    Could not navigate to Operator Options screen
    ${tapped}=    Tap Text    Soft Reboot
    Should Be True    ${tapped}    Could not tap 'Soft Reboot' in Operator Options
    # A confirmation dialog should appear — dismiss it with BACK / ESC / Cancel.
    Sleep    1s
    ${seen_before_cancel}=    Visible Texts
    # Try ESC first (the way6 C key), then BACK keycode.
    Press Esc Key
    Sleep    0.5s
    ${seen_after_esc}=    Visible Texts
    IF    "Operator Options" not in $seen_after_esc
        Go Back
        Sleep    0.5s
    END
    ${seen_after}=    Visible Texts
    List Should Contain Value    ${seen_after}    Operator Options
    ...    msg=After cancelling Soft Reboot the device did not return to Operator Options. Visible before cancel: ${seen_before_cancel}. Visible after: ${seen_after}

Ticket History Screen Loads
    [Documentation]    Operator Options -> Ticket History opens the Ticket
    ...    History screen.
    ...
    ...    The Ticket History screen must show its title and the column
    ...    headers (Product Name, Date and Time, Price).
    ...
    ...    ref: C4099942
    ${creds_id}=    Get Device Metadata Value    operator_id
    ${creds_pin}=    Get Device Metadata Value    operator_pin
    Skip If    not $creds_id or not $creds_pin
    ...    Operator credentials not seeded in devices.yaml metadata
    Ensure Signed Off
    ${signed_on}=    Sign On    ${creds_id}    ${creds_pin}    timeout=20.0
    Should Be True    ${signed_on}    Could not sign on with seeded credentials
    Sleep    1s
    ${navigated}=    Navigate To Operator Options
    Should Be True    ${navigated}
    ...    Could not navigate to Operator Options screen
    ${tapped}=    Tap Text    Ticket History
    Should Be True    ${tapped}    Could not tap 'Ticket History' in Operator Options
    ${shown}=    Wait For Text    Ticket History    timeout=10.0
    Should Be True    ${shown}    Ticket History screen title did not appear
    Assert Visible Labels    TicketHistory.Title    TicketHistory.Product
    ...    TicketHistory.Time    TicketHistory.Price    screen=Ticket History

*** Keywords ***
Navigate To Operator Options
    [Documentation]    Sign-on must already be complete. Opens Operator Menu
    ...    then Options.
    Press Menu Key
    ${menu_shown}=    Wait For Text    Operator Menu    timeout=5.0
    IF    not ${menu_shown}
        RETURN    ${False}
    END
    ${tapped}=    Tap Text    Operator Options
    IF    not ${tapped}
        RETURN    ${False}
    END
    ${opened}=    Wait For Text    Operator Options    timeout=5.0
    RETURN    ${opened}
