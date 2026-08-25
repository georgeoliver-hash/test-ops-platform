*** Settings ***
Documentation    Audit/BOSRecords ledger is reachable on the device and any
...              present records parse.
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:audit

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Audit Ledger Path Resolves
    [Documentation]    Ledger path should be set after discover().
    ${ledger}=    Get Local Audit Ledger
    Should Be True    ${ledger.path}    ledger path should be set after discover()

Newest Audit Record Is Parseable
    [Documentation]    Newest record parses and carries a _filename key.
    ${ledger}=    Get Local Audit Ledger
    ${records}=    List Local Audit Records
    Skip If    not $records    Ledger ${ledger.path} is empty — nothing to parse
    ${record}=    Newest Local Audit Record
    Should Not Be Equal    ${record}    ${None}
    ...    msg=newest_record returned None despite non-empty ledger
    Dictionary Should Contain Key    ${record}    _filename
