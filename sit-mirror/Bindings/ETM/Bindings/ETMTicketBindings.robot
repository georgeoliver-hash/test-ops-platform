*** Settings ***
Documentation     Keywords for issuing ETM tickets (single, group, basket) and asserting
...               printed-ticket outcomes.
...
...               Imports its specific dependencies directly — NOT the Bindings/ aggregator
...               (__Resources.robot), which would drag ETMWorkflowBindings into every consumer
...               and collide its generic FLU steps with device-specific bindings.
Resource          ../../Common/Bindings/UserInteractionsBindings.robot
Resource          ../Utility/ETMScreenUtility.robot
Resource          ../Utility/ETMTicketUtility.robot
Resource          ../Utility/ETMInteractionUtility.robot

*** Keywords ***
${r:(.* )?}select${r:(s)?} ${index}${r:(st|nd|rd|th)} ${r:(.* )?}from the list
    ETM: Screen: Select Item on Current Screen By Row Number     ${index}

${r:(.* )?}issues ${productgroup} group ticket for ${grp_nums} people
    ${product_group_already_selected}=    Device: Interactions: Flu product is selected    ${productgroup}
    IF    not ${product_group_already_selected}
        Device: Interactions: Press UI Button    ${productgroup}
    END
    ETM: FLU: Issue Group Ticket    ${grp_nums}

${r:(.* )?}go${r:(es)} to driver menu
    ETM: Open Driver Menu

${r:(.* )?}issues ${productgroup} ticket
    ${product_group_already_selected}=    Device: Interactions: Flu product is selected    ${productgroup}
    IF    not ${product_group_already_selected}
        Device: Interactions: Press UI Button    ${productgroup}
    END
    ETM: FLU: Issue Ticket
    ${ticket_issue_datetime}=    Date: Get Current ISO Date    time_zone=local    result_format=%d/%m/%y | %H:%M
    Set Test Variable  ${ticket_issue_datetime}

${r:(.* )?}issues ${product_group} ticket on the ${screen_name} screen
    Navigate To    ${screen_name}
    IF   '${screen_name.lower()}' == 'flu'
        ${product_group_already_selected}=    Device: Interactions: Flu product is selected    ${product_group}
        IF    not ${product_group_already_selected}
            Device: Interactions: Press UI Button    ${product_group}
        END
        ETM: FLU: Issue Ticket
    ELSE
        Device: Interactions: Press UI Button    ${product_group}
    END

${r:(.* )?}issues group ${product_group} ticket with ${number_of_passengers} on the ${screen_name} screen
    Navigate To    ${screen_name}
    IF   '${screen_name.lower()}' == 'flu'
        ${product_group_already_selected}=    Device: Interactions: Flu product is selected    ${product_group}
        IF    not ${product_group_already_selected}
            Device: Interactions: Press UI Button    ${product_group}
        END
        ETM: FLU: Issue Group Ticket    ${number_of_passengers}
    ELSE
        Device: Interactions: Press UI Button    ${product_group}
    END

${r:(.* )?}confirm${r:(s)?} the basket of tickets
    ETM: FLU: Confirm Basket

${r:(.* )?}issue${r:(s)?} the ticket for the selected stop
    [Documentation]    Intent step replacing the legacy "user presses the ENTER" that follows
    ...                "user selects Nth stop from the list" — commits the selected fare row
    ...                and issues the ticket. Platform-dispatched (WEC = ENTER; Linux stub).
    ETM: FLU: Issue Ticket For Selected Stop

${r:(.* )?}add${r:(s)?} ${total_tickets} "${product_type}" tickets to the basket
     ${product_group_already_selected}=    Device: Interactions: Flu product is selected    ${product_type}
    IF    not ${product_group_already_selected}
        Device: Interactions: Press UI Button    ${product_type}
    END
    ETM: Ticket: Add Tickets to Basket    ${total_tickets}

the ticket printer ${r:(has|is)?} ${event_name}
    ETM: Ticket Printer: Create Event on device    ticket printer   ${event_name}

### THEN ###
the annulment ticket for the last issued ticket should be printed
    ETM: Ticket: Check Annulment Ticket

the printed ticket should contain the following values
    Register Table Keyword     ETM: Ticket: Check Ticket Field Values

the total number of printed tickets should be ${exp_tickets}
    ${count}     ETM: Ticket: Get Printed Tickets Count
    Should Be Equal As Numbers    ${exp_tickets}     ${count}

printed tickets should have unique incremented sequential serial numbers
    ETM: Ticket: Check Ticket Ids are Unique And Consecutive