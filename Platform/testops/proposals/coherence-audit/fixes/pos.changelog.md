# POS fixes — 2026-07-21

Suite: **30253** (`**NEW** POS-Acceptance Suite`, project 42). Pushed live via
`tools/apply_rewrite.py proposals/coherence-audit/fixes/pos.rewrite.json --commit`.
Source of both fixes: George (live-system confirmation), 2026-07-21.

## 1. C4100414 ("Youth") and C4100417 ("Concession") — condemned as duplicates

George confirmed neither is a distinct entitlement type on the live system: "Youth" is the
yLink product under a different label, "Concession" is the Half-Fare product under a
different label.

Read the full live content of all four cases (`custom_preface`, `custom_preconds`, and all
4 `custom_steps_seperated` steps each) before acting:

- **C4100414 "Smartcard — Youth"** vs **C4100415 "Smartcard — yLink"** — same preface shape,
  same preconds pattern (NIR/Ulsterbus mode, entitlement smartcard available, NIR Adult
  Single example), identical 4-step body (present card → recognised/entitlement applied →
  CloudFare activity log → MERIT → SmartTrack). Only the product label differs (yLink
  additionally cites FBD-100250). No distinct scenario found in C4100414 beyond the label
  swap.
- **C4100417 "Smartcard — Concession"** vs **C4100413 "Smartcard — Half Fare"** — same
  shape again (Ulsterbus Adult Single example), identical 4-step body. Only the product
  label differs.

**Result:** both condemned — titles now prefixed `ZZ_DELETE_REVIEW -` (soft-delete; the
TestRail instance doesn't support hard delete via API, per `CLAUDE.md`'s documented
constraint). Content/steps left untouched other than the title prefix. yLink (C4100415) and
Half Fare (C4100413) remain the cases of record for those entitlements.

## 2. C4100360 vs C4100436 — break-mode contradiction

Both cases carried an in-suite `CONFLICT (audit 2026-07-17)` banner pointing at
`gap-register.md` Q18: *"power/suspend sign-off destination (break mode skipped or not?)"*.
George's answer, recorded in the gap register: **break mode is used.**

Read both cases' full live content:

- **C4100360 "Power — interruption duration determines resume state"** — step 2 already
  said: power lost for less than the Auto Sign Off time → *"on restart the POS goes to the
  Operator Break screen."* This case already modelled **break mode used**.
- **C4100436 "Sign Off / Suspend — inactivity timers"** — step 1 said: FLU inactivity for
  the Auto Sign Off period → *"the POS reverts to the Idle screen with no waybill (break
  mode skipped)."* This case modelled **break mode skipped** — the opposite of C4100360,
  and now confirmed wrong.

**Winner: C4100360.** It already modelled the confirmed-correct behaviour and needed no
step/precondition changes — only its preface was updated to replace the `CONFLICT` banner
with a `CONFIRMED (George, live-system confirmation, 2026-07-21)` note, closing gap Q18.

**Corrected: C4100436.** Step 1's expected outcome was changed from "Idle screen, no
waybill (break mode skipped)" to *"the POS goes to the Operator Break screen with no
waybill printed"* — mirroring C4100360's exact wording pattern. Because step 1 no longer
lands on the Idle screen, step 2's precondition was changed from "inactive on Idle" to
"inactive on the Operator Break screen" so the chain (FLU timeout → Break → Suspend →
reboot to Idle) stays internally consistent. Steps 2–4's expected outcomes are otherwise
unchanged. Not condemned as a duplicate of C4100360 — its trigger (inactivity-timer
configuration: FLU/Idle/Suspend/Suspend-Duration) is a genuinely different scenario from
C4100360's power-interruption-duration trigger, and it uniquely covers the Auto Suspend +
auto-reboot steps.

**Residual gaps flagged, not resolved by this fix** (left as explicit markers, not
guessed):
- Whether the Auto Suspend timer runs from the Operator Break screen itself, or whether
  Break first auto-transitions to Idle before the Auto Suspend timer starts, is not stated
  in any FBD-* spec (`proposals/coherence-audit/pos-2.findings.md` already flags this case
  Low/needs-confirmation for the same reason). The step-2 precondition edit is the minimal
  change needed to keep the corrected step 1 internally consistent — not a newly confirmed
  mechanic.
- C4100436's `custom_expected` summary field (business-value/automation-tag field, not part
  of the Gherkin body) still reads "FLU inactivity → Idle (no waybill, no break)" —
  `tools/apply_rewrite.py` only updates `title`/`custom_preface`/`custom_preconds`/
  `custom_steps_seperated`, not `custom_expected`, so this field needs a manual follow-up
  edit in TestRail to stay consistent with the corrected steps.
- C4100360's own internal ambiguity (its "briefly interrupted" vs "less than Auto Sign Off"
  step conditions overlap without a stated discriminating variable — flagged Medium in
  `pos-2.findings.md`) was **not** addressed here; out of scope for the break-mode question
  asked, left for a follow-up pass.

## Push record

- Proposal: `proposals/coherence-audit/fixes/pos.rewrite.json`
- Applied: `python tools/apply_rewrite.py proposals/coherence-audit/fixes/pos.rewrite.json`
  (dry-run, verified 2 updated / 2 removed / 0 missing), then `--commit` (pushed live to
  suite 30253, twice — once for the initial content, once to fix a preface-preamble
  conformance finding, see below).
- Audit: `python -m system_test_ops audit --suite 30253` → **CLEAN of blocking findings**
  after one round-trip fix (the first commit tripped 2 `preface-bad-preamble` findings
  because the CONFIRMED banner was placed before the required "This test is to confirm..."
  opening sentence; reworded so both prefaces open with that sentence and carry the
  CONFIRMED banner after it — re-audit came back clean, 50 pre-existing advisory
  title-length/em-dash findings unrelated to this change remain, as expected/allowed).
- Report: `reports/tfts-system-test/new-pos-acceptance-suite/2026-07-21/alignment-audit.md`
