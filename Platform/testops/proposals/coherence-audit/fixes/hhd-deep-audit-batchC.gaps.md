# HHD Deep Audit — Batch C gap register entries

Q&A-register-style entries for every flagged-gap case in Batch C (suite 30285, sections Top-Ups,
Penalty Warning & Fares, Sign On & Session, Operator). No Q-numbers assigned — the orchestrator
merges these into `proposals/**/gap-register.md` and assigns numbers. Each entry: question,
category, case id(s), findings, what's missing.

---

### 1. Does the HHD have a manual, operator-menu-driven "penalty warning / penalty fare" function at all?

- **Category:** Behaviour-existence gap (POSSIBLE DESIGN/SPEC BUG or suite invention).
- **Case IDs:** 4103893, 4103894, 4103895, 4103896, 4103897, 4103898, 4103899, 4103900, 4103921.
- **Findings:** FBD-100716 (Revenue Inspection Device spec — the only spec covering HHD
  penalty/inspection behaviour) describes exactly one mechanism: the HHD's Miura M020 performs a
  **cEMV bank-card inspection**; if no matching travel tap exists within the Maximum Journey Time,
  the **ABT back office** automatically charges a "**Standard Fare**" at End-of-Day settlement — no
  operator action, no printed ticket, no whitelist, no waybill entry. A full-text search of
  FBD-100716 for "penalty warning", "whitelist", and "waybill" returned nothing beyond one summary
  line ("paper ticket issues, smartcard inspections and penalty fares/warnings issued" — a Revenue
  Inspectors *report* rollup, not a device action). The same searches against FBD-100651 (Glider
  TOO), FBD-100690 (NIR TOTO), and FBD-100658 (ABT Audit) found nothing either. FBD-100690 does use
  "Penalty Fare" as an **icon label** shown in a customer's Journey History for an automatically
  charged max fare — again the automated back-office outcome, not an operator-triggered device
  action.
- **What's missing:** Either (a) there is a separate, older/legacy manual penalty-issuance function
  on the HHD (pre-dating or running alongside the cEMV Standard Fare automation) that isn't in the
  local requirement library, in which case its spec/FBD number, ticket format, whitelist rule, and
  waybill treatment need to be supplied; or (b) this entire section describes invented
  functionality and should be rewritten to test the real, documented cEMV inspection UX (RID List
  check, Success/"Card on RID List"/"Card Declined" screens, distinct audio tones, event codes
  5008-5013) instead. Need an engineer to confirm which.

---

### 2. Is there an HHD-specific sign-on / sign-off UX design document anywhere?

- **Category:** Missing source document.
- **Case IDs:** 4103901, 4103902, 4103903, 4103905, 4103906, 4103909, 4103910, 4103911.
- **Findings:** These cases cite FBD-100383 ("TFTS Operator Hierarchy") for sign-on mechanics
  (manual/smartcard sign-on, invalid-credentials rejection, lockout after N attempts + "Device
  Locked" screen, duty number entry, Message of the Day / Word & Colour of the Day with
  "Unavailable" fallbacks, sign-off, inactivity auto-sign-off, forced sign-off on docking). A
  full-text search of FBD-100383 for sign-on, PIN, duty, lockout, "Device Locked", and "Message of
  the Day" returns **zero hits** — the document is entirely the CloudFare operator/location
  hierarchy tree (routes/products/config inheritance per depot), unrelated to sign-on UX. The
  closest real evidence is the **POS** Overflow flow board (`knowledge/flows/translink-pos-signon.md`,
  transcribed 2026-06-02) which shows this exact pattern almost verbatim (3-attempt lockout,
  "Device Locked — Present Supervisor Card", MotD/Word&Colour with Unavailable fallbacks, "Sign On
  Failed — N of 3", Communication Locked) — but it is explicitly a POS (Wayfarer) flow, not HHD.
- **What's missing:** An HHD-specific sign-on/sign-off Overflow flow export (or equivalent design
  doc), transcribed the same way `translink-pos-signon.md` was for POS. Until that exists, these
  cases can't be grounded to a real HHD-confirmed source — only to an unconfirmed cross-device
  analogy. Need the engineer to supply the HHD sign-on flow board or confirm the POS flow applies
  1:1 to HHD.

---

### 3. What backs the HHD "operator break" / "driver break" mode-preservation claim, and does "CR78" exist?

- **Category:** Missing/unlocatable source.
- **Case IDs:** 4103913, 4103919.
- **Findings:** Both cases cite `FBD-100651,CR78,FBD-100690`. `CR78` is not a locatable file or
  indexed entry anywhere under the configured `REQS_DIR` (`extract_req.py --find "CR78"` returns
  nothing). Direct term searches of both FBD-100651 and FBD-100690 for "driver break", "operator
  break", "resume", and "break" return zero hits in either document.
- **What's missing:** Either the CR78 document needs to be added to the local requirement library
  (it may exist but not be indexed/dropped in yet), or an engineer needs to confirm this behaviour
  from another source. As it stands, the claim that the HHD resumes the identical pre-break
  operating mode (Inspection vs Validation) after a driver break / enforced driver break has no
  checkable citation.

---

### 4. Does the HHD have an on-device "View Totals" / "print mini-statement" / "view Status" Operator Menu, and what are the real screen names?

- **Category:** Missing source document / possible wrong-surface citation pattern.
- **Case IDs:** 4103914, 4103916, 4103917, 4103920.
- **Findings:** These cases cite FBD-100342 (User Claims — KeyCloak back-office admin menus only),
  FBD-100276 (CloudFare Operator Totals API — an external REST API explicitly documented as having
  "no user interaction"), and FBD-100266 (Device Heartbeat — a back-office Comms Monitor/staff-list
  spec). None of the three documents contains any content about an on-device HHD menu, a "View
  Totals" screen, a mini-statement print option, or a "Status" screen — confirmed by direct
  full-text term search of each. The apparent pattern is that these refs were assigned by loose
  keyword association with the case's topic (a "Totals" case pointed at the "Operator Totals API"
  doc; a "Status" case pointed at the "Device Heartbeat" doc) rather than verified content.
- **What's missing:** An HHD Operator Menu UX source (Overflow flow or equivalent). Separately, case
  4103917's Expected Result names specific mini-statement layout references — "NIR Layout 20 /
  Glider Format 15" — that have no match anywhere searched in the requirement library; these read
  as invented specifics and are marked GAP in the rewrite rather than asserted.

---

### 5. Does the HHD have a "manage sale favourites" feature at all?

- **Category:** Behaviour-existence gap.
- **Case IDs:** 4103918.
- **Findings:** FBD-100260 (Product Name Usage, the cited ref) is entirely about display-name
  resolution rules (Device/Default Display Description fallback chains) and contains zero mentions
  of "favourite"/"favorite". No other spec in the local library (searched broadly) describes a
  sale-favourites add/modify/delete function on any device.
- **What's missing:** Confirmation this capability exists on the HHD at all, and if so, its actual
  spec/FBD reference.

---

### 6. Does the HHD's printer pairing behave like the M020 payment-device pairing, and is that even the same peripheral?

- **Category:** Missing source / partial analog.
- **Case IDs:** 4103922.
- **Findings:** The originally cited FBD-100383 has zero printer-related content (confirmed). The
  best available analog is FBD-100320 (TID Management), which confirms the HHD Bluetooth-pairs to
  its **Miura M020 payment card reader** — a different peripheral from the ticket/receipt printer
  this case is actually about. No spec anywhere in the library documents printer-specific pairing.
- **What's missing:** A source confirming the HHD's printer pairing mechanism (Bluetooth, presumably,
  by analogy to the M020, but unconfirmed) and its "paired" / test-print confirmation UX.
