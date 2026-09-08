### TIBU-22311 [Technical Story] (Closed)
Port Open Payment functionality from Edinburgh Trams

Edinburgh Trams have developed functionality on their Android Axio4 PV to perform open payment taps using deny list functionality and send audit for them to the back office.

As a baseline for Translink open payment functionality it would be good to reuse what Edinburgh Trams have done as much as possible bearing in mind that the Translink PV is an Axio4S on WEC2013.

Ultimately the sort of functionality we’d like to port across is:

* PCA application handling (i.e. updates through TMS)
* Ability to tap an open payment card
* Ability to download and apply deny lists to the FEIG (full and delta)
* Validation of card taps on FEIG (i.e. checking on the deny list, expired, ODA checks, etc.)
* Auditing of Tap On Tap Off taps (useful for the future so might as well pull it in now)



---
### TIBU-22312 [Technical Story] (System Test)
Port pilot list functionality from SRUP

On SRUP pilot list functionality was developed to allow testing of ABT in the live environment. We would like this to be ported into the Translink PV solution (ultimately we’ll want this on the GV too in the future so if that can be taken into account that would be great).

The pilot list functionality should allow you to:

* Control whether pilot lists are enabled using TMS
* Put the PV into a mode (registration mode) where it accepts cEMV taps to create a pilot list and sends that list up to CloudFare using the device logging mechanism
* Put the PV into a mode whereby it uses the pilot list defined in TMS and only accepts cEMV card taps from cards on that list.

Note that for the Translink pilot list it should use the FEIG token as opposed to the ICC token. To enable this to be possible, the PilotListConverter tool developd by Pul Brine will need to be updated also to allow longer tokens to be converted as the FEIG tokens are longer than the ICC tokens.'

The full process is described in the below document:

<custom data-type="smartlink" data-id="id-0">https://docs.google.com/document/d/13fuobWNc0LyDldRoUuj5S1AQWh-v50ZNfKcJ01LnvnY/edit?usp=drive_link</custom> 

---
### TIBU-24196 [Technical Story] (Closed)
Implement TOO for Glider PV

(no description)

---
### TIBU-22316 [Story] (Closed)
As a Translink back office user I would like to be able to update software on the PV FEIG through the back office

On the PV there are 3 pieces of software that relate to the FEIG:

* Transparent application
* PCA application
* FEIG OS

In addition, the TID and TK must be able to be update on the FEIG from the PV Device group in TMS

All of these need to be able to be updated from the back office should the need arise

---
### TIBU-22317 [Story] (Closed)
As a Translink financial officer I would like the PV to be capable of downloading and applying deny lists and BIN lists

In order to mitigate financial risk on the PV while accepting payment taps the PV must download deny and BIN lists that can be used during validation of the payment media to determine if they are allowed to travel. Requirements around this are:

* At (or soon after - within 15 minutes) the End of Day time configured in TMS, the PV should download and apply a new BIN list from the back office to the FEIG
* At (or soon after - within 15 minutes) the End of Day time configured in TMS, the PV should download and apply a new full Deny list from the back office to the FEIG
* If the full deny list download/application fails for any reason then the PV should retry downloading and applying a full deny list to the FEIG every 15 minutes until it succeeds
* After the full deny list has successfully been downloaded and applied, the PV should check for delta updates to the deny list every 15 minutes and apply them to the FEIG if one is available



---
### TIBU-22318 [Story] (Closed)
As a Translink back office user I would like the PV to be able to be updated remotely to a cEMV capable software build

By the time the Glider Tap On Only PV software goes live we expect the PVs to be on version 3.1.0 of the software at a minimum. Field services are going through an exercise of upgrading the PV heads to V2 FEIGs that use FEIG OS cS02.01.00-51.54-2-2 and Transparent App 02.01.12. These will not have a PCA application on them.

We would like to be able to be sure we can upgrade from FEIGs in this state remotely to the necessary versions of FEIG OS, Transparent application and PCA application without having to visit all of the PVs.

This should also include setting the TID and TK from the PV device group in TMS.

---
### TIBU-22319 [Story] (Closed)
As a Translink ticketing manager I would like to ensure the PV only accepts cEMV taps if the right conditions are met

Similar to the ETM, the PV should only enable cEMV taps if the following conditions are met:

* Route attribute check - The ABT Type route attribute for the first route related to the home location of the device (“Glider (Metro)” for the case of the Glider PV) in the database has multiple options:

    * “Tap On Only (Flat Fare)” - cEMV taps should be **enabled** and a tap will result in a **JourneyTap** audit record going to CloudFare later on
    * “Tap On Tap Off” - cEMV taps should be **enabled** and a tap will result in a **TotoTap** audit record going to CloudFare later on (whilst we are not focusing on TOTO yet, the Ed Trams PV is TOTO so to make use of the audit code for ET it would be good to put this case in for now)
    * Any other values for this attribute should result in cEMV taps being **disabled**.
    
* Location check - The boarding location of the PV must be within the configured zone from TMS (expected to be the “Metro Network Zone”) for cEMV taps to be **enabled** - a new TMS parameter called “Glider Tap On Only Zone” will be added for this that contains a zone number. If the boarding location is not in the configured zone then cEMV taps are **disabled**.
* Fare check - A fare is available for the first “ABT Tap On Only” product in the database (note that Translink only have a single product that matches this called “ABT Product”) for cEMV taps to be **enabled**. If the returned fare is invalid then cEMV taps are **disabled**.

