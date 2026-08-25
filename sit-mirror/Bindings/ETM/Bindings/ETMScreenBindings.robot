*** Settings ***
Documentation     Keywords for user interactions with ETM screen — generic across all
...               ETM platforms (WEC, Linux). Platform-specific quirks (hardware taps,
...               Nexio colour polling) live in the device-model sliver.
...
...               Imports its specific dependencies directly — NOT the Bindings/ aggregator
...               (__Resources.robot). Importing the aggregator would drag ETMWorkflowBindings
...               into every consumer (e.g. the Nexio graph pulls this file in), colliding its
...               generic FLU steps with the device-specific NexioFLUBindings versions.
Resource      ../../Common/Bindings/UserInteractionsBindings.robot
Resource      ../../Common/Utility/ScreensUtility.robot
Resource      ../Utility/ETMInteractionUtility.robot

*** Keywords ***
${r:(.* )?}confirm${r:(s)?} the entry
    [Documentation]    Intent step: commit a typed text entry. Platform-dispatched (WEC presses
    ...                ENTER; Linux stub). Replaces the legacy "press the ENTER" mechanics step
    ...                ONLY where the ENTER commits typed text — for the FLU stop-selection
    ...                commit use "issues the ticket for the selected stop" instead.
    ETM: Screen: Confirm Entry

# ---------------------------------------------------------------------------
# Driver menu / traveling screen — generic ETM vocabulary (all platforms).
# Moved from NexioDriverMenuBindings: these use only the common framework
# (Device: Screen: Validate Screen, navigate device to screen, get device layout,
# assert element in the device layout, click device ui button) with no
# model-specific calls.
# ---------------------------------------------------------------------------

the traveling screen is active
    [Documentation]    Polls until the active-duty screen is visible (FLU/TicketsScreen
    ...                or TravelingScreen — both are valid for this step).
    ...                Uses get device layout (generic) rather than DOMSnapshot so it
    ...                does not block during React's initial bootstrap on Linux devices.
    ${end_time}=    Evaluate    time.time() + ${SCREEN_TIMEOUT}    modules=time
    WHILE    True
        ${layout}=    get device layout
        ${attrs}=    Get From Dictionary    ${layout}    Attributes    &{EMPTY}
        ${title}=    Get From Dictionary    ${attrs}    Title    ${EMPTY}
        ${name}=    Get From Dictionary    ${attrs}    Name    ${EMPTY}
        IF    'Traveling' in '${title}' or 'Traveling' in '${name}' or 'TicketsScreen' in '${title}' or 'FLU' in '${name}'
            BREAK
        END
        ${now}=    Evaluate    time.time()    modules=time
        IF    ${now} > ${end_time}
            Fail    Active duty screen not reached. Last name: '${name}' title: '${title}'
        END
        Sleep    1s
    END

the driver menu displays shift information
    assert element in the device layout    {"Text": "REGEX:.*Shift Details.*"}

the driver menu shows all navigation options
    assert element in the device layout    {"Text": "REGEX:.*Start New Trip.*"}
    assert element in the device layout    {"Text": "REGEX:.*Transaction History.*"}
    assert element in the device layout    {"Text": "REGEX:.*Interim Report.*"}
    assert element in the device layout    {"Text": "REGEX:.*Sign[- ]Off.*"}
    assert element in the device layout    {"Text": "REGEX:.*Print Report.*"}

the driver menu is open
    Device: Screen: Validate Screen    DriverMenu    ${SCREEN_TIMEOUT}

the ${actor} selects Transaction History
    click device ui button    Transaction History    ${False}

the transaction history screen is displayed
    Device: Screen: Validate Screen    TransactionHistory    ${SCREEN_TIMEOUT}

the transaction history screen is active
    Device: Screen: Validate Screen    TransactionHistory    5

the ${actor} navigates back to the driver menu
    [Documentation]    Navigate to DriverMenu using the screenflow algorithm.
    ...                The algorithm handles Back vs JS_Navigate transparently.
    navigate device to screen    DriverMenu

the driver menu is open again
    Device: Screen: Validate Screen    DriverMenu    ${SCREEN_TIMEOUT}

the ${actor} selects Interim Report
    click device ui button    Interim Report    ${False}

the interim report screen is displayed
    [Documentation]    STUB: no InterimReport screenflow template exists yet, so this
    ...                cannot validate the screen. Skips (rather than fails) so the
    ...                scenario is reported as not-run until an InterimReport template
    ...                exists — then switch to "Device: Screen: Validate Screen    InterimReport"
    ...                (see the sibling "the transaction history screen is displayed").
    Skip    Not Implemented: no InterimReport screenflow template — cannot validate the interim report screen

