from pydantic import BaseModel

class AulaBase(BaseModel):
    nombre: str
    id_sede: int

class AulaCreate(AulaBase):
    pass

class AulaOut(AulaBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2