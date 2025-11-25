from sqlalchemy import Column, Integer, ForeignKey
from app.core.config import Base

class UsuarioRol(Base):
    __tablename__ = "usuario_rol"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id"))
    id_rol = Column(Integer, ForeignKey("rol.id"))