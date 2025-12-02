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

def listar_docentes_por_sede(db: Session, id_sede: int):
    return db.query(Docente).filter(Docente.sede_id == id_sede).all()

def obtener_docente(db: Session, docente_id: int):
    return db.query(Docente).filter(Docente.id == docente_id).first()

def actualizar_docente(db: Session, id_docente: int, docente_data: DocenteCreate):
    docente = db.query(Docente).filter(Docente.id == id_docente).first()
    if not docente:
        return None

    for key, value in docente_data.dict().items():
        setattr(docente, key, value)

    db.commit()
    db.refresh(docente)
    return docente

def eliminar_docente(db: Session, docente_id: int):
    docente = db.query(Docente).filter(Docente.id == docente_id).first()
    if docente:
        db.delete(docente)
        db.commit()
    return docente