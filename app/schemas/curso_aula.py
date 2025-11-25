from pydantic import BaseModel

class CursoAulaCreate(BaseModel):
    id_curso: int
    id_aula: int

class CursoAulaOut(CursoAulaCreate):
    pass