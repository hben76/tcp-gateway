# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# base.py
#

"""
Shared response models.
"""

from pydantic import BaseModel, Field

from app.models.result_reason import ResultReason


class ConnectivityResponse(BaseModel):
    """
    Base response for all connectivity operations.
    """

    status: str = Field(
        description="API request status.",
        examples=["success"],
    )

    reachable: bool = Field(
        description="Whether the target is reachable.",
    )

    reason: ResultReason = Field(
        description="Machine-readable reason code.",
        examples=["success"],
    )

    message: str = Field(
        description="Human-readable message.",
        examples=["TCP connection established successfully."],
    )

    response_time_ms: int | None = Field(
        default=None,
        description="Response time in milliseconds.",
        examples=[14],
    )
