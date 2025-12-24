from sqlalchemy.orm import Session
from app.models.carrera import Carrera
from app.models.sede import Sede
from app.schemas.carrera import CarreraCreate
from typing import Optional

# Helper para convertir Carrera a dict
def carrera_to_dict(carrera: Carrera):
    return {
        "id": carrera.id,
        "nombre": carrera.nombre,
        "codigo": carrera.codigo,
        "sede_ids": [s.id for s in carrera.sedes]
    }

def crear_carrera(db: Session, datos: CarreraCreate):
    try:
        nueva = Carrera(
            nombre=datos.nombre,
            codigo=datos.codigo  # opcional, puede ser None
        )
        sedes = db.query(Sede).filter(Sede.id.in_(datos.sede_ids)).all()
        nueva.sedes = sedes
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return carrera_to_dict(nueva)
    except:
        db.rollback()
        raise

def listar_carreras(db: Session):
    carreras = db.query(Carrera).all()
    return [carrera_to_dict(c) for c in carreras]

def listar_carreras_por_sede(db: Session, sede_id: int):
    carreras = db.query(Carrera).join(Carrera.sedes).filter(Sede.id == sede_id).all()
    return [carrera_to_dict(c) for c in carreras]

def obtener_carrera(db: Session, carrera_id: int) -> Optional[dict]:
    carrera = db.get(Carrera, carrera_id)
    return carrera_to_dict(carrera) if carrera else None

def actualizar_carrera(db: Session, id_carrera: int, carrera_data: CarreraCreate):
    carrera = db.get(Carrera, id_carrera)
    if not carrera:
        return None
    try:
        carrera.nombre = carrera_data.nombre
        carrera.codigo = carrera_data.codigo  # opcional
        sedes = db.query(Sede).filter(Sede.id.in_(carrera_data.sede_ids)).all()
        carrera.sedes = sedes
        db.commit()
        db.refresh(carrera)
        return carrera_to_dict(carrera)
    except:
        db.rollback()
        raise

def eliminar_carrera(db: Session, carrera_id: int):
    carrera = db.get(Carrera, carrera_id)
    if carrera:
        try:
            db.delete(carrera)
            db.commit()
            return carrera_to_dict(carrera)
        except:
            db.rollback()
            raise
    return None