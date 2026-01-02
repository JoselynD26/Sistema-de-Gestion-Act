from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func
from app.core.config import Base

class HorarioCancelado(Base):
    __tablename__ = "horario_cancelado"

    id = Column(Integer, primary_key=True, index=True)
    horario_id = Column(Integer, ForeignKey("horario_docente.id"), nullable=False, index=True)
    fecha = Column(Date, nullable=False)
    motivo = Column(String, nullable=True)
    estado = Column(String, nullable=False, default="cancelado")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
