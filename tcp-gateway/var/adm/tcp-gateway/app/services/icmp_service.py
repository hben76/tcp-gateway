# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# icmp_service.py
#

"""
ICMP connectivity service.
"""

from __future__ import annotations

import re
import subprocess
from time import perf_counter

from app.models.icmp import IcmpCheckRequest, IcmpCheckResponse
from app.services.base_service import BaseConnectivityService


class IcmpService(BaseConnectivityService):
    """
    ICMP connectivity service.
    """

    def check(
        self,
        request: IcmpCheckRequest,
    ) -> IcmpCheckResponse:
        """
        Perform an ICMP connectivity check.

        Args:
            request:
                ICMP connectivity request.

        Returns:
            ICMP connectivity result.
        """

        start = perf_counter()

        try:
            result = subprocess.run(
                [
                    "ping",
                    "-c",
                    "1",
                    "-W",
                    str(request.timeout),
                    request.host,
                ],
                capture_output=True,
                text=True,
                timeout=request.timeout + 1,
            )

        except subprocess.TimeoutExpired:
            elapsed_ms = int((perf_counter() - start) * 1000)

            return IcmpCheckResponse(
                **self.timeout(
                    message="ICMP ping timed out.",
                    response_time_ms=elapsed_ms,
                ).model_dump()
            )

        except OSError:
            elapsed_ms = int((perf_counter() - start) * 1000)

            return IcmpCheckResponse(
                **self.unknown_error(
                    message="Unable to execute ping command.",
                    response_time_ms=elapsed_ms,
                ).model_dump()
            )

        elapsed_ms = int((perf_counter() - start) * 1000)

        if result.returncode != 0:
            return IcmpCheckResponse(
                **self.icmp_failed(
                    message="Host did not respond to ICMP ping.",
                    response_time_ms=elapsed_ms,
                ).model_dump()
            )

        response_time = elapsed_ms

        match = re.search(
            r"time=([0-9.]+)",
            result.stdout,
        )

        if match:
            response_time = int(float(match.group(1)))

        return IcmpCheckResponse(
            **self.success(
                message="ICMP ping successful.",
                response_time_ms=response_time,
            ).model_dump()
        )
