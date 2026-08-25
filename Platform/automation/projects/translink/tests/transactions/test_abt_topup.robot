*** Settings ***
Documentation    ABT smartcard top-up flow.
...
...              Strings (from POSStrings index):
...              - `Abt.TopUp` ("Top Up")
...              - `Abt.SuccessfulTopUp` ("Top Up Successful")
...              - `Abt.TopUpFailed` ("Unable to Top Up Card")
...              - `Abt.TopUpTitle` ("ABT Smartcard")
...              - `Abt.TopupBalance` ("Current balance: {Balance}")
...              - `AbtCardMenu.TopupProduct` ("Top Up")
...              - `AbtTopup.Title` ("Top Up")
...              - `AbtTopup.FailIssueCard` ("Unable to Issue Card")
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:topup

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Topup Title Present On Smartcard Menu
    [Documentation]    When a smartcard is present, the menu offers Top Up.
    ...    TODO: simulate smartcard insertion. This may require a hardware
    ...    harness or a fake event into com.parkeon.generic.smartcard service.
    Start Activity    com.flowbird.pos
    Skip    Card-present simulation not yet implemented -- we'd need to inject into the smartcard service or use a physical card reader fixture.

Successful Topup Emits Resource Changed
    [Documentation]    A successful top-up should produce a `resource.changed`
    ...    event for the smartcard balance update and a `state.changed` event
    ...    for the transaction.
    Skip    Card-present simulation not yet implemented (see Topup Title Present On Smartcard Menu).
