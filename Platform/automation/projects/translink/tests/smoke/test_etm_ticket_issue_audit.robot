*** Settings ***
Documentation    Live, human-assisted ETM smoke: issuing a ticket emits a printer event.
...
...              Pilots the TestRail case "Smoke -- sign on, issue a ticket and sign off"
...              (suite 30254) -- specifically the `THEN the ticket is printed` outcome.
...
...              The ETM is headless and shell-less (SFTP only), so we cannot *drive* it;
...              we verify the auditable side-effect. The operator issues a ticket on
...              the device by hand, and this test confirms a fresh `TicketPrinter`
...              event appears in `DeviceEvents.json` (Id 102 "Print started" / 110
...              "Printer OK"), newer than the pre-action baseline. This is the
...              verification half of an end-to-end case -- the half automation can
...              own for a device with no automatable UI.
...
...              Because it waits for a human action, it is OPT-IN: it skips unless
...              `ETM_LIVE_ACTION=1` is set, so an unattended suite run never blocks on it.
...
...              Run it (issue a ticket on the ETM when prompted):
...                  $env:PROJECT = "translink"
...                  $env:TRANSLINK_ETM_INF211_PASSWORD = "<etm root password>"
...                  $env:ETM_LIVE_ACTION = "1"
...                  robot --variable PROJECT:translink projects/translink/tests/smoke/test_etm_ticket_issue_audit.robot
...
...              Env knobs:
...                ETM_ACTION_TIMEOUT  seconds to wait for the action (default 150)
...                ETM_VERSION_SLOT    active GFTS version slot for the events file (default V6)
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
Ticket Issue Emits Printer Event
    ${device_obj}=    Get Connected Device
    ${os_value}=    Evaluate    $device_obj.os.value
    Skip If    '${os_value}' != 'wince'    ETM-only (WinCE) smoke

    ${live_action}=    Get Environment Variable    ETM_LIVE_ACTION    default=${EMPTY}
    Skip If    '${live_action}' != '1'    human-assisted; set ETM_LIVE_ACTION=1 to run

    ${slot}=    Get Environment Variable    ETM_VERSION_SLOT    default=V6
    ${timeout_str}=    Get Environment Variable    ETM_ACTION_TIMEOUT    default=150
    ${timeout}=    Convert To Number    ${timeout_str}

    # Baseline on EventDate -- Id is an event-TYPE code, not a row index, so a
    # new event is identified by being newer than everything already present.
    Reload Device Events    version_slot=${slot}
    ${baseline}=    Latest Device Event
    ${epoch}=    Evaluate    __import__('datetime').datetime(1970, 1, 1, tzinfo=__import__('datetime').timezone.utc)
    ${baseline_dt}=    Set Variable If    $baseline is None or $baseline.event_date is None    ${epoch}    ${baseline.event_date}

    Log    Expected: A TicketPrinter event newer than the baseline appears in DeviceEvents.json after a ticket is issued on the ETM
    Log    Baseline: newest EventDate=${baseline_dt}
    Log    >>> ACTION REQUIRED: issue/print a ticket on the ETM now. Waiting up to ${timeout} s for the printer event...

    ${new_printer}=    Poll For New Printer Event    ${slot}    ${baseline_dt}    ${timeout}

    IF    $new_printer is None
        Log    Actual: No new TicketPrinter event observed within the window
        Fail    No TicketPrinter event newer than ${baseline_dt} appeared within ${timeout} s. Either no ticket was issued, or the events file in slot ${slot} did not flush in time.
    END

    Log    Actual: TicketPrinter event Id=${new_printer.id} at ${new_printer.event_date} state=${new_printer.equipment_state} msg=${new_printer.message}
    Log    Observed printer event: ${new_printer}
    Should Be True    $new_printer.event_date > $baseline_dt

*** Keywords ***
Poll For New Printer Event
    [Documentation]    Re-pulls DeviceEvents.json every 5s, filtering to TicketPrinter
    ...    rows newer than the baseline, until one appears or `timeout` elapses.
    [Arguments]    ${slot}    ${baseline_dt}    ${timeout}
    ${deadline}=    Evaluate    __import__('time').monotonic() + float(${timeout})
    ${new_printer}=    Set Variable    ${None}
    WHILE    True
        Reload Device Events    version_slot=${slot}
        ${events}=    Device Events Since    ${baseline_dt}
        ${fresh}=    Evaluate    [r for r in $events if r.component_type == 'TicketPrinter']
        IF    $fresh
            ${new_printer}=    Evaluate    max($fresh, key=lambda r: r.event_date)
            BREAK
        END
        ${now}=    Evaluate    __import__('time').monotonic()
        IF    ${now} >= ${deadline}
            BREAK
        END
        Sleep    5s
    END
    RETURN    ${new_printer}
