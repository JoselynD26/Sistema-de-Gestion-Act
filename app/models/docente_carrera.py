from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base

class DocenteCarrera(Base):
    __tablename__ = "docente_carrera"
    id = Column(Integer, primary_key=True, index=True)
    id_docente = Column(Integer, ForeignKey("docentes.id"))
    id_carrera = Column(Integer, ForeignKey("carreras.id"))