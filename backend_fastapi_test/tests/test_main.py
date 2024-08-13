from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_author():
    response = client.post("/authors/", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
