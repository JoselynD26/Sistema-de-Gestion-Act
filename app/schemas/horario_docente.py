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


class HorarioDocenteUpdate(BaseModel):
    docente_id: int | None = None
    curso_id: int | None = None
    materia_id: int | None = None
    aula_id: int | None = None
    dia: str | None = None
    hora_inicio: time | None = None
    hora_fin: time | None = None
    estado: str | None = None



class HorarioDocenteOut(HorarioDocenteCreate):
    id: int
    estado: str

    class Config:
        from_attributes = True
