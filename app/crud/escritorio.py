from sqlalchemy.orm import Session
from app.models.escritorio import Escritorio
from app.schemas.escritorio import EscritorioCreate

def crear_escritorio(db: Session, datos: EscritorioCreate):
    nuevo = Escritorio(**datos.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_escritorios(db: Session):
    return db.query(Escritorio).all()

def listar_escritorios_por_sala(db: Session, sala_id: int):
    return db.query(Escritorio).filter_by(id_sala=sala_id).all()

def listar_escritorios_por_carrera(db: Session, carrera_id: int):
    return db.query(Escritorio).filter_by(id_carrera=carrera_id).all()

def obtener_escritorio(db: Session, escritorio_id: int):
    return db.query(Escritorio).get(escritorio_id)

def eliminar_escritorio(db: Session, escritorio_id: int):
    esc = db.query(Escritorio).get(escritorio_id)
    if esc:
        db.delete(esc)
        db.commit()
    return esc

def asignar_docente_a_escritorio(db: Session, escritorio_id: int, docente_id: int):
    esc = db.query(Escritorio).get(escritorio_id)
    if not esc:
        return None
    esc.id_docente = docente_id
    db.commit()
    return esc