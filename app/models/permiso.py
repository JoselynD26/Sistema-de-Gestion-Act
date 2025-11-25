from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.config import Base

class Permiso(Base):
    __tablename__ = "permiso"

    id = Column(Integer, primary_key=True, index=True)
    accion = Column(String, index=True)
    id_rol = Column(Integer, ForeignKey("rol.id"))