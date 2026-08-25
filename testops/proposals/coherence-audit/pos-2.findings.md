# POS Coherence & Grounding Audit — Part 2 (indices 265–end)

**4 of 265 cases flagged** — High: 0 | Medium: 1 | Low: 3

## Scope note
Of the 265 cases audited, **251 are single-step "Screen Validation" cases** with an
identical structure (`GIVEN reached '<screen>'` → `WHEN operator views the screen` →
`THEN matches approved design`). Title, preface, precondition and expected are all
derived from the same screen name, so they are coherent by construction, and each screen
name resolves to a real `.webp/.png` in the repo `knowledge/flows/...` tree — no invented
screens or capabilities. These were not individually flagged (per the "skip clean cases"
instruction).

The only cases containing real device actions / multi-step behaviour are the **14
behavioural cases** at the tail (4100358, 4100359, 4100437, 4100438, 4100360, 4100361,
4100436, 4100362–4100366, 4100371, 4100372). All findings below come from that set. Most
are coherent; the ones below have grounding gaps not confirmable from the FBD-* specs
(these behaviours — power/suspend/audio/printer — are driven by the flow screens, not by
the fares/barcode/reporting FBD specs, so several values cannot be verified against a
requirement).

## Findings

**C4100360** | Medium | coherence + needs-confirmation | Title "Power — interruption duration determines resume state". Steps: `S1 WHEN power is interrupted briefly and restored → returns to the screen the operator was on`; `S2 WHEN power is lost for less than the Auto Sign Off time → on restart the POS goes to the Operator Break screen`. The S1 condition ("briefly") and the S2 condition ("less than the Auto Sign Off time") **overlap** — a brief interruption is also "less than Auto Sign Off" — yet they assert different outcomes (same screen vs Operator Break). The discriminating variable (did the device reboot?) is never stated, so the two buckets are ambiguous as written. Separately, this case says Auto-Sign-Off-window power loss lands on the **Operator Break screen**, whereas C4100436 S1 says an Auto-Sign-Off inactivity timeout goes to the **Idle screen with "break mode skipped"** — the destination of a sign-off is modelled two different ways across the pair. No FBD-* spec confirms the threshold model or either destination. | Restate the three buckets by an unambiguous variable (e.g. "no reboot occurred" vs "rebooted, downtime < Auto Sign Off" vs "downtime ≥ Auto Sign Off"); reconcile the Operator-Break-vs-Idle destination with C4100436 against the actual power/sign-off requirement before use.

**C4100436** | Low | needs-confirmation | Title "Sign Off / Suspend — inactivity timers". Asserts a specific chain — `FLU inactivity for Auto Sign Off → Idle, no waybill, "break mode skipped"`; `Idle inactivity for Auto Suspend → screen off/suspend`; `Suspend Duration elapses → reboots and returns to Idle`. Internally coherent, but the "break mode skipped" behaviour and the auto-reboot-after-suspend step are not found in any FBD-* spec, and "break mode skipped" appears to conflict with C4100360's Operator-Break outcome (see above). | Confirm the three timer names/behaviours and the "break mode skipped" rule against the device configuration/power spec; align with C4100360.

**C4100358** | Low | needs-confirmation (grounding) | Title "Printer — paper jam detected and recoverable". `E1 THEN the Paper Jam screen is shown AND the Annul Transaction control responds`. Annulment is a real device-only capability, but that a **Paper Jam screen carries an Annul Transaction control** is asserted from the flow image only — not confirmed by any FBD-* requirement. Otherwise coherent. | Confirm the Paper Jam screen actually exposes an Annul Transaction control (check the flow screen / print-recovery requirement); if it does not, drop that clause.

**C4100437** | Low | needs-confirmation (grounding) | Title "Printer — paper low notification". `E1 THEN a temporary paper-low notification is shown (about 3 seconds)`. The **"about 3 seconds"** duration is not stated in any FBD-* spec (3s timeouts appear elsewhere for barcode error screens — FBD-100483/100167 — a different context, so this looks like a value carried over by assumption). Scenario is otherwise coherent. | Confirm the paper-low notification duration against the printer/UX requirement, or soften to "a temporary notification" without asserting a specific duration.

## Cases reviewed and passed (behavioural set)
C4100359 (out of paper), C4100438 (print-failure events → CloudFare), C4100361 (audio
tones; error tone corroborated by FBD-100373), C4100362–C4100366 (comms loss / recovery /
token / reader-failure rate-limit / status+Tray ID), C4100371 (Please Wait stability),
C4100372 (sustained-use performance) — all internally coherent with actions grounded in
real device/CloudFare behaviour.
