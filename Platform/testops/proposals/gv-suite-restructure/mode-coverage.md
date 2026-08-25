# GV direction (mode-execution) coverage map

**Why this doc exists.** GV is structured **feature/test-type-first** (Functional / Non-Functional /
HMI / Smoke), like ETM — not direction-first. That is deliberate (see `structure.md`'s "Mode decision"
section) but it means the section tree doesn't tell you which of the four **Direction** Run
Configurations a case needs to run under. This map is the missing signal, encoded directly on each
case's **Refs** field as a `MODE-*` tag, so both a human building runs and an automation harness can
answer "which configuration(s) does this case need?" without re-reading the whole suite.

## The direction dimension (not the same axis as fare/rail "mode")

GV's Configurations are **Direction**: `Entry` · `Exit` · `Bi-directional A→B` · `Bi-directional B→A`
— which physical direction the gate validates, set per lane/head. This is a different dimension from
the other devices' fare/operating mode (NIR/Ulsterbus/Metro on POS/ETM) — GV runs the same fare/product
logic regardless of direction; direction only changes the **gate mechanics** (open/close, arm
orientation, Tap-On vs Tap-Off classification) around an otherwise identical validation. Same execution
mechanism as the other devices though: TestRail **Run Configurations**, authored once, executed per
configuration.

## The six tags

| Tag | Meaning | Re-run under |
|---|---|---|
| `MODE-ALL` | Shared case; outcome could plausibly differ by direction (gate open/close, sensor/pictogram, throughput) even though steps are identical | All 4 configs |
| `MODE-ENTRY-ONLY` | Direction-specific: Entry only | Entry |
| `MODE-EXIT-ONLY` | Direction-specific: Exit only | Exit |
| `MODE-BIDI-AB-ONLY` | Direction-specific: Bi-directional A→B only | Bi-di A→B |
| `MODE-BIDI-BA-ONLY` | Direction-specific: Bi-directional B→A only | Bi-di B→A |
| `MODE-PRIMARY-ONLY` | Shared **and** genuinely direction-irrelevant (Technician Menu, HMI screen wording, comms/software distribution, most Non-Functional) | Once (Primary/Entry config only) |

A case can carry **more than one** direction-specific tag when the behaviour spans more than one
non-default configuration — see C4104025 below, the one case in this suite where that applies.

## Tally (111 live cases tagged; 1 `ZZ_DELETE_REVIEW` case excluded)

| Tag | Count |
|---|---:|
| `MODE-ALL` | 57 |
| `MODE-PRIMARY-ONLY` | 50 |
| `MODE-ENTRY-ONLY` | 2 |
| `MODE-EXIT-ONLY` | 2 |
| `MODE-BIDI-AB-ONLY` | 1 |
| `MODE-BIDI-BA-ONLY` | 1 |

(`MODE-EXIT-ONLY`/`MODE-BIDI-AB-ONLY`/`MODE-BIDI-BA-ONLY` sum to 4 tag-instances across 2 cases because
C4104025 carries all three.)

## Coverage by area

### MODE-ALL — runs under all 4 Direction configs (57 cases)
Everything whose `Then` touches gate mechanics (opens/stays closed/beeps), an audit record composed
per-head, or throughput — genuinely worth re-confirming on each physical head/config:

- **ABT cEMV Taps** (16 of 20): all valid-tap/decline/passback/offline/disarm cases — C4104011–4104016,
  4104018–4104024, 4104418–4104420. (4 of the 20 are direction-specific — see below.)
- **Multi-Use Barcode Validation** (19 cases) + its 11 product-variant expansions: C4104028–4104037,
  4104039–4104047, C4104421–4104431. No direction-specific divergence is spec-grounded for barcode in
  this suite (`structure.md`'s only named direction-specific areas are the ABT deny-list exception and
  Tap-On/Tap-Off classification, both barcode-adjacent NIR Transfers is separately flagged `needs-spec`
  and not yet built).
- **Passback** (5 cases): C4104048–4104052 — a reject is still a gate-stays-closed outcome.
- **Non-Functional / Resilience** (3 of 11): C4104091 (gate stays open, mains fail, user in aisle),
  C4104093 (Emergency Release Button opens the gate), C4104101 (Primary/Secondary throughput) — all
  explicitly gate-movement/throughput per the tag definition.
- **Smoke** (3 of 5): C4104103 (valid card opens gate), C4104104 (valid barcode opens gate), C4104105
  (immediate re-present rejected as passback) — each asserts a gate-open/close outcome.

### MODE-PRIMARY-ONLY — runs once (50 cases)
Direction-irrelevant by content — field procedure, technician workflow, screen wording, comms/device
state:

- **Commissioning & Router** (all 11): C4104053–4104063 — one-time install/router verification.
- **Technician Menu** (all 12): C4104064–4104075 — sign-on, navigation, Location Settings, Software/
  Config Versions, Display Brightness, Audio Volume, Force Communications. Exactly the "Technician
  Menu" example named in the tagging brief.
- **HMI Screen Validation** (all 17): C4104076–4104090, C4104111, C4104112 — screen wording/design is
  identical regardless of which physical head/direction shows it; the "HMI screens unrelated to gate
  movement" example named in the brief.
