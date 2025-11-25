from pydantic import BaseModel, EmailStr
from enum import Enum

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

class DocenteCreate(DocenteBase):
    pass

class DocenteOut(DocenteBase):
    id: int

    class Config:
        from_attributes = True