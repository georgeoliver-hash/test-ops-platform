*** Settings ***
Documentation     Device Function binding keywords specific to Validator devices
Resource          __Resources.robot

*** Keywords ***
### GIVEN ###
the device settings are updated with valid legacy settings data from primary device
    Device: Validator: Function: Update Device Settings    Legacy_data

the device settings are updated with valid initial settings data from primary device
    Device: Validator: Function: Update Device Settings    Init_data

the device settings are updated with valid initial settings data and invalid ${value} from primary device
    Device: Validator: Function: Update Device Settings    Init_data    EnterStop    ${value}

the device settings are updated with valid next stage data from primary device
    Device: Validator: Function: Update Device Settings    Next_stage

the device settings are updated with valid exit stop data from primary device
    Device: Validator: Function: Update Device Settings    Init_data    ExitStop

the device settings are updated with valid travelling settings data from primary device
    Device: Validator: Function: Update Device Settings    Init_data    Travelling

${r:(.* )?}sets invalid ${invalid_keys}
    Device: Validator: Function: Update Device Settings    Update_Settings    EnterStop    ${invalid_keys}

the device's operating mode set to ${opstate} from primary device
    Device: Validator: Function: Update Device Opstate     InService    ${opstate}

the device's service state set to ${opstate} from primary device
    Device: Validator: Function: Update Device Opstate     ${opstate}

reset device's opstate and settings
    Run Keyword If  "${current_device}[Type]"=="BV"    Device: Validator: Function: Update Device Settings    Init_data
    Run Keyword If  "${current_device}[Type]"=="BV"    Device: Validator: Function: Update Device Opstate
    ${vars} =  Create Dictionary  GateMode=Entry
    Run Keyword If  "${current_device}[Type]"=="GV"    Device: Function: Modify Device file     ${current_device}[Paths][PeripheralData]    ${vars}

the device responds with ${service_status} state when primary device requests
    Wait Until Keyword Succeeds  10 sec  1 sec  Device: Validator: Function: Get Device Opstate
    Should Be Equal As Strings    ${service_status}    ${device_opstate}[ServiceStatus]

${r:(.* )?}set${r:(s)?} ${op_mode} mode for GV
    ${gatemode}=   Set VariableIf  "${op_mode}" == "TagOn"   Entry   Exit
    ${vars} =  Create Dictionary  GateMode=${gatemode}
    Device: Function: Modify Device file     ${current_device}[Paths][PeripheralData]    ${vars}

${r:(.* )?}reset${r:(s)?} operating mode for GV
    ${vars} =  Create Dictionary  GateMode=Entry
    Device: Function: Modify Device file     ${current_device}[Paths][PeripheralData]    ${vars}

${r:(.* )?}modifies card control device config to ${actiontype}
   Device: Validator: Function: Modify Card Control Config    ${actiontype}

the device is set to use ${service_name} service and move to ${zone_name}
    Device: Validator: Function: Change Device Service and Zone   ${service_name}    ${zone_name}

### THEN ###
this is a dummy then keyword in TVM functions bindings
    Fail  Not Implemented