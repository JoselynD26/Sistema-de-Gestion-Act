from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.config import Base

class Sala(Base):
    __tablename__ = "sala"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    sede_id = Column(Integer, ForeignKey("sede.id"), nullable=False)