from pydantic import BaseModel
from typing import Literal

class EscritorioCreate(BaseModel):
    codigo: str
    id_sala: int
    id_carrera: int
    id_docente: int | None = None
    estado: Literal["libre", "ocupado"] = "libre"
    jornada: Literal["matutina", "vespertina", "nocturna"]

class EscritorioOut(EscritorioCreate):
    id: int

    class Config:
        from_attributes = True