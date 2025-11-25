from sqlalchemy.orm import Session
from app.models.curso_horario import CursoHorario
from app.schemas.curso_horario import CursoHorarioCreate

def crear_curso_horario(db: Session, datos: CursoHorarioCreate):
    nueva = CursoHorario(**datos.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_curso_horarios(db: Session):
    return db.query(CursoHorario).all()

def eliminar_curso_horario(db: Session, id_curso: int, id_horario: int):
    relacion = db.query(CursoHorario).filter_by(id_curso=id_curso, id_horario=id_horario).first()
    if relacion:
        db.delete(relacion)
        db.commit()
    return relacion