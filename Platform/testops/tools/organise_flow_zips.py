"""Organise Overflow per-flow image exports into tidy per-flow subfolders.

George exports each Overflow flow either as a zip of screen PNGs, or as an already-extracted folder,
named like `ETM-TFTS-V15.0.4 - <Flow>`. This consolidates both into
`knowledge/flows/<device>/<flow-slug>/`, with the canonical design screens at the top of each flow
folder. It:
  * de-duplicates Overflow's `... (1).png` / `... (2).png` re-exports of the same screen,
  * quarantines stray manual `Screenshot ....png` captures into a `_screenshots/` subfolder,
  * removes the consumed zip / source folder so `knowledge/flows/` stays neat.
Re-runnable: a screen already present in the destination is skipped.

Usage:
    python tools/organise_flow_zips.py [--device etm] [--src knowledge/flows] [--keep-sources] [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import zipfile
from pathlib import Path

IMG_EXT = {".png", ".webp", ".jpg", ".jpeg"}


def slug(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name.strip().lower()).strip("-")
    return re.sub(r"-+", "-", s)


def flow_name(stem: str) -> str:
    return stem.rsplit(" - ", 1)[-1] if " - " in stem else stem


def canonical(filename: str) -> str:
    """Strip a trailing ' (N)' duplicate marker before the extension."""
    p = Path(filename)
    base = re.sub(r" \(\d+\)$", "", p.stem)
    return base + p.suffix


def is_screenshot(filename: str) -> bool:
    return filename.lower().startswith("screenshot ")


def place(dest: Path, name: str, write_bytes, dry: bool) -> str:
    """Decide target path for a file; return action label. write_bytes() yields content."""
    if is_screenshot(name):
        target = dest / "_screenshots" / name
        label = "screenshot"
    else:
        target = dest / canonical(name)
        label = "screen"
    if target.exists():
        return "skip (exists)"
    if dry:
        return f"{label} -> {target.name}"
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "wb") as fout:
        write_bytes(fout)
    return f"{label} -> {target.name}"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="etm")
    ap.add_argument("--src", default="knowledge/flows")
    ap.add_argument("--keep-sources", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv[1:])

    src = Path(args.src)
    dev = args.device
    dest_root = src / dev
    dest_root.mkdir(parents=True, exist_ok=True)
    prefix = dev.upper()

    # source zips and source folders named like "<PREFIX>...- <Flow>".
    # Accept them dropped either at the top of `flows/` OR inside the device dest folder.
    def is_export_dir(p: Path) -> bool:
        return p.is_dir() and p != dest_root and " - " in p.name and p.name.upper().startswith(prefix)

    zips = [p for p in src.glob("*.zip") if p.stem.upper().startswith(prefix)]
    dirs = [p for p in src.iterdir() if is_export_dir(p)]
    dirs += [p for p in dest_root.iterdir() if is_export_dir(p)]
    if not zips and not dirs:
        print(f"No '{dev}' flow zips or export folders found in {src}")
        return 0

    consumed: list[Path] = []

    for z in sorted(zips):
        dest = dest_root / slug(flow_name(z.stem))
        print(f"[zip] {z.name} -> {dest.name}/")
        with zipfile.ZipFile(z) as zf:
            for m in zf.namelist():
                if m.endswith("/"):
                    continue
                nm = Path(m).name
                if Path(nm).suffix.lower() not in IMG_EXT:
                    continue
                action = place(dest, nm, (lambda fo, mm=m, zz=zf: shutil.copyfileobj(zz.open(mm), fo)), args.dry_run)
                print(f"   {nm}  {action}")
        consumed.append(z)

    for d in sorted(dirs):
        dest = dest_root / slug(flow_name(d.name))
        files = [f for f in d.rglob("*") if f.is_file() and f.suffix.lower() in IMG_EXT]
        print(f"[dir] {d.name} -> {dest.name}/  ({len(files)} images)")
        for f in files:
            action = place(dest, f.name, (lambda fo, ff=f: shutil.copyfileobj(open(ff, "rb"), fo)), args.dry_run)
            if not action.startswith("skip"):
                print(f"   {f.name}  {action}")
        consumed.append(d)

    if not args.keep_sources and not args.dry_run:
        for c in consumed:
            if c.is_dir():
                shutil.rmtree(c)
            else:
                c.unlink()
            print(f"removed source {c.name}")

    # summary
    print("\n-- per-flow image counts --")
    for sub in sorted(dest_root.iterdir()):
        if sub.is_dir():
            n = sum(1 for f in sub.glob("*") if f.is_file() and f.suffix.lower() in IMG_EXT)
            extra = sum(1 for f in (sub / "_screenshots").glob("*")) if (sub / "_screenshots").exists() else 0
            print(f"  {sub.name:<34} {n} screens" + (f"  (+{extra} screenshots)" if extra else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
