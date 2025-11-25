from sqlalchemy import Column, Integer, String
from app.core.config import Base

class SalaProfesores(Base):
    __tablename__ = "sala_profesores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))