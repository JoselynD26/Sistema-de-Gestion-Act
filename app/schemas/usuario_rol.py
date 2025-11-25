from pydantic import BaseModel

class UsuarioRolCreate(BaseModel):
    id_usuario: int
    id_rol: int

class UsuarioRolOut(BaseModel):
    id: int
    id_usuario: int
    id_rol: int

    class Config:
        from_attributes = True