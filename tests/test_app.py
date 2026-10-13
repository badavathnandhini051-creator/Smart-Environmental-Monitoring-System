from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_reading_has_expected_fields():
    response = client.get("/api/reading")
    assert response.status_code == 200
    data = response.json()
    assert "temperature_c" in data
    assert "humidity_percent" in data
    assert "alerts" in data

def test_submit_reading_and_alert():
    response = client.post("/api/reading", json={
        "temperature_c": 40,
        "humidity_percent": 80,
        "source": "test"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["source"] == "test"
    assert any("High temperature" in message for message in data["alerts"])
    assert any("High humidity" in message for message in data["alerts"])

def test_invalid_humidity_is_rejected():
    response = client.post("/api/reading", json={
        "temperature_c": 25,
        "humidity_percent": 150,
        "source": "test"
    })
    assert response.status_code == 422

def test_thresholds_can_be_updated():
    response = client.put("/api/thresholds", json={
        "temperature_max_c": 30,
        "humidity_max_percent": 65
    })
    assert response.status_code == 200
    assert response.json()["temperature_max_c"] == 30
    assert response.json()["humidity_max_percent"] == 65
