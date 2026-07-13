# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# result_reason.py
#

"""
Connectivity result reason codes.
"""

from enum import StrEnum


class ResultReason(StrEnum):
    """
    Machine-readable connectivity result codes.
    """

    SUCCESS = "success"

    TIMEOUT = "timeout"

    CONNECTION_REFUSED = "connection_refused"

    HOST_NOT_FOUND = "host_not_found"

    DNS_FAILURE = "dns_failure"

    NETWORK_UNREACHABLE = "network_unreachable"

    UNEXPECTED_STATUS = "unexpected_status"

    TLS_ERROR = "tls_error"

    INVALID_CERTIFICATE = "invalid_certificate"

    PERMISSION_DENIED = "permission_denied"

    UNKNOWN_ERROR = "unknown_error"

    ICMP_FAILED = "icmp_failed"
