# Alignment audit - suite 30254

- Cases audited: **148**
- Blocking findings: **1**
- Advisory (reviewed-intentional) findings: **11**

## Residual mojibake in any field - 0
_none_

## Title missing the ' - ' feature separator _(advisory)_ - 9
- C4100524 | Driver Sign Off
- C4100648 | ETM continues working when the BOS connection is lost
- C4100649 | Download configuration files from the back office
- C4100650 | Software distribution and fare-mode transition
- C4100651 | Upload audit files and data to the back office
- C4100654 | Auto sign-off
- C4100655 | MIFARE card type validation on the ETM
- C4100656 | Smartcard and EMV transaction timings
- C4100657 | Interface with other on-vehicle third-party equipment

## Title over 72 chars _(advisory)_ - 2
- C4100514 | Driver Sign On — incorrect PIN locks the device after the configured attempts - 77 chars
- C4100515 | Driver Sign On — communications locked / not communicating with CloudFare - 73 chars

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

## Genuine compound THEN (two distinct outcomes) - should split - 1
- C4100649 | Download configuration files from the back office - the corrupt file is rejected and the current configuration is retained

## Expected (prose) empty - 0
_none_

## Expected starts with THEN (should be prose) - 0
_none_

## Tags (@project/@device/...) written into the case - 0
_none_
