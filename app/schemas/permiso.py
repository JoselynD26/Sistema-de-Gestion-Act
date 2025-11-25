from pydantic import BaseModel

class PermisoBase(BaseModel):
    accion: str
    id_rol: int

class PermisoCreate(PermisoBase):
    pass

class PermisoOut(PermisoBase):
    id: int

    class Config:
        from_attributes = True