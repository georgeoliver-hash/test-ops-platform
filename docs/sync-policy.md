# sit-mirror/ sync policy

`sit-mirror/` is a **one-way, read-only mirror** of three things from `flowbird-group/sit`:

- `Resources/Common/ConfigSets/<Project>/<ver>/EquipmentTypes.json` — device taxonomy per project/version
- `Resources/Devices/**/Bindings/*.robot` — the function-keyword vocabulary
- `Resources/Common/ConfigSets/<Project>/<ver>/ScreenFlow/<Device>/**` — screen graphs
  (`screenflow_map.jsonc`, `Templates/*.json`, `element_queries.json`), added 2026-08-25 when
  `model/flows.py` needed a real source instead of a guessed schema. Same tree the
  EquipmentTypes.json glob already walks, not a scope expansion.

## The rule

- **This repo never writes back to `flowbird-group/sit`.** No commits, no branches, no PRs opened
  from here, ever, automatically or otherwise.
- **`sit-mirror/` is regenerated, never hand-edited.** If a file in here is wrong or stale, fix it
  by re-running the sync script against a fresher `sit` checkout — don't patch the mirrored file
  directly, that edit will be silently lost (and worse, misleads whoever reads it next into thinking
  it reflects real SIT state).
- **Every sync stamps its source.** `_sync_manifest.json` records the exact `sit` commit hash, its
  date, and the sync timestamp. A stale mirror is always detectable — check this file before trusting
  anything in `sit-mirror/` for a decision that matters.

## Refreshing the mirror

```
python tools/sync_sit_mirror.py --sit-path <path-to-a-local-sit-checkout>
```

Point it at your local `sit` clone (pull that repo yourself first if you want the latest). Re-running
overwrites `sit-mirror/` in place and rewrites the manifest — safe to run any time.

## Why mirror instead of fork or depend directly

- **Fork/diverge** — risks `model/` quietly drifting from what SIT actually does, which is worse than
  not having the schema at all (a wrong "source of truth" is more dangerous than an absent one).
  Wrong-but-confident is exactly what a fork risks — [[project_ai_boundary_map]]'s no-gap-filling
  rule extends to this platform's dependency on SIT, not just to Gherkin case text.
- **Live dependency on `flowbird-group/sit`** — would make every run here depend on SIT's repo being
  reachable/checked-out at build time, and couples this sandbox's stability to a repo owned by a
  different team's release cadence.
- **A pinned, timestamped, regeneratable copy** is the middle ground: real data, no live coupling, and
  always honest about how fresh it is.

## Sync history

- **First sync (2026-08-24/25)**: from commit `23e29c0f` (2026-08-07) — 3 `EquipmentTypes.json`,
  29 `Bindings/*.robot`. Later found this was pinned to a **feature branch** commit, not `master`.
- **Re-sync (2026-08-25)**: switched the local `sit` checkout to `master`, pulled (207 commits
  behind), re-ran the sync — now from `master@b6b27288` (2026-08-25): 3 `EquipmentTypes.json`,
  32 `Bindings/*.robot`, and (new) 262 `ScreenFlow/**` files across 8 projects. 294 function
  keywords parsed (up from 267), all `model/` schema + flow tests green against the fresh data.
