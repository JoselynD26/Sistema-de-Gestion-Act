from pydantic import BaseModel
from typing import Optional

class SalaBase(BaseModel):
    nombre: str
    sede_id: int

class SalaCreate(SalaBase):
    pass

class SalaOut(BaseModel):
    id: int
    nombre: str
    sede_id: int
    sede_nombre: Optional[str] = None  # ✅ nuevo campo

    class Config:
        from_attributes = True