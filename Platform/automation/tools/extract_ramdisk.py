"""Extract an Android ramdisk.img (gzipped cpio newc archive).

The way6 SD card carries `ramdisk.img` — the standard Android initrd format.
This tool decompresses it and unpacks the cpio archive into a directory so we
can read `init.rc`, `default.prop`, etc. — and edit them, repack, and write
back to the SD if we want to enable TCP adbd at boot.

Two outputs:
- `<out_dir>/...` — the file tree (so you can read/edit `default.prop` etc).
- `<out_dir>/manifest.json` — per-entry headers in original order, so
  `tools/pack_ramdisk.py` can rebuild a bit-faithful archive.

Usage:
    python -m tools.extract_ramdisk <ramdisk.img> <out_dir>

Symlinks: on Windows symlink creation needs admin. We write a `.symlink`
sidecar file for each symlink so the link target survives. The manifest
records the entry as `symlink_path` so the packer knows to read the sidecar
rather than the (non-existent) symlink at the canonical path.
"""
from __future__ import annotations

import gzip
import io
import json
import os
import stat
import sys
from pathlib import Path


NEWC_MAGIC = b"070701"
NEWC_HEADER_LEN = 110
MANIFEST_NAME = "manifest.json"


def parse_newc(stream: io.BufferedReader) -> list[dict]:
    """Yield records from a cpio newc-format stream. Stops at TRAILER!!!."""
    entries: list[dict] = []
    while True:
        header = stream.read(NEWC_HEADER_LEN)
        if len(header) < NEWC_HEADER_LEN:
            break
        if not header.startswith(NEWC_MAGIC):
            raise ValueError(f"Not cpio newc at offset {stream.tell() - NEWC_HEADER_LEN}: {header[:6]!r}")

        def h(start: int) -> int:
            return int(header[start:start + 8], 16)

        e = {
            "ino": h(6),
            "mode": h(14),
            "uid": h(22),
            "gid": h(30),
            "nlink": h(38),
            "mtime": h(46),
            "filesize": h(54),
            "major": h(62),
            "minor": h(70),
            "rmajor": h(78),
            "rminor": h(86),
            "namesize": h(94),
            "check": h(102),
        }
        name = stream.read(e["namesize"]).rstrip(b"\x00").decode("utf-8", "replace")
        # Pad name: total of (header + namesize) is aligned to 4 bytes.
        pad = (4 - (NEWC_HEADER_LEN + e["namesize"]) % 4) % 4
        stream.read(pad)
        if name == "TRAILER!!!":
            break
        data = stream.read(e["filesize"])
        pad = (4 - e["filesize"] % 4) % 4
        stream.read(pad)
        e["name"] = name
        e["data"] = data
        entries.append(e)
    return entries


def _write_entry(entry: dict, root: Path) -> dict:
    """Write the entry's data to disk; return a manifest record for it."""
    name = entry["name"].lstrip("/")
    target = root / name if name else root
    mode = entry["mode"]
    typ = mode & 0o170000

    record = {k: entry[k] for k in (
        "name", "ino", "mode", "uid", "gid", "nlink", "mtime",
        "filesize", "major", "minor", "rmajor", "rminor", "check",
    )}

    if typ == stat.S_IFDIR:
        target.mkdir(parents=True, exist_ok=True)
        record["kind"] = "dir"
    elif typ == stat.S_IFLNK:
        target.parent.mkdir(parents=True, exist_ok=True)
        link_target = entry["data"].decode("utf-8", "replace")
        record["kind"] = "symlink"
        record["link_target"] = link_target
        try:
            os.symlink(link_target, target)
            record["sidecar"] = None
        except (OSError, NotImplementedError):
            sidecar = target.with_suffix(target.suffix + ".symlink")
            sidecar.write_text(link_target, encoding="utf-8")
            record["sidecar"] = str(sidecar.relative_to(root)).replace("\\", "/")
    elif typ == stat.S_IFREG:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(entry["data"])
        record["kind"] = "file"
    else:
        # device nodes etc — store raw data so packer can round-trip them
        record["kind"] = "raw"
        record["data_b64"] = entry["data"].hex()  # hex for readability
    return record


def extract(img_path: Path, out_dir: Path) -> dict:
    raw = img_path.read_bytes()
    if raw[:2] == b"\x1f\x8b":
        body = gzip.decompress(raw)
        compression = "gzip"
    else:
        body = raw
        compression = "none"

    entries = parse_newc(io.BufferedReader(io.BytesIO(body)))
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest_entries: list[dict] = []
    for e in entries:
        manifest_entries.append(_write_entry(e, out_dir))

    manifest = {
        "compression": compression,
        "compressed_size": len(raw),
        "decompressed_size": len(body),
        "entry_count": len(entries),
        "entries": manifest_entries,
    }
    (out_dir / MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    return manifest


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("Usage: python -m tools.extract_ramdisk <ramdisk.img> <out_dir>", file=sys.stderr)
        return 2
    img = Path(argv[1])
    out = Path(argv[2])
    if not img.exists():
        print(f"error: {img} does not exist", file=sys.stderr)
        return 2
    info = extract(img, out)
    print(f"Compression:        {info['compression']}")
    print(f"Compressed size:    {info['compressed_size']:>10} bytes")
    print(f"Decompressed size:  {info['decompressed_size']:>10} bytes")
    print(f"Entry count:        {info['entry_count']}")
    print(f"Manifest:           {(out / MANIFEST_NAME).resolve()}")
    print(f"Extracted to:       {out.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
