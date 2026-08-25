*** Settings ***
Documentation    Live event-capture scaffold for ETM Tier-A automation candidates.
...
...              These pilot the ETM TestRail cases whose `THEN` is an auditable
...              side-effect we can read over SFTP (suite 30254 -- see
...              `docs/etm-automation-backlog.md`). The ETM is headless/shell-less,
...              so the operator performs each action *at the device* and the test
...              asserts the event lands in `DeviceEvents.json`.
...
...              Why "capture": the cached snapshot only carried 11 historical
...              events, so for sign-on/off, annul and smartcard taps we know the
...              *component* but not yet the exact `(Id, message)`. Each run
...              therefore dumps every new event since the baseline into the log --
...              so this session doubles as the way we learn the real codes. Once
...              observed, tighten `expect_components` / add an `expect_id` per
...              candidate and promote stable codes into `framework/wince/events.py`.
...
...              OPT-IN: skips unless `ETM_LIVE_ACTION=1` (waits for a human), so an
...              unattended suite never blocks.
...
...                  $env:PROJECT = "translink"
...                  $env:TRANSLINK_ETM_INF211_PASSWORD = "<etm root password>"
...                  $env:ETM_LIVE_ACTION = "1"
...                  # run one candidate at a time and perform its action when prompted:
...                  robot --variable PROJECT:translink -t "*sign_off*" projects/translink/tests/smoke/test_etm_live_event_capture.robot
...
...              Env knobs: ETM_ACTION_TIMEOUT (default 150s), ETM_VERSION_SLOT (default V6).
Resource         ${CURDIR}/../../../../resources/common.resource
Library          OperatingSystem
Library          framework.robot.wince_library.WinceLibrary
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:ETMS    feature:smoke

*** Variables ***
${DEVICE_TYPES}    ETMS

*** Test Cases ***
Action Emits Event
    [Template]    Verify Candidate Emits Event
    sign_off    Driver Sign Off    Sign the driver OFF (press P / sign-off) and let it return to the idle screen    ${EMPTY}
    sign_on    Driver Sign On — Manual, first use    Sign a driver ON: ID + PIN, through safety check / duty / route / journey to the FLU screen    ${EMPTY}
    annul    Ticket Issue — annul the last issued ticket    Issue a ticket, then annul the last issued ticket    TransactionService,TicketPrinter
    smartcard_tap    Smoke — smartcard validates on tap    Present a valid smartcard to the reader so it validates    SmartcardService
    abt_tap    Smoke — ABT contactless tap succeeds    Tap a valid contactless (ABT) card on the reader    SmartcardService,OpenPaymentService

*** Keywords ***
Verify Candidate Emits Event
    [Documentation]    One CANDIDATES row from the pytest version: (key, testrail_case,
    ...    action, expect_components as a comma-joined string, empty = "any new event").
    [Arguments]    ${key}    ${testrail_case}    ${action}    ${expect_components_csv}=${EMPTY}
    ${device_obj}=    Get Connected Device
    ${os_value}=    Evaluate    $device_obj.os.value
    Skip If    '${os_value}' != 'wince'    ETM-only (WinCE) capture

    ${live_action}=    Get Environment Variable    ETM_LIVE_ACTION    default=${EMPTY}
    Skip If    '${live_action}' != '1'    human-assisted; set ETM_LIVE_ACTION=1 to run

    ${slot}=    Get Environment Variable    ETM_VERSION_SLOT    default=V6
    ${timeout_str}=    Get Environment Variable    ETM_ACTION_TIMEOUT    default=150
    ${timeout}=    Convert To Number    ${timeout_str}

    ${components}=    Evaluate    [c.strip() for c in '''${expect_components_csv}'''.split(',') if c.strip()]

    Reload Device Events    version_slot=${slot}
    ${baseline}=    Latest Device Event
    ${epoch}=    Evaluate    __import__('datetime').datetime(1970, 1, 1, tzinfo=__import__('datetime').timezone.utc)
    ${baseline_dt}=    Set Variable If    $baseline is None or $baseline.event_date is None    ${epoch}    ${baseline.event_date}

    ${want}=    Set Variable If    ${components}    a new event of component ${components}    any new event
    Log    Expected: [${testrail_case}] after the action, ${want} appears in DeviceEvents.json
    Log    Baseline: newest EventDate=${baseline_dt}
    Log    >>> ACTION (${key}): ${action}. Waiting up to ${timeout} s for the event...

    ${fresh}=    Poll For New Event    ${slot}    ${baseline_dt}    ${components}    ${timeout}

    IF    $fresh
        Log New Events    ${fresh}
    END

    Should Not Be Empty    ${fresh}
    ...    msg=No new event appeared within ${timeout} s for '${key}'. Either the action wasn't performed, the events file didn't flush, or slot ${slot} is wrong.

    ${newest}=    Evaluate    max($fresh, key=lambda r: r.event_date)
    Log    Actual: Id=${newest.id} component=${newest.component_type} msg=${newest.message}
    IF    ${components}
        Should Contain    ${components}    ${newest.component_type}
    END

Poll For New Event
    [Documentation]    Re-pulls DeviceEvents.json every 5s until a matching new
    ...    event appears or `timeout` seconds elapse. Returns the (possibly
    ...    empty) list of matching fresh rows.
    [Arguments]    ${slot}    ${baseline_dt}    ${components}    ${timeout}
    ${deadline}=    Evaluate    __import__('time').monotonic() + float(${timeout})
    ${fresh}=    Create List
    WHILE    True
        Reload Device Events    version_slot=${slot}
        ${events}=    Device Events Since    ${baseline_dt}
        IF    ${components}
            ${matched}=    Evaluate    [r for r in $events if r.component_type in $components]
            IF    $matched
                ${fresh}=    Set Variable    ${matched}
                BREAK
            END
        ELSE
            IF    $events
                ${fresh}=    Set Variable    ${events}
                BREAK
            END
        END
        ${now}=    Evaluate    __import__('time').monotonic()
        IF    ${now} >= ${deadline}
            BREAK
        END
        Sleep    5s
    END
    RETURN    ${fresh}

Log New Events
    [Arguments]    ${events}
    ${sorted_events}=    Evaluate    sorted($events, key=lambda r: r.event_date)
    FOR    ${row}    IN    @{sorted_events}
        Log    New event captured: Id=${row.id} component=${row.component_type} state=${row.equipment_state} date=${row.event_date} msg=${row.message}
    END
