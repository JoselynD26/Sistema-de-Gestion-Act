from pydantic import BaseModel

class SalaProfesoresCreate(BaseModel):
    nombre: str

class SalaProfesoresOut(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True