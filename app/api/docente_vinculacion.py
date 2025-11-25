from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.controllers.docente_vinculacion import vista_docentes_con_vinculaciones

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/panel/docentes-vinculados/")
def ver_docentes_vinculados(db: Session = Depends(get_db)):
    return vista_docentes_con_vinculaciones(db)