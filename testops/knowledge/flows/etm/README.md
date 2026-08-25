# ETM Overflow design assets

Drop the **downloaded ETM Overflow images here**, one subfolder per flow. Images anywhere under
`knowledge/flows/**` are gitignored (png/webp/jpg/jpeg) — they're large reference assets, kept
locally / in a shared store, **not committed**. The committed, derived text is:

- `knowledge/flows/ETMoverflow_data.json` — full Overflow export (also gitignored; 12MB source).
- `knowledge/flows/etm-flow-annotations.md` — the annotation notes + screen names extracted per flow
  by `tools/extract_overflow_annotations.py`. **This is what the agents read.** Re-run the extractor
  if the Overflow doc is re-exported:
  `python tools/extract_overflow_annotations.py knowledge/flows/ETMoverflow_data.json knowledge/flows/etm-flow-annotations.md`

## Where to put images — drop the export zip, the organiser tidies it

Export each Overflow flow as a zip of screen PNGs (named like `ETM-TFTS-V15.0.4 - <Flow>.zip`) and
drop it straight in `knowledge/flows/`. Then run:

```
python tools/organise_flow_zips.py --device etm
```

It extracts each zip into `knowledge/flows/etm/<flow-slug>/`, names kept from Overflow's screen
captions, and removes the redundant zip. Re-runnable as you add more zips. (`--dry-run` to preview,
`--keep-zips` to retain the archives.)

Source: `overflow.io/s/NDLGF6NF`. 16 boards; the real flows (skip "Title Board" / "Board 1", and the
superseded "Driver Menu / Options (Old layout draft)"):

| Overflow flow | Folder (auto-slug) | Screens |
|---|---|---|
| Startup | `etm/startup/` | 5 |
| Driver Sign On | `etm/driver-sign-on/` | 37 |
| FLU | `etm/flu/` | 80 |
| FLU 2.0 Navigation | `etm/flu-2-0-navigation/` | 27 |
| FLU 2.0 Ticket Issuance | `etm/flu-2-0-ticket-issuance/` | 6 |
| FLU - Basket Mode | `etm/basket-mode/` | 17 |
| Driver Menu / Options | `etm/options/` | 60 |
| Supervisor | `etm/supervisor/` | 19 |
| Technician | `etm/technician/` | 36 |
| Displays LEDs and Audio Tones | `etm/displays-leds-and-audio-tones/` | 29 |
| Barcode Scanning | `etm/barcode-scanning/` | 22 |
| Power Interruption | `etm/power-interruption/` | 3 |
| Revenue Limit | `etm/revenue-limit/` | 2 |

> Note: the slug comes from the text after the last " - " in the zip name, so name your zips with the
> flow at the end (e.g. `... - Driver Sign On.zip`). Done so far: **startup** (5).

## Naming

Keep Overflow's screen-caption filenames (e.g. `01.1.4 - Sign On - Incorrect Details.png`). The
screen names already appear in `etm-flow-annotations.md`, so HMI screen-validation cases can cite
the exact image filename in the case preface — TestRail's API on this instance **cannot attach
images** (`add_attachment_to_case` 404), so the preface-reference is how screen cases point at the
picture, same convention as POS.
