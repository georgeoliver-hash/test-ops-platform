*** Settings ***
Documentation    Sign On screen field entry and the 'C' key. TestRail C4099912, suite 30253,
...              Functional / Sign On & Session / Sign On.
Resource         ${CURDIR}/../../../../resources/translink/signon.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:auth

*** Test Cases ***
Sign On Screen Shows ID And PIN Fields And Keyed Digits Update Them
    [Documentation]    C4099912 (part 1). GIVEN the idle Sign On screen, WHEN the screen is
    ...    displayed, THEN the ID and PIN fields are shown; WHEN a digit is keyed in, THEN
    ...    the field updates to show it.
    [Tags]    testrailid=C4099912
    Given the operator is signed off
    Then the ID and PIN fields should be shown
    When the operator keys a digit into the active field    5
    Then the field should show the digit just entered    5

The 'C' Key Clears One Character Per Press
    [Documentation]    C4099912 (part 2). GIVEN a digit has been entered into a field, WHEN
    ...    the operator presses 'C', THEN exactly one character is cleared per press --
    ...    not the whole field.
    [Tags]    testrailid=C4099912
    Given the operator is signed off
    When the operator keys a digit into the active field    12
    Then the field should show the digit just entered    12
    When the operator presses the 'C' key
    Then the field should show the digit just entered    1
