*** Settings ***
Documentation    Live first-contact smoke tests for the Translink ETM (WinCE / SFTP-only).
...
...              Unlike the offline tests under `tests/provisioning/`, these exercise the
...              *real device*: they connect over SSH and SFTP-pull `DeviceEvents.json`
...              from the active version slot, then assert the framework can read it.
...              `Connect To Device` does the pull (over the transport's `pull`, never
...              `run()` -- the ETM has no shell). If the ETM is unreachable or creds
...              are wrong, `Connect To Device` raises SkipExecution (it never errors
...              the run). If the pull path is wrong for this device's active version
...              slot, the pull raises and the failure names the path we tried.
...
...              Run against the live device:
...                  $env:PROJECT = "translink"
...                  $env:TRANSLINK_ETM_INF211_PASSWORD = "<etm root password>"
...                  robot --variable PROJECT:translink projects/translink/tests/smoke/test_etm_live_connectivity.robot
Resource         ${CURDIR}/../../../../resources/common.resource
Library          framework.robot.wince_library.WinceLibrary
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:ETMS    feature:smoke

*** Variables ***
${DEVICE_TYPES}    ETMS

*** Test Cases ***
Etm Sftp Pull Returns Events
    [Documentation]    We can reach the ETM, SFTP-pull its SRSService event store,
    ...    and parse it to a non-empty set of rows.
    ${events}=    Get Device Events
    ${count}=    Get Length    ${events}
    Log    Expected: DeviceEvents.json pulled over SFTP, parses to >= 1 row
    Log    Actual: ${count} event rows pulled
    Should Be True    ${count} > 0    pulled DeviceEvents.json parsed to zero rows

Etm Live Rows Are Typed
    [Documentation]    Every pulled row exposes an integer event-id and a parseable
    ...    UTC date -- confirms the live file matches the schema our reader expects.
    ${events}=    Get Device Events
    FOR    ${row}    IN    @{events}
        Should Not Be Equal    ${row.id}    ${None}
        ...    msg=row has no integer Id: ${row}
        Should Not Be Equal    ${row.event_date}    ${None}
        ...    msg=unparseable EventDate on event ${row.id}
    END

Etm Latest Event Visible
    [Documentation]    Report the most-recent event so a live run leaves a
    ...    human-readable trace of what the device last logged.
    ${latest}=    Latest Device Event
    Should Not Be Equal    ${latest}    ${None}    msg=no datable events in the live store
    Log    Latest live event: Id=${latest.id} component=${latest.component_type} date=${latest.event_date} msg=${latest.message}
