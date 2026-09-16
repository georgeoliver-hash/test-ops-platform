# Test-Ops Console — click-by-click guide (for someone who's never used it)

Follow this in order. Every step says exactly what to click and what it does — you don't
need to know anything about the tool beforehand.

## Part 1 — Setup (once, before you touch the browser)

1. Ask George for GitHub access to three repos: `test-ops-platform`, `system-test-ops`, `test-automation-sit`.
2. Clone all three into the same folder, next to each other (not one inside another).
3. Install Claude Code and log in — type `claude` in a terminal to check it works.
4. In a terminal, go into `system-test-ops` and run `python -m venv .venv` then `.venv\Scripts\python.exe -m pip install -e ".[dev]"`.
5. Do the same thing (step 4) again, but inside the `test-ops-platform` folder.
6. In `system-test-ops`, copy the file `.env.example` and rename the copy to `.env`.
7. Open that new `.env` file in a text editor and fill in your own TestRail web address, your own TestRail username, and your own TestRail API key (ask George or IT if you don't have an API key).
8. In a terminal, go into `test-ops-platform` and run: `.venv\Scripts\python.exe -m uvicorn Platform.webapp.app:app --host 127.0.0.1 --port 8791`.
9. Leave that terminal window open — closing it shuts the tool down.
10. Open a web browser and go to `http://127.0.0.1:8791` — you should see the console's home page.

## Part 2 — Set up your target (project + device + suite)

1. At the top of the page, click the button labelled **"Change target"**.
2. A pop-up window appears. Find the button inside it called **"Add / edit this pair"** and click it.
3. A small form appears. In the two boxes labelled "New project / device name", type your project's name (e.g. your client's name) and your device's name (e.g. the machine you're testing).
4. Tick the checkbox **"Fresh build"** — this means you're building a brand-new suite from documents, not copying an old one.
5. Click the dropdown labelled "TestRail project" and pick the real TestRail project your new suite will live in.
6. A second dropdown for the suite will appear — either pick your suite from the list if it already exists in TestRail, or go create an empty suite in TestRail first if it doesn't exist yet, then come back and pick it.
7. Click **"Save pair"**.
8. Back in the main pop-up, tick the box that says **"I approve pointing this console at the suites shown above"**.
9. Click **"Approve & apply target"** — the pop-up closes and your target is now active. (Doing step 7 alone does NOT make it active — you must also do steps 8–9.)

## Part 3 — Check everything's ready

1. On the left-hand sidebar, click **"Start"**.
2. Click the **"Run"** button that appears.
3. Wait for it to finish — it checks your setup (credentials, Python packages, etc.) and tells you what's missing, if anything.
4. If it says something is missing, fix that specific thing, then click **"Run"** again until it comes back clean.

## Part 4 — Upload your documents

1. On the left-hand sidebar, click **"Docs"**.
2. Click **"Choose File"** (or similar), pick a document from your computer, and click **"Upload"**.
3. Repeat for every requirement/design document you have for this project.

## Part 5 — Turn the documents into structured notes (ingest-docs)

1. On the left-hand sidebar, find the section called **"Build"** and click it to open it.
2. Inside "Build", click **"ingest docs"**.
3. Click the **"Run"** button.
4. A list of steps appears below, each with its own status. Watch it:
   - When a step turns into a box asking you to **"Continue"**, read the text next to it first, then click **"Continue"**.
   - Some steps run by themselves and take a few minutes — that's normal, just wait.
5. When you reach a step called **"commit_pr"**, read what it says carefully — it's telling you it's about to save real files into the `system-test-ops` project. Click **"Continue"** once you're happy.
6. After that, open GitHub Desktop, point it at the `system-test-ops` folder, and you should see new files ready to commit. Write a short commit message and click commit, then push.

## Part 6 — Build the actual test suite (onboard-suite)

1. Still inside the **"Build"** section on the left, click **"onboard suite"**.
2. Click **"Run"**.
3. It will show you a message asking you to confirm you actually have what's needed (documents, screen designs, etc.) — read it and answer honestly, then continue.
4. Keep watching the step list. Some steps pause and say **"Continue"** — read each one before clicking it.
5. Some steps take several minutes each (especially ones that draft new test cases) — this is completely normal, don't worry if it looks like nothing's happening for a few minutes.
6. Eventually you'll see steps that say **"Approve & Push"** instead of "Continue" — these are serious: clicking this actually writes real test cases into TestRail. Before clicking, read what's been drafted. There will be one of these per topic/area in your documents, so you'll click it multiple times.
7. If any step turns red / says "failed", look for a button on that step called **"Retry from here"** and click that — do NOT click Run again from the top, that would redo everything that already worked.
8. At the very end there's a manual clean-up step in TestRail itself — it will tell you exactly what to go and tidy up there.

## Part 7 — Hand off to automation (export-automation)

1. Still inside **"Build"**, click **"export automation"**.
2. Click **"Run"**.
3. This produces a list of which of your new test cases are flagged as suitable for automated testing — no clicking needed beyond Run.

## Passing failures to Claude

1. Whenever a step fails, copy the exact text shown (the "Run failed" message and anything under "Result") and paste it to Claude, word for word — don't retype it in your own words.
2. If a step seems to be asking you to make up an answer you don't actually know, don't guess — tell Claude, or ask George.

## Things that might look weird but are normal

1. The name at the bottom of the page might say "George Oliver" even though it's you using it — this is a known cosmetic quirk, your work is still separate and safe on your own machine.
2. Some steps take 5–10 minutes each — that's genuine work happening, not a freeze.
3. The old suite and the new suite for a target can be in **different** TestRail projects — always double check both, don't assume.
4. `onboard-suite` is the newest, least-tested part of this tool — expect to hit more rough edges here than anywhere else, and that's expected, not your fault.
