from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.core.config import Base

class Notificacion(Base):
    __tablename__ = "notificacion"

    id = Column(Integer, primary_key=True, index=True)
    mensaje = Column(String)
    tipo = Column(String)
    id_usuario = Column(Integer, ForeignKey("usuario.id"))

    leido = Column(Boolean, default=False)
    fecha = Column(DateTime, default=datetime.now)