In addition, cEMV taps should be disabled if the PV is in the technician menu

---
### TIBU-22322 [Story] (Closed)
As a Translink ticketing manager I would like to cEMV taps to be rejected by the PV in the right cases

Similar to the ETM, the PV should reject cEMV taps if one of the following conditions are met:

* If the card is not read successfully then an error screen should be displayed (see screen 1.6.3 in UX) - no audit is raised for this
* If the card is not from a valid scheme (only valid ones are Visa, Mastercard, Maestro) then an error screen should be displayed (see screen 1.6.2 in UX) - no audit is raised for this
* If the card has expired then an error screen should be displayed (see screen 1.6.2 in UX) - an audit record should be raised for this with a declined reason of 1 (Expired)
* If the card fails ODA (Offline Data Authentication) checks then an error screen should be displayed (see screen 1.6.2 in UX) - an audit record should be raised for this with a declined reason of 3 (Declined)
* If the card BIN is on the BIN list then an error screen should be displayed (see screen 1.6.2 in UX) - an audit record should be raised for this with a declined reason of 15 (On BIN List)
* If the card token is on the Deny list then an error screen should be displayed (see screen 1.6.2 in UX) - an audit record should be raised for this with a declined reason of 2 (On Deny List)
* If the card has already been tapped within the passback time (configured from TMS - parameter called “ABT Passback” - configured in seconds) then an error screen should be displayed (see screen 1.6.6 in UX) - an audit record should be raised for this with a declined reason of 20 (Passback)

These error screens will timeout back to the main screen after 3 seconds.

If another card or barcode is presented to the PV whilst this screen is displayed then that card/barcode should be validated using the normal flow.

