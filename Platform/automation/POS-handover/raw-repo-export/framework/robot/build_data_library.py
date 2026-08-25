"""Robot Framework Library: authored build-verification data, no device needed.

Replaces the pytest `dataset_parameters` fixture (POS `DatasetParameters.json`).
The ETM analogue (`etm_dm_parameters`) lives in `WinceLibrary` alongside the
rest of the ETM-specific reading, since it's only ever used on ETM suites.
"""
from __future__ import annotations

from robot.api.deco import keyword, library
from robot.api.exceptions import SkipExecution

from framework.build.dataset_parameters import load_dataset_parameters


@library(scope="GLOBAL")
class BuildDataLibrary:
    @keyword("Get Dataset Parameters")
    def get_dataset_parameters(self) -> dict:
        try:
            return load_dataset_parameters()
        except FileNotFoundError as e:
            raise SkipExecution(str(e)) from e
