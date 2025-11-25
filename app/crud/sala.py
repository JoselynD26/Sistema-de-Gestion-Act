from sqlalchemy.orm import Session
from app.models.sala import Sala
from app.schemas.sala import SalaCreate

def crear_sala(db: Session, datos: SalaCreate):
    nueva = Sala(**datos.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_salas_por_sede(db: Session, sede_id: int):
    return db.query(Sala).filter_by(id_sede=sede_id).all()

def obtener_sala(db: Session, sala_id: int):
    return db.query(Sala).get(sala_id)