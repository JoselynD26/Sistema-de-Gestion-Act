from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship  
from app.core.config import Base
from app.models.relaciones import sala_carrera
class Sala(Base):
    __tablename__ = "sala"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    tipo = Column(String, default="docentes")
    jornada = Column(String)
    id_sede = Column(Integer, ForeignKey("sede.id"))
    carreras = relationship("Carrera", secondary=sala_carrera, back_populates="salas")
    escritorios = relationship("Escritorio", back_populates="sala")