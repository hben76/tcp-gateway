# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# test_tcp.py
#

"""
TCP API tests.
"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_tcp_check_success() -> None:
    """
    Verify TCP connectivity check endpoint.
    """

    response = client.post(
        "/v1/tcp/check",
        headers={
            "X-API-Key": "awx-secret-key",
        },
        json={
            "host": "google.com",
            "port": 443,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["reachable"] is True
    assert body["status"] == "success"


def test_tcp_check_invalid_port() -> None:
    """
    Verify TCP port validation.
    """

    response = client.post(
        "/v1/tcp/check",
        headers={
            "X-API-Key": "awx-secret-key",
        },
        json={
            "host": "google.com",
            "port": 70000,
        },
    )

    assert response.status_code == 422


def test_tcp_check_missing_api_key() -> None:
    """
    Verify API key protection.
    """

    response = client.post(
        "/v1/tcp/check",
        json={
            "host": "google.com",
            "port": 443,
        },
    )

    assert response.status_code == 401
