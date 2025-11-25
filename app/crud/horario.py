from sqlalchemy.orm import Session
from app.models.horario import Horario
from app.schemas.horario import HorarioCreate
from datetime import date

def crear_horario(db: Session, datos: HorarioCreate):
    nuevo = Horario(**datos.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_horarios_cancelados(db: Session, sede_id: int, fecha: date):
    return db.query(Horario).filter_by(
        id_sede=sede_id,
        fecha=fecha,
        estado="cancelado"
    ).all()