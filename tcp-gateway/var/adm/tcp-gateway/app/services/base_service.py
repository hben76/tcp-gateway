# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# base_service.py
#

"""
Base service for all connectivity services.
"""

from __future__ import annotations

from app.models.api_status import ApiStatus
from app.models.base import ConnectivityResponse
from app.models.result_reason import ResultReason


class BaseConnectivityService:
    """
    Base class for all connectivity services.

    Provides helper methods for creating consistent API responses.
    """

    @staticmethod
    def _response(
        *,
        reachable: bool,
        reason: ResultReason,
        message: str,
        response_time_ms: int | None = None,
    ) -> ConnectivityResponse:
        """
        Create a standard connectivity response.
        """

        return ConnectivityResponse(
            status=ApiStatus.SUCCESS,
            reachable=reachable,
            reason=reason,
            message=message,
            response_time_ms=response_time_ms,
        )

    @classmethod
    def success(
        cls,
        *,
        message: str,
        response_time_ms: int | None = None,
    ) -> ConnectivityResponse:
        """
        Successful connectivity check.
        """

        return cls._response(
            reachable=True,
            reason=ResultReason.SUCCESS,
            message=message,
            response_time_ms=response_time_ms,
        )

    @classmethod
    def timeout(
        cls,
        *,
        message: str,
        response_time_ms: int | None = None,
    ) -> ConnectivityResponse:
        """
        Connectivity timeout.
        """

        return cls._response(
            reachable=False,
            reason=ResultReason.TIMEOUT,
            message=message,
            response_time_ms=response_time_ms,
        )

    @classmethod
    def connection_refused(
        cls,
        *,
        message: str,
        response_time_ms: int | None = None,
    ) -> ConnectivityResponse:
        """
        Connection refused.
        """

        return cls._response(
            reachable=False,
            reason=ResultReason.CONNECTION_REFUSED,
            message=message,
            response_time_ms=response_time_ms,
        )

    @classmethod
    def host_not_found(
        cls,
        *,
        message: str,
        response_time_ms: int | None = None,
    ) -> ConnectivityResponse:
        """
        Hostname could not be resolved.
        """

        return cls._response(
            reachable=False,
            reason=ResultReason.HOST_NOT_FOUND,
            message=message,
            response_time_ms=response_time_ms,
        )

    @classmethod
    def dns_failure(
        cls,
        *,
        message: str,
        response_time_ms: int | None = None,
    ) -> ConnectivityResponse:
        """
        DNS lookup failed.
        """

        return cls._response(
            reachable=False,
            reason=ResultReason.DNS_FAILURE,
            message=message,
            response_time_ms=response_time_ms,
        )

    @classmethod
    def network_unreachable(
        cls,
        *,
        message: str,
        response_time_ms: int | None = None,
    ) -> ConnectivityResponse:
        """
        Network is unreachable.
        """

        return cls._response(
            reachable=False,
            reason=ResultReason.NETWORK_UNREACHABLE,
            message=message,
            response_time_ms=response_time_ms,
        )

    @classmethod
    def icmp_failed(
        cls,
        *,
        message: str,
        response_time_ms: int | None = None,
    ) -> ConnectivityResponse:
        """
        ICMP echo request failed.
        """

        return cls._response(
            reachable=False,
            reason=ResultReason.ICMP_FAILED,
            message=message,
            response_time_ms=response_time_ms,
        )

    @classmethod
    def permission_denied(
        cls,
        *,
        message: str,
        response_time_ms: int | None = None,
    ) -> ConnectivityResponse:
        """
        Permission denied.
        """

        return cls._response(
            reachable=False,
            reason=ResultReason.PERMISSION_DENIED,
            message=message,
            response_time_ms=response_time_ms,
        )

    @classmethod
    def unexpected_status(
        cls,
        *,
        message: str,
        response_time_ms: int | None = None,
    ) -> ConnectivityResponse:
        """
        Unexpected protocol response.
        """

        return cls._response(
            reachable=False,
            reason=ResultReason.UNEXPECTED_STATUS,
            message=message,
            response_time_ms=response_time_ms,
        )

    @classmethod
    def tls_error(
        cls,
        *,
        message: str,
        response_time_ms: int | None = None,
    ) -> ConnectivityResponse:
        """
        TLS validation error.
        """

        return cls._response(
            reachable=False,
            reason=ResultReason.TLS_ERROR,
            message=message,
            response_time_ms=response_time_ms,
        )

    @classmethod
    def unknown_error(
        cls,
        *,
        message: str,
        response_time_ms: int | None = None,
    ) -> ConnectivityResponse:
        """
        Unexpected error.
        """

        return cls._response(
            reachable=False,
            reason=ResultReason.UNKNOWN_ERROR,
            message=message,
            response_time_ms=response_time_ms,
        )
