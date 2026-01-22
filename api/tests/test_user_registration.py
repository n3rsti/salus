import sys
from pathlib import Path

# add project root to python path
root_path = Path(__file__).resolve().parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

import pytest
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel, Session, create_engine, StaticPool

from main import app
from api.database import get_session


# Test database (in-memory)
engine_test = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def get_session_override():
    with Session(engine_test) as session:
        yield session


app.dependency_overrides[get_session] = get_session_override


@pytest.fixture(autouse=True)
def setup_db():
    SQLModel.metadata.create_all(engine_test)
    yield
    SQLModel.metadata.drop_all(engine_test)


@pytest.mark.asyncio
async def test_register_user_success():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:

        res = await ac.post(
            "/api/users",
            json={
                "username": "new_user",
                "email": "new@test.pl",
                "password": "StrongPass123*",
                "role_id": 1,
            },
        )

        assert res.status_code == 201
        assert "id" in res.json()


@pytest.mark.asyncio
async def test_register_user_duplicate_email():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:

        await ac.post(
            "/api/users",
            json={
                "username": "user1",
                "email": "dup@test.pl",
                "password": "Password123*",
                "role_id": 1,
            },
        )

        res = await ac.post(
            "/api/users",
            json={
                "username": "user2",
                "email": "dup@test.pl",
                "password": "Password123*",
                "role_id": 1,
            },
        )

        assert res.status_code == 409
