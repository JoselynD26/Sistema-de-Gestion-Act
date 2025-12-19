from pydantic import BaseModel
from typing import Optional

class PlazaBase(BaseModel):
    nombre: str
    sede_id: int
    croquis_url: Optional[str] = None

class PlazaCreate(PlazaBase):
    pass

class PlazaOut(PlazaBase):
    id: int

    class Config:
        from_attributes = True