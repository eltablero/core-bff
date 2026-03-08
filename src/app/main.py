from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy import text

from app.api.endpoints import health
from app.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup: Verificar conexión a Azure SQL
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("🚀 Conexión a Azure SQL verificada exitosamente.")
    except Exception as e:
        print(f"❌ Error crítico al conectar a la DB: {e}")
        # En producción, podrías querer que el contenedor falle aquí

    yield

    # Shutdown: Limpiar el pool de conexiones
    await engine.dispose()
    print("💤 Conexiones a la DB cerradas.")


app = FastAPI(
    title="Core BFF API",
    description="Core Backend for Frontend para El Tablero",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan,
)

app.include_router(health.router, prefix="/api/v1", tags=["System"])
