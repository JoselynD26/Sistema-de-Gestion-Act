from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.controllers.curso_vinculacion import vista_cursos_con_vinculaciones, vista_cursos_con_detalle

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/panel/cursos-vinculados/")
def ver_cursos_vinculados(db: Session = Depends(get_db)):
    return vista_cursos_con_vinculaciones(db)

@router.get("/panel/cursos-detalle/")
def ver_cursos_con_detalle(db: Session = Depends(get_db)):
    return vista_cursos_con_detalle(db)