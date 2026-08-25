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

# ── C4099921 — Sign On, incorrect credentials ──────────────────────────────

the operator enters an unrecognised ID or PIN
    [Arguments]    ${timeout}=15.0
    # Deliberately not the seeded operator_id/operator_pin (300051 / 1234) --
    # any value that isn't the seeded pair is "unrecognised" per C4099921.
    ${ok}=    the operator signs on with credentials    000000    9999    timeout=${timeout}
    RETURN    ${ok}

the Sign On Failed screen should be shown with an attempt counter
    ${visible}=    Visible Texts
    # GAP: `SignOnFailed.attempts` (POSStrings) is the raw Xamarin template
    # "{Attempt} of {MaxAttempts}" -- the runtime-substituted text isn't a
    # static resource, so we can't do an exact string match without guessing
    # the current attempt number. Check the *shape* of the counter instead
    # (e.g. "1 of 3") rather than inventing an exact value.
    ${counter_seen}=    Evaluate
    ...    any(__import__('re').fullmatch(r'\\d+ of \\d+', t) for t in $visible)
    Should Be True    ${counter_seen}
    ...    msg=Expected an attempt-counter label matching 'N of M' on screen; visible texts: ${visible}

# ── C4099922 / C4099923 — lockout and Supervisor-card unlock ───────────────

the operator repeatedly enters incorrect credentials up to the configured lockout threshold
    [Arguments]    ${threshold}
    # GAP: the real TMS-configured lockout threshold for this environment is
    # not confirmed -- caller must pass it explicitly (see the test's own
    # [Setup] Skip until it's known; do not hard-code a guessed number here).
    FOR    ${i}    IN RANGE    ${threshold}
        the operator enters an unrecognised ID or PIN
    END

the Device Locked screen should be shown
    Assert Visible Labels    DeviceLocked.title    DeviceLocked.subtitle    screen=Device Locked

a supervisor presents a valid Supervisor card
    # GAP: no keyword in this repo can present a physical smartcard over ADB --
    # this needs a hardware card-reader fixture. Every caller of this keyword
    # must Skip before reaching it (see test_signon_lockout.robot); this stub
    # exists only so `robot --dryrun` resolves the keyword name, and fails
    # loudly rather than silently no-op'ing if it's ever actually reached.
    Fail    Not implemented: presenting a physical Supervisor card requires a hardware fixture, not available over ADB.

# ── C4099924 — Communication Locked ────────────────────────────────────────

the Communication Locked screen should be shown
    Assert Visible Labels    CommsLock.Title    CommsLock.Subtitle    screen=Communication Locked

comms with CloudFare have been down beyond the configured period
    # GAP: no keyword in this repo can force a sustained comms loss -- see
    # test_signon_communication_locked.robot's [Documentation]. Every caller
    # must Skip before reaching this; it fails loudly rather than no-op'ing.
    Fail    Not implemented: no mechanism exists in this repo to force sustained CloudFare comms loss.

the idle screen is viewed
    ${dummy}=    Visible Texts
    RETURN    ${dummy}

# ── C4099925 — Message / Word & Colour of the Day ──────────────────────────

the Message of the Day should be shown if available, or the Unavailable state otherwise
    ${available_title}=      Lookup POS String    SignonMessageOfTheDay.page_title
    ${unavailable_title}=    Lookup POS String    SignonMessageOfTheDayError.title
    ${seen}=    Wait For Any Text    ${available_title}    ${unavailable_title}    timeout=15
    Should Not Be Equal    ${seen}    ${None}
    ...    msg=Neither the Message of the Day screen nor its Unavailable state appeared
    RETURN    ${seen}

the Word and Colour of the Day should be shown if available, or the Unavailable state otherwise
    ${available_title}=      Lookup POS String    SignonWordAndColourOfTheDay.page_title
    ${unavailable_title}=    Lookup POS String    SignonWordAndColourOfTheDayError.title
    ${seen}=    Wait For Any Text    ${available_title}    ${unavailable_title}    timeout=15
    Should Not Be Equal    ${seen}    ${None}
    ...    msg=Neither the Word and Colour of the Day screen nor its Unavailable state appeared
    RETURN    ${seen}

# ── C4099912 — Sign On screen field entry and the 'C' key ──────────────────

the ID and PIN fields should be shown
    Assert Visible Labels    SignOn.id    SignOn.pin    screen=Sign On

the operator keys a digit into the active field
    [Arguments]    ${digit}
    Press Digits    ${digit}

the operator presses the 'C' key
    Press Clear Key

the field should show the digit just entered
    [Arguments]    ${expected}
    ${visible}=    Visible Texts
    List Should Contain Value    ${visible}    ${expected}
    ...    msg=Expected the active field to show '${expected}'; visible texts: ${visible}
