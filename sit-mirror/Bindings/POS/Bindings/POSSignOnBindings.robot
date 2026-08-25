*** Settings ***
Documentation     Given/When/Then steps for POS operator sign-on / sign-off.
...
...               The EventLog-based steps (baseline / wait for event) are implemented and
...               runnable today. The steps that drive the sign-on screen itself (typing
...               credentials, reading the ID/PIN labels) call into keywords that currently
...               raise "Not Implemented" — see POSAndroidInteractionUtility.robot for why.
...               Test files using this Resource will run as far as that gap and then fail
...               loudly there, which is intentional: it should be obvious exactly where
...               POS testing is blocked, rather than silently skipping.
Resource          ../Utility/POSInteractionUtility.robot
Resource          ../../../Common/Utility/StaffUtility.robot

*** Keywords ***
an available pos ${role}
    [Documentation]    Pulls a real staff id/PIN for this device's home location from the
    ...                ConfigSet's DeviceStaff.json (role "<Role>_POS" — Operator, Supervisor
    ...                and Technician are all present for Translink) via SAM/StaffUtility —
    ...                the same mechanism ETM's demo suite uses, rather than a hardcoded
    ...                credential the way the old repo's devices.yaml did.
    ${staff_id}    ${staff_pin}=    Staff: Get Available Staff Member
    ...    ${role}    POS    ${current_device}[homelocation]
    RETURN    ${staff_id}    ${staff_pin}

the operator is signed off
    POS: Ensure Signed Off

a baseline is recorded for ${event_type} events
    ${baseline}=    POS: EventLog: Latest Index    ${event_type}
    RETURN    ${baseline}

the operator signs on with the available credentials
    [Arguments]    ${timeout}=20
    ${operator_id}    ${operator_pin}=    an available pos Operator
    POS: Sign On    ${operator_id}    ${operator_pin}    timeout=${timeout}

the ${role} signs on with the available credentials
    [Documentation]    Role-based variant, modeled on
    ...                Tests/Devices/DeviceFunctions/DeviceLogOn.robot (which covers
    ...                Operator/Technician/Supervisor for ETM) — new coverage per TIBU-33556,
    ...                not in George's original 26.
    [Arguments]    ${timeout}=20
    ${staff_id}    ${staff_pin}=    an available pos ${role}
    POS: Sign On    ${staff_id}    ${staff_pin}    timeout=${timeout}

the operator signs off
    POS: Sign Off

a ${event_type} event should be emitted within ${seconds} seconds of the ${baseline} baseline
    POS: EventLog: Wait For Event    ${event_type}    ${baseline}    timeout=${seconds}

the operator attempts to sign on with an unrecognised ID and PIN
    [Documentation]    C4099921. Uses a fixed non-staff ID/PIN pair -- any value not present
    ...                as a "<Role>_POS" entry in the ConfigSet's DeviceStaff.json qualifies
    ...                as unrecognised, so this doesn't need its own confirmed fact.
    POS: Sign On With Incorrect Credentials    999999    0000

the operator attempts to sign on with an unrecognised ID and PIN ${attempts} times
    [Documentation]    C4099922 (destructive: locks the device on the final attempt). The
    ...                lockout threshold is TMS-configured (per George's review note on the
    ...                original handover case: "don't hard-code 3") -- the caller must pass
    ...                the value actually configured for the target environment, not assume 3.
    FOR    ${i}    IN RANGE    ${attempts}
        POS: Sign On With Incorrect Credentials    999999    0000
    END

communication with CloudFare has been lost beyond the configured period
    [Documentation]    C4099924 / C4100362 precondition. See
    ...                POS: Simulate Communication Loss's Documentation for why this can't
    ...                be implemented yet -- it's a missing test fixture, not the Android
    ...                UI-driving gap the rest of this file is blocked on.
    POS: Simulate Communication Loss

the operator attempts to sign on
    [Documentation]    C4099924 -- a normal sign-on attempt (valid credentials would still be
    ...                rejected here, since comms are down, not the credentials). Not
    ...                wrapped in a swallow-the-error keyword: like every other Sign On step
    ...                in this file, it should fail loudly at the same UI-driving gap, not
    ...                silently pass because the error was caught.
    ${operator_id}    ${operator_pin}=    an available pos Operator
    POS: Sign On    ${operator_id}    ${operator_pin}

a supervisor presents a valid Supervisor card
    [Documentation]    C4099923. GAP: no Supervisor-card presentation fixture exists in this
    ...                repo yet (hardware, same class of gap as every other card-present
    ...                case) -- see test_signon_lockout.robot's [Setup] Skip.
    Fail    Not Implemented — no Supervisor-card presentation fixture, see keyword Documentation
