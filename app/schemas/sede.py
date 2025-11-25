from pydantic import BaseModel

class SedeBase(BaseModel):
    nombre: str
    ubicacion: str

class SedeCreate(SedeBase):
    pass

class SedeOut(SedeBase):
    id: int

    class Config:
        from_attributes = True