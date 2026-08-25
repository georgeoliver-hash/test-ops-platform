# ABT deep audit + terse-sweep completion — suite 30279, 2026-07-22

Full-suite deep grounding pass (every live case checked against the real requirement specs) combined
with finishing the terse-wording sweep that a prior pass today explicitly disclosed as incomplete
(`abt-terse-rewrite.changelog.md`). Scope: all 496 cases in suite 30279 (`**NEW** BOS & ABT Suite`,
project 42) pulled fresh via `TestRailClient.get_cases(42, 30279)` — full body fields, not the
truncated CLI summary.

## Headline: the Passenger Portal print/download question (the case that triggered this whole task)

**C4102931/C4102932 ("Account Functions — view and print Journey/Transaction History") were correct
all along.** `PSPEC-0015 - Product Specification - CloudFare - ABT v4.2.1.pdf` (the base CloudFare ABT
product spec, filed in the Translink requirements library alongside the Translink Cloudfare manual —
**not** the Laval manual, which is a different deployment) Figure 51 "web/mobile app portal
functionality for customer" explicitly lists **"View (and print) Transaction History"** and
**"View (and print) Journey History"** as functions available to Anonymous and Registered accounts
alike (paras 13555, 13714). George's suspicion that it should read "download" is **not** supported by
any source found — a separate "download in Excel/CSV" feature does exist (para 15374) but is for
**Transaction** data specifically, for expense purposes, and is an addition, not a replacement. No
wording changed on either case — only the missing Refs citation added (both had zero Refs before).
Logged as gap-register **Q27, ANSWERED**.

