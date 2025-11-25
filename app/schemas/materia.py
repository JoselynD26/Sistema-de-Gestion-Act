from pydantic import BaseModel

class MateriaBase(BaseModel):
    nombre: str
    id_sede: int

class MateriaCreate(MateriaBase):
    pass

class MateriaOut(MateriaBase):
    id: int

    class Config:
        from_attributes = True