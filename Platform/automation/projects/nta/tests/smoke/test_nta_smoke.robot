*** Settings ***
Documentation    NTA smoke tests -- auto-skip cleanly until ADB transport lands
...              on each device.
...
...              These hit the same scaffolding as the Translink smoke suite:
...              `Run On Device` will raise SkipExecution (via `Connect To
...              Device`) when the device's `transport.serial` is still 'TBD'
...              or the device is unreachable. So even today (no live NTA
...              hardware) this file collects cleanly and shows up as
...              `skipped` in the report rather than `failed`.
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Resolve Device
Test Setup       Skip Unless Device Has Serial
Test Teardown    NTA Test Teardown
Force Tags       project:nta    device_types:POS    device_types:BV    feature:smoke

*** Variables ***
${DEVICE_TYPES}    POS,BV

*** Keywords ***
Skip Unless Device Has Serial
    [Documentation]    Connects per-test (rather than once in Suite Setup) so
    ...    the NTA_DEVICE serial-not-yet-populated skip can happen before ever
    ...    touching the transport, matching the pytest `transport` fixture's
    ...    per-test skip behaviour.
    ${device}=    Get Connected Device
    ${serial}=    Evaluate    getattr($device.transport, 'serial', '')
    Skip If    '${serial}' == 'TBD'
    ...    NTA device ${device.id} has no serial yet -- populate devices.yaml
    Connect To Device

NTA Test Teardown
    Collect Test Artefacts
    Disconnect From Device

*** Test Cases ***
Device Responds To Echo
    [Documentation]    Most basic reachability check -- `echo` over the configured transport.
    ${result}=    Run On Device    echo hello-from-nta-test
    Should Be True    ${result.ok}    echo failed: stderr=${result.stderr}
    Should Contain    ${result.stdout}    hello-from-nta-test

Device Is Android
    [Documentation]    Confirm device reports an Android build (sanity for the Android shell layer).
    ${sdk}=    Getprop    ro.build.version.sdk
    ${is_digit}=    Evaluate    bool('${sdk}') and '${sdk}'.isdigit()
    Should Be True    ${is_digit}    Expected numeric SDK level from getprop, got '${sdk}'
