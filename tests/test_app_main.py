from http import HTTPStatus


def test_hello_world(client):
    response = client.get('/')  # Act (Ação)
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}
