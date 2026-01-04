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

class UsuarioChangePassword(BaseModel):
    contrasena_actual: str
    nueva_contrasena: str

class UsuarioResetPassword(BaseModel):
    nueva_contrasena: str


class UsuarioUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    correo: Optional[EmailStr] = None
    rol: Optional[str] = None
    id_docente: Optional[int] = None

class UsuarioLogin(BaseModel):
    correo: EmailStr
    contrasena: str