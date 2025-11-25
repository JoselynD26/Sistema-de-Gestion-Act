from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.curso import CursoCreate, CursoOut
from app.crud import curso as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/cursos/", response_model=CursoOut)
def crear_curso(curso: CursoCreate, db: Session = Depends(get_db)):
    return crud.crear_curso(db, curso)

@router.get("/cursos/", response_model=list[CursoOut])
def listar_cursos(db: Session = Depends(get_db)):
    return crud.listar_cursos(db)

@router.get("/cursos/{id_curso}", response_model=CursoOut)
def obtener_curso(id_curso: int, db: Session = Depends(get_db)):
    return crud.obtener_curso(db, id_curso)

@router.delete("/cursos/{id_curso}")
def eliminar_curso(id_curso: int, db: Session = Depends(get_db)):
    curso = crud.eliminar_curso(db, id_curso)
    if curso:
        return {"mensaje": "Curso eliminado correctamente"}
    return {"mensaje": "Curso no encontrado"}