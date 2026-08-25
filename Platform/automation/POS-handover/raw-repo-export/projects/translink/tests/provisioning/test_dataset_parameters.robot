*** Settings ***
Documentation    Build verification — live device matches the canonical
...              `DatasetParameters.json`.
...
...              The build's authored configuration carries 14 application-level
...              behaviour values. The cleanest cross-check available without a
...              runtime config provider mapping is `softwareVersion` ↔ the
...              installed POS package's `versionName`, because
...              `package_version` is a stable platform API.
...
...              The other 13 values (automaticLogOff, screenSaverTimeout,
...              enableEmv, etc.) are runtime behaviour assertions — they belong
...              in feature-specific tests (idle/screensaver, EMV-disabled-build,
...              etc.) where they can be exercised rather than just compared as
...              strings.
...
...              The pure-data sanity test (no device) verifies the JSON is
...              well-formed and carries every key we test against — guards
...              against silent build-pipeline schema drift.
Resource         ${CURDIR}/../../../../resources/common.resource
Suite Setup      Connect To Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts

*** Variables ***
${DEVICE_TYPES}    POS
@{EXPECTED_KEYS}    softwareVersion    automaticLogOff    screenSaverTimeout
...    powerInterrupt    audioLevelDefault    brightnessLevelDefault
...    maxRevenueWithoutComms    conversionValue    decimalPrecision
...    lowPaperLengthMetres    slipsPaperJam
...    numberDaysAutonomyWithoutFullSynchronisation    merchantReceipt    enableEmv

*** Test Cases ***
Dataset Parameters Has All Expected Keys
    [Documentation]    The authored DatasetParameters carries every key tests
    ...    rely on.
    [Tags]    feature:smoke
    ${params}=    Get Dataset Parameters
    ${missing}=    Evaluate    sorted(set(${EXPECTED_KEYS}) - set($params.keys()))
    Should Be Empty    ${missing}    DatasetParameters.json missing keys: ${missing}

Pos Package Version Matches Dataset Software Version
    [Documentation]    The installed `com.flowbird.pos` versionName matches
    ...    DatasetParameters.softwareVersion.
    [Tags]    project:translink    device_types:POS    feature:smoke
    ${params}=    Get Dataset Parameters
    ${expected}=    Set Variable    ${params}[softwareVersion]
    ${installed}=    Package Version    com.flowbird.pos
    Should Not Be Equal    ${installed}    ${None}    could not read versionName from dumpsys
    Should Contain    ${installed}    ${expected}
    ...    msg=installed versionName=${installed} does not match DatasetParameters.softwareVersion=${expected}

Registry Build Version Matches Dataset Software Version
    [Documentation]    The project's devices.yaml registry version matches the
    ...    authored build.
    [Tags]    project:translink    device_types:POS    feature:smoke
    ${params}=    Get Dataset Parameters
    ${expected}=    Set Variable    ${params}[softwareVersion]
    ${registry_version}=    Get Device Build Version
    Skip If    not $registry_version or $registry_version == 'TBD'
    ...    No build.version pinned in registry for the device
    ${match}=    Evaluate    ($expected in $registry_version) or ($registry_version in $expected)
    Should Be True    ${match}
    ...    devices.yaml build.version=${registry_version} does not match DatasetParameters.softwareVersion=${expected}
