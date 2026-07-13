# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# common.py
#

from typing import Any

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """
    Standard error response returned by the API.
    """

    status: str = Field(
        default="error",
        description="Response status",
    )

    code: int = Field(
        ...,
        description="HTTP status code",
        examples=[401],
    )

    message: str = Field(
        ...,
        description="Human readable error message",
        examples=["Missing X-API-Key header"],
    )

    request_id: str | None = Field(
        default=None,
        description="Request correlation ID",
    )

    errors: list[Any] | None = Field(
        default=None,
        description="Validation errors",
    )


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
        description="Operation result",
        examples=["Operation completed successfully"],
    )
