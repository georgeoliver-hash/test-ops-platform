# GV regression register — folding 4.1.0 → 4.2.0 defects into functional homes

Propose-first, read-only. Maps the **75 `Fixes/Changes` cases** + **3 `Previous TIBU scenarios`** from
the old suite (14973) — plus the two Primary/Secondary bug themes called out in `old-suite-audit.md` —
onto the consolidated new suite (30286). Governing rule (`docs/gherkin-standard.md`): **fold each defect
into the functional/non-functional case that owns the behaviour via the Refs field** (link `TIBU-#####`),
organised by behaviour not by release; only genuinely **un-homeable** defects become dedicated
`@regression` cases.

**This register is the fold map, not new cases.** Where the owning case lives in a sibling proposal
(ABT taps / barcode / smartcard functional), that is named as the home; the folds authored *here* land
in the Refs of the cases in `commissioning-tech-nonfunctional-smoke.cases.yaml`.

## Recurring ids — dedupe on fold (counted once)
`18302` (×3: 4.1.0/4.1.1/4.1.2) · `16372` (×2) · `18310` (×2) · `18606` (×2) · `18566` (×2) ·
`14160` (×2: 4.1.1/4.1.5) · `18930` (Fixes 4.1.2 **and** Previous-TIBU). Fold each id once into its
owning case; do not create per-build duplicates.

---

## 1. Primary/Secondary head state machine  *(the dominant theme — bug-derived, [needs-spec], FBD-100348 rows pending)*
**Home:** `Non-Functional / Primary-Secondary Head State Machine` (structure.md — a needs-spec behaviour
section to author from this cluster) + the `Resilience` power-up/mains-restore/heartbeat cases in this file.

| TIBU | Defect (short) | Folds into |
|---|---|---|
| 14648 | Primary state not recovered after power failure when previously Fully Free | Head State Machine — Fully-Free power recovery |
| 14670 | Fully Free — Primary not OOS when tech signed in on Secondary | Head State Machine — tech-signon-on-Secondary side effects |
| 14668 | GV freezes leaving tech menu in Fully Free | Head State Machine — Fully-Free / tech-menu exit |
| 18606 | Primary head incorrect display in Fully Free *(recurs)* | Head State Machine — Fully-Free display |
| 18607 | Gate OOS after Fully Free, unrecoverable by mode change/power cycle | Head State Machine — Fully-Free recovery |
| 14711 | Primary & Secondary state issues (general) | Head State Machine — inter-head state |
| 18944 | Primary shows OOS while Secondary still accepting cards *(Prev-TIBU)* | Head State Machine — independent head state |
| 14660 | Cannot put Secondary OOS via remote commands | Head State Machine — remote-command mode change |
| 14717 | Exit mode — tech sign-on/off on Secondary puts device OOS | Head State Machine — tech-signon-on-Secondary |
| 14722 | Tech sign-off on Secondary leaves gate in Maintenance | Head State Machine — tech-signoff recovery |
| 16491 | Sign-out of tech menu in Exit mode → both OOS | Head State Machine — tech-signoff recovery |
| 16779 | Tech logout on Secondary (Entry mode) → Present-Card screen on Secondary | Head State Machine + HMI screen state |
| 16836 | Exit-mode gate reverts to Entry mode after location change | Head State Machine + Commissioning (Location Settings) |
| 18941 | Changing location on both GVs → both OOS *(Prev-TIBU)* | Head State Machine + Commissioning (Location Settings) |
| 17473 | Delay updating operating mode after Station Manager change | Head State Machine — Station-Manager propagation |
| 16798 | Station Manager gate representation not updating after commands | Head State Machine — Station-Manager propagation |
| 18636 | Station Manager flicking between operating modes | Head State Machine — Station-Manager propagation |
| 18302 | Reboot command puts Primary OOS *(recurs ×3)* | Head State Machine — reboot recovery |
| 18930 | Rebooting Secondary → both OOS after boot *(recurs; Prev-TIBU)* | Head State Machine — reboot recovery |
| 18614 | Rebooting Secondary → both OOS + CloudFare spamming | Head State Machine — reboot recovery + Comms/BOS |
| 19026 | Primary OOS, not performing nightly reboot | Head State Machine — nightly-reboot recovery |
| 19250 | Primary OOS after nightly reboot | Head State Machine — nightly-reboot recovery |
| 19220 | Platform permission issue preventing reboot | Head State Machine — reboot recovery |
| 18413 | Comms-block via CloudFare then re-establish — no recovery to last state | Head State Machine — comms-block recovery + Comms/BOS |
| 23832 | Device spamming + state issues after common-state-changes merge | Head State Machine — inter-head state + Comms/BOS |
| 22159 | Tailgating in Entry mode — Secondary shows "Present card or Barcode" | Head State Machine + infraction/HMI |
| 16800 | Secondary stuck amber "please wait" ~2 min after Primary validation | Head State Machine + HMI (Please Wait) |
| 14570 | "Please wait" screen delayed appearing in Bi-directional | Head State Machine + HMI (Please Wait) |

