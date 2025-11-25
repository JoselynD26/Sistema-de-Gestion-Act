from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.core.config import Base
from app.models.relaciones import docente_materia, docente_carrera


class Docente(Base):
    __tablename__ = "docente"

    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String, unique=True, nullable=False, index=True)
    correo = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    nombres = Column(String, nullable=False)
    regimen = Column(Enum("LOES", "Codigo de trabajo", name="regimen_enum"), nullable=False)
    observacion = Column(Enum("Medio tiempo", "Tiempo completo", name="observacion_enum"), nullable=False)
    materias = relationship("Materia", secondary=docente_materia, back_populates="docentes")
    carreras = relationship("Carrera", secondary=docente_carrera, back_populates="docentes")