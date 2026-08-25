*** Settings ***
Documentation     Given/When/Then steps for POS on-screen checks (status panels, options
...               menu, FLU, clock). All of these route through
...               POS: Assert Screen Contains Labels, which currently raises "Not
...               Implemented" — see POSAndroidInteractionUtility.robot for why. Test files
...               using these steps are specified correctly and will run as far as this gap
...               and fail loudly there; that is intentional so the exact blocker is obvious.
Resource          ../Utility/POSInteractionUtility.robot

*** Keywords ***
the ${screen_name} screen should show the following labels
    [Arguments]    @{expected_labels}
    POS: Assert Screen Contains Labels    @{expected_labels}

the operator completes a test transaction
    POS: Complete Test Transaction

the ${key_name} key is pressed
    POS: Press Key    ${key_name}

a digit is keyed into the ${field_name} field
    [Documentation]    GAP: no confirmed keycode/input method for digit entry on this
    ...    hardware yet -- see Tests/POS/SignOn/test_signon_idle_screen.robot Documentation.
    Fail    Not Implemented — no confirmed digit-entry mechanism, see keyword Documentation

the ${field_name} field should show the keyed digit
    [Documentation]    GAP: depends on the Android UI-driving layer (reading field text) as
    ...    well as the digit-entry gap above.
    Fail    Not Implemented — depends on the generic Android UI-driving layer, see keyword Documentation

the ${field_name} field should be cleared by one character
    [Documentation]    GAP: depends on the Android UI-driving layer (reading field text) as
    ...    well as the digit-entry gap above.
    Fail    Not Implemented — depends on the generic Android UI-driving layer, see keyword Documentation
