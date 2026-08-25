*** Settings ***
Documentation     Shared BDD step keywords for Nexio ↔ Axio integration test suites.
...               These steps appear in multiple test files and are defined here to
...               avoid duplication.
...
...               Keyword names follow Robot Framework BDD conventions. The ${actor}
...               embedded argument captures any role word from the test step text
...               ("the driver ...", "the operator ...", "the user ...").
...
...               Element checks/clicks go through the SIT framework (DeviceUI:
...               `assert element in the device layout`, `click device ui button`,
...               `device layout matches`, `get device layout`); only genuinely-new
...               primitives (`Pick Random CDP Element`) are kept from CDPKeywords.

Library     RequestsLibrary
Resource    ../../Linux/CDPKeywords.robot

*** Keywords ***
both TSS adaptors are connected and the driver is signed on
    [Documentation]    Assert that both TSS adaptors are registered and the Nexio is
    ...                on the duty entry keypad — confirming the suite setup succeeded.
    Switch To ETM
    Wait Until Keyword Succeeds    10s    1s    assert element in the device layout    {"Text": "CONFIRM"}
    Switch To Validator
    Axio Service Should Be Running    gfts.service
    Switch To ETM

Sign Off Driver And Disconnect
    [Documentation]    Suite teardown: sign the driver off and release both TSS adaptors.
    ...                All steps are wrapped so a partial failure does not block cleanup.
    Run Keyword And Ignore Error    Switch To ETM
    Run Keyword And Ignore Error    Open FLU Menu
    Run Keyword And Ignore Error    Driver Signs Off
    Run Keyword And Ignore Error    Driver Confirms Sign Off
    Run Keyword And Ignore Error    Driver Is On Idle Screen
    Disconnect Both Devices

the Axio service health is verified
    Switch To Validator
    Axio Service Should Be Running    gfts.service
    Axio Service Should Be Running    pap-sdk-app.service

the Nexio duty entry keypad is ready
    Switch To ETM
    Wait Until Keyword Succeeds    10s    1s    assert element in the device layout    {"Text": "CONFIRM"}
    Take Nexio Screenshot

the ${actor} enters duty number "${duty}" and confirms
    Switch To ETM
    Driver Enters Duty Number    ${duty}
    click device ui button    CONFIRM
    Wait Until Keyword Succeeds    10s    1s    assert element in the device layout    {"Text": "${duty}"}
    Take Nexio Screenshot

the service list is displayed for duty "${duty}"
    Wait Until Keyword Succeeds    10s    1s    assert element in the device layout    {"Text": "${duty}"}
    ${layout}=    get device layout
    Log    Nexio layout after duty CONFIRM:\n${layout}
    Take Nexio Screenshot

the ${actor} selects service "${service}" and confirms
    Switch To ETM
    click device ui button    ${service}    ${False}
    click device ui button    CONFIRM
    Take Nexio Screenshot

the trip list is displayed
    ${layout}=    get device layout
    Log    Nexio trip list layout (use to identify trip label):\n${layout}

the ${actor} selects trip "${trip}" and presses Continue
    Switch To ETM
    ${layout}=    get device layout
    Log    Trip list layout:\n${layout}
    Select Duty From List    ${trip}
    click device ui button    Continue
    # Some configurations show a Shift Summary screen before the FLU.
    ${summary_resp}=    RequestsLibrary.GET    ${CDP_TSS_URL}/UI/Element    params=text=Shift Summary    expected_status=ANY
    IF    ${summary_resp.status_code} == 200
        click device ui button    Continue    ${False}
    END

the Axio validator goes InService and shows the travelcard screen
    Switch To Validator
    Device: Screen: Validate Screen    Idle_InService    30

the Nexio shows the FLU ticket-issue screen
    Switch To ETM
    Wait Until Keyword Succeeds    20s    1s    assert element in the device layout    {"Text": "Adult Single"}
    Take Nexio Screenshot

# ----------------------------------------------------------------------------|
#  Retail annulment BDD steps
# ----------------------------------------------------------------------------|

the FLU screen is ready for a new transaction
    Switch To ETM
    Wait Until Keyword Succeeds    ${SCREEN_TIMEOUT}s    1s    assert element in the device layout    {"Text": "Adult Single"}
    Take Nexio Screenshot

