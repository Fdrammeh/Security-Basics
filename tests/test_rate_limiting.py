
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_items_rate_limit():
    # Requests 1–60 should succeed.
    for _ in range(60):
        response = client.get("/items/")
        assert response.status_code == 200

    # Request 61 should be rate-limited.
    response = client.get("/items/")
    assert response.status_code == 429


def test_create_item_rate_limit():
    payload = {
        "name": "Test item",
        "description": "Testing rate limits"
    }

    # Requests 1–20 should succeed.
    for _ in range(20):
        response = client.post("/items/", json=payload)
        assert response.status_code == 200

    # Request 21 should be rate-limited.
    response = client.post("/items/", json=payload)
    assert response.status_code == 429
