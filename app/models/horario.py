from sqlalchemy import Column, Integer, Date, Time, String, ForeignKey
from app.core.config import Base

class Horario(Base):
    __tablename__ = "horario"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    hora = Column(Time)
    estado = Column(String, default="activo")
    id_docente = Column(Integer, ForeignKey("docente.id"))
    id_materia = Column(Integer, ForeignKey("materia.id"))
    id_aula = Column(Integer, ForeignKey("aula.id"))
    id_sede = Column(Integer, ForeignKey("sede.id"))