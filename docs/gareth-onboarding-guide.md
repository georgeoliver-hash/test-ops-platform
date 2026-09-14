# Test-Ops Console — step-by-step guide for a new user (Gareth)

This walks through onboarding a brand-new suite end to end, using the Test-Ops Console
web UI — the same flow George dry-ran on NJT. Follow it in order; don't skip steps even
if a button looks clickable out of sequence.

**Before you start:** George needs to add one row for your project/device to the console's
database (there's no self-serve "add a new target" button yet) — confirm with him that this
is done before step 3.

---

## Part 1 — One-time machine setup

This is per-machine, one-off. Skip anything you've already done.

1. **Install Claude Code** and log in (`claude` on the command line should work and be
   authenticated). Several steps in this tool run Claude Code under the hood — without it,
   those steps fail.
2. **Clone all three repos as siblings** — same parent folder, not nested inside each other:
   ```
   SomeFolder/
     test-ops-platform/
     system-test-ops/
     test-automation-sit/
   ```
   This exact layout matters — the console looks for the other two repos as siblings of
   itself on disk.
3. **Set up each repo's Python environment** (in `system-test-ops` and `test-ops-platform`):
   ```
   cd system-test-ops
   python -m venv .venv
   .venv\Scripts\python.exe -m pip install -e ".[dev]"
   ```
   Repeat for `test-ops-platform`. (`test-automation-sit` only matters once you reach Part 5.)
4. **Your own TestRail credentials.** In `system-test-ops/.env` (copy `.env.example` if it's
   not there yet), set:
   ```
   TESTRAIL_URL=...
   TESTRAIL_USER=...
   TESTRAIL_API_KEY=...
   ```
   Use **your own** TestRail account/API key, not George's — pushes get attributed to
   whoever's key is configured, so this is how the audit trail says "Gareth" and not "George."
   Ask George or IT if you don't have a TestRail API key yet.
5. Leave `TESTRAIL_WRITE_SUITE_ID` unset for now — a later step sets it once the target
   suite exists.

---

## Part 2 — Start the console

From `test-ops-platform`:
```
cd test-ops-platform
.venv\Scripts\python.exe -m uvicorn Platform.webapp.app:app --host 127.0.0.1 --port 8791
```
Leave that window open — it's the server. Open **http://127.0.0.1:8791** in your browser.

You'll see "George Oliver" at the bottom of the page — that's a known cosmetic issue, not a
bug on your end. It doesn't affect your data; everything you do is stored locally on your own
machine, separate from George's.

---

## Part 3 — Readiness check

1. Click **Start**. This runs a readiness check (`doctor`) against your setup.
2. If anything shows as **NEEDS_YOU**, it'll tell you exactly what's missing (usually a
   credential or an unset env var) — fix it and re-run Start before continuing.
3. Don't proceed past this until Start comes back clean.

---

## Part 4 — Target your suite

1. Find your project/device in the target switcher (this is the row George pre-added for
   you).
2. If it shows an **"Approve this target"** action, click it and confirm — this is a real
   sign-off, not cosmetic. Nothing that writes to TestRail is allowed to run until the
   target is approved.
3. Note whether it's marked a **fresh build** (no old suite — you're building purely from
   documents, like NJT) or has an **old suite** listed (you're rebuilding/migrating an
   existing one). This changes which steps later pipelines skip.

---

## Part 5 — Ingest the docs

1. Upload your project's requirement/design documents via the docs upload area.
2. Open the **ingest-docs** pipeline and check the `docs_path` field is pointing at where
   you just uploaded to (it should default correctly).
3. Click **Run**. Watch the step list:
   - `sync_check` (human) — confirms the docs are in place; click **Continue**.
   - `convert` (cli) — converts raw docs to text.
   - `distil` (agent) — writes grounded, cited notes to `knowledge/<project>/specs/*.md`.
     This can take a while — it's reading full documents.
   - `cross_examine` (agent) — flags gaps between the docs and what's testable.
   - `commit_pr` (human) — **stop and actually read the diff** it's proposing to commit
     before clicking Continue. This step does a real `git commit` in `system-test-ops`.
4. If `cross_examine` surfaces gaps (marked `**GAP**`/`**UNCONFIRMED**`), those need answers
   before the suite you build next will be fully grounded — don't skip past them silently.

---

## Part 6 — Build the suite (onboard-suite)

1. Open **onboard-suite**, confirm project/device, click **Run**.
2. Read the **preconditions prompt carefully** before confirming — it's asking you to
   confirm you actually have what's needed (docs, UX flows, defect history). If you're
   missing something, say so rather than guessing.
3. If your target is a **fresh build**, you'll notice `discover_fields`, `audit_old_suite`,
   and `audit_run_history` are skipped automatically (there's no old suite to sample from) —
   that's expected, not a failure.
4. `cross_tab` / `confirm_scope` / `write_structure` — these are agent + human steps proving
   out the suite's shape before any case gets written. Read what's proposed; this is your
   chance to correct scope before authoring starts.
5. `author_area` — runs once per functional area found in the ingested specs, drafting
   `.cases.yaml` for each. You'll see one step per area in the list.
6. `push_area` — **this is a real TestRail write.** Each area gets its own
   **"Approve & Push"** button. It will refuse to proceed if:
   - your target isn't approved (go back to Part 4), or
   - the same area's cases aren't clean per the conformance audit.
   Review the drafted cases before clicking Approve & Push — this is not reversible in the
   same casual way a draft is.
7. `definition_of_done` — re-runs the audit against the new suite; must come back clean.
8. `human_cleanup` — manual TestRail UI tidy-up (bin any `ZZ_DELETE_*` placeholder sections,
   set up Run Configurations). This step just tells you what to go do in TestRail directly.

---

## Part 7 — Hand off to automation (export + write-automation)

1. Run **export-automation** — produces a backlog of which pushed cases are flagged
   automatable.
2. Run **write-automation**. The first step is a **human** step asking you to confirm real
   device facts (transport, IP/serial, connection details for whatever rig will actually run
   these tests) — **do not let anyone invent these**; if you don't know them yet, that's the
   point of the step, answer honestly rather than guessing.
3. It then writes `.robot` test files into `test-automation-sit/projects/<project>/`.
4. The final step is a **human** gate before `git commit && git push` to that repo's remote —
   review the actual files before approving. Nothing pushes to that repo without you
   explicitly confirming.

---

## If something goes wrong

- Server won't start / port already in use: someone else (or a previous run of yours) still
  has it open — close that window/process first.
- A step fails with a subprocess error: check the raw output shown for that step first —
  usually a missing credential or an unset `.env` value.
- Anything that looks like it's asking you to invent a fact you don't actually know (a device
  IP, a screen behaviour not in the docs) — stop and ask, don't guess. That's a deliberate gap
  the tool is surfacing, not something it expects you to fill in confidently.
- Stuck: message George with the pipeline name, the step id it stopped on, and whatever
  error text is shown.
