from sqlalchemy import Column, Integer, String
from app.core.config import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String)  # ← agrega este campo
    apellidos = Column(String) 
    correo = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(100), nullable=False)
    rol = Column(String(50), nullable=False)
    id_docente = Column(Integer, nullable=True)
