from pydantic import BaseModel

class SalaCarreraCreate(BaseModel):
    id_sala: int
    id_carrera: int