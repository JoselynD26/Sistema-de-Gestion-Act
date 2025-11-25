from pydantic import BaseModel

class CursoHorarioCreate(BaseModel):
    id_curso: int
    id_horario: int

class CursoHorarioOut(CursoHorarioCreate):
    pass