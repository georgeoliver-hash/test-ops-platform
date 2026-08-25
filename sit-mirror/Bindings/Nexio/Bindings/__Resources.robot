*** Settings ***
Documentation     Nexio bindings — imports the common SIT bindings layer plus
...               Nexio-specific BDD step files (FLU workflow, driver menu, sign-on).
...               Common bindings provide device-agnostic step keywords.
...               Nexio bindings provide ETM/FLU-specific step keywords.

Resource    ../../Common/Bindings/ScreenBindings.robot
Resource    ../../Common/Bindings/DeviceFunctionBindings.robot
Resource    ../../Common/Bindings/UserInteractionsBindings.robot
Resource    ../../Common/Bindings/SmartcardBindings.robot
Resource    ../../Linux/CDPKeywords.robot
Resource    ../../ETM/Bindings/ETMScreenBindings.robot
Resource    NexioFLUBindings.robot
Resource    NexioWorkflowBindings.robot
Resource    NexioSignOnBindings.robot
