from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.materia import MateriaCreate, MateriaOut
from app.crud import materia as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/materias/", response_model=MateriaOut)
def crear_materia(materia: MateriaCreate, db: Session = Depends(get_db)):
    return crud.crear_materia(db, materia)

@router.get("/materias/", response_model=list[MateriaOut])
def listar_materias(db: Session = Depends(get_db)):
    return crud.listar_materias(db)

@router.get("/materias/{id_materia}", response_model=MateriaOut)
def obtener_materia(id_materia: int, db: Session = Depends(get_db)):
    return crud.obtener_materia(db, id_materia)

@router.delete("/materias/{id_materia}")
def eliminar_materia(id_materia: int, db: Session = Depends(get_db)):
    materia = crud.eliminar_materia(db, id_materia)
    if materia:
        return {"mensaje": "Materia eliminada correctamente"}
    return {"mensaje": "Materia no encontrada"}