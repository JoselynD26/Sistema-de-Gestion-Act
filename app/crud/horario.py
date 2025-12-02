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

def obtener_horario(db: Session, horario_id: int):
    return db.query(Horario).filter(Horario.id == horario_id).first()

def actualizar_horario(db: Session, horario_id: int, datos: HorarioCreate):
    horario = db.query(Horario).filter(Horario.id == horario_id).first()
    if not horario:
        return None
    for key, value in datos.dict().items():
        setattr(horario, key, value)
    db.commit()
    db.refresh(horario)
    return horario

def eliminar_horario(db: Session, horario_id: int):
    horario = db.query(Horario).filter(Horario.id == horario_id).first()
    if not horario:
        return None
    db.delete(horario)
    db.commit()
    return True

def listar_horarios_cancelados(db: Session, sede_id: int, fecha: date):
    return db.query(Horario).filter(
        Horario.id_sede == sede_id,
        Horario.fecha == fecha,
        Horario.estado == "cancelado"
    ).all()