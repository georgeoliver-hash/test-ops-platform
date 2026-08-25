*** Settings ***
Documentation    Build verification for the Translink ETM — the WinCE
...              counterpart of `test_dataset_parameters.robot`.
...
...              The ETM authors 22 application-level behaviour values into
...              `DMParameters.json`. As with the POS, most are *runtime
...              behaviour* assertions (auto-logoff, max-invalid-logins,
...              EMV-disabled) that belong in feature tests once the device is
...              reachable. What we can verify offline today:
...
...              * the authored JSON is well-formed and carries every key
...              tests rely on (guards against silent build-pipeline schema
...              drift), and
...              * the registry's pinned build version agrees with the
...              authored `softwareVersion`.
...
...              No live-device assertion here: the ETM has `ui: none` and no
...              shell, so there's no `package_version`-style cross-check like
...              the POS has.
Resource         ${CURDIR}/../../../../resources/common.resource
Library          framework.robot.wince_library.WinceLibrary
Suite Setup      Resolve Device
Suite Teardown   Disconnect From Device
Test Setup       Clear Device Logs
Test Teardown    Collect Test Artefacts

*** Variables ***
${DEVICE_TYPES}    ETMS
@{EXPECTED_KEYS}    softwareVersion    automaticLogOff    powerSaveTimeout
...    suspendDuration    powerInterrupt    audioLevelDefault
...    brightnessLevelDefault    maxRevenueWithoutComms    maximumRevenueWarning
...    maximumInvalidLoginAttempts    conversionValue    decimalPrecision
...    offLineValueThreshold    abtPassback    abtMetroTooZone
...    abtUlsterbusTooZone    lowPaperLengthMetres    slipsPaperJam
...    numberDaysAutonomyWithoutFullSynchronisation    enableEmv
...    logfilesMaxSize    logfilesMaxNumber

*** Test Cases ***
Etm Dm Parameters Has All Expected Keys
    [Documentation]    The authored DMParameters carries every key tests rely on.
    [Tags]    feature:smoke
    ${params}=    Get ETM DM Parameters
    ${missing}=    Evaluate    sorted(set(${EXPECTED_KEYS}) - set($params.keys()))
    Should Be Empty    ${missing}    DMParameters.json missing keys: ${missing}

Etm Registry Build Version Matches Dm Software Version
    [Documentation]    The project's devices.yaml registry version matches the
    ...    authored build.
    [Tags]    project:translink    device_types:ETMS    feature:smoke
    ${params}=    Get ETM DM Parameters
    ${expected}=    Set Variable    ${params}[softwareVersion]
    ${registry_version}=    Get Device Build Version
    Skip If    not $registry_version or $registry_version == 'TBD'
    ...    No build.version pinned in registry for the device
    ${match}=    Evaluate    ($expected in $registry_version) or ($registry_version in $expected)
    Should Be True    ${match}
    ...    devices.yaml build.version=${registry_version} does not match DMParameters.softwareVersion=${expected}
