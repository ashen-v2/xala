from tests.conftest import client
import models

def test_health_check():
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_user(send_email_mock):
    response = client.post("/v1/users/", json={"name": "testuser","store_name": "teststore", "email": "testuser@example.com", "password": "testpassword"})
    print(response.json())
    assert response.status_code == 201

def test_login_user(mock_user_create):
    response = client.post("/v1/users/login", data={"username": "testuser0@example.com", "password": "testpassword"})
    print(response.json())
    assert response.status_code == 200

def test_update_me(mock_user_header):
    response = client.patch("/v1/users/me", json={"store_name": "updatedstore"}, headers=mock_user_header)
    print(response.json())
    assert response.status_code == 200


