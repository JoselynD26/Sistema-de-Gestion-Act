from pydantic import BaseModel

class DocenteSalaCreate(BaseModel):
    id_docente: int
    id_aula: int

class DocenteSalaOut(DocenteSalaCreate):
    id: int

    class Config:
        from_attributes = True