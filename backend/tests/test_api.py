from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_returns_healthy() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_chat_endpoint_returns_answer_shape() -> None:
    response = client.post(
        "/chat",
        json={"question": "What is the purpose of this project?"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert "answer" in payload
