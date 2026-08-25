*** Settings ***
Documentation     Keywords for user interactions
Resource   ../Variables/ScreenObjectVariables.robot
Resource   ../Utility/UserInteractionsUtility.robot

*** Keywords ***
${r:(.* )?}click${r:(s)?} on the ${UIbutton} button
    Device: Interactions: Click UI Button   ${UIbutton}   ${False}

${r:(.* )?}click${r:(s)?} on the "${UIbutton}" button
    Device: Interactions: Click UI Button   ${UIbutton}   ${True}

${r:(.* )?}press${r:(es)?} the${r:(.* )?}${key}
    Device: Interactions: Press Key    ${key}

${r:(.* )?}type${r:(s)?} ${text} into ${text_box} text entry
    Device: Interactions: Enter Text  ${text}    ${text_box}

${r:(.* )?}enter${r:(s)?} number ${text}
    Device: Interactions: Press Button Sequence   ${text}

${r:(.* )?}type${r:(s)?} ${text} into the ${box_name} text box
    type into device textbox  ${text}  ${box_name}

${r:(.* )?}click${r:(s)?} the button with text "${UI_button}"
    click device ui button    ${UI_button}