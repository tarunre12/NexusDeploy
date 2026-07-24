from app import app
import pytest

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health_status_code(client):
    res = client.get("/health")
    assert res.status_code == 200

def test_health_body(client):
    res = client.get("/health")
    assert res.get_json()["status"] == "healthy"

def test_api_status_code(client):
    res = client.get("/api")
    assert res.status_code == 200

def test_api_message(client):
    res = client.get("/api")
    assert "message" in res.get_json()

def test_404_route(client):
    res = client.get("/nonexistent")
    assert res.status_code == 404