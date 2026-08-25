*** Settings ***
Documentation    EventLog content provider responds and reports recent
...              state-change events.
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:audit

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Eventlog Has Recent State Changes
    [Documentation]    EventLog returns rows for state.changed with an eventIndex.
    ${el}=    Get Event Log
    ${rows}=    Call Method    ${el}    latest    state.changed    limit=${5}
    Should Be True    ${rows}
    ...    EventLog returned no rows for state.changed — provider may be unreachable
    ${any_index}=    Evaluate    any(row.event_index is not None for row in $rows)
    Should Be True    ${any_index}
    ...    No row in ${rows} carries an eventIndex; column schema may have changed

Eventlog Indices Are Monotonic
    [Documentation]    EventLog rows sort=eventIndex DESC come back monotonically descending.
    ${el}=    Get Event Log
    ${rows}=    Call Method    ${el}    latest    state.changed    limit=${10}
    ${count}=    Get Length    ${rows}
    Skip If    ${count} < 2    Not enough state.changed rows to check monotonicity
    ${indices}=    Evaluate    [row.event_index for row in $rows if row.event_index is not None]
    ${sorted_desc}=    Evaluate    sorted($indices, reverse=True)
    Should Be Equal    ${indices}    ${sorted_desc}
    ...    msg=EventLog indices not monotonically descending under sort=eventIndex DESC: ${indices}
