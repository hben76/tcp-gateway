# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# Request logging middleware
#

from time import perf_counter

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.logger import configure_logging

logger = configure_logging()


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Log every HTTP request.
    """

    async def dispatch(self, request: Request, call_next):

        start = perf_counter()

        response = await call_next(request)

        elapsed_ms = int((perf_counter() - start) * 1000)

        client_ip = "-"

        if request.client:
            client_ip = request.client.host

        logger.info(
            "request_id=%s source_ip=%s method=%s path=%s status=%d elapsed_ms=%d",
            getattr(request.state, "request_id", "-"),
            client_ip,
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )

        return response
