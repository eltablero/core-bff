from typing import Dict

from app.core.logger import logger
from app.database import get_db
from app.schemas import HealthCheck
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/liveness", status_code=status.HTTP_200_OK, tags=["System"])
def get_liveness() -> Dict[str, str]:
    """
    Liveness Probe: Indica si el proceso del contenedor está en ejecución.
    No verifica dependencias externas para evitar reinicios innecesarios.
    """
    return {"status": "alive"}


@router.get("/health", response_model=HealthCheck)
async def get_health(
    response: Response,
    db_session: AsyncSession = Depends(get_db),
) -> HealthCheck:
    checks = {"database": "unknown"}

    # Llamamos a una función auxiliar pasando la sesión ya abierta
    is_healthy = await check_database_status(db_session)

    if is_healthy:
        checks["database"] = "connected"
        return HealthCheck(status="ok", checks=checks)
    else:
        checks["database"] = "error: connection failed"
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return HealthCheck(status="unhealthy", checks=checks)


async def check_database_status(session: AsyncSession) -> bool:
    """Lógica reutilizable para validar la conexión"""
    try:
        await session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(
            "Database connection failed during health check",
            exc_info=True,
            error=str(e),
        )
        return False
