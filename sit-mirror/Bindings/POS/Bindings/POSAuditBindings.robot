*** Settings ***
Documentation     Given/When/Then steps for POS EventLog liveness and on-device audit-ledger
...               checks. These are fully implemented — they only need the OS/EventLog-level
...               keywords, not the (currently unimplemented) Android UI-driving layer — and
...               are the cheapest, most foundational checks to run right after onboarding.
Resource          ../Utility/POSInteractionUtility.robot

*** Keywords ***
the ${event_type} eventlog should have recent rows
    POS: EventLog: Assert Has Recent Rows    ${event_type}

the ${event_type} eventlog indices should be monotonic
    POS: EventLog: Assert Indices Monotonic    ${event_type}

the audit ledger path should resolve
    ${records}=    POS: Audit Ledger: List Records
    Log    Found ${{len($records)}} audit ledger record(s)

the newest audit record should be parseable
    ${record}=    POS: Audit Ledger: Newest Record
    Should Not Be Empty    ${record}
