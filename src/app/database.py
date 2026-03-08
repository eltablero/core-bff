from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


# 1. Definimos la Base para SQLAlchemy 2.0 con soporte Async
class Base(AsyncAttrs, DeclarativeBase):
    pass


# 2. Creamos el motor asíncrono para SQL Server (Azure SQL)
# Asegúrate de que DATABASE_URL use mssql+aioodbc://
_engine = None


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        from app.core.config import settings

        _engine = create_async_engine(
            settings.db_url,
            pool_size=10,
            max_overflow=20,
            pool_recycle=1800,
            pool_pre_ping=True,
        )
    return _engine


# 4. Dependencia para FastAPI (Dependency Injection)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    engine = get_engine()
    async with async_sessionmaker(bind=engine)() as session:
        try:
            yield session
        finally:
            await session.close()
