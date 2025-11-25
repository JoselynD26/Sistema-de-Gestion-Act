from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.config import Base

class Aula(Base):
    __tablename__ = "aula"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    id_sede = Column(Integer, ForeignKey("sede.id"))