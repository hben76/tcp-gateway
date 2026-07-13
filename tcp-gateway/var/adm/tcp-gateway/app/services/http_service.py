# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# http_service.py
#

"""
HTTP connectivity service.
"""

from __future__ import annotations

from time import perf_counter, sleep

import httpx

from app.models.http import (
    HttpCheckRequest,
    HttpCheckResponse,
    HttpWaitRequest,
    HttpWaitResponse,
)
from app.services.base_service import BaseConnectivityService


class HttpService(BaseConnectivityService):
    """
    HTTP connectivity service.
    """

    def check(
        self,
        request: HttpCheckRequest,
    ) -> HttpCheckResponse:
        """
        Perform an HTTP connectivity check.

        Args:
            request:
                HTTP connectivity request.

        Returns:
            HTTP connectivity result.
        """

        start = perf_counter()

        try:
            with httpx.Client(
                timeout=request.timeout,
                follow_redirects=request.follow_redirects,
            ) as client:
                response = client.get(str(request.url))

            elapsed_ms = int((perf_counter() - start) * 1000)

            if response.status_code == request.expected_status:
                return HttpCheckResponse(
                    status=self.success(
                        message="HTTP endpoint returned expected status.",
                        response_time_ms=elapsed_ms,
                    ).status,
                    reachable=True,
                    reason=self.success(
                        message="HTTP endpoint returned expected status.",
                        response_time_ms=elapsed_ms,
                    ).reason,
                    message="HTTP endpoint returned expected status.",
                    response_time_ms=elapsed_ms,
                    status_code=response.status_code,
                )

            return HttpCheckResponse(
                **self.unexpected_status(
                    message=(f"Unexpected HTTP status code {response.status_code}."),
                    response_time_ms=elapsed_ms,
                ).model_dump(),
                status_code=response.status_code,
            )

        except httpx.ConnectTimeout:
            elapsed_ms = int((perf_counter() - start) * 1000)

            return HttpCheckResponse(
                **self.timeout(
                    message="HTTP connection timed out.",
                    response_time_ms=elapsed_ms,
                ).model_dump(),
                status_code=None,
            )

        except httpx.ConnectError:
            elapsed_ms = int((perf_counter() - start) * 1000)

            return HttpCheckResponse(
                **self.unknown_error(
                    message="Unable to connect to HTTP endpoint.",
                    response_time_ms=elapsed_ms,
                ).model_dump(),
                status_code=None,
            )

        except httpx.HTTPError:
            elapsed_ms = int((perf_counter() - start) * 1000)

            return HttpCheckResponse(
                **self.unknown_error(
                    message="Unexpected HTTP client error.",
                    response_time_ms=elapsed_ms,
                ).model_dump(),
                status_code=None,
            )

    def wait(
        self,
        request: HttpWaitRequest,
    ) -> HttpWaitResponse:
        """
        Wait until an HTTP endpoint becomes available.

        Args:
            request:
                HTTP wait request.

        Returns:
            HTTP wait result.
        """

        start = perf_counter()

        while True:
            check = self.check(
                HttpCheckRequest(
                    url=request.url,
                    timeout=request.timeout,
                    expected_status=request.expected_status,
                    follow_redirects=request.follow_redirects,
                )
            )

            elapsed_seconds = int(perf_counter() - start)

            if check.reachable:
                return HttpWaitResponse(
                    **check.model_dump(),
                    elapsed_seconds=elapsed_seconds,
                )

            if elapsed_seconds >= request.timeout:
                return HttpWaitResponse(
                    **check.model_dump(),
                    elapsed_seconds=elapsed_seconds,
                )

            sleep(request.interval)
