# TVM regression fold — register (the plan, not cases)

Read-only / propose-first. This maps the old **Fixes/Changes** regression suites — **Kiosk 22274
(345)** and **Astreo 22279 (296)**, **641 rows** — onto the new `**NEW** TVM Test Suite` (30284).
It is a **fold plan**, not authored cases.

Governing rule (`docs/gherkin-standard.md` "Pinning past defects", `docs/test-practices.md`): a fixed
defect is pinned **preferentially by folding a step + the defect Ref into the functional case that
owns the behaviour**, organised **by behaviour, not by the release it was fixed in**. A dedicated
`@regression` case is written **only** when the scenario has no natural functional home. The old
suites are release-versioned (`5.3.1`, `4.0.0.80`, …) — exactly the anti-pattern; we re-home by
behaviour. Old suites stay read-only; "fold" = add the assertion + `Refs: TIBU-#####` to the target
case in 30284, never modify/carry the old case.

Evidence: title+ref scan of both suites (scratchpad dumps; method in `cross-tab.md`). The two suites
overlap heavily — the same defect (e.g. `EMV only mode is not applied`, `Tapping European card
freezes`, the barcode-API user stories) recurs across versions **and** across both suites; count once
per behaviour when folding.

## Fold map — defect theme → new functional area / case (via Refs)

| Defect theme (old Fixes/Changes) | Rows (K+A) | New area it folds into (structure.md) | Fold vs dedicated | Representative Refs to carry |
|---|---:|---|---|---|
| EMV-only mode not applied from CloudFare; ChipDNA config not applied; card reader inactive/freezes on EU/intl tap; card top-ups missing in Merit; TID/TK mgmt | ~48 | **Payments — EMV / Contactless** | fold | TIBU-13795, TIBU-14179, UKCUKTODM-3907, TIBU-13119, TIBU-14030, TIBU-13559, FBD-100320/100353 |
| Note polymer-vs-paper acceptance, King Charles III notes, change voucher / IOU when low coin change, coins-then-note reject, float-by-hopper report, £1 coin reporting | ~19 | **Payments — Cash** (+ Astreo BNR/change leaf; Kiosk coin-hopper leaf) | fold | TIBU-13371, TIBU-13757, TIBU-14571, TIBU-14718, TIBU-19908, TIBU-19995 |
| Smartpass validation (60+/Senior/Dependents/DLA/Blind), iLink/Daylink top-up, yLink product/ticket-format, smartcard mini-statement fields, unrecognised-card timeouts, reader unresponsive, quarantined smartcard audits | ~103 | **Smartcards & ABT** | fold | TIBU-13603, TIBU-13572, TIBU-14079, TIBU-13721, TIBU-18887, UKCUKTODM-3925, REQ-2147 |
| Barcode encode/encrypt (AES/keys/zones), type B/D/E/U/H/S validation & display, single-use vs disabled, offline redemption to Core3, long-ticket barcode length, Glider barcode templates, integrated barcode API rollout | ~107 | **Barcode Redemption (single-use)** | fold | TIBU-14395, TIBU-14096, TIBU-21582, TIBU-21583, TIBU-13385, FBD-100167/100317/100483 |
| Cross-Border/NIR product availability & valid-from/to dates, 3-Day select day choice, popular-journey lock-up, ticket templates/logo/spacing/overlap, DayTracker format, collect-ticket info, product-description mapping, Ulsterbus-only destinations, home-location product filtering | ~222 | **Sales — Tickets** (+ mode leaves) / **Sales — Collection & Mini Statement** / **Ticket Formats & Receipts** | fold | TIBU-13727, TIBU-14568, TIBU-14200, TIBU-16742, TIBU-18348, TIBU-18445, TIBU-13361, TIBU-14611 |
| Print service crash on missing template, TL80 template removal on topology, offline print list, healthcheck rollback, version rollback on install | ~13 | **Ticket Formats & Receipts** / **Degraded & Resilience** | fold | TIBU-19247, TIBU-19121, TIBU-3847, TIBU-14966, UKCAFTVM-3196 |
| Teltonika modem config, screen-background via TMS, GFTS config ordering, legacy-stages file config, mode update from TMS | ~13 | **Commissioning & Deployment** | fold | TIBU-13039, TIBU-21634, TIBU-2892, UKCAFTVM-66 |
| Sporadic transient Out-of-Service on Back/Cancel, TMS comms-test no success message, location-change destination delay, mode config for a Kiosk | ~18 | **EMS / TMS Maintenance** | fold | TIBU-13118, TIBU-13080, TIBU-14678, TIBU-13330 |
| Red Status LED in UPS/power-cycle mode, machine stuck in Burglary mode, Out-of-Order red light strip | ~13 | **EMS Maintenance — Alarmboard & Enclosure (Kiosk only)** (status-LED surface shared) | fold | TIBU-13474, TIBU-13993, TIBU-14965, TIBU-13121 |
| Missing audit data, offline-transaction mechanism + reprocessing at intervals, service-timeout breaks offline records | ~8 | **Comms / SaaS / Heartbeat** | fold | UKCAFTVM-3157, TIBU-3843, TIBU-3852, TIBU-14015, FBD-100266/100359 |
| Error-screen 3s timeout, log-failure messages/body, healthcheck reboot | ~9 | **Degraded States & Error Management** | fold | TIBU-2956, TIBU-13977, TIBU-14081, TIBU-14966 |
| Language update files; name-wrapping/legacy-stop name display; old logo on UX screens | ~9 | **Screensaver/Multi-modal & Language** / **Ticket Formats** / **Usability** | fold | TIBU-13558, TIBU-17002, TIBU-21279, TIBU-13925, UKCAFTVM-3126 |
| Dependents/Smartpass CloudFare time-rule; unique-ID sequence not hex; time-sync settings | ~10 | **Smartcards & ABT** / **Commissioning** (unique-id → 5602 C2628938 "TVM Unique Identifier") | fold | TIBU-4307, TIBU-14540, REQ-2147 |

