from pydantic import BaseModel

class DocenteCarreraCreate(BaseModel):
    id_docente: int
    id_carrera: int