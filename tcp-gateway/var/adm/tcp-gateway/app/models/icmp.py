# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# icmp.py
#

"""
ICMP request and response models.
"""

from pydantic import BaseModel, Field

from app.models.base import ConnectivityResponse


class IcmpCheckRequest(BaseModel):
    """
    ICMP connectivity check request.
    """

    host: str = Field(
        ...,
        description="Hostname or IP address.",
        examples=["8.8.8.8"],
    )

    timeout: int = Field(
        default=5,
        ge=1,
        le=300,
        description="Ping timeout in seconds.",
    )


class IcmpCheckResponse(ConnectivityResponse):
    """
    ICMP connectivity check response.
    """
