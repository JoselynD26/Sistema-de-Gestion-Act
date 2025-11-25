from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.sala_carrera import SalaCarreraCreate
from app.crud.sala_carrera import crear_relacion

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/sala-carrera/")
def crear_sala_carrera(relacion: SalaCarreraCreate, db: Session = Depends(get_db)):
    return crear_relacion(db, relacion)