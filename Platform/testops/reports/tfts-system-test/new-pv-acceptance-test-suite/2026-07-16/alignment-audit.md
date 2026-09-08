# Alignment audit - suite 30255

- Cases audited: **133**
- Blocking findings: **0**
- Advisory (reviewed-intentional) findings: **26**

## Residual mojibake in any field - 0
_none_

## Title missing the ' - ' feature separator _(advisory)_ - 16
- C4100981 | Validate a Concession SmartPass
- C4100982 | Validate a Half-Fare SmartPass
- C4100983 | Validate a Metro Daylink smartcard
- C4100984 | Validate a Metro Multi-Journey smartcard
- C4100985 | Validate a Metro Travelcard
- C4100986 | Validate an Ulsterbus Multi-Journey smartcard
- C4100987 | Validate an iLink smartcard
- C4100988 | Validate an aLink smartcard
- C4100989 | Validate a yLink or 24+ smartcard
- C4100990 | Validate a Translink Employee smartcard
- C4100991 | Validate an EA Smartpass (Pupil and Further Education)
- C4101007 | Legacy smartcard support
- C4101009 | Passback handling
- C4101010 | PV operating times
- C4101018 | Power interruption and recovery
- C4101022 | Daylight Saving Time change

## Title over 72 chars _(advisory)_ - 10
- C4101092 | cEMV — tap audit content (JourneyTap, stop/stage, direction, payment method) - 76 chars
- C4103564 | Pilot Registration — the registration file uploads once per day at End-of-Day - 77 chars
- C4103566 | Legacy Transfer — decided by the product Transfer Time, not a route property - 76 chars
- C4103567 | Legacy Transfer — re-validation outside the product Transfer Time counts as a journey - 85 chars
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
