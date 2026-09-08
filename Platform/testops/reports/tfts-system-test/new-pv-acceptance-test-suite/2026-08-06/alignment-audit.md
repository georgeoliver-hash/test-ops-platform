# Alignment audit - suite 30255

- Cases audited: **196**
- Blocking findings: **0**
- Advisory (reviewed-intentional) findings: **49**

## Residual mojibake in any field - 0
_none_

## Title missing the ' - ' feature separator _(advisory)_ - 32
- C4100981 | Validate a 60+ Concession SmartPass
- C4100982 | Validate a DLA Half-Fare SmartPass
- C4100983 | Validate a Metro Daylink smartcard
- C4100984 | Validate a City-zone Metro Multi-Journey smartcard
- C4100985 | Validate a Metro Travelcard
- C4100986 | Validate an Ulsterbus Multi-Journey smartcard
- C4100987 | Validate an iLink Zone 4 smartcard
- C4100988 | Validate an aLink smartcard
- C4100989 | Validate a yLink smartcard
- C4100990 | Validate a Staff Translink Employee smartcard
- C4100991 | Validate an EA Pupil Smartpass
- C4104432 | Validate a Blind Concession SmartPass
- C4104433 | Validate a Senior Concession SmartPass
- C4104435 | Validate a ROI Senior Concession SmartPass
- C4104436 | Validate a War Pensioner Concession SmartPass
- C4104438 | Validate a Learning Disability Half-Fare SmartPass
- C4104440 | Validate a No Driving Licence Half-Fare SmartPass
- C4104442 | Validate a PIPS Half-Fare SmartPass
- C4104444 | Validate a Partially Sighted Half-Fare SmartPass
- C4104446 | Validate a Inner-zone Metro Multi-Journey smartcard
- C4104448 | Validate a Extended-zone Metro Multi-Journey smartcard
- C4104450 | Validate an iLink Zone 1 smartcard
- C4104451 | Validate an iLink Zone 2 smartcard
- C4104453 | Validate an iLink Zone 3 smartcard
- C4104455 | Validate an iLink NW smartcard
- C4104457 | Validate a Belfast Visitor Pass
- C4104459 | Validate a 24+ smartcard
- C4104461 | Validate a Staff Partner Translink Employee smartcard
- C4104464 | Validate a Retired Staff Translink Employee smartcard
- C4104465 | Validate a External Staff Translink Employee smartcard
- C4104467 | Validate a Dependents Pass Translink Employee smartcard
- C4104469 | Validate an EA Further Education Smartpass

## Title over 72 chars _(advisory)_ - 17
- C4101092 | cEMV — tap audit content (JourneyTap, stop/stage, direction, payment method) - 76 chars
- C4104931 | Duplicate tap — a same-stage re-tap within the Same Location Time still shows Tap Successful - 92 chars
- C4104932 | Duplicate tap — a same-stage re-tap outside the Same Location Time is a genuine new tap - 87 chars
- C4104939 | Cross-device duplicate — a PV tap followed by an ETM tap at the same halt within the Same Location Time still shows Tap Successful - 130 chars
- C4104109 | PV — barcode/smartcard reader disconnect shows the correct banner and raises an event - 85 chars
- C4101009 | Passback — re-presentation within the window is handled per product rules - 73 chars
- C4103564 | Pilot Registration — the registration file uploads once per day at End-of-Day - 77 chars
- C4103566 | Legacy Transfer — decided by the product Transfer Time, not a route property - 76 chars
- C4103567 | Legacy Transfer — re-validation outside the product Transfer Time counts as a journey - 85 chars
- C4105410 | Device Fault — Machine Not in Service recovers to Present SmartCard or Barcode when corrected - 93 chars
- C4103568 | Comms Lock — a sustained loss of both Ethernet and cellular drives the PV out of service - 88 chars
- C4103569 | Comms Recovery — transactions queued during an outage are delivered on restore - 78 chars
- C4101057 | Screen Validation — 11_01_03 Technician Menu - Location Settings - Edit - Clear - 79 chars
- C4101059 | Screen Validation — 11_01_10 Technician Menu - Select Location - Selected - 73 chars
- C4101065 | Screen Validation — 11_05_02 Technician Menu - Network interfaces - Details - 75 chars
- C4101066 | Screen Validation — 11_05_03 Technician Menu - Network interfaces - FecDetails - 78 chars
- C4101067 | Screen Validation — 11_05_04 Technician Menu - Network interfaces -ChangeIP - 75 chars

## Objective/preface empty - 0
_none_

## Objective not starting 'This test is to confirm' - 0
_none_

## Preconditions empty - 0
_none_

## Preconditions without a GIVEN - 0
_none_

## No When/Then steps at all - 0
_none_

## First step is not a WHEN - 0
_none_

## Step content not WHEN/AND - 0
_none_

## A WHEN with no THEN outcome - 0
_none_

## Genuine compound THEN (two distinct outcomes) - should split - 0
_none_

## Expected (prose) empty - 0
_none_

## Expected starts with THEN (should be prose) - 0
_none_

## Tags (@project/@device/...) written into the case - 0
_none_
