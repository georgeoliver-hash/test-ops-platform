*** Settings ***
Documentation    com.flowbird.pos is installed on the POS at the build version
...              recorded in the registry.
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:smoke

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Flowbird Pos App Installed
    ${installed_pkg}=    Is Package Installed    com.flowbird.pos
    Should Be True    ${installed_pkg}    com.flowbird.pos is not installed on the device

    ${installed}=    Package Version    com.flowbird.pos
    ${expected}=    Get Device Build Version
    Skip If    not $expected or $expected == 'TBD'
    ...    No build.version pinned in registry for the device
    Should Not Be Equal    ${installed}    ${None}    could not read versionName from dumpsys
    Should Contain    ${installed}    ${expected}
    ...    msg=installed versionName=${installed} does not contain registry version=${expected}
