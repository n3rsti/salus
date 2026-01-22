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
from api.models.user_models import Users
from api.security.crypto import hash_password


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
async def test_login_existing_user():
    with Session(engine_test) as session:
        user = Users(
            username="testuser",
            email="testuser@email.hr",
            password=hash_password("correct_password"),
            role_id=1,
        )
        session.add(user)
        session.commit()

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:

        res = await ac.post(
            "/api/auth/login",
            json={
                "username_or_email": "testuser@email.hr",
                "password": "correct_password",
            },
        )

        assert res.status_code == 200
        body = res.json()
        assert "user" in body
        assert body["user"]["username"] == "testuser"


@pytest.mark.asyncio
async def test_login_nonexisting_user():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:

        res = await ac.post(
            "/api/auth/login",
            json={
                "username_or_email": "nonexisting@email.hr",
                "password": "nonexisting",
            },
        )

        assert res.status_code == 401
        assert "detail" in res.json()
