from typing import AsyncGenerator

import pytest_asyncio
from app.database import get_db
from app.main import app


# Usamos el decorador específico del plugin, NO el genérico de pytest.mark
@pytest_asyncio.fixture(autouse=True, loop_scope="function")
async def override_get_db() -> AsyncGenerator[None, None]:
    """
    Al usar @pytest_asyncio.fixture, el plugin toma control total
    y Pytest 9 deja de emitir el warning de 'no plugin handled it'.
    """

    async def _mock_get_db() -> AsyncGenerator[str, None]:
        yield "mock_session"

    app.dependency_overrides[get_db] = _mock_get_db
    yield
    app.dependency_overrides.clear()
