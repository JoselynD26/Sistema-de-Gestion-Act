from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.config import Base

class Croquis(Base):
    __tablename__ = "croquis"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    sede_id = Column(Integer, ForeignKey("sede.id"))
    imagen_url = Column(String)