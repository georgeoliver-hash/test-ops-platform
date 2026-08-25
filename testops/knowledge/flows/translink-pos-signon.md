# Flow: Translink POS — Sign On

- Source: Overflow export `v4.0.3 Translink POS - 1.0 Sign On` (17 screens), transcribed from the
  PNG/WebP boards in `knowledge/flows/translink-pos-signon/` on 2026-06-02.
- Project: translink   Device: POS (Wayfarer)   Feature: auth
- Transcription confidence: **high** — cross-checked 2026-08-04 against the full verbatim
  Chrome-extension transcription (`translink-pos-full-transcription-v4.0.3.md`, board "1.0 Sign On"),
  which confirmed the branch wiring below. See "Confirm against Overflow" section for what that
  cross-check resolved.
- Note: design doc is **v4.0.3**; if you're prepping the **5.0.0** fix version, re-export when the
  flow changes for that release.

## Diagram
```mermaid
flowchart TD
  IDLE[1_0 Idle Screen<br/>"Present Card or Press Any Key to Continue"]
  IDLE -->|press any key| SO[1_1 Sign On<br/>ID + PIN fields, "Press Enter to Confirm"]

  SO -->|enter ID then PIN, press Enter| WAIT[1_2_2 Please Wait...]

  WAIT -->|comms down| COMMS[1_2_1 Communication Locked<br/>"Notify a Supervisor or Technician"]
  WAIT -->|credentials invalid| BAD[1_3_1 Sign On Failed<br/>"ID or PIN is incorrect — N of 3"]
  WAIT -->|credentials valid| MOTDQ{Message of<br/>the Day available?}

  BAD -->|attempts remain| SO
  BAD -->|3rd failure| LOCK[1_4_1 Device Locked<br/>"Present Supervisor Card"]

  MOTDQ -->|yes| MOTD[1_3_2 Message of the Day]
  MOTDQ -->|no| MOTDU[1_5_1 Message of the Day Unavailable]
  MOTD -->|press any key| WCQ{Word & Colour<br/>available?}
  MOTDU -->|press any key| WCQ
  WCQ -->|yes| WC[1_4_2 Word & Colour of the Day]
  WCQ -->|no| WCU[1_6_1 Word & Colours of the Day Unavailable]
  WC -->|press any key| MAIN[2_2 Main Screen — Rail selected]
  WCU -->|press any key| MAIN
```

## Paths (each path = one candidate scenario)
| # | Path | Feature | Tags | Covered by |
|---|------|---------|------|------------|
| 1 | Idle → press any key → Sign On screen shows ID + PIN fields | auth | — | 4099912, 4100036, 4100037 |
| 2 | Sign On → valid ID + PIN → Please Wait → MotD → Word & Colour → Main Screen | auth | @bos | FRAGMENTED — see consolidation-audit.md |
| 3 | Sign On → invalid ID + PIN → "Sign On Failed … 1 of 3" → back to Sign On (retry) | auth | @destructive | 4099921 |
| 4 | Sign On → invalid ID + PIN ×3 → Device Locked ("Present Supervisor Card") | auth | @destructive | 4099922, 4100045 |
| 5 | Sign On submit while comms down → Communication Locked screen | auth | @destructive | 4099924, 4100041 |
| 6 | Valid sign-on, **MotD unavailable** → "Message of the Day Unavailable" → continue | auth | — | 4099925, 4100047 |
| 7 | Valid sign-on, **Word & Colour unavailable** → "Word & Colours of the Day Unavailable" → continue | auth | — | 4099925, 4100048 |
| 8 | Valid sign-on, MotD present → dated message shown → press any key → continue | auth | — | 4099925, 4100044 |
| 9 | Word & Colour of the Day shown (colour blocks + WORD) → press any key → Main Screen | auth | — | 4099925, 4100046, 4100049 |

> `Covered by` filled in 2026-08-06 against live TestRail suite 30253.
> Paths 4–7 (lockout, comms-locked, and the two "unavailable" branches) are exactly the kind of edge
> cases that tend to be missing from a suite — worth checking first.

