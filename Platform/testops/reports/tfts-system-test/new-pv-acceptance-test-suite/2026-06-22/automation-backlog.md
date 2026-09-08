# Automation backlog — **NEW** PV-Acceptance Test Suite (PV)

_Generated 2026-06-22T10:01:28+00:00 by system-test-ops. Suite id 30255, project TFTS - System Test._

**12 fully automatable + 45 partial** of 122 cases (4 destructive, 65 manual-only). _Partial = the UI flow is automatable but a step (card tap / print / cash) needs a hardware fixture or human eye._

## How to consume

- Reference `ref` (TestRail case id, e.g. C4099911) in each automated test so a result maps back to its case.
- Mirror device + feature as pytest markers; add @pytest.mark.destructive where destructive is true (deselected by default).
- cross_check lists the back-office systems the case asserts — the test must verify the event landed there (CloudFare / MERIT / SmartTrack).
- automatable/priority are system-test-ops judgements and a starting point; the automation engineer may override with rationale.


## Priority: High

### C4100998 · ABT — contactless tap validation  (6m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / ABT (Glider)_

**Given** a Glider PV has ABT/cEMV enabled and is showing the Present screen
**WHEN** a valid contactless payment card or device is presented
**THEN** the tap is accepted for the journey
**AND** the success outcome is shown to the passenger
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4100999 · ABT — declined or errored tap  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / ABT (Glider)_

