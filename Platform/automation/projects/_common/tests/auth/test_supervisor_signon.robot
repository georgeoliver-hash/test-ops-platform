*** Settings ***
Documentation    Supervisor sign-on produces a BOS audit event.
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Start Device UI
Test Teardown    Common Auth Test Teardown
Force Tags       project:common    feature:auth

*** Variables ***
${DEVICE_TYPES}    POS,TVM,ETMS,HHD

*** Keywords ***
Common Auth Test Teardown
    Run Keyword And Ignore Error    Stop Device UI
    Collect Test Artefacts

*** Test Cases ***
Supervisor Signon Audited
    ${device}=    Get Connected Device
    ${ui}=        Get Device UI
    Call Method    ${ui}    login    supervisor    supervisor    password
    ${audit}=    Expect BOS Audit Event    SUPERVISOR_SIGN_ON    ${device.id}    within_seconds=30
    Should Be Equal    ${audit}[device_id]    ${device.id}
    Should Be Equal    ${audit}[event]    SUPERVISOR_SIGN_ON
