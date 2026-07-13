# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# responses.py
#

"""
Common API response models.
"""

from typing import Any

from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    """
    Standard success response.
    """

    status: str = Field(
        default="success",
        description="Response status",
    )

    message: str = Field(
        ...,
        description="Human readable message.",
        examples=["Operation completed successfully"],
    )


class ErrorResponse(BaseModel):
    """
    Standard error response.
    """

    status: str = Field(
        default="error",
        description="Response status.",
    )

    code: int = Field(
        ...,
        description="HTTP status code.",
        examples=[401],
    )

    message: str = Field(
        ...,
        description="Human readable error message.",
        examples=["Missing X-API-Key header"],
    )

    request_id: str | None = Field(
        default=None,
        description="Unique request identifier.",
    )

    errors: list[Any] | None = Field(
        default=None,
        description="Validation errors.",
    )
