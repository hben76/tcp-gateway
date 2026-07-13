# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
#

from fastapi.testclient import TestClient


def test_version(client: TestClient) -> None:
    """
    Verify the version endpoint.
    """

    response = client.get("/version")

    assert response.status_code == 200

    body = response.json()

    assert "version" in body
