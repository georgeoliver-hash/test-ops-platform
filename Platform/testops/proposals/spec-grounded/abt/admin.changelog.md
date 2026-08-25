# ABT admin/access/staff/settings/ticket-editor — spec-grounding changelog

Batch date: 2026-07-17. **Status (2026-07-21): partially pushed live 2026-07-17 with a bug — every
step row came out blank (`content`/`expected` both `""`) because this file's steps used the
`{"when","then"}` shorthand while `tools/apply_rewrite.py`/TestRail's `custom_steps_seperated`
expected `{"content","expected"}`. Title/preface/preconditions/expected pushed correctly; only the
step rows were blank. Fully corrected and properly re-pushed 2026-07-21 (all 51 cases in this file)
after fixing `tools/apply_rewrite.py` to normalise both schemas and refuse any blank step outright.
See `proposals/coherence-audit/fixes/abt-blank-steps-fix.changelog.md` for the full writeup.**
Source: `suite_ABT.json`
(section export of the ABT suite). 51 cases across 9 sections re-grounded strictly against
the real specs; no invented behaviour (see `admin.gaps.md` for every unknown).

## Governing specs used

| Spec | Doc read | Covers |
|------|----------|--------|
| FBD-100342 | User Claims Specification **V3.00** (docx) | KeyCloak/AD, realm **Translink**, clients `operator-react-client` (ABT Operator Portal) and `CloudFareWeb`; the full claim catalogue; user groups |
| FBD-100363 | Translink Ticket Editor Specification **V1.00** (docx) | Ticket Editor create/edit/copy, elements, device types, barcodes, payment-card fields, publish, Product Editor assignment |
| FBD-100306 | Merit Web Specification **V3.00** (docx) | Closest spec for the Administration/Merit editors — **not** in the named grounding set; only partial coverage found |
| FBD-100383 | TFTS Operator Hierarchy v4.00 (**PDF**) | **Not machine-readable** with current tooling (no pdfminer/PyPDF2). Hierarchy facts cited from FBD-100342 (paras 206-212, 251-252) instead |
| FBD-100266 | Device Heartbeat Functionality & Reporting V3.00 (docx) | Alerts / Comms Monitor only — does **not** cover the Settings sub-pages in this batch |

## Action tally (per rewrite `action`)

| Action | Count | Meaning |
|--------|-------|---------|
| REWRITE | 6 | Behaviour grounded; title/preface/steps fixed for conformance |
| REGROUND | 3 | Wrong label/role/screen/surface corrected against spec |
| SPLIT | 4 | Case bundled >1 behaviour; split recommended (grounded) |
| GAP | 3 | Feature/label absent from all provided specs; marked GAP |
| UNCONFIRMED | 35 | Access role grounded where possible; behaviour not in the named specs |
| **Total** | **51** | |

Grounded against named specs: **13** (REWRITE + REGROUND + SPLIT).
Grounded-as-absent (GAP): **3**. Unconfirmed: **35**.

## Cross-cutting corrections applied

1. **"user role" -> composite claims / user groups.** The system has no free-form roles.
   KeyCloak (SaaS) / ADFS+AD (hosted) assign **composite claims** to **user groups**; users
   inherit them (FBD-100342 paras 129-132, 277). A first-time user with **no** claims cannot
   access the portal at all (para 131). Applied to 4102856/4102857 and to the access preconds
   on Staff Manager, Settings, Drawing Tool, Labeling, Ticket Editor, Administrator Settings.
2. **Portal / client names.** ABT Operator Portal = `operator-react-client`; CloudFare web =
   `CloudFareWeb`; realm = **Translink** (paras 124, 229, 279). Sign-on is by **Active
   Directory credentials**, not a local username/password (para 125, 203).
3. **Ticket "layout" -> "template".** FBD-100363 uses "template" throughout; renamed.
4. **Compound THENs split.** Every `Then ... and <new predicate>` broken to one predicate per
   line; multi-action `When`s split into ordered steps (per `gherkin-standard.md`).
5. **Access preconds grounded to a named claim** wherever the module claim exists: Staff
   Manager (para 185), Topology/Drawing Tool/Labeling (para 174), System Configuration/Settings
   (para 198), Admin settings (paras 146-148), Ticket Editor (para 177).

