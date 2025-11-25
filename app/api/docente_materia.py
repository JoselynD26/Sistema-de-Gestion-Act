from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.docente_materia import DocenteMateriaCreate
from app.crud.docente_materia import crear_relacion

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/docente-materia/")
def crear_docente_materia(relacion: DocenteMateriaCreate, db: Session = Depends(get_db)):
    return crear_relacion(db, relacion)