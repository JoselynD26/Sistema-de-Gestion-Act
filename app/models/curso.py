from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.config import Base

class Curso(Base):
    __tablename__ = "curso"

    id = Column(Integer, primary_key=True, index=True)
    nivel = Column(String(50), nullable=False)
    paralelo = Column(String(10), nullable=False)
    jornada = Column(String(50), nullable=False)
    id_sede = Column(Integer, ForeignKey("sede.id"), nullable=False)