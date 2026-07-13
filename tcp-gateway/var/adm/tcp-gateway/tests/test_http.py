# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# test_http.py
#

"""
HTTP API tests.
"""

from fastapi.testclient import TestClient


def test_http_check_success(client: TestClient) -> None:
    """
    Verify HTTP connectivity check.
    """

    response = client.post(
        "/v1/http/check",
        headers={
            "X-API-Key": "awx-secret-key",
        },
        json={
            "url": "https://www.google.com",
            "expected_status": 200,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["reachable"] is True
    assert body["status"] == "success"
    assert body["status_code"] == 200


def test_http_check_wrong_status(client: TestClient) -> None:
    """
    Verify unexpected HTTP status handling.
    """

    response = client.post(
        "/v1/http/check",
        headers={
            "X-API-Key": "awx-secret-key",
        },
        json={
            "url": "https://www.google.com",
            "expected_status": 404,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["reachable"] is False
    assert body["reason"] == "unexpected_status"


def test_http_check_missing_api_key(client: TestClient) -> None:
    """
    Verify HTTP API key protection.
    """

    response = client.post(
        "/v1/http/check",
        json={
            "url": "https://www.google.com",
        },
    )

    assert response.status_code == 401
