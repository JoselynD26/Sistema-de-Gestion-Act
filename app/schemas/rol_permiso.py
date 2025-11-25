from pydantic import BaseModel

class RolPermisoCreate(BaseModel):
    rol: str
    accion: str