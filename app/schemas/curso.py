from pydantic import BaseModel
from typing import Optional

class CursoBase(BaseModel):
    nombre: str
    nivel: str
    paralelo: str
    carrera_id: int
    id_sede: int
    jornada: Optional[str] = None

class CursoCreate(CursoBase):
    pass

class CursoOut(CursoBase):
    id: int

    class Config:
        from_attributes = True