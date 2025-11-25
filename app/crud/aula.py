from sqlalchemy.orm import Session
from app.models.aula import Aula
from app.schemas.aula import AulaCreate

def crear_aula(db: Session, datos: AulaCreate):
    nueva = Aula(**datos.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_aulas(db: Session):
    return db.query(Aula).all()

def obtener_aula(db: Session, aula_id: int):
    return db.query(Aula).get(aula_id)

def eliminar_aula(db: Session, aula_id: int):
    aula = db.query(Aula).get(aula_id)
    if aula:
        db.delete(aula)
        db.commit()
    return aula