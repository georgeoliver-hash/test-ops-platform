*** Settings ***
Documentation    Operator sign-on flow (PIN entry -> main menu) and the
...              InvalidLogin failure path. Each test resets to the sign-on
...              screen first so prior session state doesn't leak.
Resource         ${CURDIR}/../../../../resources/translink/signon.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:auth

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Signon Screen Shows Id And Pin Labels
    [Documentation]    Static check: the sign-on screen renders the expected labels.
    Given the operator is signed off
    Then the sign-on screen shows the ID and PIN labels

Invalid Signon Shows Failure Dialog
    [Documentation]    Wrong PIN -> 'Sign On Failed' dialog appears.
    ...    Marked `destructive`: repeated bad credentials trip a Fatal Error
    ...    lockout on the POS that needs a power cycle to clear. Excluded by
    ...    default; opt in with `--include destructive`.
    [Tags]    destructive
    Given the operator is signed off
    When the operator signs on with credentials    0000    9999    timeout=10.0
    Then sign on should fail with the invalid login dialog

Successful Signon Emits State Changed
    [Documentation]    Valid sign-on credentials produce a `state.changed` EventLog entry.
    ${operator_id}=    Get Device Metadata Value    operator_id
    ${operator_pin}=    Get Device Metadata Value    operator_pin
    Skip If    not $operator_id or not $operator_pin
    ...    Test operator credentials not seeded in devices.yaml metadata (operator_id, operator_pin).
    Given the operator is signed off
    ${baseline}=    Latest Event Index    state.changed
    ${baseline}=    Set Variable If    $baseline is None    ${0}    ${baseline}
    ${ok}=    the operator signs on with credentials    ${operator_id}    ${operator_pin}    timeout=20.0
    Should Be True    ${ok}    sign_on() reported the InvalidLogin dialog with seeded credentials
    Then a state.changed event should be emitted for the sign-on    ${baseline}
