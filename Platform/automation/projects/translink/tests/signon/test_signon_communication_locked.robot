*** Settings ***
Documentation    Sign-on is blocked once the POS has lost CloudFare communication beyond the
...              configured period. TestRail C4099924, suite 30253, Functional /
...              Sign On & Session / Communication Locked.
Resource         ${CURDIR}/../../../../resources/translink/signon.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:auth

*** Test Cases ***
Communication Locked Screen Shown After Sustained Comms Loss
    [Documentation]    C4099924. GIVEN comms with CloudFare have been down beyond the
    ...    configured period, WHEN the idle screen is viewed, THEN the Communication
    ...    Locked screen is shown instead of Sign On.
    ...
    ...    GAP: no keyword in this repo can force a *sustained* CloudFare comms loss --
    ...    `AndroidShell` has no network/wifi/airplane-mode primitive, and `Configuration`'s
    ...    get/set is a key-value store with no confirmed path for this. (The same gap was
    ...    independently found on the SIT side of this work -- "Force Comms only forces a
    ...    reconnect, not a loss".) Confirm the mechanism before this can be automated.
    [Tags]    testrailid=C4099924
    [Setup]    Skip    GAP: no way to force sustained CloudFare comms loss exists in this repo today -- see [Documentation]
    Given comms with CloudFare have been down beyond the configured period
    When the idle screen is viewed
    Then the Communication Locked screen should be shown
