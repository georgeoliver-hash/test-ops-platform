*** Settings ***
Documentation    Basket confirmation -> choice of payment method.
...
...              Screen: `basketconfirmationlayout.xml` exposes the three
...              payment-method buttons as static strings:
...              `PaymentMethod.Cash` ("Cash"), `PaymentMethod.BankCard`
...              ("Bank Card"), `PaymentMethod.Warrant` ("Warrant"), plus
...              `PaymentMethod.AddMore` ("Add More") to return to the basket
...              view.
...
...              The transaction event lands in EventLog under an
...              as-yet-unverified eventType. Best guess from BSP-base scan: a
...              `state.changed` row with a transaction payload, possibly
...              accompanied by a `resource.changed` row for the receipt.
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:transactions

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Payment Method Button Present
    [Documentation]    All three payment-method buttons are visible on the
    ...    basket confirmation. TODO (carried over from pytest): bring the
    ...    device to the basket-confirmation screen first (sign-on -> add
    ...    product -> tap confirm). For now just assume we're there.
    [Template]    Assert Payment Method Button Present
    PaymentMethod.Cash
    PaymentMethod.BankCard
    PaymentMethod.Warrant

Cash Payment Emits Transaction Event
    [Documentation]    Tapping Cash should produce an EventLog row for the
    ...    transaction. We don't know the exact event_type yet, so we watch
    ...    the two most likely candidates (state.changed and resource.changed)
    ...    and require *something* new to land. Tighten when a real run lets
    ...    us pin the schema. TODO: precondition (signed on + item in basket +
    ...    on confirm screen).
    Start Activity    com.flowbird.pos
    ${state_baseline}=       Latest Event Index    state.changed
    ${resource_baseline}=    Latest Event Index    resource.changed
    ${state_baseline}=       Set Variable If    $state_baseline is None    ${0}    ${state_baseline}
    ${resource_baseline}=    Set Variable If    $resource_baseline is None    ${0}    ${resource_baseline}

    ${cash_label}=    Lookup POS String    PaymentMethod.Cash
    ${tapped}=        Tap Text    ${cash_label}
    Should Be True    ${tapped}    Could not tap the Cash payment-method button

    ${new_state}=       Events Since    state.changed    ${state_baseline}
    ${new_resource}=    Events Since    resource.changed    ${resource_baseline}
    ${any_new}=    Evaluate    bool($new_state) or bool($new_resource)
    Should Be True    ${any_new}
    ...    No state.changed or resource.changed events fired after cash payment

*** Keywords ***
Assert Payment Method Button Present
    [Arguments]    ${method_resource}
    Start Activity    com.flowbird.pos
    # TODO: bring the device to the basket-confirmation screen first
    # (sign-on -> add product -> tap confirm). For now just assume we're there.
    Assert Visible Labels    ${method_resource}    screen=basket confirmation
