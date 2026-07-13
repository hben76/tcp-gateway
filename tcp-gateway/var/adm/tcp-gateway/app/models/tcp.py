# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# tcp.py
#

"""
TCP request and response models.
"""

from pydantic import BaseModel, Field

from app.models.base import ConnectivityResponse


class TcpCheckRequest(BaseModel):
    """
    TCP connectivity check request.
    """

    host: str = Field(
        ...,
        description="Hostname or IP address.",
        examples=["127.0.0.1"],
    )

    port: int = Field(
        ...,
        ge=1,
        le=65535,
        description="TCP port.",
        examples=[22],
    )

    timeout: int | None = Field(
        default=None,
        ge=1,
        le=300,
        description="Connection timeout in seconds. Uses config default if omitted.",
    )


class TcpCheckResponse(ConnectivityResponse):
    """
    TCP connectivity check response.
    """


class TcpWaitRequest(BaseModel):
    """
    TCP wait request.
    """

    host: str = Field(
        ...,
        description="Hostname or IP address.",
        examples=["127.0.0.1"],
    )

    port: int = Field(
        ...,
        ge=1,
        le=65535,
        description="TCP port.",
        examples=[22],
    )

    timeout: int | None = Field(
        default=None,
        ge=1,
        le=3600,
        description="Maximum time to wait in seconds. Uses config default if omitted.",
    )

    interval: int | None = Field(
        default=None,
        ge=1,
        le=60,
        description="Polling interval in seconds. Uses config default if omitted.",
    )


class TcpWaitResponse(ConnectivityResponse):
    """
    TCP wait response.
    """

    elapsed_seconds: int = Field(
        description="Total wait time.",
        examples=[8],
    )
