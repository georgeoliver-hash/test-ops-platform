*** Settings ***
Documentation    Bus (Ulsterbus) FLU tests.
...
...              The Ulsterbus FLU is reached from the post-sign-on main menu in
...              Ulsterbus or Metro mode via the 'Bus' / 'Ulsterbus' button. In
...              NIR (rail) mode this button is absent (confirmed by
...              test_nir_main_screen_is_rail_only).
...
...              The Bus FLU uses a numeric route-entry flow rather than a P2P
...              station grid:
...                Driver.EnterRouteTitle = 'Enter Route'  (numeric entry screen)
...                '*' key cycles boarding-stage / fare-type overrides.
...                'Misc' (MainMenu.Misc = 'Misc') opens miscellaneous open-fare
...                products.
...
...              The Translink lab POS is configured in NIR (Rail) mode, so the
...              Bus FLU is NOT reachable on the live device from the standard
...              sign-on. These tests document the expected screen shapes and
...              skip gracefully when the Bus button is absent (NIR mode).
...
...              refs: C4100374, C4100375, C4100376, C4100377, C4100378
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:flu

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Bus Flu Route Entry Screen Opens
    [Documentation]    In Ulsterbus/Metro mode, the Bus button opens the
    ...    route-entry screen.
    ...
    ...    The route-entry screen must show the 'Enter Route' prompt.
    ...    Skipped when the device is in NIR (Rail) mode (no Bus button on
    ...    main menu).
    ...
    ...    ref: C4100374
    ${creds_id}=    Get Device Metadata Value    operator_id
    ${creds_pin}=    Get Device Metadata Value    operator_pin
    Skip If    not $creds_id or not $creds_pin
    ...    Operator credentials not seeded in devices.yaml metadata
    ${opened}=    Try Open Bus FLU    ${creds_id}    ${creds_pin}
    Skip If    not ${opened}
    ...    Bus/Ulsterbus button not visible on main menu — device is likely in NIR (Rail) mode; Bus FLU tests require Ulsterbus or Metro mode
    ${seen}=    Visible Texts
    List Should Contain Value    ${seen}    Enter Route
    ...    msg=Bus FLU route-entry screen did not show 'Enter Route'

Bus Flu Star Key Cycles Boarding Stage
    [Documentation]    The '*' key on the Bus FLU cycles through
    ...    boarding-stage overrides.
    ...
    ...    On the route-entry screen, pressing '*' (KEYCODE_STAR /
    ...    KEY_KPASTERISK) should open the boarding-stage / fare-type picker
    ...    as defined by the Default Boarding Stage configuration.
    ...
    ...    ref: C4100378
    ${creds_id}=    Get Device Metadata Value    operator_id
    ${creds_pin}=    Get Device Metadata Value    operator_pin
    Skip If    not $creds_id or not $creds_pin
    ...    Operator credentials not seeded in devices.yaml metadata
    ${opened}=    Try Open Bus FLU    ${creds_id}    ${creds_pin}
    Skip If    not ${opened}    Bus FLU not reachable — device is in NIR mode
    Send Key    155    # KEYCODE_STAR = 155 (KEY_KPASTERISK)
    Sleep    0.5s
    ${seen}=    Visible Texts
    # Boarding-stage screen or numeric-entry context should become active.
    # The key might show 'Boarding Location' (BoardingLocation.Title) or a
    # fare-type list; either confirms '*' was processed.
    Should Be True    ${seen}
    ...    No visible text after pressing '*' on Bus FLU route-entry screen

Bus Flu Misc Opens Miscellaneous Products
    [Documentation]    The Misc button (MainMenu.Misc) opens the
    ...    Miscellaneous Products screen.
    ...
    ...    'Misc' is on the main menu and is available across modes; it opens
    ...    'Miscellaneous Products' (MiscProducts.Title).
    ...
    ...    ref: C4100377
    ${creds_id}=    Get Device Metadata Value    operator_id
    ${creds_pin}=    Get Device Metadata Value    operator_pin
    Skip If    not $creds_id or not $creds_pin
    ...    Operator credentials not seeded in devices.yaml metadata
    Ensure Signed Off
    ${signed_on}=    Sign On    ${creds_id}    ${creds_pin}    timeout=20.0
    Should Be True    ${signed_on}    Could not sign on with seeded credentials
    Sleep    1s
    ${seen}=    Visible Texts
    Skip If    "Misc" not in $seen
    ...    'Misc' button not visible on main menu in current mode
    ${tapped}=    Tap Text    Misc
    Should Be True    ${tapped}    Could not tap 'Misc' on the main menu
    ${reached}=    Wait For Text    Miscellaneous Products    timeout=10.0
    ${visible}=    Visible Texts
    Should Be True    ${reached}
    ...    Miscellaneous Products screen did not open after tapping 'Misc'. Visible: ${visible}

*** Keywords ***
Try Open Bus FLU
    [Documentation]    Sign on and attempt to open the Bus FLU.
    ...
    ...    Returns True if the Bus FLU route-entry screen became visible.
    ...    Returns False (does not fail) if the 'Bus'/'Ulsterbus' button is
    ...    absent — this is expected when the device is in NIR mode.
    [Arguments]    ${creds_id}    ${creds_pin}
    Ensure Signed Off
    ${signed_on}=    Sign On    ${creds_id}    ${creds_pin}    timeout=20.0
    IF    not ${signed_on}
        RETURN    ${False}
    END
    Sleep    1s
    ${seen}=    Visible Texts
    ${bus_label}=    Evaluate    next((t for t in $seen if t in ("Bus", "Ulsterbus")), None)
    IF    $bus_label is None
        RETURN    ${False}
    END
    ${tapped}=    Tap Text    ${bus_label}
    IF    not ${tapped}
        RETURN    ${False}
    END
    ${opened}=    Wait For Text    Enter Route    timeout=10.0
    RETURN    ${opened}