**Given** a Glider PV has ABT/cEMV enabled
**WHEN** a card that is declined, expired or mis-read is presented
**THEN** the tap is rejected
**AND** the See Driver / decline outcome is shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4101000 · ABT — BIN, Deny and Pilot list handling  (5m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / ABT (Glider)_

**Given** a Glider PV has the BIN, Deny and Pilot lists applied
**WHEN** a card on the Deny or BIN list is presented
**THEN** the tap is rejected per the list rules
**WHEN** a card on the Pilot list is presented
**THEN** the tap is handled per the pilot rules
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4101001 · cEMV — tap enablement by route, location and fare  (5m)  — PARTIAL; **DESTRUCTIVE**; cross-check: CloudFare / MERIT
_Functional / ABT (Glider)_

**Given** a Glider PV uses route-attribute, location and fare checks to enable cEMV
**WHEN** the PV is in a context where all checks pass
**THEN** cEMV taps are enabled
**WHEN** any of the route, location or fare checks fail
**THEN** cEMV taps are disabled in that context
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4101002 · Glider TOO — tap-on-only flat-fare journeys  (5m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / ABT (Glider)_

**Given** a Glider PV is on a Tap-On-Only flat-fare route
**WHEN** a passenger taps on for a journey
**THEN** a flat-fare journey is recorded
**WHEN** the same passenger taps multiple times in a day
**THEN** the daily tap and duplicate-tap rules are applied
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4101003 · Glider — transfers  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / ABT (Glider)_

**Given** a passenger has tapped a first Glider journey
**WHEN** they tap a connecting journey within the transfer window
**THEN** the transfer is recognised per the transfer rules
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4101004 · ABT — end-to-end journey to back office  (4m)  — cross-check: CloudFare / MERIT
_Functional / ABT (Glider)_

**Given** a Glider PV with ABT enabled and back-office comms available
**WHEN** a passenger completes an ABT journey
**THEN** the journey is recorded
**AND** the journey is sent to the back office for settlement
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4101078 · ABT — Pilot List management and validation  (7m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / ABT (Glider)_

**Given** a Glider PV with cEMV is configured for the Pilot List via TMS
**WHEN** a pilot list (pilotlist.zip) is applied to the PV via TMS, including registration mode
**THEN** the PV applies the pilot list configuration
**WHEN** an EMV card that is included on the Pilot List is presented
**THEN** the card is accepted per the pilot rules
**WHEN** an EMV card that is NOT on the Pilot List is presented
**THEN** the card is handled per the not-included rule
**WHEN** the pilot list is exported
**THEN** it can be converted from CSV to DAT and downloaded as CSV from Device Log Manager
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4101079 · ABT — Deny and BIN list updates  (7m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-26320, TIBU-25745
_Functional / ABT (Glider)_

**Given** a Glider PV with cEMV and back-office comms
**WHEN** delta and full Deny/BIN list updates are published
**THEN** the PV downloads and applies them, taking the full lists at end of day and deltas on schedule
**WHEN** a list download fails
**THEN** the PV retries the download and application
**WHEN** a card on the Deny or BIN list is presented
**THEN** the tap is rejected
**WHEN** a card is removed from the list and re-presented
**THEN** the tap is accepted
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4101088 · cEMV — decline reasons and route-type enablement  (6m)  — PARTIAL; **DESTRUCTIVE**; cross-check: CloudFare / MERIT
_Functional / ABT (Glider)_

**Given** a Glider PV with cEMV
**WHEN** a card fails Offline Data Authentication, is an unsupported scheme (e.g. AMEX), is expired, has an invalid BIN, fails the AID check, is a card clash, is on the deny or negative list, or is not read successfully
**THEN** the Please Try Again outcome is shown with the corresponding decline reason
**WHEN** the route is "Tap On Only (Flat Fare)" or "Tap On Tap Off"
**THEN** cEMV taps are enabled for that route type
**WHEN** no valid fare is found, the boarding location is outside the configured area, or cEMV is disabled in the Technician Menu
**THEN** cEMV taps are disabled
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4101089 · cEMV — JourneyTap audit and alighting-stage derivation  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / ABT (Glider)_

**Given** a Glider PV with cEMV on a Tap-On-Only route
**WHEN** a successful cEMV tap is made
**THEN** the tap is audited as a "JourneyTap" in CloudFare
**AND** the alighting stage is derived from the Furthest Alighting Point file
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4101092 · cEMV — tap audit content (JourneyTap, stop/stage, direction, payment method)  (6m)  — PARTIAL; cross-check: CloudFare / MERIT; refs: TIBU-22332, TIBU-30476, TIBU-28856, TIBU-28645
_Functional / ABT (Glider)_

**Given** a Glider PV with cEMV on a Tap On Only route
**WHEN** a successful cEMV tap is made
**THEN** the tap is audited as a "JourneyTap" in CloudFare
**AND** the audit records both the stop id and the stage id
**AND** the tap direction is audited correctly as IN
**AND** the payment method is audited correctly for the Glider TOO transaction
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4101093 · cEMV — EMV result screens and transaction generation  (9m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack; refs: TIBU-25700, TIBU-25702, TIBU-25704, TIBU-25705
_Functional / ABT (Glider)_

**Given** a Glider PV with cEMV
**WHEN** a cEMV tap succeeds or fails
**THEN** the correct EMV success or failure screen is shown
**AND** the EMV result screen times out after the configured period rather than persisting
**WHEN** a smartcard is presented while an EMV success or failure screen is shown
**THEN** the smartcard tap is accepted
**WHEN** an EMV tap fails
**THEN** a transaction is still generated for the failed tap
**WHEN** a card is re-presented for EMV passback
**THEN** the correct EMV passback screen is shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4101005 · Barcode — single-use validation  (5m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Barcodes_

**Given** the PV is showing the Present SmartCard or Barcode screen
**WHEN** a valid single-use barcode is presented
**THEN** the barcode is validated
**AND** the validation is recorded in the back office (CloudFare and MERIT)
**WHEN** an invalid single-use barcode is presented
**THEN** the barcode is rejected with the specific reason shown

### C4101006 · Barcode — multi-use validation  (5m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Barcodes_

**Given** the PV is showing the Present SmartCard or Barcode screen
**WHEN** a valid multi-use barcode is presented
**THEN** the barcode is validated
**AND** a use is recorded
**AND** the validation is recorded in the back office (CloudFare and MERIT)
**WHEN** the barcode is presented beyond its allowed uses or is invalid
**THEN** the barcode is rejected with the specific reason shown

### C4102428 · Barcode — early-morning expiry displays the previous day  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Barcodes_

**Given** the PV is showing the Present SmartCard or Barcode screen
**WHEN** a valid barcode with an expiry time between 00:00 and 04:00 is presented
**THEN** the barcode is validated
**AND** the validation success screen displays the previous day as the expiry date
**AND** the validation is recorded in the back office (CloudFare and MERIT)

### C4102430 · PV commissioning — uncommissioned until location programmed  (5m)  — cross-check: CloudFare
_Functional / Commissioning_

**Given** an uncommissioned PV with an unprogrammed Plinth-ID
**WHEN** the device starts up before any location is programmed
**THEN** the status bar shows no programmed Device ID, Sub Location or Location values
**WHEN** the PV has comms and a technician signs in and programs the location details
**THEN** the status bar displays the programmed Device ID, Sub Location and Location

### C4101007 · Legacy smartcard support  (7m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Legacy & Card Tech_

**Given** the PV is showing the Present SmartCard or Barcode screen
**WHEN** a valid legacy journey-based or time-based smartcard is presented
**THEN** the card is validated per its legacy rules
**WHEN** an invalid legacy smartcard is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4101008 · Card technology — MIFARE and DESFire  (6m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Legacy & Card Tech_

**Given** the PV is in service
**WHEN** a MIFARE Classic EV1 or DESFire card is presented
**THEN** the PV reads and validates the card per its type
**AND** the validation is recorded in the back office (CloudFare, MERIT and SmartTrack)

### C4101009 · Passback handling  (8m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Legacy & Card Tech_

**Given** a card has just been validated at the PV
**WHEN** the same card is presented again within the passback window
**THEN** passback is applied per the product rules
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT

### C4101010 · PV operating times  (2m)  — PARTIAL; **DESTRUCTIVE**
_Functional / Legacy & Card Tech_

**Given** the PV has configured operating times
**WHEN** a card is presented within the operating times
**THEN** the card is validated normally
**WHEN** a card is presented outside the operating times
**THEN** the PV does not validate
**AND** shows the out-of-service state

### C4100996 · Rail — NIR transfer validation  (7m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Rail-specific_

**Given** a Rail PV is in service
**WHEN** a valid transfer-eligible smartcard is presented for an NIR transfer
**THEN** the transfer is validated per the transfer rules
**WHEN** the card is not eligible for the transfer
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100997 · Rail — zone validation  (7m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Rail-specific_

**Given** a Rail PV is in service in a defined zone
**WHEN** a valid zonal smartcard is presented within its zone
**THEN** the card is validated for the zone
**WHEN** the card is presented outside its valid zone
**THEN** the card is rejected as wrong zone
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4102429 · Rail — ABT tap success shows the Northern Ireland travel line  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_Functional / Rail-specific_

**Given** a Rail/NIR PV has ABT enabled and is showing the Present screen
**WHEN** a valid contactless card is tapped and accepted
**THEN** the ABT tap success screen is shown
**AND** the success screen displays the additional line "Northern Ireland Travel Only"

### C4100981 · Validate a Concession SmartPass  (7m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcard Validation_

**Given** the PV is in service showing the Present SmartCard or Barcode screen
**WHEN** a valid concession SmartPass is presented
**THEN** the card is validated
**AND** the success outcome is shown
**WHEN** an invalid concession SmartPass is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100982 · Validate a Half-Fare SmartPass  (7m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcard Validation_

**Given** the PV is in service showing the Present SmartCard or Barcode screen
**WHEN** a valid Half-Fare SmartPass is presented
**THEN** the card is validated
**AND** the success outcome is shown
**WHEN** an invalid Half-Fare SmartPass is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100983 · Validate a Metro Daylink smartcard  (7m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcard Validation_

**Given** the PV is in service showing the Present SmartCard or Barcode screen
**WHEN** a valid Metro Daylink smartcard is presented
**THEN** the card is validated
**AND** the success outcome is shown
**WHEN** an invalid Metro Daylink smartcard is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100984 · Validate a Metro Multi-Journey smartcard  (7m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcard Validation_

**Given** the PV is in service showing the Present SmartCard or Barcode screen
**WHEN** a valid Metro Multi-Journey smartcard is presented within its zone
**THEN** the card is validated
**AND** a journey is deducted with the passback rules applied
**WHEN** the card is presented out of zone or is otherwise invalid
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100985 · Validate a Metro Travelcard  (7m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcard Validation_

**Given** the PV is in service showing the Present SmartCard or Barcode screen
**WHEN** a valid Metro Travelcard is presented
**THEN** the card is validated
**AND** the success outcome is shown
**WHEN** an invalid Metro Travelcard is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100986 · Validate an Ulsterbus Multi-Journey smartcard  (7m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcard Validation_

**Given** the PV is in service showing the Present SmartCard or Barcode screen
**WHEN** a valid Ulsterbus Multi-Journey smartcard is presented
**THEN** the card is validated
**AND** a journey is deducted with the passback rules applied
**WHEN** an invalid Ulsterbus Multi-Journey smartcard is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100987 · Validate an iLink smartcard  (7m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcard Validation_

**Given** the PV is in service showing the Present SmartCard or Barcode screen
**WHEN** a valid iLink smartcard is presented within its zone
**THEN** the card is validated
**AND** the success outcome is shown
**WHEN** the card is presented out of zone or is otherwise invalid
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100988 · Validate an aLink smartcard  (7m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcard Validation_

**Given** the PV is in service showing the Present SmartCard or Barcode screen
**WHEN** a valid aLink smartcard is presented
**THEN** the card is validated
**AND** the success outcome is shown
**WHEN** an invalid aLink smartcard is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100989 · Validate a yLink or 24+ smartcard  (7m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcard Validation_

**Given** the PV is in service showing the Present SmartCard or Barcode screen
**WHEN** a valid yLink or 24+ smartcard is presented
**THEN** the card is validated
**AND** the success outcome is shown
**WHEN** an invalid yLink or 24+ smartcard is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100990 · Validate a Translink Employee smartcard  (7m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcard Validation_

**Given** the PV is in service showing the Present SmartCard or Barcode screen
**WHEN** a valid Translink employee smartcard is presented
**THEN** the card is validated
**AND** the success outcome is shown
**WHEN** an invalid Translink employee smartcard is presented
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4100991 · Validate an EA Smartpass (Pupil and Further Education)  (7m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcard Validation_

**Given** the PV is in service showing the Present SmartCard or Barcode screen
**WHEN** a valid EA Smartpass is presented within its valid time
**THEN** the card is validated
**AND** the success outcome is shown
**WHEN** it is presented before start date, after expiry, outside the valid time, at a weekend or during a school holiday
**THEN** the card is rejected with the specific reason shown
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4101090 · Smartcard — inter-device top-up then validate on PV  (9m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Smartcard Validation_

**Given** a smartcard has been topped up on another device (e.g. POS) or a legacy device
**WHEN** the card is presented to the PV for validation
**THEN** the PV validates the card reflecting the top-up made elsewhere
**WHEN** the card was topped up on its last day of travel, with expired journeys, or with no days remaining
**THEN** the PV applies the corresponding outcome
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log
**WHEN** the data is reviewed in MERIT
**THEN** the transaction appears in MERIT
**WHEN** the smartcard record is reviewed in SmartTrack
**THEN** the updated smartcard record appears in SmartTrack

### C4101011 · Technician Menu — login  (7m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Technician Menu_

**Given** the PV is in service displaying the Technician Menu login screen
**WHEN** a technician presents a valid technician smartcard and enters the correct PIN
**THEN** the Technician Menu home screen is displayed
**WHEN** an invalid technician smartcard or an incorrect PIN is presented
**THEN** the incorrect-details message is shown
**AND** access to the Technician Menu is refused

### C4101014 · Technician Menu — software and configuration versions  (5m)  — cross-check: CloudFare
_Functional / Technician Menu_

**Given** a technician is in the Technician Menu
**WHEN** the technician views the Software Versions page
**THEN** the software versions are listed (OS, BSP, EBoot, Configuration Version, application software and operating files)
**WHEN** the technician views the Configuration Versions page
**THEN** the configuration versions are listed (Configuration Version, Furthest Alighting file, TD.Product, TD.Topology, Staff List)

### C4101015 · Technician Menu — force communications  (6m)  — cross-check: CloudFare
_Functional / Technician Menu_

**Given** a technician is in the Technician Menu
**WHEN** the technician opens the Force Communications page
**THEN** the page summarises the comms status — pending audit-record count, last successful audit send, last manifest download attempt, last successful manifest download, pending software/configuration file count
**WHEN** the technician presses Call Now
**THEN** the PV checks the back-office manifest and attempts to send any pending audit records
**WHEN** the technician presses Refresh
**THEN** the displayed values update to the most recent information

### C4102166 · Technician Menu — sign off  (4m)  — cross-check: CloudFare
_Functional / Technician Menu_

**Given** a technician is signed in to the Technician Menu
**WHEN** the technician selects Sign Off
**THEN** the technician is signed off
**AND** the PV returns to its in-service state
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4102181 · Technician Menu — auto sign-off and page timeouts  (5m)  — cross-check: CloudFare
_Functional / Technician Menu_

**Given** a technician is signed in to the Technician Menu
**WHEN** no input is made on a page and it times out
**THEN** the PV returns to the Technician Menu home screen
**WHEN** the inactivity period elapses
**THEN** the PV auto signs the technician off with a tone
**AND** the sign-off is audited
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4100992 · Validation — invalid reasons displayed  (6m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Validation Outcomes_

**Given** the PV is in service showing the Present SmartCard or Barcode screen
**WHEN** a card is presented that cannot be validated
**THEN** the specific reason screen is displayed
**AND** the denied validation is recorded in the back office (CloudFare, MERIT and SmartTrack)

### C4100993 · Validation — passback  (6m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Functional / Validation Outcomes_

**Given** a card has just been validated on the PV
**WHEN** the same card is presented again within the passback period
**THEN** passback is applied per the product rules
**AND** the journeys or period remaining is shown where applicable
**AND** the validation is recorded in the back office (CloudFare, MERIT and SmartTrack)

### C4100994 · Validation — machine not in service  (1m)  — PARTIAL
_Functional / Validation Outcomes_

**Given** the PV is out of service
**WHEN** a passenger presents a card
**THEN** the Machine Not In Service screen is displayed and no validation occurs

### C4101021 · PV to BOS — transaction upload  (4m)  — PARTIAL; cross-check: CloudFare
_Non-Functional / PV_

**Given** the PV has recorded validation and tap transactions
**WHEN** the PV communicates with the back office
**THEN** the transactions are uploaded to the back office

### C4101082 · PV to BOS — MERIT heartbeat  (5m)  — cross-check: CloudFare / MERIT
_Non-Functional / PV_

**Given** a PV is in service
**WHEN** the configured 24-hour period elapses
**THEN** a MERIT heartbeat transaction is sent to the back office
**WHEN** a technician signs out of the Technician Menu
**THEN** a heartbeat occurs

### C4101084 · PV to BOS — configuration and topology distribution  (6m)  — cross-check: CloudFare
_Non-Functional / PV_

**Given** the back office has a configuration or topology update for the PV
**WHEN** the PV downloads a configuration or topology update for immediate activation
**THEN** the update is applied
**WHEN** the update has a future activation date
**THEN** it is stored and activated on that date
**WHEN** a corrupt configuration file is downloaded
**THEN** it is rejected
**AND** the current configuration is retained

### C4101085 · PV to BOS — communications resilience and failover  (5m)  — PARTIAL; cross-check: CloudFare
_Non-Functional / PV_

**Given** a PV in service communicating with the back office
**WHEN** communications are interrupted or lost
**THEN** the PV continues to validate and queues data to upload
**AND** data due for download is retrieved once comms return
**WHEN** the primary comms channel fails
**THEN** the PV fails over to the secondary communication method
**WHEN** the CloudFare activity log is checked
**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log

### C4101072 · Smoke — valid smartcard validates  (6m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Smoke_

**Given** the PV is in service showing the Present SmartCard or Barcode screen
**WHEN** a valid smartcard is presented
**THEN** the card is validated
**AND** the success outcome is shown

### C4101073 · Smoke — invalid smartcard shows a reason  (6m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Smoke_

**Given** the PV is in service showing the Present SmartCard or Barcode screen
**WHEN** an invalid smartcard is presented
**THEN** the card is rejected with the specific reason shown

### C4101074 · Smoke — valid barcode validates  (1m)  — PARTIAL
_Smoke_

**Given** the PV is in service showing the Present SmartCard or Barcode screen
**WHEN** a valid barcode is presented
**THEN** the barcode is validated

### C4101075 · Smoke — ABT contactless tap succeeds  (4m)  — PARTIAL; cross-check: CloudFare / MERIT
_Smoke_

**Given** a Glider PV has ABT enabled and is showing the Present screen
**WHEN** a valid contactless card is tapped
**THEN** the tap is accepted with a success outcome

### C4101076 · Smoke — Technician Menu login  (6m)  — PARTIAL; cross-check: CloudFare / MERIT / SmartTrack
_Smoke_

**Given** the PV is in service displaying the Technician Menu login screen
**WHEN** a technician presents a valid technician smartcard and enters a valid PIN
**THEN** the Technician Menu home screen is displayed

### C4101077 · Smoke — PV communicates with the back office  (4m)  — cross-check: CloudFare
_Smoke_

**Given** the PV is in service
**WHEN** communications with the back office are forced
**THEN** the PV exchanges data with the back office successfully


## Priority: Normal

### C4101016 · Technician Menu — network settings  (1m)
_Functional / Technician Menu_

**Given** a technician is in the Technician Menu
**WHEN** the technician views and edits the network settings and confirms
**THEN** the network settings are updated

### C4101017 · Technician Menu — operating times  (1m)  — **DESTRUCTIVE**
_Functional / Technician Menu_

**Given** a technician is in the Technician Menu
**WHEN** the technician reconfigures the operating start time
**THEN** the new operating times are applied
**AND** the PV goes out of service and then into service per the configured times

### C4101086 · PV — scheduled maintenance  (2m)
_Non-Functional / PV_

**Given** a scheduled maintenance window is configured
**WHEN** the PV is in idle mode during the window
**THEN** the scheduled maintenance is performed
**WHEN** the PV comes out of the suspended state
**THEN** the PV resumes to service

