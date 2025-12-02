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
    return db.get(Sede, sede_id)   # ✅ forma moderna

def actualizar_sede(db: Session, id_sede: int, data):
    sede = db.query(Sede).filter(Sede.id == id_sede).first()
    if not sede:
        return None

    for key, value in data.dict(exclude_unset=True).items():  # ✅ solo actualiza campos enviados
        setattr(sede, key, value)

    db.commit()
    db.refresh(sede)
    return sede

def eliminar_sede(db: Session, sede_id: int) -> bool:
    sede = db.get(Sede, sede_id)
    if sede:
        db.delete(sede)
        db.commit()
        return True
    return False