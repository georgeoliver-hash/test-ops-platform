*** Settings ***
Documentation    Smartcard-status panel -- issued card inspection surfaces.
...
...              Screen: `smartcardstatuslayout.xml`. Eleven static labels -- when a
...              card is presented the panel shows its identity (ESN, PSN, CardRef),
...              validity dates, remaining journeys / days, and last-usage /
...              last-topup timestamps.
...
...              We don't drive card presentation from a test (yet) -- this is a
...              label-shape assertion: open the panel, verify every expected field
...              label renders.
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:status

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Smartcard Status Panel Renders Labels
    [Documentation]    All 11 static labels on the smartcard-status screen render.
    Start Activity    com.flowbird.pos
    # TODO: navigate into the smartcard-status panel. Likely entry: supervisor
    # menu -> Smartcard -> tap "Status" or present a card on the reader.
    Assert Visible Labels
    ...    SmartcardStatus.CardRef
    ...    SmartcardStatus.CardType
    ...    SmartcardStatus.ESN
    ...    SmartcardStatus.PSN
    ...    SmartcardStatus.StartDate
    ...    SmartcardStatus.ExpiryDate
    ...    SmartcardStatus.DaysLeft
    ...    SmartcardStatus.JourneysLeft
    ...    SmartcardStatus.LastTopUp
    ...    SmartcardStatus.LastUsage
    ...    SmartcardMenu.MiniStatement
    ...    screen=smartcard-status panel
