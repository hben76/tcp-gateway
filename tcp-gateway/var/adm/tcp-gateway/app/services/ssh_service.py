# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# ssh_service.py
#

"""
SSH connectivity service.
"""

from __future__ import annotations

import socket
from time import perf_counter

from app.models.ssh import (
    SshCheckRequest,
    SshCheckResponse,
)


SSH_BANNER_PREFIX = "SSH-"
SSH_BANNER_MAX_SIZE = 255


class SshService:
    """
    SSH connectivity service.
    """

    @staticmethod
    def check(request: SshCheckRequest) -> SshCheckResponse:
        """
        Verify that an SSH service is responding.
        """

        start = perf_counter()

        try:
            with socket.create_connection(
                (request.host, request.port),
                timeout=request.timeout,
            ) as sock:

                banner = (
                    sock.makefile("rb")
                    .readline(SSH_BANNER_MAX_SIZE)
                    .decode("ascii", errors="replace")
                    .strip()
                )

        except socket.timeout:
            elapsed_ms = int((perf_counter() - start) * 1000)

            return SshCheckResponse(
                reachable=False,
                response_time_ms=elapsed_ms,
                message="Connection timed out.",
            )

        except ConnectionRefusedError:
            elapsed_ms = int((perf_counter() - start) * 1000)

            return SshCheckResponse(
                reachable=False,
                response_time_ms=elapsed_ms,
                message="Connection refused.",
            )

        except socket.gaierror:
            elapsed_ms = int((perf_counter() - start) * 1000)

            return SshCheckResponse(
                reachable=False,
                response_time_ms=elapsed_ms,
                message="Host not found.",
            )

        except OSError:
            elapsed_ms = int((perf_counter() - start) * 1000)

            return SshCheckResponse(
                reachable=False,
                response_time_ms=elapsed_ms,
                message="Unexpected operating system error.",
            )

        elapsed_ms = int((perf_counter() - start) * 1000)

        if not banner:
            return SshCheckResponse(
                reachable=False,
                response_time_ms=elapsed_ms,
                message="No SSH banner received.",
            )

        if not banner.startswith(SSH_BANNER_PREFIX):
            return SshCheckResponse(
                reachable=False,
                response_time_ms=elapsed_ms,
                message="Invalid SSH banner.",
            )

        return SshCheckResponse(
            reachable=True,
            response_time_ms=elapsed_ms,
            ssh_banner=banner,
        )
