*** Settings ***
Library  REST
Library  OperatingSystem
Library  Collections
Library  String
Library  Process

Resource    ../../../Common/Utility/RobotExtensionsUtility.robot

*** Keywords ***
the ${card_type} smartcard is tapped with types ${card_fields_raw}
    ${card_fields} =  Split String  ${card_fields_raw}
    ${card_data} =  Smartcard: Search for card  ${card_type}  ${card_fields}
    ${card_image} =  Smartcard: Process smartcard  ${card_data}
    Log  Presenting smartcard ${card_data}[ID]
    Device: Smartcard: Present Card  ${card_image}  ${False}

the ${card_type} smartcard is presented with types ${card_fields_raw}
    ${card_fields} =  Split String  ${card_fields_raw}
    ${card_data} =  Smartcard: Search for card  ${card_type}  ${card_fields}
    ${card_image} =  Smartcard: Process smartcard  ${card_data}
    Log  Presenting smartcard ${card_data}[ID]
    Device: Smartcard: Present Card  ${card_image}

${r:(.* )?}present${r:(s)?} a ${valid_barcode} barcode to the device
    Device: Function: Present Barcode     ${valid_barcode}

${r:(.* )?}presents the ${card_type} smartcard
    ${card_fields} =  Split String  ${card_type}
    ${card_data} =  Smartcard: Search for card   common   ${card_fields}
    ${card_image} =  Smartcard: Process smartcard  ${card_data}
    Log  Presenting smartcard ${card_data}[ID]
    Set Test Variable    ${expected_display_label}    ${card_data}[Exp_Display_label]
    ${card_image} =    remove string    ${card_image}    \n
    Log  ${card_image}
    Device: Smartcard: Present Card  ${card_image}

${r:(.* )?}re-presents the ${card_type} smartcard after ${minutes} minutes
    Device: Smartcard: Re-Present Stored Card After Given Time    ${minutes}   ${last_presented_smartcard}

${r:(.* )?}remove and re-present the smartcard within passback time for product "${product_description}"
    Device: Smartcard: Remove Card
    ${passback_time}    SQLite: FaresProduct: Get PassbackTime by Product    ${product_description}
    log to console    ${passback_time}
    Device: Smartcard: Re-Present Stored Card After Given Time    ${passback_time}   ${last_presented_smartcard}

${r:(.* )?}removes the card and represent the same smartcard
    Device: Smartcard: Re-Present Card

${r:(.* )?}removes the card and represent the same smartcard after ${minutes} minutes
    Device: Smartcard: Re-Present Card After Given Time    ${minutes}

the same smartcard is presented again
    Device: Smartcard: Present Card  ${Empty}

the smartcard is removed from the device
    Device: Smartcard: Remove Card

