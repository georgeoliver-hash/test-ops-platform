# The Gherkin standard

One way to write a TestRail case, across every project and device. Common cases should read
**identically** between projects; only genuinely bespoke cases differ. `standards-keeper` enforces
this; `gherkin-author` writes to it.

## Anatomy of a case

Every case has three parts: a **title**, a **tag line**, and a **Given/When/Then body**.

```
Title: <Feature> — <observable behaviour>
Tags: @project(<name|common>) @device(<POS|TVM|BV|ETMS|GV|PV|HHD>) @feature(<area>)

Given <the device/system is in this starting state>
  And <any additional precondition>
When <the operator or system performs the action under test>
Then <the observable, checkable outcome>
  And <a BOS audit event / EventLog entry, when the feature produces one>
```

## Title

- Format: `<Feature> — <observable behaviour>`. Title-cased feature, plain-language behaviour.
- Describe **what the user/system observes**, not the mechanics. Good: `Sign On — valid credentials
  reach the main menu`. Bad: `test signon function returns true`.
- One behaviour per case. If the title needs an "and", it's probably two cases.
- **Keep titles short.** State just what's tested; don't tack on the downstream outcome. Good:
  `Sign On — Supervisor sign on`. Too long: `Sign On — Supervisor signs on with valid credentials
  and reaches the Supervisor menu`. Add a variant in brackets only when it distinguishes the case,
  e.g. `Sign On — Supervisor sign on (smartcard)`.

## Tags (the convergence mechanism)

Three tags, mirroring the `automation-tests` pytest markers so the two repos line up:

| Tag | Values | Meaning |
|-----|--------|---------|
| `@project` | `common` or a project name (`translink`, `nta`, …) | `common` = identical across projects; a name = bespoke to that project. |
| `@device` | `POS`, `TVM`, `BV`, `ETMS`, `GV`, `PV`, `HHD` | The device type(s) the case applies to. |
| `@feature` | `auth`, `transactions`, `printing`, `provisioning`, `status`, `sync`, … | High-level area, used to group/select. |
| `@mode` | `all` or an operating mode (`NIR`, `Ulsterbus`, `Metro`, …) | For devices with operating modes. `all` = behaves identically in every mode (the default); a mode = the case is specific to that mode's behaviour. |

Optional extra tags: `@destructive` (puts the device in a manual-recovery state — mark it, like the
framework does), `@bos` (asserts a back-office audit event), `@regression` (pins a previously-fixed
defect — see below).

### Pinning past defects (regression coverage)

Every fixed bug should be caught by a case so it can't silently come back. Two ways, preferred first:
- **Fold a step into the functional case** that owns that behaviour — add the assertion/flow that
  would catch the regression. No separate case needed.
- **Write a dedicated `@regression` case** only when the scenario doesn't belong to an existing case.

Either way, **link the defect via the Refs field** (e.g. `TIBU-28530`) — never just in the title —
so coverage is queryable. Organise by **behaviour/feature**, not by the release the bug was fixed in.

### Operating modes (the convergence mechanism, one level down)

Some devices run in several **operating modes** — e.g. Translink POS runs as **NIR**, **Ulsterbus**,
and **Metro**. Most flows are identical across modes; only a few (e.g. **top-up**) differ. Model
this the same way we model common-vs-bespoke across projects:

- **Default to `@mode(all)`.** Write the shared case **once**. Execute it against each mode using
  TestRail **Run Configurations** (NIR / Ulsterbus / Metro) — one case, three configs, no copies.
- **Only split when the steps genuinely differ.** Then write a `@mode(<NIR|Ulsterbus|Metro>)` case
  for that mode and keep it in the feature's mode-specific subsection. Don't fork a whole flow when
  one screen differs — split at the case that differs, not the section above it.
- A `@mode(all)` case must read identically regardless of mode; if you're tempted to write "in NIR
  mode, …" inside an `@mode(all)` case, it isn't `all` — tag the mode.

Example — top-up, where Sign On is shared but top-up varies:

```
Title: Sign On — valid credentials reach the main menu
Tags: @project(translink) @device(POS) @mode(all) @feature(auth)
# one case, run under NIR + Ulsterbus + Metro configurations

Title: Top-up — Metro smartcard top-up adds value and prints a receipt
Tags: @project(translink) @device(POS) @mode(Metro) @feature(transactions)
# a Metro-specific case, only because the Metro top-up steps differ
```

## The body — rules

