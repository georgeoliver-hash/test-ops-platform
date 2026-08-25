# HHD deep-grounding audit — Batch E gap register entries

Q&A-register-style entries for cases flagged `flagged-gap` in this batch. No Q-numbers assigned —
the human orchestrator merges these into the real `gap-register.md`.

---

### Does a legacy "Old Barcode Redemption (BRS)" flow exist on Glider HHD?

- **Category:** Invented/unconfirmed capability (device × barcode-class mismatch)
- **Case(s):** C4103970 ("Old Barcode Redemption — a legacy BRS barcode is redeemed on Glider")
- **Findings:** Searched the full local requirements library by filename (`--find "BRS"`, `"barcode
  redemption"`, `"Old Barcode"`, `"legacy"`) and by content within FBD-100167, FBD-100317,
  FBD-100318, FBD-100483, and the "Barcode Acceptance on TFTS Devices" matrix doc. No document
  anywhere mentions a "BRS" flow or an "Old Barcode Redemption" concept. FBD-100317's device ×
  barcode matrix and the TFTS acceptance-matrix doc both show Glider HHD validates **multiple-use
  (Flowbird) barcodes offline only** and rejects every single-use barcode class ("Not Accepted —
  Error Message displayed"). FBD-100483 states outright: "Glider HHD does NOT use single-use
  functionality." This upgrades the prior lighter coherence-audit flag (which only asked "does a
  legacy BRS flow exist?") to a confirmed spec gap.
- **What's missing:** Either (a) a spec that actually defines a legacy BRS redemption mechanism on
  Glider HHD that simply isn't in the current requirements library, or (b) confirmation that this
  case describes a capability that does not exist and should be retired/rewritten to match what
  Glider HHD actually does (multi-use barcode validation per FBD-100167/FBD-100317).

---

### Is there a documented pass-type colour scheme on the HHD smartcard-inspection result screen?

- **Category:** Unconfirmed UI/screen detail
- **Case(s):** C4103972 (adult iLink → adult colour), C4103973 (child pass → child colour)
- **Findings:** Checked FBD-100236 (DESFire ABT card format), FBD-100250 (pre-printed smartcard
  format), the `HHD Inspection and Validation Design Note` (and its "Copy of" variant), and
  `Smartcard Use Matrix.xlsx`. None document a colour-coding scheme by passenger type on the
  inspection result screen; the Design Note only says wording "varies depending on smartcard" with
  no colour detail (screenshots referenced but not extractable as text).
- **What's missing:** The actual UX/screen-design reference (Overflow flow or a UI spec) that
  defines the adult vs child colour indicators, if one exists.

---

### Is the ~90-minute smartcard revalidation window a real, documented figure — or borrowed from the unrelated cEMV inspection MJT?

- **Category:** Unconfirmed configured value / possible cross-contamination between specs
- **Case(s):** C4103975 (within window → accepted, no revalidation), C4103976 (after window →
  offers revalidation)
- **Findings:** No spec documents a smartcard-inspection revalidation/passback window of 90
  minutes (or any other figure) for iLink/period-pass inspection. The only "~90 minute" figure
  found anywhere in the requirements library is the Glider/NIR **cEMV inspection Maximum Journey
  Time** in FBD-100651/FBD-100716 — a materially different mechanism (a bank-card penalty-fare
  matching window, not a smartcard revalidation window). Reusing that number here looks like it
  may have been copied across from the cEMV inspection cases in error — the exact kind of
  cross-section duplication the task brief flagged as a risk. Cases have been reframed to reference
  "the currently configured window" (assumed-knowledge precondition) rather than asserting an
  unconfirmed number.
- **What's missing:** The real spec/config source for the smartcard revalidation window (if
  distinct from the cEMV MJT), or confirmation that no such window exists for smartcard inspection
  at all (in which case these two cases may need re-scoping).

---

### Does CR78 "break mode" exist, and is smartcard inspection actually available in it?

- **Category:** Unconfirmed CR / feature existence
- **Case(s):** C4103977 ("Inspection is available in break mode")
- **Findings:** `--find "CR78"`, `--find "break mode"`, and `--find "break"` returned nothing
  relevant anywhere in the requirements library (the only "break" hit was an unrelated ETM
  configuration-mapping spreadsheet). No document describes a "break mode" operator sign-on state
  or a CR78 change request.
- **What's missing:** The CR78 change request document itself (may live outside the currently
  synced `_current` requirements folder, e.g. in a CR tracker not mirrored locally), or
  confirmation from the engineer that break mode is a live, named operator state and that
  smartcard inspection is available in it.
