*** Settings ***
Documentation    Device lockout after repeated failed sign-on attempts, and recovery via a
...              Supervisor card. TestRail C4099922 (destructive) + C4099923 (partial --
...              needs a physical Supervisor smartcard fixture), suite 30253, Functional /
...              Sign On & Session / Failures & Lockout.
Resource         ${CURDIR}/../../../../resources/translink/signon.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:auth

*** Test Cases ***
Device Locks After The Configured Number Of Failed Attempts
    [Documentation]    C4099922. GIVEN the TMS-configured failed-attempt lockout threshold,
    ...    WHEN the operator enters incorrect credentials that many times, THEN the device
    ...    locks and shows the Device Locked screen.
    ...
    ...    ${LOCKOUT_THRESHOLD} below is a placeholder, NOT a confirmed value -- GAP: the
    ...    real TMS-configured threshold for this environment must be confirmed before this
    ...    is run for real (the case's own precondition only says "e.g. 3").
    [Tags]    testrailid=C4099922    destructive
    [Setup]    Skip    GAP: needs the confirmed TMS-configured lockout threshold for this environment before running for real -- see [Documentation]
    ${LOCKOUT_THRESHOLD}=    Set Variable    ${3}
    Given the operator is signed off
    When the operator repeatedly enters incorrect credentials up to the configured lockout threshold    ${LOCKOUT_THRESHOLD}
    Then the Device Locked screen should be shown

Locked Device Unlocks With A Valid Supervisor Card
    [Documentation]    C4099923 (partial: needs a physical Supervisor smartcard fixture,
    ...    same as every other card-present case in this repo). GIVEN the Device Locked
    ...    screen, WHEN a valid Supervisor card is presented, THEN the device unlocks and
    ...    returns to the Sign On screen.
    [Tags]    testrailid=C4099923
    [Setup]    Skip    GAP: needs a physical Supervisor smartcard fixture (hardware, not software) -- no keyword in this repo can present a card over ADB alone. Depends on Device Locks After The Configured Number Of Failed Attempts for its starting state.
    Given the Device Locked screen should be shown
    When a supervisor presents a valid Supervisor card
    Then the ID and PIN fields should be shown
