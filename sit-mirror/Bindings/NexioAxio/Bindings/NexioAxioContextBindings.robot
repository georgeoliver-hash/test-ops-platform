*** Settings ***
Documentation     NexioAxio context-switching bindings.
...               A device "switch" must move BOTH layers that target a device:
...                 - the Python device context (DeviceUI / DeviceNavigation), via
...                   Device.set_active_device — this is what `device layout matches`
...                   and `navigate device to screen` read (testsupport_uri); and
...                 - the Robot CDP keyword layer, via ${CDP_TSS_URL} (CDPKeywords.robot).
...               Focus is by position + type against the job-data ${devices}
...               (ETM_1 = Nexio, BV_1 = Axio) using the common Environment keyword —
...               not a hand-rolled re-implementation.

Resource    ../../../Common/Utility/EnvironmentUtility.robot

*** Keywords ***
Switch To Device
    [Documentation]    Generic, platform-agnostic context switch by device Type. Moves BOTH
    ...                layers: the Python device context (via Environment: Focus on device,
    ...                read by `device layout matches` / `navigate device to screen`) AND the
    ...                Robot CDP keyword layer (${CDP_TSS_URL}), derived from the focused
    ...                device's own testsupport extension — no per-device URL globals.
    ...
    ...                Multi-device runs focus by position+type against the job-data
    ...                ${devices} dict (ETM_1 = Nexio, BV_1 = Axio). Single-device local runs
    ...                (robot --variablefile local_variables.py) have no ${devices} dict — just
    ...                ${current_device}; there the switch is a no-op re-sync provided the
    ...                active device already IS the requested type (a real cross-device switch
    ...                to an absent device fails with a clear message).
    [Arguments]    ${device_type}    ${position}=1
    # Decide by the ACTIVE device's Type rather than probing the ${devices} job-data
    # dict (which does not exist in single-device --variablefile runs, and testing for
    # a missing variable trips Robot's argument resolution). If we are already on the
    # requested type it is a no-op re-sync (single-device case, or already focused);
    # only a genuine type change consults the multi-device ${devices} dict.
    IF    '${current_device}[Type]' == '${device_type}'
        Device.set_active_device
        Set Suite Variable    ${CDP_TSS_URL}    ${TSS_URL}
    ELSE
        Environment: Focus on device    ${position}    ${device_type}
        Set Suite Variable    ${CDP_TSS_URL}    ${SWITCH_DEVICE_TSS_URL}
    END

Switch To ETM
    [Documentation]    Focus the ETM (e.g. Nexio) and point the CDP layer at it.
    [Arguments]    ${position}=1
    Switch To Device    ETM    ${position}

Switch To Validator
    [Documentation]    Focus the Validator (e.g. Axio / BV) and point the CDP layer at it.
    [Arguments]    ${position}=1
    Switch To Device    BV    ${position}
