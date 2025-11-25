from sqlalchemy.orm import Session
from app.models.rol import Rol
from app.schemas.rol import RolCreate

def crear_rol(db: Session, datos: RolCreate):
    if datos.nombre not in ["admin", "docente"]:
        raise ValueError("Rol inválido. Solo se permite 'admin' o 'docente'")
    nuevo = Rol(**datos.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_roles(db: Session):
    return db.query(Rol).filter(Rol.nombre.in_(["admin", "docente"])).all()

def obtener_rol(db: Session, rol_id: int):
    return db.query(Rol).get(rol_id)