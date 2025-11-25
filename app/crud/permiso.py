from sqlalchemy.orm import Session
from app.models.permiso import Permiso
from app.schemas.permiso import PermisoCreate

def crear_permiso(db: Session, datos: PermisoCreate):
    nuevo = Permiso(**datos.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_permisos_por_rol(db: Session, rol_id: int):
    return db.query(Permiso).filter_by(id_rol=rol_id).all()

def eliminar_permiso(db: Session, permiso_id: int):
    permiso = db.query(Permiso).get(permiso_id)
    if permiso:
        db.delete(permiso)
        db.commit()
    return permiso

def eliminar_permiso_por_rol_y_accion(db: Session, rol_id: int, accion: str):
    permiso = db.query(Permiso).filter_by(id_rol=rol_id, accion=accion).first()
    if permiso:
        db.delete(permiso)
        db.commit()
    return permiso