## Per-section notes

### Administration (7) — all UNCONFIRMED
"Merit" desktop editors. Governed by the **Merit** product, outside the named grounding set.
Closest spec FBD-100306 (Merit Web V3.00) only partially confirms: Timebands (paras 267-268),
Class/Route grouping (paras 255/263), Location Restrictions (para 328). **Not found** in any
provided spec: Date Editor period/roll-over/start-of-week (4103093), Staff Editor (4103095),
Route Revenue generation-factor/BRT/journey-allocation (4103099). Raised as a possible mis-file
+ missing-spec question.

### Sign On & Access (6)
- 4102856 **SPLIT** — sign-on separated from menu navigation (compound THEN).
- 4102857 **REWRITE** — regrounded to composite-claim access model.
- 4102858 **REWRITE** — standardised sign-off, portal named.
- 4102960 **REGROUND** — CloudFare sign-on is AD credentials; Dashboard is a real claim (para 191).
- 4102961 **GAP** — "Sign on with a Google account": no Google/OAuth path in FBD-100342.
- 4102962 **REWRITE** — sign-off standardised; back-button variant demoted to UNCONFIRMED.

### Sign On & Account (4) — all UNCONFIRMED
Passenger Web Portal. **No** Passenger Portal spec exists in the named set or the library
(searched Passenger Web / Passenger Portal / Anonymous). Failure-case case (4102928) split into
three ordered steps. All flagged for a governing-spec question.

### Settings (8)
Access grounded to the **System Configuration** claim (para 198). Sub-pages (Event Codes,
Operating Units, Scheduled Tasks purges, System Settings/VAT/toggles, Notifications, External
Interface, Scheduled Adherence) not enumerated in provided specs -> UNCONFIRMED. 4102965 marked
**SPLIT** (navigation smell). Multi-action pages split into ordered steps.

### Administrator Settings (5) — all UNCONFIRMED
Admin tab access grounded to **AdminFullAccess/AdminReadAccess** (+EPurseReadAccess) claims
(paras 146-148); the capping/debt-recovery/e-Purse **setting semantics** belong to specs not in
the named set. Preconditions fixed (e.g. 4102880 "wants to configure" -> signed-in admin state).

### Staff Manager (4)
Module access grounded to the **Staff Manager** claim (para 185). Function detail not specified
anywhere in the named set. 4103044 **SPLIT** (add/modify/disable are 3 behaviours). Note the
CloudFare Staff Manager is distinct from the Merit Staff Editor (4103095).

### Ticket Editor (8) — best-grounded section
- 4103080 **SPLIT** — Create/Edit/Copy are 3 distinct entry options (para 254-257).
- 4103081 **REWRITE** — named the real elements (para 362-366); dynamic fields show green (191).
- 4103082 **REGROUND** — device type fixed at creation; separate template per device; reuse =
  copy + change device type (para 178-180, 338). Not "one layout for many devices".
- 4103083 **GAP** — "change ticket" not in FBD-100363.
- 4103084 **REGROUND** — assigning a template to a product is a **Product Editor** function,
  not Ticket Editor (para 391-393). Recommend re-filing under Products.
- 4103085 **GAP** — no "group a set of ticket layouts" feature exists.
- 4103086 **REWRITE** — barcode placement grounded; preview is illustrative only (para 262-264).
- 4103087 **REWRITE** — payment-card fields mapped 1:1 to REQ-1750.16/17/18/20/21.

### Drawing Tool (5) — all UNCONFIRMED
Access grounded to the **Topology** claim (para 174). Drawing-Tool functions (map points, zones,
positional points, CSV import/export, search) not in the named set. 4102982 split into 4 steps.

### Labeling & Publishing (4) — all UNCONFIRMED
Access grounded to the **Topology** claim (para 174). FBD-100363 confirms only that ticket
templates publish at a hierarchy level and cascade to sub-levels (para 251-252) — not a general
topology-label / future-transition-date / delete-label workflow. 4103012 split (publish vs
transition).

## Encoding note
Source titles contained mojibake em-dashes (`â€”`). Rewrites use proper UTF-8
`--`/em-dash via the editor tools (never PowerShell Set-Content), per the CLAUDE.md encoding rule.
