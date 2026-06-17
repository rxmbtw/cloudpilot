from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():

    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code in [200, 201]
