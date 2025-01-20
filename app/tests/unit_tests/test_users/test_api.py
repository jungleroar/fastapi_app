from httpx import AsyncClient
from app.tests.conftest import ac
import pytest


@pytest.mark.asyncio
async def test_register_user(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": "kot@pes.com",
        "password": "kotopes",
    })

    assert response.status_code == 200
