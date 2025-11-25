from sqlalchemy import Column, Integer, ForeignKey
from app.core.config import Base

class DocenteSala(Base):
    __tablename__ = "docente_sala"

    id = Column(Integer, primary_key=True, index=True)
    id_docente = Column(Integer, ForeignKey("docente.id"))
    id_aula = Column(Integer, ForeignKey("aula.id"))