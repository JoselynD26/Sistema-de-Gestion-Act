from sqlalchemy.orm import Session
from app.models.plaza import Plaza
from app.schemas.plaza import PlazaCreate

def crear_plaza(db: Session, datos: PlazaCreate):
    nueva = Plaza(**datos.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_plazas_por_sede(db: Session, sede_id: int):
    return db.query(Plaza).filter(Plaza.sede_id == sede_id).all()

def obtener_plaza(db: Session, plaza_id: int):
    return db.query(Plaza).filter(Plaza.id == plaza_id).first()

def actualizar_croquis_plaza(db: Session, plaza_id: int, croquis_url: str):
    plaza = db.query(Plaza).filter(Plaza.id == plaza_id).first()
    if plaza:
        plaza.croquis_url = croquis_url
        db.commit()
        db.refresh(plaza)
    return plaza