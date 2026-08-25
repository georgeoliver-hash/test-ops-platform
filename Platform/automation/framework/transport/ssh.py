from __future__ import annotations

import os

from ..registry.models import SSHTransport as SSHConfig
from .base import CommandResult, Transport

try:
    import paramiko
except ImportError:
    paramiko = None  # type: ignore[assignment]


class SSHTransportImpl(Transport):
    def __init__(self, config: SSHConfig):
        if paramiko is None:
            raise RuntimeError("paramiko not installed; run: pip install -e .[ssh]")
        self.config = config
        self._client: paramiko.SSHClient | None = None

    def connect(self) -> None:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        password = (
            os.getenv(self.config.env_password_var)
            if self.config.env_password_var
            else None
        )
        keyfile = (
            os.getenv(self.config.env_keyfile_var)
            if self.config.env_keyfile_var
            else None
        )
        client.connect(
            hostname=self.config.host,
            port=self.config.port,
            username=self.config.user,
            password=password,
            key_filename=keyfile,
            timeout=10,
        )
        self._client = client

    def disconnect(self) -> None:
        if self._client:
            self._client.close()
            self._client = None

    def run(self, command: str, timeout: float = 30.0) -> CommandResult:
        if not self._client:
            raise RuntimeError("Not connected")
        _, stdout, stderr = self._client.exec_command(command, timeout=timeout)
        exit_code = stdout.channel.recv_exit_status()
        return CommandResult(
            exit_code=exit_code,
            stdout=stdout.read().decode(errors="replace"),
            stderr=stderr.read().decode(errors="replace"),
        )

    def push(self, local: str, remote: str) -> None:
        if not self._client:
            raise RuntimeError("Not connected")
        sftp = self._client.open_sftp()
        try:
            sftp.put(local, remote)
        finally:
            sftp.close()

    def pull(self, remote: str, local: str) -> None:
        if not self._client:
            raise RuntimeError("Not connected")
        sftp = self._client.open_sftp()
        try:
            sftp.get(remote, local)
        finally:
            sftp.close()
