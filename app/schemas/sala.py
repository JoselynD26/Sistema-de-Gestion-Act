from pydantic import BaseModel

class SalaBase(BaseModel):
    nombre: str
    tipo: str
    jornada: str
    id_sede: int

class SalaCreate(SalaBase):
    pass

class SalaOut(SalaBase):
    id: int

    class Config:
        from_attributes = True