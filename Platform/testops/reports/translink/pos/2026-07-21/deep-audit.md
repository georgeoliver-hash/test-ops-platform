# POS deep audit — suite 30253, 2026-07-21/22

## Verdict

**Suite is materially sound.** A full citation-grounded, case-by-case sweep of all 530 active cases
(628 total minus 98 out-of-scope `ZZ_DELETE_*`/`Delete` cases) found the large majority already
correctly grounded, but confirmed George's original concern was right: this suite had never had a
full per-case check against the real FBD/PSPEC source documents, and that gap had let two classes of
defect through — a **mode-boundary contradiction** (Metro claimed card payment in one case, cash-only
in its sibling) and a **duplicated behavioural contradiction** that an earlier same-day fix hadn't
fully propagated to. Both are now fixed. The audit is **CLEAN of blocking findings** post-fix.

## Coverage table

| Area | Cases | Verified-clean | Corrected | Flagged-gap | Sampled | Not-reached |
|---|---:|---:|---:|---:|---:|---:|
| Sign On & Session / Roles (Operator/Supervisor/Technician/Administrator) / Smoke | 50 | 44 | 2 | 0 | — | 0 |
| Fare Look-Up (Rail/Bus/Common) / Tickets / NIR-UB-Metro mode-specific | 57 | 30 | 26 | 1 | — | 0 |
| Basket & Payment / Top Up / Issue Card / Smartcards / Barcode / Refund | 87 | 80 | 5 | 2 | — | 0 |
| Non-Functional (Comms/CloudFare, Printer, Power & Audio, Device Stability) | 14 | 9 | 4 | 1 | — | 0 |
| Screen Validation (16 sub-sections) | 322 | 51† | 0 | 0 | 322 | 0 |
| **Total** | **530** | **214** | **37** | **4** | **322** | **0** |

†Full-body checked; the remaining 271 got a title-only sweep (see below) — disclosed sampling, not
silent partial coverage, per George's explicit instruction for this area only.

**No case anywhere was silently skipped.** Every Functional/Non-Functional case (208 total) was
individually checked; Screen Validation (322) was sampled per instruction with exact disclosure of
what was and wasn't full-body graded.

## By area

### Sign On & Session / Roles / Smoke (50 cases) — 44 clean, 2 corrected
Mostly excellent grounding already (FBD-100183 hardware citations, TIBU regression pins, the
assumed-knowledge "configured value" pattern used correctly throughout for lockout/timeout thresholds).
**Finding**: C4099933 ("Sign Off — automatic") and C4099934 ("Sign Off — forced by power cycle") still
modelled the old, now-disproven "Auto Sign Off skips break mode" behaviour — the exact contradiction
already found and fixed in C4100360/C4100436 back on 2026-07-17, just not propagated to these two.
Corrected to match the confirmed live behaviour (Auto Sign Off → Operator Break, not Idle).

### Fare Look-Up / Tickets / mode-specific (57 cases) — 30 clean, 26 corrected, 1 gap
**Most significant finding of the whole audit**: C4100391 ("Top Up — Metro Multi-Journey") claimed a
Card payment option on Metro, directly contradicting its own sibling case C4100425 ("Metro — payment
is cash only") in the very same section. Fixed by removing the false Card variation. The other 25
corrections were a recurring citation-placement pattern (an FBD number baked into precondition prose
instead of the Refs field) concentrated in NIR/Ulsterbus Tickets sections the earlier terse-rewrite
pass hadn't reached — now swept clean. One case (C4100411, Rail Substitution Service) was upgraded
with a concrete worked example (Larne Line) where it had previously been vague.

### Basket & Payment / Top Up / Issue Card / Smartcards / Barcode / Refund (87 cases) — 80 clean, 5 corrected, 2 gaps
The **Refund** (12 cases) and **Barcode Validation** (8 cases) sub-areas are exemplary — every case
cites its FBD paragraph precisely, including exact spec worked examples. Five ref-only/spelling fixes
applied elsewhere (group-ticket citation, barcode-sync citation, "Dependents"→"Dependants" spelling
consistency, a bare citation tightened to specific paragraphs). One real gap-worthy finding: C4103581
("Heartbeat") asserted a specific CloudFare behaviour straight from a document that itself frames the
mechanism as a *proposed* solution, not confirmed shipped — a textbook "CR written ≠ feature live"
case. Marked `**UNCONFIRMED**`.

### Non-Functional — Comms/Printer/Power&Audio/Device Stability (14 cases) — 9 clean, 4 corrected, 1 gap
Four printer/audio cases previously had no citation at all; all four are verbatim confirmed by the
Overflow flow-annotations doc (§15.0 Printer Errors, §16.0 Power Interruption & Audio Tones, §2.0
FLU-Bus for the timeout tone) — added as citations, no wording changed. One case (C4100363, comms
"recovery reconnects and syncs") has no citation anywhere and its mirror case is TIBU-pinned while it
isn't — flagged as a gap rather than blocked (low risk, uncontradicted). **Process note**: this
14-case slice was initially mis-scoped out of every batch during setup and caught mid-pass — audited
separately, nothing lost.

### Screen Validation (322 cases, sampled per instruction) — clean
51 cases (~16%) full-body graded across all 16 sub-sections (spread through each section's id range,
weighted toward the two largest sub-sections), plus a 100% title sweep of all 322 to catch outliers.
Zero template breaks, zero mode-boundary violations (specifically checked: no bus-ticket/rail-ticket/
smartcard-validation screen scoped to Metro, consistent with Metro selling no tickets), zero mis-filed
functional cases. This is the highest-volume area in the suite and the cleanest — consistent with
being template-generated per-screen checks rather than hand-authored behavioural claims.

## Audit result

`python -m system_test_ops audit --suite 30253` (post-commit): **CLEAN of blocking findings**.
528 cases audited (98 out-of-scope `ZZ_DELETE_*` excluded), 0 blocking across every rule, 43 advisory
(title-length/em-dash only, pre-existing, explicitly advisory per `CLAUDE.md`).

## New open questions (gap-register Q25–Q29)

Logged to `proposals/coherence-audit/gap-register.md` for George's Q&A loop:
- **Q25** — tooling gap: no local REQ-id index (extract_req.py matches FBD filenames only).
- **Q26** — is Excess Ticket's rail-only claim backed by an FBD, or TIBU-only traceability?
- **Q27** — is FBD-100266's heartbeat Method 2 (StaffList reuse) confirmed live, or still proposal-only?
- **Q28** — is "Half-Fare" the real umbrella name for the Funded-group entitlement sub-types?
- **Q29** — is there any spec/design basis for the Comms "recovery reconnects and syncs" case, or is it an untested assumed inverse of its TIBU-pinned sibling?

## Files

- Changelog: `proposals/coherence-audit/fixes/pos-deep-audit.changelog.md`
- Rewrite proposals applied: `proposals/coherence-audit/fixes/pos-deep-audit-signon-roles.rewrite.json`,
  `pos-deep-audit-flu-tickets.rewrite.json`, `pos-deep-audit-basket-topup-cards.rewrite.json`,
  `pos-deep-audit-nfr.rewrite.json` (41 rows total, all applied `--commit`)
- Gap register: `proposals/coherence-audit/gap-register.md` (Q25–Q29 added)
- Conformance audit: `reports/tfts-system-test/new-pos-acceptance-suite/2026-07-22/alignment-audit.md`
