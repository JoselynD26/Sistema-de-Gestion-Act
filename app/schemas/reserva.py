from pydantic import BaseModel
from datetime import date, time

class ReservaCreate(BaseModel):
    fecha: date
    hora: time
    id_docente: int
    id_aula: int
    id_escritorio: int

class ReservaOut(ReservaCreate):
    id: int
    disponibilidad: bool
    estado: str

    class Config:
        from_attributes = True