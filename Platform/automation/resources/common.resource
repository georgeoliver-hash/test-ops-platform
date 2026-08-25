*** Comments ***
# Shared library imports + teardown keyword for every suite in this repo.
#
# Suite Setup/Teardown/Test Setup/Teardown themselves can't live in a Resource
# file in Robot Framework -- they're suite-file-only settings -- so every
# suite still declares these four lines itself:
#
#     *** Settings ***
#     Resource        ${CURDIR}/../../../resources/common.resource   # adjust depth
#     Suite Setup     Connect To Device
#     Suite Teardown  Disconnect From Device
#     Test Setup      Clear Device Logs
#     Test Teardown   Collect Test Artefacts
#
# Suites needing the device UI (Appium/Playwright) additionally do
# `Start Device UI` / `Stop Device UI` as their own Test Setup/Teardown (see
# resources/translink/signon.resource for the pattern), since only some tests
# in a suite need the UI up.

*** Settings ***
Library    Collections
Library    framework.robot.device_library.DeviceLibrary
Library    framework.robot.android_library.AndroidLibrary
Library    framework.robot.bos_library.BOSLibrary
Library    framework.robot.build_data_library.BuildDataLibrary

*** Keywords ***
Collect Test Artefacts
    [Documentation]    Standard Test Teardown: pull device logs, and on
    ...    failure an Android UI dump + screenshot, into ${REPORT_DIR} (set by
    ...    RobotReportListener.start_test). Mirrors the old `transport` fixture
    ...    teardown.
    Collect Device Logs    ${REPORT_DIR}
    Run Keyword If Test Failed    Capture UI State On Failure    ${REPORT_DIR}
