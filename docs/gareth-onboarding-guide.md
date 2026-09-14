# Test-Ops Console — complete setup + first run guide (for Gareth)

Follow every step in order. Don't skip ahead even if something looks clickable early —
later steps depend on earlier ones actually being done.

---

## Part 0 — Before you start

Ask George for:
- **GitHub access** to these three repos (they're private, under his personal GitHub
  account — you can't clone them without being added as a collaborator first):
  - `https://github.com/georgeoliver-hash/test-ops-platform`
  - `https://github.com/georgeoliver-hash/system-test-ops`
  - `https://github.com/georgeoliver-hash/test-automation-sit`
- **Your own TestRail account** with an API key (not George's — see Part 4).
- Confirmation of which project/device target you'll actually be onboarding (so you know
  what to type in Part 6).

---

## Part 1 — Install Git and Claude Code

1. If you don't already have Git installed, install it (search "Git for Windows" if unsure).
2. Install **Claude Code** and log in — several steps in this tool run Claude Code behind
   the scenes, so it needs to be installed and signed in on your machine before anything else
   will work. Run `claude` in a terminal to confirm it opens/works.
3. Install **Python 3.11+** if you don't have it.

---

## Part 2 — Clone the three repos, in the right place

This exact folder layout matters — the tool looks for the other two repos as siblings
(next to each other, same parent folder) on disk.

1. Open a terminal (PowerShell or Git Bash) and pick or create a folder to work in, e.g.:
   ```
   cd C:\Users\<you>\Documents\GitHub
   ```
   (Create the `GitHub` folder first if it doesn't exist: `mkdir GitHub` then `cd GitHub`.)
2. Clone all three repos into that same folder, one after another:
   ```
   git clone https://github.com/georgeoliver-hash/test-ops-platform.git
   git clone https://github.com/georgeoliver-hash/system-test-ops.git
   git clone https://github.com/georgeoliver-hash/test-automation-sit.git
   ```
3. Check it looks like this when you're done (`dir` or `ls`):
   ```
   Documents\GitHub\
     test-ops-platform\
     system-test-ops\
     test-automation-sit\
   ```
   All three folders side by side, not nested inside one another. If GitHub asks you to log
   in during the clone, use your own GitHub account (the one George added as a collaborator).

---

## Part 3 — Set up each repo's Python environment

Do this for **both** `system-test-ops` and `test-ops-platform` (not `test-automation-sit` yet
— you only need that one later, in Part 8).

For `system-test-ops`:
```
cd C:\Users\<you>\Documents\GitHub\system-test-ops
python -m venv .venv
.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

Then the same thing for `test-ops-platform`:
```
cd C:\Users\<you>\Documents\GitHub\test-ops-platform
python -m venv .venv
.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

Each of these can take a minute or two — that's normal.

---

## Part 4 — Your TestRail credentials

1. In `system-test-ops`, find the file `.env.example` and make a copy of it in the same
   folder named exactly `.env`.
2. Open `.env` in a text editor and fill in:
   ```
   TESTRAIL_URL=<the real TestRail URL — ask George if you don't have it>
   TESTRAIL_USER=<your own TestRail login email>
   TESTRAIL_API_KEY=<your own TestRail API key>
   ```
   Use **your own** account, not George's — this is what makes any suite push show up as
   done by you, not him. If you don't have a TestRail API key yet, generate one from your
   TestRail account settings, or ask George/IT.
3. Leave `TESTRAIL_WRITE_SUITE_ID` blank/unset for now — you'll set that later, and only if
   this specific pipeline step asks you to.
4. Save the file.

---

## Part 5 — Start the console and open it in your browser

1. Open a terminal in `test-ops-platform`:
   ```
   cd C:\Users\<you>\Documents\GitHub\test-ops-platform
   .venv\Scripts\python.exe -m uvicorn Platform.webapp.app:app --host 127.0.0.1 --port 8791
   ```
2. Leave that terminal window open — closing it stops the server. You should see lines
   ending in `Application startup complete.`
3. Open your web browser and go to: **http://127.0.0.1:8791**
4. You should see the console's home page. (You'll see "George Oliver" written at the
   bottom of the page — that's a known display quirk, not a bug. All your own data is stored
   separately on your machine regardless of what name is shown there.)

If the terminal prints an error about the port already being in use, something is already
running on it — close that other window/process first, then try again.

---

## Part 6 — Add your target (project + device + suite)

Skip this whole part if George tells you your target already shows up in the console for
you — check first by clicking the current target name at the top of the page.

1. Click the target name shown near the top of the page (it opens a "Change target" popup).
2. Pick your **Project** and **Device** from the dropdowns if they're already listed. If your
   project isn't listed yet, use the two text boxes below labelled "New project / device name"
   to type it in instead — leave the dropdowns alone in that case.
3. Click the button **"Add / edit this pair"**.
4. Fill in:
   - If this is a genuinely new suite with nothing built yet, tick **"Fresh build"**.
   - If it's not a fresh build, fill in the **old suite** name and its **numeric TestRail
     suite id** (the number in the suite's TestRail URL).
   - Always fill in the **new suite** name and its **numeric TestRail suite id** — this is
     the suite you'll actually be writing to. If you don't have this suite created in
     TestRail yet, go create an empty one there first and come back with its number.
5. Click **"Save pair"**.
6. Back in the main popup, tick **"I approve pointing this console at the suites shown
   above"**, then click **"Approve & apply target"**. (This is a real, meaningful
   confirmation — nothing that writes to TestRail is allowed to run until you've done this.)

---

## Part 7 — Run "Start" (readiness check)

1. Find and click **Start** in the console's navigation.
2. Click **Run**.
3. Watch what comes back. If anything is listed as needing your attention (missing
   credentials, an unset setting), it will say exactly what and where to fix it. Fix it, then
   run Start again.
4. Don't move on until this comes back clean.

---

## Part 8 — Ingest your project's documents

1. Upload your project's requirement/design documents wherever the console's docs upload
   area is (look for "Docs" or "Upload" in the navigation).
2. Find and open the **ingest-docs** pipeline.
3. Check the `docs_path` field shown is pointing at where you just uploaded (it should fill
   in automatically). If it's empty or looks wrong, ask George before continuing.
4. Click **Run**. You'll see a list of steps appear, each with its own status:
   - **sync_check** — a pause asking you to confirm the docs are in place. Read it, then
     click **Continue**.
   - **convert** — runs automatically, converts your raw docs to text.
   - **distil** — runs automatically (this is Claude reading your documents and writing
     grounded notes) — can take a few minutes, that's normal.
   - **cross_examine** — runs automatically, flags anything unclear or missing from the docs.
   - **commit_pr** — another pause. **Actually read what it's proposing to commit before
     clicking Continue** — this step does a real save into the `system-test-ops` repo.
5. If gaps get flagged (anything marked `**GAP**` or `**UNCONFIRMED**`), don't ignore them —
   flag them to George or whoever owns the source documents before moving to Part 9.

---

## Part 9 — Build the suite

1. Find and open the **onboard-suite** pipeline.
2. Confirm your project/device are correct, then click **Run**.
3. It will ask you to confirm some things before starting (do you actually have the docs,
   flows, defect history it needs). Answer honestly — if you're missing something, say so.
4. Watch the step list. Some steps run and finish on their own. Some are pauses that need
   you to click **Continue** after reading what they say. If your target is a fresh build,
   you'll notice a few steps get skipped automatically — that's expected, not an error.
5. You'll reach steps that draft test cases (one per topic/area found in your docs) — read
   what's drafted.
6. Then you'll reach **push** steps — these are the ones that actually write into TestRail.
   Each one shows an **"Approve & Push"** button instead of a plain Continue button. This
   is a deliberate, serious confirmation point:
   - It will refuse to let you push if your target isn't approved (go back to Part 6, step 6).
   - Actually read the drafted cases before clicking Approve & Push.
7. At the end there's a manual tidy-up step in TestRail itself (it will tell you exactly
   what to go do there).

---

## Part 10 — Hand off to automation

1. Open and run **export-automation** — this produces a list of which pushed cases are
   flagged as automatable.
2. Open and run **write-automation**.
   - The first step will ask you to confirm real facts about your test device (how to
     connect to it, its address, etc.). **Do not guess or make these up** — if you don't
     know them, say so; someone who does needs to confirm them.
   - It then writes automated test files into the `test-automation-sit` repo.
   - The very last step is another pause before anything is actually saved/shared to that
     repo — read the files it created before approving.

---

## If something goes wrong

- **Server won't start / "port already in use"**: something is already using that port —
  close it first, or ask whoever set your machine up.
- **A step fails and shows an error**: read the error text shown for that step — it's
  usually a missing credential or a setting that needs fixing in `.env`.
- **Anything is asking you to guess or invent a fact you genuinely don't know** (a device
  address, a screen behaviour that isn't in the docs): stop, don't guess, and ask. That's the
  tool correctly surfacing something nobody's confirmed yet — not something you're expected
  to fill in confidently.
- **Still stuck**: message George with the pipeline name, the exact step it stopped on, and
  whatever error text is shown on screen.
