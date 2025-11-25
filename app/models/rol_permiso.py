from sqlalchemy import Column, Integer, String
from app.core.config import Base

class RolPermiso(Base):
    __tablename__ = "rol_permiso"

    id = Column(Integer, primary_key=True, index=True)
    rol = Column(String(50))
    accion = Column(String(100))