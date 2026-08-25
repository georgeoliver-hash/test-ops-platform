# PV suite — proposed structure (test-type-first, Glider + Rail Configurations)

Target `**NEW** PV-Acceptance Test Suite` (30255). Consolidate the old 1,144 → ~150, same coverage +
more (gaps the old suite exposes), neater, run under Glider/Rail Configurations.

```
**NEW** PV-Acceptance Test Suite           ← Configurations: Glider · Rail
│
├─ SMOKE                                    present a valid smartcard → validates; invalid → reason
│
├─ FUNCTIONAL
│   ├─ Smartcard Validation                 one case per product family (valid + invalid), with
│   │     Adult/Child + product as variation lines. Families: Concession SmartPass, Half Fare,
│   │     Metro Daylink, Metro Multi-Journey (zones), Metro Travelcard, Ulsterbus Multi-Journey,
│   │     iLink (+ Belfast Visitor), aLink, yLink/24+, Employee Smartcards, EA Pupil/FE.
│   ├─ Validation Outcomes                   the shared invalid/edge reasons once: Not Valid At This
│   │     Location, Invalid Time Of Day, Product Expired, Represent Card, Unable to Validate,
│   │     outside time band, hotlisted, Passback (journeys left), Machine Not In Service.
│   ├─ ABT / cEMV (Glider)                    tap success/declined, BIN/Deny/Pilot lists, cEMV
│   │     enablement (route/location/fare checks), Glider TOO daily taps, Glider transfers.
│   ├─ Barcodes                               single + multi-use, HHD- & TVM-produced, barcode screens.
│   ├─ Legacy & Card Tech                     Legacy (journey/time-based), MIFARE Classic EV1, DESFire,
│   │     Passback, Invalid Smartcard, Operating Times.
│   ├─ Rail-specific                          NIR Transfers, Zone Validation, EA Rail Pupil/FE.
│   └─ Technician Menu                        login/PIN, Location, Brightness/Ambient, Audio, Versions,
│         Force Comms, Network, Power, Operating Times, DST.
│
├─ NON-FUNCTIONAL
│   ├─ Power Interrupt / Power Management
│   ├─ Comms / BOS (PV↔BOS: software/FEIG update via CloudFare TMS, Deny/BIN download, upload)
│   └─ Daylight Saving Time changes
│
├─ HMI SCREEN VALIDATION                      per-screen from the UX images (Validation + Technician
│         Menu) — one case per screen, cite image + screen name.
│
└─ REGRESSION                                 fold `Fixes/Changes / PV vX` defects into the owning
          case via Refs; dedicated case only where nothing covers it.
```

**Mode handling:** shared validation authored once, run under Glider + Rail Configurations; Rail-only
(NIR Transfers, Zone) and Glider-only (TOO/cEMV) in their own sections. **Excluded:** BOS web-admin
cases; `Delete`/`Unsure` housekeeping (triaged, not carried). Variations (product, Adult/Child,
valid/invalid reason) ride as data-variation lines per `docs/test-practices.md`.
