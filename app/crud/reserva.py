from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.aula import get_db
from app.models.reserva import Reserva
from app.schemas.reserva import ReservaCreate

def crear_reserva(db: Session, datos: ReservaCreate):
    nueva = Reserva(**datos.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def obtener_reserva(db: Session, reserva_id: int):
    return db.query(Reserva).filter(Reserva.id == reserva_id).first()

def actualizar_estado_reserva(db: Session, reserva_id: int, nuevo_estado: str):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if reserva:
        reserva.estado = nuevo_estado
        db.commit()
        db.refresh(reserva)
    return reserva

def listar_reservas(db: Session):
    return db.query(Reserva).all()
def cancelar_reserva(reserva_id: int, docente_id: int, db: Session = Depends(get_db)):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id, Reserva.id_usuario == docente_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada o no pertenece al usuario")
    reserva.estado = "cancelada"
    db.commit()
    db.refresh(reserva)
    return reserva