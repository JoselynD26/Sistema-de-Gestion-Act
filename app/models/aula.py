from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.config import Base

class Aula(Base):
    __tablename__ = "aula"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    numero = Column(String(50), nullable=True)
    capacidad = Column(Integer, nullable=True)
    descripcion = Column(String(255), nullable=True)
    id_sede = Column(Integer, ForeignKey("sede.id"), nullable=False)