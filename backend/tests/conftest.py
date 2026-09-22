from urllib import response

import pytest
from main import app
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from db.session import get_session

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def test_get_session():
    test_engine = create_engine("sqlite:///test.db", echo=True, connect_args={"check_same_thread": False})

    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session

    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture(autouse=True)
def override_get_session(test_get_session):
    def _override_get_session():
        yield test_get_session

    app.dependency_overrides[get_session] = _override_get_session


@pytest.fixture(scope="function")
def send_email_mock(monkeypatch):
    def fake_send_email(to_email: str, subject: str, html_content: str, text_content: str = ""):
        pass  # Do nothing, just simulate sending an email

    monkeypatch.setattr("integrations.mailtrap.mailtrap_client.send_email", fake_send_email)

@pytest.fixture(scope="function")
def mock_user_create(send_email_mock):
    response = client.post("/v1/users/", json={"name": "testuser0","store_name": "teststore0", "email": "testuser0@example.com", "password": "testpassword"})
    assert response.status_code == 201
    return response.json()

@pytest.fixture(scope="function")
def mock_user_login(mock_user_create):       
    response = client.post("/v1/users/login", data={"username":"testuser0@example.com" , "password": "testpassword"})
    assert response.status_code == 200
    return response.json().get("access_token")

@pytest.fixture(scope="function")
def mock_user_header(mock_user_login):
    return {"Authorization": f"Bearer {mock_user_login}"}


    


