from sqlalchemy import Column, Integer, ForeignKey
from app.core.config import Base

class DocenteVinculacion(Base):
    __tablename__ = "docente_vinculacion"

    id = Column(Integer, primary_key=True, index=True)
    id_docente = Column(Integer, ForeignKey("docente.id"))
    id_carrera = Column(Integer, ForeignKey("carrera.id"))
    id_materia = Column(Integer, ForeignKey("materia.id"))
    id_sala = Column(Integer, ForeignKey("sala.id"))
    id_escritorio = Column(Integer, ForeignKey("escritorio.id"))