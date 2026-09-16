# Test-Ops Console — click-by-click guide (for someone who's never used it)

Follow this in order, top to bottom. Every step says what to click, what it looks like on
screen, and what actually happens underneath — so you always know whether it worked before
moving to the next one. Don't skip ahead even if a later button looks clickable.

## Part 1 — Setup (once, before you touch the browser)

This gets your machine ready. You only do this once, ever.

1. Ask George for GitHub access to three repos: `test-ops-platform`, `system-test-ops`, `test-automation-sit`. Without this, the `git clone` commands below will fail with a permission error.
2. Clone all three into the same folder, next to each other — e.g. `Documents\GitHub\test-ops-platform`, `Documents\GitHub\system-test-ops`, `Documents\GitHub\test-automation-sit`, all siblings, none nested inside another. This exact layout matters: the tool looks for the other two repos right next to itself on disk, and won't find them otherwise.
3. Install Claude Code and log in. Test it by typing `claude` in a terminal — it should open without an error. Several steps later on run Claude Code behind the scenes, so this has to work first.
4. Open a terminal, navigate into `system-test-ops`, and run `python -m venv .venv`. This creates an isolated Python environment just for this project, so it doesn't clash with anything else on your machine. Then run `.venv\Scripts\python.exe -m pip install -e ".[dev]"` — this installs all the Python packages the tool needs; it can take a minute or two, that's normal.
5. Inside `test-ops-platform`, run `python -m venv .venv` the same as step 4. But the install command is different here — this repo's dependency list lives in a `requirements.txt` file at the top level, not a `pyproject.toml` (that's only true for `system-test-ops`). Run `.venv\Scripts\python.exe -m pip install -r requirements.txt` instead. If you see an error like "does not appear to be a Python project: neither setup.py nor pyproject.toml found", that means the wrong command (the `pip install -e ".[dev]"` one from step 4) got used here by mistake — use the `-r requirements.txt` command shown above instead.
6. Inside `system-test-ops`, find the file `.env.example`. Make a copy of it in the same folder and rename the copy to exactly `.env` (no ".example" on the end). This file holds your personal settings and credentials — it's deliberately never shared or committed to git.
7. Open your new `.env` file in a plain text editor. Fill in `TESTRAIL_URL` (the TestRail web address), `TESTRAIL_USER` (your own login email), and `TESTRAIL_API_KEY` (your own API key — generate one from your TestRail account settings, or ask George/IT). Using your own account matters: it's what makes any work you do show up as done by you, not George.
8. Open a terminal in `test-ops-platform` and run: `.venv\Scripts\python.exe -m uvicorn Platform.webapp.app:app --host 127.0.0.1 --port 8791`. This starts the actual web server that the browser talks to.
9. Leave that terminal window open in the background — it's not frozen, it's just running quietly. Closing it, or closing the terminal app, immediately shuts the whole tool down.
10. Open a web browser and go to the address `http://127.0.0.1:8791`. You should see the console's home page load, with a sidebar on the left and a "Change target" button near the top. If the page doesn't load, the server (step 8) probably isn't running — check that terminal window for an error.

## Part 2 — Set up your target (project + device + suite)

A "target" tells the tool which project, which device, and which real TestRail suite you're
working on. Nothing else works until this is set correctly.

