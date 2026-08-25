from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import requests

from .auth import KeycloakTokenClient


@dataclass
class BOSConfig:
    base_url: str
    identity_provider_uri: str | None = None
    comms_group_id: str | None = None
    static_token_env: str = "BOS_API_TOKEN"

    @property
    def static_token(self) -> str | None:
        return os.getenv(self.static_token_env)


class BOSClient:
    """HTTP client for the Back Office System.

    Auth precedence:
      1. If BOS_API_TOKEN is set in the env, use it as a Bearer token. (Useful
         for early bring-up against a recorded session or a test stub.)
      2. Otherwise, if a KeycloakTokenClient is provided, fetch a token from
         the project's Keycloak realm and refresh on demand.

    All endpoint methods raise NotImplementedError until the BOS API contract
    is documented — tests must not silently pass against a fake.
    """

    def __init__(self, config: BOSConfig, auth: KeycloakTokenClient | None = None):
        self.config = config
        self.auth = auth
        self._session = requests.Session()
        if config.comms_group_id:
            self._session.headers["X-Comms-Group-Id"] = config.comms_group_id
        if config.static_token:
            self._session.headers["Authorization"] = f"Bearer {config.static_token}"

    def _ensure_auth(self) -> None:
        if self.config.static_token:
            return
        if not self.auth:
            raise RuntimeError(
                "No BOS auth configured: set BOS_API_TOKEN or wire a KeycloakTokenClient."
            )
        self._session.headers["Authorization"] = f"Bearer {self.auth.token()}"

    def get_audit_events(
        self,
        device_id: str,
        event: str | None = None,
        since_iso: str | None = None,
    ) -> list[dict[str, Any]]:
        self._ensure_auth()
        raise NotImplementedError(
            "BOS audit endpoint path not confirmed yet. Likely shape: "
            "GET {base}/audit/records?deviceId=...&event=...&since=... — verify with George."
        )
