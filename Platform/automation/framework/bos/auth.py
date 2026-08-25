"""Keycloak (OpenID Connect) token client for BOS access.

The on-device backofficeagent.config.json points at a Keycloak realm
(e.g. https://auth-...albedo-gen.co.uk/auth/realms/TranslinkDevices/). For tests
we need a service-account or test-user token in the same realm — credentials
come from env vars, never the registry.

Two grant types supported:
- `client_credentials` — when KEYCLOAK_CLIENT_SECRET is set without a username.
- `password`           — when KEYCLOAK_USERNAME + KEYCLOAK_PASSWORD are set.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass

import requests


@dataclass
class KeycloakConfig:
    realm_uri: str  # e.g. https://.../auth/realms/TranslinkDevices/
    client_id_env: str = "KEYCLOAK_CLIENT_ID"
    client_secret_env: str = "KEYCLOAK_CLIENT_SECRET"
    username_env: str = "KEYCLOAK_USERNAME"
    password_env: str = "KEYCLOAK_PASSWORD"


class KeycloakTokenClient:
    def __init__(self, config: KeycloakConfig):
        self.config = config
        self._token: str | None = None
        self._expires_at: float = 0.0

    def token(self) -> str:
        if self._token and time.monotonic() < self._expires_at - 60:
            return self._token
        return self._refresh()

    def _refresh(self) -> str:
        endpoint = self.config.realm_uri.rstrip("/") + "/protocol/openid-connect/token"
        client_id = os.getenv(self.config.client_id_env)
        if not client_id:
            raise RuntimeError(f"{self.config.client_id_env} not set")
        client_secret = os.getenv(self.config.client_secret_env)
        username = os.getenv(self.config.username_env)
        password = os.getenv(self.config.password_env)

        if username and password:
            data = {
                "grant_type": "password",
                "client_id": client_id,
                "username": username,
                "password": password,
            }
            if client_secret:
                data["client_secret"] = client_secret
        elif client_secret:
            data = {
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            }
        else:
            raise RuntimeError(
                f"Need either {self.config.client_secret_env} (client_credentials) "
                f"or {self.config.username_env}/{self.config.password_env} (password grant)"
            )

        resp = requests.post(endpoint, data=data, timeout=10)
        resp.raise_for_status()
        body = resp.json()
        self._token = body["access_token"]
        self._expires_at = time.monotonic() + body.get("expires_in", 300)
        return self._token
