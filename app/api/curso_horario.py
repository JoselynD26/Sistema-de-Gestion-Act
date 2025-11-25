from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.curso_horario import CursoHorarioCreate, CursoHorarioOut
from app.crud import curso_horario as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/curso-horario/", response_model=CursoHorarioOut)
def crear_relacion_curso_horario(relacion: CursoHorarioCreate, db: Session = Depends(get_db)):
    return crud.crear_relacion(db, relacion)

@router.get("/curso-horario/", response_model=list[CursoHorarioOut])
def listar_relaciones_curso_horario(db: Session = Depends(get_db)):
    return crud.listar_relaciones(db)

@router.delete("/curso-horario/")
def eliminar_relacion_curso_horario(id_curso: int, id_horario: int, db: Session = Depends(get_db)):
    relacion = crud.eliminar_relacion(db, id_curso, id_horario)
    if relacion:
        return {"mensaje": "Relación eliminada correctamente"}
    return {"mensaje": "Relación no encontrada"}