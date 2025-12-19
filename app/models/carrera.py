from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from app.core.config import Base

# Tabla intermedia carrera_sede
carrera_sede = Table(
    "carrera_sede",
    Base.metadata,
    Column("carrera_id", ForeignKey("carrera.id"), primary_key=True),
    Column("sede_id", ForeignKey("sede.id"), primary_key=True),
)

class Carrera(Base):
    __tablename__ = "carrera"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(50), nullable=False, default="AUTO")

    # Relaciones
    docentes = relationship("Docente", secondary="docente_carrera", back_populates="carreras")
    salas = relationship("Sala", secondary="sala_carrera", back_populates="carreras")
    sedes = relationship("Sede", secondary="carrera_sede", back_populates="carreras")
    materias = relationship("Materia", secondary="carrera_materia", back_populates="carreras")
    escritorios = relationship("Escritorio", back_populates="carrera")

