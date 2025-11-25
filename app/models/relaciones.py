from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.config import Base

docente_materia = Table(
    "docente_materia",
    Base.metadata,
    Column("docente_id", Integer, ForeignKey("docente.id"), primary_key=True),
    Column("materia_id", Integer, ForeignKey("materia.id"), primary_key=True)
)

docente_carrera = Table(
    "docente_carrera",
    Base.metadata,
    Column("docente_id", Integer, ForeignKey("docente.id"), primary_key=True),
    Column("carrera_id", Integer, ForeignKey("carrera.id"), primary_key=True)
)

sala_carrera = Table(
    "sala_carrera",
    Base.metadata,
    Column("sala_id", Integer, ForeignKey("sala.id"), primary_key=True),
    Column("carrera_id", Integer, ForeignKey("carrera.id"), primary_key=True)
)