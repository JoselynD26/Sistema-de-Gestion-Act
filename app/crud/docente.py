from sqlalchemy.orm import Session
from app.models.docente import Docente
from app.schemas.docente import DocenteCreate

def crear_docente(db: Session, datos: DocenteCreate):
    nuevo = Docente(**datos.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_docentes(db: Session):
    return db.query(Docente).all()

def obtener_docente(db: Session, docente_id: int):
    return db.query(Docente).get(docente_id)

def eliminar_docente(db: Session, docente_id: int):
    docente = db.query(Docente).get(docente_id)
    if docente:
        db.delete(docente)
        db.commit()
    return docente