- **Given** sets state only. No actions, no assertions. Always reset to a known state ("Given the
  POS is signed off") so prior session state can't leak.
- **When** is the single action under test. One `When` per case; use `And` sparingly for an
  inseparable two-step action.
- **Then** is observable and checkable — a screen label, a dialog, a printed receipt, an audit
  event. Never "Then it works".
- **BOS audit**: if the feature emits a back-office event, assert it explicitly as a `Then ... And`,
  naming the event. Don't invent event names — confirm them (`knowledge/`, the `bos-auditor`/
  EventLog assertions in `automation-tests`).
- **No hard-coded secrets/IPs/PINs in the case text.** Use named test data ("the seeded operator
  credentials"), not `9999`.
- Plain language a manual tester could execute and an automated test could mirror 1:1.

## How a case maps to TestRail (and 3 rules)

In this project's case template, a case is made of: a **Preface** (objective), **Preconditions**, a
**Steps** table (When/Then rows), and an **Expected result**. The standard maps onto them like this:

| Standard part | TestRail field | Rule |
|---|---|---|
| Objective | Preface | A sentence: **"This test is to confirm the user can …"** — not the title repeated. |
| `Given/And` | Preconditions | The starting state ("given this, and this is happening"). State only. |
| `When/And` → `Then/And` | Steps table | **Always at least one When→Then step.** Even a static check gets a `When the operator views …`. **One clause per line** — never join two independent outcomes with "and" in a single Then (write `Then signed on` / `And menu displayed`, not `Then signed on and menu displayed`). Use multiple steps for multiple actions. |
| (summary) | Expected result | A short **prose** sentence or two of what we expect to happen — not a copy of the `Then` lines. |

**Tags are NOT written into the case.** `@project / @device / @mode / @feature` are realised by
TestRail natively — the project, the device-type field, the run **Configurations**, and the
**section**. Tags live only in the repo (this standard, the mapping docs) for our reasoning.

## Gherkin / BDD best practices (researched — Cucumber)

Aligns the suite with the canonical Cucumber/BDD guidance (cucumber.io):

- **Declarative, not imperative.** Describe the *behaviour/intent*, not key-by-key mechanics. Test:
  *"Would this wording need to change if the implementation changed?"* If yes, raise the altitude
  ("the operator signs on", not "types email, presses Submit"). **Exception:** where a specific key
  or screen *is* the behaviour under test on this hardware POS (e.g. the 'C'-key field behaviour),
  keep it — that's the point of the case.
- **Keep it concise — 3–5 steps.** A scenario should read as one behaviour in a handful of steps.
  Past ~6 it's usually two cases.
- **One When.** Given = context, When = the single event, Then = the observable outcome. And/But
  continue same-type steps (each clause on its own line — never a compound `Then … and …`).
  - *What "compound" means:* a single `Then` that bundles **two distinct outcomes** with inline
    "and" — e.g. `Then the breakdown is displayed and printed` → split into `Then … is displayed` /
    `And … is printed`. This does **not** apply to an "and" inside one observable assertion that
    simply lists attributes — e.g. `Then the screen matches the approved design (layout, wording,
    labels and colours)` or `Then up and down arrows are available` are single checks and stay on
    one line. Heuristic: if the words after "and" start a *new predicate* (verb), split; if they
    only extend a noun list belonging to the same check, leave it. `tools/audit_suite.py` enforces
    exactly this distinction.
- **Then asserts observable outputs only** — a screen, a printout, a recorded audit event in
  CloudFare — not internal/implementation state.
- **Superseded 2026-07-24 — see below.** ~~Data variations are an Examples list, not extra cases~~:
  this used to say list passenger types/payment methods/products as one "Data variations:" line
  rather than multiply cases. George overturned this: **every genuinely distinct variant now gets its
  own separate case.** A named list inside one case reads as covered but only ever executes one
  example — a card/product/entitlement type can fail independently of its siblings, so each needs its
  own trackable pass/fail. See `test-practices.md` "Structure by flow/risk" for the full rule and
  rationale. TestRail **Configurations** still cover the *operating-mode* dimension (NIR/Ulsterbus/
  Metro, Glider/Rail) — that part is unchanged; this only affects data-value variants (card schemes,
  smartcard/entitlement types, payment methods, ticket products) that were previously compressed into
  one case's variation line.
- **Business-readable.** Plain language a manual tester executes and an automated test mirrors 1:1.

## Concrete grounding — enough to actually run the case

A declarative case still has to be **executable**. If running the case depends on specifics — a
**route, operator/role, boarding & alighting stop, product, zone, fare, or config flag** — the case
must carry a **concrete worked example** so a tester (or an automated script) has real values to use,
not a blank they must guess. This is the lesson from the ABT capping cases: "make two Metro-zone
taps" is unrunnable; "*e.g. 10A (IN) Casement Park → City Hall, £2.30*" is.

Rules:
- Put the worked example in the **Preconditions** (state), and reference what it demonstrates in the
  **Preface**. Keep the **title/When/Then declarative** (behaviour, not the specific data).
- **(Updated 2026-07-24)** One case = one behaviour + **one** concrete worked example. Where the
  behaviour genuinely has other distinct values/variants worth testing (a different fare band, a
  different card scheme), each gets its **own separate case** with its own worked example — not a
  trailing "Data variations:" list on a single case (that pattern is retired, see the "Terse, not
  bloated" and "Structure by flow/risk" sections). A worked example still keeps the case runnable and
  concrete; it just doesn't try to carry multiple variants at once anymore.
- **Ground the example in a source**, not invention — cite the requirement/spec it comes from
  (`FBD-#####`, a fares export, `knowledge/translink/specs/…`) or a seeded test-data set.
- **No gap-filling — this is the cardinal rule.** If a value, screen name, action, or capability is
  **not** in the source requirements, you may **not** invent a plausible one to make the case read
  better or feel complete. Write an explicit marker at that exact spot and stop:
  - `**GAP** — <what is unknown> — not in requirements; confirm before running` for something absent.
  - `**UNCONFIRMED** — <feature> is specified (cite CR/FBD) but not verified live` for something that
    is written in a spec but whose real-world existence is unproven (a CR being written ≠ it shipped).
  A visible gap is correct and useful; fluent invented functionality is a defect that looks fine and
  isn't. When in doubt, mark it, don't fill it.
- **Check the surface can actually do the action.** Before writing an action, confirm the *device or
  portal* in the case can perform it per spec — do not move a capability across surfaces (e.g. a
  tap-off on a tap-on-only device; a "cancel a journey" button on a portal that has no such function;
  a barcode scan on a device with no scanner; a smartcard issue on a device that can't issue). Cross-
  surface invention is the most damaging gap-fill because it reads plausibly. If unsure which surface
  owns the action, mark it `**GAP**`.
- **Unknown *how* (not unknown *what*) → assumed-competence step, not invention and not a block.** When
  the OUTCOME is real but the exact screen/steps/role to perform it aren't confirmed (an upcoming/
  proposed feature like CR122, or a mechanism the spec doesn't detail), do NOT invent a screen name or
  steps, and do NOT bury the case under a blocking marker that makes it un-runnable. Instead name the
  outcome and **defer the mechanism to the tester**:
  - `**AND** you change the journey's alighting stop` — not "open the Update Stop list and select…".
  - `**GIVEN** you know how to change a journey's alighting stop` when it's a precondition skill.
  - Add a short parenthetical for honesty: `(ABT portal alighting-stop correction, CR122 — upcoming;
    confirm the exact screen/role on the live system)`.
  This keeps the case runnable by someone who knows the system, avoids asserting an actor/screen we
  can't confirm (it may be an admin, not the operator), and stays transparent that the *how* is to be
  confirmed. Reserve the full `**UNCONFIRMED**`/`**GAP**` block for when the **behaviour/outcome itself**
  is unknown — not merely the how-to.
- **Unknown *configured value* (not unknown behaviour) → assumed-knowledge precondition, not a block.**
  A lot of thresholds/windows/limits are back-end configurable and change over time — the lockout
  attempt count, a duplicate-tap/passback window, a fare/cap amount, a correction limit. The
  *behaviour* (there is a passback window; it locks after N attempts) is real and known; only the
  *current number* isn't pinned in the case. Don't hard-code a guessed figure, and don't block the
  case on an `**UNCONFIRMED**` marker either — both are wrong for the same reason (the exact value
  isn't the point; the tester checks it live). Instead add an assumed-knowledge precondition:
  - `**GIVEN** the tester knows the currently configured passback window` (then reference "the
    configured window" in When/Then, never a literal number, unless the case is specifically citing
    a documented example like `docs/gherkin-standard.md`'s worked-example convention above).
  - This is the same pattern as the fare/cap reframe already used in the ABT capping suite: *"example
    per current ABT pricing config; verify the charge matches the configured rule"* — generalise it to
    any configurable value, not just fares.
  Reserve `**GAP**`/`**UNCONFIRMED**` for when the *existence* of the behaviour itself is in doubt, not
  for "I don't know today's number for a setting everyone agrees exists."
- Applies to preface/preconditions/steps: enough context that someone unfamiliar with the exact
  route or operator could still execute it.
- **`MODE-ALL` cases must NOT hard-code a single operator's route — this is a hard rule (George,
  2026-08-03).** A case tagged `MODE-ALL` runs, unchanged, under every operating-mode Configuration
  (e.g. both Metro and Ulsterbus for ETM). A concrete worked example naming one operator's route (`a
  Driver is signed on to Ulsterbus route 72b`) is a **lie under every other Configuration it also
  runs in** — a Metro tester executing that case is handed a nonsensical precondition and correctly
  marks it Invalid. This is not a hypothetical: a live-run audit of `ETM - OS v8.0.6356` (plan 52401,
  2026-08-03) found 62 of 183 `MODE-ALL` ETM cases doing exactly this, driving the majority of that
  run's Invalid-Test marks. Fix: state the route/operator generically —
  `**GIVEN** a Driver is signed on to a valid route (IN) at the FLU screen` — never a named operator
  or route number. This does not weaken "concrete grounding" above: for a `MODE-ALL` case the specific
  route number was never actually load-bearing (nothing in the steps/expected references it), so
  dropping it loses no real coverage. **Contrast with `MODE-<OPERATOR>-ONLY` cases**, which SHOULD
  keep a concrete, operator-specific worked example (e.g. `Ulsterbus route 72b (IN)`) exactly as the
  "concrete grounding" rule above requires, grounded via `knowledge/ABT/ABT_FARE_REFERENCE.md` (the
  derived, committed reference built from the ABT Testing Crib Sheet CSVs — confirmed routes, zones,
  and reference fares) — cite the specific route/zone section from that file rather than repeating a
  raw number with no traceable source. When authoring any new shared/multi-operator case, decide
  `MODE-ALL` vs `MODE-<OPERATOR>-ONLY` **first**, then write the precondition to match: generic for
  the former, concrete-and-cited for the latter.

Example (Ulsterbus reference-fare cap):
```
Preface: This test is to confirm the daily reference-fare cap is reached within a fare band.
Given the reference cap governs the day (ref.60 = £7.20, single £4.50), zonal capping off
  And example journeys: 72b (IN) Moygashel Busby Shop → Armagh Bus Centre, ~09:00 then ~12:00
When the two same-ref taps settle at EndOfDay
Then the first tap is charged £4.50
  And the second is charged £2.70 to complete the £7.20 cap
```
Each other fare band (ref.10 £3.80 / ref.20 £4.60 / ref.55 £6.40 / ref.61 £8.20) is its **own case**
with the same shape and its own worked example — not a trailing variations line on this one (per the
2026-07-24 rule above).

(Source: FBD-100662 Ulsterbus Tap-On-Only; the UB-TOO tracker.)

## Terse, not bloated — trust the tester (George, 2026-07-21 — a hard rule)

The body of a case is what a tester reads while executing it. It is **not** a place for provenance,
sourcing, dates, or explanatory prose. Two failure modes, both banned:

- **Citations/confirmations baked into Given/When/Then text.** Wrong:
  `AND the portal alighting-stop adjustment (CR122) is confirmed live in the Operator Portal test
  environment — George (live-system confirmation), 2026-07-21 (mechanism per FBD-100662 §5.6, paras
  691, 693, 271)`. Right: `AND CR122 alighting-stop correction is available`. Every citation, date,
  "confirmed by X", and spec paragraph reference belongs in the **Refs field** / the proposal's
  `citations` metadata / `gap-register.md` — never in the text a tester executes. If you're tempted to
  write "— George, 2026-07-21" or "per FBD-#####" inside a Given/When/Then line, stop and move it out.
- **Full sentences where a short tag would do.** Wrong: `AND the reference cap governs the day (ref.60
  = £7.20, single £4.50)`. Right: `AND ref.60 cap £7.20, single £4.50`. Wrong: `AND the tester has
  confirmed the currently configured value of the passback window before proceeding`. Right: `AND
  tester knows the current passback window`. Have faith the person running the test has baseline
  competence — a value, a claim name, a config flag doesn't need a sentence explaining what it is or
  why it's there, just the fact itself, tersely.

This does **not** relax the "concrete grounding" or "no gap-filling" rules above — a worked example
still needs real values and still must trace to a source. It only changes **where** the sourcing lives
(metadata, not body) and **how much prose** wraps the fact (a tag/fragment, not a sentence). Applies to
every precondition, step, and the expected-result summary, in every suite.

## Executable — walk the tester through it (the most important rule)

A case must read as a **procedure a tester can follow start to finish**, not an abstract statement
*about* the behaviour. If a tester opens the case and can't tell **what to prepare, what to do, in
what order, and where to look for the result**, it fails this rule — even if it's "grounded".

- **One scenario, aligned.** The **title**, **objective**, **preconditions** and **steps** must all
  describe the *same* concrete scenario. If the title says one thing and the steps exercise another,
  fix it.
- **Title: concise and accurate to the test.** `<Feature> — <the specific behaviour this case
  proves>`, short and plain. If the current title is vague, generic, or drifts from what the steps
  actually do, **tighten it** — on an in-place update, rename by keeping the old title as the `match:`
  key and giving the improved `title:` (so it renames the same case, never duplicates).
- **GIVEN = the full setup you can actually prepare.** Name the card/account/device state, the config
  that matters (e.g. "the duplicate window is 15 minutes"), where you're signed in to verify, and any
  journeys/state the scenario assumes already exist. Don't start mid-air.
- **Each WHEN is a real, ordered action.** "tap the card at Casement Park (10A IN) at 09:00", "make a
  same-stage retail transaction", "run the EndOfDay settlement", "open the card's Journey History in
  the Operator Portal" — concrete enough to perform without guessing. Multiple actions = multiple
  ordered WHEN/AND lines, in the order you do them.
- **Each THEN says what you observe and WHERE.** Name the screen/portal/field and the expected value
  ("in Journey History the 09:06 tap shows £0.00, marked Duplicate"), not "then it's a duplicate".
- **No gap between setup and check.** Spell out how you reach the state and how you read the result —
  don't collapse a multi-step procedure into "GIVEN all this happened, THEN outcome".
- **This overrides terse "declarative" phrasing for manual cases.** Stay behaviour-focused (not
  key-by-key UI unless the key *is* the test), but always give enough operational detail to execute
  unambiguously. A manual tester and an automated script should both be able to follow it 1:1.
- **Group into a few clear steps (ideally 1–3), not one long chain and not a step per micro-action.**
  Each step is a coherent *action-and-check* (a `WHEN`+`AND` action group with its `THEN`+`AND`
  observations) — e.g. Step 1 "make the day's taps → each is recorded", Step 2 "run settlement and
  open Journey History → the duplicates show £0.00". This maps to TestRail's steps table.
- **Cap the ANDs per step — a wall of ANDs is a smell.** If a single step's `THEN` needs **more than
  about 3 `AND` lines**, split it into another step. A long list of observations under one `WHEN`
  almost always means two actions were collapsed — break them out so each step has one action and a
  short, readable set of checks. Prefer **2–3 tight steps over 1 step with 5–6 ANDs.**

> Rule of thumb: read the case as if it's the first time you've seen this device. Could you run it
> and know whether it passed? If not, it isn't done.

## Worked example — Sign On (common across projects)

This is the canonical reference. It mirrors `automation-tests`
`projects/translink/tests/signon/test_operator_signon.py`.

```
Title: Sign On — screen shows the ID and PIN labels
Tags: @project(common) @device(POS) @feature(auth)

Given the POS is signed off and showing the sign-on screen
Then the screen displays the "ID" label
  And the screen displays the "PIN" label
```

```
Title: Sign On — valid credentials emit a state.changed audit event
Tags: @project(common) @device(POS) @feature(auth) @bos

Given the POS is signed off and showing the sign-on screen
  And a valid operator's seeded credentials are available
When the operator signs on with the seeded ID and PIN
Then the main menu is displayed
  And a "state.changed" entry is written to the device EventLog within 15 seconds
```

```
Title: Sign On — invalid credentials show the failure dialog
Tags: @project(common) @device(POS) @feature(auth) @destructive

Given the POS is signed off and showing the sign-on screen
When the operator signs on with an unrecognised ID and PIN
Then the "Sign On Failed" dialog is displayed
  And the operator is not signed on
```

## Bespoke vs common — quick test

Ask: *would this case read the same for a different project's POS?*
- **Yes** → tag `@project(common)`. Keep the wording identical to the shared version.
- **No, it depends on project-specific data/flows** → tag `@project(<name>)` and keep the bespoke
  detail in the body, not smuggled into a "common" case.

## Checklist (what `standards-keeper` looks for)

- [ ] Title is `<Feature> — <observable behaviour>`, single behaviour.
- [ ] Exactly the three required tags, valid values; `@destructive`/`@bos` where relevant.
- [ ] `Given` = state only; one `When`; `Then` is observable.
- [ ] BOS/EventLog events named, not invented.
- [ ] No hard-coded secrets/IPs/PINs.
- [ ] `@project(common)` cases match the shared wording verbatim.
