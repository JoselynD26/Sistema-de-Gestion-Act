from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.curso_aula import CursoAulaCreate, CursoAulaOut
from app.crud import curso_aula as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/curso-aula/", response_model=CursoAulaOut)
def crear_relacion_curso_aula(relacion: CursoAulaCreate, db: Session = Depends(get_db)):
    return crud.crear_relacion(db, relacion)

@router.get("/curso-aula/", response_model=list[CursoAulaOut])
def listar_relaciones_curso_aula(db: Session = Depends(get_db)):
    return crud.listar_relaciones(db)

@router.delete("/curso-aula/")
def eliminar_relacion_curso_aula(id_curso: int, id_aula: int, db: Session = Depends(get_db)):
    relacion = crud.eliminar_relacion(db, id_curso, id_aula)
    if relacion:
        return {"mensaje": "Relación eliminada correctamente"}
    return {"mensaje": "Relación no encontrada"}