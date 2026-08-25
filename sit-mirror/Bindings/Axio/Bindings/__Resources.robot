*** Settings ***
Documentation     Axio (BV / Validator) bindings — imports the common SIT bindings layer.
...
...               The Axio is notification-driven, but it is still a Validator device and
...               reuses the shared keyword set rather than a bespoke per-screen file:
...                 - screen navigation  → `navigate device to screen <Screen>`, driven by
...                   ScreenFlow/BV/screenflow_map.jsonc (ValidatorNotification actions); and
...                 - screen assertion   → `the <Screen> screen should be displayed`
...                   (Device: Screen: Validate Screen → `device layout matches`).
...               The notification-injection + screen-check that AxioNotificationBindings.robot
...               used to re-implement are exactly those two framework operations, so that
...               file has been removed. Axio-only device primitives (adaptor lifecycle,
...               screenshots) live in Utility/AxioAdaptorUtility.robot.

Resource    ../../Common/Bindings/ScreenBindings.robot
Resource    ../../Common/Bindings/DeviceFunctionBindings.robot
Resource    ../../Common/Bindings/UserInteractionsBindings.robot
Resource    ../../Common/Bindings/SmartcardBindings.robot
Resource    ../../Linux/CDPKeywords.robot
