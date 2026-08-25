*** Settings ***
Documentation     Contains keywords for the Smartcard REST interface.
Library           Collections
Library           OperatingSystem
Library           REST
Library           XML

*** Keywords ***

${r:(.* )?}selects a random ${cardType} smartcard
    @{files}=    Get Smartcard Files list  ${cardType}
    ${max}=    Get Length    ${files}
    ${max}=    Evaluate    ${max}-1
    ${file}=    A random number between 0 and ${max} is generated
    ${file}=    Set variable    @{files}[${file}]
    Device: Simulators: Present a smartcard to the PV    ${cardType}    ${file}
    Log many    ${file} selected from ${cardType}
    ${CARDDIR}=    Set variable    ${cardType}
    ${CARDFILE}=    Set variable    ${file}
    Set test variable    ${CARDDIR}
    Set test variable    ${CARDFILE}

${r:(.* )?}tries to validate the smartcard within the passback period
    Sleep    5 sec
    Device: Simulators: Read the updated smartcard
    Device: Simulators: Remove the Smartcard
    POST    http://${remoteServerName}:9087/SmartCardServiceRemoteHost/1.0/SmartcardXml    {"ImageXml": "${UpdatedCard}"}    validate=false
    Sleep    2s

${r:(.* )?}selects a ${journeysBalance} Journeys Multi Journey smartcard
    ${SCARD}=    Split String From Right    ${CURDIR}    Tests    1
    ${SCARD}=    Set variable    ${SCARD}[0]
    ${SCARD}=    Set variable    ${SCARD}\\Testdata\\Smartcards\\${CONFIG}
    ${FileLocation}=    Join Path    ${SCARD}    Boundaries
    @{files}=    List Files In Directory    ${FileLocation}    *${journeysBalance} Journeys*.xml
    ${max}=    Get Length    ${files}
    ${max}=    Evaluate    ${max}-1
    ${file}=    A random number between 0 and ${max} is generated
    ${file}=    Set variable    @{files}[${file}]
    Device: Simulators: Present a smartcard to the PV    boundaries    ${file}
    ${BALANCE}=    Set variable    ${journeysBalance}
    Set test variable    ${BALANCE}
    Log many    ${file} selected from ${journeysBalance}
    ${CARDDIR}=    Set variable    ${journeysBalance}
    ${CARDFILE}=    Set variable    ${file}
    Set test variable    ${CARDDIR}
    Set test variable    ${CARDFILE}

${r:(.* )?}selects a ${folder}, ${card} smartcard
    ${SCARD}=    Split String From Right    ${CURDIR}    Tests    1
    ${SCARD}=    Set variable    ${SCARD}[0]
    ${SCARD}=    Set variable    ${SCARD}\\Testdata\\Smartcards\\${CONFIG}
    ${FileLocation}=    Join Path    ${SCARD}    ${folder}
    @{splitVar}=    Split string    ${card}    ${SPACE}
    : FOR    ${num}    IN RANGE    1
    \    Run keyword if    '@{splitVar}[0]'!='time'    Exit for loop
    \    @{iLink}=    List Files In Directory    ${FileLocation}    *iLinkZone[1234]*.xml
    \    @{bvp}=    List Files In Directory    ${FileLocation}    *BelfastVisitorPass*.xml
    \    @{files}=    Combine Lists    ${iLink}    ${bvp}
    : FOR    ${num}    IN RANGE    1
    \    Run keyword if    '@{splitVar}[0]'!='daylink'    Exit for loop
    \    @{files}=    List Files In Directory    ${FileLocation}    *Daylink*.xml
    : FOR    ${num}    IN RANGE    1
    \    Run keyword if    '@{splitVar}[0]'=='time' or '@{splitVar}[0]'=='daylink' or '@{splitVar}[0]'=='free'    Exit for loop
    \    ${card}=    Replace string    ${card}    multi journey    MJ
	\    @{files}=    List Files In Directory    ${FileLocation}    *${card}*.xml
    : FOR    ${num}    IN RANGE    1
    \    Run keyword if    '@{splitVar}[0]'=='time' or '@{splitVar}[0]'=='daylink' or '@{splitVar}[0]'=='multi'    Exit for loop
    \    ${card}=    Replace string    ${card}    free    SmartPass
	\    @{files}=    List Files In Directory    ${FileLocation}    *${card}*.xml
    ${file}=    Set variable    @{files}[0]
    Device: Simulators: Present a smartcard to the PV    ${folder}    ${file}
    Log many    ${file} selected from ${folder}
    ${CARDDIR}=    Set variable    ${folder}
    ${CARDFILE}=    Set variable    ${file}
    Set test variable    ${CARDDIR}
    Set test variable    ${CARDFILE}

${r:(.* )?}tries to validate the smartcard after the passback period
    Sleep    1m5s
    Device: Simulators: Read the updated smartcard
    Device: Simulators: Remove the Smartcard
    POST    http://${remoteServerName}:9087/SmartCardServiceRemoteHost/1.0/SmartcardXml    {"ImageXml": "${UpdatedCard}"}
    Sleep    2s

