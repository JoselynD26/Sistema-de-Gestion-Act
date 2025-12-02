from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.config import Base

class Escritorio(Base):
    __tablename__ = "escritorio"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, nullable=False)

    sala_id = Column(Integer, ForeignKey("sala.id"), nullable=False)
    docente_id = Column(Integer, ForeignKey("docente.id"), nullable=True)
    carrera_id = Column(Integer, ForeignKey("carrera.id"), nullable=False)


    estado = Column(
        Enum("libre", "ocupado", name="estado_escritorio_enum"),
        nullable=False,
        default="libre"
    )

    jornada = Column(
        Enum("matutina", "vespertina", "nocturna", name="jornada_enum"),
        nullable=False
    )

    sala = relationship("Sala", back_populates="escritorios")
    docente = relationship("Docente", back_populates="escritorio", uselist=False)
    carrera = relationship("Carrera", back_populates="escritorios")

