# FS002 — Section 7: Special User Functionality (distilled)

**Source:** `NJT_FRFRP_FS002 - Fare Register Functional Specification.pdf.txt`, lines 13906–15081
("7. Special User Functionality" — 7.1 Supervisor Mode, 7.2 Administrator Mode). Raw text held
locally in `njt-requirements/_text/`, not committed. Page citations use the nearest preceding
"Page N" marker found in-range; the marker for a subsection sometimes falls after that subsection's
text (PDF page-break artifact) — treated as "nearest preceding" per the task rule.

## Sign-on to special user mode (FM-7)
- Entry point: press the **Issue key** while the **idle screen** is displayed.
- Device prompts for **operator number + PIN**.
- Validated against the **latest staff list received from CloudFare**.
- The **user role defined in the staff list** determines which special-user mode is entered (i.e.
  Supervisor vs Administrator membership is staff-list-driven, not a device-side setting).
- On success: a **special user logon message** is sent to CloudFare (refs **GR-3, FRT-1**), and a
  **maintenance logon message** is sent to the **Clever Device**.
- **GAP** — PIN length/format, lockout-on-repeated-failure behaviour, and the on-screen wording for
  a rejected operator number/PIN are not stated in this range; confirm before writing negative-path
  cases. (NJT_FRFRP_FS002 p.82)

## 7.1 Supervisor Mode — menu overview
"The following functions are available from the supervisor menu": Software Versions, Force
Communications, Historic Trip Reports, Serial Numbers, Device Settings, System Status, Enable OBV
Maintenance mode, Exit Supervisor mode. (NJT_FRFRP_FS002 p.82)

### 7.1.1 Software Versions
- Supervisor opens the **Versions screen** via the corresponding Soft Key on the Supervisor Menu
  screen; it lists installed software versions and associated configuration.
- **Down Arrow** = next page, **Up Arrow** = previous page.
- Supervisor can obtain a **printout** of the versions/configuration via the corresponding Soft Key.
- **GAP** — which components/subsystems appear in the version list (Fare Register app, OBV, Farebox
  firmware, etc.) is not itemised in this range. (NJT_FRFRP_FS002 p.82)

### 7.1.2 Force Communications
- Supervisor views comms state from the **Force Comms** menu, reached via Soft Key on the
  Supervisor Main Menu.
- Forcing a comms call causes the Fare Register to **upload all outstanding audit data** and
  **check for software/configuration updates**.
- **GAP** — no on-screen feedback/result states (success/failure, in-progress indicator) are
  described in this range. (NJT_FRFRP_FS002 p.83)

### 7.1.3 Historic Trip Reports
- Supervisor opens the **Historic Waybills screen** via Soft Key on the Supervisor Menu screen; it
  lists performed-duty waybills held on the device, **most recent first**.
- **Down/Up Arrow** = next/previous page of the list; Soft Key = select a waybill to view its
  details; a further Soft Key **prints** the selected waybill's details.
- **Down/Up Arrow** also moves to the next/previous individual waybill once one is selected/viewed.
- **GAP** — the fields shown on a waybill's detail view, and how many waybills are retained on
  device, are not specified in this range. (NJT_FRFRP_FS002 p.83)

### 7.1.4 Serial Numbers
- Supervisor views the **Serial Numbers** menu via Soft Key on the Supervisor Main Menu.
- Screen displays: **device serial number**, plus tray-programmed data — **home location**, **tray
  serial number**, **bus number**.
- View-only per the text (no edit/program action described here — programming the Farebox number is
  a separate function, see 7.2.2). **GAP** — confirm this screen is read-only with no supervisor
  edit capability. (NJT_FRFRP_FS002 p.83)

### 7.1.5 Device Settings
- Menu allows the **driver** (note: text says "driver," not "Supervisor," for this item — refs
  **GR-10, FM-1**) to adjust:
  - Increment/decrement **Fare Register backlight** level
  - Increment/decrement **Fare Register volume** level
  - **Restore default** Fare Register brightness or volume
  - Increment/decrement **Farebox backlight** level
  - Increment/decrement **Farebox volume** level
