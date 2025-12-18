from sqlalchemy import Column, Integer, Date, Time, Boolean, String, ForeignKey, Text
from app.core.config import Base

class Reserva(Base):
    __tablename__ = "reserva"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
    motivo = Column(Text)
    disponibilidad = Column(Boolean, default=True)
    estado = Column(String, default="pendiente")
    id_docente = Column(Integer, ForeignKey("docente.id"))
    id_aula = Column(Integer, ForeignKey("aula.id"))
    id_escritorio = Column(Integer, ForeignKey("escritorio.id"))