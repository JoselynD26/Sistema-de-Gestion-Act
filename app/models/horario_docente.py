from sqlalchemy import Column, Integer, String, Time, ForeignKey
from app.core.config import Base

class HorarioDocente(Base):
    __tablename__ = "horario_docente"

    id = Column(Integer, primary_key=True, index=True)

    docente_id = Column(Integer, ForeignKey("docente.id"), nullable=False)
    curso_id = Column(Integer, ForeignKey("curso.id"), nullable=False)
    materia_id = Column(Integer, ForeignKey("materia.id"), nullable=False)
    aula_id = Column(Integer, ForeignKey("aula.id"), nullable=False)

    dia = Column(String, nullable=False)  # Lunes, Martes, etc
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    estado = Column(String, default="activo")
