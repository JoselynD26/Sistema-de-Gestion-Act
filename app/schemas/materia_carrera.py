from pydantic import BaseModel

class MateriaCarreraCreate(BaseModel):
    id_materia: int
    id_carrera: int

class MateriaCarreraOut(MateriaCarreraCreate):
    pass