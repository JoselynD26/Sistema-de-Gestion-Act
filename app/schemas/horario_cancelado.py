from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class HorarioCanceladoBase(BaseModel):
    horario_id: int
    fecha: date
    motivo: Optional[str] = None
    estado: str = "cancelado"

class HorarioCanceladoCreate(HorarioCanceladoBase):
    pass

class HorarioCancelado(HorarioCanceladoBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
