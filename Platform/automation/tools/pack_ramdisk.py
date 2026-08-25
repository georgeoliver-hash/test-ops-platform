"""Pack a directory tree back into an Android `ramdisk.img` (gzipped cpio newc).

Inverse of `tools/extract_ramdisk.py`. Reads `manifest.json` from the input
dir to get the original entry headers (mode, mtime, ordering, link targets);
re-reads file content from disk so any edits to `default.prop`/`init.rc`
take effect.

Usage:
    python -m tools.pack_ramdisk <in_dir> <out_img>

The output is suitable to drop on the SD card's FAT partition as
`ramdisk.img`. Verify first with `tools/extract_ramdisk.py <out_img> <tmp>`
and diff the trees.

We deliberately do NOT try to match Flowbird's original gzip header
byte-for-byte — the Linux kernel only cares that the gzip+cpio streams are
valid. A round-trip extract→pack→extract must yield identical file contents
and identical manifest fields; that's the verification target.
"""
from __future__ import annotations

import gzip
import io
import json
import stat
import sys
from pathlib import Path


NEWC_MAGIC = b"070701"
NEWC_HEADER_LEN = 110
TRAILER_NAME = "TRAILER!!!"


def _pad4(n: int) -> int:
    return (4 - n % 4) % 4


def _emit_entry(buf: io.BytesIO, header_fields: dict, name: str, data: bytes) -> None:
    """Append one cpio newc record to `buf`."""
    name_bytes = name.encode("utf-8") + b"\x00"
    namesize = len(name_bytes)

    fields = (
        header_fields["ino"],
        header_fields["mode"],
        header_fields["uid"],
        header_fields["gid"],
        header_fields["nlink"],
        header_fields["mtime"],
        len(data),
        header_fields["major"],
        header_fields["minor"],
        header_fields["rmajor"],
        header_fields["rminor"],
        namesize,
        header_fields["check"],
    )
    header = NEWC_MAGIC + b"".join(f"{v:08X}".encode("ascii") for v in fields)
    assert len(header) == NEWC_HEADER_LEN, len(header)

    buf.write(header)
    buf.write(name_bytes)
    buf.write(b"\x00" * _pad4(NEWC_HEADER_LEN + namesize))
    buf.write(data)
    buf.write(b"\x00" * _pad4(len(data)))


def _entry_data(record: dict, root: Path) -> bytes:
    """Return the bytes that go in the entry's data field, re-reading from disk."""
    kind = record["kind"]
    if kind == "dir":
        return b""
    if kind == "symlink":
        # link target is the data; prefer the sidecar (which we may have edited)
        sidecar = record.get("sidecar")
        if sidecar:
            return (root / sidecar).read_text(encoding="utf-8").encode("utf-8")
        target = root / record["name"].lstrip("/")
        # On a system that supports symlinks we'd readlink; fall back to manifest target
        try:
            import os
            return os.readlink(target).encode("utf-8")
        except OSError:
            return record["link_target"].encode("utf-8")
    if kind == "file":
        path = root / record["name"].lstrip("/")
        return path.read_bytes()
    if kind == "raw":
        return bytes.fromhex(record["data_b64"])
    raise ValueError(f"unknown record kind: {kind}")


def pack(in_dir: Path, out_img: Path) -> dict:
    manifest_path = in_dir / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"No manifest.json in {in_dir} — extract with tools/extract_ramdisk first")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    body = io.BytesIO()
    for record in manifest["entries"]:
        data = _entry_data(record, in_dir)
        _emit_entry(body, record, record["name"], data)

    # TRAILER!!! sentinel — ino=0 everything zero, nlink=1, filesize=0
    trailer = {
        "ino": 0, "mode": 0, "uid": 0, "gid": 0, "nlink": 1,
        "mtime": 0, "major": 0, "minor": 0, "rmajor": 0, "rminor": 0, "check": 0,
    }
    _emit_entry(body, trailer, TRAILER_NAME, b"")

    cpio_bytes = body.getvalue()
    # Some kernels insist the whole archive is 512-byte aligned. Pad with zeros.
    pad = (512 - len(cpio_bytes) % 512) % 512
    cpio_bytes += b"\x00" * pad

    if manifest.get("compression") == "gzip":
        # mtime=0 → deterministic gzip header (no filename, no current time).
        gz_buf = io.BytesIO()
        with gzip.GzipFile(fileobj=gz_buf, mode="wb", compresslevel=9, mtime=0) as gz:
            gz.write(cpio_bytes)
        out_bytes = gz_buf.getvalue()
    else:
        out_bytes = cpio_bytes

    out_img.write_bytes(out_bytes)
    return {
        "entries": len(manifest["entries"]),
        "cpio_size": len(cpio_bytes),
        "out_size": len(out_bytes),
        "out_path": str(out_img.resolve()),
    }


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("Usage: python -m tools.pack_ramdisk <in_dir> <out_img>", file=sys.stderr)
        return 2
    in_dir = Path(argv[1])
    out_img = Path(argv[2])
    if not in_dir.is_dir():
        print(f"error: {in_dir} is not a directory", file=sys.stderr)
        return 2
    info = pack(in_dir, out_img)
    print(f"Entries packed:     {info['entries']}")
    print(f"CPIO size:          {info['cpio_size']:>10} bytes")
    print(f"Output (gzipped):   {info['out_size']:>10} bytes")
    print(f"Wrote:              {info['out_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
