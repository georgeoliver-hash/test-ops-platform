*** Settings ***
Documentation    Capture an EventLog baseline so a downstream test can wait
...              for new events.
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:audit

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
State Changed Arrives Within 60s
    [Documentation]    The platform emits state.changed events at least once
    ...    per minute under normal idle (NTP, network watchdogs). If we don't
    ...    see a new one in 60s, something is wrong with the platform's event
    ...    pipeline.
    ${baseline}=    Latest Event Index    state.changed
    ${baseline}=    Set Variable If    $baseline is None    ${0}    ${baseline}
    ${start}=    Evaluate    time.monotonic()    time
    ${row}=    Wait For Event    state.changed    baseline_index=${baseline}
    ...    within_seconds=60
    ${elapsed}=    Evaluate    time.monotonic() - ${start}    time
    Should Be True    $row.event_index is not None and $row.event_index > $baseline
    ...    wait_for returned a row but its eventIndex (${row.event_index}) is not > baseline (${baseline})
    Should Be True    ${elapsed} < 60
