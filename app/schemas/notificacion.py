from pydantic import BaseModel
from datetime import datetime

class NotificacionCreate(BaseModel):
    mensaje: str
    tipo: str
    id_usuario: int

class NotificacionOut(BaseModel):
    id: int
    mensaje: str
    tipo: str
    leido: bool
    fecha: datetime

    class Config:
        from_attributes = True