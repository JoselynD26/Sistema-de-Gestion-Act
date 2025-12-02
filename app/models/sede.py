from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.config import Base

class Sede(Base):
    __tablename__ = "sede"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    ubicacion = Column(String, nullable=False)

    # ✅ Relaciones
    carreras = relationship("Carrera", secondary="carrera_sede", back_populates="sedes")
    docentes = relationship("Docente", back_populates="sede")
    materias = relationship("Materia", secondary="sede_materia", back_populates="sedes")

    # 👉 Relación directa con Sala (One-to-Many)
    salas = relationship("Sala", back_populates="sede")