from pydantic import BaseModel
from datetime import date, time

class HorarioCreate(BaseModel):
    fecha: date
    hora: time
    estado: str
    id_docente: int
    id_materia: int
    id_aula: int
    id_sede: int

class HorarioOut(HorarioCreate):
    id: int

    class Config:
        from_attributes = True