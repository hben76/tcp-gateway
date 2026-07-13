# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# statistics.py
#

"""
Runtime statistics models.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class GatewayStatus(str, Enum):
    """Gateway status."""

    UP = "UP"
    DOWN = "DOWN"


class RequestStatistics(BaseModel):
    """Request statistics."""

    model_config = ConfigDict(frozen=True)

    total: int = Field(
        ge=0,
        description="Total number of processed requests.",
    )

    active: int = Field(
        ge=0,
        description="Currently active requests.",
    )


class ConnectivityStatistics(BaseModel):
    """Connectivity statistics."""

    model_config = ConfigDict(frozen=True)

    reachable: int = Field(
        ge=0,
        description="Number of successful connectivity checks.",
    )

    unreachable: int = Field(
        ge=0,
        description="Number of unsuccessful connectivity checks.",
    )


class StatisticsResponse(BaseModel):
    """Gateway runtime statistics response."""

    model_config = ConfigDict(frozen=True)

    status: GatewayStatus = Field(
        default=GatewayStatus.UP,
        description="Gateway status.",
    )

    version: str = Field(
        description="TCP Gateway version.",
    )

    uptime_seconds: int = Field(
        ge=0,
        description="Gateway uptime in seconds.",
    )

    requests: RequestStatistics = Field(
        description="Request statistics.",
    )

    connectivity: ConnectivityStatistics = Field(
        description="Connectivity statistics.",
    )
