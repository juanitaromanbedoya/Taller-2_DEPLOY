from pydantic import BaseModel, Field


class Pedido(BaseModel):
    producto_id: str
    cantidad: int = Field(..., gt=0)
    cliente: str = Field(..., min_length=2, max_length=100)