*** Settings ***
Resource    ../../../Common/Utility/SmartcardUtility.robot
Resource    ../Utility/PaymentCardUtility.robot
Library     ../../../Common/CustomLibs/TimeTools.py

*** Keywords ***
clear payment device history of received deny lists
    Device: PaymentCard: Clear Deny List


there was a full deny list downloaded "${relative_date}"
    ${date_time} =    TimeTools.Relative To Datetime    ${relative_date}
    ${timestamp} =    Convert Date    ${date_time}    epoch
    ${timestamp} =    Convert To Integer    ${timestamp}
    ${values} =    Create Dictionary
    ...    DenyListLastDownloaded    /Date(${timestamp})/
    ...    DenyListUpdateTimestamp    ${timestamp}
    Device: Function: Modify Device file    ${current_device}[Paths][PaymentTerminalConfig]    ${values}


the payment device configuration is reset
    ${values} =    Create Dictionary
    ...    DenyListLastDownloaded    /Date(-62135596725)/
    ...    DenyListUpdateTimestamp    ${0}
    Device: Function: Modify Device file    ${current_device}[Paths][PaymentTerminalConfig]    ${values}


a full list was sent to the payment device with the following tokens:
    [Arguments]    @{expected_tokens}
    ${full_list} =    Device: PaymentCard: Get Full Deny List
    Lists Should Be Equal    ${full_list}[Additions]    ${expected_tokens}

a delta list was sent to the payment device with the following tokens:
    [Arguments]    @{expected_tokens}
    ${delta_list} =    Device: PaymentCard: Get Delta Deny List
    @{add_tokens} =  Create List
    @{remove_tokens} =  Create List
    FOR    ${token_and_type}    IN    @{expected_tokens}
        ${list_type}    ${token} =    Split String    ${token_and_type}    max_split=1
        ${list_type} =    Convert To Lower Case    ${list_type}
        Append To List    ${${list_type}_tokens}    ${token}
    END
    Lists Should Be Equal    ${delta_list}[Additions]    ${add_tokens}
    Lists Should Be Equal    ${delta_list}[Removals]     ${remove_tokens}

${r:(.* )?}taps a ${valid} ${card_scheme} payment card
    ${card_scheme} =   Convert To Lower Case   ${card_scheme}
    ${card_args} =   Create List   emv   ${card_scheme}
    ${card_data} =  Smartcard: Search for card   common   ${card_args}
    ${card_image} =  Smartcard: Process smartcard  ${card_data}
    Log  Presenting valid payment ${card_scheme} card ${card_data}[ID]
    IF  '${valid}' == 'valid'
      Device: PaymentCard: Tap Card  ${card_image}  AuthorisationApproved
    ELSE
      Device: PaymentCard: Tap Card  ${card_image}  AuthorisationDeclined
    END

