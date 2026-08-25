*** Settings ***
Documentation    Annul-last-ticket flow.
...
...              Screen chain (from docs/screens.md):
...              - `annulmentticketslayout.xml` (list -- strings set programmatically)
...              - `annulmentticketconfirmationlayout.xml` exposes `Annulment.Total`
...                ("Total:"), `AnnulmentConfirmation.Title` ("Annul Last Ticket"),
...                `LinkWord_At` ("at").
...              - Negative-path string: `Annulment.NothingToAnnul` ("No Ticket to
...                Annul") triggers when there's nothing to cancel.
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:transactions

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Nothing To Annul When No Recent Ticket
    [Documentation]    Fresh device with no transactions -> annul flow reports
    ...    no ticket to annul.
    ...    TODO: navigate into annul flow (menu -> Annul Transaction). The
    ...    'Annul Transaction' menu entry uses `Annul.title_ticket`.
    Start Activity    com.flowbird.pos
    Assert Visible Labels    Annulment.NothingToAnnul    screen=annul flow (fresh device)

Annul Confirmation Screen Shows Total
    [Documentation]    After running a successful transaction, annul flow shows the total.
    Skip    Needs a precondition: at least one prior transaction in the day's register. Add this when we have a way to seed device state from tests.
