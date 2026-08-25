*** Settings ***
Documentation    Message of the Day and Word & Colour of the Day during sign-on, each with an
...              Unavailable fallback that still lets sign-on continue. TestRail C4099925,
...              suite 30253, Functional / Sign On & Session / Sign-on Messages.
Resource         ${CURDIR}/../../../../resources/translink/signon.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:auth

*** Test Cases ***
Message And Word And Colour Of The Day Shown Or Gracefully Unavailable During Sign On
    [Documentation]    C4099925. GIVEN a valid sign-on, WHEN the Message of the Day and
    ...    Word & Colour of the Day are checked, THEN each is either shown or its
    ...    Unavailable state is shown -- either way sign-on continues.
    ...
    ...    This test asserts "one of the two known states appeared", not which one --
    ...    which branch appears depends on live CloudFare content at the time of the
    ...    run, not something this test can or should force.
    [Tags]    testrailid=C4099925
    Given the operator is signed off
    ${operator_id}=    Get Device Metadata Value    operator_id
    ${operator_pin}=    Get Device Metadata Value    operator_pin
    Skip If    not $operator_id or not $operator_pin
    ...    Test operator credentials not seeded in devices.yaml metadata (operator_id, operator_pin).
    When the operator signs on with credentials    ${operator_id}    ${operator_pin}    timeout=20.0
    Then the Message of the Day should be shown if available, or the Unavailable state otherwise
    And the Word and Colour of the Day should be shown if available, or the Unavailable state otherwise
