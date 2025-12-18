from pydantic import BaseModel, field_validator
from datetime import date, time
from typing import Optional, Union

class HorarioCreate(BaseModel):
    fecha: date
    hora_inicio: Optional[Union[str, time]] = None
    hora_fin: Optional[Union[str, time]] = None
    estado: str
    id_docente: int
    id_materia: int
    id_aula: int
    id_sede: int
    
    @field_validator('hora_inicio', 'hora_fin')
    @classmethod
    def parse_time(cls, v):
        if v is None:
            return v
        if isinstance(v, str):
            # Convertir "17" a "17:00"
            if ':' not in v:
                v = f"{v}:00"
            return time.fromisoformat(v)
        return v

class HorarioOut(BaseModel):
    id: int
    fecha: date
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    estado: str
    id_docente: int
    id_materia: int
    id_aula: int
    id_sede: int

    class Config:
        from_attributes = True