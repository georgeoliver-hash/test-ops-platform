*** Comments ***
# Domain-level Given/When/Then keywords for the Translink POS sign-on flow.
# RF strips Given/When/And/But/Then automatically before keyword lookup, so
# these are defined by their bare name and used with any BDD prefix from a
# test case's steps.

*** Settings ***
Resource    ${CURDIR}/../common.resource

*** Keywords ***
the operator is signed off
    Ensure Signed Off

the sign-on screen shows the ID and PIN labels
    ${id_label}=      Lookup POS String    SignOn.id
    ${shown}=         Wait For Text    ${id_label}    timeout=5
    Should Be True    ${shown}    Sign-on screen never showed the 'ID' label
    ${pin_label}=      Lookup POS String    SignOn.pin
    ${visible}=        Visible Texts
    List Should Contain Value    ${visible}    ${pin_label}
    ...    msg=Sign-on screen missing the 'PIN' label

the operator signs on with credentials
    [Arguments]    ${operator_id}    ${pin}    ${timeout}=15.0
    ${ok}=    Sign On    ${operator_id}    ${pin}    timeout=${timeout}
    RETURN    ${ok}

sign on should fail with the invalid login dialog
    ${label}=      Lookup POS String    InvalidLogin.title
    ${visible}=    Visible Texts
    List Should Contain Value    ${visible}    ${label}
    ...    msg=Expected 'Sign On Failed' dialog after bad signon

a state.changed event should be emitted for the sign-on
    [Arguments]    ${baseline}
    # FALSE-PASS RISK (carried over from the pytest suite, flagged by
    # log-intelligence on run 2026-05-21_08-35-16): the device emits a
    # `state.changed` from com.parkeon.systemstate roughly every 30s as a side
    # effect of NTP clock sync, which also carries a non-empty payload, so
    # `require_payload=True` alone can pass without a genuine sign-on.
    # TODO(live-adb-window): tighten to the operator/session node once a real
    # sign-on payload is captured.
    ${row}=    Wait For Event    state.changed    baseline_index=${baseline}
    ...    within_seconds=15    require_payload=${True}
    Should Be Equal    ${row.event_type}    state.changed
