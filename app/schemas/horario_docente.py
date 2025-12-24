from pydantic import BaseModel
from datetime import time

class HorarioDocenteCreate(BaseModel):
    docente_id: int
    curso_id: int
    materia_id: int
    aula_id: int
    dia: str
    hora_inicio: time
    hora_fin: time


class HorarioDocenteOut(HorarioDocenteCreate):
    id: int
    estado: str

    class Config:
        from_attributes = True
