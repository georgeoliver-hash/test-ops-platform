
*** Settings ***
Resource  ../Utility/FunctionsUtility.robot
Resource  ../../../Common/Utility/FileUtility.robot
Library   ../../../Common/CustomLibs/TimeTools.py

*** Keywords ***
### GIVEN ###
the current device has been rebooted
    Log To Console  ---> Rebooting the current device ${current_device}[device_id]...
    Device: Function: Reboot Device

the audit, bos, logs and state has been cleared on the device
    Device: Function: Clean BosRecords, Logs, Audit And State

the device software has been started
    Device: Function: Start Device Software

the device services have been started
    Device: Function: Set: Prepare and Start Device Services

the device staff polling time has been set to ${polling_time} secs and started
    Set Suite Variable    ${polling_time}
    Device: Function: Set: StaffList Polling Time     ${polling_time}

the device's out of hours period is from now to 3 and a half minutes from now
    Device: Function: Set: Out Of Hours Period

the device software has been stopped
    Device: Function: Stop Device Software

the device services have been stopped
    Device: Function: Stop Device Software
    Device: Function: Services Are Not Running

the device services are not running
    Device: Function: Services Are Not Running

the device has been decomissioned
    Device: Function: Set: Uncommissioned

the device has been recomissioned
    Device: Function: Set: Commissioned

the test support service adaptor has been closed
    Log To Console    ---->Closing adaptor
    Device: Function: Close Test Support Service Adaptor

the test support service adaptor has been initiated
    Device: Function: Initiate Test Support Service Adaptor

the device staff list polling time has been set to ${polling_time} seconds
    Set Suite Variable    ${polling_time}
    Device: Function: Set: StaffList Polling Time     ${polling_time}

the devices system files have been downloaded
    Set Suite Variable  ${device_software_tmp}  ${current_temp_dir}/Device_software_temp
    Create Directory  ${device_software_tmp}
    Directory Should Exist  ${device_software_tmp}
    Device: Function: Gather system files  ${device_software_tmp}

the devices software has been forcibly stopped
    Device: Function: Halt software

the devices audit files have been downloaded
    Set Suite Variable  ${device_audits_temp}   ${current_temp_dir}/Device_audits_temp
    Create Directory  ${device_audits_temp}
    Directory Should Exist  ${device_audits_temp}
    Device: WEC: Function: Gather audits  ${device_audits_temp}

the device is moved to map point ${map_point_id} and homelocation ${home_location}
    Device: Function: Set: Map Point and HomeLocation    ${map_point_id}   ${home_location}

${r:(.* )?}wait${r:(s)?} until stafflist gets updated in the device
    Wait Until Keyword Succeeds    260    2   Device: Function: Assert StaffList Get Modified

${r:(.* )?}reset${r:(s)?} date and time in the device
    Device: Function: Re-Set Device Date and Time

${r:(.* )?}set${r:(s)?} device date and time to ${datetime}
    Device: Function: Set Device Date and Time    ${datetime}

${r:(.* )?}send${r:(s)?} force comms request
    Device: Function: Requests Force Comms

${r:(.* )?}add${r:(s)?} ${minutes} minutes to device's current time and set to device
    Device: Function: Add Date and Time and Set to Device     0     ${minutes}    0

${r:(.* )?}set${r:(s)?} passback time to ${passback_time} sec in products data source
    Device: Function: Set: PassbackTime in RuleProperties of FareProducts database     ${passback_time}

the device downloads and stores new manifest from BOS within ${wait_time} seconds
    Wait Until Keyword Succeeds    ${wait_time}    2    Device: Function: Assert Manifest Get Modified

the ${product_name} product is disabled in the device
    Device: Function: Disable Product    ${product_name}

${r:(.* )?}set${r:(s)?} workday and time ${time} to the device
     Device: Function: Set Workday and Time    ${time}

the device has set up to ${exp_service} service
    ${working_homelocation_list}    SQLite: FaresTopology: Services: Get HomeLocation for the Service    ${exp_service}
    ${cur_loc_details}   Device: Function: Get Device Location Parameters
    ${service_check}     Run Keyword And Return Status  List Should Contain Value  ${working_homelocation_list}   ${cur_loc_details}[HomeLocation]
    Return From Keyword If     ${service_check}
    Device: Function: Stop Device Software
    Device: Function: Change Device Service     ${working_homelocation_list}[0]
    Device: Function: Start Device Software

the device has set up to ${exp_service} service and defalut location settings
    ${working_homelocation_list}    SQLite: FaresTopology: Services: Get HomeLocation for the Service    ${exp_service}
    ${cur_loc_details}   Device: Function: Get Device Location Parameters
    ${service_check}     Run Keyword And Return Status  List Should Contain Value  ${working_homelocation_list}   ${cur_loc_details}[HomeLocation]
    ${stop_check}     Run Keyword And Return Status  Should Be Equal As Strings  ${current_device}[stop_id]   ${cur_loc_details}[StopId]
    Return From Keyword If   '${service_check}'=='True' and "${stop_check}"=="True"
    Device: Function: Stop Device Software
    Device: Function: Change Device Location Parameters     ${working_homelocation_list}[0]    ${current_device}[stop_id]
    Device: Function: Start Device Software

### WHEN ###
the device services are started
    Device: Function: Start Device Software
    Log To Console  ---> Device ${current_device}[device_id] services have been started

### THEN ###
the token stored on the device matches token in the system
    the device registration details should be in the system
    Log To Console  ---> Ensuring token "${current_system_device_token}" is available on device ${current_device}[device_id]...
    Wait Until Keyword Succeeds  100  1s   Device: Function: Assert Device Token
    Log To Console  ---> Successfully found token "${current_system_device_token}" used by device

the device does not contain the token in any of its system files
#    the device registration details should be in the system
    ${device_software_tmp} =  Use  ${current_temp_dir}/Device_software_tempp
    Create Directory  ${device_software_tmp}
    Directory Should Exist  ${device_software_tmp}
    Device: Function: Gather system files  ${device_software_tmp}
    Log  Temporarily disabling logging
    ${logLevel} =  BuiltIn.Set Log Level  NONE
    ${found} =  Files: Search directory for content  ${device_software_tmp}  ${current_system_device_token}
    BuiltIn.Set Log Level  ${logLevel}
    Log  ${found}
    Should Be Empty  ${found}  msg=Device token found in filesystem!
    Files: Delete directory  ${device_software_tmp}

the device services are running
    Log To Console  ---> Polling device services to ensure running on ${current_device}[device_id]...
    Device: Function: Services Are Running
    Log To Console  ---> Device ${current_device}[device_id] services are running

the device services continue to run during a period of ${end_timeout}
    Run Keyword And Expect Error    Beep    

the device's current state should be ${exp_state} within ${seconds} seconds
    Wait Until Keyword Succeeds    ${seconds} s   2 s   the device's current state should be ${exp_state}

the device's current state should be ${exp_state}
    ${device_current_state}=    Device: Function: Gather Device State
    Should Be Equal As Strings    ${device_current_state}    ${exp_state}

the device's current state should not be ${exp_state}
    ${device_current_state}=    Device: Function: Gather Device State
    Should not Be Equal As Strings    ${device_current_state}    ${exp_state}
    ${cf_state}=    Set Variable IF    '${device_current_state}'=='OutOfService'    Out Of Service    ${device_current_state}
    Set Test Variable   ${exp_cf_state}    ${cf_state}
