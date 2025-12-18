import sys
from pathlib import Path
from datetime import timedelta

# Ustawienie ścieżek importu
root_path = Path(__file__).resolve().parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

import pytest
import pytest_asyncio # Dodany import
from httpx import AsyncClient, ASGITransport
from main import app  
from api.security.jwt import create_access_token

# Konfiguracja pętli zdarzeń dla testów asynchronicznych
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest_asyncio.fixture
async def token_user_a():
    """Generuje token dla właściciela (ID 1)"""
    return create_access_token(subject="1", expires_delta=timedelta(minutes=30))

@pytest_asyncio.fixture
async def token_user_b():
    """Generuje token dla innego użytkownika (ID 2)"""
    return create_access_token(subject="2", expires_delta=timedelta(minutes=30))

@pytest.mark.asyncio
async def test_program_ownership_logic(token_user_a, token_user_b):
    # Transport ASGITransport pozwala na testowanie aplikacji bez socketów
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        
        # 1. POST - Tworzenie (User A)
        create_res = await ac.post(
            "/api/programs", 
            json={
                "name": "Testowy Program",
                "duration_days": 5,
                "description": "Opis",
                "language": "pl",
                "image_url": "http://img.pl/1.jpg"
            }, 
            cookies={"access_token": token_user_a}
        )
        assert create_res.status_code == 200
        program_id = create_res.json()["id"]

        # 2. PUT - Próba edycji przez User B (Oczekiwane 403)
        update_res = await ac.put(
            f"/api/programs/{program_id}", 
            json={"name": "Zmiana"}, 
            cookies={"access_token": token_user_b}
        )
        assert update_res.status_code == 403

        # 3. DELETE - Poprawne usunięcie przez User A
        final_delete = await ac.delete(
            f"/api/programs/{program_id}", 
            cookies={"access_token": token_user_a}
        )
        assert final_delete.status_code == 200