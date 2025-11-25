from pydantic import BaseModel

class PlazaCreate(BaseModel):
    nombre: str
    piso: str
    id_aula: int