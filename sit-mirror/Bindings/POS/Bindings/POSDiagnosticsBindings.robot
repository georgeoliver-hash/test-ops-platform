*** Settings ***
Documentation     Given/When/Then steps for the two POS diagnostic smoke checks:
...               (1) app install/runtime details — is it installed, when installed/updated,
...               where and how big on-device, is it running/foreground and for how long, with
...               a screenshot when launched; and (2) full platform/system report — OS/kernel/
...               build, uptime, errors/coredumps, network, memory, storage, SD card and
...               processor/hardware identity. Both write a plain-text report under
...               results/evidence/ (picked up by the pipeline's "Upload Robot results" step)
...               in addition to logging to the Robot log/console.
Resource          ../Utility/POSInteractionUtility.robot
Resource          ../../Common/Utility/DeviceEvidenceUtility.robot
Library           OperatingSystem

*** Keywords ***
the flowbird pos app install details should be reported
    [Documentation]    Reports app name (package id), first-install/last-update timestamps,
    ...                on-device install location and installed size (MB) for
    ...                ${current_device}[appPackage].
    ${info}=    POS: App Install Info
    ${size_bytes}=    POS: App Size Bytes    ${info}[install_path]
    ${size_mb}=    Evaluate    round(${size_bytes} / (1024 * 1024), 2)
    ${report}=    Catenate    SEPARATOR=\n
    ...    ==================== Flowbird POS App — Install Details ====================
    ...    App name (package)   : ${current_device}[appPackage]
    ...    First install time   : ${info}[first_install_time]
    ...    Last update time     : ${info}[last_update_time]
    ...    Install location     : ${info}[install_path]
    ...    Installed size       : ${size_mb} MB (${size_bytes} bytes)
    ...    ==============================================================================
    Log    ${report}    console=True
    Create Directory    results/evidence
    Create File    results/evidence/pos_app_install_report.txt    ${report}

the flowbird pos app runtime status should be reported
    [Documentation]    Reports whether the app is running/foreground/background and, if
    ...                running, for how long — plus a screenshot when it's running (via the
    ...                device-agnostic Device: Capture State, saved to
    ...                results/evidence/state_app_launched.png).
    ${state}=    POS: App Foreground State
    ${uptime_s}=    POS: App Uptime Seconds
    ${report}=    Catenate    SEPARATOR=\n
    ...    ==================== Flowbird POS App — Runtime Status ======================
    ...    Current status       : ${state}
    ...    Running for          : ${uptime_s} seconds
    ...    ==============================================================================
    Log    ${report}    console=True
    Create Directory    results/evidence
    Create File    results/evidence/pos_app_runtime_report.txt    ${report}
    IF    '${state}' != 'Not Running'
        Device: Capture State    app_launched
        Log    Screenshot captured: results/evidence/state_app_launched.png    console=True
    ELSE
        Log    App is not running — no launched-state screenshot captured    console=True
    END

the pos device platform information should be reported
    [Documentation]    Gathers and reports OS/kernel/build version, uptime, errors/alarms,
    ...                coredumps, network interfaces/ports, installed third-party apps, RAM,
    ...                internal storage, SD card and processor/hardware info for the Translink
    ...                POS device. Writes a human-readable report to
    ...                results/evidence/pos_platform_report.txt and logs it to the
    ...                console/Robot log.
    ${data}=    POS: Platform Report
    ${errors_text}=    Catenate    SEPARATOR=\n    @{data}[recent_errors]
    ${errors_text}=    Set Variable If    "${errors_text}" == ""    (none in the last 50 ERROR lines)    ${errors_text}
    ${coredumps_count}=    Get Length    ${data}[coredumps]
    ${apps_text}=    Catenate    SEPARATOR=\n    @{data}[installed_apps]
    ${report}=    Catenate    SEPARATOR=\n
    ...    ================================================================================
    ...    Translink POS Device — Platform Report (${current_device}[device_id])
    ...    ================================================================================
    ...    -- Operating System --
    ...    OS type             : ${data}[os][os_type]
    ...    Android version     : ${data}[os][android_version]
    ...    OS build version    : ${data}[os][build_version]
    ...    Kernel version      : ${data}[os][kernel_version]
    ...    Device uptime       : ${data}[uptime_seconds] seconds
    ...
    ...    -- Health --
    ...    Recent errors (last 50 logcat ERROR lines):
    ...    ${errors_text}
    ...    Coredumps/tombstones found : ${coredumps_count}
    ...    ${data}[coredumps]
    ...
    ...    -- Network --
    ...    Interfaces:
    ...    ${data}[network_interfaces]
    ...    Listening ports:
    ...    ${data}[listening_ports]
    ...
    ...    -- Memory (RAM) --
    ...    Total   : ${data}[memory][total_mb] MB
    ...    Used    : ${data}[memory][used_mb] MB (${data}[memory][used_percent]%)
    ...    Free    : ${data}[memory][free_mb] MB
    ...    (RAM chip type e.g. LPDDR4 is not exposed by standard Android OS interfaces)
    ...
    ...    -- Storage (internal /data) --
    ...    Total   : ${data}[storage][total_mb] MB
    ...    Used    : ${data}[storage][used_mb] MB (${data}[storage][used_percent]%)
    ...    Free    : ${data}[storage][free_mb] MB
    ...    (Storage chip type e.g. eMMC/UFS is not exposed by `df`)
    ...
    ...    -- SD Card --
    ...    ${data}[sd_card]
    ...
    ...    -- Processor --
    ...    Hardware/SoC   : ${data}[processor][hardware]
    ...    Platform code  : ${data}[processor][platform]
    ...    Manufacturer   : ${data}[processor][manufacturer]
    ...    Core count     : ${data}[processor][core_count]
    ...
    ...    -- Hardware / Model --
    ...    Model              : ${data}[hardware_version][model]
    ...    Hardware id        : ${data}[hardware_version][hardware_id]
    ...    Build incremental  : ${data}[hardware_version][build_incremental]
    ...
    ...    -- Installed Third-Party Apps (name + install path) --
    ...    ${apps_text}
    ...    ================================================================================
    Log    ${report}    console=True
    Create Directory    results/evidence
    Create File    results/evidence/pos_platform_report.txt    ${report}
