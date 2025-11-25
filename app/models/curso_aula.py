from sqlalchemy import Column, Integer, ForeignKey
from app.core.config import Base

class CursoAula(Base):
    __tablename__ = "curso_aula"

    id_curso = Column(Integer, ForeignKey("curso.id"), primary_key=True)
    id_aula = Column(Integer, ForeignKey("aula.id"), primary_key=True)