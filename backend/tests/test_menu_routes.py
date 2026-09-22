from tests.conftest import client

def test_create_menu_item(mock_user_header):
    response = client.post("/v1/menu/", json={"name": "testitem", "description": "test description", "price": 9.99}, headers=mock_user_header)
    print(response.json())
    assert response.status_code == 201