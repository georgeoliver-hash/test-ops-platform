# ETM Regression Defects — register (41 cases from old suite section "Regression Defects")

Defect ids are the **3xxxxx** numbers (and **TODM-###**) carried in the old case titles; some also
carry **REQ-####** refs. Per the consolidation principle (one test per risk, fold bug-fixes into the
owning behaviour), each defect is either **FOLD** (covered by an existing functional case — add the
defect id to that case's Refs) or **NEW** (no natural home → a dedicated Regression case).

| Defect | Title (old) | Disposition | Owning / new case |
|---|---|---|---|
| 301107 & 300367 | Power Glitch during Basket Purchase (Retry/Annul) | FOLD | Ticket Issue — printer/power interrupt during print; Basket Mode |
| 301058 | No Automatic Validation after Top-up | FOLD | Smartcard top-up — successful with auto-validation |
| 301074 | Sequence ID Out of Sync During Power Loss | **NEW** | Regression — sequence ID integrity across power loss |
| 301241 | Starting New Journey while Signed On — filter still applied | FOLD | FLU — start a new journey mid-shift |
| 301488 | ABT — wrong decline reason for passback & BIN list | FOLD | ABT — declined or error tap |
| 301186 | Paper Jam Multiple Tickets — annul before jam cleared | FOLD | Paper management; Ticket Issue annul |
| 301106 | Deny List not Downloaded / Downloads Daily | **NEW** | Regression — Deny/BIN list download and update |
| 300751 | ETM Customer Display — GDPR | **NEW** | Regression — passenger display GDPR compliance |
| 301245 | Promo Sub-menu incorrectly returns to FLU | FOLD | Promo Menu — basket tracker persists in sub-menus |
| 301263 | Paper Out During Basket Purchase — reload & cancel | FOLD | Paper management; Basket Mode |
| 301272 | Parkeon Key — sign-out flow | FOLD | Driver Sign Off |
| 301599 | Sign In — press C at Route Selection | FOLD | Driver Sign On — Manual, first use (full flow) |
| 301209 | ETM Freeze — smartcard removal too quick after top-up | **NEW** | Regression — no freeze on quick smartcard removal after top-up |
| 301598 | Driver Sign In too slow to load | FOLD | Regression — performance (covers sign-in load) |
| 301683 | Internal Error — going back from Adult/Child/Other + menu | **NEW** | Regression — no internal error navigating back from passenger-type menu |
| 301485 | Expired MJ with journeys remaining — top-up journey-removal receipt | FOLD | Smartcard top-up — expired journeys removed |
| (REQ) C2433854-858 | Flat Fare Tap — Apple/Google/Samsung Pay (mobile/watch) | FOLD | ABT — mobile wallet taps |
| 301597 | Route Selection — filtered results begin at first page | FOLD | Driver Sign On — Manual, first use (full flow) |
| 301564 | Shift Cash Totals — annulment totals deducted | FOLD | Driver options — duty and journey totals; annulment |
| 301258 | Ticket Print Speed — 110mm | **NEW** | Regression — performance (print speed) |
| 301723 | Product Group Toggling performance optimised | FOLD | Regression — performance (toggling) |
| 301934 & 301566 | Amending Boarding Stage — products still available | FOLD | FLU — change boarding stage manually |
| 301937 | NOT FIXED | **NEEDS GEORGE** | open defect — confirm current status before authoring |
| 301324 | Annulled Ticket Printing — map point not StageID | FOLD | Ticket Issue — annul the last issued ticket |
| 301200 & 302069 | Faulty Smartpass Receipt references previous ticket | FOLD | Smartcard — faulty card handling |
| 301210 | ABT — passback of payment card implies successful tap | FOLD | ABT — passback on second tap |
| 301541 | ABT — invalid taps displayed in back office | FOLD | ABT — invalid taps recorded in back office |
| 301563 | Driver Sign In — journey number audit in CloudFare | FOLD | Driver Sign On — Manual, first use (audit step) |
| 301715 | Driver Totals — smartcard use in passes total | FOLD | Driver options — duty and journey totals |
| 302090 | Open Payments — Deny/BIN updates while FEIG doing comms | FOLD | Regression — Deny/BIN list download and update |
| 301621 | Inspector Report — annulled smartcard top-ups not included | FOLD | Inspector — report and smartcard check |
| 301801 | Label change — "Calculate change" now "Change receipt" | FOLD | Ticket Issue — issue with a change receipt |
| 301828 | (blank title) | **NEEDS GEORGE** | title missing in old suite — needs detail |
| 301276 | Performance Degradation | **NEW** | Regression — performance under sustained use |
| TODM-312 | Expired UBMJ top-up followed by a Daylink top-up | FOLD | Smartcard top-up — successful with auto-validation |

## Summary
- **NEW dedicated Regression cases (7):** sequence-ID integrity, Deny/BIN list download+update,
  passenger-display GDPR, no-freeze-on-quick-card-removal, no-internal-error-on-menu-back,
  performance (print speed / toggling / sign-in / sustained use), and a print-speed perf check.
- **FOLD (~32):** add the defect id to the named owning case's Refs (traceability without a new case).
- **NEEDS GEORGE (2):** 301937 "NOT FIXED" (confirm status), 301828 (blank title — needs detail).
