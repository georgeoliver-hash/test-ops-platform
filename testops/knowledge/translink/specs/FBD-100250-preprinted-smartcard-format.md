# FBD-100250 — Smart Card Format for Translink Pre-Printed Cards (distilled)

**Source:** `Smart Card Format for Translink Preprinted Cards (FBD-100250) Issue 1.51` (30 Jul 2024, SJ).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed. **No key values reproduced** (diversified keys / master keys are secret).
This is the **legacy Mifare (Mikron)** pre-printed card format — SmartPass / Funded / Multi-Journey / rail travelcards — distinct from the DESFire ABT card (FBD-100236).

## Card physical/format model
- Mifare card = **16 sectors × 4 blocks × 16 bytes**. Sector 0 block 0 = read-only manufacture data (serial, serial-check, card size, card type, revision, batch, date code). **Block 3 of every sector** = Transport Key A + Access Conditions (`FF 07 80 00`) + Transport Key B.
- Blank cards ship with default transport keys (all-`FF` or `A0..A5`/`B0..B5`); manufacturer converts these to **diversified keys** unique per card (based on 4-byte serial + secret master, via `DivDLL.DLL fnDiversify`, dongle-metered). Serial passed to the DLL **reverse-order** to on-card storage.
- Product data is mirrored across a **primary + backup sector pair** (Sector 1↔5 for product, Sector 4↔8 for create-date/bus-number) — both copies must match.

## Card taxonomy (each has Card Type / Field ID / Group ID)
- **Fare Foregone** (Group `02`): Senior, War Pensioner, Blind, ROI Senior, 60+ — all Card Type `02`/hex `02` (deposit-flag hex `82`), Field IDs `40`–`44`.
- **Pupil (EA)** (Group `29`): EA Bus Pupil/FE, EA Rail Pupil/FE — Card Types dec 31–34, Field IDs `54`–`57`.
- **Funded** (Group `1C`): Partially Sighted, No DL, Learning Disability, DLA, yLink, PIPS, 24 Plus — Card Type dec 6, Field IDs `01`–`07`.
- **Corporate**: Staff, Staff Spouse, Dependants, Retired Staff, External, **NIR Gate Pass** (Parkeon card type 11 vs 14 corrected in Issue 1.49; on-card issue-record type `14`).
- **SmartLink / iLink / Ulsterbus Town Service / DayLink** (non-personalised, Group `13`/`27`/`29`/`2A`): Metro Multi-Journey (Inner/City/Extended, Adult/Child), Metro Travelcard, Ulsterbus Multi-Journey, iLink zones 1–4 + NW (Adult/Child), **aLink** (personalised), Belfast Visitors Pass (= same product as iLink), DayLink. Each carries a **Zone Bitmap** (e.g. iLink Z1=`80`, Z4=`E0`, NW=`04`).

## Testable data rules
- **Checksums (Appendix A):** three types, all must recompute — **LRC** (8-bit XOR, seeded `FFh`), **Smart Card CRC** (16-bit "egg-beater", seeded `11h` both bytes), **Customer CRC** (1-byte EOR, seed `FFh`) over the customer-detail area.
- **Date formats (Appendix B):** Create Date = 3-byte (dd/mm/yy + minutes-since-midnight); Start/Expiry = 2-byte (dd/mm/**yy**). **Year = offset from 1991**, wrapping every 16 years (0 = 1991/2007/2023…). Expiry rules are per-card and are prime edge-case fodder:
  - Funded: expiry = end of month of 60th birthday **or** 5 years from birth-month at issue, **whichever sooner**.
  - War Pensioner/Blind: end of month, 5 yrs from next birthday after issue. Senior/ROI Senior/60+: birthday-anchored (Senior start = later of 3mo-before-65th or scheme start; 60+ expiry = end of month of 65th birthday).
  - **EA Pupil/FE:** start always **1 Sept**, expiry always **30 June** (academic year).
  - TaxSmart: 5 yrs from month-end of issue. aLink: 1 yr from month-end. **NIR Gate Pass: expiry fixed `31 Dec 2099`**.
- **Multi-journey/day balance** encoding (BAL): 1→`0100`, 5→`0500`, 10→`0A00`, … 40→`2800`. Duration codes: 1 Week `0451`, 1 Month `0401`, 1 Year `0421`.
- **Printed Serial Number** = 8-digit, stored MSB→LSB; issue records use digits 11–17 of the printed number.

## Issue records (CSV to back office / SmarTrack)
- `130` Issue Record (fare-foregone/pupil/taxsmart), `142` Extended Issue Record (funded — includes NI number), `132` Pass Create Record, and for product-loaded SmartLink/iLink/UTS/DayLink a **`130` card-issue + `133` product-create** pair. Each has a fixed positional field list and per-card Field ID/Group ID/Class values. **Rule: never place a comma inside a quoted field.**

## Suite implications
- Card-format correctness is largely a **bureau/perso** concern, but device validation suites should assert the **read/decode contract**: correct Card Type/Field ID/Group ID → correct product; bad **LRC/CRC/Customer-CRC** → card rejected; **primary vs backup sector** mismatch handling.
- Highest-value device cases = **expiry-date logic** edge cases (academic-year EA cards, birthday-anchored concessions, NIR Gate Pass 2099, the **1991-offset / 16-year wrap** — a genuine boundary bug risk).
- Assert **zone bitmap** enforcement for iLink/aLink (right zone accepted, wrong zone rejected) and **multi-journey balance decrement**.
- Issue-record generation (`130/142/132/133`) is a **POS + BOS** coverage area — assert the correct record type + Field/Group/Class per card and the "no comma in quotes" rule; treat as POS-issue/BOS cases, not validator cases.
- **No key material or full byte-maps** into TestRail — reference this note + the spec instead.
