"""Reader for the ETM's `DMParameters.json` — the WinCE analogue of the POS
`DatasetParameters.json` (framework/build/dataset_parameters.py).

The GFTS device-management layer authors application-level behaviour values
into `\\SD Memory\\GFTS\\State\\Params\\DM\\DMParameters.json`. The ETM carries
a richer set than the POS (22 keys vs 14) — extra fields like
`maximumInvalidLoginAttempts`, `offLineValueThreshold`, `abtPassback`, and the
`abt*TooZone` fare-zone bounds. All values are string-typed in the source,
matching how the platform consumes them.

Used as the expected-value source for ETM build-verification assertions.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SD_ROOT = REPO_ROOT / "builds" / "etm" / "GFTS"
RELATIVE_PATH = Path("State") / "Params" / "DM" / "DMParameters.json"
LIVE_OVERRIDE = REPO_ROOT / "artifacts" / "etm_dm_parameters_live.json"


def load_dm_parameters(sd_root: Path | str | None = None) -> dict[str, str]:
    """Return the parsed ETM `DMParameters.json`.

    Resolution order mirrors `load_dataset_parameters`:
    1. Explicit `sd_root` (the `GFTS` root) — caller forces a specific layout.
    2. `artifacts/etm_dm_parameters_live.json` — refreshed from the live device
       when the on-board build moves ahead of the cached SD dump.
    3. `builds/etm/GFTS/State/Params/DM/DMParameters.json` — the cached snapshot.

    All values come out as strings.
    """
    if sd_root is not None:
        path = Path(sd_root) / RELATIVE_PATH
    elif LIVE_OVERRIDE.exists():
        path = LIVE_OVERRIDE
    else:
        path = DEFAULT_SD_ROOT / RELATIVE_PATH
    with path.open("r", encoding="utf-8-sig") as fh:  # tolerate Windows BOM
        data = json.load(fh)
    return {str(k): str(v) for k, v in data.items()}
