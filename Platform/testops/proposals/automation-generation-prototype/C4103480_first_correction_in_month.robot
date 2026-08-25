*** Settings ***
Documentation    PROOF OF CONCEPT — "step 7" auto-generated automated test.
...              Generated from TestRail case C4103480 (ABT / Functional / Correction Limits —
...              "First alighting-stop correction in the month is accepted"), suite 30279.
...              Target: Robot Framework (Browser library = Playwright under the hood) driving the
...              ABT Operator / Passenger web portal. Structure + tags are generated deterministically
...              from the case's Gherkin; locators/creds/waits are left as TODOs for the engineer.
Library          Browser
Resource         ../resources/abt_portal_keywords.resource    # shared page objects (to be built)
Suite Setup      Open ABT Portal    ${PORTAL}    ${OPERATOR_USER}    ${OPERATOR_PASS}
Suite Teardown   Close Browser
Force Tags       project:translink    device:ABT    feature:correction-limits    priority:high
...              case:C4103480    ref:CR122    automatable:yes

*** Variables ***
${PORTAL}            operator                 # run against operator AND passenger portal (2 configs)
${OPERATOR_USER}     %{ABT_PORTAL_USER}
${OPERATOR_PASS}     %{ABT_PORTAL_PASS}
# --- worked example carried from the TestRail case (real journey data) ---
${ROUTE}             72b (IN)
${BOARDING}          Moygashel Busby Shop
${ALIGHT_FROM}       Armagh Bus Centre
${ALIGHT_TO}         Dungannon Bus Station
${ORIGINAL_FARE}     £4.50

*** Test Cases ***
First Alighting-Stop Correction In The Month Is Accepted
    [Documentation]    C4103480 — a passenger's first alighting-stop correction in a calendar month
    ...                is accepted and the fare recalculates. GIVEN no prior correction this month.
    [Tags]    smoke:no    tier:yes
    # GIVEN a settled TOO journey with no prior correction this calendar month
    Given A Settled Journey Exists    route=${ROUTE}    boarding=${BOARDING}    alighting=${ALIGHT_FROM}
    And The Passenger Has No Correction This Calendar Month
    # WHEN the passenger corrects the alighting stop
    When The Alighting Stop Is Corrected    from=${ALIGHT_FROM}    to=${ALIGHT_TO}
    And The EndOfDay Settlement Runs
    # THEN the correction is accepted AND the fare is recalculated
    Then The Correction Is Accepted
    And The Journey Fare Is Recalculated For    stop=${ALIGHT_TO}
    # cross-check: the correction event is recorded back-office
    And The Correction Event Is Recorded In    systems=CloudFare, MERIT

*** Keywords ***
# NOTE: these are generated stubs — the engineer fills locators/waits/oracles, or they resolve
# against the shared ../resources/abt_portal_keywords.resource once that page-object exists.
A Settled Journey Exists
    [Arguments]    ${route}    ${boarding}    ${alighting}
    # TODO: seed or locate a settled TOO journey for the test card (fixture or portal search)
    Fail    Not implemented — seed a settled ${route} journey ${boarding} -> ${alighting}

The Passenger Has No Correction This Calendar Month
    # TODO: assert the correction counter for the card is 0 this month (reset fixture if needed)
    Fail    Not implemented

The Alighting Stop Is Corrected
    [Arguments]    ${from}    ${to}
    # TODO: open Journey History -> Update Stop, select ${to}, confirm
    Fail    Not implemented

The EndOfDay Settlement Runs
    # TODO: trigger / await the EndOfDay settlement (portal action or scheduled job hook)
    Fail    Not implemented

The Correction Is Accepted
    # TODO: assert the portal shows the correction accepted (no refusal message)
    Fail    Not implemented

The Journey Fare Is Recalculated For
    [Arguments]    ${stop}
    # TODO: assert the journey now alights at ${stop} with the recalculated fare
    Fail    Not implemented

The Correction Event Is Recorded In
    [Arguments]    ${systems}
    # TODO: cross-check the correction event reached ${systems} (activity log / MERIT)
    Fail    Not implemented
