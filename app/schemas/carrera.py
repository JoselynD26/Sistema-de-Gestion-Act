from pydantic import BaseModel

class CarreraBase(BaseModel):
    nombre: str

class CarreraCreate(CarreraBase):
    pass

class CarreraOut(CarreraBase):
    id: int

    class Config:
        from_attributes = True