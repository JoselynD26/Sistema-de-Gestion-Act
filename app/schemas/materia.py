from pydantic import BaseModel
from typing import List

class MateriaBase(BaseModel):
    nombre: str

class MateriaCreate(MateriaBase):
    carrera_ids: List[int] = []
    sede_ids: List[int] = []
    docente_ids: List[int] = []   # ✅ nuevo campo para docentes

class MateriaOut(MateriaBase):
    id: int
    carrera_ids: List[int] = []
    sede_ids: List[int] = []
    docente_ids: List[int] = []

    @classmethod
    def from_orm(cls, materia):
        return cls(
            id=materia.id,
            nombre=materia.nombre,
            carrera_ids=[c.id for c in materia.carreras],
            sede_ids=[s.id for s in materia.sedes],
            docente_ids=[d.id for d in materia.docentes],
        )

    class Config:
        orm_mode = True   # ✅ permite convertir desde SQLAlchemy ORM