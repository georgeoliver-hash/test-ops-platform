*** Settings ***
Documentation     Given/When/Then steps for NJT Farebox (NJT_FRFRP) test cases: Program
...               Farebox Number (C4087052/C4087053), Communication Restore
...               (C4105012/C4105013, NJT_FRFRP_FS002 §5.6.6.2), and Communications Lock /
...               Force Comms (C4087164, NJT_FRFRP_FS002 §3.1.2).
...
...               Step wording is kept as close to the TestRail case text as possible so a
...               reviewer can line up a test file's *** Test Cases *** section against the
...               TestRail case directly. Every step here calls into
...               ETMFareboxInteractionUtility.robot, which today fails loudly for every NJT
...               verb (see Platforms/ETMFareboxNjtUtility.robot) - these suites are expected
...               to run and fail at the first Farebox step until that layer is wired against
...               a live device, same as the existing Duty/FLU sliver.
Resource          ../Utility/ETMFareboxInteractionUtility.robot
Resource          ../Utility/ETMAdaptorUtility.robot

*** Keywords ***
# ─────────────────────────────────────────────────────────────────────────────
#  Shared preconditions (Program Farebox Number + Communication Restore)
# ─────────────────────────────────────────────────────────────────────────────
the FR is powered on
    [Documentation]    No explicit action - the device is powered and reachable as a
    ...                precondition of the suite even being able to run at all.
    No Operation

the user has signed into the Administrator Mode
    ETM: Farebox: Enter Administrator Mode

the Farebox is connected to the FR
    ETM: Farebox: Assert Farebox Connected

the Farebox has no faults
    ETM: Farebox: Assert Farebox Has No Faults

# ─────────────────────────────────────────────────────────────────────────────
#  Program Farebox Number (C4087052 / C4087053)
# ─────────────────────────────────────────────────────────────────────────────
the user selects the Program Farebox Number option
    ETM: Farebox: Select Program Farebox Number Option

the the user will be prompted to enter the new Farebox ID
    [Documentation]    Keyword name mirrors the TestRail case's own doubled "the the" wording
    ...                verbatim, so this step maps 1:1 back to the case text.
    ETM: Farebox: Assert Prompted For New Farebox Id

the user enters a valid Farebox ID
    [Documentation]    Farebox ID is 3-byte BCD on the wire (NJT_FRFRP_IS001 v2 command 0x31)
    ...                - any 6-digit numeric value is a structurally valid ID. TestRail does
    ...                not specify a particular value, so a fixed placeholder is used; swap
    ...                for a data-driven value once this is wired against a live device.
    [Arguments]    ${farebox_id}=654321
    ETM: Farebox: Enter Farebox Id    ${farebox_id}
    Set Test Variable    ${FAREBOX_ID_ENTERED}    ${farebox_id}

the user enters an invalid Farebox ID
    [Documentation]    NJT_FRFRP_HMI01 v4 §12.1.1 now confirms the validation rule: 1-6
    ...                digits is valid, so the placeholder must be outside that range.
    ...                7 digits is the smallest invalid value (this file previously used
    ...                "1234", a 4-digit value that the spec confirms is actually VALID -
    ...                fixed here now that the real rule is known).
    [Arguments]    ${farebox_id}=1234567
    ETM: Farebox: Enter Farebox Id    ${farebox_id}

the user confirms the number
    ETM: Farebox: Confirm Number

the FR will send the Program Farebox ID message to the Farebox with the new number
    ETM: Farebox: Assert Program Farebox Id Message Sent    ${FAREBOX_ID_ENTERED}

the FR will send a Request Farebox details message
    ETM: Farebox: Assert Fb Information Request Sent

the FR will display the number to confirm the action has completed
    ETM: Farebox: Assert Farebox Number Displayed    ${FAREBOX_ID_ENTERED}

the FR will return to the Administrator menu
    ETM: Farebox: Assert Returned To Administrator Menu

# ─────────────────────────────────────────────────────────────────────────────
#  Communication Restore (C4105012 / C4105013)
# ─────────────────────────────────────────────────────────────────────────────
a communication loss has been registered between the Fare Register and the Farebox
    ETM: Farebox: Simulate Communication Loss

the Fare Register is signed onto an Exact Fare trip
    [Documentation]    Requires NJT Duty/TripSetup onboarding, which is not yet wired for
    ...                NJT either (ETM: Duty: Njt: * in ETMNjtInteractionUtility.robot) -
    ...                this suite will fail here until that lands, independent of the
    ...                Farebox-specific gaps in this file.
    ETM: Sign On Fresh
    ETM: Duty: Onboard To Trip Selection

the communications has been restored between the Fare Register and the Farebox
    ETM: Farebox: Restore Communication

the communications has not been restored between the Fare Register and the Farebox
    [Documentation]    Deliberately a no-op: "not restored" means we simply don't call
    ...                Restore Communication, leaving the loss from the Given step in place.
    No Operation

the Farebox simulator communication should be restored to normal
    [Documentation]    Test-cleanup step (call from Test Teardown, not from the TestRail
    ...                step sequence itself): unconditionally clears no_response and
    ...                re-enables auto_reply on the Farebox simulator regardless of test
    ...                outcome, so Communication-Restore-Failure's deliberately-left-open
    ...                comms loss never leaks into whatever runs next.
    ETM: Farebox: Ensure Simulator Communication Normal

the user waits for 1 minute
    Sleep    1 minute

the Fare Register automatically tries to restore the communications by polling the Farebox for 2 seconds
    [Documentation]    Passive/automatic FR behaviour (NJT_FRFRP_FS002 §5.6.6.2) - nothing to
    ...                drive from the test side, the FR does this on its own timer. Logged for
    ...                traceability against the TestRail step rather than omitted.
    Log    Waiting for the FR's own automatic communication-restore poll (no test action)

the Fare Register will revert back to Exact Fare mode
    ETM: Farebox: Assert Fare Mode    Exact Fare

the Fare Register will stay in Full Service mode
    ETM: Farebox: Assert Fare Mode    Full Service

# ─────────────────────────────────────────────────────────────────────────────
#  Communications Lock / Force Comms (C4087164)
# ─────────────────────────────────────────────────────────────────────────────
the FR is in the Locked state
    ETM: Farebox: Force FR Into Locked State

the user has signed on as a Supervisor
    ETM: Farebox: Sign On As Supervisor

the user is viewing the Force Communications page of the Supervisor Menu
    ETM: Farebox: Navigate To Force Communications Page

the user is able to re-establish comms with the back office
    [Documentation]    A stated capability/precondition, not an action to drive - kept as a
    ...                no-op step (matching "the user is able to..." phrasing) so the test
    ...                file's Given block reads identically to the TestRail case.
    No Operation

the user re-establishes comms with the back office
    [Documentation]    TestRail's own step text reads "When is user re-establishes..." (typo
    ...                for "the") - cleaned up here rather than reproduced verbatim.
    ETM: Farebox: Reestablish Back Office Comms

the user selects the option available to force a communications session
    ETM: Farebox: Select Force Communications Session Option

a successful communications session occurs
    ETM: Farebox: Assert Communications Session Successful

the FR will enter the Idle functional state
    ETM: Farebox: Assert Idle Functional State
