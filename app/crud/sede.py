from sqlalchemy.orm import Session
from app.models.sede import Sede
from app.schemas.sede import SedeCreate

def crear_sede(db: Session, datos: SedeCreate):
    nueva = Sede(**datos.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_sedes(db: Session):
    return db.query(Sede).all()

def obtener_sede(db: Session, sede_id: int):
    return db.query(Sede).get(sede_id)

def actualizar_sede(db: Session, id_sede: int, data):
    sede = db.query(Sede).filter(Sede.id == id_sede).first()  

    if not sede:
        return None

    for key, value in data.dict().items():
        setattr(sede, key, value)

    db.commit()
    db.refresh(sede)
    return sede

def eliminar_sede(db: Session, sede_id: int):
    sede = db.query(Sede).get(sede_id)
    if sede:
        db.delete(sede)
        db.commit()
    return sede