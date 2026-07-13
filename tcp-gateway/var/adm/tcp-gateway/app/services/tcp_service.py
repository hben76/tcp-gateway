# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# tcp_service.py
#

"""
TCP connectivity service.
"""

from __future__ import annotations

import socket
from time import perf_counter, sleep

from app.config import config
from app.models.tcp import (
    TcpCheckRequest,
    TcpCheckResponse,
    TcpWaitRequest,
    TcpWaitResponse,
)
from app.services.base_service import BaseConnectivityService


class TcpService(BaseConnectivityService):
    """
    TCP connectivity service.
    """

    def check(self, request: TcpCheckRequest) -> TcpCheckResponse:
        """
        Perform a TCP connectivity check.

        Args:
            request:
                TCP connectivity check request.

        Returns:
            TCP connectivity result.
        """

        start = perf_counter()

        timeout = (
            request.timeout
            if request.timeout is not None
            else config.tcp.default_timeout
        )

        try:
            with socket.create_connection(
                (request.host, request.port),
                timeout=timeout,
            ):
                elapsed_ms = int((perf_counter() - start) * 1000)

                return TcpCheckResponse(
                    **self.success(
                        message="TCP connection established successfully.",
                        response_time_ms=elapsed_ms,
                    ).model_dump()
                )

        except socket.timeout:
            elapsed_ms = int((perf_counter() - start) * 1000)

            return TcpCheckResponse(
                **self.timeout(
                    message="TCP connection timed out.",
                    response_time_ms=elapsed_ms,
                ).model_dump()
            )

        except ConnectionRefusedError:
            elapsed_ms = int((perf_counter() - start) * 1000)

            return TcpCheckResponse(
                **self.connection_refused(
                    message="The remote host refused the TCP connection.",
                    response_time_ms=elapsed_ms,
                ).model_dump()
            )

        except socket.gaierror:
            elapsed_ms = int((perf_counter() - start) * 1000)

            return TcpCheckResponse(
                **self.host_not_found(
                    message="Unable to resolve hostname.",
                    response_time_ms=elapsed_ms,
                ).model_dump()
            )

        except PermissionError:
            elapsed_ms = int((perf_counter() - start) * 1000)

            return TcpCheckResponse(
                **self.permission_denied(
                    message="Permission denied while creating TCP connection.",
                    response_time_ms=elapsed_ms,
                ).model_dump()
            )

        except OSError:
            elapsed_ms = int((perf_counter() - start) * 1000)

            return TcpCheckResponse(
                **self.unknown_error(
                    message="Unexpected operating system error.",
                    response_time_ms=elapsed_ms,
                ).model_dump()
            )

    def wait(self, request: TcpWaitRequest) -> TcpWaitResponse:
        """
        Wait until the TCP endpoint becomes reachable.

        Args:
            request:
                TCP wait request.

        Returns:
            TCP wait result.
        """

        start = perf_counter()

        timeout = (
            request.timeout
            if request.timeout is not None
            else config.tcp.default_timeout
        )

        interval = (
            request.interval
            if request.interval is not None
            else config.tcp.poll_interval
        )

        while True:
            result = self.check(
                TcpCheckRequest(
                    host=request.host,
                    port=request.port,
                    timeout=timeout,
                )
            )

            elapsed_seconds = int(perf_counter() - start)

            if result.reachable:
                return TcpWaitResponse(
                    **result.model_dump(),
                    elapsed_seconds=elapsed_seconds,
                )

            if elapsed_seconds >= timeout:
                return TcpWaitResponse(
                    **result.model_dump(),
                    elapsed_seconds=elapsed_seconds,
                )

            sleep(interval)
