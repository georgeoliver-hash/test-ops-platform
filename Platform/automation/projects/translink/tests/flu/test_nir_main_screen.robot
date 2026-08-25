*** Settings ***
Documentation    NIR (Rail) fare look-up screen tests.
...
...              refs: C4099975
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:flu

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Nir Main Screen Is Rail Only
    [Documentation]    After sign-on in NIR mode the main screen shows rail
    ...    options only.
    ...
    ...    Bus and Day Tours buttons must not be present on the NIR main
    ...    screen.
    ...    ref: C4099975
    ${creds_id}=    Get Device Metadata Value    operator_id
    ${creds_pin}=    Get Device Metadata Value    operator_pin
    Skip If    not $creds_id or not $creds_pin
    ...    Operator credentials not seeded in devices.yaml metadata
    Ensure Signed Off
    ${signed_on}=    Sign On    ${creds_id}    ${creds_pin}    timeout=20.0
    Should Be True    ${signed_on}    Could not sign on with seeded credentials
    Sleep    1s
    ${seen}=    Visible Texts
    List Should Not Contain Value    ${seen}    Bus
    ...    msg='Bus' button found on NIR main screen — should not be present in rail mode. Visible: ${seen}
    List Should Not Contain Value    ${seen}    Day Tours
    ...    msg='Day Tours' button found on NIR main screen — should not be present in rail mode. Visible: ${seen}
