# Bug-regression sweep — disposition of all 247 TIBU defects

- **171 already folded** into the new suite (refs on the committed cases).
- **76 not yet covered** — classified below: **FOLD** (add the ref to the named area during its
  reformat pass) or **LEAVE** (out of POS functional-test scope, with reason).

## FOLD — add ref to an existing case in this area
| TIBU | What it is | Fold into |
|---|---|---|
| 19341 | Sign On — Cancel doesn't return to previous field | Sign On / Failures |
| 22563 | 'C' button on sign-in after Operator Break | Sign On / Break + Failures |
| 19559 | Signing on to Metro Home Location shows wrong screen | Sign On (Metro) |
| 24891 | POS didn't sign off automatically | Sign On / Sign Off (auto) |
| 19560 | Time shown 12hr not 24hr, no seconds | Technician / Display (new check) |
| 21411 | Time one hour in the future | Technician / Display (clock) |
| 19374 | Rail Cross-Border (XB) ticket price wrong | NIR / Fare Look-Up |
| 21770 | Rail FLU (L4) text says "example" | NIR / Fare Look-Up |
| 21933 | Presenting smartcard on Rail FLU → fatal | NIR / Fare Look-Up |
| 24862 | Rail FLU boarding/alighting/ticket layout | NIR / Fare Look-Up |
| 24853 | Auditing wrong boarding/alighting/purchase location | NIR / Fare Look-Up + Audit |
| 24855 | Route reference id not audited | Audit / FLU |
| 24848 | Rail ticket template naming alignment | Receipts & Printing (rail) |
| 24795 | Half-fare/concession smartcard "not recognised" | Top Up / Faulty Card |
| 20868 | Metro Daylink — Card Ref amount in Days-Left field | Top Up / DayLink |
| 24051 | Adult MJ Inner Zone top-up crash | Top Up / Multi-Journey |
| 24350 | Metro Travelcard top-up doesn't proceed | Top Up / Metro Travelcard |
| 25081 | Metro MJ mini-statement expiry text wrong | Top Up / mini statement |
| 25078 | Travelcard first-use wrong error screen | Top Up / Metro Travelcard |
| 25886 | Can't top-up journeys if card has expired journeys | Top Up |
| 21463 | Expired MJ prints no receipt on top-up | Top Up / Receipts |
| 22558 | On-screen mini statement missing card details | Top Up / mini statement |
| 21219 | Non-toppable card → (crash) on presentation | Top Up / Faulty Card |
| 22985 | Rail — unable to top up / issue smartcards | Top Up |
| 26713 | Ulsterbus Town Service card first use | Ulsterbus / Top Up |
| 23009 | Metro MJ issue doesn't match UX flow | Metro / Issue Card |
| 24715 | Stuck on "Card Write Failed" screen | Issue Card |
| 25890 | Issuing — Top-Up option cut short | Issue Card / Top Up |
| 21443 | New Adult Belfast Visitors Pass can't be annulled | Annulment |
| 25073 | Re-presenting a different card during annul | Annulment |
| 25116 | Cancelled tickets information incorrect | Annulment |
| 25404 | Metro — wrong journeys on annulment receipts | Annulment / receipts |
| 25800 | Metro — wrong journeys on iLink/Metro annul receipts | Annulment / receipts |
| 20914 | Fatal error printing Totals | Operator/Supervisor / Totals |
| 21367 | Supervisor Duty Information details page not shown | Supervisor / Reports |
| 22643 | Duty Information missing chevron-key instructions | Supervisor / Reports |
| 22647 | Day Information missing chevron-key instructions | Supervisor / Reports |
| 23928 | 'Back' on Paper Status → fatal | Technician / Paper Status |
| 15782 | Software Versions not showing real version numbers | Technician+Supervisor / Versions |
| 16044 | Cannot update Tray ID | Technician / Device Settings |
| 16228 | Cannot update Mounting Point ID | Technician / Device Settings |
| 20967 | Tray ID not prefixed with "AT" | Technician / Device Settings |
| 24866 | Device Settings UI changes | Technician / Device Settings |
| 26995 | Paper Low not being displayed | Non-Functional / Printer |
| 26860 | UX — Metro Travelcard Top-Up screen 7.5.8 | Screen Validation (Metro) |
| 26864 | UX — Metro MJ Issue screen 8.7.1 | Screen Validation (Metro) |
| 26871 | UX — BVP Issue screen 8.3.5 | Screen Validation |

## FOLD — to a new Non-Functional "device stability / performance" area
These are crash/freeze/perf items with no single functional home → one or two stability cases.
| TIBU | What it is |
|---|---|
| 25825 / 25826 / 25935 / 26648 | "Please Wait" freeze / infinite loop / freeze on startup / stuck |
| 26763 | Randomly crashes & auto-reboots |
| 21397 | BRReportTransactionSequenceIdsOutOfSync causing POS issue |
| 16113 / 25077 | Slow device performance |

## LEAVE — out of POS functional-test scope (don't carry into the suite)
| TIBU | Reason |
|---|---|
| 17471, 19017, 19373 | **Perth ETIM** — a different device/project, not Translink POS |
| 13513 | Post Hub — backend encryption-key storage |
| 21122, 22545, 26880 | Transactions in **Merit / Smartrack / Product Class** — back-office systems |
| 21121 | CloudFare transaction numbering — BOS data, not POS UI |
| 21118, 24870 | Software update mechanism / version batch send — infra/telemetry |
| 21447 | Device Log Manager configuration — infra/config |
| 22963 | Cellular connection/configuration **process** — provisioning, not a POS test |
| 20886 | Commissioning from decommissioned state — provisioning/process |
| 18895, 18897, 21825 | CLESS stack / ESN read — contactless firmware/backend |
| 15942, 20815, 20876 | USB access prompts (Metro / Bixolon LCD / MIURA) — peripheral driver/setup |
| 24273 | BVT/Jira tracking item, not a test (per George) — leave |

**TIBU-23963** (was blank-titled): identified by George — "pressing Adult Belfast Visitors after
placing an Adult BVP or iLink Zone 1 'blank' card shows the iLink Zone card options." → **FOLD into
Issue Card** (blank-card option handling).

## Next step
The FOLD items get their ref added to the named case during each area's reformat pass (Roles,
FLU, Basket/Payment, Top-Up, Issue Card) plus a new Technician "Display/Clock" case and a
Non-Functional "Device stability / performance" case. The LEAVE items are consciously not carried
over (they stay in the old suite untouched).
