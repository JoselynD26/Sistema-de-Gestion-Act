from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class Regimen(str, Enum):
    LOES = "LOES"
    codigo = "Codigo de trabajo"

class Observacion(str, Enum):
    medio = "Medio tiempo"
    completo = "Tiempo completo"

class DocenteBase(BaseModel):
    cedula: str
    correo: EmailStr
    apellidos: str
    nombres: str
    regimen: Regimen
    observacion: Observacion
    sede_id: int 

class DocenteCreate(DocenteBase):
    pass

class DocenteUpdate(BaseModel):
    cedula: Optional[str] = None
    correo: Optional[EmailStr] = None
    apellidos: Optional[str] = None
    nombres: Optional[str] = None
    regimen: Optional[Regimen] = None
    observacion: Optional[Observacion] = None
    sede_id: Optional[int] = None

class DocenteOut(DocenteBase):
    id: int

    class Config:
        from_attributes = True