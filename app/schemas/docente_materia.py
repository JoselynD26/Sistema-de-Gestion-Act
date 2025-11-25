from pydantic import BaseModel

class DocenteMateriaCreate(BaseModel):
    id_docente: int
    id_materia: int