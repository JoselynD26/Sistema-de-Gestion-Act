from sqlalchemy.orm import Session
from app.models.docente_sala import DocenteSala
from app.schemas.docente_sala import DocenteSalaCreate

def crear_docente_sala(db: Session, datos: DocenteSalaCreate):
    nueva = DocenteSala(**datos.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_docente_salas(db: Session):
    return db.query(DocenteSala).all()

def eliminar_docente_sala(db: Session, relacion_id: int):
    relacion = db.query(DocenteSala).get(relacion_id)
    if relacion:
        db.delete(relacion)
        db.commit()
    return relacion