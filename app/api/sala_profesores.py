from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.sala_profesores import SalaProfesoresCreate, SalaProfesoresOut
from app.crud.sala_profesores import crear_sala, listar_salas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/salas/", response_model=SalaProfesoresOut)
def crear_sala_profesores(sala: SalaProfesoresCreate, db: Session = Depends(get_db)):
    return crear_sala(db, sala)

@router.get("/salas/", response_model=list[SalaProfesoresOut])
def listar_salas_profesores(db: Session = Depends(get_db)):
    return listar_salas(db)