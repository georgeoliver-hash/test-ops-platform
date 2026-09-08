# ETM deep spec-grounding audit — suite 30254

**Date run:** 2026-07-22 (folder kept at `2026-07-21` per the task's target path). **Verdict: DONE for
Functional/Non-Functional/Regression/Smoke citation-resolution; HMI sample-verified only (disclosed).
Audit CLEAN of blocking findings.**

## Summary table

| Metric | Count |
|---|---:|
| Total cases in suite (incl. ZZ bin) | 524 |
| Active (non-ZZ) cases | 454 |
| ZZ - To Delete (untouched, out of scope) | 70 |
| Corrected this pass | 6 |
| Verified-clean-with-citation this pass (newly re-checked against full spec) | 5 |
| Flagged-gap this pass (new gap-register Qs) | 2 (Q25, Q26) |
| Carried forward, already deep-audited 2026-07-17 (not re-derived this session) | ~163 |
| HMI Screen Validation — sample-verified only | 280 (of which ~6 spot-checked in prior passes) |
| Not reached (ZZ bin) | 70 |

## What changed today

Six cases corrected and pushed live (`proposals/coherence-audit/fixes/etm-deep-audit.rewrite.json`,
applied via `tools/apply_rewrite.py --commit`):

- **C4100550** — dropped an unearned "the change receipt can be annulled" clause; that behaviour is
  owned by the existing C4100551.
- **C4100545** — the "alighting-stage key toggles currency" claim had no spec support anywhere in the
  requirements library; reworded to the gherkin-standard "Unknown how" pattern (outcome kept, exact
  control deferred to the tester with a `**GAP**` marker). Gap logged as **Q26**.
- **C4100950 / C4100949** — both asserted a CloudFare Activity Log event for a claim (print speed;
  sustained-use response time) that has **no matching event type** anywhere in FBD-100358's full
  §3.2.1–3.2.18 list. Dropped the ungrounded step from both. C4100950 also had its unstated numeric
  print-speed target replaced with the "assumed-configured-value" precondition pattern.
- **C4100945** — "FEIG" and "Open Payments" terminology has zero hits in the requirements library;
  marked `**GAP**` (logged as **Q25**) rather than asserted as fact; dropped the same ungrounded
  CloudFare-event step.
- **C4100944** — the vague "the corresponding event is recorded" now names the actual event: **Device
  Status** (FBD-100358 §3.2.12), the only event type covering a device power/restart condition.

Two cases from the 2026-07-17 pass were re-checked against the full spec text (not just re-flagged)
and are now **verified-clean-with-citation** — no wording change needed, just confirmation:

- **C4103547** (Rail Sub tap audit fields) — FBD-100335 para 155 supports the TransportationType
  assertion; the rail-sub gating question (whether it's live) was separately answered NO by George on
  2026-07-21 (gap Q20) — case correctly stays as-is, gated.
- **C4103548** (Rail Sub PJT ignored / MJT applied) — FBD-100335 **para 159** verbatim: *"the Maximum
  Journey Time still applies to these journeys"* — directly confirms the clause that was previously
  uncited at paragraph level.

A fresh, additional risk-weighted spot-check (not previously flagged by any pass) of 3 Transfer-area
citations against FBD-100271 (**C4103556, C4103553, C4103554**) all confirmed accurate.

## The four ETM facts George confirmed live on 2026-07-21 — full-suite check

Swept **all 454 active cases** for the wrong-version patterns; found no case beyond the 3 already
fixed on 2026-07-21 (C4100586, C4100587, C4100588) assumes:
- a customer tap-off on Metro/Ulsterbus (TOO/ETM-calculated or driver-selected only) — clean
- Ulsterbus flat/fixed fare (Metro-only now) — clean, the one stale case is in the ZZ bin
- absence of a customer-facing passenger display — clean, 2 cases correctly assume it exists
- absence of a fare-paying/e-purse smartcard product — clean, 3 cases correctly assume it's real

## Honest disclosure — what was and wasn't independently re-done this session

The suite already carried a **full** coherence + spec-grounding pass from 2026-07-17
(`proposals/coherence-audit/etm-1.findings.md`, `etm-2.findings.md`) that read all 455 then-active
cases and cited FBD-100662/100658/100335/100271/100831/100358 etc. per case, plus a 2026-07-21
terse-wording pass that reread the same 455 for prose/citation bloat. This session:
- Pulled a **fresh** dump (not reused the 2026-07-21 raw file) and reconfirmed suite shape.
- Took every item that pass left **open/uncertain** (8 findings) and resolved each one against the
  **full** FBD text via `tools/extract_req.py` — not just re-stated the earlier finding.
- Full-suite-swept for the 4 specific facts George corrected live yesterday.
- Spot-checked 3 additional, not-previously-flagged citations as a confidence check on the earlier
  pass's citation quality (all passed).
- **Did not** independently re-open and re-derive a citation for each of the remaining ~163
  Functional/Non-Functional/Regression/Smoke cases from raw spec text in this session — that would
  substantially duplicate the 2026-07-17 pass's already-cited, already-reviewed work. If a full,
  independent second read-through of those ~163 cases against raw spec text (as opposed to resolving
  the earlier pass's open items) is wanted, that is separate, not-yet-done work.
- **HMI Screen Validation (280 cases)** — sample-verified only, per the task's explicit allowance;
  relied on the prior passes' ~6-case representative sample rather than re-sampling. Not a full
  280-case check.

## Audit result

`python -m system_test_ops audit --suite 30254` (after commit): **CLEAN of blocking findings** — 0
across every blocking rule (mojibake, preface/preconds/steps/expected structure, compound-THEN, stray
tags). 74 pre-existing advisory title findings (length/em-dash style) remain, out of this pass's scope.

## Paths

- Rewrite: `proposals/coherence-audit/fixes/etm-deep-audit.rewrite.json`
- Changelog: `proposals/coherence-audit/fixes/etm-deep-audit.changelog.md`
- Gap register additions: `proposals/coherence-audit/gap-register.md` (Q25, Q26)
- Fresh raw dump: `proposals/coherence-audit/fixes/etm-suite-30254-raw-2026-07-22.json`
- Audit report: `reports/tfts-system-test/new-etm-acceptance-suite/2026-07-22/alignment-audit.md`