PV UX: [https://overflow.io/s/9LR2K30N/?node=afc506ae](https://overflow.io/s/9LR2K30N/?node=afc506ae)

---
### TIBU-22323 [Story] (Closed)
As a Translink ticketing manager I would like a success screen to be displayed if all validation checks passed

In the case that all of the validation checks pass then a successful ABT tap screen should be displayed (see 1.6.1.1 in UX). This will timeout back to the main screen after 2 seconds.

If another card or barcode is presented to the PV whilst this screen is displayed then that card/barcode should be validated using the normal flow.

PV UX: <custom data-type="smartlink" data-id="id-0">https://overflow.io/s/4860R82E/?node=8afaddd7</custom> 

---
### TIBU-28098 [Story] (Ready for Release)
As a back office user I'd like the auditing for a TOTO tap to be correct

If the ABT Type route attribute is set to “Tap On Tap Off” then cards are validated as per the same rules as Glider TOO but the auditing must follow the structure defined in the attached Translink ABT Audit Specification document (section 3.2 - NIR PV). Most notable is that there is a TotoTap structure within the audit instead of a JourneyTap structure. Within these structure a lot of the fields are the same but there are a small number of differences.

---
### TIBU-28386 [Story] (Ready for Release)
As a back office user I'd like a transaction to be sent to MERIT every 24 hours as a heartbeat on PV

Arrive will support this request by creating a paper ticket transaction record on a PV and GV under the following conditions:

1. When the PV or GV enters an in-service state
2. Periodically, every 24 hours

Note that for 1. above, this will be for all scenarios where the PV or GV enters an in-service state. This includes after an automatic or manual (via Technician Menu or CF remote reboot), after a technician has signed out when the PV or GV returns to an in-service state, and when returning to an in-service state after temporarily taking itself automatically out of service.

  
Note that for 2. above, this is to cover the potential (although unlikely) scenario where the daily reboot for a PV or GV is disabled via TMS configuration. A 24 hour timer will be enabled when the PV or GV software goes into an in-service or forced out of service state. If a 24 hour timer is already enabled, then the timer will be reset. When the  
timer elapses, a paper ticket transaction record will be created, and the timer reset. This approach means that typically the timer will not trigger because it will be reset during the daily reboot or during a transition to an in-service state, however it ensures that a paper ticket transaction is created at least every 24 hours.  

Note as mentioned above, the 24 hour timer will only be enabled where a PV or goes into an in-service state, or into a forced out of service state (i.e. remote out of service command). The timer will not be enabled if the PV or GV is in an out of service state due to an error – this is because it is expected that a PV or GV that has been unexpectedly  
out of service for an extended period of time is just as important a device to visit as a PV or GV that is not communicating.  

Configuration of the product class to use for the paper ticket transaction will be managed through a new TMS setting that will be added for the PV and GV devices under “4 – Device Settings”. The new TMS setting will be called “Comms Product Name” and will be a string that will contain the product class name. Following the example provided by Translink in this CR, it will be set to “Val Startup”.  

The product will be configured within CloudFare with the following:

* Preset Product

    * Product Description = “Val Startup”
    
* Audit

    * Annul Allowed = No
    * Count As Passenger = No
    * Count As Pass = No
    
* Reference

    * Reference ID = 1999
    * MERIT Default Alighting Stage = 98 For Example
    
* No Ticket will be assigned to the product

  
Note that if Translink require a different alighting stage for Glider and NIR, then two products would require  
creating in CF, “Val Startup NIR” and “Val Startup GL” for example, and the appropriate product set for the  
“Comms Product Name” specified in the TMS dataset. The Reference ID can still be set to be the same for  
both products. If multiple products are required, then it is important to ensure that only one of these products has  
“Merit Synchronisation” set to Yes.

  
Note that although the CR requests an artificial smartcard tap transaction, the implementation will instead use a  
preset product. This is because this type of transaction is more suitable, as it does not require generating dummy  
smartcard data such as the ESN and PSN.

  
When the PV or GV enters an in-service state, or when the 24 hour timer elapses, a new business rule will be run by  
the PV to issue the paper ticket transaction that will:

* Audit the preset product paper transaction
* Set the transaction value to 0
* Set the Boarding Stage to the stage configured on the PV or GV
* Set the Route as per the route configured on the PV or GV
* The PV or GV will NOT display any success message and will NOT emit a success tone: the transaction will be  
  performed silently
* Place the audit record into the audit queue to be uploaded to CloudFare, which will in turn send on the  
  audit record to Merit



---
### TIBU-21950 [Bug] (Ready for Release)
Barcodes & Cards not accepted banners don't match UI Spec

The banners displayed on the bottom of the idle screen when either the Barcode Scanner or Smartcard Reader are disconnected, do not currently match the spec 

 

![](blob:https://media.staging.atl-paas.net/?type=file&localId=null&id=5273586a-2b14-40b6-9230-244c95f2b0e6&&collection=&height=4080&occurrenceKey=null&width=3072&__contextId=null&__displayType=null&__external=false&__fileMimeType=null&__fileName=null&__fileSize=null&__mediaTraceId=null&url=null)
![](blob:https://media.staging.atl-paas.net/?type=file&localId=null&id=84f10ed3-c6aa-48bb-aa38-63b22eafb883&&collection=&height=4080&occurrenceKey=null&width=3072&__contextId=null&__displayType=null&__external=false&__fileMimeType=null&__fileName=null&__fileSize=null&__mediaTraceId=null&url=null)
 Spec: <custom data-type="smartlink" data-id="id-0">https://overflow.io/s/SO7Q4QNZ/?node=ed08d60e</custom>  

---
### TIBU-24428 [Bug] (Ready for Release)
TL PV "PrimaryCommsChannelFailed" event spamming seen in CF on build 3.1.1 in TL Test Environment

We have an apparent issue with the 3.1.1 PV build reported by Translink when testing in their test environment, where it is frequently “spamming” CF with the “PrimaryCommsChannelFailed” event, suggesting that the PV is frequently flipping between ethernet and cellular.   
  
We do not see the same issues in our own Poole test environment, so this may be a pointer that the issue is a Translink network problem.  
  
TL have reported that they do not see the spamming if the cellular SIM is removed from the PV, and the PV will continue to communicate over ethernet with no “PrimaryCommsChannelFailed” event spamming. At face value this is odd, but it may simply be another indication of a poor network, and the lack of any “PrimaryCommsChannelFailed” event spamming in this scenario may be simply because we have no secondary comms channel to fail over to with the SIM removed.  
  
DEBUG logs have been attached along with a screenshot of the event spamming to better direct investigation.  
  
Some possible points of interest within the logs:  
  
**Failed to send an audit record, and then 5 seconds later failed over to cellular (GFTS.log1.txt):**  
  
2025-07-07 14:02:00.771 WARN \[BackOfficeAgent\] - BOSRecordHandler batch send ended - send failure \\SD Memory\\GFTS\\BOSRecords\\000000\\00000060.evt  
2025-07-07 14:02:05.710 INFO \[NetworkConfiguration\] - \[Network Route\] Monitor Route: Adaptor FEC1, Route backofficeprimary, available False  
  
**Modem IP Comparison Oddity:**  
  
2025-07-07 14:02:07.595 DEBUG \[NetworkConfiguration\] - ConnectionState: OS IP 10.100.211.23 and Modem IP 100.103.117.238 do not match  
2025-07-07 14:02:07.596 DEBUG \[NetworkConfiguration\] - ConnectionState: OS IP 100.103.117.238 and Modem IP 100.103.117.238 match  
  
The above maybe normal, it is logged often. It looks like it is first comparing the IP address of the ethernet with the Modem IP and finding they don’t match (as expected) but on the very next line after it does correctly match the Modem IP so this is probably nothing to be concerned about?  
  
**Exception:**  
  
2025-07-07 14:02:05.694 WARN \[NetworkConfiguration\] - \[NetworkRouteDestinationClient\] SendWebRequest WebException: Error while processing request./jikdl.atufc: Error while processing request. ---> System.Net.Sockets.SocketException: A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond

  
The above exception seems to be what is consistently aligning with when we raise the PrimaryCommsChannelFailed “set” event and fail over to cellular.  
  
**NOTE: The screenshot added of CF is showing “pairs” of the PrimaryCommsChannelFailed” event which is not immediatley obvious from the screenshot. the PrimaryCommsChannelFailed event is a set/clear event.**

---
### TIBU-25446 [Bug] (System Test)
TL PV - "spamming" of FEIG Manifest requests in the log file at least every second

Similar to an issue we had on the GV (fixed in TIBU-22904) , the PV is constantly requesting a FEIG manifest far too often (every 1 second) despite there being no manifest for the FEIGs. This causes not only lots of noise in the log, but also unnecessary strain on the CF back office.  
  
Similar changes that were made on the GV need to be made to the PV, ensuring the manifest is requested at a more sensible frequency (for example every 15 mins).  
  
See log attached for example PV with lots of FEIG manifest spamming

---
### TIBU-25691 [Bug] (Closed)
EMV Taps disabled for Glider PV

Discovered on build **1.1.962.17108**  
  
FEIG Versions - PCA - **79**, Trans - **79**, Firmware - **cD02.01.00-00.70-2-2**  
  
  
EMV taps are not being detected with this build and my current device setup, The open payment service logs a “PollSocket: x bytes” message every few seconds but there is no response from the device on screen or in the logs when an EMV card is presented.   
  
Open Payment debug logs initially show the FEIG as “connected” and then it enters an “update settings” state, it seems to perform the update and then can no longer (or doesn’t attempt to) enable EMV taps after that:  
  
2025-09-08 10:57:30.000 DEBUG \[OpenPayment\] - FeigLoop InLock BIGdelta 32225 State Connected etime 32225 count 2  
2025-09-08 10:57:30.017 DEBUG \[OpenPayment\] - ---> Sending   Tag 7F818107  Len 0   Full TLV  
7F81810700  
2025-09-08 10:57:30.032 DEBUG \[OpenPayment\] -  sendPoll \_socket Hash 0x72191D0AspTo=85000000  
2025-09-08 10:57:30.033 DEBUG \[OpenPayment\] - sendSend  
2025-09-08 10:57:30.034 INFO \[OpenPayment\] - PollSocket: Sent 5 bytes.  
2025-09-08 10:57:30.035 DEBUG \[OpenPayment\] - ETLV HBcount 0 PollReceiveTLV next  
2025-09-08 10:57:30.036 DEBUG \[OpenPayment\] - ETLV other TLV  
2025-09-08 10:57:30.147 DEBUG \[OpenPayment\] - FRT CO: FWver cD02.01.00-00.70-2-2   PCAVersion: 0201230079 DeviceId: 17F13BDA TerminalId: 99963322 OS Config:  
2025-09-08 10:57:30.148 DEBUG \[OpenPayment\] - Reader changed from state Connected to state UpdatingSettings  
2025-09-08 10:57:30.149 INFO \[OpenPayment\] - \[OnPaymentDeviceVersionsCollected\] Versions collected from Payment Device  
2025-09-08 10:57:30.681 WARN \[SmartCard\] - \[FeigTcpClientHandler\] ResetConnection()  
2025-09-08 10:57:30.682 INFO \[SmartCard\] - \[FeigReader\] Connection state changed to Disconnected  
2025-09-08 10:57:30.683 INFO \[SmartCard\] - \[FeigTcpClientHandler\] ResetConnection() - connection reset completed  
2025-09-08 10:57:30.689 INFO \[SmartCard\] - \[FeigReader\] Connection state changed to Connected  
2025-09-08 10:57:31.000 DEBUG \[OpenPayment\] - FeigLoop InLock BIGdelta 1202 State UpdatingSettings etime 33427 count 3  
2025-09-08 10:57:31.001 INFO \[OpenPayment\] - FRT US: DT  
2025-09-08 10:57:31.002 DEBUG \[OpenPayment\] - ---> Sending   Tag 7F818115  Len 12   Full TLV  
7F8181150C5F8181230720250908105731  
2025-09-08 10:57:31.003 DEBUG \[OpenPayment\] -  sendPoll \_socket Hash 0x72191D0AspTo=85000000  
2025-09-08 10:57:31.004 DEBUG \[OpenPayment\] - sendSend  
2025-09-08 10:57:31.005 INFO \[OpenPayment\] - PollSocket: Sent 17 bytes.  
2025-09-08 10:57:31.006 DEBUG \[OpenPayment\] - ETLV HBcount 0 PollReceiveTLV next  
2025-09-08 10:57:31.569 DEBUG \[OpenPayment\] - ETLV other TLV  
2025-09-08 10:57:31.570 INFO \[OpenPayment\] - FRT US: DT set  
2025-09-08 10:57:31.571 DEBUG \[OpenPayment\] - Reader changed from state UpdatingSettings to state TapDisabled  
2025-09-08 10:57:31.572 INFO \[OpenPayment\] - FRT US: ECP=False do send  
2025-09-08 10:57:31.573 DEBUG \[OpenPayment\] - ---> Sending   Tag 7F81812B  Len 24   Full TLV  
7F81812B185F81814E01015F81814F0D6A02C80100030BAD7800000000  
2025-09-08 10:57:31.574 DEBUG \[OpenPayment\] -  sendPoll \_socket Hash 0x72191D0AspTo=85000000  
2025-09-08 10:57:31.575 DEBUG \[OpenPayment\] - sendSend  
2025-09-08 10:57:31.576 INFO \[OpenPayment\] - PollSocket: Sent 29 bytes.  
2025-09-08 10:57:31.577 DEBUG \[OpenPayment\] - ETLV HBcount 0 PollReceiveTLV next  
2025-09-08 10:57:31.584 INFO \[OpenPayment\] - FRT US: ECP gen err  
2025-09-08 10:57:31.695 DEBUG \[OpenPayment\] - FeigLoop InLock BIGdelta 733 State TapDisabled etime 34160 count 4  
2025-09-08 10:57:33.000 DEBUG \[OpenPayment\] - FeigLoop InLock Tick 34783 State TapDisabled etime 34783 count 10  
  
  
Full log:  

---
### TIBU-26048 [Bug] (System Test)
PV - Device fails to perform Feig update via TMS 

PV 3.1.2.15214

Device fails to perform Feig update via TMS. I have send down new versions of Smartcard PCA Application, Smartcard Reader Firmware, and Smartcard Transparent Application within a TMS dataset and then deployed that dataset down to the Feig’s device ID which in this case was 17F138C2. It appears that the device never tries to download a manifest for the Feig update, I would if the download had started I would of expected to see a FeigUpdate folder within the State folder but this was not present on my device. Another thing worth noting is that in the logs I am not seeing the device ID of Feig which previously could be commonly found when checking the device logs.

Expected Result:

TMS Feig update is successful on the PV

Actual Result:

TMS Feig update is unsuccessful on the PV

Logs:

![](blob:https://media.staging.atl-paas.net/?type=file&localId=null&id=7be909cb-e36e-494e-befe-cafe14794790&&collection=&height=null&occurrenceKey=null&width=null&__contextId=null&__displayType=null&__external=false&__fileMimeType=null&__fileName=null&__fileSize=null&__mediaTraceId=null&url=null)‌

---
### TIBU-26303 [Bug] (System Test)
PV V3.1.2 - Missing Network Interface screen is displayed when trying to access Network Setting on Technician Menu

PV v3.1.2

Missing Network Interface screen is displayed when trying to access Network Setting on Technician Menu. 

![](blob:https://media.staging.atl-paas.net/?type=file&localId=null&id=a0d5c0f9-9120-40f7-9226-948017095a40&&collection=&height=566&occurrenceKey=null&width=785&__contextId=null&__displayType=null&__external=false&__fileMimeType=null&__fileName=null&__fileSize=null&__mediaTraceId=null&url=null)
Both ethernet and SIM were both connected when I left it yesterday afternoon but getting some 'PrimaryCommsChannelFailed' events in CF 

![](blob:https://media.staging.atl-paas.net/?type=file&localId=null&id=9ce30405-b672-42d8-b1f1-7f5fae38992d&&collection=&height=570&occurrenceKey=null&width=1768&__contextId=null&__displayType=null&__external=false&__fileMimeType=null&__fileName=null&__fileSize=null&__mediaTraceId=null&url=null)
I have had to hard reboot the PV and it is showing both ethernet and Sim connected.

![](blob:https://media.staging.atl-paas.net/?type=file&localId=null&id=eb4fed56-39b7-4a22-a93e-700dd0415825&&collection=&height=440&occurrenceKey=null&width=732&__contextId=null&__displayType=null&__external=false&__fileMimeType=null&__fileName=null&__fileSize=null&__mediaTraceId=null&url=null)
Expected Result:

Network Setting page is displayed with the page showing both Ethernet and cellular connected

Actual Result:

Missing Network Interface screen is displayed

Logs:

![](blob:https://media.staging.atl-paas.net/?type=file&localId=null&id=e225b69c-765b-4701-a197-b1543105d371&&collection=&height=null&occurrenceKey=null&width=null&__contextId=null&__displayType=null&__external=false&__fileMimeType=null&__fileName=null&__fileSize=null&__mediaTraceId=null&url=null)‌

---
### TIBU-26522 [Bug] (System Test)
PV DEV BUILD Glider TOO - After performing Feig update the device fails to detect EMV cards

**PV 1.1.972.17167**

**Original Feig Versions:**

 Smartcard PCA Application - Not Available

Smartcard Reader Application Version - 020112

Smartcard Reader Firmware Version - cD02.01.00-00.39-2-2

**Original Feig Versions:**

Smartcard PCA Application - 0201230079

Smartcard Reader Application Version - 020179

Smartcard Reader Firmware Version - cD02.01.00-00.70-2-2

The versions were updated via the Deployment Manager tool due to another issue where the device cannot perform Feig updates via TMS. On boot up after updating the Feig the device takes a few minutes to go into service, the Feig is able to successfully read smartcard. However when presenting an EMV card to the device, the device is not responsive.

**Expected Result:**

Device is able to read/detect EMV cards after Feig update while running Glider TOO development build

**Actual Result:**

 Device isn’t able to read/detect EMV cards after Feig update while running Glider TOO development build

**Logs:**

![](blob:https://media.staging.atl-paas.net/?type=file&localId=null&id=3bd4fbe3-3b02-4cab-81f9-49b53b1e63ea&&collection=&height=null&occurrenceKey=null&width=null&__contextId=null&__displayType=null&__external=false&__fileMimeType=null&__fileName=null&__fileSize=null&__mediaTraceId=null&url=null)‌

---
### TIBU-26531 [Bug] (Closed)
PV DEV BUILD Glider TOO - Two sets of Feig versions are displayed in Asset Manager for the device

**PV 1.1.972.17167**

Two sets of Feig versions are displayed in Asset Manager for the device, one with Version on the end of the description and one without. The older version displayed is the version with ‘Version’ in the description.

![](blob:https://media.staging.atl-paas.net/?type=file&localId=null&id=9712e3a8-df72-4cfe-b644-5480c5c79003&&collection=&height=221&occurrenceKey=null&width=362&__contextId=null&__displayType=null&__external=false&__fileMimeType=null&__fileName=null&__fileSize=null&__mediaTraceId=null&url=null)
**Expected Result:**

Only one version of the Feig Versions is displayed in Asset Manager for the device

**Actual Result:**

Two versions of the Feig Versions are displayed in Asset Manager for the device

**Logs:**

![](blob:https://media.staging.atl-paas.net/?type=file&localId=null&id=711aeed6-b1ff-42b4-9a9c-0205b9108f39&&collection=&height=null&occurrenceKey=null&width=null&__contextId=null&__displayType=null&__external=false&__fileMimeType=null&__fileName=null&__fileSize=null&__mediaTraceId=null&url=null)‌

---
### TIBU-27289 [Bug] (System Test)
PV > No event for barcode reader dropouts

Version: v3.1.2 (NIR)

Actual: Unlike the GV there is no event that triggers when there is a barcode reader dropout on the PV

Expected: An event should trigger when the barcode reader drops out (much like GV)

Steps:

1. Simulate a barcode reader dropout by disconnecting the barcode reader USB
2. Barcode functionality will not trigger any more

Actual Result:

Notice in Cloudfare how there is no event for the dropout

Expected Result:

Event code 941 should be raised and then when the barcode reader is able to be connected to again then the 941 event should be cleared

---
### TIBU-27324 [Bug] (System Test)
PV 3.1.2 - Audible Beep functionality for MUB validation not performing as expected 

**Version:** 3.1.2

**Detail:** NIR PV is not performing the correct validation beeps when presenting MUBs for specific product types. This includes Senior/Concession and child MUBs purchased from HHD, TVM or mLink (where applicable)

**Actual:** 

Adult (Local and XB) - **Single validation beep**

Child (Local and XB) - **Single validation beep**

Student XB - **Single validation beep**

Half Fare - **Single validation beep**

yLink - **Single validation beep**

24+ - **Single validation beep**

Senior/Concession (All types - Local and XB) - **Single validation beep**

PRV-A - **Single validation beep**

PRV-C - **Single validation beep**

Unemployed - **Single validation beep**

**Expected:** 

Adult (Local and XB) - Single validation beep

Child (Local and XB) - Double validation beep

Student XB - Double validation beep

Half Fare - Double validation beep

yLink - Double validation beep

24+ - Double validation beep

Senior/Concession (All types - Local and XB) - Double validation beep

PRV-A - Single validation beep

PRV-C - Double validation beep

Unemployed - Single validation beep

**Video (PV vs GV):** 

PV functionality (video demonstrates Senior/Concession, yLink and Child MUB types):

<custom data-type="smartlink" data-id="id-0">https://drive.google.com/file/d/1rClc_ttaeyAY46xEwmiDeUPIjOOgBgBU/view?usp=sharing</custom> 

GV functionality (video demonstrates correct functionality for Senior/Concession, yLink and Child MUB types):

<custom data-type="smartlink" data-id="id-1">https://drive.google.com/file/d/1Ary0rhFFIsJs7ZgC8no2wMRhPcy5PjxW/view?usp=sharing</custom> 

---
### TIBU-28139 [Bug] (System Test)
PV - Remote logging isn't working for PV devices

PV v3.1.2

Remote logging isn't working for PV devices. When sending a remote command requesting device logs when using Device Log Manager, the devices fails to return back logs.

Steps to reproduce:

1. Open Device Log Manager
2. Select Device Type and Device ID on Device Log Manager for the PV device you want the logs from
3. Select Get Devices button
4. Select the Get Files button (note the to date time is midnight so to retrieve logs for today the to date must be set to tomorrow)
5. Select Show/Refresh button
6. Wait for 10 minutes or so
7. Select Show/Refresh button again

Expected Result:

Logs will be available to download for the device via Device Log Manager

Actual Result:

Logs are not available to download from the device via Device Log Manager 

---
### TIBU-28240 [Bug] (Customer Test)
PV - Device Frozen on black screen after reboot

During recommissioning of PV 2318 for soak testing (funnily enough, witht the aim of trying to reproduce “this” issue) an instance of the PV stuck on the black screen was observed. This was believed to be after the PV had downloaded updates and was performing an automatic update as part of the update process.   
  
This is something also reported on live TL PVs. The PV was powered off to obtain logs, and when powered back on again the PV booted fine. Do not believe that the OS boot screens were shown : the PV performed its reboot and immediately (the next thing we saw) was the black screen.  
  
Logs attached including a readme of the time when the PV was powered off. Unfortunately I expect nothing to be within the logs because I don’t think it got even as far as booting the OS so the application will not have loaded.

---
### TIBU-28649 [Bug] (System Test)
PV - Deny List and BIN List URLs is incorrect for PV builds

PV v1.1.1147.30040

Deny List and BIN List URLs is incorrect for PV builds.

For example the URLs for uktest-tl-env7 should of been:

[https://device-uktest-tl-env6.albedo-gen.co.uk/binlist](https://device-uktest-tl-env6.albedo-gen.co.uk/binlist)

[https://device-uktest-tl-env6.albedo-gen.co.uk/denylist/v2/DenyList/BankCard/18446744073709551615?schemaType=EMV2](https://device-uktest-tl-env6.albedo-gen.co.uk/denylist/v2/DenyList/BankCard/18446744073709551615?schemaType=EMV2)

However they were configured as:

[https://device-uktest-tl-env7.albedo-gen.co.uk/binlist](https://device-uktest-tl-env7.albedo-gen.co.uk/binlist)

[https://device-uktest-tl-env7.albedo-gen.co.uk/denylist/v2/DenyList/BankCard/18446744073709551615?schemaType=EMV2](https://device-uktest-tl-env7.albedo-gen.co.uk/denylist/v2/DenyList/BankCard/18446744073709551615?schemaType=EMV2)

It will be worth checking all of the other environment builds as well for incorrect URLs

Expected Result:

Device builds for PV will contain the correct URLs

Actual Result:

Device builds for PV do not contain the correct URLs

‌

**Correct URLs:**

STE12

https://device-uktest-tl-env6.albedo-gen.co.uk/binlist

https://device-uktest-tl-env6.albedo-gen.co.uk/denylist/v2/DenyList/BankCard/{0}?schemaType=EMV2

‌

STE11

https://device-uktest-tl-env4.albedo-gen.co.uk/binlist

https://device-uktest-tl-env4.albedo-gen.co.uk/denylist/v2/DenyList/BankCard/{0}?schemaType=EMV2

‌

STE10

https://device-uktest-tl-env3.albedo-gen.co.uk/binlist

https://device-uktest-tl-env3.albedo-gen.co.uk/denylist/v2/DenyList/BankCard/{0}?schemaType=EMV2

‌

TFTS-Test

https://device-uktest-tl2-env1.albedo-gen.co.uk/binlist

https://device-uktest-tl2-env1.albedo-gen.co.uk/denylist/v2/DenyList/BankCard/{0}?schemaType=EMV2

‌

TFTS-Live and Glider-TFTS-Live

https://device-translink-prod.cloudfare.co.uk/binlist

https://device-translink-prod.cloudfare.co.uk/denylist/v2/DenyList/BankCard/{0}?schemaType=EMV2

---
### TIBU-28805 [Bug] (System Test)
PV - EMV taps which are declined due to not being on the Pilot List are incorrectly creating audits 

PV v1.1.1160.26839

EMV taps which are declined due to not being on the Pilot List are incorrectly creating audits.

![](blob:https://media.staging.atl-paas.net/?type=file&localId=null&id=c6e657d0-e5cc-4ede-ba9f-c11246a75796&&collection=&height=443&occurrenceKey=null&width=1504&__contextId=null&__displayType=null&__external=false&__fileMimeType=null&__fileName=null&__fileSize=null&__mediaTraceId=null&url=null)
Expected Result:

If the FEIG token is not on the Pilot list then the device will reject the tap with the standard rejection screen and will not perform any auditing.

Actual Result:

When the FEIG token is not on the list then the device will reject the tap with the standard rejection screen and the device is creating a transaction audit for the tap

Logs:

![](blob:https://media.staging.atl-paas.net/?type=file&localId=null&id=3730c6b5-321f-44aa-8ccf-8d8dc2b0076a&&collection=&height=null&occurrenceKey=null&width=null&__contextId=null&__displayType=null&__external=false&__fileMimeType=null&__fileName=null&__fileSize=null&__mediaTraceId=null&url=null)‌

---
### TIBU-29191 [Bug] (System Test)
PV > QA > COMMS > FAILOVER > Sim remains "connected" when removed physically

**Version**: QA Build

**Actual:** 

SIM remaining connected when physically removed from PV.

PV required hard reboot to connect ethernet (on occasion)

Audit files sending when device shows ethernet disconnected.

PV did not complete overnight reboot when ethernet only connected/ required hard reboot.

**Expected:** 

PV should recognise when sim card is removed and update accordingly, showing that Sim is disconnected. All correct and relevant reporting should trigger

**Logs:**

![](blob:https://media.staging.atl-paas.net/?type=file&localId=null&id=2f91a25f-c9e0-49d3-a91b-061c646be126&&collection=&height=null&occurrenceKey=null&width=null&__contextId=null&__displayType=null&__external=false&__fileMimeType=null&__fileName=null&__fileSize=null&__mediaTraceId=null&url=null)‌

---
### TIBU-31287 [Bug] (System Test)
PV - Downloading Deny List with 200000 entries causes "PollSocket: Send failed. Exception" 

PV v1.1.1284.24210

Downloading Deny List with 200000 entries causes "PollSocket: Send failed. Exception".

`2026-05-15 14:18:57.590 WARN [OpenPayment] - [BackOfficeProviderBase] RemoveRequestResponseFromList removed request for URI: https://device-uktest-tl-env6.albedo-gen.co.uk/denylist/v2/DenyList/BankCard/18446744073709551615?schemaType=EMV2`

`2026-05-15 14:18:57.591 INFO [OpenPayment] - [BackOfficeDenyListProviderBase] Got response OK`

`2026-05-15 14:18:59.000 ERROR [TimeSync] - [NtpTimeCommunicator] Date Time Fetch Request timed out`

`2026-05-15 14:19:11.000 WARN [OpenPayment] - [SetDenyList] calling Send`

`2026-05-15 14:19:11.562 INFO [SRS] - [WecOsWatchdogMonitor] KICKED`

`2026-05-15 14:19:12.000 ERROR [OpenPayment] - PollSocket: Send failed. Exception[ System.Net.Sockets.SocketException: An existing connection was forcibly closed by the remote host`

`   at System.Net.Sockets.Socket.SendNoCheck(Byte[] buffer, Int32 index, Int32 size, SocketFlags socketFlags)`

`   at System.Net.Sockets.Socket.Send(Byte[] buffer, Int32 offset, Int32 size, SocketFlags socketFlags)`

`   at Flowbird.GFTS.Utils.PollSocket.Send(Byte[] buffer, Int32 offset, Int32 size, SocketFlags socketFlags)`

`   at Flowbird.GFTS.Utils.PollSocket.Send(Byte[] buffer)`

`   at Flowbird.GFTS.Services.OpenPayment.Feig.FeigReader.SendTlv(Tlv tlv)`

`   at Flowbird.GFTS.Services.OpenPayment.Feig.FeigReader.SetDenyList(BinaryList list)`

`   at Flowbird.GFTS.Services.OpenPayment.Feig.FeigAdaptor.SetDenyList(BinaryList newDenyList)`

`   at Flowbird.GFTS.Services.OpenPayment.OpenPaymentWrapper.SetDenyList(BinaryList denyList)`

`   at Flowbird.GFTS.Services.OpenPayment.OpenPaymentService.UpdateDenyList(BinaryList list)`

`   at Flowbird.GFTS.Services.OpenPayment.BackOfficeDenyListProvider.UpdateData(BinaryList list)`

`   at Flowbird.GFTS.Services.BackOfficeListSupport.BackOfficeDenyListProviderBase.CheckForDenyList()`

`   at Flowbird.GFTS.Services.BackOfficeAgent.TimerSchedule.TimerElapsedCallback(Object state)`

`   at System.Threading.Timer.ring()`

Expected Result:

Device successfully downloading Deny List which doesn’t impact devices performance 

Actual Result:

Device attempts to download Deny List but fails due to unhandled exception

Logs:

![](blob:https://media.staging.atl-paas.net/?type=file&localId=null&id=218e3550-c327-4dcb-94a6-ea2469efc92e&&collection=&height=null&occurrenceKey=null&width=null&__contextId=null&__displayType=null&__external=false&__fileMimeType=null&__fileName=null&__fileSize=null&__mediaTraceId=null&url=null)‌

---
### TIBU-31705 [Bug] (Customer Test)
Technician screen speed on processing sub menu screens

Processing screen taking 10/15 seconds on Network settings between screens on cellular/ FEC1 etc.

---
### TIBU-30923 [Bug] (QA TEST)
Devices cannot apply brand new configuration settings at the same time as a software update

In cases whereby a new parameter has been added to TMS that the current software does not ‘know’ about, if new application software is distributed that does ‘know’ about the new setting it will not apply the new setting(s) until after a second distribution currently. Examples include the new ABT settings (i.e. zone numbers/product names) and barcode files previously.

---
### TIBU-25444 [Bug] (System Test)
TL PV : Issue with barcode expiry date shown on PV when validating barcode (NIR)

Similar to the issue found on the GV with the introduction of the changes for CR116 (TIBU-25154) there appears to be an issue with the way the PV is displaying the expiry date of the barcode when it is validated.   
  
Please see attached images.   
  
”Barcode Ticket” shows the original purchase time of the barcode (11:39) and the barcode purchased has a validation time of 3.5 hours based on the topology used. This should mean that the barcode expires at 15:09 however the expiry time on the screen shows 14:09 as per the “Validation Screen” image.  
  
NOTE That the expiry time encoded into the barcode is UTC, so when displaying the expiry time the PV needs to account for this and convert the UTC expiry time into local time

---
### TIBU-31722 [Bug] (Ready for Release)
PV - ABT Glider Metro not enabling even with ABT Tap Zone configured correctly

Build - 5.0.0

Glider ABT EMV Enabled via Param fields on TMS - ABT Tap Zone

1. Deploy TMS with configured ABT Tap zone
2. Ensure Device has the same ABT Tap Zone configured
3. **Unable to tap EMV cards on device**

‌

Logs:  

---
### TIBU-32037 [Bug] (Ready for Release)
[TL PV] Failure to update FEIG PCA and FW due to watchdog kicking in

When attempting to deploy an updated PCA and Firmware to the FEIG on the PV, the GFTS application watchdog reboots before the update can happen.  
  
Symptoms:  
  
\- PV boots into the OOS screen  
\- After approx 60 seconds the PV displays the in service “present card” screen  
\- PV then quite quickly displays the “Processing” screen (indicating the FEIG update has started)  
\- You can hear the FEIG beep indicating the update has started  
\- Shortly after, the PV watchdog reboots  
  
The above is a permanent loop.  
  
When appsettings.json is updated to set the IntervalMilliseconds to 3000000 (instead of 30000) and WatchdogEnabled is set to False for each of the services, then the FEIG PCA and FW updates complete successfully.  
  
Logs attached.
