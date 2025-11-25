from sqlalchemy.orm import Session
from app.models.docente_materia import DocenteMateria
from app.schemas.docente_materia import DocenteMateriaCreate

def crear_relacion(db: Session, data: DocenteMateriaCreate):
    nueva = DocenteMateria(**data.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva