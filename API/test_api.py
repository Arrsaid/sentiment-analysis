from fastapi.testclient import TestClient
from API.api import app

client = TestClient(app)


def test_predict():
    with TestClient(app) as client:
        response1 = client.post(
            "/predict", json={"text": "I love flying with air paradis!"}
        )
        assert response1.status_code == 200
        data = response1.json()
        assert "sentiment" in data
        assert data["sentiment"] == "positif"
        assert "confidence" in data
        assert 0 <= data["confidence"] <= 1
        response2 = client.post(
            "/predict", json={"text": "Bad experience! this is the worst airline ever!"}
        )
        assert response2.status_code == 200
        data = response2.json()
        assert "sentiment" in data
        assert data["sentiment"] == "négatif"
        assert "confidence" in data
        assert 0 <= data["confidence"] <= 1
