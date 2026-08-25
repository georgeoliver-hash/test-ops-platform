"""Fingerprint a single SD-card root and print what we know about the device.

Auto-detects the build layout:
  * Android/POS SD (way6) — reads `pos/backofficeagent.config.json`, `artifact.VID`,
    `dtbs.list`, `splash.info`.
  * Windows-CE/ETM SD (GFTS/SRSService) — reads `backoffice/.deviceinfo/device/*`,
    `GFTS/State/Params/{DM,RM}/*Parameters.json`, and the SRSService
    `BackOfficeAgentConfig.json` (BOS uri, DeviceSSN, IdP).

Prints one JSON document. Useful when a fresh build arrives and you need to
figure out which device it is.

Usage:
  python -m tools.inspect_device_build builds/External-SD
  python -m tools.inspect_device_build builds/etm
  python -m tools.inspect_device_build builds/Internal-SD/1.3.12.22119_APK_Packages.pos.STE11
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def is_wince_build(root: Path) -> bool:
    """A Windows-CE/ETM SD root carries a WinCE launcher + the GFTS app tree."""
    return (root / "GFTS").is_dir() or (root / "Launcher.config").exists() or (
        root / "STARTUP.BAT"
    ).exists()


def _read_json(path: Path) -> dict | str:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001 — surface the reason inline
        return f"<unreadable: {e}>"


def fingerprint_wince(root: Path) -> dict:
    info: dict = {"root": str(root), "platform": "wince"}

    # Device identity — small text files, one value each.
    devinfo = root / "backoffice" / ".deviceinfo" / "device"
    if devinfo.is_dir():
        ident: dict = {}
        for f in sorted(devinfo.glob("*")):
            if f.is_file() and f.name != "hash":  # hash is binary
                try:
                    ident[f.name] = f.read_text(encoding="utf-8", errors="replace").strip()
                except Exception as e:  # noqa: BLE001
                    ident[f.name] = f"<unreadable: {e}>"
        info["device_identity"] = ident

    for label, rel in (
        ("dm_parameters", Path("GFTS/State/Params/DM/DMParameters.json")),
        ("rm_parameters", Path("GFTS/State/Params/RM/RMParameters.json")),
    ):
        p = root / rel
        if p.exists():
            info[label] = _read_json(p)

    # SRSService BackOfficeAgentConfig — buried under an ArtifactCache GUID dir,
    # so glob for it rather than hard-coding the version/GUID path.
    boa = next(
        root.rglob("SRSService/Configuration/BackOfficeAgentConfig.json"), None
    )
    if boa is not None:
        cfg = _read_json(boa)
        if isinstance(cfg, dict):
            info["backoffice_agent"] = {
                k: cfg.get(k)
                for k in (
                    "DeviceSSN",
                    "DeviceType",
                    "BOSUri",
                    "CommsGroupId",
                    "IdentityProviderUri",
                )
            }
        else:
            info["backoffice_agent"] = cfg

    artifact = root / "artifact.VID"
    if artifact.exists():
        info["artifact_vid"] = _read_json(artifact)

    return info


def fingerprint(root: Path) -> dict:
    if is_wince_build(root):
        return fingerprint_wince(root)
    info: dict = {"root": str(root)}

    boa = root / "pos" / "backofficeagent.config.json"
    if boa.exists():
        try:
            info["backoffice_agent"] = json.loads(boa.read_text(encoding="utf-8"))
        except Exception as e:
            info["backoffice_agent_error"] = str(e)

    artifact = root / "artifact.VID"
    if artifact.exists():
        try:
            info["artifact_vid"] = json.loads(artifact.read_text(encoding="utf-8"))
        except Exception as e:
            info["artifact_vid_error"] = str(e)

    dtbs = root / "dtbs.list"
    if dtbs.exists():
        info["dtbs"] = [
            line.strip()
            for line in dtbs.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    splash = root / "splash.info"
    if splash.exists():
        info["splash"] = splash.read_text(encoding="utf-8").strip()

    boot_txt = root / "boot.txt"
    if boot_txt.exists():
        info["boot_txt_size"] = boot_txt.stat().st_size

    apk_pkg = list(root.glob("*_APK_Packages.*"))
    if apk_pkg:
        info["apk_packages"] = [p.name for p in apk_pkg]

    return info


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python -m tools.inspect_device_build <path-to-sd-root>")
        return 2
    root = Path(argv[1])
    if not root.exists():
        print(f"Path not found: {root}", file=sys.stderr)
        return 1
    print(json.dumps(fingerprint(root), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
