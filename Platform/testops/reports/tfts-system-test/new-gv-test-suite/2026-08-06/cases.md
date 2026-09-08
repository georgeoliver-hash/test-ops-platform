# Cases — TFTS - System Test / **NEW** GV Test Suite

- Generated: 2026-08-06T10:15:22.233887+00:00
- Total cases: 125

| Case | Title | Section | Linked refs | Has steps |
|---|---|---|---|---|
| C4104011 | ABT Tap — a valid contactless card tap succeeds and the gate opens (Visa Debit) | Functional / ABT cEMV Taps | FBD-100658, FBD-100690 | yes |
| C4104012 | ABT Tap — a successful tap posts an ABT audit record with zero revenue | Functional / ABT cEMV Taps | FBD-100658, FBD-100690 | yes |
| C4104013 | ABT Tap — the TapId is composed of DeviceId, TID and UNIX timestamp | Functional / ABT cEMV Taps | FBD-100658 | yes |
| C4104014 | ABT Tap — an expired card is declined with Declined Reason 1 | Functional / ABT cEMV Taps | FBD-100658, FBD-100690 | yes |
| C4104015 | ABT Tap — a card failing ODA is declined with Declined Reason 3 | Functional / ABT cEMV Taps | FBD-100658, FBD-100690 | yes |
| C4104016 | ABT Tap — a card on the BIN List is declined with Declined Reason 15 | Functional / ABT cEMV Taps | FBD-100658, FBD-100690 | yes |
| C4104017 | ABT Tap — a card on the Deny List is rejected in entry mode with Declined Reason 2 | Functional / ABT cEMV Taps | FBD-100658, FBD-100690 | yes |
| C4104018 | ABT Tap — a re-tap within the passback window is declined with Declined Reason 20 | Functional / ABT cEMV Taps | FBD-100658, FBD-100690 | yes |
| C4104019 | ABT Tap — an offline transaction is accepted and queued for the back office | Functional / ABT cEMV Taps | FBD-100658, FBD-100690 | yes |
| C4104020 | ABT Tap — the reader stays disarmed when the route ABT Type is not Tap On Tap Off | Functional / ABT cEMV Taps | FBD-100690 | yes |
| C4104021 | ABT Tap — the reader stays disarmed when the home location is outside the Northern Ireland Zone | Functional / ABT cEMV Taps | FBD-100690 | yes |
| C4104022 | ABT Tap — the reader stays disarmed when the ABT Tap Product is not configured | Functional / ABT cEMV Taps | FBD-100690 | yes |
| C4104023 | ABT Tap — an unreadable card presentation gives an error and the gate stays closed | Functional / ABT cEMV Taps | FBD-100690 | yes |
| C4104024 | ABT Tap — a Maestro card is not accepted at the GV | Functional / ABT cEMV Taps | FBD-100690 | yes |
| C4104025 | ABT Tap — an exit-capable gate opens for a deny-listed card but audits the tap invalid | Functional / ABT cEMV Taps | FBD-100658, FBD-100690 | yes |
| C4104026 | ABT Tap — an entry-configured gate audits the tap as a Tap On | Functional / ABT cEMV Taps | FBD-100658, FBD-100690 | yes |
| C4104027 | ABT Tap — an exit-configured gate audits the tap as a Tap Off | Functional / ABT cEMV Taps | FBD-100658, FBD-100690 | yes |
| C4104418 | ABT Tap — a valid contactless card tap succeeds and the gate opens (Visa Credit) | Functional / ABT cEMV Taps | FBD-100658, FBD-100690 | yes |
| C4104419 | ABT Tap — a valid contactless card tap succeeds and the gate opens (Mastercard Debit) | Functional / ABT cEMV Taps | FBD-100658, FBD-100690 | yes |
| C4104420 | ABT Tap — a valid contactless card tap succeeds and the gate opens (Mastercard Credit) | Functional / ABT cEMV Taps | FBD-100658, FBD-100690 | yes |
| C4104028 | Barcode — a valid multi-use barcode is accepted with a green tick and the gate opens (Adult) | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104029 | Barcode — a barcode on a mobile device screen validates the same as a printed one | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104030 | Barcode — a TVM-produced barcode validates at the GV | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104031 | Barcode — an HHD-produced barcode validates at the GV | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104032 | Barcode — a route/location-only failure gives a yellow question mark | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104033 | Barcode — a failed validation gives a red cross with a reason | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104034 | Barcode — an already-validated barcode is rejected | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104035 | Barcode — an expired barcode is rejected | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104036 | Barcode — a rail barcode failing the location check is treated valid when the fare is at least the £90 fallback | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104037 | Barcode — a rail barcode failing the location check is rejected when the fare is below the £90 fallback | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104039 | Barcode — an expiry between midnight and 4am shows the previous day and no time | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104040 | Barcode — an expiry just after 4am shows the same day with a time | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104041 | Barcode — the read-to-beep response is within one second | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104042 | Barcode — a new barcode presented during a result screen is processed immediately | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104043 | Barcode — a successful validation posts a zero-fare BarcodeUsage transaction | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104044 | Barcode — a failed validation posts an event carrying the Unique ID and reason | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104045 | Barcode — the GV validates multi-use barcodes | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104046 | Barcode — a 3-Day Select ticket is valid on its start date | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104047 | Barcode — a barcode encoded for bus mode only is rejected on a rail gate | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104421 | Barcode — a valid multi-use barcode is accepted with a green tick and the gate opens (Child) | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104422 | Barcode — a valid multi-use barcode is accepted with a green tick and the gate opens (3-Day Select) | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104423 | Barcode — a valid multi-use barcode is accepted with a green tick and the gate opens (1-3 Off Day Return) | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104424 | Barcode — a valid multi-use barcode is accepted with a green tick and the gate opens (24+) | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104425 | Barcode — a valid multi-use barcode is accepted with a green tick and the gate opens (Ylink) | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104426 | Barcode — a valid multi-use barcode is accepted with a green tick and the gate opens (Concession) | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104427 | Barcode — a valid multi-use barcode is accepted with a green tick and the gate opens (Half Fare) | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104428 | Barcode — a valid multi-use barcode is accepted with a green tick and the gate opens (Day Tracker) | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104429 | Barcode — a valid multi-use barcode is accepted with a green tick and the gate opens (Unemployed Day Return) | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104430 | Barcode — a 3-Day Select ticket is valid on an additional date within its validity | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104431 | Barcode — a 3-Day Select ticket is valid on its end date | Functional / Multi-Use Barcode Validation | FBD-100167 | yes |
| C4104048 | Passback — a barcode re-presented within the passback window is rejected | Functional / Passback | FBD-100167 | yes |
| C4104049 | Passback — a barcode re-presented after other transactions is still rejected within the window | Functional / Passback | FBD-100167 | yes |
| C4104050 | Passback — a card re-tapped within the passback time is declined with Declined Reason 20 | Functional / Passback | FBD-100658, FBD-100690 | yes |
| C4104051 | Passback — a barcode presented on a second gateline head is rejected as passback | Functional / Passback | FBD-100167 | yes |
| C4104052 | Passback — a barcode presented after the passback window elapses is accepted | Functional / Passback | FBD-100167 | yes |
| C4104053 | Commissioning — both GV heads boot into service after live software load | Functional / Commissioning & Router | FBD-100654 | yes |
| C4104054 | Commissioning — Primary head is Entry/unpaid and Secondary head is Exit/paid (roles not swapped) | Functional / Commissioning & Router | FBD-100654 | yes |
| C4104055 | Commissioning — SkyLane interface firmware is HF03 | Functional / Commissioning & Router | FBD-100653, FBD-100654 | yes |
| C4104056 | Commissioning — correct gate width variant (Standard vs Wide) is installed | Functional / Commissioning & Router | FBD-100654 | yes |
| C4104057 | Commissioning — one-wire homeLocation and zoneNo match the install spreadsheet | Functional / Commissioning & Router | FBD-100654 | yes |
| C4104058 | Commissioning — Technician Location Settings match the install spreadsheet | Functional / Commissioning & Router | FBD-100654 | yes |
| C4104059 | Router — each lane has a unique static WAN IP per the install spreadsheet | Functional / Commissioning & Router | FBD-100653 | yes |
| C4104060 | Router — SkyLane at .200 with eth0 gateway .0.1 and a port-80 NAT rule | Functional / Commissioning & Router | FBD-100653 | yes |
| C4104061 | Router — the router admin password is set (not blank) | Functional / Commissioning & Router | FBD-100653 | yes |
| C4104062 | Software Distribution — a software / configuration / barcode-data file downloads to the GV | Functional / Commissioning & Router | FBD-100654 | yes |
| C4104063 | Software Distribution — a configuration file with a future activation date applies on that date | Functional / Commissioning & Router | FBD-100654 | yes |
| C4105407 | Boot — uncommissioned plinth shows Machine Not Commissioned (Gate) | Functional / Commissioning & Router | — | yes |
| C4104064 | Technician Sign On — valid technician card reaches the Technician Menu | Functional / Technician Menu | FBD-100654 | yes |
| C4104065 | Technician Sign On — an invalid PIN is rejected | Functional / Technician Menu | FBD-100654, REQ-0050 | yes |
| C4104066 | Technician Sign On — an abandoned sign-on returns to the idle screen | Functional / Technician Menu | FBD-100654 | yes |
| C4104067 | Technician Menu — the session auto signs off after the inactivity timeout | Functional / Technician Menu | FBD-100654, REQ-3129 | yes |
| C4104068 | Technician Menu — a technician navigates the menu pages | Functional / Technician Menu | FBD-100654 | yes |
| C4104069 | Location Settings — a technician sets the GV location | Functional / Technician Menu | FBD-100654 | yes |
| C4104070 | Location Settings — a no-comms condition is indicated when changing location without back-office comms | Functional / Technician Menu | FBD-100654 | yes |
| C4104071 | Software Versions — the Software Versions screen lists all software versions | Functional / Technician Menu | FBD-100654 | yes |
| C4104072 | Configuration Versions — the Configuration Versions screen lists all configuration versions | Functional / Technician Menu | FBD-100654 | yes |
| C4104073 | Display Brightness — a technician adjusts the screen brightness | Functional / Technician Menu | FBD-100654, REQ-0511 | yes |
| C4104074 | Audio Volume — a technician adjusts the audio volume | Functional / Technician Menu | FBD-100654, REQ-0511 | yes |
| C4104075 | Force Communications — a technician forces a comms session with the back office | Functional / Technician Menu | FBD-100266, FBD-100654, REQ-0348 | yes |
| C4105395 | Technician Sign On — PIN entry back returns to Login Screen | Functional / Technician Menu | — | yes |
| C4105396 | Technician Menu — Sign Off returns to Home Screen | Functional / Technician Menu | — | yes |
| C4105397 | Location Settings — selecting a Home Location returns to Edit | Functional / Technician Menu | — | yes |
| C4105398 | Location Settings — unavailable Home Location list shows Fail screen | Functional / Technician Menu | — | yes |
| C4105399 | Location Settings — Edit Cancel returns to Gate | Functional / Technician Menu | — | yes |
| C4105400 | Location Settings — entering details into a cleared field returns to Edit | Functional / Technician Menu | — | yes |
| C4105401 | Location Settings — Edit - Clear Cancel returns to Gate | Functional / Technician Menu | — | yes |
| C4105402 | Network Interfaces — Details returns to Network Interfaces | Functional / Technician Menu / Network Settings | — | yes |
| C4105403 | Network Interfaces — FecDetails ChangeIP navigation | Functional / Technician Menu / Network Settings | — | yes |
| C4105404 | Network Interfaces — Network Routing Table returns to Network Interfaces | Functional / Technician Menu / Network Settings | — | yes |
| C4105405 | Network Interfaces — back returns to Home Screen | Functional / Technician Menu / Network Settings | — | yes |
| C4105406 | Tests and Diagnostics — back returns to Home Screen | Functional / Technician Menu / Tests & Diagnostics | — | yes |
| C4104076 | Idle Screen — Present Card or Barcode | Non-Functional / HMI Screens | FBD-100348 | yes |
| C4104077 | Idle Screen — Not In Service | Non-Functional / HMI Screens | FBD-100348 | yes |
| C4104078 | Error Screen — Re-present Card | Non-Functional / HMI Screens | FBD-100348 | yes |
| C4104079 | Error Screen — Not Valid At This Location | Non-Functional / HMI Screens | FBD-100348 | yes |
| C4104080 | Error Screen — Invalid Time Of Day | Non-Functional / HMI Screens | FBD-100348 | yes |
| C4104081 | Error Screen — Product Expired | Non-Functional / HMI Screens | FBD-100348 | yes |
| C4104082 | Error Screen — Faulty Card | Non-Functional / HMI Screens | FBD-100348 | yes |
| C4104083 | Error Screen — Not Accepted | Non-Functional / HMI Screens | FBD-100348 | yes |
| C4104084 | Passback Screen — Card Already Validated | Non-Functional / HMI Screens | FBD-100167, FBD-100690 | yes |
| C4104085 | Success Screen — Successful | Non-Functional / HMI Screens | FBD-100348 | yes |
| C4104086 | Barcode Error Screen — Barcode Already Validated | Non-Functional / HMI Screens | FBD-100167 | yes |
| C4104087 | Barcode Error Screen — Barcode Has Expired | Non-Functional / HMI Screens | FBD-100167 | yes |
| C4104088 | Barcode Error Screen — Barcode Not Valid At This Location | Non-Functional / HMI Screens | FBD-100167 | yes |
| C4104089 | Barcode Error Screen — Barcode Type Invalid | Non-Functional / HMI Screens | FBD-100167 | yes |
| C4104090 | Barcode Success Screen — Barcode Use | Non-Functional / HMI Screens | FBD-100167 | yes |
| C4104111 | Barcode Error Screen — Barcode Not Valid At The Current Time | Non-Functional / HMI Screens | FBD-100167 | yes |
| C4104112 | Barcode Error Screen — Barcode Not Valid On This Service | Non-Functional / HMI Screens | FBD-100167 | yes |
| C4104091 | Power — the gate stays open when mains fails with a user inside the aisle | Non-Functional / Resilience | FBD-100348 | yes |
| C4104092 | Power — a power loss of two seconds or less does not force a reboot | Non-Functional / Resilience | FBD-100348, TIBU-14160 | yes |
| C4104093 | Emergency Release — the Emergency Release Button opens the gate | Non-Functional / Resilience | FBD-100348, TIBU-16813, TIBU-18635 | yes |
| C4104094 | Heartbeat — loss of a validator heartbeat raises a major fault | Non-Functional / Resilience | FBD-100266, FBD-100348 | yes |
| C4104095 | Power-up — the gate is Out of Service until both validators communicate | Non-Functional / Resilience | FBD-100348 | yes |
| C4104096 | Mains restore — the gate returns to its previous operational mode | Non-Functional / Resilience | FBD-100348 | yes |
| C4104097 | BOS Comms — the GV keeps validating and queues audit data while the back office is unreachable | Non-Functional / Resilience | FBD-100263, FBD-100359 | yes |
| C4104098 | BOS Comms — queued audit data uploads to CloudFare when comms is restored | Non-Functional / Resilience | FBD-100263, FBD-100359, TIBU-16455, TIBU-17104, TIBU-18566 | yes |
| C4104099 | SaaS — a sustained Translink-network outage drives the GV to a communication-locked Out of Service state | Non-Functional / Resilience | FBD-100359 | yes |
| C4104100 | Comms — the GV updates CloudFare Last Communication at least every 15 minutes via the StaffList refresh | Non-Functional / Resilience | FBD-100266, TIBU-18310 | yes |
| C4104101 | Throughput — Primary and Secondary heads sustain back-to-back validations | Non-Functional / Resilience | FBD-100348, TIBU-16221, TIBU-18597, TIBU-21005 | yes |
| C4104102 | Smoke — both heads boot into service | Smoke | FBD-100348, FBD-100654 | yes |
| C4104103 | Smoke — a valid card opens the gate with a success screen and beep | Smoke | FBD-100348, FBD-100690 | yes |
| C4104104 | Smoke — a valid multi-use barcode opens the gate with a success screen | Smoke | FBD-100167 | yes |
| C4104105 | Smoke — an immediate re-present of the same card is rejected as passback | Smoke | FBD-100167, FBD-100690 | yes |
| C4104106 | Smoke — a technician can sign on to the Technician Menu | Smoke | FBD-100654 | yes |
| C4104038 | ZZ_DELETE_REVIEW - Barcode — a barcode validated on one gate head is rejected on another head of the same gateline | delete | FBD-100167 | yes |