- **GAP** — numeric range/step size for backlight and volume levels, and whether there's a
  restore-default for the Farebox settings (only Fare Register default-restore is mentioned), are
  not stated. (NJT_FRFRP_FS002 p.84)

### 7.1.6 System Status
- Screen shows **GPS lock** status + satellite count, and connection status of devices on the
  **RS485** networks. Printable via the mapped Soft Key.
- Table of components/statuses given:
  - **GPS Lock**: lock + satellite count, or "No lock"
  - **Printer**: Ok + approx. tickets remaining, or Error (Paper low / Paper Jam / Paper out)
  - **OBV**: Connected Ok, Connected Fault, or not connected
  - **Farebox**: Connected Ok, Connected Fault, or not connected (footnote 1)
  - **Clever IVN**: Connected or not connected
  - **Spotter Display**: Connected or not connected
- Footnote 1 (Farebox row): background colour signals the last-signed-on route type — **grey** if
  last signed on to a **full-service route** (assumed full-service bus), **red** if last signed on
  to an **Exact route** (assumed exact-fare bus).
- **GAP** — background-colour semantics are only specified for the Farebox status row; confirm no
  equivalent colour coding applies to the other rows. (NJT_FRFRP_FS002 p.84)

### 7.1.7 Enable OBV Maintenance mode
- Selecting this option sends an **$E4 Status Change** command to the OBV: **Maintenance mode
  byte = 01**, **Agent Number = the Employee number used to sign on to supervisor mode**.
- An **audible beep** confirms the option was selected.
- The **OBV indicator** changes to reflect maintenance mode **upon receipt of an OBV status message
  with the relevant bit set** — i.e. confirmation is asynchronous, driven by the OBV's own status
  reply, not by the button press itself.
- **GAP** — exact OBV indicator appearance (icon/colour/text) before vs after the status bit is set
  is not described in this range. (NJT_FRFRP_FS002 p.84–85)

### 7.1.8 Exit Supervisor mode
- User selects the **"exit supervisor mode"** menu option.
- Fare Register sends an **End Run message to the Clever Device with transaction count = 9999**
  (sentinel value marking a supervisor-session end-run, distinct from a normal driver end-run count).
- **If** OBV maintenance mode was enabled during the session, the Fare Register also sends an
  **$E4 Status Change** command to the OBV with **Maintenance mode byte = 00** and
  **Agent Number = 000000**, telling it to exit maintenance mode.
- Fare Register **returns to idle mode**.
- **GAP** — confirm behaviour if maintenance mode was enabled AND separately disabled again within
  the same session before exit (does exit still re-send the exit command, is it idempotent/harmless
  to send it regardless of current OBV state). (NJT_FRFRP_FS002 p.85)

## 7.2 Administrator Mode
- A distinct special mode from Supervisor, restricted to unlocking the Farebox door remotely.
- Explicitly **"only available to a very restricted group of users"**, due to the security
  implications of unlocking the Farebox outside the normal probing process / electronic-key flow.
- **GAP** — the staff-list role name(s) that map to Administrator Mode (vs Supervisor Mode) are not
  given in this range — confirm the role taxonomy before writing sign-on cases that need to
  distinguish the two entry paths. (NJT_FRFRP_FS002 p.85)

### 7.2.1 Unlock Farebox (EFADLS-3)
- Sends a command to the Farebox instructing it to **unlock its door**.
- Selecting this option sends an **event to CloudFare**.
- **GAP** — no on-screen confirmation/feedback to the user is described (e.g. does the screen show
  success/failure of the unlock command itself, or only that the event was raised).
  (NJT_FRFRP_FS002 p.85)

