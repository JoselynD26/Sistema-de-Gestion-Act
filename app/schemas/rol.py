from pydantic import BaseModel

class RolCreate(BaseModel):
    nombre: str

class RolOut(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True