from typing import AsyncGenerator
from unittest.mock import AsyncMock

import pytest
from app.main import app
from httpx import ASGITransport, AsyncClient

# Configuramos el transporte para que HTTPX hable directamente con la app de FastAPI
transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_read_health() -> None:
    # 1. Definimos un mock para la base de datos
    async def mock_get_db() -> AsyncGenerator[AsyncMock, None]:
        # Simulamos un generador asíncrono que cede una sesión falsa
        yield AsyncMock()

    # 2. Inyectamos el override directamente en la app
    from app.database import get_db
    from app.main import app

    app.dependency_overrides[get_db] = mock_get_db

    try:
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
    finally:
        # 3. Limpiamos para no afectar otros tests
        app.dependency_overrides.clear()
