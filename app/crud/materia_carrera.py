from sqlalchemy.orm import Session
from app.models.materia_carrera import MateriaCarrera
from app.schemas.materia_carrera import MateriaCarreraCreate

def crear_materia_carrera(db: Session, datos: MateriaCarreraCreate):
    nueva = MateriaCarrera(**datos.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_materia_carreras(db: Session):
    return db.query(MateriaCarrera).all()

def eliminar_materia_carrera(db: Session, id_materia: int, id_carrera: int):
    relacion = db.query(MateriaCarrera).filter_by(id_materia=id_materia, id_carrera=id_carrera).first()
    if relacion:
        db.delete(relacion)
        db.commit()
    return relacion