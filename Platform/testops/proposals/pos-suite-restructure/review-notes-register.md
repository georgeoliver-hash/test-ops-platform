# POS suite — George's review notes (2026-06-03), audited against the live suite

George's gospel review of `GG - POS - Claude Suite`. Each note mapped to the actual live cases
(from the section dump) and classified. Verdicts: **EXISTS** (already covered) / **EDIT** /
**REMOVE** / **REORGANISE** / **ADD** / **DECISION** (needs George's call before building).

| # | Note (verbatim, condensed) | Live evidence | Verdict |
|---|---|---|---|
| 1 | Sign On locks after 3 attempts — value is TMS-configured, may not be 3 | C4099922 "Sign On — device locks after 3 attempts" | **EDIT** title+steps → "after the configured number of attempts (TMS)"; don't hard-code 3 |
| 2 | Operator Break "no Out Of Service" is pointless — other Break test covers it | C4099941; siblings C4099939 enter, C4099940 leave | **REMOVE** C4099941 (fold any unique check into C4099939/40) |
| 3 | Bus (Ulsterbus/Metro) section not relevant to Metro | C4099982–986 (Functional/FLU/Bus shared, superseded); C4100379–383 (Metro/FLU) | **REMOVE** both: the superseded shared Bus FLU **and** Metro/Fare-Look-Up (Metro can't sell tickets). Keep Ulsterbus/FLU C4100374–378 |
| 10 | Can't sell tickets on Metro — only top-ups + new smartcard issues | C4100412 "Metro — sell a ticket"; Metro/Tickets section | **REMOVE** C4100412 + Metro/Tickets section. Keep Metro/Top Up + Metro/Issue Card |
| 11 | Issue Card in Rail/UB aren't card issues; overlaps the Tickets section | C4100032 "Issue Card — Warrant option (rail)"; empty NIR/Issue Card & Metro/Issue Card sections; NIR/Tickets/Warrant C4100398 | **REORGANISE**: drop C4100032 (Warrant is a ticket, covered by C4100398); remove empty NIR/Issue Card; **move** Metro MJ issue C4100025 + Metro Travelcard issue C4100029 into Metro/Issue Card |
| 20 | Test for Card Dump | C4099964 "Administrator — Card Dump" | **EXISTS** ✓ (confirm wording covers it) |
| 21 | Test for Card Clear | C4099963 "Administrator — Clear Card" | **EXISTS** ✓ |
| 4 | Top Up should include UB MJ products | C4100392 "Top Up — Ulsterbus Multi-Journey" (Ulsterbus/Top Up); generic C4100009 | **PARTIAL** — UB MJ top-up exists; ADD any further UB MJ product variants if >1 |
| 5 | Issue Card should include UB MJ + UB Town Service Travelcard | Issue from Blank C4100024–032,390 has Metro MJ/Travelcard but **no** UB MJ / Town Service | **ADD** "Issue Card — Ulsterbus Multi-Journey", "Issue Card — Town Service Travelcard" |
| 6 | All top-up options need a test per payment option (Cash/Warrant/Card) | Top Up C4100007–017,388,389,435 — no payment-method dimension | **DECISION** — data-variation line per case, or dedicated per-payment cases? (Warrant = Rail/UB only, not Metro) |
| 7 | All new-issue options need a test per payment option (Cash/Warrant/Card) | Issue from Blank cases — no payment-method dimension | **DECISION** — same approach as #6 |
| 8 | Smartcard validation should cover all card-type variants (e.g. Half-Fare: Partial Sighted, Learning Disability, No Driving Licence) | Smartcards C4100413–418; Validation C4100018–021,427,428; screen-val evidence: Senior, DLA, yLink, 24+, Dependants single | **DECISION/ADD** — confirm full variant list; data-variation vs per-variant cases |
| 9 | Tickets section misses ticket types — e.g. Child products, Cross-Border | Functional/Tickets C4100419–423; NIR C4100393–402; UB C4100403–411; rail XB C4100429 | **ADD** Child products + Cross-Border products (list to confirm) |
| 12 | Need Passenger Display tests for Rail and UB POS | C4100033 generic passenger display only | **ADD** "Customer Display — Rail" + "Customer Display — Ulsterbus" |
| 13 | Need tests for Application + Topology updates via TMS | none | **ADD** (new area) — DECISION on what to verify (trigger, version reported, no data loss, audit event?) |
| 14 | Need test for enabling Euros currency for Cross-Border products | C4100429 (rail XB + currency toggle, partial) | **ADD** "Cross-Border — enable Euro currency" (config + applied to XB products) |
| 15 | Need annulments of new-issued smartcards, top-up, ticket issues | C4099996 last-txn, C4099997 new smartcard ✓, C4099998 MJ top-up ✓, C4100386 BVP | **PARTIAL** — smartcard + top-up annul exist; **ADD** explicit "Annulment — ticket issue" |
| 16 | Check mini statements after actions (usage, top-ups) | C4100017 top-up mini statement; C4100004 receipt mini statement | **ADD** "Mini Statement — reflects validation/usage and top-ups (incl. other devices)" |
| 17 | Setting Default Boarding Stage in Technician | Bus-FLU '*'-key cases C4099986/378/383; screen-val C4100084 Boarding Location | **ADD** "Technician — set Default Boarding Stage" (config action, not the '*' key behaviour) |
| 18 | Ticket-issue tests must include Green Banner on successful issue | all Tickets cases (Functional/NIR/UB) | **EDIT** (bulk) — add AND "a green success banner is displayed" to ticket-issue cases |
| 19 | Tests for changing boarding & alighting stages on Rail and UB | UB: C4099984/376/381 ✓; Rail: stations C4099972 but no explicit change-stage | **ADD** "Rail FLU — change boarding & alighting stations" (UB already covered) |
| 22 | Test for changing Ethernet setting in Network Settings | C4099957 Technician Network Settings, C4099967 Admin Network Settings (generic) | **EDIT/ADD** — add explicit "change Ethernet setting" (fold into C4099957 or new case) |

## Roll-up
- **Remove/bin:** C4099941; shared Bus FLU C4099982–986; Metro/FLU C4100379–383; Metro sell-ticket C4100412; rail Warrant "issue card" C4100032. (Removes go via UI — API delete unavailable — so they'll be flagged `ZZ_DELETE_*`.)
- **Reorganise (UI moves):** Metro MJ issue C4100025 + Metro Travelcard issue C4100029 → Metro/Issue Card; drop empty NIR/Issue Card.
- **Edit:** C4099922 (TMS threshold); ticket-issue green-banner (bulk); Ethernet (C4099957).
- **Add (clear):** UB MJ + Town Service issue; Passenger Display Rail/UB; Euro currency enable; ticket-issue annulment; mini-statement-after-action; set Default Boarding Stage (Technician); Rail change boarding/alighting.
- **Decisions needed first:** payment-option coverage style (#6/#7); validation-variant list+style (#8); ticket-type list for Child/Cross-Border (#9); TMS update scope (#13).
