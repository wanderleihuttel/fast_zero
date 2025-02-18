from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'test',
            'email': 'test@test.com',
            'password': 'test123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 2,
        'username': 'test',
        'email': 'test@test.com',
    }


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission!'}


def test_create_user_username_already_exist(client, user):
    response = client.post(
        '/users',
        json={
            'username': user.username,
            'email': 'other@test.com',
            'password': 'test123',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists!'}


def test_create_user_email_already_exist(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'test_new',
            'email': user.email,
            'password': 'test123',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists!'}


def test_list_all_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_list_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_list_single_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_list_single_user_not_found(client):
    response = client.get('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'id': 1,
            'username': 'test2',
            'email': 'test2@test.com',
            'password': 'test123',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'test2',
        'email': 'test2@test.com',
    }


def test_update_user_not_found(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'id': f'{other_user}',
            'username': 'test2',
            'email': 'teste2@test.com',
            'password': 'test123',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission!'}


def test_delete_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission!'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted!'}
