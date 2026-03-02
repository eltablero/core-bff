from typing import Optional

from pydantic import BaseModel, Field


class Item(BaseModel):
    id: int
    # Use `json_schema_extra` instead of passing `example` directly to Field
    name: str = Field(
        ...,
        json_schema_extra={"example": "Frontend Plugin"},
    )
    description: Optional[str] = None
    price: float = Field(..., gt=0)  # Precio debe ser mayor a 0


class HealthCheck(BaseModel):
    status: str = "ok"
