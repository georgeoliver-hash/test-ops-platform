*** Settings ***
Documentation    Volume and brightness options panel.
...
...              Screen: `volumeandbrightnesssettingslayout.xml`. Static
...              labels:
...              - `OptionsMenu.volume_title` ("Volume")
...              - `OptionsMenu.brightness_title` ("Brightness")
...              - `OptionsMenu.plus_sign` ("+") and `OptionsMenu.minus_sign`
...                ("-") — the step controls.
...
...              DatasetParameters provisions defaults
...              `audioLevelDefault=4` and `brightnessLevelDefault=5`. On a
...              freshly-booted device the current sliders should reflect
...              those — the second test below sketches that assertion, but
...              the slider value lives in a Xamarin-side control whose
...              `@text` we haven't mapped yet, so it's TODO'd.
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts
Force Tags       project:translink    device_types:POS    feature:options

*** Variables ***
${DEVICE_TYPES}    POS
@{OPTIONS_LABELS}    OptionsMenu.volume_title    OptionsMenu.brightness_title
...    OptionsMenu.plus_sign    OptionsMenu.minus_sign

*** Test Cases ***
Volume Brightness Panel Renders Labels
    [Documentation]    All 4 static controls render on the volume/brightness
    ...    settings panel.
    Start Activity    com.flowbird.pos
    # TODO: navigate into the volume/brightness settings panel. Entry likely:
    # supervisor menu -> Options -> Volume/Brightness.
    Assert Visible Labels    @{OPTIONS_LABELS}    screen=volume/brightness panel

Volume Brightness Defaults Match Dataset
    [Documentation]    Current volume/brightness slider values match the
    ...    DatasetParameters defaults.
    ...
    ...    Skipped until the slider-value node is identified — its @text
    ...    isn't set in the layout XML and we haven't observed it in a live
    ...    uiautomator dump yet.
    ${dataset}=    Get Dataset Parameters
    ${expected_volume}=    Set Variable    ${dataset}[audioLevelDefault]
    ${expected_brightness}=    Set Variable    ${dataset}[brightnessLevelDefault]
    Start Activity    com.flowbird.pos
    ${volume_label}=    Lookup POS String    OptionsMenu.volume_title
    ${seen}=    Visible Texts
    Skip If    $volume_label not in $seen
    ...    Volume/brightness panel not currently on screen
    Skip    Slider-value node not yet identified; expected audioLevelDefault=${expected_volume}, brightnessLevelDefault=${expected_brightness}.
