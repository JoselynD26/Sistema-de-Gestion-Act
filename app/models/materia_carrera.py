from sqlalchemy import Column, Integer, ForeignKey
from app.core.config import Base

class MateriaCarrera(Base):
    __tablename__ = "materia_carrera"

    id_materia = Column(Integer, ForeignKey("materia.id"), primary_key=True)
    id_carrera = Column(Integer, ForeignKey("carrera.id"), primary_key=True)