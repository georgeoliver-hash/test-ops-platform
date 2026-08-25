*** Settings ***
Documentation     Given/When/Then steps for the NJT ETM platform/system diagnostic smoke
...               check - OS/kernel/build, app version, uptime, errors, network, RS485
...               serial port, memory, storage and processor identity. Mirrors
...               POSDiagnosticsBindings.robot's report-and-write-a-text-file pattern
...               exactly, one device family later.
Resource          ../Utility/ETMDiagnosticsInteractionUtility.robot
Library           OperatingSystem

*** Keywords ***
the njt etm device platform information should be reported
    [Documentation]    Gathers and reports reachability, app version, OS/kernel/build,
    ...                uptime, recent errors, network interfaces/ports, RS485 serial port,
    ...                RAM, storage and processor info for the NJT ETM. Writes a
    ...                human-readable report to results/evidence/njt_etm_platform_report.txt
    ...                and logs it to the console/Robot log.
    [Arguments]    ${device_ip}=${current_device}[Ip]
    ${data}=    ETM: Diagnostics: Platform Report    ${device_ip}
    ${errors_text}=    Catenate    SEPARATOR=\n    @{data}[recent_errors]
    ${errors_text}=    Set Variable If    "${errors_text}" == ""    (none in the last 50 error-priority journal lines)    ${errors_text}
    ${report}=    Catenate    SEPARATOR=\n
    ...    ================================================================================
    ...    NJT ETM Device — Platform Report (${device_ip})
    ...    ================================================================================
    ...    -- Reachability --
    ...    Ping reachable      : ${data}[ping][reachable]
    ...    ${data}[ping][output]
    ...
    ...    -- Application --
    ...    pap-sdk-app version : ${data}[app_version]
    ...
    ...    -- Operating System --
    ...    OS                  : ${data}[os][os_name]
    ...    Kernel version      : ${data}[os][kernel_version]
    ...    Build string        : ${data}[os][build_string]
    ...    Device uptime       : ${data}[uptime_seconds] seconds
    ...
    ...    -- Health --
    ...    Recent errors (last 50 error-priority journal lines):
    ...    ${errors_text}
    ...
    ...    -- Network --
    ...    Interfaces:
    ...    ${data}[network_interfaces]
    ...    Listening ports:
    ...    ${data}[listening_ports]
    ...
    ...    -- RS485 (Farebox link) --
    ...    Serial device(s):
    ...    ${data}[rs485_serial][devices]
    ...    In use:
    ...    ${data}[rs485_serial][in_use]
    ...
    ...    -- Memory (RAM) --
    ...    Total   : ${data}[memory][total_mb] MB
    ...    Used    : ${data}[memory][used_mb] MB (${data}[memory][used_percent]%)
    ...    Free    : ${data}[memory][free_mb] MB
    ...
    ...    -- Storage (root filesystem /) --
    ...    Total   : ${data}[storage][total_mb] MB
    ...    Used    : ${data}[storage][used_mb] MB (${data}[storage][used_percent]%)
    ...    Free    : ${data}[storage][free_mb] MB
    ...
    ...    -- Processor / Hardware --
    ...    Hardware/SoC   : ${data}[processor][hardware]
    ...    Model          : ${data}[processor][model]
    ...    Core count     : ${data}[processor][core_count]
    ...    ================================================================================
    Log    ${report}    console=True
    Create Directory    results/evidence
    Create File    results/evidence/njt_etm_platform_report.txt    ${report}

the njt etm device should be reachable and connected
    [Arguments]    ${device_ip}=${current_device}[Ip]
    ${ping}=    ETM: Diagnostics: Njt: Ping Device    ${device_ip}
    Should Be True    ${ping}[reachable]    msg=NJT ETM at ${device_ip} did not respond to ping.
    ETM: Diagnostics: Assert Device Connected
