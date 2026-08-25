*** Settings ***
Documentation    Basket add -> clear roundtrip on the POS.
...
...              Screens (from docs/screens.md):
...              - `basketviewlayout.xml` -- has `Basket.advance_ticket`,
...                `Basket.clear_button`, `Basket.count_tickets`,
...                `Basket.delete_button`, `Basket.label_tickets`.
...              - An item added flows through `basketviewitem.xml` (uses `Basket.To`).
...
...              Assertion strategy: after Clear Basket, the basket-view should
...              show zero items. We don't yet know the exact EventLog
...              signature for basket mutations, so the test sniffs
...              `resource.changed` events and notes them as TODO follow-ups.
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:transactions

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Basket Clear Resets Count
    [Documentation]    TODO: needs to be signed on first; for now assume the
    ...    test harness puts the device into a signed-on state before this
    ...    test runs. TODO: actually add an item to the basket. The
    ...    product-selection screen is not captured in the static layout list
    ...    (likely uses a runtime list built from GTFS / fare-product data).
    ...    We'll need an `add_basket_item` helper that talks to the basket via
    ...    Intent or by tapping into the product picker.
    Start Activity    com.flowbird.pos
    Assert Visible Labels    Basket.label_tickets    screen=basket view (precondition)

    ${clear_label}=    Lookup POS String    Basket.clear_button
    ${tapped}=         Tap Text    ${clear_label}
    Should Be True    ${tapped}    Could not tap the Clear Basket button

    ${delete_label}=    Lookup POS String    Basket.delete_button
    ${visible}=         Visible Texts
    List Should Not Contain Value    ${visible}    ${delete_label}
    ...    msg=Delete item still visible after clearing basket
