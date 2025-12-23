from pydantic import BaseModel, field_validator
from datetime import date, time
from typing import Optional, Union

from pydantic import BaseModel, field_validator, Field
from datetime import date, time
from typing import Optional, Union

class HorarioCreate(BaseModel):
    # Campos que puede enviar el frontend
    fecha: Optional[date] = None
    dia: Optional[str] = None
    hora_inicio: Union[str, time]
    hora_fin: Union[str, time]
    id_materia: int
    id_docente: int
    id_aula: int
    id_curso: Optional[int] = 1  # Valor por defecto
    id_sede: int
    estado: Optional[str] = "activo"
    
    def __init__(self, **data):
        # Si viene fecha pero no dia, convertir fecha a dia de la semana
        if 'fecha' in data and 'dia' not in data and data['fecha']:
            import datetime
            fecha_obj = data['fecha'] if isinstance(data['fecha'], datetime.date) else datetime.datetime.strptime(data['fecha'], '%Y-%m-%d').date()
            dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
            data['dia'] = dias[fecha_obj.weekday()]
        elif 'dia' not in data:
            data['dia'] = 'Lunes'  # Valor por defecto
        super().__init__(**data)
    
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
    dia: str
    hora_inicio: time
    hora_fin: time
    id_materia: int
    id_docente: int
    id_aula: int
    id_curso: int
    id_sede: int
    fecha: Optional[date] = None
    estado: Optional[str] = None

    class Config:
        from_attributes = True