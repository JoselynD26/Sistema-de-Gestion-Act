from sqlalchemy import Column, Integer, String
from app.core.config import Base

class Sede(Base):
    __tablename__ = "sede"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    ubicacion = Column(String, nullable=False)