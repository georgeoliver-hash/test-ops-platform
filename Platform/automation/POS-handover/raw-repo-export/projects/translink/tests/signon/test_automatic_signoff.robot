*** Settings ***
Documentation    Automatic sign-off after inactivity timeout.
...
...              The DatasetParameters value `automaticLogOff` specifies the
...              idle timeout in milliseconds before the POS automatically
...              signs the operator off. For the Translink build this is
...              10000 ms (10 seconds).
...
...              ref: C4099933
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:auth

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Automatic Signoff After Inactivity
    [Documentation]    POS automatically signs off after the configured
    ...    inactivity timeout.
    ...
    ...    Steps:
    ...    1. Sign on.
    ...    2. Wait for `automaticLogOff` ms (+ a 5 s safety margin) without input.
    ...    3. Assert the device returns to the idle/sign-on screen.
    ...
    ...    ref: C4099933
    ${creds_id}=    Get Device Metadata Value    operator_id
    ${creds_pin}=    Get Device Metadata Value    operator_pin
    Skip If    not $creds_id or not $creds_pin
    ...    Operator credentials not seeded in devices.yaml metadata

    ${params}=    Get Dataset Parameters
    ${timeout_ms_str}=    Get From Dictionary    ${params}    automaticLogOff    default=${EMPTY}
    Skip If    not $timeout_ms_str
    ...    automaticLogOff not found in DatasetParameters — cannot determine wait time

    ${conv_status}    ${timeout_ms}=    Run Keyword And Ignore Error
    ...    Convert To Integer    ${timeout_ms_str}
    Skip If    '${conv_status}' == 'FAIL'
    ...    automaticLogOff value ${timeout_ms_str} is not an integer

    Skip If    ${timeout_ms} > 120000
    ...    automaticLogOff is ${timeout_ms} ms (>120s) — too long for an automated test

    ${wait_seconds}=    Evaluate    (${timeout_ms} / 1000.0) + 5.0

    Ensure Signed Off
    ${signed_on}=    Sign On    ${creds_id}    ${creds_pin}    timeout=20.0
    Should Be True    ${signed_on}    Could not sign on with seeded credentials

    # Idle — no UI interaction for the full timeout period.
    Sleep    ${wait_seconds}s

    ${returned}=    Wait For Any Text    Press Any Key to Continue    Present card    Sign On
    ...    timeout=10.0
    ${visible}=    Visible Texts
    Should Be True    ${returned}
    ...    POS did not auto-sign-off after ${wait_seconds}s idle (automaticLogOff=${timeout_ms} ms). Visible: ${visible}
