# HHD deep-audit — Batch D gap register entries

Q&A-register-style entries for the 3 `flagged-gap` cases from Batch D (suite 30285, sections
Supervisor / Technician). No Q-numbers assigned here — the human orchestrator merges these into
`proposals/**/gap-register.md` and assigns numbers there. Each entry needs an engineer answer before
the corresponding case can be considered grounded.

---

### Question: Can a Supervisor "act as an Operator" on the HHD (sign on, sign off, end an operator's
duty as a separate operator session)?

- **Category:** device capability / role behaviour (existence, not mechanism)
- **Case(s):** 4103924 — "Supervisor — act as Operator (sign on, sign off, end duty)"
- **Findings:** Searched FBD-100383 (Operator Hierarchy, raw text — 0 hits for "act as"/"acting"),
  FBD-100342 (User Claims), FBD-100320 (TID Management), and the full TFTS Requirements Matrix
  (`1_Requirements\TFTS Project Delivery Matrices & VCRMs\TFTS Requirements Matrix.xlsx`) for
  "act as operator" / "acting operator" / related phrasing. No requirement, design note, or ticket-
  format reference describes this capability for the HHD.
- **What's missing:** Either (a) a requirement/CR document not currently in the local library that
  describes this Supervisor capability, or (b) confirmation that the capability doesn't exist as
  described and the case is testing something invented in a prior authoring pass. Needs an engineer
  who knows the live HHD Supervisor menu to confirm whether "act as Operator" is a real menu option.

---

### Question: Does a Supervisor "authorise" an operator into break mode, or only override/end one
already in progress?

- **Category:** device capability / workflow direction (existence + direction of an already-real feature)
- **Case(s):** 4103925 — "Supervisor — authorise an operator break (ID entry and card)"
- **Findings:** TFTS Requirements Matrix confirms break mode is real: REQ-0305.0 (operator enters
  break mode unaided — no supervisor step described), REQ-0305.1 (operator leaves break mode by
  re-entering their own PIN), REQ-0360.0 (**"The device shall allow the Translink Supervisor to
  override operator break mode. The Translink operator who entered break mode will be signed off...
  Does not require the Translink operator's PIN."**), REQ-1137.0 (supervisor functions accessible via
  smartcard + manually-entered PIN, including while the device is in Operator Break Mode). All
  supervisor-related break-mode text found describes *ending/overriding* a break (with the operator
  signed off as a result) — none describes a supervisor *authorising* an operator to start or
  continue a break by ID+PIN or card, as the case's title and steps claim.
- **What's missing:** Confirmation of which behaviour is correct on the live system: (a) the case is
  right and there's an "authorise" workflow not captured in the requirement library, or (b) the case
  has the wrong verb/direction and should instead test the documented "Supervisor overrides break →
  operator signed off" behaviour (REQ-0360.0). If (b), this is also a candidate title/steps rewrite
  once confirmed — not just a gap marker.

---

### Question: How does a Technician connect the HHD's Bluetooth printer — is it genuinely a MAC-address
manual-entry-or-barcode-scan choice, and is that the correct mechanism?

- **Category:** device mechanism ("how", not "what" — outcome is real, exact steps unconfirmed)
- **Case(s):** 4103936 — "Technician — connect the printer (MAC entered or scanned)"
- **Findings:** REQ-0819.0 (TFTS Requirements Matrix) confirms the HHD hardware genuinely includes
  Bluetooth communications and barcode scanning as capabilities, so a Bluetooth-printer-pairing flow
  that can accept a scanned code is plausible. However, no requirement, design note, or ticket-format
  document in the local library describes the specific printer-connection workflow (MAC address
  manual entry vs. barcode-reader scan) for the HHD. FBD-100320 (TID/payment-device management) — the
  case's prior citation — does not cover printer pairing at all; it's exclusively about the Miura M020
  payment terminal.
- **What's missing:** A design note or requirement describing the HHD printer-commissioning screen, OR
  confirmation from an engineer who has commissioned a live HHD that this dual-path (manual MAC entry
  / scan) is accurate. Given the outcome (printer gets connected) is a reasonable inference from
  existing hardware capability, this is lower-risk than the other two gaps in this batch, but the
  specific mechanism is still unconfirmed.
