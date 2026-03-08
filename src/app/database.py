from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import DATABASE_URL


# 1. Definimos la Base para SQLAlchemy 2.0 con soporte Async
class Base(AsyncAttrs, DeclarativeBase):
    pass


# 2. Creamos el motor asíncrono para SQL Server (Azure SQL)
# Asegúrate de que DATABASE_URL use mssql+aioodbc://
engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_recycle=1800,
    pool_pre_ping=True,
)

# 3. Fábrica de sesiones asíncronas
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# 4. Dependencia para FastAPI (Dependency Injection)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
