from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.config import Base

# Tabla intermedia para Materia ↔ Carrera
carrera_materia = Table(
    "carrera_materia",
    Base.metadata,
    Column("carrera_id", Integer, ForeignKey("carrera.id"), primary_key=True),
    Column("materia_id", Integer, ForeignKey("materia.id"), primary_key=True),
)

# Tabla intermedia para Materia ↔ Sede
sede_materia = Table(
    "sede_materia",
    Base.metadata,
    Column("sede_id", Integer, ForeignKey("sede.id"), primary_key=True),
    Column("materia_id", Integer, ForeignKey("materia.id"), primary_key=True),
)

class Materia(Base):
    __tablename__ = "materia"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)

    # Relaciones
    docentes = relationship("Docente", secondary="docente_materia", back_populates="materias")
    carreras = relationship("Carrera", secondary=carrera_materia, back_populates="materias")
    sedes = relationship("Sede", secondary=sede_materia, back_populates="materias")