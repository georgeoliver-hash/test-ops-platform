# FBD-100236 — DESFire EV3 ABT Card Format (distilled)

**Source:** `Translink DESFire ABT Card Format Specification (FBD-100236) V6.00` (08 Nov 2021, Flowbird).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed. **No key values / secrets reproduced here** (test-env values live in ref [1] `Translink AV3 SAM & Scheme Card Keys Configuration`).
This is the **Account-Based Ticketing (ABT)** smartcard (NXP DESFire EV3), distinct from the legacy Mifare pre-printed cards in FBD-100250.

## Card structure (testable format rules)
- Two applications: **`ABT`** (AID `0x414254`) and **`TRK`** ABT Tracking (AID `0x54524B`, optional, for max security).
- **A terminal MUST reject any product that has the ABT application but is missing the ABT Tracking application.**
- ABT app files: **ABT Data** (#1, 32 bytes, MAC), **ABT Log** (#2, 32 bytes, backup — initially all-zero), **ABT SigFile** (#3, 8×32-byte records — first **4×32 bytes** hold the 1024-bit RSA signature). TRK app files: **TRK Data** (#10, 48 bytes, Full/encipher, initially all-zero) and **TRK TMAC** (#11, TransactionMAC, 12 bytes) auto-updated by the card on transaction commit.
- **Free read:** initial access conditions permit validation devices to **freely read** the ABT token (Access Rights #1 = Free Access, non-MACed); in that scenario **no data is written** to the card on validation (ABT Log not written).

## ABT Data field content (32 bytes)
- `VV` Version = `0x01`; `XD` Expiry Date = **yyyymmdd in BCD**; `OP` Operator Number = **`0x2057`** (Flowbird's Translink identifier); `PS` Printed Serial Number = **8 digit + check digit** (check via **BPay Modulus-10**), stored right-justified/zero-padded; `PA` padding = 7×`0x00`; `SA` Signing Algorithm = **`0x01` RSA1024**; `SV` Signing Key Reference (start at 0, increment on key change); `SL` Signature Length (in 32-byte blocks).
- PSNs are **allocated by Translink and must be unique**.

## Cryptography (assertable behaviour, not values)
- **Symmetric (AES-128, mandatory AV3 SAM during perso):** scheme keys **AbtRead** (secure read at validation), **AbtLog** (write ABT Log at validation), **AbtPerso** (issuer writes ABT Data + SigFile). All AES-128 **diversified with the Card UID**. SAM host keys (HostPerso/HostUsage/HostRFU) diversified with the **SAM UID** (`DIV_SAM(kv,uid)=TDEA_CBC_encipher(key=kv,msg=kv,iv=[0x88,sam_uid])`); HostRFU must not be all-zero.
- **Asymmetric:** ABT Data (32 bytes) **+ Card UID (8 bytes)** signed with private key → SigFile. Hash **SHA-256**, signature **RSA-1024** (deliberate perf/security trade-off). Terminal verifies with the **RSA public key stored on the terminal**.
- **TrkTMAC** key known **only to card + back office** (never to terminals) — used to prove an ABT product is genuine. On commit, TransactionMAC Counter + Value + initial/new TRK Data are sent to back office for authenticity check. Reading TRK data requires correct card authentication.

## Issue / registration
- Card Bureau sends a **registration record to ABT** for **Child, 24+, yLink** cards (not required for others). **yLink & 24+** are personalised — include **passenger name + email** at registration; expiry = end of concessionary period.
- Appendix A: Registered/Personalised by bureau — **24+** (Y/Y), **Adult** (N/N), **Child** (Y/N), **yLink** (Y/Y).

## Suite implications
- If an ABT/DESFire validation suite exists (likely GV/PV/HHD rail): assert **terminal rejects ABT-without-TRK** — a discrete security case.
- Assert **signature verification**: valid RSA1024/SHA-256 signature over ABT Data + Card UID → accept; tampered ABT Data or wrong Card UID → reject.
- Assert **free-read at validation writes nothing** to the card (ABT Log unchanged) under the initial access conditions.
- Assert **PSN Modulus-10 check-digit** validation and **Operator Number `0x2057`** gate (foreign-operator card rejected).
- Assert **Expiry Date (BCD yyyymmdd)** enforcement at validation.
- Registration-record coverage is largely a **bureau/back-office** concern (Child/24+/yLink only) — likely out of device-test scope; note as a BOS/ABT-integration gap rather than a device case.
- **No key material** belongs in TestRail/Gherkin — reference ref [1] by name only.
