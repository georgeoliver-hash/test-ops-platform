# Alignment audit - suite 30286

- Cases audited: **97**
- Blocking findings: **0**
- Advisory (reviewed-intentional) findings: **38**

## Residual mojibake in any field - 0
_none_

## Title missing the ' - ' feature separator _(advisory)_ - 0
_none_

## Title over 72 chars _(advisory)_ - 38
- C4104017 | ABT Tap — a card on the Deny List is rejected in entry mode with Declined Reason 2 - 82 chars
- C4104019 | ABT Tap — an offline transaction is accepted and queued for the back office - 75 chars
- C4104020 | ABT Tap — the reader stays disarmed when the route ABT Type is not Tap On Tap Off - 81 chars
- C4104021 | ABT Tap — the reader stays disarmed when the home location is outside the Northern Ireland Zone - 95 chars
- C4104022 | ABT Tap — the reader stays disarmed when the ABT Tap Product is not configured - 78 chars
- C4104023 | ABT Tap — an unreadable card presentation gives an error and the gate stays closed - 82 chars
- C4104025 | ABT Tap — an exit-capable gate opens for a deny-listed card but audits the tap invalid - 86 chars
- C4104028 | Barcode — a valid multi-use barcode is accepted with a green tick and the gate opens - 84 chars
- C4104029 | Barcode — a barcode on a mobile device screen validates the same as a printed one - 81 chars
- C4104036 | Barcode — a rail barcode failing the location check is treated valid when the fare is at least the £90 fallback - 111 chars
- C4104037 | Barcode — a rail barcode failing the location check is rejected when the fare is below the £90 fallback - 103 chars
- C4104039 | Barcode — an expiry between midnight and 4am shows the previous day and no time - 79 chars
- C4104042 | Barcode — a new barcode presented during a result screen is processed immediately - 81 chars
- C4104043 | Barcode — a successful validation posts a zero-fare BarcodeUsage transaction - 76 chars
- C4104044 | Barcode — a failed validation posts an event carrying the Unique ID and reason - 78 chars
- C4104046 | Barcode — a 3-Day Select ticket is valid on its start, additional and end dates - 79 chars
- C4104049 | Passback — a barcode re-presented after other transactions is still rejected within the window - 94 chars
- C4104050 | Passback — a card re-tapped within the passback time is declined with Declined Reason 20 - 88 chars
- C4104051 | Passback — a barcode presented on a second gateline head is rejected as passback - 80 chars
- C4104052 | Passback — a barcode presented after the passback window elapses is accepted - 76 chars
- C4104054 | Commissioning — Primary head is Entry/unpaid and Secondary head is Exit/paid (roles not swapped) - 96 chars
- C4104056 | Commissioning — correct gate width variant (Standard vs Wide) is installed - 74 chars
- C4104057 | Commissioning — one-wire homeLocation and zoneNo match the install spreadsheet - 78 chars
- C4104058 | Commissioning — Technician Location Settings match the install spreadsheet - 74 chars
- C4104059 | Router — each lane has a unique static WAN IP per the install spreadsheet - 73 chars
- C4104062 | Software Distribution — a software / configuration / barcode-data file downloads to the GV - 90 chars
- C4104063 | Software Distribution — a configuration file with a future activation date applies on that date - 95 chars
- C4104067 | Technician Menu — the session auto signs off after the inactivity timeout - 73 chars
- C4104070 | Location Settings — a no-comms condition is indicated when changing location without back-office comms - 102 chars
- C4104071 | Software Versions — the Software Versions screen lists all software versions - 76 chars
- C4104072 | Configuration Versions — the Configuration Versions screen lists all configuration versions - 91 chars
- C4104075 | Force Communications — a technician forces a comms session with the back office - 79 chars
- C4104091 | Power — the gate stays open when mains fails with a user inside the aisle - 73 chars
- C4104097 | BOS Comms — the GV keeps validating and queues audit data while the back office is unreachable - 94 chars
- C4104098 | BOS Comms — queued audit data uploads to CloudFare when comms is restored - 73 chars
- C4104099 | SaaS — a sustained Translink-network outage drives the GV to a communication-locked Out of Service state - 104 chars
- C4104100 | Comms — the GV updates CloudFare Last Communication at least every 15 minutes via the StaffList refresh - 103 chars
- C4104101 | Throughput — Primary and Secondary heads sustain back-to-back validations - 73 chars

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
