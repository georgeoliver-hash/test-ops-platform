*** Settings ***
Library   ../../../Common/CustomLibs/Device.py
Resource  ../Utility/TicketUtility.robot
Resource  ../../../Common/Utility/RobotExtensionsUtility.robot

*** Keywords ***
${r:(.* )?}device has printed ${tickets} ticket${r:s?}
    check number of printed tickets    ${tickets}

the ${ticket_number} ticket contains the following values
    Wait Until Keyword Succeeds    30 seconds    1 second    get printed ticket  ${ticket_number}
    ${ticket}    get printed ticket  ${ticket_number}
    Set Test Variable    ${ticketdetails}    ${ticket}
    Register Table Keyword    Device: Ticket: Check field values
