# PV coverage map — old suite (1,144) → new suite, for BOTH modes

Purpose (George): prove the new suite covers **every needed behaviour** from the old suite, **even
cases never run**, for **both Glider and Rail**. Run-data was used only to prioritise — coverage is
driven by the old-suite content. "Covered" = the behaviour is exercised by a new case (products /
passenger / valid-invalid / mode ride as variation lines + Glider/Rail Configurations).

## Smartcard Validation (both Glider + Rail — shared families, run under both Configurations)
| Old area (Glider AND Rail trees) | New case |
|---|---|
| Concession SmartPass (60+, Blind, Senior, ROI Senior, War Pensioner) valid+invalid | Validate a Concession SmartPass |
| Half Fares (DLA, Learning Disability, No Driving Licence, PIPS, Partially Sighted) | Validate a Half-Fare SmartPass |
| Metro Daylink (Adult/Child) | Validate a Metro Daylink smartcard |
| Metro Multi-Journey (City/Inner/Extended, Adult/Child) | Validate a Metro Multi-Journey smartcard |
| Metro Travelcard (Adult/Child) | Validate a Metro Travelcard |
| Ulsterbus Multi-Journey (Adult/Child) | Validate an Ulsterbus Multi-Journey smartcard |
| iLink Zones 1-4/NW + Belfast Visitor (Adult/Child) | Validate an iLink smartcard |
| aLink | Validate an aLink smartcard |
| yLink/24+ | Validate a yLink or 24+ smartcard |
| Translink Employee (Staff/Partner/Retired/External/Dependents) | Validate a Translink Employee smartcard |
| EA Smartpass — EA **Bus** (Glider) + EA **Rail** Pupil/FE | Validate an EA Smartpass (Pupil and FE) |
| Invalid reasons (Not Valid Location / Time / Expired / Represent / Unable / time band / hotlist) | Validation — invalid reasons displayed |
| Passback (smartcard, journeys/days left) | Validation — passback |
| Offline transaction | Validation — offline transaction |
| Machine Not In Service | Validation — machine not in service |

## Mode-specific
| Old area | Mode | New case |
|---|---|---|
| NIR Transfers (iLink/Belfast Visitor/Staff/aLink/EA transfers) | **Rail** | Rail — NIR transfer validation |
| Zone Validation (Inner Zone etc.) | **Rail** | Rail — zone validation |
| Glider TOO cEMV validation, daily taps, duplicate taps, flat fare | **Glider** | Glider TOO — tap-on-only flat-fare journeys |
| Glider transfers | **Glider** | Glider — transfers |
| cEMV enablement (route attribute / location / fare checks) | **Glider** | cEMV — tap enablement by route, location and fare |

## ABT / cEMV / lists / FEIG
| Old area | New case |
|---|---|
| ABT Card Presentation, Visa, Mastercard | ABT — contactless tap validation |
| ABT Declined Taps | ABT — declined or errored tap |
| BIN/Deny/Pilot list (validation-time rejection) | ABT — BIN, Deny and Pilot list handling |
| **Pilot List** (TMS config, registration mode, CSV↔DAT, Device Log Manager, apply zip, included/not) | **ABT — Pilot List management** *(addition)* |
| **Deny/BIN list** (delta + full updates, end-of-day, retries, removed-from-list; TIBU-26320/25745) | **ABT — Deny and BIN list updates** *(addition)* |
| **FEIG** (software versions/deployment/OTA, deploy-newest Transparent/PCA/OS) | **FEIG — reader software management** *(addition)* |
| **FEIG** (ITSO tap, valid/invalid EMV tap) | **FEIG — card reading** *(addition)* |
| ABT End-to-End | ABT — end-to-end journey to back office |

## Barcodes / Legacy / Card tech
| Old area | New case |
|---|---|
| Single-use barcode + validator screens | Barcode — single-use validation |
| Multi-Use Barcodes (HHD-produced, TVM-produced) | Barcode — multi-use validation |
| Legacy Support (journey-based, time-based) | Legacy smartcard support |
| MIFARE Classic EV1, DESFire | Card technology — MIFARE and DESFire |
| Passback (card tech) | Passback handling |
| Operating Times | PV operating times + Technician — operating times |

