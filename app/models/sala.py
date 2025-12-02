from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.relaciones import sala_carrera
from app.core.config import Base

class Sala(Base):
    __tablename__ = "sala"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)

    # ✅ Relación directa con sede
    sede_id = Column(Integer, ForeignKey("sede.id"), nullable=False)

    # ✅ Relaciones
    carreras = relationship("Carrera", secondary=sala_carrera, back_populates="salas")
    escritorios = relationship("Escritorio", back_populates="sala")
    sede = relationship("Sede", back_populates="salas")