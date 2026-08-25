*** Settings ***
Documentation    Device responds to a basic shell command over its configured transport.
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:common    feature:smoke

*** Variables ***
${DEVICE_TYPES}    POS,TVM,ETMS,HHD,GV,PV,BV

*** Test Cases ***
Device Responds To Echo
    [Tags]    device_types:POS    device_types:TVM    device_types:ETMS
    ...    device_types:HHD    device_types:GV    device_types:PV    device_types:BV
    ${result}=    Run On Device    echo hello-from-test
    Should Be True    ${result.ok}    echo failed: stderr=${result.stderr}
    Should Contain    ${result.stdout}    hello-from-test