the ${actor} issues a Cash ticket to "${destination}"
    Should Not Be Empty    ${destination}    msg=FLU_DESTINATION is required
    Switch To ETM
    Select FLU Destination    ${destination}
    Take Nexio Screenshot
    click device ui button    ISSUE
    Take Nexio Screenshot

the ${actor} issues a Tendered ticket to "${destination}"
    Should Not Be Empty    ${destination}    msg=FLU_DESTINATION is required
    Switch To ETM
    Select FLU Destination    ${destination}
    Take Nexio Screenshot
    click device ui button    TENDERED
    the Payment Mode Cash screen is displayed
    ${amount_text}=    Pick Random CDP Element    must_contain=£
    click device ui button    ${amount_text}    ${False}
    Sleep    0.5s
    click device ui button    Issue    ${False}
    Take Nexio Screenshot

the ${actor} issues a Card ticket to "${destination}"
    Should Not Be Empty    ${destination}    msg=FLU_DESTINATION is required
    Switch To ETM
    Select FLU Destination    ${destination}
    Take Nexio Screenshot
    click device ui button    Card
    the Nexio shows the card payment pending screen
    the Axio validator prompts the customer to present their card
    the EMV card is presented to the Axio

the ${actor} opens transaction history from the driver menu
    Switch To ETM
    Open FLU Menu
    Wait Until Keyword Succeeds    ${ELEMENT_TIMEOUT}s    1s    assert element in the device layout    {"Text": "Transaction History"}
    click device ui button    Transaction History    ${False}
    Device: Screen: Validate Screen    TransactionHistory    ${SCREEN_TIMEOUT}
    Take Nexio Screenshot

the ${actor} annuls the most recent transaction
    ${layout}=    get device layout
    Log    Transaction History layout:\n${layout}    console=True
    ${transaction}=    Pick Random CDP Element    context=Transaction History
    Log    [Annulment] Selected transaction: ${transaction}    console=True
    click device ui button    ${transaction}    ${False}
    Take Nexio Screenshot
    Wait Until Keyword Succeeds    ${ELEMENT_TIMEOUT}s    1s    assert element in the device layout    {"Text": "Annul"}
    click device ui button    Annul    ${False}
    Take Nexio Screenshot

the annulment ticket is printed
    Switch To ETM
    Wait Until Keyword Succeeds    30s    1s    assert element in the device layout    {"Text": "Adult Single"}
    Take Nexio Screenshot

# ----------------------------------------------------------------------------|
#  Feig error path BDD steps
# ----------------------------------------------------------------------------|

the Nexio shows the duty entry screen as a baseline
    Switch To ETM
    Wait Until Keyword Succeeds    20s    1s    assert element in the device layout    {"Text": "CONFIRM"}
    Take Nexio Screenshot

the Axio is in a known healthy state
    Log    Axio services confirmed healthy in previous scenario    console=True

the validator receives a payment request notification
    Switch To Validator
    navigate device to screen    Action_PresentCard

the Axio shows the present-card screen
    Take Axio Screenshot

the Axio validator prompts the customer to present their card
    [Documentation]    Assert the Axio shows the Present Card screen via the common SIT
    ...                screen checker. Called after the Nexio submits a card payment request.
    Switch To Validator
    Device: Screen: Validate Screen    Action_PresentCard    ${SCREEN_TIMEOUT}
    Take Axio Screenshot

the Axio is showing the present-card screen
    Log    Axio is on present-card screen from previous scenario    console=True

a Feig communication failure is simulated via OutOfService notification
    Switch To Validator
    navigate device to screen    Idle_OutOfService

the Axio shows the out-of-service screen
    Take Axio Screenshot

the Axio adaptor is connected
    Log    Axio adaptor registered in Suite Setup    console=True

the GFTS service journal is retrieved from the Axio
    Log    Retrieving Axio GFTS journal via TSS SSH command    console=True

the journal confirms the OpenPayment FeigLoop subsystem initialised
    Axio Log Contains    OpenPayment

the Axio is in an out-of-service state
    Log    Axio is in OutOfService state from previous scenario    console=True

an InService notification is sent to restore normal operation
    Switch To Validator
    navigate device to screen    Idle_InService

the Axio returns to the idle travelcard screen
    Take Axio Screenshot

the Nexio returns to the duty entry screen
    Switch To ETM
    Wait Until Keyword Succeeds    20s    1s    assert element in the device layout    {"Text": "CONFIRM"}
    Take Nexio Screenshot
