from sqlalchemy.orm import Session
from app.models.materia import Materia
from app.schemas.materia import MateriaCreate

def crear_materia(db: Session, datos: MateriaCreate):
    nueva = Materia(**datos.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_materias(db: Session):
    return db.query(Materia).all()

def obtener_materia(db: Session, materia_id: int):
    return db.query(Materia).get(materia_id)

def eliminar_materia(db: Session, materia_id: int):
    materia = db.query(Materia).get(materia_id)
    if materia:
        db.delete(materia)
        db.commit()
    return materia