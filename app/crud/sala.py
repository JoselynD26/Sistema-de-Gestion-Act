from sqlalchemy.orm import Session
from app.models.sala import Sala
from app.schemas.sala import SalaCreate

def get_sala(db: Session, sala_id: int):
    return db.query(Sala).filter(Sala.id == sala_id).first()

def get_salas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Sala).offset(skip).limit(limit).all()

def create_sala(db: Session, sala: SalaCreate):
    db_sala = Sala(**sala.dict())
    db.add(db_sala)
    db.commit()
    db.refresh(db_sala)
    return db_sala

def delete_sala(db: Session, sala_id: int):
    db_sala = db.query(Sala).filter(Sala.id == sala_id).first()
    if db_sala:
        db.delete(db_sala)
        db.commit()
    return db_sala