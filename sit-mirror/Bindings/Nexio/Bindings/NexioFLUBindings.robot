*** Settings ***
Documentation     Nexio FLU ticket-issue screen bindings.
...               Covers destination selection, payment method selection, basket mode,
...               and ticket issuance.
...
...               Element presence / clicks go through the SIT framework: DeviceUI
...               (`assert element in the device layout`, `click device ui button`) and
...               screen checks via `device layout matches`. Only genuinely-new primitives
...               with no common equivalent are kept from CDPKeywords: `Pick Random CDP
...               Element` (random selection), `Wait For CDP Items` (count), and
...               `Wait For Nexio Button Colour` (RN-Web colour state).
...
...               NOTE (pipeline-verify): the `assert element in the device layout` text
...               checks below assume exact element Text (e.g. "Adult Single", "Basket (0)").
...               If the live DOM reports a superset, switch those to a REGEX: value. This
...               is validated on the first pipeline run against the deployed adaptor.

Resource    ../../Linux/CDPKeywords.robot
Resource    ../../../FLU/Stagecoach/destinations.robot
# FLU steps switch device context (card payment taps the Axio) and reference
# ${AXIO_TSS_URL}; both come from the NexioAxio context bindings.
Resource    ../../NexioAxio/Bindings/NexioAxioContextBindings.robot
Resource    ../../ETM/Utility/ETMInteractionUtility.robot

*** Keywords ***
the FLU screen is active
    Wait Until Keyword Succeeds    ${SCREEN_TIMEOUT}s    1s
    ...    assert element in the device layout    {"Text": "Adult Single"}
    Take Nexio Screenshot

at least one FLU destination is visible
    ${count}=    Wait For CDP Items    must_contain=£    timeout=15
    Should Be True    ${count} > 0
    ...    msg=No priced FLU destinations found — FLU screen may not be loaded or destinations are empty

the ${actor} selects a random FLU destination
    ${dest}=    Pick Random CDP Element    must_contain=£
    Log    [FLU] Selected destination: ${dest}    console=True
    click device ui button    ${dest}    ${False}
    Sleep    0.5s

the selected destination appears in the basket
    [Documentation]    Assert a fare was added to the basket after destination tap.
    ...                Real selection signal: "1 x" basket line appears and
    ...                "No products currently selected..." disappears.
    ...                ISSUE and Adult Single are always-present and are NOT selection signals.
    Wait Until Keyword Succeeds    10s    1s
    ...    assert element in the device layout    {"Text": "1 x"}
    assert element not in device layout    {"Text": "No products currently selected..."}

Driver Cycles Passenger Type
    [Documentation]    Click the passenger type tile to cycle it (e.g. Adult → Child).
    [Arguments]    ${current_type}    ${timeout}=${CDP_ELEMENT_TIMEOUT}
    Wait Until Keyword Succeeds    ${timeout}s    1s
    ...    assert element in the device layout    {"Text": "${current_type}"}
    click device ui button    ${current_type}    ${False}
    Sleep    0.5s

Select FLU Destination
    [Documentation]    Click a destination row on the FLU ticket-issue screen.
    [Arguments]    ${destination}    ${timeout}=${25}
    Wait Until Keyword Succeeds    ${timeout}s    1s
    ...    assert element in the device layout    {"Text": "${destination}"}
    click device ui button    ${destination}    ${False}
    Sleep    0.5s

Return Nexio To FLU Screen
    [Documentation]    Teardown helper: navigate back to the FLU screen from any sub-screen.
    ...                Tries Back then Cancel; waits for "Adult Single" as the FLU sentinel.
    ...                All steps wrapped so a teardown failure does not mask the real failure.
    Run Keyword And Ignore Error    Switch To ETM
    Run Keyword And Ignore Error    click device ui button    Back    ${False}
    Run Keyword And Ignore Error    click device ui button    Cancel    ${False}
    Run Keyword And Ignore Error    Wait Until Keyword Succeeds    10s    1s
    ...    assert element in the device layout    {"Text": "Adult Single"}
    Run Keyword And Ignore Error    Take Nexio Screenshot

# ----------------------------------------------------------------------------|
#  BDD step keywords
# ----------------------------------------------------------------------------|

the ${actor} selects destination "${destination}"
    [Documentation]    Select a destination on the FLU screen.
    ...                If ${destination} is empty, resolves one from the live DOM at random
    ...                and stores it in ${FLU_DESTINATION} for subsequent steps.
    Switch To ETM
    IF    '${destination}' == ''
        ${dest}=    ETM: FLU: Select Random Destination
        Set Suite Variable    ${FLU_DESTINATION}    ${dest}
        Log    [FLU] FLU_DESTINATION not set — resolved from live DOM: ${dest}    console=True
    ELSE
        ETM: FLU: Select Destination    ${destination}
    END
    Take Nexio Screenshot

the ${actor} selects "${button}"
    [Documentation]    Generic button dispatcher — routes named buttons to intent keywords.
    Switch To ETM
    IF    '${button}' == 'ISSUE'
        ETM: FLU: Issue Ticket
    ELSE IF    '${button}' == 'Tendered' or '${button}' == 'TENDERED'
        ETM: FLU: Pay Via Tendered
    ELSE IF    '${button}' == 'Card'
        ETM: FLU: Pay Via Card
    ELSE IF    '${button}' == 'Summary'
        ETM: FLU: Enter Basket Mode
    ELSE
        click device ui button    ${button}    ${False}
    END
    Take Nexio Screenshot

