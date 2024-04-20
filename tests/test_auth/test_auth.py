import pytest
import sqlalchemy
from httpx import AsyncClient
from sqlalchemy import select

from services.authenticate.models import Role
from tests.conftest import async_session_factory
from contextlib import nullcontext as not_rais


class TestAuth:

    @staticmethod
    async def test_make_role():
        async with async_session_factory() as session:
            role_data = Role(role_name='user')
            session.add(role_data)
            await session.commit()

    @staticmethod
    async def test_check_role_table():
        async with async_session_factory() as session:
            query = await session.execute(select(Role))
            data = query.all()
            assert data[0][0].id == 1, data[0][0].role_name == 'user'

    @staticmethod
    @pytest.mark.parametrize("user_data, expectation", [
        ({"username": "Ivan", "email": "ivanemail@example.com", "password": "qwerty"}, not_rais()),
        ({"username": "John", "email": "john@example.com", "password": "password123"}, not_rais()),
        ({"username": "Kate", "email": "ivanemail@example.com", "password": "qwerty"},
         pytest.raises(sqlalchemy.exc.IntegrityError))])
    async def test_registration(ac: AsyncClient, user_data, expectation):
        with expectation:
            response = await ac.post('/auth/registration', json=user_data)
            assert response.status_code == 200

    @staticmethod
    @pytest.mark.parametrize('user_data', [
        ({"username": "Ivan", "password": "qwerty"}),
        ({"username": "Ivanya", "password": "qwertya"})
    ])
    async def test_login(ac: AsyncClient, user_data):
        response = await ac.post('/auth/login', json=user_data)
        if user_data["username"] == "Ivan":
            assert response.status_code == 200
            assert 'access_token' in response.cookies
        else:
            assert response.status_code == 401
            assert 'access_token' not in response.cookies
            assert response.json() == {'detail': 'Incorrect username or password'}

    @staticmethod
    async def test_user_with_auth(ac: AsyncClient):
        response = await ac.get('/auth/user')
        assert response.json() == {'username': 'Ivan', 'email': 'ivanemail@example.com', 'id': 1, 'role_id': 1}

    @staticmethod
    async def test_logout(ac: AsyncClient):
        response = await ac.post('/auth/logout')
        assert 'access_token' not in response.cookies
        assert response.json() == {'message': 'Successfully logged out'}

    @staticmethod
    async def test_user_without_auth(ac: AsyncClient):
        response = await ac.get('/auth/user')
        assert response.json() == {'detail': 'Sorry yours token not valid :('}
