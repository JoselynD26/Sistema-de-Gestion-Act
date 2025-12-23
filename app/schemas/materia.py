from pydantic import BaseModel
from typing import List, Optional

class MateriaBase(BaseModel):
    nombre: str
    codigo: str

class MateriaCreate(BaseModel):
    nombre: str
    codigo: Optional[str] = None
    carrera_ids: Optional[List[int]] = []
    sede_ids: Optional[List[int]] = []
    docente_ids: Optional[List[int]] = []

class MateriaOut(MateriaBase):
    id: int

    class Config:
        from_attributes = True