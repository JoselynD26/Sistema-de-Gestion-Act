from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base

class DocenteMateria(Base):
    __tablename__ = "docente_materia"
    id = Column(Integer, primary_key=True, index=True)
    id_docente = Column(Integer, ForeignKey("docentes.id"))
    id_materia = Column(Integer, ForeignKey("materias.id"))