**Folds into an existing area: ~608 of the 641 rows** (≈95%), across the 9 functional families above.

## Genuinely un-homeable → candidate `@regression` cases (write only these)

Two cross-cutting stability/integrity themes have **no single functional owner** — the behaviour spans
every sale/flow rather than one feature, so a folded step wouldn't naturally live anywhere. Author as
dedicated `@regression` cases in the REGRESSION section, each pinning its defect cluster via Refs:

1. **Audit-time integrity** — the audited transaction time must equal the printed time, and a sale
   made near midnight must be audited to a single service day. No functional case owns cross-flow
   timestamp consistency. Refs: **TIBU-4606** (minute discrepancy printed vs audited), **TIBU-17730**
   (transaction spread over 2 days), **TIBU-19599** (time-sync settings).
2. **Reboot / crash recovery (Win10 stability)** — after an unexpected/health-check reboot the TVM
   must return to the Sales home screen with CardPaymentService and SalesApp available, not stick on
   "Please Wait" or go Out of Service. A stability regression cluster, not a feature. Refs:
   **TIBU-27809** (random reboots), **TIBU-26882/26884/26892/26935**, **TIBU-29223/29251**,
   **TIBU-18602/18716** (frozen on boot/print), **TIBU-14966** (healthcheck reboot/rollback).
   (Borderline — could fold into *Degraded / Resilience*; flagged as candidate for George to decide.)

## Drop — NOT test cases (do not carry, do not turn into regression cases)

~20–25 rows are dev/build/CI/spike/plumbing artefacts with no black-box behaviour of their own;
their user-observable outcome is already covered by the functional folds above:
- **Build/CI/admin:** TIBU-13064 (release build), TIBU-5164 (Jenkins), TIBU-13844 (release 3.0.74),
  TIBU-13528 (fix confluence-endpoint typos), TIBU-13533/13499 ([Hotfix] un/encrypt configs),
  and the `Delete` / `**Needs deleting` / `No Release` / `Do not Use` holding sections.
- **Spike/investigation:** TIBU-5009 (Java upgrade options), TIBU-20991 ([Spike] long-ticket barcode
  print — the *outcome* folds to Ticket Formats/Barcode), TIBU-14757/14758/14759 ([SPIKE] field
  diagnosis — the underlying "not reading/updating smartcards" folds to Smartcards & ABT).
- **Internal API plumbing user stories** whose behaviour is observable only through the barcode/print
  stack already covered by *Barcode Redemption* + *Ticket Sale*: TIBU-13173/13174/13175/13176 (AES
  encrypt/decrypt/key store), TIBU-13319 (barcode validator), TIBU-3660/3662/3665/3669/3708/3710/
  3715/3723/3737 (Validate/Redeem/Print/Log-Failure API endpoints), TIBU-13055 (secure key store).
  Pin the *behaviour* (a barcode ticket redeems / prints / logs a failure) via Refs on the functional
  case; do not author one case per endpoint.

## Summary
- **641** old regression rows (Kiosk 345 + Astreo 296), heavily duplicated across versions/suites.
- **≈608 (≈95%) fold into 9 existing functional areas** via Refs — no new cases; pin the defect on
  the functional case that owns the behaviour.
- **2 themes need a dedicated `@regression` case** (audit-time integrity; reboot/crash recovery).
- **~20–25 rows are non-test dev/build/spike/plumbing artefacts** — drop; their behaviour is already
  covered by the functional folds.
