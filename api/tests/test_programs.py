import sys
from pathlib import Path
from datetime import timedelta

root_path = Path(__file__).resolve().parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlmodel import (
    SQLModel,
    create_engine,
    Session,
    StaticPool,
)  # Ważny import StaticPool
from main import app

from api.models.user_models import Users, Role
from api.models.program_models import Program, ProgramDay
from api.models.program_day_activities_link import ProgramDayActivityLink
from api.models.programs_tags_link import ProgramTagLink
from api.database import get_session
from api.security.jwt import create_access_token

sqlite_url = "sqlite://"
engine_test = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def get_session_override():
    with Session(engine_test) as session:
        yield session


app.dependency_overrides[get_session] = get_session_override


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    SQLModel.metadata.create_all(engine_test)

    with Session(engine_test) as session:
        role = Role(id=1, name="user")
        user_a = Users(id=1, username="user_a", email="a@test.pl", role_id=1)
        user_b = Users(id=2, username="user_b", email="b@test.pl", role_id=1)
        session.add_all([role, user_a, user_b])
        session.commit()

    yield

    SQLModel.metadata.drop_all(engine_test)


@pytest.fixture
def token_user_a():
    return create_access_token(subject="1")


@pytest.fixture
def token_user_b():
    return create_access_token(subject="2")


@pytest.mark.asyncio
async def test_program_ownership_in_memory(token_user_a, token_user_b):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:

        create_res = await ac.post(
            "/api/programs",
            json={
                "name": "Memory Program",
                "duration_days": 1,
                "description": "Test",
                "language": "pl",
                "image_url": "http://img.pl",
            },
            cookies={"access_token": token_user_a},
        )

        assert create_res.status_code == 200, f"Błąd: {create_res.text}"
        prog_id = create_res.json()["id"]

        edit_res = await ac.put(
            f"/api/programs/{prog_id}",
            json={"name": "Evil Change"},
            cookies={"access_token": token_user_b},
        )

        assert edit_res.status_code == 403
        assert (
            edit_res.json()["detail"] == "Not enough permissions to edit this program"
        )

        delete_res = await ac.delete(
            f"/api/programs/{prog_id}", cookies={"access_token": token_user_a}
        )
        assert delete_res.status_code == 200
