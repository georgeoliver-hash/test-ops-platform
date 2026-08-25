# Findings — NJT Fare Register: CloudFare Communication vs FS002 §8

**Source cases dump:** `reports/uk-bus-projects/njt-farebox-and-register-replacement/2026-08-13/area-cases/cloudfare-comms.md` (51 cases, 4 trees: orphaned top-level "Cloudfare" (3), main "Fare Register / CloudFare Communication" incl. Remote Commands (22 + 9 non-remote = 31), TIBU "Cloudfare Comms" (14 mirrored scenarios), plus 3 orphaned Device Communication cases).
**Spec:** `knowledge/njt/specs/fs002-cloudfare-communication.md` (NJT_FRFRP_FS002 §8/8.1, p.86–88).

## 1. Checklist walk (knowledge-note "Suite implications")

| # | Checklist item | Status | Evidence |
|---|---|---|---|
| 1 | Staff-list check period (15 min), independently configurable | **Partial** | C4087054 asserts the wait-and-request behaviour but not that the period is independently configurable by Flowbird staff (p.86) |
| 2 | Manifest check period (15 min), independently configurable | **Partial** | C4087055, same gap as #1 |
| 3 | Force Comms bypasses both timers immediately | **Covered** | C4087065 (dup: C4099044/45 body, mislabeled — see §3) |
| 4 | Background download + activation-date gating | **Covered** | C4087056 (past date, applies immediately), C4087057 (future date, applies at time), C4087058 (background, doesn't affect trip) — dup C4099039/40 |
| 5 | Current + future config set dual-storage, explicitly asserted | **Missing** | No case explicitly asserts both a current *and* a future set are held simultaneously (p.86); C4087057 implies it but only tests the future-set outcome, not the coexistence |
| 6 | Update integrity verification: invalid → rejected + event to CloudFare | **Covered** | C4087059, dup C4099041 |
| 7 | 10s transaction-delivery SLA (measured from completion) | **Covered** | C4087060, dup C4099036 (SLA-vs-comms-dependent nuance intentionally not asserted — flagged GAP, not drafted, per instructions) |
| 8 | Unauthorised-device rejection → OOS until successful comms | **Covered** | C4087063 (reject), C4087064 (recovers to in-service on authorisation) — dup C4099034/33 |
| 9 | Force Comms / Out of Service / In Service / Lock / Reboot as distinct scenarios | **Covered, with gaps** | See §2 breakdown below |
| 10 | Local-precedence override (mid-transaction OOS, degraded In-Service) | **Covered** | C4087068 (OOS mid-transaction, transaction allowed to finish first), C4087073 (In Service refused while degraded) |
| 11 | Exit-state gating: OOS/Lock only exit via explicit command from CloudFare | **Partial** | OOS→In Service: C4087080 covered. Lock→In Service: C4087081 covered. **Lock→Out of Service is NOT tested** — spec explicitly states Lock can also be exited by an *Out of Service* command (p.87), and no case exercises this path |
| 12 | Lock is a one-way local exit (reboot/supervisor/admin don't clear it) | **Covered** | C4087077, C4087079 (C4087078 is bugged — see §3) |
| 13 | Block is state-only, not a command; no-ack while blocked; both entry+confirmation CloudFare-side | **Covered (wording caveat)** | C4087093, C4087097. Wording says "the user performs a Block command", which frames Block as an operator-triggered command rather than a CloudFare-side state change — a phrasing drift from the spec's explicit "Block is NOT a device command", worth a standards-keeper pass, not a coverage gap |
| 14 | Auto sign-off on transition to OOS/Lock/Block while signed on | **Covered** | C4087067 (OOS), C4087075 (Lock), C4087097 (Block) |

## 2. Remote-Commands breakdown (22 cases in "Fare Register / CloudFare Communication / Remote Commands")

| Command | Count | Cases | Note |
|---|---|---|---|
| Force Comms | 1 | C4087065 | Adequate — spec gives it one behaviour to assert |
| Out of Service | 7 | C4087066, 082, 067, 068, 069, 070, 071 | Thorough |
| In Service | 4 | C4087072, 073, 080, 081 | Thorough |
| Lock | 7 | C4087074, 086, 075, 076, 077, **078**, 079 | **C4087078 is a copy-paste defect**: titled "Lock - Does Not Exit State - Supervisor Mode" but its Given/When/Then body is identical to the *Out of Service* version (C4087070) — asserts "an out of service state", not "a locked state". This is an existing-case defect, not a coverage gap; flag for correction, do not silently invent a fix here |
| Reboot | 1 | C4087088 | **Asserts unconfirmed behaviour**: "the FR powers on in the same state it was in before the reboot" — FS002 has no stated detail on reboot resume-state (flagged GAP in knowledge note). This case currently asserts specific behaviour beyond the source spec, contrary to the hard rule against inventing device behaviour. Logged to gap register (§4), not rewritten here — out of scope of this pass to edit the old suite/existing case wording |
| Block | 2 | C4087093, 097 | Covered (Idle + on-a-trip) |
| **Total** | **22** | | Matches task's stated count |

Net: all 5 named commands + Block are represented; no command is entirely missing. The one true coverage gap is **Lock-exit-via-Out-of-Service** (§1 #11).

## 3. Duplication / data-quality issues (orphaned + TIBU trees vs main tree)

- **TIBU "Remote Device Management" mislabeling (TIBU-29326, 5 cases: C4099042–46):** titles and bodies are shifted by one relative to the command named:
  - C4099042 "Remotely Place a Device Out of Service" — body matches (OOS). OK.
  - C4099043 "**Remotely Lock a Device**" — body describes a **Reboot** command ("executes a graceful reboot cycle"). Mismatched.
  - C4099044 "**Remotely Trigger a Reboot**" — body describes **Force Comms** ("immediately attempts a new communication session… to check for updates"). Mismatched.
  - C4099045 "Remotely Force a Communication Check" — body also Force Comms (duplicate of 44's body, correctly labeled itself).
  - C4099046 "Remotely Place a Healthy Device In Service" — body matches (In Service). OK.
  - Net effect: the TIBU tree has **two Force Comms cases** (duplicate), **zero genuine Lock cases**, and **zero genuine Reboot cases**, despite titles implying otherwise. Since Lock and Reboot ARE covered in the main tree, this is a duplication/mislabeling defect in the TIBU tree rather than a true coverage gap — flag for the engineer to retitle/refile or condemn as redundant with the main tree.
- **TIBU tree overall is a near 1:1 duplicate** of the main "Fare Register / CloudFare Communication" tree's scenarios (device auth/reject, data-loss recovery, transaction/event/status transmission, config management, remote commands) under different section names (TIBU-29319/29320/29321/29325/29326). Recommend consolidation/condemnation of one tree once ownership is decided — out of scope for this drafting pass.
- **Orphaned top-level "Cloudfare" section (3 cases):**
  - C4085072 "Placeholder" — content is about an "Enter Alighting Zone Screen" auto-timeout, completely unrelated to CloudFare comms. Clear misfile; not a CloudFare-comms case at all.
  - C4105030 "Device Communication - Quarantined Data" — uses the term "CloudFare Quarantine data", which does **not** appear anywhere in the distilled FS002 §8 spec (the spec's language for a failed-verification update is "event to CloudFare" reporting an invalid dataset, not a queryable "quarantine" store). This may be grounded in a different spec section not covered by this excerpt, or may be inventing a UI/data concept — flagged to gap register rather than assumed.
  - C4105031 "Device Communication - Data Sent After Comms Re-Established" — legitimately grounded by the general "guaranteed delivery mechanism" fact (p.86); duplicates TIBU's C4099035. Not a gap.
  - C4105032 "Device Communication - Device Registration" — asserts a "registration token" is returned on registration; this term is not present in the distilled excerpt either. Possibly from an un-excerpted part of FS002 §8. Flagged to gap register.

## 4. Grounded missing/partial items drafted as new cases

Drafted to `proposals/njt-fr-suite-restructure/cloudfare-comms.cases.yaml`:
1. Lock state exit via an explicit **Out of Service** command (p.87) — closes checklist item #11.
2. Staff-list and manifest check periods are **independently configurable** by Flowbird support staff (p.86) — closes checklist items #1/#2 (Partial → will be Covered).
3. FR **stores both a current and a future configuration set simultaneously**, with the future set inactive until its activation date/time (p.86) — closes checklist item #5.

Items explicitly excluded from drafting (per task instruction — no invented detail):
- 10-second transaction-delivery retry/backoff/queue-on-failure behaviour.
- Reboot mid-transaction safeguard and post-reboot resume-state behaviour (also flags the existing C4087088 wording as asserting unconfirmed behaviour).
- On-screen/visible behaviour to the operator when a device enters the Block state.
- The "CloudFare Quarantine data" (C4105030) and "registration token" (C4105032) terminology — ungrounded in the excerpted spec text; routed to gap register rather than drafted around.

All logged to `proposals/njt-fr-suite-restructure/gap-register-cloudfare-comms.md`.
