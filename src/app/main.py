from fastapi import FastAPI

from app.schemas import HealthCheck, Item

app = FastAPI(
    title="Core BFF API",
    description="Core Backend for Frontend para El Tablero",
    version="1.0.0",
    # OpenAPI Doc está habilitado por defecto en /docs
    openapi_url="/api/v1/openapi.json",
)


@app.get("/health", response_model=HealthCheck, tags=["System"])
async def get_health() -> HealthCheck:
    """
    Endpoint para Liveness y Readiness probes en Azure Container Apps.
    """
    return HealthCheck(status="ok")


@app.post("/items/", response_model=Item, tags=["Business Logic"])
async def create_item(item: Item) -> Item:
    # Aquí iría la lógica de persistencia
    return item
