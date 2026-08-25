"""Robot Framework Library: BOS audit assertions + the on-device local audit
ledger.

Replaces the pytest `bos` and `local_audit` fixtures.
"""
from __future__ import annotations

import os

from robot.api.deco import keyword, library
from robot.api.exceptions import SkipExecution
from robot.libraries.BuiltIn import BuiltIn

from framework.bos.audits import AuditAssertion
from framework.bos.auth import KeycloakConfig, KeycloakTokenClient
from framework.bos.client import BOSClient, BOSConfig
from framework.bos.local_audit import LocalAuditLedger
from framework.registry.models import OS


@library(scope="TEST")
class BOSLibrary:
    def __init__(self):
        self._device_lib = None
        self._audit: AuditAssertion | None = None
        self._local_audit: LocalAuditLedger | None = None

    @property
    def device_lib(self):
        if self._device_lib is None:
            self._device_lib = BuiltIn().get_library_instance("DeviceLibrary")
        return self._device_lib

    @property
    def audit(self) -> AuditAssertion:
        if self._audit is None:
            project = self.device_lib.project
            base_url = project.bos_base_url or os.getenv("BOS_BASE_URL")
            if not base_url:
                raise SkipExecution(
                    "No BOS base URL (set bos_base_url in devices.yaml or BOS_BASE_URL env)"
                )
            idp = project.identity_provider_uri or os.getenv("KEYCLOAK_REALM_URI")
            auth = None
            if idp and not os.getenv("BOS_API_TOKEN"):
                auth = KeycloakTokenClient(KeycloakConfig(realm_uri=idp))
            cfg = BOSConfig(
                base_url=base_url,
                identity_provider_uri=idp,
                comms_group_id=project.comms_group_id,
            )
            self._audit = AuditAssertion(BOSClient(cfg, auth=auth))
        return self._audit

    @property
    def local_audit(self) -> LocalAuditLedger:
        device = self.device_lib.device
        if device.os != OS.ANDROID:
            raise SkipExecution("local audit ledger reader is only implemented for Android devices")
        if self._local_audit is None:
            ledger = LocalAuditLedger(self.device_lib.transport)
            if not ledger.discover():
                raise SkipExecution(f"Audit/BOSRecords directory not found on {device.id}")
            self._local_audit = ledger
        return self._local_audit

    # ─── BOS audit (remote) ──────────────────────────────────────────────────

    @keyword("Expect BOS Audit Event")
    def expect_bos_audit_event(self, event: str, device_id: str, within_seconds: float = 30.0) -> dict:
        return self.audit.expect(event=event, device_id=device_id, within_seconds=within_seconds)

    # ─── local audit ledger (on-device) ─────────────────────────────────────

    @keyword("Get Local Audit Ledger")
    def get_local_audit_ledger(self) -> LocalAuditLedger:
        return self.local_audit

    @keyword("List Local Audit Records")
    def list_local_audit_records(self) -> list:
        return self.local_audit.list_records()

    @keyword("Newest Local Audit Record")
    def newest_local_audit_record(self):
        return self.local_audit.newest_record()

    @keyword("Expect Local Audit Record")
    def expect_local_audit_record(self, event: str, within_seconds: float = 30.0) -> dict:
        return self.local_audit.expect(event=event, within_seconds=within_seconds)
