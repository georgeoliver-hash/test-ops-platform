*** Settings ***
Documentation    Smoke test for BOS/ABT/CloudFare/Merit back-office web portals.
...
...              Infrastructure scaffold only, for the export-automation backlog
...              (217 full + 136 partial automatable cases in the sibling
...              system-test-ops repo) to have somewhere to eventually run. No
...              live portal URL or credentials exist yet -- see
...              projects/bos/devices.yaml. Until George supplies the real
...              web_ui_url (or exports BOS_PORTAL_URL) and
...              BOS_PORTAL_USERNAME/BOS_PORTAL_PASSWORD, `Start Device UI`
...              raises SkipExecution and this test skips gracefully rather
...              than failing.
Resource         ${CURDIR}/../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Start Device UI
Test Teardown    Portal Test Teardown
Force Tags       project:bos    device_types:PORTAL    feature:smoke

*** Variables ***
${DEVICE_TYPES}    PORTAL

*** Keywords ***
Portal Test Teardown
    Run Keyword And Ignore Error    Stop Device UI
    Collect Test Artefacts

*** Test Cases ***
Portal Reachable
    [Documentation]    The portal loads and reports a non-empty title or URL.
    ${ui}=          Get Device UI
    ${title}=       Call Method    ${ui}    title
    ${url}=         Call Method    ${ui}    current_url
    ${screenshot}=  Set Variable    ${REPORT_DIR}/portal_landing.png
    Call Method     ${ui}    screenshot    ${screenshot}
    ${has_title_or_url}=    Evaluate    bool($title) or bool($url)
    Should Be True    ${has_title_or_url}
    ...    Portal page loaded but reported neither a title nor a URL