## 2. Device status / state reporting to CloudFare  *(FBD-100263 / FBD-100358, [partial])*
**Home:** `Non-Functional / Resilience` → *BOS Comms — queued audit uploads* + a `Comms / BOS` device-status
case (cross-ref ETM). Folded here via Refs on the Resilience comms cases.

| TIBU | Defect (short) | Folds into |
|---|---|---|
| 16455 | Not sending `gateValidatorState` to CloudFare | Comms/BOS — device-status reporting (Resilience comms-restore case) |
| 17104 | Data did not upload from Primary to CloudFare | Comms/BOS — audit upload on restore |
| 18306 | Secondary state shown as "Not defined" in CloudFare | Comms/BOS — device-status reporting |
| 18309 | "Gate Validator Status" shows entry for all gate modes | Comms/BOS — device-status reporting |
| 18310 | Device-status event spamming in CloudFare *(recurs)* | Comms/BOS — heartbeat/status cadence (Resilience 15-min case) |
| 14871 | OOS "Status Reason" not defined in CloudFare | Comms/BOS — device-status reporting |
| 18566 | Quarantined audit data (missing tail of record) *(recurs)* | Comms/BOS — audit upload integrity |
| 18637 | Activity Log reports incorrect device status for each head | Comms/BOS — Activity Log (FBD-100358) |
| 18416 | Primary reports its *previous* location in CloudFare | Commissioning (Location Settings) + Asset reporting (FBD-100263) |
| 16809 | GV mapping issue (GV00085) | Commissioning + Asset mapping (FBD-100263) |

## 3. Barcode reader hardware / dropout & throughput  *(FBD-100167 barcode; throughput [needs-spec])*
**Home:** barcode functional section (sibling proposal) + `Resilience / Throughput` in this file.

| TIBU | Defect (short) | Folds into |
|---|---|---|
| 18305 | Shows "Barcode Reader Not Available" but still validates | Barcode reader status |
| 20792 | Platform raises CommunicationError alarm on every reader disconnect | Barcode reader dropout handling |
| 20178 | App restarts when barcode reader disconnected | Barcode reader dropout handling + Resilience |
| 20176 | Barcode reader spamming misconfiguration alarms | Barcode reader dropout handling |
| 19450 | Temporary barcode disconnects not handled by application | Barcode reader dropout handling |
| 21245 | Disconnect/reconnect reader on Secondary changes screen/state | Barcode reader dropout + HMI/Head State Machine |
| 22674 | Barcode reader dropout — possible link to ABT enabled in error | Barcode reader dropout handling |
| 23455 | Card reader not available after nightly reboot | Barcode reader + Head State Machine (nightly reboot) |
| 21316 | "Barcodes not accepted" banner despite working functionality | Barcode reader status + HMI |
| 21005 | Regression in barcode throughput *(recurs theme)* | Resilience / Throughput |
| 19749 | Performance degraded since 4.1.1 | Resilience / Throughput |
| 16221 | Multiple MUB in quick succession → gates close on a valid barcode | Resilience / Throughput + Gate open/close |
| 18597 | GV not allowing quick succession of cards | Resilience / Throughput |
| 18638 | Successful barcode sporadically shows "Barcode Already Validated" | Barcode functional (result state) + HMI |

## 4. Validation screen / tone timing  *(FBD-100167 / [needs-spec] audio)*
**Home:** `Non-Functional / HMI Screens` + a `Resilience / Audio Feedback` case (needs-spec).

| TIBU | Defect (short) | Folds into |
|---|---|---|
| 14884 | "Present Card" shown briefly when validating a second barcode | HMI — barcode success/idle transition |
| 17063 | Allow smartcard validations while barcode success screen shown | HMI + smartcard/barcode concurrency |
| 17064 | Adjust when success/failure tones play during validations | Audio Feedback (needs-spec) + HMI |
| 18595 | No validation beep during success screen for previous tap | Audio Feedback (needs-spec) |
| 18638 | *(also §3)* sporadic "Already Validated" after success | HMI barcode result |

## 5. Audio assistance messages  *([needs-spec], bug-derived)*
**Home:** `Resilience / Audio Feedback` (needs-spec — flag; no issued GV spec asserts audible-assist behaviour).

