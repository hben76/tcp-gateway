# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# api_status.py
#

"""
API status values.
"""

from enum import StrEnum


class ApiStatus(StrEnum):
    """
    API request status.
    """

    SUCCESS = "success"

    ERROR = "error"