## Technician Menu / Non-Functional / Comms
| Old area | New case |
|---|---|
| Login/PIN/incorrect, Sign Off, Reboot | Technician Menu — login, sign off and reboot |
| Location Settings (view/edit/clear/fail/select) | Technician Menu — location settings |
| Brightness + Ambient Mode + Audio Volume | Technician Menu — display and audio settings |
| Software + Configuration Versions | Technician Menu — software and configuration versions |
| Force Communications | Technician Menu — force communications |
| Network Settings/Interfaces/Routing/ChangeIP | Technician Menu — network settings |
| Operating Times (engineer reconfigure) | Technician Menu — operating times |
| Power Interrupt / Power Management | Power interruption and recovery |
| **Scheduled Reboot at configured time** | **PV — scheduled reboot** *(addition)* |
| FEIG/PV software update via CloudFare TMS | PV to BOS — software and FEIG update via CloudFare TMS |
| Deny/BIN download & application to FEIG | PV to BOS — Deny and BIN list download |
| BOS Comms Upload | PV to BOS — transaction upload |
| **MERIT 24-hour heartbeat + heartbeat after sign-out** | **PV to BOS — MERIT heartbeat** *(addition)* |
| Daylight Saving Time changes | Daylight Saving Time change |

## HMI Screen Validation
Per-screen from the UX image folders: Validation Screens (Present/validate/ABT/barcode outcomes,
passback, machine-not-in-service) + Technician Menu screens. 49 cases. Old `Non-Functional / HMI /
Screens` (Smartcards/Barcodes/Technician) maps here.

## Deliberately EXCLUDED (not dropped coverage)
- **BOS/CloudFare web-admin** cases (Dashboard/Reports/Settings/Rules/CloudFare sign-on) — different
  system, not the PV device.
- **`Delete` / `Unsure (To Be Organised)`** housekeeping — triaged into the structure above; the
  duplicate `Delete/*` Glider TOO copies are superseded by the Glider TOO cases.
- **`Fixes/Changes / PV vX`** version fix-checks — folded into the owning functional case via Refs
  (`regression-register.md`); v5.0.0 defects TIBU-26320/25745 pinned on the Deny/BIN case.

## Full reconciliation of all 1,144 old cases (2026-06-08)
Every old case classified — zero genuine gaps:
| Bucket | Cases |
|---|---|
| Folded — validation matrix (product × Adult/Child × Valid/Invalid × Glider/Rail × passback/transfer) | 781 |
| Covered — ABT/cEMV/FEIG/lists | 47 |
| Covered — barcodes | 41 |
| Covered — legacy/card-tech/passback/invalid | 50 |
| Covered — technician/comms/power/DST/maintenance | 84 |
| Covered — HMI screens | 59 |
| Regression folded (Fixes/Changes, via Refs) | 32 |
| Excluded — Delete/housekeeping ("DONT RUN"/"to be deleted") | 44 |
| Excluded — BOS web-admin (different system) | 5 |
| Residual (Smartcard Validation Timings — covered by the performance case) | 1 |
| **Total** | **1,144** |

**781 (68%) are the single validation-matrix block** → 11 family cases + variation lines + Glider/Rail
Configurations. The trade-off (approved as full consolidation): those 781 are covered as variation
lines within a case, not 781 runnable rows — same behavioural coverage, less per-combination execution
granularity. Specific high-value products can be un-folded into their own rows on request.

## Status
All old-suite behaviour areas map to a new case, for both Glider and Rail. Gaps George flagged
(Pilot List, Deny/BIN management, FEIG, MERIT heartbeat, scheduled reboot) are the 6 cases in
`pv-additions.cases.yaml` — **pending push when TestRail is reachable** (network drop 2026-06-08).
After push: re-audit, then a final case-title-level diff old→new to confirm no behaviour orphaned.
