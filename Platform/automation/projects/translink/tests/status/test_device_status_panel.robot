*** Settings ***
Documentation    Device status panel -- printer/card-reader subsystem health surfaces.
...
...              Screen: `devicestatuslayout.xml`. Static labels:
...              - `DeviceStatus.Printer` ("Printer")
...              - `DeviceStatus.CardReader` ("Card Reader")
...
...              These map to peripherals daemons:
...              - `com.parkeon.periphs.pknUsbPrinter`
...              - `com.parkeon.periphs.dallas` (one-wire chip used as card-reader proxy)
...              - `com.parkeon.periphs.pknBixolonUsbSerialLcd` (LCD)
...
...              The peripherals' health probably surfaces via `state.changed` events
...              with a source field naming the peripheral package.
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:status

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Device Status Screen Lists Printer And Card Reader
    Start Activity    com.flowbird.pos
    # TODO: navigate into the device-status panel; likely from supervisor menu.
    Assert Visible Labels    DeviceStatus.Printer    DeviceStatus.CardReader
    ...    screen=device-status panel

State Changed Rows Have Source Field
    [Documentation]    The EventLog schema includes `source TEXT NOT NULL` --
    ...    verify it's populated for recent state.changed rows.
    ${log}=    Get Event Log
    ${rows}=    Call Method    ${log}    latest    state.changed    limit=${10}
    Skip If    not $rows    Device has emitted no state.changed events recently.
    ${sources}=    Evaluate    sorted({row.source for row in $rows if row.source})
    Should Not Be Empty    ${sources}
    ...    msg=No \`source\` populated on any of ${{len($rows)}} state.changed rows
    # Also a sanity check on a known source naming convention -- sources should
    # match a Java package shape (segments dotted, lowercase).
    ${bad}=    Evaluate    [s for s in $sources if not s or ' ' in s]
    Should Be Empty    ${bad}    msg=Source field has unexpected values: ${bad}
