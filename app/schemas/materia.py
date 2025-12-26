from pydantic import BaseModel
from typing import List, Optional


class CarreraSimple(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True


class SedeSimple(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True


class DocenteSimple(BaseModel):
    id: int
    nombres: str
    apellidos: str

    class Config:
        from_attributes = True


class MateriaCreate(BaseModel):
    nombre: str
    codigo: Optional[str] = None
    carrera_ids: Optional[List[int]] = []
    sede_ids: Optional[List[int]] = []
    docente_ids: Optional[List[int]] = []


class MateriaOut(BaseModel):
    id: int
    nombre: str
    codigo: str

    carreras: List[CarreraSimple] = []
    sedes: List[SedeSimple] = []
    docentes: List[DocenteSimple] = []

    class Config:
        from_attributes = True
