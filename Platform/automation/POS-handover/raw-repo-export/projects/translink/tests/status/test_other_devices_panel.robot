*** Settings ***
Documentation    Other-devices panel -- fleet visibility from this POS.
...
...              Screen: `otherdeviceslayout.xml`. Static labels:
...              - `OtherDevicesStatus.Device` ("Device") -- column header
...              - `OtherDevicesStatus.Status` ("Status") -- column header
...
...              The body rows are populated programmatically (Xamarin-side) once
...              the POS queries the BOS for sibling devices in the same
...              `CommsGroupId`. We only assert the column headers render -- body
...              shape is a TODO for once we have a live device with a populated fleet.
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:status

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Other Devices Panel Renders Column Headers
    [Documentation]    Other-devices panel renders the Device/Status column headers.
    Start Activity    com.flowbird.pos
    # TODO: navigate into the other-devices panel. Likely entry: supervisor
    # menu -> "Other devices" or similar.
    Assert Visible Labels    OtherDevicesStatus.Device    OtherDevicesStatus.Status
    ...    screen=other-devices panel
