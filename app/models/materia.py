from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.core.config import Base
from app.models.relaciones import docente_materia, carrera_materia

# Tabla intermedia sede_materia (solo aquí)
sede_materia = Table(
    "sede_materia",
    Base.metadata,
    Column("sede_id", ForeignKey("sede.id"), primary_key=True),
    Column("materia_id", ForeignKey("materia.id"), primary_key=True),
)

class Materia(Base):
    __tablename__ = "materia"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(20), nullable=False)

    sedes = relationship(
        "Sede",
        secondary=sede_materia,
        back_populates="materias",
    )

    docentes = relationship(
        "Docente",
        secondary=docente_materia,
        back_populates="materias",
    )

    carreras = relationship(
        "Carrera",
        secondary=carrera_materia,
        back_populates="materias",
    )
