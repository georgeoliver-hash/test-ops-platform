# PV Acceptance Suite (30255) — terse-not-bloated compression pass

Date: 2026-07-21
Mandate: `docs/gherkin-standard.md` § "Terse, not bloated — trust the tester (George, 2026-07-21 — a
hard rule)". Scope: suite **30255** (`**NEW** PV-Acceptance Test Suite`, project 42) only.

## What was done

1. Pulled the suite fresh and live at the start of this pass (not reused from earlier in the day,
   per instruction — the suite had already had a coherence-fixes / release-coverage / comms-failover
   pass earlier today):
   - `python -m system_test_ops cases --project 42 --suite 30255` → 136 cases.
   - Full raw case bodies via `TestRailClient.get_cases(42, 30255)` (title, `custom_preface`,
     `custom_preconds`, `custom_steps_seperated`, `custom_expected`, `refs`) dumped to
     `reports/tfts-system-test/new-pv-acceptance-test-suite/2026-07-21/cases.raw.json`.
2. Read and classified **all 136 cases** (100% coverage, not a sample) against the mandate:
   full sentence-style Given/And/When/Then/Expected text where a short tag would do, and any
   citation/date/"confirmed by X"/spec-paragraph reference baked inline into the body a tester
   executes.
3. Result: **135 of 136 cases were already clean** — terse tag-style preconditions/steps/expected
   throughout, and every existing citation (`FBD-#####`, `TIBU-#####`, `REQ-####`) already lives in
   the case's **Refs** field, not in the Given/When/Then body. This includes the two cases the brief
   flagged as likely prime targets from today's edits:
   - **C4101085 "Comms Failover — Ethernet loss fails the PV over to cellular"** — preface/preconds/
     steps are already terse and citation-free; `refs` already carries `REQ-2746.0, TIBU-24428`.
   - **C4103568 "Comms Lock — a sustained loss of both Ethernet and cellular…"** and
     **C4103569 "Comms Recovery — transactions queued during an outage…"** — same: already terse,
     `refs` already carries `FBD-100359[, TIBU-24428]`.
   Conclusion: an earlier pass today (the "coherence fixes" / "release-coverage build" mentioned in
   the brief) had already applied this exact tersification + citation-relocation to the suite before
   this session started. Re-pulling live data (as instructed) confirmed that state, rather than
   finding fresh bloat to fix.
4. The **one** remaining case with inline citation/provenance text in the body: **C4101005
   "ZZ_DELETE_REVIEW - Barcode — single-use validation"** (Delete section). Its `custom_preface` read:

   > `**UNCONFIRMED (audit 2026-07-17)** — has the PV validating a single-use barcode; FBD-100167
   > says PV validates multi-use only, and sibling C4103559 correctly rejects it. Confirm before
   > running — gap-register Q8.`

   This bakes a spec citation (`FBD-100167`), an audit date (`audit 2026-07-17`), and a gap-register
   pointer (`gap-register Q8`) directly into the objective text. Fixed via
   `proposals/coherence-audit/fixes/pv-terse-rewrite.rewrite.json` (`apply_rewrite.py`, dry-run then
   `--commit`):

   **Before:**
   > `**UNCONFIRMED (audit 2026-07-17)** — has the PV validating a single-use barcode; FBD-100167
   > says PV validates multi-use only, and sibling C4103559 correctly rejects it. Confirm before
   > running — gap-register Q8.`

   **After (preface):**
   > `**UNCONFIRMED** — PV validating a single-use barcode conflicts with sibling C4103559 (PV is
   > multi-use only); confirm before running.`

   **Refs field** (was empty) → `FBD-100167, gap-register Q8`

   No behavioural change: still slated `ZZ_DELETE_REVIEW` (superseded by C4103559); the fix only
   relocates provenance out of the body and shortens the remaining note to a tag-style fragment.
   `tools/apply_rewrite.py` already had a `refs` pass-through (checked the current source first, per
   instruction — no extension was needed).

## Coverage — honest disclosure

- **136 / 136 cases read and classified. 0 not-reached.**
- **1 case changed** (C4101005 — citation/date relocated to Refs, preface shortened).
- **135 cases already clean** — no further action; verified, not assumed.
- No case's tested behaviour, title, preconditions, or steps were altered in meaning — this was a
  compression/relocation pass only, per the mandate ("this is a compression pass, not a
  re-authoring pass").

## Audit result

`python -m system_test_ops audit --suite 30255` after the commit:

```
        0  mojibake
       11  title-no-emdash (advisory)
       13  title-too-long (advisory)
        0  preface-empty / preface-bad-preamble
        0  preconds-empty / preconds-no-given
        0  steps-empty / step-first-not-when / step-content-not-when-and / step-no-then
        0  then-compound-genuine
        0  expected-empty / expected-starts-then
        0  has-tags
  audited 135 cases: CLEAN; 24 advisory.
```

**CLEAN of blocking findings.** The 24 advisory findings are pre-existing title-style items
(missing em-dash / long titles, mostly on Screen Validation cases whose titles intentionally mirror
exact UI screen names) — unrelated to this pass and out of scope for the terse-not-bloated mandate.

## Files

- `proposals/coherence-audit/fixes/pv-terse-rewrite.rewrite.json` — the one-case rewrite proposal.
- `proposals/coherence-audit/fixes/pv-terse-rewrite.changelog.md` — this file.
- `reports/tfts-system-test/new-pv-acceptance-test-suite/2026-07-21/cases.raw.json` — full live case
  dump used for the classification pass.
- `reports/tfts-system-test/new-pv-acceptance-test-suite/2026-07-21/alignment-audit.md` — the
  post-commit audit report.
