# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# statistics_service.py
#

"""
Runtime statistics service.
"""

from __future__ import annotations

from threading import Lock
from time import monotonic

from app.models.statistics import (
    ConnectivityStatistics,
    RequestStatistics,
    StatisticsResponse,
)
from app.version import __version__


class StatisticsService:
    """Runtime statistics service."""

    def __init__(self) -> None:
        self._lock = Lock()

        self._start_time = monotonic()

        self._total_requests = 0
        self._active_requests = 0

        self._reachable = 0
        self._unreachable = 0

    def request_started(self) -> None:
        """Record the start of a request."""

        with self._lock:
            self._total_requests += 1
            self._active_requests += 1

    def request_finished(self) -> None:
        """Record the completion of a request."""

        with self._lock:
            if self._active_requests > 0:
                self._active_requests -= 1

    def record_check(self, reachable: bool) -> None:
        """Record the result of a connectivity check."""

        with self._lock:
            if reachable:
                self._reachable += 1
            else:
                self._unreachable += 1

    def snapshot(self) -> StatisticsResponse:
        """Return a snapshot of the current runtime statistics."""

        with self._lock:
            return StatisticsResponse(
                version=__version__,
                uptime_seconds=int(monotonic() - self._start_time),
                requests=RequestStatistics(
                    total=self._total_requests,
                    active=self._active_requests,
                ),
                connectivity=ConnectivityStatistics(
                    reachable=self._reachable,
                    unreachable=self._unreachable,
                ),
            )

    def reset(self) -> None:
        """Reset all runtime statistics."""

        with self._lock:
            self._start_time = monotonic()

            self._total_requests = 0
            self._active_requests = 0

            self._reachable = 0
            self._unreachable = 0


statistics_service = StatisticsService()
