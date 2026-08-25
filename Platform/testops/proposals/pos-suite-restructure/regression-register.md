# POS Regression Defects — register

Defect ids are JIRA **TIBU-#####** keys. Per the consolidation principle (one test per risk, fold
bug-fixes into the owning behaviour), each defect is either **FOLD** (covered by an existing
functional case — add the defect id to that case's Refs) or **NEW** (no natural home → a dedicated
case).

| Defect | Title (JIRA) | Disposition | Owning / new case |
|---|---|---|---|
| TIBU-29756 | Cloudfare > Remote Reboot > POS (QA PASSED, build 1.0.602.20592, Ready for Release) | **NEW** | Comms — a CloudFare Remote Reboot command reboots the POS (`C4105016`, Non-Functional / Comms (CloudFare)) — no existing case covers a back-office-initiated reboot; the only reboot coverage found (`C4099956` Technician - Soft Reboot; `C4100072`/`C4100073` screen validation) is the local technician-menu flow, a different trigger/actor, so folding into it would misrepresent the scenario. |