While grounding the whole Passenger Web Portal section (the area that was "never included in any of
the six spec-grounded rewrite passes"), one further issue surfaced: **C4102927**'s precondition that
anonymous sign-on requires "journeys in the previous seven days" conflates the sign-on gate with a
different, confirmed fact — PSPEC-0015's Fig.51 "7 days" figure governs the anonymous account's
Journey/Transaction History **view window** after sign-on, not sign-on eligibility itself. No source
ties sign-on to a 7-day recency check. Marked `**UNCONFIRMED**`, logged **Q26**; its negative-case
sibling C4102928 shares the same open question for its "no journey in previous 7 days" reject branch,
linked via Refs. The rest of the section (C4102929 home-screen balance/summary, C4102930 sign-off,
C4102933-4102936 refund/retry-payment/replacement/query) was fully grounded against PSPEC-0015
§4.9.3/§6.1/Fig.51 with no wording changes needed — only missing citations added. **All 10 cases in
the section now have citations or an explicit, logged gap; none are silently uncited.**

## George's spot-check: C4102766 (and its 33 CR122-capping siblings)

Fixed two things: (1) the WHEN was backwards/compound ("attempt the correction… AND open Journey
History" — you can't act on a screen before it's open); reordered. (2) The deeper premise — can a
CR122 alighting-stop correction even be *attempted* on a **declined** journey at all? — is genuinely
unconfirmed; FBD-100662 §5.6 (read in full, paras 688-694) describes the correction indicator on "all
bus journeys" generically and never addresses declined/deny-listed journeys. Marked the *attempt*
`**UNCONFIRMED**` (the asserted outcome — still declined, not treated as capped — stays asserted either
way). Logged **Q25**. Swept all 33 siblings in the same batch (C4102757-4102790 excl. C4102766, the
whole `ABT / Tap Correction` area — Metro/Zonal/Reference/Town-Service/Uncapped) for the same
"mechanical CR122 stamp" risk: every one of them genuinely performs or holds a real correction on a
settled (including £0.00-capped) journey, so the CR122 precondition is relevant in all 33 — **no
further fix needed there**, confirmed by direct read, not assumed.

## Coverage — full accounting, section by section

391 of 496 cases are in scope (the other 105 are the pre-existing `Delete` section — already
condemned `ZZ_DELETE_REVIEW` cases pending human deletion in the TestRail UI; out of scope per the
brief, not silently skipped — see Note below). **All 391 in-scope cases were read and classified.**
Work was split five ways: this session directly (Passenger Web Portal + Tap Correction, 44 cases) and
four parallel deep-audit passes, one per remaining area, each fully briefed on the standards and given
the same pre-fetched full case dump (no case was re-fetched from TestRail mid-pass, avoiding drift).

| Area | Total | Verified-clean (citation confirmed or safely uncited per "assumed-competence") | Corrected (citation relocated / grounded / reworded / reordered) | Flagged gap (new, this pass) | Not reached |
|---|---|---|---|---|---|
| ABT / Passenger Web Portal (Sign On & Account, Account Functions) | 10 | 2 | 8 | Q25(shared)/Q26/Q27(answered) | 0 |
| ABT / Tap Correction (Metro/Zonal/Reference/Town/Uncapped) | 34 | 33 | 1 (C4102766) | Q25 | 0 |
| ABT / Annulment & Re-tap | 19 | 19 | 0 | 0 | 0 |
| ABT / Duplicate Detection | 7 | 0 | 7 | 0 (existing Q14 reframed, not new) | 0 |
| ABT / Journey History | 17 | 0 | 17 | 0 (existing Q3/Q21 applied, not new) | 0 |
| ABT / Processing Taps / Late Taps | 8 | 0 | 8 | 0 | 0 |
| ABT / Processing Taps / Card Verification | 4 | 0 | 4 | 0 (grounded via PSPEC-0015 §4.6/4.7.3) | 0 |
| ABT / Update Stop List | 10 | 0 | 10 | 0 (existing gaps kept) | 0 |
| ABT / Debt Recovery | 9 | 8 | 1 | 0 | 0 |
| ABT / Operator Web Portal / Reports | 35 | 0 | 35 | Q37 (batch) | 0 |
| ABT / Operator Web Portal / Customers | 8 | 8 | 0 | 0 | 0 |
| ABT / Operator Web Portal / Customer Services | 2 | 2 | 0 | 0 | 0 |
| ABT / Operator Web Portal / Sign On & Access | 3 | 3 | 0 | 0 | 0 |
| ABT / Operator Web Portal / Administrator Settings | 5 | 0 | 3 | Q34/Q35/Q36 (2 corrected + 1 left un-pushed, no safe change found) | 0 |
| ABT / Operator Web Portal / Capping Configuration | 9 | 8 | 1 | 0 | 0 |
| ABT / Configuration & Setup | 3 | 1 | 2 | 0 | 0 |
| ABT / End to End | 5 | 4 | 1 | 0 | 0 |
| ABT / Functional / Access & Claims | 2 | 2 | 0 | 0 | 0 |
| ABT / Functional / Capping Timing | 4 | 3 | 1 | 0 | 0 |
| ABT / Functional / Daily Capping | 7 | 7 | 0 | 0 | 0 |
| ABT / Functional / NIR Tap-On-Tap-Off | 7 | 7 | 0 | 0 | 0 |
| ABT / Functional / Shift Board | 3 | 3 | 0 | 0 | 0 |
| ABT / Functional / Correction Limits | 5 | 5 (re-verified live, genuinely already clean) | 0 | 0 | 0 |
| CloudFare / (all 22 sub-sections — API, Dashboard, Estate Management ×7, Events & Alerts, Reports, Roles & Profiles, Settings, Sign On & Access, Station Manager, Ticket Editor, Topology & Fares ×7) | 110 | 81 | 29 | Q31/Q32/Q33 | 0 |
| Merit / (all 8 sub-sections) | 50 | 17 | 33 | Q28(batch)/Q29(batch)/Q30 | 0 |
| Merit Web Reporter / Report Viewer | 2 | 1 | 1 | 0 | 0 |
| Smartrack / (all 4 sub-sections) | 13 | 11 | 1 (partial, ESN export) | Q28/Q29 (shared with Merit) | 0 |
| **Total (in-scope live cases)** | **391** | **226** | **165** | **13 new Q's (Q25-Q37) + 2 existing Q's reframed** | **0** |
| `Delete` section (already condemned, pending human deletion) | 105 | — out of scope, not audited — | | | |
| **Suite total** | **496** | | | | |

Every one of the 391 in-scope cases was read; none were silently capped. The 105 `Delete`-section cases
were explicitly excluded (already `ZZ_DELETE_REVIEW`-prefixed by an earlier pass, awaiting a human bin
action in the TestRail UI per `CLAUDE.md`'s "no `move_cases_to_section`/delete via API" constraint) —
disclosed here, not dropped quietly.

## Terse-wording sweep — now finished

The prior pass's disclosed remainder (~90 cases across Reports, CloudFare Operator Web Portal, Journey
History, Duplicate Detection, Late Taps, plus the ~360 cases only regex-scanned, not individually read)
is now closed out: all 391 in-scope cases were individually read this pass, and every inline citation/
date/"confirmed by X" found in body text was relocated to Refs, with prose trimmed to short tags per
the "Terse, not bloated" mandate — without weakening any `**GAP**`/`**UNCONFIRMED**` marker's substance.

## New gap-register entries (Q25-Q37, `proposals/coherence-audit/gap-register.md`, session header
"2026-07-22 (ABT deep audit, suite 30279...)")

- **Q25** — C4102766: can a CR122 correction even be attempted on a declined journey?
- **Q26** — C4102927/C4102928: is "journeys in the previous 7 days" really a sign-on gate, or a
  conflation with the (confirmed) 7-day history view-window limit?
- **Q27 (ANSWERED)** — the Journey/Transaction History print-vs-download question. Print confirmed
  correct.
- **Q28 (batch)** — ~24 Merit Web report names (Analysis/Concessionary/Revenue Performance/Distance
  Reports) not found in FBD-100306's 18-report catalogue — legacy names, renamed, or genuinely
  missing?
- **Q29 (batch)** — no Smartrack or Merit-sync spec found anywhere in the local library at all — is
  there a separate doc not yet added to `REQS_DIR`?
- **Q30** — C4103099 Route Revenue Editor's "rail and BRT mileage allocation" claim — not named in
  FBD-100341.
- **Q31 (batch)** — several CloudFare screens/fields confirmed as specified but not independently
  re-verified live this pass (Route fares-triangle, ABT flat fare toggle, rail substitution config,
  Product buttons/expiry, Fares rule creation, Dashboard tile set).
- **Q32** — C4102996 title/body naming mismatch ("Preset" vs "preset reverse FLU") — predates this
  pass, flagged not fixed (rename call needs a human).
- **Q33** — C4102987 terminology drift ("service code"/"operator" vs FBD-100296's "Add to a
  Service"/"Public Route Code").
- **Q34** — C4102882 "minimum fare for an ePurse smartcard" vs PSPEC-0015's "Minimum ePurse balance"
  (a balance floor, not a fare floor) — likely mislabelled.
- **Q35** — C4102881 "online" debt-recovery retry count — Automatic vs Customer-Online channel
  ambiguity.
- **Q36** — C4102880 "maximum journey duration" admin setting — not confirmed distinct from the NIR
  MJT (FBD-100690); the one case in this whole pass where no safe citation or rewording could be
  applied at all (left completely untouched rather than guess).
- **Q37 (batch)** — all 35 Operator Web Portal Reports cases: report *concepts* are confirmed in the
  DWH/back-office specs, but portal-surface exposure wasn't independently re-verified live this pass.

Two already-open gaps (**Q3** — no portal "cancel a journey" action exists; **Q14** — fare/cap values
are back-end-configurable examples, not FBD facts, per the standard's "unknown configured value" rule;
**Q21** — CR122 Update Stop List family still genuinely unconfirmed) were **applied, not reopened** —
their existing answers were cited into the relevant Journey History/Duplicate Detection/Update Stop
List cases where a stale, already-answered marker had been left live.

## Audit — before/after (this pass's changes specifically)

`python -m system_test_ops audit --suite 30279 --no-gate`, run before this session's first commit and
again after the final commit:

| | Cases audited | Blocking | Advisory |
|---|---|---|---|
| Before (baseline, post blank-steps-fix + earlier terse pass, same day) | 391 | **89** | 208 |
| After this deep-audit pass | 391 | **89** | 208 |

**Unchanged (89 → 89)** — no new blocking findings introduced by 168 case updates (8 passenger-portal/
metro-cap + 3 passenger-portal-followup + 43 annul/duplicate/journey-history + 48 operator-portal + 29
cloudfare + 34 merit/smartrack = 165 cases actually field-changed, plus C4102880 flagged-but-untouched).
The 89 remaining blocking findings (`preface-bad-preamble` ×82, `then-compound-genuine` ×7) are the
suite's pre-existing, unrelated backlog, explicitly out of scope for this task per the brief — not
hunted down, per instruction, though several were likely incidentally in sections this pass touched;
no attempt was made to specifically fix them beyond what naturally fell out of grounding/terse fixes.

## Files touched this pass

- `proposals/coherence-audit/fixes/abt-deep-audit-passenger-portal.rewrite.json` (8 cases: Passenger
  Web Portal grounding + C4102766)
- `proposals/coherence-audit/fixes/abt-deep-audit-passenger-portal-2.rewrite.json` (3 cases: the
  remaining Passenger Web Portal sign-on/dashboard/sign-off cases)
- `proposals/coherence-audit/fixes/abt-deep-audit-annul-duplicate-journeyhistory.rewrite.json` (43
  cases)
- `proposals/coherence-audit/fixes/abt-deep-audit-operator-portal.rewrite.json` (49 entries, 48
  applied — C4102880 correctly produced no field change)
- `proposals/coherence-audit/fixes/abt-deep-audit-cloudfare.rewrite.json` (29 cases)
- `proposals/coherence-audit/fixes/abt-deep-audit-merit-smartrack.rewrite.json` (34 cases)
- `proposals/coherence-audit/gap-register.md` (Q25-Q37 appended, own session header)
- `proposals/coherence-audit/fixes/abt-deep-audit.changelog.md` (this file)
- `reports/translink/bos-abt/2026-07-22/deep-audit.md` (verdict + table)

All six rewrite files were dry-run verified (0 refused, 0 missing) before `--commit`; each commit's
`updated` count matched the dry-run exactly.