| TIBU | Defect (short) | Folds into |
|---|---|---|
| 16372 | Partial-Sight Half-fare smartcard — audio assist message not played *(recurs)* | Audio Feedback (needs-spec) |
| 14246 | Blind SmartPass hotlisted — audible message not played | Audio Feedback (needs-spec) |

## 6. Power / emergency  *(FBD-100348 [pending integration])*
**Home:** `Non-Functional / Resilience` power/emergency cases in this file (folded via Refs already).

| TIBU | Defect (short) | Folds into |
|---|---|---|
| 14160 | Power loss < 2 s → immediate shutdown *(recurs)* | Resilience — "power loss ≤ 2 s does not force a reboot" (folded) |
| 16813 | Emergency open requires reboot to change operating mode | Resilience — "Emergency Release Button" (folded) |
| 18635 | Irregular behaviour following Emergency Switch testing | Resilience — "Emergency Release Button" (folded) |
| 18642 | Paddles remain closed after successful validation (specific scenario) | Gate Mode & Access Control (open-on-authorise, sibling proposal) |

## 7. Technician menu / network settings  *(FBD-100654)*
**Home:** `Functional / Technician Menu` in this file.

| TIBU | Defect (short) | Folds into |
|---|---|---|
| 14001 | Network Settings menu not showing connected ethernet | Technician Menu — Network Settings *(add a Network Settings case if authored)* |
| 21315 | Unable to sign in / use Technician Menu | Technician Menu — Technician Sign On (folded via Refs) |
| 18301 | Stuck on "Error Reading Screen" when tech card briefly presented | Technician Menu — Sign On + HMI (Re-present) |

## 8. Barcode / product functional  *(FBD-100167)*
**Home:** barcode + smartcard functional (sibling proposal).

| TIBU | Defect (short) | Folds into |
|---|---|---|
| 19295 | CR116 — show previous date on barcode screen when expiry is midnight–4am | Barcode — CR116 expiry display (FBD-100167) |
| 18616 | War Pensioner barcode displayed as WAR senior | Barcode / smartcard product display |

## 9. NIR transfers  *([needs-spec])*
**Home:** `Functional / NIR Transfers` (needs-spec, sibling proposal).

| TIBU | Defect (short) | Folds into |
|---|---|---|
| 22401 | Transfer still occurs at a location where the product is not valid | NIR Transfers — transfer-window validity (needs-spec) |

---

## Un-homeable → candidate `@regression`
Defects with no owning functional behaviour (dev-internal or lacking detail). Carry as dedicated
`@regression` cases only if retained; otherwise raise for detail.

| TIBU | Why un-homeable | Action |
|---|---|---|
| 22904 | "Improve logging to reduce noise" — internal logging/observability change, no user-observable behaviour to assert | Not a functional test — drop from suite; verify via log review, not a case |
| 23837 | No title / no detail in source | **Needs detail** before it can be homed — query owner; hold |

---

## Fold summary
- **78 source cases** (75 Fixes/Changes + 3 Previous TIBU) → **~72 unique defects** after de-duping the
  recurring ids (18302 ×3, and 16372 / 18310 / 18606 / 18566 / 14160 / 18930 each counted once).
- **~70 fold into functional/non-functional homes** via Refs — the largest cluster (**~28**) into the
  **Primary/Secondary head state machine**, then **~14** into **barcode-reader/throughput**, **~10** into
  **Comms/BOS device-status**, the rest across power/emergency, HMI/tone timing, audio-assist,
  technician menu, barcode/product, and NIR transfers.
- **2 un-homeable** (22904 non-testable logging; 23837 no detail) → candidate `@regression` / needs-detail.
- **No parking lot.** Every retained defect is queryable through the Refs of the case that owns its
  behaviour, organised by behaviour rather than by the 4.1.0→4.2.0 release it was fixed in.

## Flags
- The **head state machine** cluster is **[needs-spec]** — FBD-100348's governing rows are marked
  *pending integration*. Fold as regression coverage against the behaviour, but the owning section must
  carry the needs-spec marker; do not assert these as validated acceptance until a spec lands.
- **Audio-assist** (16372/14246) and **throughput** (21005/19749/16221/18597) homes are **[needs-spec]** —
  no issued GV spec; carry as flagged scaffolding.
- **NIR transfer** (22401) home is **[needs-spec]** — transfer-window rule at the gate not clearly specced.
- `18642` (paddles stay closed after successful validation) belongs to the **Gate Mode & Access Control**
  section (FBD-100348 open-on-authorise), which is authored in a sibling proposal — folded there, not here.
