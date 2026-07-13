# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# http.py
#

"""
HTTP request and response models.
"""

from pydantic import BaseModel, Field, HttpUrl

from app.models.base import ConnectivityResponse


class HttpCheckRequest(BaseModel):
    """
    HTTP connectivity check request.
    """

    url: HttpUrl = Field(
        ...,
        description="HTTP or HTTPS URL to check.",
        examples=["https://example.com"],
    )

    timeout: int = Field(
        default=10,
        ge=1,
        le=300,
        description="Connection timeout in seconds.",
    )

    expected_status: int = Field(
        default=200,
        ge=100,
        le=599,
        description="Expected HTTP status code.",
    )

    follow_redirects: bool = Field(
        default=True,
        description="Follow HTTP redirects.",
    )


class HttpCheckResponse(ConnectivityResponse):
    """
    HTTP connectivity check response.
    """

    status_code: int | None = Field(
        default=None,
        description="HTTP status code returned by the server.",
        examples=[200],
    )


class HttpWaitRequest(BaseModel):
    """
    HTTP wait request.
    """

    url: HttpUrl = Field(
        ...,
        description="HTTP or HTTPS URL to wait for.",
        examples=["https://example.com"],
    )

    timeout: int = Field(
        default=300,
        ge=1,
        le=3600,
        description="Maximum time to wait in seconds.",
    )

    interval: int = Field(
        default=2,
        ge=1,
        le=60,
        description="Polling interval in seconds.",
    )

    expected_status: int = Field(
        default=200,
        ge=100,
        le=599,
        description="Expected HTTP status code.",
    )

    follow_redirects: bool = Field(
        default=True,
        description="Follow HTTP redirects.",
    )


class HttpWaitResponse(ConnectivityResponse):
    """
    HTTP wait response.
    """

    status_code: int | None = Field(
        default=None,
        description="Last HTTP status code received.",
        examples=[200],
    )

    elapsed_seconds: int = Field(
        description="Time spent waiting.",
        examples=[18],
    )
