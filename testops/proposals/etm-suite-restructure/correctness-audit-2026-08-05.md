# ETM correctness sense-check — confirmed issues (2026-08-05)

Not a coverage-gap check (that's `flow-coverage.md`) — this checks whether cases that already exist
say the **right thing**. Every finding below survived an independent adversarial re-read (a second
agent tried to refute it against the actual case text and flow-map/knowledge source, blind to the
first agent's reasoning) before landing here. 41 potential issues were flagged; 30 survived
verification, 11 were refuted as false positives and are not listed.

**None of these have been edited yet.** This is a findings list for you to triage — some are one-line
wording fixes, some need a design/spec answer before they can be fixed at all.

## By defect type

### Invented detail (case asserts something not in any source) — 15
| Case | Flow-map | What's invented |
|---|---|---|
| 4100511 | driver-signon | Smartcard-removal effect on First Use Safety Check screen — not in any source |
| 4100513 | driver-signon | "skipped ... or overridden per configuration" — source shows a deterministic screen, not a skip/config-override |
| 4100615 | technician | Brightness/volume adjustment via L2/R2/L4/R4 keys — Display Settings only has Restore Defaults + Go Back |
| 4100620 | technician | CloudFare Activity Log reboot-entry audit — not documented for Soft Reboot anywhere |
| 4100550 | flu-ticket-issue | "flows to MERIT and SmartTrack" (ETM only audits to CloudFare) + title "(Metro Single)" when this sub-flow is mode-generic |
| 4100640 | flu-printer-travel-mode | Invented "Paper Out condition" screen + "replace roll restores printing" — no such screen documented |
| 4100641 | flu-printer-travel-mode | Asserts printer-failure trigger as settled fact; flow-map's own notes call this exact case built on an unconfirmed assumption |
| 4100546 | flu-printer-travel-mode | Relabels documented on-time/within-tolerance/outside-tolerance as "early/on time/late" — not the source's framing |
| 4100627 | barcode-scanning | Asserts multi-use reference validates via Driver Menu entry; source explicitly says multi-use is "reviewed post R2.0" (unconfirmed) |
| 4100628 | barcode-scanning | Barcode-appended-at-end-of-printout + no-duplicate/no-orphan guarantee + "legacy barcodes handled the same way" — none in source; empty Refs |
| 4100635 | power-interruption | Narrows generic "screen they were on" to specifically "FLU screen" |
| 4100635 | power-interruption | Invents a CloudFare Activity Log/Estate Management audit trail for power interruption — not documented |
| 4100637 | power-interruption | Invents a hold/loop mechanic ("held until sufficient charge") vs. source's simple boot-progression |
| 4100634 | revenue-limit | States "requires a Supervisor/Technician to proceed" as fact; source only says "must be notified" — the flow-map's own notes already flag this exact gap |
| 4100607 | driver-menu-options | "Inspector report is printed" on valid smartcard — source shows a screen-transition/remove-card flow, no print action |

### Contradicts the flow-map (case and source actively disagree) — 12
| Case | Flow-map | The contradiction |
|---|---|---|
| 4100514 | driver-signon | Case says "configured attempts"; flow-map's own notes confirm the literal transcribed rule is exactly 3 attempts and says to cite that, not leave it vague |
| 4100515 | driver-signon | Case collapses the documented two-stage (transient warning → persistent lock) comms-fail model into one simultaneous outcome |
| 4100597 | driver-menu-options | Cited for the "Restore Defaults" path but only tests manual raise/lower — never presses Restore Defaults |
| 4100551 | driver-menu-annulment | Cited for the fail→retry→succeed loop but actually tests an unrelated timeout scenario; no case in the whole cited set exercises the real loop |
| 4100551 | driver-menu-annulment | Case asserts an active "refused with reason" dialog on stage-change; flow-map says the annulment list simply clears (nothing to annul) — plus invents MJ-validated/pass-validated/concession-pass as refusal triggers absent from any source |
| 4104522/4104524/4104525 | flu-abt-emv | ABT passback family (3 cases) assert a bare "enters passback" continuation; flow-map specifies an explicit failure screen (02.6.5) requiring 2s/removal/L6 to clear — flow-map's own notes already flagged this as worth double-checking |
| 4100563 | flu-basket-mode | Asserts a "greyed out Add More to Basket button"; source explicitly documents a "Basket Full error" message instead — no button-greying anywhere in source |
| 4100539 | flu-promo-numeric | Cited for a purpose-specific "Unable to Calculate Change" message but only asserts a generic unnamed error-bar message |
| 4100624 | barcode-scanning | Asserts "queued offline result posts to CloudFare" as confirmed under the wrong decision node (that exact behaviour is a *different*, explicitly-untested path in the same flow-map) |
| 4104538 | barcode-scanning | Mislabels a manual operator "Not Valid" rejection (post-validation) as an automatic "online validation fails" (scan-time) outcome |
| 4100636 | power-interruption | Uses an entirely different recovery model (recovery-period/break-state/"10A FLU") than the flow-map's temporary-vs-longer/shutdown model, with no shutdown outcome at all — flow-map's own notes already flagged this as an unreconciled near-duplicate |

### Wrong behaviour (case asserts a branch it never actually reaches) — 2
| Case | Flow-map | Issue |
|---|---|---|
| 4100557 | flu-printer-travel-mode | Cited for the "driver annuls instead of retrying" branch; every step in the case is actually the retry-succeeds path — annul is never selected or asserted |
| 4100613 | supervisor-menu | Cited for the Soft-Reboot-lands-on-Idle-Screen path (the one thing that distinguishes it from the Driver Menu's own Soft Reboot) but never asserts a landing screen at all — the flow-map's own notes already called this the highest-risk gap in the whole ETM pass |

### Outdated — 1
| Case | Flow-map | Issue |
|---|---|---|
| 4100613 | supervisor-menu | Same case as above — reads like a generic reboot case that predates the Idle-vs-On-Break distinction being documented |

## Pattern worth noting
Several of these (4104522/24/25, 4100551 ×2, 4100613, 4100634, 4100641, 4100636) are cases where **the
flow-map's own Notes/unknowns section had already flagged the exact discrepancy** during the earlier
coverage pass, but nothing had gone back to fix the case yet. That's a good sign the process is
working — the gaps were visible, just not yet acted on.

## Done (2026-08-05, later same day)
All 28 non-conflicted findings fixed and pushed live to suite 30254 —
`proposals/etm-suite-restructure/correctness-fixes-2026-08-05.cases.yaml` (26 cases updated, 2 new
cases created: C4105033 "Ticket Issue — annulment fails then retry succeeds", C4105034 "Ticket Issue
— printer or power interrupt during print, driver annuls"). Conformance audit CLEAN (0 blocking, 75
pre-existing advisory titles, unrelated). The two unconfirmed-mechanism cases (4100634, 4100641) were
edited to remove the invented certainty and now carry an inline `**UNCONFIRMED**` marker citing
gap-register.md Q12/Q6 respectively — not left un-touched, but not asserted as fact either.

**4100636 deliberately NOT edited** — it's a live CONFLICT with 4100635 (two different, unreconciled
recovery models for power loss), not a simple wording fix. Logged as Q16 in
`proposals/coherence-audit/gap-register.md`, Session 2026-08-05. Whichever framing George confirms is
correct, the other case needs rewriting to match — that's the next action once answered.
