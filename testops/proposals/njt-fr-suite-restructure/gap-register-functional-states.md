# Gap Register & Q&A — NJT Fare Register (Functional States)

**Purpose.** Every gap is a question, not a silent marker. See CLAUDE.md's "gaps trigger a Q&A loop" rule.

---

**Q1 · CONFLICT · Operational State vs Functional State mapping** — OPEN
FS002's Scope note (p.10-11) distinguishes Operational State (In Service / Out of Service / Locked-Blocked, set by back-office command) from Functional State (Initialising / Idle / Comms Locked / Low Power / Screen Saver / Out of Service, the device's own state machine) but never states the exact mapping between them - specifically whether "Comms Locked" IS the functional-state realisation of the "Locked/Blocked Operational State", or whether they are distinct. This blocks writing a confident case for "Screen Saver is only enterable from Idle" as a negative assertion, because existing case `C4098832` already asserts Screen Saver is entered directly from the "Idle - Non Operational" operational state (which may or may not be the same thing as the Idle functional state). Also relevant to the large-scale duplication finding: the three legacy "In Service / Out of Service / Locked-Blocked Operation State" case trees each replay the identical functional-state transition set, which only makes sense if the two state models are meant to be near-identical - but that isn't confirmed either.
A:
source: `knowledge/njt/specs/fs002-functional-states.md` (Scope note, "GAP" at line 17-20); existing cases `C4098832`, and the duplicated legacy trees (`C4087098`/`C4087128`/`C4087145` and siblings).

---

**Q2 · SURFACE · Target functional state on failed initialisation** — OPEN
FS002 3.1.1 (p.11) states initialisation moves to Idle only when it completes without errors AND no Driver-access-blocking condition is active, but never states what functional state the FR enters when either fails. §3.1.5 lists Out-of-Service fault *examples* but doesn't explicitly say "failed initialisation -> Out of Service." Existing cases `C4098827`-`C4098830` assert the "Idle - Non Operational" *screen* is shown for various conditions detected at init (comms lock / fault / OOS-remote / blocked-remote), but that only proves the screen, not the formal functional-state name reached. This blocks writing a case that asserts a named functional state (e.g. "enters Out of Service") on init failure without inventing behaviour.
A:
source: `knowledge/njt/specs/fs002-functional-states.md` (3.1.1, GAP at line 26-28); existing cases `C4098827`, `C4098828`, `C4098829`, `C4098830`.

---

**Q3 · VALUE · Low Power / Screen Saver inactivity timeout default and range** — OPEN
FS002 3.1.3/3.1.4 (p.11-12) give no numeric default or range for either the Low Power or Screen Saver inactivity timeout (unlike Comms Lock's explicit 0-99,999hr range). It also isn't confirmed that Screen Saver's timeout is intentionally shorter than Low Power's (implied by the required Idle -> Screen Saver -> Low Power chain, but not stated as a rule). This blocks writing boundary-value cases for either timeout, and blocks asserting a specific numeric ordering relationship between the two configured values in a case (the drafted chain case in `functional-states.cases.yaml` therefore asserts *order only*, not timing values). Note: `hmi01-fare-register-hmi.md`'s distilled screen table cites 60s (Idle->Screen Saver) and 10 min (Screen Saver->Low Power) as example figures used in several existing HMI cases (e.g. `C4087302`, `C4087304`, `C4098826`, `C4098835`) - confirm whether these are the actual configured defaults or illustrative examples from the HMI mock-ups only.
A:
source: `knowledge/njt/specs/fs002-functional-states.md` (3.1.3 GAP line 49-50, 3.1.4 GAP line 56-59); `knowledge/njt/specs/hmi01-fare-register-hmi.md` (Signed Off table, p.16-18); existing cases `C4087302`, `C4087304`, `C4098826`, `C4098835`.

---

**Q4 · SCOPE · Out of Service fault list is non-exhaustive** — OPEN
FS002 3.1.5 (p.12-13) lists three OOS fault examples (missing/corrupt software or config, unreadable mounting-tray key info, essential component failure) with the wording "examples of this are" - explicitly non-exhaustive. The suite (via `C4087176`, `C4087177`, `C4087178`, and TIBU `C4099022`) covers exactly these three named examples but no others. This isn't a case that can be drafted without inventing an unnamed fourth fault class - flagging so the suite isn't assumed complete for OOS triggers.
A:
source: `knowledge/njt/specs/fs002-functional-states.md` (3.1.5, GAP at line 80-81); existing cases `C4087176`, `C4087177`, `C4087178`, `C4099022`.

---

**Q5 · VALUE · Special-user invocation mechanism and CloudFare "force In Service" mechanism** — OPEN
Two related gaps from FS002: (a) "special user" access is referenced in both 3.1.2 (Comms Locked) and 3.1.5 (Out of Service) but the credential/action that invokes special-user mode is never defined in this section; (b) the mechanism by which CloudFare pushes an "In Service" command to recover a device from Out of Service is stated to exist but not detailed. Existing cases (`C4087160`, `C4087175`, `C4087174`) already exercise these flows using generic phrasing ("signs into the Special User Mode", "sends an In Service command from CloudFare") without naming the exact credential or CloudFare action - which is consistent with the Gherkin standard's "unknown how, not unknown what" allowance (defer mechanism to tester), so these existing cases are not flagged as defective. Logging this here per FS002's own explicit routing instruction ("Route the following to the gap register... (4) special-user invocation mechanism, (5) CloudFare 'force In Service' mechanism"), in case a future case needs the concrete mechanism (e.g. a dedicated case testing the special-user credential itself, or a Supervisor-menu case that names the exact CloudFare action).
A:
source: `knowledge/njt/specs/fs002-functional-states.md` (3.1.2 GAP line 38-39; 3.1.5 GAP line 82-83; Suite implications line 116-119); existing cases `C4087160`, `C4087175`, `C4087174`.

---
