*** Settings ***
Documentation     Nexio hardware-tap sign-on BDD step keywords.
...               These steps drive the physical QML sign-on screen via evdev touch injection.
...               Coordinate variables (${KEYPAD_COORDS}, ${SIGNON_WAKE_X}, etc.) are
...               defined in Resources/Devices/Nexio/Variables/NexioVariables.robot.

Library     String

*** Keywords ***
evdev is installed and available on the device
    ${result}=    Nexio Run Command    python3 -c "import evdev; print('OK')"
    Should Contain    ${result}    OK
    ...    msg=evdev not found on device. Install with: ssh root@<device_ip> pip3 install evdev

the ${actor} sends a hardware tap to wake the screen
    Hardware Tap    ${SIGNON_WAKE_X}    ${SIGNON_WAKE_Y}
    Sleep    0.5s

the device screen is active and the sign-on keypad is showing
    Log    Screen wake tap delivered — sign-on keypad should be visible on device    console=True

the sign-on keypad is showing
    Sleep    0.2s

the ${actor} enters user ID "${user_id}" digit by digit on the hardware keypad
    ${uid_str}=    Convert To String    ${user_id}
    ${digits}=     Split String To Characters    ${uid_str}
    FOR    ${digit}    IN    @{digits}
        ${coords}=    Get From Dictionary    ${KEYPAD_COORDS}    ${digit}
        ${xy}=        Split String    ${coords}    ,
        Hardware Tap    ${xy}[0]    ${xy}[1]
        Sleep    0.15s
    END

the ${actor} taps Next to advance to PIN entry
    Hardware Tap    ${SIGNON_NEXT_X}    ${SIGNON_NEXT_Y}
    Sleep    0.5s

the PIN entry screen is ready
    Sleep    0.3s

the ${actor} enters PIN "${pin}" digit by digit on the hardware keypad
    ${pin_str}=    Convert To String    ${pin}
    ${digits}=     Split String To Characters    ${pin_str}
    FOR    ${digit}    IN    @{digits}
        ${coords}=    Get From Dictionary    ${KEYPAD_COORDS}    ${digit}
        ${xy}=        Split String    ${coords}    ,
        Hardware Tap    ${xy}[0]    ${xy}[1]
        Sleep    0.15s
    END

the ${actor} taps Sign On to submit credentials
    Hardware Tap    ${SIGNON_SUBMIT_X}    ${SIGNON_SUBMIT_Y}

the driver console application loads and the duty screen is shown
    Connect Nexio CDP Tab
    Wait Until Keyword Succeeds    30s    1s    assert element in the device layout    {"Text": "CONFIRM"}
    Take Nexio Screenshot
