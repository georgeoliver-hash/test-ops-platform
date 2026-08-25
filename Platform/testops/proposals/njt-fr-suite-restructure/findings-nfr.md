# Findings — NJT Fare Register Non-Functional Requirements

**Scope.** Cross-examines the 14 existing TestRail "Non Functional Requirements" cases
(`reports/uk-bus-projects/njt-farebox-and-register-replacement/2026-08-13/area-cases/nfr.md`)
against the 13 NFRs catalogued in `knowledge/njt/specs/ss003-fare-register-nfrs.md` (source:
`NJT_FRFRP_SS003 Fare Register Non Functional Requirements.pdf`, v1, 6 Jul 2026).

## Coverage matrix — all 13 catalogued NFRs

| # | NFR (SS003) | Target | Case(s) | Classification |
|---|---|---|---|---|
| 1 | Start-up time | 4 min | C4105015 | **Covered** |
| 2 | Offline storage capacity | ≥5 days, no data loss | C4105017 | **Partial** — see below |
| 3 | CloudFare send latency — transaction | 10 s | C4105018 | **Covered** |
| 3 | CloudFare send latency — event | 10 s | C4105019 | **Covered** |
| 4 | Remote command apply latency | 5 s | C4105020 | **Covered** |
| 5 | Fleet-wide config update activation | ≤6 h | C4105021 | **Partial** — see below |
| 6 | Single-device config update activation | ≤1 h | C4105022 | **Covered** |
| 7 | Fleet-wide software update activation | ≤24 h | C4105023 | **Partial** — see below |
| 8 | Single-device software update activation | ≤1.5 h | C4105024 | **Covered** |
| 9 | Sign-on (Start of Run) | 3 s + report + Ticket Issue mode | C4105025 | **Covered** |
| 10 | Sign-off (End of Run) | 5 s + report + idle screen | C4105026 | **Covered** |
| 11 | Sign-on (Start of trip) | 3 s + Ticket Issue mode | C4105027 | **Covered** |
| 12 | Sign-off (End of trip) | 5 s + report + next-trip screen | C4105028 | **Covered** |
| 13 | Ticket/receipt print | 2.5 s | C4105029 | **Covered** |

**Result:** all 13 catalogued NFRs have at least one existing case (14 cases total; NFR #3 is
split across two cases, transaction data and event data, a reasonable 1:1 split of the same
metric's two data types per SS003 p.5). **No NFR is Missing** against this source document.

## "Partial" classification — 3 NFRs (#2, #5, #7)

Per `knowledge/njt/specs/ss003-fare-register-nfrs.md` ("Not testable via a single functional/
system test case" section): the existing cases for these three NFRs are written as simple,
same-run functional checks, but the underlying targets are inherently **soak-test** (#2) or
**fleet-scale** (#5, #7) claims that a single-device, single-pass case cannot fully verify:

- **C4105017** (Offline Transaction Data Storage Capacity) — as written, checks that logs/events
  "are stored locally" but does not exercise a genuine 5-day accumulation window. A same-day case
  can, at best, be a proxy (data-volume-per-day calculation) — it cannot itself prove 5 days of
  loss-free storage. (Source: SS003 p.5; distilled note "5-day offline storage capacity... needs
  either a multi-day soak or an audited proxy calculation".)
- **C4105021** (all devices, config update, 6h) — asserts "all Fare Registers" applied the
  update, but a functional case run against one test rig cannot represent an actual fleet-wide
  rollout at scale. (Source: SS003 p.6; distilled note "Fleet-wide items... testable only as
  fleet/soak tests, not standard functional cases".)
- **C4105023** (all devices, software update, 24h) — same fleet-scale caveat as above. (Source:
  SS003 p.6, same distilled note.)

These are not wrong to have as functional smoke checks, but they should not be presented as full
verification of the fleet-wide/soak target. Recommendation logged to the gap register: supplement,
don't replace, with a dedicated soak/fleet-rig test owned outside the standard per-case suite
pattern.

## Ungrounded-category check (security / environmental / reliability)

Per `knowledge/njt/specs/ss003-fare-register-nfrs.md`: SS003 defines **only three** topic groups
(§2.1 System Initialization & Offline Resilience, §2.2 Cloud Synchronization & Configuration
Management, §2.3 Driver Operations) and explicitly has **no security, environmental, or
reliability/MTBF sections**.

**Check result: none of the 14 existing "Non Functional Requirements" cases claim to test
security, environmental, or reliability/MTBF behaviour.** All 14 cases' sections and content map
exactly onto SS003's three defined groups with no case outside that scope. So there is **no
ungrounded case to flag in this batch** — the suspected finding from the task brief does not
materialise against these 14 cases.

This does surface the inverse finding, though: **security, environmental, and reliability/MTBF
NFRs have zero TestRail coverage under "Non Functional Requirements" at all** — not because they
were tested against the wrong source, but because no case for them exists yet. Since SS003 itself
states the formal baseline NFRs live in the FDR documentation (not this doc), this is a genuine
open question for the engineer: do FDR-sourced security/environmental/reliability NFR cases exist
elsewhere in the suite, or is this an uncovered gap? Logged to the gap register.

## Cross-cutting finding — Performance Disclaimer not reflected in any existing case

SS003 §1 / Performance Disclaimer (p.4): every metric in Section 2 is a **non-binding engineering
design goal** ("Target"), explicitly stated not to constitute a breach of contract if missed. None
of the 14 existing cases' Expected results reference this disclaimer — each reads as if the timing
figure is a hard pass/fail contractual gate. This is a standards/wording finding (not a
missing-coverage finding) — logged to the gap register rather than edited in place, consistent
with this task not touching the existing 14 cases.

## Cases drafted

Three new cases drafted into `proposals/njt-fr-suite-restructure/nfr.cases.yaml`, one per Partial
NFR (#2, #5, #7), explicitly framed as soak-test/fleet-scale-rig checks (not standard single-run
functional cases) and citing the SS003 non-contractual Target disclaimer. These supplement — they
do not replace or edit — the existing C4105017 / C4105021 / C4105023.
