# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# constants.py
#

"""
Application-wide constants.

This module contains constants that are shared across the application.
Avoid hardcoding these values elsewhere.
"""

# ----------------------------------------------------------------------
# API
# ----------------------------------------------------------------------

API_VERSION = "v1"
API_PREFIX = f"/{API_VERSION}"

# ----------------------------------------------------------------------
# Headers
# ----------------------------------------------------------------------

API_KEY_HEADER = "X-API-Key"
REQUEST_ID_HEADER = "X-Request-ID"

# ----------------------------------------------------------------------
# TCP Defaults
# ----------------------------------------------------------------------

DEFAULT_TCP_TIMEOUT = 300
DEFAULT_POLL_INTERVAL = 2

# ----------------------------------------------------------------------
# HTTP Defaults
# ----------------------------------------------------------------------

DEFAULT_HTTP_TIMEOUT = 30

# ----------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------

DEFAULT_LOG_LEVEL = "INFO"
