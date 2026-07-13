# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# ssh.py
#

"""
SSH request and response models.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


DEFAULT_SSH_PORT = 22
DEFAULT_TIMEOUT = 5


class SshCheckRequest(BaseModel):
    """
    SSH connectivity check request.
    """

    host: str = Field(
        ...,
        description="Target hostname or IP address.",
        examples=["192.168.1.10", "server.example.com"],
    )

    port: int = Field(
        default=DEFAULT_SSH_PORT,
        ge=1,
        le=65535,
        description="Target SSH port.",
    )

    timeout: int = Field(
        default=DEFAULT_TIMEOUT,
        ge=1,
        le=300,
        description="Connection timeout in seconds.",
    )


class SshCheckResponse(BaseModel):
    """
    SSH connectivity check response.
    """

    reachable: bool = Field(
        ...,
        description="SSH server responded successfully.",
    )

    response_time_ms: int = Field(
        ...,
        ge=0,
        description="Response time in milliseconds.",
    )

    ssh_banner: str | None = Field(
        default=None,
        description="SSH identification banner returned by the server.",
    )

    message: str | None = Field(
        default=None,
        description="Status or error message.",
    )