- **Non-Functional / Resilience** (8 of 11): C4104092 (≤2s power loss, no reboot), C4104094 (heartbeat
  loss → major fault), C4104095 (power-up OOS until both validators comms), C4104096 (mains restore →
  previous mode), C4104097–C4104100 (BOS/CloudFare comms, StaffList refresh) — device/comms state, not
  gate mechanics.
- **Smoke** (2 of 5): C4104102 (both heads boot into service), C4104106 (technician signs on to
  Technician Menu) — boot/technician-workflow checks, not gate-open/close assertions.

### Direction-specific (4 cases; all in ABT cEMV Taps — the only spec-grounded divergence point)
Per `structure.md`'s "Mode decision" section — the deny-list exception and the Tap-On/Tap-Off
classification are the *only* spec-grounded (`FBD-100690`) direction-specific behaviours in the suite:

| Case | Tag(s) | Why |
|---|---|---|
| C4104017 — "...is rejected in **entry mode**..." | `MODE-ENTRY-ONLY` | Title names entry mode explicitly; Entry rejects a deny-listed card outright |
| C4104026 — "an **entry-configured** gate audits the tap as a Tap On" | `MODE-ENTRY-ONLY` | Direction ⇒ Tap classification, entry side |
| C4104027 — "an **exit-configured** gate audits the tap as a Tap Off" | `MODE-EXIT-ONLY` | Direction ⇒ Tap classification, exit side |
| C4104025 — "an **exit-capable** gate opens for a deny-listed card but audits the tap invalid" | `MODE-EXIT-ONLY`, `MODE-BIDI-AB-ONLY`, `MODE-BIDI-BA-ONLY` | `structure.md` names this behaviour "Exit / bi-directional" — it applies to every config that has an exit-capable direction, i.e. every config except pure Entry |

## Flagged for engineer review (judgment calls made, not silently guessed)

These calls were made on the stated MODE-ALL criterion (outcome could plausibly differ by direction)
but are borderline enough to flag rather than bury:

1. **C4104020/4104021/4104022** ("reader stays disarmed when [ABT Type not Tap-On-Tap-Off /
   home-location outside NI Zone / product not configured]") — tagged `MODE-ALL` because disarming
   gates whether a tap is even processed (gate-open/close-adjacent), but these are arguably pure
   **configuration** checks (route/product config, not physical direction) that would give the same
   result regardless of which head runs them — closer in spirit to the `MODE-PRIMARY-ONLY`
   commissioning checks. Kept as `MODE-ALL` since disarming directly gates the open/close outcome;
   flagging so George can override to `MODE-PRIMARY-ONLY` if the config-check framing is preferred.
2. **C4104091/4104093** (mains-fail-gate-stays-open; Emergency Release Button) — tagged `MODE-ALL`
   because the gate arm physically stays open/opens, which is squarely the tag's own "gate open/close
   behaviour" example. Flagging because these read as safety/resilience mechanism tests (same hardware
   response regardless of which direction the lane is configured for) rather than validation-outcome
   tests — a reasonable case exists for `MODE-PRIMARY-ONLY` instead. No spec (`FBD-100348`, still
   pending integration) distinguishes behaviour by direction either way.
3. **C4104025's Bi-di scope** — `structure.md` names this "Exit / bi-directional" but doesn't specify
   whether **both** Bi-di A→B and B→A configs are exit-capable simultaneously or only whichever
   direction is "live" at a given moment. Tagged both `MODE-BIDI-AB-ONLY` and `MODE-BIDI-BA-ONLY`
   (in addition to `MODE-EXIT-ONLY`) on the conservative reading that a bi-directional gate is
   exit-capable in whichever direction is currently open, so the exception could surface under either
   Bi-di config. **UNCONFIRMED** — worth a one-line confirmation from the gate spec/vendor doc when
   FBD-100348 integration validation happens.
4. **Smoke section** (C4104103–4104105 tagged `MODE-ALL`) — smoke is meant to be a thin, fast sanity
   pass; tagging its gate-opening cases `MODE-ALL` means a full smoke run technically spans all 4
   configs if run to the letter of the tag. In practice a team may choose to run Smoke under one
   default config only for day-to-day sanity and reserve the full 4-way pass for release regression —
   that's a run-authoring choice, not a tagging one; noting it here so it isn't a surprise later.

## Not yet built (no tag needed today)

`structure.md` flags **NIR Transfers** (`[needs-spec]`) as a third potential direction-specific area
("any genuinely direction-specific transfer-window behaviour, TIBU-22401 territory") — no such section
exists yet in the live suite, so there is nothing to tag. When that section is authored, classify its
cases against this same six-tag scheme at that time.

## Keeping this accurate

Regenerate/extend this map whenever: (a) a new case is added to suite 30286 — classify and tag it
against the six values above before it's considered done; (b) the ABT deny-list-exception / Tap
classification spec (`FBD-100690`) is clarified for the Bi-di scope question in item 3 above; (c) NIR
Transfers or any other new direction-specific behaviour is authored — name it by direction and add it
to the "Direction-specific" table.

## Suites
- **Source (old, read-only):** 14973 `AA - Gate Validator - Acceptance Test`. Not touched by this task.
- **Target (tagged):** 30286 `**NEW** GV Test Suite` — all 111 live cases tagged in place via
  `update_case_fields` (refs appended, never overwritten).
