# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# test_health.py
#

"""
Health endpoint tests.
"""

from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    """
    Verify the health endpoint.
    """

    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "UP"
