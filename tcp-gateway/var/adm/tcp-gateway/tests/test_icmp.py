# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# test_icmp.py
#

"""
ICMP API tests.
"""

from fastapi.testclient import TestClient


def test_icmp_check_success(client: TestClient) -> None:
    """
    Verify ICMP connectivity check.
    """

    response = client.post(
        "/v1/icmp/check",
        headers={
            "X-API-Key": "awx-secret-key",
        },
        json={
            "host": "8.8.8.8",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["reachable"] is True
    assert body["status"] == "success"


def test_icmp_check_missing_api_key(client: TestClient) -> None:
    """
    Verify ICMP API key protection.
    """

    response = client.post(
        "/v1/icmp/check",
        json={
            "host": "8.8.8.8",
        },
    )

    assert response.status_code == 401
