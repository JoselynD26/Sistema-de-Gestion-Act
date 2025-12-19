from sqlalchemy.orm import Session
from app.models.carrera import Carrera
from app.models.sede import Sede
from app.schemas.carrera import CarreraCreate

def crear_carrera(db: Session, datos: CarreraCreate):
    # Generar código único si es AUTO
    codigo = datos.codigo
    if codigo == "AUTO":
        # Generar código basado en el nombre
        base_codigo = datos.nombre[:3].upper()
        contador = 1
        while True:
            codigo_generado = f"{base_codigo}{contador:03d}"
            existe = db.query(Carrera).filter(Carrera.codigo == codigo_generado).first()
            if not existe:
                codigo = codigo_generado
                break
            contador += 1
    
    nueva = Carrera(nombre=datos.nombre, codigo=codigo)
    sedes = db.query(Sede).filter(Sede.id.in_(datos.sede_ids)).all()
    nueva.sedes = sedes
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    # construir salida con sede_ids
    return {
        "id": nueva.id,
        "nombre": nueva.nombre,
        "codigo": nueva.codigo,
        "sede_ids": [s.id for s in nueva.sedes]
    }
    
def listar_carreras(db: Session):
    carreras = db.query(Carrera).all()
    return [
        {
            "id": c.id,
            "nombre": c.nombre,
            "codigo": c.codigo,
            "sede_ids": [s.id for s in c.sedes]
        }
        for c in carreras
    ]


def listar_carreras_por_sede(db: Session, sede_id: int):
    return db.query(Carrera).join(Carrera.sedes).filter(Sede.id == sede_id).all()

def obtener_carrera(db: Session, carrera_id: int):
    return db.query(Carrera).get(carrera_id)

def actualizar_carrera(db: Session, id_carrera: int, carrera_data: CarreraCreate):
    carrera = db.query(Carrera).filter(Carrera.id == id_carrera).first()
    if not carrera:
        return None
    carrera.nombre = carrera_data.nombre
    sedes = db.query(Sede).filter(Sede.id.in_(carrera_data.sede_ids)).all()
    carrera.sedes = sedes
    db.commit()
    db.refresh(carrera)
    return carrera

def eliminar_carrera(db: Session, carrera_id: int):
    carrera = db.query(Carrera).get(carrera_id)
    if carrera:
        db.delete(carrera)
        db.commit()
    return carrera