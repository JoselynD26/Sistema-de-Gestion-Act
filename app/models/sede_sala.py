from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.config import Base

sede_sala = Table(
    "sede_sala",
    Base.metadata,
    Column("sede_id", Integer, ForeignKey("sede.id"), primary_key=True),
    Column("sala_id", Integer, ForeignKey("sala.id"), primary_key=True),
)