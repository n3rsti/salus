import sys
from pathlib import Path
from datetime import timedelta

# 1. Ustawienie ścieżek
root_path = Path(__file__).resolve().parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel, create_engine, Session, StaticPool, select
from main import app  

# 2. IMPORTUJEMY WSZYSTKIE MODELE - MUSZĄ BYĆ TU JAWNIE
from api.models.user_models import Users, Role
from api.models.activity_models import Activity, ActivityMedia
from api.models.program_models import Program, ProgramDay
from api.models.program_day_activities_link import ProgramDayActivityLink

from api.database import get_session
from api.security.jwt import create_access_token

# --- KONFIGURACJA ENGINE ---
sqlite_url = "sqlite://"
engine_test = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# --- DEPENDENCY OVERRIDE ---
def get_session_override():
    # Używamy tego samego engine_test
    with Session(engine_test) as session:
        yield session

app.dependency_overrides[get_session] = get_session_override

# --- FIXTURE PRZYGOTOWUJĄCE ---

@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    # WYMUSZENIE TWORZENIA TABEL
    # Sprawdzamy, czy tabele są w metadata przed stworzeniem
    print(f"\nDebug: Tabele wykryte w metadanych: {SQLModel.metadata.tables.keys()}")
    
    SQLModel.metadata.create_all(engine_test)
    
    with Session(engine_test) as session:
        # 1. Dodajemy rolę
        role = Role(id=1, name="user")
        session.add(role)
        session.commit()

        # 2. Dodajemy userów (muszą mieć role_id=1)
        user_a = Users(id=1, username="user_a", email="a@test.pl", role_id=1)
        user_b = Users(id=2, username="user_b", email="b@test.pl", role_id=1)
        session.add_all([user_a, user_b])
        session.commit()
    
    yield
    
    # Po teście czyścimy wszystko
    SQLModel.metadata.drop_all(engine_test)

@pytest.fixture
def token_user_a():
    return create_access_token(subject="1")

@pytest.fixture
def token_user_b():
    return create_access_token(subject="2")

# --- TEST ---

@pytest.mark.asyncio
async def test_activity_ownership_in_memory(token_user_a, token_user_b):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        
        # Payload zgodny z Twoim ActivityBase
        activity_data = {
            "name": "Testowa Aktywność",
            "duration_minutes": 10,
            "description": "Opis",
            "difficulty": 1,
            "image_url": "http://img.pl/1.jpg"
        }

        # 1. Tworzenie (User A)
        create_res = await ac.post(
            "/api/activities", 
            json=activity_data, 
            cookies={"access_token": token_user_a}
        )
        
        # Jeśli tu dostaniesz błąd 500, sprawdź logi w konsoli pod kątem "no such table"
        assert create_res.status_code == 200, f"Błąd POST: {create_res.text}"
        activity_id = create_res.json()["id"]

        # 2. Próba edycji (User B) -> 403
        edit_res = await ac.put(
            f"/api/activities/{activity_id}", 
            json={"name": "Evil Change"}, 
            cookies={"access_token": token_user_b}
        )
        assert edit_res.status_code == 403

        # 3. Poprawne usuwanie (User A)
        del_res = await ac.delete(
            f"/api/activities/{activity_id}", 
            cookies={"access_token": token_user_a}
        )
        assert del_res.status_code == 200