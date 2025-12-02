from pydantic import BaseModel
from typing import Literal

class CursoBase(BaseModel):
    nivel: str
    paralelo: str
    jornada:  Literal["Matutina", "Vespertina", "Nocturna"] 
    id_sede: int

class CursoCreate(CursoBase):
    pass

class CursoOut(CursoBase):
    id: int

    class Config:
        from_attributes = True