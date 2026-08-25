*** Settings ***
Documentation    Clock display tests.
...
...              ref: C4100373
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:display

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Clock Displays 24 Hour Time
    [Documentation]    The on-screen clock shows time in 24-hour HH:MM format.
    ...
    ...    ref: C4100373
    ${texts}=    Visible Texts
    ${time_texts}=    Evaluate
    ...    [t for t in $texts if re.match(r'^([01]\d|2[0-3]):[0-5]\d$', t)]
    ...    re
    Should Be True    ${time_texts}
    ...    No 24-hour time (HH:MM) visible on screen. Visible texts: ${texts}
