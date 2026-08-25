*** Settings ***
Documentation    Operator sign-off tests.
...
...              refs: C4100370, C4099929
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:auth

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Signoff Returns To Idle Screen
    [Documentation]    After sign-off the POS returns to the idle/sign-on screen.
    ...
    ...    ref: C4100370
    ${creds_id}=    Get Device Metadata Value    operator_id
    ${creds_pin}=    Get Device Metadata Value    operator_pin
    Skip If    not $creds_id or not $creds_pin
    ...    Operator credentials not seeded in devices.yaml metadata

    Ensure Signed Off
    ${signed_on}=    Sign On    ${creds_id}    ${creds_pin}    timeout=20.0
    Should Be True    ${signed_on}    Could not sign on with seeded credentials

    ${signed_off}=    Sign Off
    Should Be True    ${signed_off}    sign_off() could not find the Sign Off button

    ${returned}=    Wait For Any Text    Press Any Key to Continue    Present card    Sign On
    ...    timeout=15.0
    Should Be True    ${returned}    POS did not return to idle/sign-on screen after sign-off

Signoff Emits State Changed Event
    [Documentation]    Sign-off produces a state.changed EventLog entry.
    ...
    ...    ref: C4099929
    ${creds_id}=    Get Device Metadata Value    operator_id
    ${creds_pin}=    Get Device Metadata Value    operator_pin
    Skip If    not $creds_id or not $creds_pin
    ...    Operator credentials not seeded in devices.yaml metadata

    Ensure Signed Off
    ${signed_on}=    Sign On    ${creds_id}    ${creds_pin}    timeout=20.0
    Should Be True    ${signed_on}    Could not sign on with seeded credentials

    ${baseline}=    Latest Event Index    state.changed
    ${baseline}=    Set Variable If    $baseline is None    ${0}    ${baseline}
    ${signed_off}=    Sign Off
    Should Be True    ${signed_off}    sign_off() could not find the Sign Off button

    ${event}=    Wait For Event    state.changed    baseline_index=${baseline}    within_seconds=30
    Should Not Be Equal    ${event}    ${None}
    ...    No state.changed event emitted after sign-off (baseline_index=${baseline})
