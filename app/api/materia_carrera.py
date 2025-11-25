from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.materia_carrera import MateriaCarreraCreate, MateriaCarreraOut
from app.crud import materia_carrera as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/materia-carrera/", response_model=MateriaCarreraOut)
def crear_materia_carrera(relacion: MateriaCarreraCreate, db: Session = Depends(get_db)):
    return crud.crear_relacion(db, relacion)

@router.get("/materia-carrera/", response_model=list[MateriaCarreraOut])
def listar_materia_carrera(db: Session = Depends(get_db)):
    return crud.listar_relaciones(db)

@router.delete("/materia-carrera/")
def eliminar_materia_carrera(id_materia: int, id_carrera: int, db: Session = Depends(get_db)):
    relacion = crud.eliminar_relacion(db, id_materia, id_carrera)
    if relacion:
        return {"mensaje": "Relación eliminada correctamente"}
    return {"mensaje": "Relación no encontrada"}