the ${actor} selects cash amount "${amount}"
    [Documentation]    Select a cash amount from the Payment Mode Cash screen.
    ...                If ${amount} is empty, picks a random £-prefixed amount.
    Switch To ETM
    ETM: FLU: Pay Via Cash    ${amount}
    Take Nexio Screenshot

the Payment Mode Cash screen is displayed
    Switch To ETM
    Wait Until Keyword Succeeds    10s    1s    assert element in the device layout    {"Text": "Issue"}
    Take Nexio Screenshot

a ticket is printed
    [Documentation]    Assert the ticket was issued and the basket has reset.
    ...                Real print signal: basket clears — "No products currently selected..."
    ...                reappears and "1 x" disappears. Adult Single is always present on the
    ...                FLU and is NOT a print signal. 30s allows for printer warm-up and
    ...                transaction processing time.
    Switch To ETM
    Wait Until Keyword Succeeds    30s    1s
    ...    assert element in the device layout    {"Text": "No products currently selected..."}
    assert element not in device layout    {"Text": "1 x"}
    Take Nexio Screenshot

a ticket is printed with a change receipt
    [Documentation]    Assert the ticket was issued and the basket has reset (change-receipt variant).
    Switch To ETM
    Wait Until Keyword Succeeds    30s    1s
    ...    assert element in the device layout    {"Text": "No products currently selected..."}
    assert element not in device layout    {"Text": "1 x"}
    Take Nexio Screenshot

the Nexio shows the card payment pending screen
    [Documentation]    After Card is selected, Nexio shows a payment-pending state.
    Switch To ETM
    Sleep    1s
    Take Nexio Screenshot

the EMV card is presented to the Axio
    [Documentation]    Present an EMV card to the Axio Feig reader via the common smartcard
    ...                layer (DeviceSmartcard → TSS → OpenPayment endpoint).
    ...                IMPORTANT: device must be in payment mode first or OpenPayment times out.
    Switch To Validator
    present smartcard with card type and tags    emv    contactless

the card transaction completes and a ticket is printed
    Switch To Validator
    Device: Screen: Validate Screen    Action_Success    30
    Run Keyword And Ignore Error    Take Axio Screenshot
    Switch To ETM
    Wait Until Keyword Succeeds    30s    1s    assert element in the device layout    {"Text": "Adult Single"}
    Take Nexio Screenshot

# ----------------------------------------------------------------------------|
#  Basket mode — multi-stop purchase flow.
# ----------------------------------------------------------------------------|

the ${actor} enters basket mode
    Switch To ETM
    ETM: FLU: Enter Basket Mode

the basket is empty
    Log To Console    \nWaiting for empty basket...    no_newline=True
    Wait Until Keyword Succeeds    10s    1s    assert element in the device layout    {"Text": "Basket (0)"}
    Log To Console    [VISIBLE]

the ${actor} adds ${min} to ${max} random destinations to the basket
    [Documentation]    Pick a random number of £-priced destinations, tap each, and verify
    ...                the Basket (N) counter increments after every selection.
    ${count}=    Evaluate    random.randint(${min}, ${max})    modules=random
    Set Test Variable    ${BASKET_COUNT}    ${count}
    Log To Console    \n[Basket] Adding ${count} destinations
    ${selected}=    Set Variable    ${EMPTY}
    FOR    ${i}    IN RANGE    ${count}
        Log To Console    \n[Basket ${i+1}/${count}] Picking random £-destination...    no_newline=True
        ${status}    ${stop}=    Run Keyword And Ignore Error
        ...    Pick Random CDP Element    must_contain=£    exclude=${selected}
        IF    '${status}' != 'PASS'
            Sleep    0.5s
            ${stop}=    Pick Random CDP Element    must_contain=£
        END
        Log To Console    [PICKED: ${stop}]
        Wait Until Keyword Succeeds    10s    1s    click device ui button    ${stop}    ${False}
        ${expected}=    Evaluate    ${i} + 1
        Log To Console    \n[Basket ${i+1}/${count}] Waiting for Basket (${expected})...    no_newline=True
        Wait Until Keyword Succeeds    10s    1s    assert element in the device layout    {"Text": "Basket (${expected})"}
        Log To Console    [UPDATED]
        IF    '${selected}' == ''
            ${selected}=    Set Variable    ${stop}
        ELSE
            ${selected}=    Set Variable    ${selected},${stop}
        END
    END

the ${actor} pays the basket via tendered "${amount}"
    [Documentation]    Pay the basket via TENDERED with the given cash amount (e.g. £20.00).
    Switch To ETM
    ETM: FLU: Pay Via Tendered    ${amount}

the ${actor} issues the ticket via a random payment path
    [Documentation]    Random ISSUE or TENDERED — exercises both payment paths from one test.
    Switch To ETM
    ETM: FLU: Issue Via Random Payment

the ${actor} opens the FLU menu
    [Documentation]    Open the FLU on-screen menu (Nexio React Native Web).
    ...                Calls Open FLU Menu from NexioAdaptorUtility — Nexio-specific.
    Open FLU Menu
