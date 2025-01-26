from httpx import AsyncClient
from app.tests.conftest import ac
import pytest


@pytest.mark.parametrize("email, password, status_code", [
    ("kot@pes.com", "kotopes", 200),
    ("kot@pes.com", "kot0pes", 409),
    ("pes@kot.com", "pesokot", 200),
    ("abcde", "kotopes", 422)
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email, password, status_code", [
    ("john.doe@example.com", "hashed_password_1", 200),
    ("jane.smith@example.com", "hashed_password_2", 200),
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code
    