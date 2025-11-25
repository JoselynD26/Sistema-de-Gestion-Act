from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base

class SalaCarrera(Base):
    __tablename__ = "sala_carrera"
    id = Column(Integer, primary_key=True, index=True)
    id_sala = Column(Integer, ForeignKey("salas.id"))
    id_carrera = Column(Integer, ForeignKey("carreras.id"))