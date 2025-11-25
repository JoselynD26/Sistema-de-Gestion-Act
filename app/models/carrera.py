from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.config import Base
from app.models.relaciones import docente_carrera, sala_carrera

class Carrera(Base):
    __tablename__ = "carrera"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    
    docentes = relationship("Docente", secondary=docente_carrera, back_populates="carreras")
    salas = relationship("Sala", secondary=sala_carrera, back_populates="carreras")