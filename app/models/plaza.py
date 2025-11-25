from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.config import Base

class Plaza(Base):
    __tablename__ = "plaza"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    piso = Column(String(10))
    id_aula = Column(Integer, ForeignKey("aula.id"))