*** Settings ***
Documentation     Generic ETM BDD step keywords for the driver workflow smoke test.
...               Uses the ETM intent layer exclusively — no platform-specific calls.
...               Compatible with any ETM platform that has an ETMInteractionUtility implementation.

*** Keywords ***
the trip selection screen is showing
    [Documentation]    Deterministically onboard to the trip-selection screen after sign-on.
    ETM: Duty: Onboard To Trip Selection

the ${actor} selects the first available trip
    [Documentation]    Select the topmost trip and advance through the shift summary to FLU.
    ETM: Duty: Select First Trip
    ETM: Duty: Advance To FLU

the FLU screen is active
    [Documentation]    Assert the FLU ticket-issue screen is visible.
    ETM: FLU: Assert Screen Active

at least one FLU destination is visible
    [Documentation]    Assert that at least one £-priced destination row is loaded on the FLU screen.
    ETM: FLU: Assert Destinations Visible

the ${actor} selects a random FLU destination
    [Documentation]    Pick a random priced destination and add it to the basket.
    ETM: FLU: Select Random Destination

the selected destination appears in the basket
    [Documentation]    Assert the basket shows a fare entry.
    Wait Until Keyword Succeeds    15s    1s    assert element in the device layout    {"Text": "1 x"}

the ${actor} issues the ticket via a random payment path
    [Documentation]    Issue the ticket via the ISSUE button.
    ETM: FLU: Issue Via Random Payment

a ticket is printed
    [Documentation]    Assert the FLU screen returned to the empty basket state after ticket issue.
    Wait Until Keyword Succeeds    15s    1s    assert element in the device layout    {"Text": "No products currently selected..."}
