*** Settings ***
Documentation    Incorrect sign-on credentials: rejection message + attempt counter + retry.
...              TestRail C4099921 (suite 30253, Functional / Sign On & Session / Failures & Lockout).
Resource         ${CURDIR}/../../../../resources/translink/signon.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:auth

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Incorrect Credentials Show Sign On Failed With An Attempt Counter
    [Documentation]    C4099921. GIVEN the Sign On screen, WHEN the operator enters an
    ...    unrecognised ID or PIN, THEN a rejection message is shown with an attempt
    ...    counter (e.g. "1 of 3") and the operator can retry. The exact counter value
    ...    isn't asserted -- POSStrings' `SignOnFailed.attempts` is a runtime-substituted
    ...    template ("{Attempt} of {MaxAttempts}"), not a static resource, so this test
    ...    checks the counter's *shape* rather than inventing a specific number.
    [Tags]    testrailid=C4099921
    Given the operator is signed off
    ${ok}=    When the operator enters an unrecognised ID or PIN
    Should Be True    not $ok    sign_on() reported success for unrecognised credentials
    Then the Sign On Failed screen should be shown with an attempt counter
