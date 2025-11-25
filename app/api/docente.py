from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.docente import DocenteCreate, DocenteOut
from app.crud import docente as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/docentes/", response_model=DocenteOut)
def crear_docente(docente: DocenteCreate, db: Session = Depends(get_db)):
    return crud.crear_docente(db, docente)

@router.get("/docentes/", response_model=list[DocenteOut])
def listar_docentes(db: Session = Depends(get_db)):
    return crud.listar_docentes(db)

@router.get("/docentes/{id_docente}", response_model=DocenteOut)
def obtener_docente(id_docente: int, db: Session = Depends(get_db)):
    return crud.obtener_docente(db, id_docente)

@router.delete("/docentes/{id_docente}")
def eliminar_docente(id_docente: int, db: Session = Depends(get_db)):
    docente = crud.eliminar_docente(db, id_docente)
    if docente:
        return {"mensaje": "Docente eliminado correctamente"}
    return {"mensaje": "Docente no encontrado"}