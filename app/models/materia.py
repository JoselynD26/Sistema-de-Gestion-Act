from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.config import Base
from app.models.relaciones import docente_materia
class Materia(Base):
    __tablename__ = "materia"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    id_sede = Column(Integer, ForeignKey("sede.id"))

    docentes = relationship("Docente", secondary=docente_materia, back_populates="materias")
