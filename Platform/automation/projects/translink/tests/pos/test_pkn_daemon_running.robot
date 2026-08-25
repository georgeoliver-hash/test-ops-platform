*** Settings ***
Documentation    pkn_command_server daemon is running — without it the on-device
...              RPC channel is dead.
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:smoke

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Pkn Command Server Running
    [Documentation]    pkn_command_server daemon is running — without it the
    ...    on-device RPC channel is dead.
    ${running}=    Is Process Running    pkn_command_server
    Should Be True    ${running}    pkn_command_server is not running on the device
