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

def actualizar_carrera(db: Session, id_carrera: int, carrera_data):
    carrera = db.query(Carrera).filter(Carrera.id == id_carrera).first()  

    if not carrera:
        return None

    for key, value in carrera_data.dict().items():
        setattr(carrera, key, value)

    db.commit()
    db.refresh(carrera)
    return carrera

def eliminar_carrera(db: Session, carrera_id: int):
    carrera = db.query(Carrera).get(carrera_id)
    if carrera:
        db.delete(carrera)
        db.commit()
    return carrera