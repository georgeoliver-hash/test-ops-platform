# Sign On & Session — old → new (worked example)

How the old `AA-POS Acceptance Test` Sign On cases consolidate into the new
`GG - POS - Claude Suite`, applying `docs/test-practices.md`. Drafted cases: `sign-on.cases.yaml`.

## What the old suite looked like (the problem)
- **Triplication:** the same sign-on behaviours written per mode (NIR/Ulsterbus/Metro) — e.g.
  "Operator sign on - Manual" exists 3× (C2668237 + 2).
- **Inconsistent duplicates:** Supervisor sign-off appears as `Supervisor Menu - Sign Off`,
  `Supervisor Menu: Sign Off`, and `Supervisor Sign off` (dash vs colon vs plain) — same behaviour,
  three cases.
- **Mixed altitude:** behaviour cases (with REQ refs) sit alongside screen-by-screen micro-cases
  ("Sign On - Empty Fields / ID Entered / PIN Entry") that have no refs and thin steps.
- **Coverage holes:** Invalid Credentials / Device Locked / Unlock exist for some roles+modes but
  not others; "Sign On Messages Unavailable" exists only for Metro; Communication Locked has no
  functional case at all (only TIBU confirmation tests).

## The consolidation (≈40+ old cases → 25 new, `@mode(all)`)
Each new case is written **once** and runs under the NIR/Ulsterbus/Metro **Configurations** —
no per-mode copies. Decisions by the rubric:

| New case (see YAML) | From old | Action |
|---|---|---|
| Idle → Sign On screen | C4056022 | rewrite (raise from micro-state to behaviour) |
| Screen shows ID + PIN fields | C4056022/23 | merge micro-cases → 1 |
| Operator/Supervisor/Technician/Administrator sign on (manual) | C2668237, C4053266, C4053279, C3550481 (each ×modes) | **copy+rewrite, collapse modes** |
| Sign on by smartcard — **per role** (Operator/Supervisor/Technician/Administrator) | C2669055, C4053267, C4053280, C3550482 | copy+rewrite, collapse modes, **kept per role** (role-specific cards); fold TIBU-20813 on Operator |
| Incorrect credentials → Sign On Failed + counter | C2669075 + C4056026 | merge + fold TIBU-22671, TIBU-24379 |
| Three attempts → Device Locked | C2669077 + C4056027 | merge + fold TIBU-22672, TIBU-22003 |
| Unlock with Supervisor card | C2682258 | copy+rewrite + fold TIBU-21384 |
| Communication Locked | — (none) | **NEW gap** (flow 1_2_1) + fold TIBU-28530, TIBU-21278 |
| Message of the Day (present) | — | new (flow 1_3_2) |
| Message of the Day Unavailable | C4053106 (Metro only) | copy+rewrite → universal |
| Word & Colour (present / unavailable) | — | new (flow 1_4_2 / 1_6_1) |
| Operator sign off | C4053105 + C4056028 | **merge dupes** + fold TIBU-21440, TIBU-26846 |
| Supervisor / Technician / Administrator sign off | 3+2+3 inconsistent dupes | **merge each → 1** |
| Auto sign-off (inactivity) | C2691758 (Ulsterbus only) | copy+rewrite → universal |
| Power-cycle forced sign-off | C4095749 (Metro, no steps) | rewrite to real steps + fold TIBU-24790 |
| Audited sign on/off events | C4095807/8/9 (Metro, no steps) | rewrite → one @bos case |

## "Do we need a new test?" — applied
- **Most answers were NO-new-test:** the bulk is *collapse modes* and *merge duplicates*, not new
  cases. We did **not** create a case per TIBU bug — 11 sign-on defects were **folded as regression
  assertions/links** into the case that already owns the behaviour (linked via Refs).
- **Genuinely new** (true gaps the flow exposed, nothing covered them): Communication Locked, the
  universal "Unavailable" message fallbacks, Word & Colour of the Day.

## Bugs folded (regression coverage, linked via Refs not title)
TIBU-20813 (smartcard sign-on), 22671/24379 (incorrect-details), 22672/22003 (device-locked),
21384/21278 (unlock/comms), 28530 (comms-lock timing), 21440/26846 (sign-off), 24790 (forced sign-off).

> **Menu/role defects deferred:** several "sign-on related" TIBU hits are really role-menu issues
> (Supervisor Duty Information, Technician Force Comms, Operator Options, Admin Network Settings —
> TIBU-21096/21110/21138/22632/22640/22649/24740…). Those belong to the **Operator/Supervisor/
> Technician/Administrator** functional areas (flows 9–12), not Sign On — they'll be folded there.

## Traceability preserved
REQ refs carried through (REQ-0050/0056/0276/2821/3013 sign-on; REQ-0099 lockout; REQ-1137 unlock),
now in the **Refs field** alongside the folded TIBU ids — so both "is REQ-X covered?" and "is bug Y
pinned?" are answerable.

## Confirmed by George
- **Day messages** (Message of the Day, Word & Colour of the Day) **always show on sign on when
  configured** — drafts reworded to "when configured".
- **Communication Locked** is a genuine reachable state — case retained.
- **Smartcards are role-specific** → smartcard sign-on kept as a case per role.

## Open confirmations (minor, non-blocking)
From `knowledge/flows/translink-pos-signon.md`: is Comms Lock checked at idle or on submit; the
attempt-counter reset behaviour; any step between Word & Colour and the Main Screen. These refine
wording only.