## Screen states (Given/Then anchors — wording quoted from the screens)
- **1_0 Idle Screen** — Translink logo; "Present Card" / "or" / "Press Any Key to Continue"; clock.
- **1_1 Sign On** — header "Sign On"; **ID** field, **PIN** field; "Press Enter to Confirm" + Enter
  button. (Sub-states: Empty Fields → ID Entered → PIN Entry → PIN Entry (4 digits).)
- **1_2_2 Please Wait…** — spinner; transitional while authenticating.
- **1_2_1 Communication Locked** — red ✕; "Communication Locked"; "Your device has been
  automatically locked as it has not been communicating…"; "Please Notify a Supervisor or Technician".
- **1_3_1 Sign On Failed** — red ✕; "Sign On Failed"; "The ID or PIN is incorrect"; "Please try
  again"; **"1 of 3"** attempt counter.
- **1_4_1 Device Locked** — red ✕; "Device Locked"; "The ID or PIN was entered incorrectly too many
  times"; **"Present Supervisor Card"**.
- **1_3_2 Message of the Day** — dated notice (e.g. "25 Oct 2019 | 15:23 …"); "Press Any Key to Continue".
- **1_5_1 Message of the Day Unavailable** — red ✕; "Message of the Day Unavailable"; "Press Any Key…".
- **1_4_2 Word & Colour of the Day** — two colour blocks (e.g. orange | green) + a "WORD"; "Press Any Key…".
- **1_6_1 Word & Colours of the Day Unavailable** — red ✕; same message, unavailable variant.
- **2_2 Main Screen (Rail selected)** — ticket sales: Rail/Bus/Misc/Day Tours/Smartcard tabs, ticket
  types + prices. The signed-on landing screen.
- **7_1_2 Metro Smartcard — "Please Present Smartcard"** — appears downstream of the main screen
  (smartcard sub-flow); likely **not** part of sign-on itself.

## Confirm against Overflow — RESOLVED 2026-08-04 against the full verbatim transcription

- ~~Is Communication Locked reached on sign-on submit, at idle, or both?~~ **RESOLVED: from Idle
  only.** The transcription's connection list has `1.0 Idle Screen → 1.2.1 Communications Locked`
  directly; the `Sign On Succesful?` decision only branches to `Please Wait...` or `Sign On -
  Incorrect Details`, never to Comms Locked. So Comms Locked is an idle-state condition (device
  already can't reach the back office before a sign-on is even attempted), not a submit-time failure.
- ~~Do Message of the Day / Word & Colour show on every sign-on or only when present?~~ **RESOLVED:
  genuinely conditional**, confirmed by two explicit decision points ("Is Message of the Day
  available?", "Are Word and Colour of the Day available?"), each with real Yes/No branches to the
  content screen or its "Unavailable" fallback. The original modelling was correct.
- Retry counter 1→2→3 then Device Locked — **narrowed, not fully resolved.** Confirmed: a single
  "Sign On - Incorrect Details" screen is the branch point for both outcomes — it connects back to
  retry (Empty Fields / PIN Entry) **and** forward to Device Locked, per the annotation "If User
  enters an incorrect Pin for more than the allowed number of attempts, the Device will become
  locked." Still open: the exact attempt threshold and whether anything resets the counter — the
  transcription confirms the mechanism, not the exact number.
- ~~Does a successful sign-on land directly on Main Screen, or is a step missed?~~ **RESOLVED, plus a
  new detail:** both `Word & Colour of the Day` and its `Unavailable` variant connect straight to
  `2.2 Main Screen - Rail selected` — no missed step. But there's a **second, parallel destination**:
  both also connect to `7.1.2 Metro Smartcard / Please Present Smartcard`, and the annotation says
  "Metro Operator will go to this screen after Sign On" — i.e. which screen a signed-on operator
  actually lands on depends on the operator's mode (Rail → Main Screen; Metro → Present Smartcard
  directly). The existing diagram above only shows the Rail/Main path and should be extended with a
  Metro branch — flagged here rather than guessed at, since the exact mode-selection trigger isn't
  in this transcription.
- Cross-check: `automation-tests` asserts a **`state.changed`** EventLog entry on successful sign-on
  — still open, this transcription is screen/flow-only and doesn't cover back-office audit events.

source: `knowledge/flows/translink-pos-full-transcription-v4.0.3.md`, board "2. 1.0 Sign On"
(Chrome-extension verbatim transcription, 2026-08-04).
```
