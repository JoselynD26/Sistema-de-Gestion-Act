from sqlalchemy.orm import Session
from app.models.curso import Curso
from app.schemas.curso import CursoCreate

def crear_curso(db: Session, datos: CursoCreate):
    nuevo = Curso(**datos.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_cursos(db: Session):
    return db.query(Curso).all()

def obtener_curso(db: Session, curso_id: int):
    return db.query(Curso).get(curso_id)

def eliminar_curso(db: Session, curso_id: int):
    curso = db.query(Curso).get(curso_id)
    if curso:
        db.delete(curso)
        db.commit()
    return curso