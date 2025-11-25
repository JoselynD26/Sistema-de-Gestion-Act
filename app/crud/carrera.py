from sqlalchemy.orm import Session
from app.models.carrera import Carrera
from app.schemas.carrera import CarreraCreate

def crear_carrera(db: Session, datos: CarreraCreate):
    nueva = Carrera(**datos.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_carreras(db: Session):
    return db.query(Carrera).all()

def obtener_carrera(db: Session, carrera_id: int):
    return db.query(Carrera).get(carrera_id)

def eliminar_carrera(db: Session, carrera_id: int):
    carrera = db.query(Carrera).get(carrera_id)
    if carrera:
        db.delete(carrera)
        db.commit()
    return carrera