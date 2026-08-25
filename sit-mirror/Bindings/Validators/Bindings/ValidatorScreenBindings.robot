*** Settings ***
Documentation     Screen binding keywords specific to Validator devices
Resource          __Resources.robot

*** Keywords ***
### GIVEN ###

### WHEN ###

### THEN ###
${r:(.* )?}the ${checkmark} light/sound is configured
    ${checkmark}   Convert To Lowercase   ${checkmark}
    Wait Until Keyword Succeeds   10   1   Device: Validator: Screen: Assert Element In Layout config   ${checkmark}
    Log to Console  \nCheckmark is correct