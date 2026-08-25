*** Settings ***
Documentation    Offline verification of the ETM SRSService event store + its
...              reader.
...
...              These run against the cached `builds/etm/` V6 snapshot (the
...              active version slot per the GFTS log), so they need no live
...              device. They cover two things:
...
...              * the `DeviceEvents` reader correctly parses real device data —
...              every row yields a typed event-id and a parseable Microsoft
...              `/Date(ms)/` timestamp;
...              * the events store and its `EventsConfig.json` catalogue are
...              consistent enough to test against.
...
...              Note we deliberately do NOT assert that every stored event-id
...              is in the `EnabledEvents` catalogue: the store is historical
...              and legitimately retains events recorded under earlier
...              configurations (e.g. 812, 40041, 40042 in the current
...              snapshot). We assert a non-empty *overlap* instead.
Library          Collections
Library          framework.robot.wince_library.WinceLibrary

*** Test Cases ***
Device Events Snapshot Is Non Empty
    [Tags]    feature:smoke
    ${events}=    the cached ETM events snapshot
    ${length}=    Get Length    ${events}
    Should Be True    ${length} > 0    cached DeviceEvents.json parsed to zero rows

Every Row Has Typed Id And Parseable Date
    [Documentation]    Reader correctness against real data: every row exposes
    ...    an int event-id and a parseable UTC EventDate.
    [Tags]    feature:smoke
    ${events}=    the cached ETM events snapshot
    ${rows}=    Call Method    ${events}    all
    FOR    ${row}    IN    @{rows}
        ${id}=    Evaluate    $row.id
        Should Not Be Equal    ${id}    ${None}    row has no integer Id
        ${event_date}=    Evaluate    $row.event_date
        Should Not Be Equal    ${event_date}    ${None}    unparseable EventDate on row
        ${tzinfo}=    Evaluate    $row.event_date.tzinfo
        Should Not Be Equal    ${tzinfo}    ${None}    EventDate must be timezone-aware (UTC)
    END

Latest Event Is Most Recent By Date
    [Documentation]    `latest()` returns the row with the maximum EventDate.
    [Tags]    feature:smoke
    ${events}=    the cached ETM events snapshot
    ${latest}=    Call Method    ${events}    latest
    Should Not Be Equal    ${latest}    ${None}
    ${rows}=    Call Method    ${events}    all
    ${newest}=    Evaluate    max([r.event_date for r in $rows if r.event_date])
    ${latest_date}=    Evaluate    $latest.event_date
    Should Be Equal    ${latest_date}    ${newest}

Component Filter Subsets The Store
    [Tags]    feature:smoke
    ${events}=    the cached ETM events snapshot
    ${printer}=    Call Method    ${events}    by_component    TicketPrinter
    Should Not Be Empty    ${printer}    expected at least one TicketPrinter event in the snapshot
    FOR    ${row}    IN    @{printer}
        ${component_type}=    Evaluate    $row.component_type
        Should Be Equal    ${component_type}    TicketPrinter
    END

Enabled Events Catalogue Overlaps Store
    [Documentation]    EventsConfig parses, is non-empty, and shares at least
    ...    one event-type with what the device has actually recorded.
    [Tags]    feature:smoke
    ${events}=    the cached ETM events snapshot
    ${config_path}=    Get Default ETM Events Config Path
    ${enabled}=    Load Enabled Events From File    ${config_path}
    Should Not Be Empty    ${enabled}    EventsConfig.json EnabledEvents is empty
    ${event_ids}=    Call Method    ${events}    event_ids
    ${overlap}=    Evaluate    set($event_ids) & set($enabled)
    Should Not Be Empty    ${overlap}    no overlap between recorded event-ids and the EnabledEvents catalogue

Parse Ms Date Handles Offsets
    [Template]    Assert Parse Ms Date Equals
    /Date(1780325744000)/    1780325744000
    /Date(1780325744000+0000)/    1780325744000
    /Date(0)/    0

Parse Ms Date Rejects Non Ms Format
    [Template]    Assert Parse Ms Date Returns None
    ${None}
    ${EMPTY}
    not-a-date
    2026-06-01T00:00:00Z

*** Keywords ***
the cached ETM events snapshot
    ${path}=    Get Default ETM Events Snapshot Path
    ${events}=    Load Device Events From File    ${path}
    RETURN    ${events}

Assert Parse Ms Date Equals
    [Arguments]    ${raw}    ${expected_ms}
    ${dt}=    Parse MS Date    ${raw}
    Should Not Be Equal    ${dt}    ${None}
    ${ms}=    Evaluate    int($dt.timestamp() * 1000)
    Should Be Equal As Integers    ${ms}    ${expected_ms}
    ${tzinfo}=    Evaluate    $dt.tzinfo
    Should Not Be Equal    ${tzinfo}    ${None}

Assert Parse Ms Date Returns None
    [Arguments]    ${raw}
    ${dt}=    Parse MS Date    ${raw}
    Should Be Equal    ${dt}    ${None}
