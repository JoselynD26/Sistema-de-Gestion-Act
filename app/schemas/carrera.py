from pydantic import BaseModel
from typing import List, Optional

class CarreraBase(BaseModel):
    nombre: str
    codigo: Optional[str] = None

class CarreraCreate(CarreraBase):
    sede_ids: List[int]  # ✅ lista de sedes asociadas

class CarreraOut(CarreraBase):
    id: int
    codigo: str
    sede_ids: List[int]      # ✅ devolver también las sedes

    class Config:
        from_attributes = True