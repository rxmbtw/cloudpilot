from fastapi.testclient import TestClient
from app.main import app

def test_login_invalid_credentials():

    with TestClient(app) as client:

        response = client.post(
            "/login",
            json={
                "email": "fake@example.com",
                "password": "wrong"
            }
        )

        assert response.status_code == 401
