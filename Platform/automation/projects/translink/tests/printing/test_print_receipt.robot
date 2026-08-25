*** Settings ***
Documentation    Receipt printing — happy path and degraded states (low paper /
...              battery).
...
...              Strings:
...              - `Critical.button_print_receipt` ("Print Receipt")
...              - `BankCard.TransactionApproved.Print` ("Print Receipt")
...              - `Concession.printing` ("Printing Receipt")
...              - `Battery.low_title_printer` ("Printer Low Battery")
...              - `Battery.low_description_printer` (long warning text)
...
...              The printer is the `com.parkeon.periphs.pknUsbPrinter` daemon;
...              events about paper/battery surface via the EventLog.
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:printing

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Print Receipt Button Appears After Card Payment
    [Documentation]    The card-payment success screen offers 'Print Receipt'.
    Skip    Needs a completed card transaction precondition. Wire this when we have a deterministic transaction-seeding mechanism.

Low Paper Alarm Surfaces In Eventlog
    [Documentation]    Confirm the EventLog reports the low-paper alarm event type.
    ...
    ...    From the BSP-base dex scan we saw alarms-tree paths like
    ...    `/alarms/system/memory/data/almostFull` — there should be a parallel
    ...    `/alarms/printer/paper/low` (or similar) that emits an
    ...    `alarms.changed` EventLog row when crossed.
    ${el}=    Get Event Log
    ${rows}=    Call Method    ${el}    latest    alarms.changed    limit=${20}
    Skip If    not $rows    Device has emitted no alarms.changed events recently.
    # We don't yet know whether the paper alarm path appears in the payload
    # by exact name; this is a sniff-test to verify alarms surface at all.
    ${paper_related}=    Evaluate
    ...    [r for r in $rows if r.payload_json and any('paper' in str(v).lower() for v in r.payload_json.values())]
    Skip If    not $paper_related
    ...    No paper-related alarms in the most recent 20 alarms.changed rows. Test will only run meaningfully under a low-paper condition.
    # If we got here, at least one paper alarm fired — sanity-check the row
    ${row}=    Set Variable    ${paper_related}[0]
    ${event_type}=    Evaluate    $row.event_type
    Should Be Equal    ${event_type}    alarms.changed
    ${event_index}=    Evaluate    $row.event_index
    Should Not Be Equal    ${event_index}    ${None}
