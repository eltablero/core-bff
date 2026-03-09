import uuid
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Awaitable, Callable

import structlog
from fastapi import FastAPI, Request
from sqlalchemy import text
from starlette.responses import Response as StarletteResponse

from app.api.endpoints import health
from app.core.logger import logger, setup_logging
from app.database import get_engine

# Definimos el tipo para call_next para mayor claridad
# Recibe un Request y devuelve una Awaitable que resuelve en una Response
CallNext = Callable[[Request[Any]], Awaitable[StarletteResponse]]

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup: Verificar conexión a Azure SQL
    try:
        engine = get_engine()
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

app.include_router(health.router, tags=["System"])


@app.middleware("http")
async def logging_middleware(
    request: Request[Any], call_next: CallNext
) -> StarletteResponse:
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    # Inyectamos el ID en el contexto del log
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id)

    response = await call_next(request)

    logger.info(
        "request_processed",
        path=request.url.path,
        method=request.method,
        status=response.status_code,
    )  # noqa: E501
    return response
