from pydantic import BaseModel
from typing import Literal, Optional

# Base con los campos comunes
class EscritorioBase(BaseModel):
    codigo: str
    sala_id: int
    carrera_id: int
    docente_id: Optional[int] = None
    estado: Literal["libre", "ocupado"] = "libre"
    jornada: Literal["matutina", "vespertina", "nocturna"]

# Para crear
class EscritorioCreate(EscritorioBase):
    pass

# Para salida enriquecida
class EscritorioOut(EscritorioBase):
    id: int
    sala_nombre: Optional[str] = None
    carrera_nombre: Optional[str] = None
    docente_nombre: Optional[str] = None

    class Config:
        from_attributes = True   # ✅ en Pydantic v2
        # orm_mode = True        # ✅ si usas Pydantic v1

# Para actualizar
class EscritorioUpdate(BaseModel):
    codigo: Optional[str]
    sala_id: Optional[int]
    carrera_id: Optional[int]
    docente_id: Optional[int] = None
    estado: Optional[Literal["libre", "ocupado"]]
    jornada: Optional[Literal["matutina", "vespertina", "nocturna"]]

    class Config:
        from_attributes = True   # ✅ en Pydantic v2
        # orm_mode = True        # ✅ si usas Pydantic v1