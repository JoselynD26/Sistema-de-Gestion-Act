from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base


class UsuarioCreate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    correo: EmailStr
    contrasena: str
    rol: str
    id_docente: Optional[int] = None

class UsuarioOut(BaseModel):
    id: int
    correo: EmailStr
    rol: str
    id_docente: Optional[int]

    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    correo: EmailStr
    clave: str

class UsuarioRol(Base):
    __tablename__ = "usuario_rol"
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"))
    id_rol = Column(Integer, ForeignKey("roles.id"))