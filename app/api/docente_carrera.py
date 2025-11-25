from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.docente_carrera import DocenteCarreraCreate
from app.crud.docente_carrera import crear_relacion

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/docente-carrera/")
def crear_docente_carrera(relacion: DocenteCarreraCreate, db: Session = Depends(get_db)):
    return crear_relacion(db, relacion)