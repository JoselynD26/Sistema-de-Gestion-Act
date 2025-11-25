from pydantic import BaseModel
from typing import Optional

class CroquisCreate(BaseModel):
    nombre: str
    sede_id: int
    imagen_url: Optional[str] = None

class CroquisOut(BaseModel):
    id: int
    nombre: str
    sede_id: int
    imagen_url: Optional[str]

    class Config:
        from_attributes = True