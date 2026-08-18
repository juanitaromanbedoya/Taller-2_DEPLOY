from pydantic import BaseModel, Field


class Producto(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: str | None = None
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)