*** Settings ***
Documentation    Android device produces a non-empty PNG screenshot via screencap.
Library          OperatingSystem
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:common    feature:smoke

*** Variables ***
${DEVICE_TYPES}    POS,TVM,ETMS,HHD,PV,BV
${PNG_MAGIC}       ${{ b'\x89PNG\r\n\x1a\n' }}

*** Test Cases ***
Screencap Produces Png
    ${out}=    Set Variable    ${REPORT_DIR}/screen.png
    Take Screenshot    ${out}
    File Should Exist    ${out}    screenshot file not created
    ${data}=    Get Binary File    ${out}
    ${size}=    Get Length    ${data}
    Should Be True    ${size} > 1000    screenshot suspiciously small: ${size} bytes
    ${header}=    Evaluate    $data[:8]
    Should Be Equal    ${header}    ${PNG_MAGIC}    file is not a PNG
