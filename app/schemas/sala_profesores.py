from pydantic import BaseModel
from typing import Optional

class SalaProfesoresCreate(BaseModel):
    nombre: str
    capacidad: int = 20
    sede_id: int = 1

class SalaProfesoresOut(BaseModel):
    id: int
    nombre: str
    capacidad: int
    sede_id: int
    croquis_url: Optional[str] = None

    class Config:
        from_attributes = True