### 7.2.2 Program Farebox Number
- User is prompted to enter the **new Farebox ID**; the prompt text says a **6-digit number**, but
  the validation rule stated is **1–6 numeric digits** — a wording inconsistency in the source.
  **GAP/ambiguity** — confirm on the live system whether a shorter-than-6-digit entry (e.g. "42") is
  actually accepted, or whether the field enforces exactly 6 digits and the "1-6" text is a spec
  error.
- On confirming a valid number: Fare Register sends the **Program Farebox ID message** to the
  Farebox with the new number, then sends a **Request Farebox details message** and **displays the
  returned number** to confirm the action completed.
- **GAP** — behaviour on an invalid entry (non-numeric, >6 digits) — error message text/whether the
  user can retry — is not stated. (NJT_FRFRP_FS002 p.85)

## Suite implications
- **Sign-on gating**: cover valid Supervisor sign-on (Issue key from idle → operator#+PIN →
  staff-list validated → mode entered per role) and invalid sign-on (operator not in staff list, not
  special-user role, wrong PIN) — negative-path detail is a GAP above, so mark expected
  behaviour **UNCONFIRMED** until the engineer answers.
  - Assert the **dual notification** on successful sign-on: special-user logon message to CloudFare
    AND maintenance logon message to the Clever Device — both, not just one.
- **Software Versions**: view + paginate (Down/Up Arrow) + print — assert printout is triggered by
  Soft Key, not automatic.
- **Force Communications**: assert both side-effects together — outstanding audit data upload *and*
  a software/config update check — a case that only checks one is a partial cover.
- **Historic Trip Reports**: list ordering (most-recent-first), pagination, per-waybill detail view,
  and print-from-detail-view as four distinct checkpoints.
- **Serial Numbers**: assert the four displayed fields (device serial, home location, tray serial
  number, bus number) individually — a single "screen displays correctly" case under-specifies this.
- **Device Settings**: cover increment, decrement, and restore-default for each of the five listed
  controls (FR backlight, FR volume, Farebox backlight, Farebox volume, FR restore-default) — note
  the spec only names a restore-default for the Fare Register, not the Farebox; if a Farebox
  restore-default exists in the suite today, cross-check it against this GAP.
- **System Status**: assert each of the six component rows independently, including the
  Printer's three distinct error variants (Paper low/Jam/out) and the Farebox background-colour
  logic tied to last-signed-on route type (full-service = grey, Exact = red) — this colour-coding
  rule is easy to omit and easy to get backwards.
- **Enable OBV Maintenance mode**: assert the command payload semantics (byte 01, Agent Number =
  signed-on employee number), the confirmation beep, and that the **OBV indicator updates on the
  OBV's own status reply**, not immediately on button press — a case asserting instant UI update
  would be testing the wrong thing.
- **Exit Supervisor mode**: assert the sentinel End Run transaction count of **9999**, and the
  conditional OBV exit-maintenance command (byte 00, Agent Number 000000) — only sent **if**
  maintenance mode was enabled during that session. Cover both the "was enabled" and "was not
  enabled" exit paths as separate cases.
- **Administrator Mode entry**: since the restricted-role detail is a GAP, log a gap-register
  question on which staff-list role(s) grant Administrator access, and whether Administrator mode
  is entered via the same Issue-key/operator#+PIN flow as Supervisor mode or a separate path.
- **Unlock Farebox**: assert the CloudFare event fires on selection; treat the absence of described
  on-screen confirmation as a gap to confirm on the live system before asserting any specific UI
  feedback.
- **Program Farebox Number**: assert the happy path (valid number → Program Farebox ID message →
  Request Farebox details → display returned number). Treat the 6-digit-prompt vs 1–6-digit-rule
  mismatch as a resolve-gaps question before writing the boundary/negative cases (e.g. do not assume
  "42" is accepted without confirmation) — flag as **POSSIBLE SPEC BUG** if the engineer can't
  clarify which rule is authoritative.
