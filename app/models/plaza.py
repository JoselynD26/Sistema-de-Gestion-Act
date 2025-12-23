from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.config import Base

class Plaza(Base):
    __tablename__ = "plaza"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)  # "Piso 1", "Piso 2"
    sede_id = Column(Integer, ForeignKey("sede.id"), nullable=False)
    croquis_url = Column(Text, nullable=True)

    # Relaciones
    # sede = relationship("Sede", back_populates="plazas")
    # salas = relationship("SalaProfesores", back_populates="plaza")