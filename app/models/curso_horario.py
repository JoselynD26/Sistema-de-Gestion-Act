from sqlalchemy import Column, Integer, ForeignKey
from app.core.config import Base

class CursoHorario(Base):
    __tablename__ = "curso_horario"

    id_curso = Column(Integer, ForeignKey("curso.id"), primary_key=True)
    id_horario = Column(Integer, ForeignKey("horario.id"), primary_key=True)