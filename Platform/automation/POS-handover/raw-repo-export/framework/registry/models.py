from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class DeviceType(str, Enum):
    ETMS = "ETMS"
    POS = "POS"
    TVM = "TVM"
    GV = "GV"
    PV = "PV"
    BV = "BV"
    HHD = "HHD"
    PORTAL = "PORTAL"  # back-office web portal target (BOS/ABT/CloudFare/Merit) — no physical device


class OS(str, Enum):
    LINUX = "linux"
    ANDROID = "android"
    WINCE = "wince"  # Windows Embedded Compact (e.g. Translink ETM4 / GFTS stack)
    NONE = "none"  # no physical device/OS — pure web-portal target


class UIKind(str, Enum):
    WEB = "web"
    ANDROID_APP = "android_app"
    NONE = "none"


class SSHTransport(BaseModel):
    kind: Literal["ssh"] = "ssh"
    host: str
    port: int = 22
    user: str
    env_password_var: str | None = None
    env_keyfile_var: str | None = None


class ADBTransport(BaseModel):
    kind: Literal["adb"] = "adb"
    serial: str  # e.g. "10.0.1.51:5555" or "ABCD1234"


class NullTransport(BaseModel):
    """No shell target: back-office web portals with no physical device behind them."""

    kind: Literal["none"] = "none"


class BuildInfo(BaseModel):
    variant: str | None = None
    package: str | None = None
    version: str | None = None


class Device(BaseModel):
    id: str
    type: DeviceType
    os: OS
    ui: UIKind = UIKind.NONE
    transport: SSHTransport | ADBTransport | NullTransport = Field(discriminator="kind")
    build: BuildInfo | None = None
    web_ui_url: str | None = None
    # Name of an env var carrying the real URL, for portals where the URL itself
    # isn't known/committed yet. Mirrors SSHTransport.env_password_var — resolved
    # by WebUIDriver at start() time. web_ui_url wins if both are set.
    env_web_ui_url_var: str | None = None
    # Escape hatch for portals whose login form fields don't match WebUIDriver's
    # generic username/password selector guess, e.g. {"username": "#user",
    # "password": "#pass", "submit": "button[type=submit]"}.
    login_selectors: dict[str, str] | None = None
    appium_app_package: str | None = None
    # Identity fields the device sends to BOS (from backofficeagent.config.json).
    bos_device_id: str | None = None
    bos_device_type: str | None = None
    customer_code: str | None = None
    # Free-form per-device test metadata: operator_id, operator_pin, fixture
    # IDs, etc. Used by tests via `device.metadata.get(...)`. Keep secrets in
    # env vars referenced from here by name, not committed values.
    metadata: dict[str, Any] = Field(default_factory=dict)


class Project(BaseModel):
    project: str
    description: str = ""
    common_modules: list[str] = []
    bos_base_url: str | None = None
    identity_provider_uri: str | None = None
    comms_group_id: str | None = None
    devices: list[Device] = []
