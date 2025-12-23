from sqlalchemy import Column, Integer, Date, Time, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.config import Base

class Horario(Base):
    __tablename__ = "horario"

    id = Column(Integer, primary_key=True, index=True)
    dia = Column(String, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    id_materia = Column(Integer, ForeignKey("materia.id"), nullable=False)
    id_docente = Column(Integer, ForeignKey("docente.id"), nullable=False)
    id_aula = Column(Integer, ForeignKey("aula.id"), nullable=False)
    id_curso = Column(Integer, ForeignKey("curso.id"), nullable=True)
    id_sede = Column(Integer, ForeignKey("sede.id"), nullable=False)
    fecha = Column(Date, nullable=True)
    estado = Column(String, nullable=True)