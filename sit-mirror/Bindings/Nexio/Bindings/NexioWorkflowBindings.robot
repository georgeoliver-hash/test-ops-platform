*** Settings ***
Documentation     Nexio driver workflow bindings — duty entry, trip selection, and
...               sign-off flow keywords called directly from test cases.
...               Delegates to ETM: Duty: * intent keywords (ETMInteractionUtility)
...               which dispatch to the Linux/React platform implementation.

Resource    ../../ETM/Utility/ETMInteractionUtility.robot

*** Keywords ***
the duty entry keypad is visible
    assert element in the device layout    {"Text": "CONFIRM"}

a screenshot is captured for evidence
    Take Nexio Screenshot

the ${actor} enters duty number "${duty}"
    ETM: Duty: Enter Duty    ${duty}

the ${actor} presses CONFIRM
    click device ui button    CONFIRM    ${False}

the duty trip screen is reached
    Wait Until Keyword Succeeds    30s    1s
    ...    assert element in the device layout    {"Text": "Unscheduled Trip"}

# ----------------------------------------------------------------------------|
#  Trip selection — random pick path used by demo / smoke suites.
# ----------------------------------------------------------------------------|

the trip selection screen is showing
    [Documentation]    Ensure the device is on the real /TripSelection screen. After a fresh
    ...                sign-on it may instead be on the duty-entry screen (/RouteSignOn); the
    ...                onboarding intent enters the test duty and confirms as needed. Screen
    ...                identity is checked by route Name, not by element text — "Unscheduled
    ...                Trip" appears on BOTH screens and is not a safe sentinel.
    ETM: Duty: Onboard To Trip Selection

the ${actor} picks a random trip
    [Documentation]    Kept for backward compatibility with coverage suites. The smoke path
    ...                uses "selects the first available trip" for determinism.
    ETM: Duty: Select Random Trip

the ${actor} selects the first available trip
    [Documentation]    Deterministically select the topmost trip, then advance through the
    ...                trip-detail / shift-summary screens to FLU. Repeatable — no random pick.
    ETM: Duty: Select First Trip
    ETM: Duty: Advance To FLU
