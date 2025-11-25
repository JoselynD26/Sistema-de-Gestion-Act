from sqlalchemy.orm import Session
from app.models.croquis import Croquis
from app.schemas.croquis import CroquisCreate

def crear_croquis(db: Session, datos: CroquisCreate):
    nuevo = Croquis(**datos.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_croquis(db: Session):
    return db.query(Croquis).all()

def obtener_croquis(db: Session, croquis_id: int):
    return db.query(Croquis).get(croquis_id)

def eliminar_croquis(db: Session, croquis_id: int):
    croquis = db.query(Croquis).get(croquis_id)
    if croquis:
        db.delete(croquis)
        db.commit()
    return croquis