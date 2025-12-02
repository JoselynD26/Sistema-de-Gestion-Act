from pydantic import BaseModel

class AulaBase(BaseModel):
    nombre: str
    numero: str | None = None
    capacidad: int | None = None
    descripcion: str | None = None
    id_sede: int

class AulaCreate(AulaBase):
    pass

class AulaOut(AulaBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2