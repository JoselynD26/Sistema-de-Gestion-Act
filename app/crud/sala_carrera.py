from sqlalchemy.orm import Session
from app.models.sala_carrera import SalaCarrera
from app.schemas.sala_carrera import SalaCarreraCreate

def crear_relacion(db: Session, data: SalaCarreraCreate):
    nueva = SalaCarrera(**data.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva