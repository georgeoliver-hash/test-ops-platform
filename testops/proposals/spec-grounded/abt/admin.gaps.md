# ABT admin/access/staff/settings/ticket-editor — gap register

Every `GAP` / `UNCONFIRMED` below is a **question for the engineer** (CLAUDE.md Q&A loop), not a
closed finding. Answers get cited back into the cases and into `knowledge/`. A gap nobody can
answer is itself a finding (`POSSIBLE DESIGN/SPEC BUG`). Nothing here was gap-filled.

## A. Hard GAPs — feature/label absent from all provided specs

| # | Case | Gap | Question |
|---|------|-----|----------|
| G1 | 4102961 Sign on with a Google account | FBD-100342 specifies AD/ADFS/KeyCloak auth only (paras 203, 214-215). No Google/OAuth IdP. | Was Google federation added to KeyCloak (need a CR ref -> becomes UNCONFIRMED), or is this case invalid? |
| G2 | 4103083 Configure a change ticket | No "change ticket" type/flow in FBD-100363 (ticket types are paper / smartcard / barcode / payment-card receipt, para 125, 155-159). | What is a "change ticket" — a money-change receipt, a ticket-amendment flow, or a mistake? Which spec/CR? |
| G3 | 4103085 Group a set of ticket layouts | No template-grouping feature in FBD-100363 (only Create/Edit/Copy + per-level publish + product-class association). | Does "group layouts" mean publishing at a hierarchy level, product-class association, or a feature that doesn't exist? |

## B. Cross-surface / wrong-surface corrections (regrounded, confirm the move)

| # | Case | Issue | Question |
|---|------|-------|----------|
| B1 | 4103084 Configure a product on a ticket | Template-to-product assignment is a **Product Editor** function, not Ticket Editor (FBD-100363 para 391-393). Regrounded + retitled. | Confirm re-filing this case under the Products section. |
| B2 | 4103082 Configure a ticket for different devices | Device type is fixed at creation; separate template per device; reuse = **copy + change device type** (para 178-180, 338). Not one layout across devices. | Confirm the intended behaviour is the copy-and-change-device-type flow. |

## C. UNCONFIRMED — outside the named grounding set (access grounded, behaviour not)

### C1. Administration / Merit editors (7) — POSSIBLE MIS-FILE + missing spec
- Merit desktop editors sit in an ABT/CloudFare suite. Closest spec FBD-100306 (Merit Web V3.00)
  only partially confirms Timebands (267-268), Class/Route grouping (255/263), Location
  Restrictions (328). **Not found anywhere**: Date Editor period/roll-over/start-of-week
  (4103093), Merit Staff Editor (4103095), Route Revenue generation-factor/BRT/journey-allocation
  (4103099).
- **Questions:** (a) Should Merit desktop-editor cases live in this suite at all? (b) Which spec
  governs the Merit desktop editors — is a Merit desktop-application spec missing from the
  library (cf. FBD-100300 MERIT Route Consolidation, FBD-100347 Merit DWH)? (c) Does 4103095
  Merit Staff Editor duplicate CloudFare Staff Manager (4103044-047)?

### C2. Sign On & Account / Passenger Web Portal (4)
- No Passenger Web Portal spec in the named set or the library.
- **Question:** Which FBD governs the Passenger Web Portal (anonymous sign-on, seven-day journey
  window, home-screen summary, sign-off)? Provide it to reground 4102927-4102930, incl. the exact
  rejection messages (4102928).

### C3. Settings / CloudFare System Configuration (8)
- Access grounded to the System Configuration claim (FBD-100342 para 198); the sub-pages are not
  enumerated in any provided spec.
- **Question:** Which FBD specifies CloudFare System Configuration pages — Event Codes, Operating
  Units, Scheduled Tasks (purges), System Settings/VAT/feature toggles, Notifications, External
  Interface Settings, Scheduled Adherence? Also confirm the live Settings menu contents (4102965).
  Is Scheduled Adherence related to FBD-100266 heartbeat?

### C4. Administrator Settings / capping + debt recovery + e-Purse (5)
- Admin tab access grounded to AdminFullAccess/AdminReadAccess/EPurseReadAccess (paras 146-148);
  the setting semantics are not in the named set.
- **Question:** Which specs govern: End of Operational Day/Week & 24-hour capping period (4102878),
  maximum late data period (4102879), maximum journey duration / incomplete-journey rule
  (4102880), debt-recovery retry counts + unsuccessful-recovery message (4102881), e-Purse minimum
  fare (4102882)? (Likely a capping spec + a debt-recovery spec not supplied.)

### C5. Staff Manager (CloudFare) function detail (4)
- Module access grounded to the Staff Manager claim (para 185); no functional spec in the named
  set.
- **Question:** Which FBD specifies CloudFare Staff Manager functions — add/modify/disable staff
  (4103044), modify PIN (4103045), home/working location (4103046), staff history (4103047)?

### C6. Drawing Tool (5) & Labeling & Publishing (4) / Topology & Fares
- Access grounded to the Topology claim (para 174). Function/workflow not in the named set.
- **Questions:** (a) Which FBD governs the Topology & Fares **Drawing Tool** (map points, zones,
  positional points, CSV import/export, search)? (b) Which FBD governs Topology **labelling &
  publishing** (label config data, future-transition-date publish, re-publish older config, delete
  label)? FBD-100363 confirms only ticket-template publishing at a hierarchy level (para 251-252).
  (c) For 4103014, what happens to devices already transitioned when an active label is deleted?

## D. Tooling gap (blocks full grounding)
- **FBD-100383 TFTS Operator Hierarchy v4.00 is a PDF and could not be read** — `extract_req.py`
  reports "no extractor available (No module named 'PyPDF2')". Hierarchy facts were cited from
  FBD-100342 instead (paras 206-212, 251-252). **Action:** install `pdfminer.six` (or `PyPDF2`) in
  the repo `.venv` so PDF specs can be grounded, then re-verify any hierarchy/level claims against
  FBD-100383 directly.
