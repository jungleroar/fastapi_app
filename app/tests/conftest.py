import pytest
import json
import asyncio
from datetime import datetime
from sqlalchemy import insert
from app.database import Base, async_session_maker, engine
from app.config import settings
from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.main import app as fastapi_app
from sqlalchemy.exc import IntegrityError


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)
        
    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        try:
            add_hotels = insert(Hotels).values(hotels)
            add_rooms = insert(Rooms).values(rooms)
            add_users = insert(Users).values(users)
            add_bookings = insert(Bookings).values(bookings)

            await session.execute(add_hotels)
            await session.execute(add_rooms)
            await session.execute(add_users)
            await session.execute(add_bookings)

            await session.commit()
        except IntegrityError as e:
            print(f"IntegrityError при заполнении базы данных: {e}")
            await session.rollback()
            raise  # Re-raise the exception for pytest to catch
        except Exception as e:
            print(f"Ошибка при заполнении базы данных: {e}")
            await session.rollback()
            raise  # Re-raise the exception for pytest to catch


# @pytest.fixture(scope="session")
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("/auth/login", json={
            "email": "john.doe@example.com",
            "password": "hashed_password_1",
        })
        assert ac.cookies["booking_access_token"]
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
        