import sys
from pathlib import Path

# add project root to python path
root_path = Path(__file__).resolve().parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

import pytest
from httpx import AsyncClient, ASGITransport

from main import app


@pytest.mark.asyncio
async def test_non_existent_endpoint_returns_404():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:

        res = await ac.get("/api/this-endpoint-does-not-exist")

        assert res.status_code == 404
        body = res.json()
        assert "detail" in body
        assert body["detail"] == "Not Found"
