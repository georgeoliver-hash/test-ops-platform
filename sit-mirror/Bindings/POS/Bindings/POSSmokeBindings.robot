*** Settings ***
Documentation     Given/When/Then steps for POS smoke checks — is the app installed, is it the
...               expected version, is a given background process alive. Mechanically the
...               same checks as George Oliver's test_pos_app_installed.robot and
...               test_pkn_daemon_running.robot from the POS-handover package, re-platformed
...               onto SIT's "run command on device" primitive instead of raw ADB.
Resource          ../Utility/POSInteractionUtility.robot

*** Keywords ***
the flowbird pos app should be installed
    ${installed}=    POS: Is Package Installed
    Should Be True    ${installed}
    ...    msg=${current_device}[appPackage] is not installed on ${current_device}[device_id]

the installed pos app version should be ${expected_version}
    ${version}=    POS: Package Version
    Should Be Equal As Strings    ${version}    ${expected_version}
    ...    msg=Installed POS app version does not match the expected version

the ${process_name} process should be running
    ${running}=    POS: Is Process Running    ${process_name}
    Should Be True    ${running}    msg=${process_name} is not running on ${current_device}[device_id]
