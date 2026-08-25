# HHD deep-audit — Batch F — gap register entries

Q&A-register-style entries for the two `flagged-gap` cases in Batch F. No Q-numbers assigned here —
the human orchestrator merges these into the real `gap-register.md` and assigns numbers there.

---

**Question:** Does the HHD actually pair with an external printer by presenting an NFC chip — and if
so, on what hardware/model — or does every HHD use its own integrated printer for ticket printing?

**Category:** Device capability / possible cross-surface mix-up

**Case(s):** 4103995 ("Printer — the HHD pairs to a printer by presenting its NFC chip")

**Findings:**
- `REQ-0819.6` (TFTS Requirements Matrix): "The HHD shall be equipped with 2\" thermal printer" —
  i.e. an **integrated** printer, not an external unit to pair with.
- `FBD-100320` (TID Management) device matrix: HHD's only non-embedded/paired payment peripheral is the
  **Miura M020**, paired over **Bluetooth** — not NFC, and it's a payment terminal, not a printer.
- No document in the local requirements library (`REQS_DIR`) mentions an external printer, a
  Bluetooth/NFC printer accessory, or any "printer NFC chip" pairing procedure for any device type.
- `REQ-0819.8` mentions HHD short-range wireless "capable of communicating to an external payment card
  device to perform EMV and NFC payment transactions" — this is the M020 payment link, again not a
  printer.

**What's missing:** Confirmation that an external/NFC-paired printer variant exists for the HHD estate
at all. If it doesn't, this case may be describing a capability that was never built, or may be a
mislabelled/garbled version of the M020 pairing test (which already has its own case, 4104007, tagged
correctly to FBD-100320). If it does exist (e.g. a receipt-printer accessory not covered by this
requirements library), we need the real screen name, pairing mechanism, and a citation to add.

---

**Question:** What are the real Android OS versions the HHD is upgraded between (the case currently
asserts "OS 7" and "OS 8" specifically) — and is there a spec/CR that documents this specific upgrade?

**Category:** Unconfirmed specific value (device OS versioning)

**Case(s):** 4104002 ("Security — the HHD upgrades from OS 7 to OS 8")

**Findings:**
- `REQ-0569.0`: "The system will manage the distribution of the device operating system software and
  firmware updates" — confirms OS upgrades are a real, TMS-managed capability.
- `REQ-1618.0` / `REQ-3511.0`: "The HHD shall be capable of hosting an Android operating system" —
  confirms HHD runs Android generically, no version number given.
- No document in the local requirements library mentions "OS 7", "OS 8", or any specific Android
  version number for the HHD anywhere.

**What's missing:** The actual current/target OS versions in use on the live HHD estate (or in the
relevant CR/release notes, if this upgrade is a specific project milestone). Until confirmed, the case
should not assert a specific version pairing as fact — reworded precondition marks this GAP rather than
inventing/confirming the "OS 7 → OS 8" figures.
