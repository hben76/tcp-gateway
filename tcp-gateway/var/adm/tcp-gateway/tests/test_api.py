from fastapi.testclient import TestClient


def test_api_discovery(client: TestClient) -> None:
    response = client.get("/api")

    assert response.status_code == 200
