from sqlalchemy.orm import Session
from app.models.docente_carrera import DocenteCarrera
from app.schemas.docente_carrera import DocenteCarreraCreate

def crear_relacion(db: Session, data: DocenteCarreraCreate):
    nueva = DocenteCarrera(**data.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva