from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.config import Base

class SalaProfesores(Base):
    __tablename__ = "sala_profesores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    capacidad = Column(Integer, nullable=False)
    sede_id = Column(Integer, ForeignKey('sede.id'), nullable=False)
    plaza_id = Column(Integer, ForeignKey('plaza.id'), nullable=True)
    croquis_url = Column(Text, nullable=True)
    
    # Relaciones
    # escritorios = relationship("Escritorio", back_populates="sala")
    # plaza = relationship("Plaza", back_populates="salas")