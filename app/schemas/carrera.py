from pydantic import BaseModel
from typing import List

class CarreraBase(BaseModel):
    nombre: str
    codigo: str = "AUTO"  # Valor por defecto

class CarreraCreate(CarreraBase):
    sede_ids: List[int]  # ✅ lista de sedes asociadas

class CarreraOut(CarreraBase):
    id: int
    codigo: str
    sede_ids: List[int]      # ✅ devolver también las sedes

    class Config:
        from_attributes = True