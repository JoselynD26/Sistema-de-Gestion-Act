from pydantic import BaseModel

class CursoBase(BaseModel):
    nivel: str
    paralelo: str
    jornada: str
    id_sede: int

class CursoCreate(CursoBase):
    pass

class CursoOut(CursoBase):
    id: int

    class Config:
        from_attributes = True