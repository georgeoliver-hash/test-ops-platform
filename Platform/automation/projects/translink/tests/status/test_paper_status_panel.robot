*** Settings ***
Documentation    Paper-status panel -- printer health and roll-life surfaces.
...
...              Screen: `paperstatuslayout.xml`. Labels from static APK analysis:
...              - `PaperStatus.TicketRollLength` ("Ticket Roll Length:")
...              - `PaperStatus.PaperPercentageRemaining` ("Paper Percentage Remaining")
...              - `PaperStatus.AverageTicketsRemaining` ("Average Tickets Remaining:")
...              - `PaperStatus.PaperLowThreshold` ("Paper Low Threshold:")
...              - `PaperStatus.ReversePaperFeed` ("Reverse Paper Feed")
...
...              Per DatasetParameters.json the build is provisioned with
...              `lowPaperLengthMetres=10` -- once we can navigate into this panel
...              on a live device, that value should surface next to the "Paper Low
...              Threshold" label. That assertion is TODO'd below -- for now we only
...              verify the panel renders.
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:status

*** Variables ***
${DEVICE_TYPES}    POS

*** Test Cases ***
Paper Status Panel Renders Labels
    [Documentation]    All 5 static labels on the paper-status screen render.
    Start Activity    com.flowbird.pos
    # TODO: navigate into the paper-status panel; likely from a maintenance or
    # device-status submenu. For now assume the test runner has driven us here.
    Assert Visible Labels
    ...    PaperStatus.TicketRollLength
    ...    PaperStatus.PaperPercentageRemaining
    ...    PaperStatus.AverageTicketsRemaining
    ...    PaperStatus.PaperLowThreshold
    ...    PaperStatus.ReversePaperFeed
    ...    screen=paper-status panel

Paper Low Threshold Matches Dataset
    [Documentation]    The threshold shown next to `PaperStatus.PaperLowThreshold`
    ...    matches DatasetParameters.lowPaperLengthMetres.
    ...
    ...    Skipped until we can navigate into the panel and locate the value node
    ...    -- the value sits in a sibling view set programmatically in Xamarin.
    ${dataset_parameters}=    Get Dataset Parameters
    ${expected}=    Evaluate    $dataset_parameters['lowPaperLengthMetres']
    Start Activity    com.flowbird.pos
    ${label}=    Lookup POS String    PaperStatus.PaperLowThreshold
    ${visible}=    Visible Texts
    Skip If    $label not in $visible    Paper-status panel not currently on screen
    # TODO: extract the value adjacent to the label. uiautomator dump exposes
    # siblings by bounds proximity -- implement once a real screenshot lands.
    Skip    Adjacent-value extraction not yet implemented; expected lowPaperLengthMetres=${expected} from DatasetParameters.
