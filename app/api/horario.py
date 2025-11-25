from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.core.config import SessionLocal
from app.controllers.horario_controller import horarios_cancelados

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/horarios/cancelados/")
def ver_horarios_cancelados(sede_id: int, fecha: date, db: Session = Depends(get_db)):
    return horarios_cancelados(db, sede_id, fecha)