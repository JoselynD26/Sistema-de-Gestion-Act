from sqlalchemy.orm import Session
from app.models.curso_aula import CursoAula
from app.schemas.curso_aula import CursoAulaCreate

def crear_curso_aula(db: Session, datos: CursoAulaCreate):
    nueva = CursoAula(**datos.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_curso_aulas(db: Session):
    return db.query(CursoAula).all()

def eliminar_curso_aula(db: Session, id_curso: int, id_aula: int):
    relacion = db.query(CursoAula).filter_by(id_curso=id_curso, id_aula=id_aula).first()
    if relacion:
        db.delete(relacion)
        db.commit()
    return relacion