1. Near the top of the page, find and click the button labelled **"Change target"**. A pop-up window opens on top of the page.
2. Inside that pop-up, find a smaller button labelled **"Add / edit this pair"** and click it. A small form expands underneath it.
3. You'll see two text boxes labelled "New project / device name". Type your project's real name (e.g. your client's name) into the first, and your device's name (e.g. the machine you're testing) into the second. This is what creates a brand-new entry — it doesn't need to exist anywhere yet.
4. Tick the checkbox labelled **"Fresh build"**. This tells the tool there's no old/existing TestRail suite to copy from — you're building a suite purely from your documents, from scratch. Leave it unticked only if you genuinely have an old suite you're replacing.
5. A dropdown labelled "TestRail project" appears — click it and pick the real TestRail project your suite belongs to (this is a real project already set up in TestRail itself, not something you're creating here). Picking from this list — rather than typing a number — is what stops you accidentally pointing at the wrong project, which has caused real problems before.
6. Once you've picked a project, a second dropdown for suites appears, listing every real suite inside that project. If your suite is already there, pick it. If it isn't, go create an empty suite for it in the TestRail website first, then come back to this dropdown and pick it.
7. Click **"Save pair"**. This saves your new target, but does NOT yet make it the active one you're working against — that's the next two steps.
8. Back in the main pop-up (not the smaller form), tick the checkbox that says **"I approve pointing this console at the suites shown above"**. This is a real, meaningful confirmation, not a formality — nothing that writes to TestRail is allowed to happen until this is ticked.
9. Click **"Approve & apply target"**. The pop-up closes, and the target shown at the top of the page updates to your new project/device/suite. If it still shows the old target after this, something didn't save — go back to step 1.

## Part 3 — Check everything's ready (Start)

This is a safety check that catches missing setup before you waste time further in.

1. On the left-hand sidebar, click **"Start"**.
2. Click the **"Run"** button on that page.
3. Wait a few seconds. It checks things like: are your credentials set correctly, is TestRail actually reachable, are the right Python packages installed. When it finishes, it prints a clear verdict — either "all green" or a list of exactly what's missing and how to fix it.
4. If anything's flagged, fix that one specific thing, then click **"Run"** again. Repeat until it comes back clean before moving on — later steps will behave strangely if this isn't sorted first.

## Part 4 — Upload your documents

The tool needs your real requirement/design documents before it can build anything from them.

1. On the left-hand sidebar, click **"Docs"**.
2. Click the file-upload button, choose a document from your computer, then click **"Upload"**. You should see it appear in a list on the page once it's done — that confirms it actually landed on the server.
3. Repeat step 2 for every relevant document you have for this project (specs, interface docs, HMI descriptions, anything that describes how the device should behave).

## Part 5 — Turn the documents into structured notes (ingest-docs)

This step reads your raw documents and produces clean, cited notes that everything later is
grounded in — nothing gets invented that isn't actually in your documents.

1. On the left sidebar, find and click open the section labelled **"Build"** — it expands to show several sub-items.
2. Click **"ingest docs"**.
3. Click **"Run"**. A list of steps appears below and starts updating live.
4. You'll hit a pause that says something like "awaiting confirmation" with a **"Continue"** button — read the text next to it (it's usually confirming your documents are actually in place), then click **"Continue"**.
5. The next couple of steps run by themselves with no clicking needed — one converts your documents to plain text, the next (the slowest — genuinely reads and writes real content, can take several minutes per document) produces the actual structured notes. Don't worry if it looks idle for a few minutes; that's real work happening, not a freeze.
6. You'll reach another pause called **commit_pr** — read what it says (it's telling you it's about to save real new files into the `system-test-ops` project on your computer). Click **"Continue"**.
7. Open GitHub Desktop, point it at your `system-test-ops` folder, and you should see the new files listed as changes ready to commit. Write a short commit message describing what this is, click "Commit", then click "Push" so it's saved to GitHub, not just your machine.

## Part 6 — Build the actual test suite (onboard-suite)

This is the main event: it reads the notes from Part 5 and drafts a real, structured test
suite, then (with your explicit approval) writes it into TestRail for real.

1. Still inside the **"Build"** section, click **"onboard suite"**.
2. Click **"Run"**.
3. First you'll see a message asking you to confirm you actually have everything needed (documents, any existing screen designs, defect history). Answer honestly — if something's missing, say so rather than guessing, and it'll still proceed but flag that gap.
4. Watch the step list. Steps that finish on their own will just tick over to a green "succeeded" status. Steps that need you will show a **"Continue"** button and some explanation text — always read that text before clicking, since a few of these are asking you to actually confirm something, not just acknowledge it.
5. Several steps (especially the ones drafting new test cases, one per topic found in your documents) genuinely take a few minutes each — this is the tool doing real, careful work, not hanging. You'll see one step per topic area appear in the list as it works through them.
6. Eventually you'll reach steps showing a button labelled **"Approve & Push"** instead of "Continue" — this is different and serious: clicking it makes a real, permanent write into TestRail. Before clicking, actually read what's been drafted for that topic area. You'll see one of these buttons per topic area, so expect to click through several of them, one at a time.
7. If any step turns red and shows "failed", look on that same step for a button called **"Retry from here"** — click that one specifically. Don't click the main "Run" button again from the top of the page, since that would throw away everything that already worked and start over from scratch.
8. At the very end there's a manual clean-up step that happens in the TestRail website itself, not in this tool — it will tell you exactly what to go tidy up there (e.g. deleting placeholder sections, setting up run configurations).

## Part 7 — Hand off to automation (export-automation)

Once your suite is built and pushed, this step produces a list of which of the new cases are
suitable for automated (not manual) testing.

1. Still inside **"Build"**, click **"export automation"**.
2. Click **"Run"** and wait for it to finish — no further clicking needed.
3. It produces a file listing which cases are automatable, which are destructive (need extra care), and which are manual-only — this is the handoff point to actually writing automated test scripts, a separate piece of work.

## Passing failures to Claude

1. Whenever a step fails, copy the exact text shown on screen — the "Run failed" message and anything under "Result" or "Raw CLI output" — and paste all of it to Claude, word for word. Don't summarise or retype it in your own words; the exact wording often matters for diagnosing the real cause.
2. If a step seems to be asking you to make up an answer you don't actually know (a device address, a specific behaviour not in your documents), don't guess. Say so to Claude, or ask George — inventing an answer here creates a real, hidden defect in the suite.

## Things that might look weird but are actually normal

1. The name shown at the bottom of the page might say "George Oliver" even when it's you using the tool — this is a known display quirk. Your own work stays completely separate and safe on your own machine regardless of what name is shown.
2. Some steps take 5–10 minutes each with no visible progress in between — that's genuine work happening in the background, not a freeze. If you're ever unsure, ask Claude to check rather than assuming it's stuck.
3. The "old" suite and the "new" suite for the same target can live in **different** TestRail projects — always check both dropdowns carefully in Part 2, don't assume they're the same project just because they're for the same device.
4. `onboard-suite` (Part 6) is the newest and least-tested part of this whole tool — expect to hit more rough edges here than anywhere else in this guide. That's expected, not something you're doing wrong.
