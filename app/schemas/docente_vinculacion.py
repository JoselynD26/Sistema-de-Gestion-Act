from pydantic import BaseModel

class DocenteVinculacionCreate(BaseModel):
    id_docente: int
    id_carrera: int
    id_materia: int
    id_sala: int
    id_escritorio: int