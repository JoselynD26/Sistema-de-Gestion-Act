from sqlalchemy.orm import Session
from app.models.sala import Sala
from app.schemas.sala import SalaCreate

# Crear sala
def crear_sala(db: Session, datos: SalaCreate):
    nueva = Sala(**datos.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return {
        "id": nueva.id,
        "nombre": nueva.nombre,
        "sede_id": nueva.sede_id,
        "sede_nombre": nueva.sede.nombre if nueva.sede else None
    }

# Listar salas por sede
def listar_salas_por_sede(db: Session, sede_id: int):
    salas = db.query(Sala).filter(Sala.sede_id == sede_id).all()
    return [
        {
            "id": s.id,
            "nombre": s.nombre,
            "sede_id": s.sede_id,
            "sede_nombre": s.sede.nombre if s.sede else None
        }
        for s in salas
    ]

# Obtener sala por ID
def obtener_sala(db: Session, sala_id: int):
    s = db.query(Sala).filter(Sala.id == sala_id).first()
    if not s:
        return None
    return {
        "id": s.id,
        "nombre": s.nombre,
        "sede_id": s.sede_id,
        "sede_nombre": s.sede.nombre if s.sede else None
    }

# Actualizar sala
def actualizar_sala(db: Session, sala_id: int, datos: SalaCreate):
    sala = db.query(Sala).filter(Sala.id == sala_id).first()
    if not sala:
        return None
    for key, value in datos.dict().items():
        setattr(sala, key, value)
    db.commit()
    db.refresh(sala)
    return {
        "id": sala.id,
        "nombre": sala.nombre,
        "sede_id": sala.sede_id,
        "sede_nombre": sala.sede.nombre if sala.sede else None
    }

# Eliminar sala
def eliminar_sala(db: Session, sala_id: int):
    sala = db.query(Sala).filter(Sala.id == sala_id).first()
    if not sala:
        return None
    db.delete(sala)
    db.commit()
    return {"msg": f"Sala con id {sala_id} eliminada"}