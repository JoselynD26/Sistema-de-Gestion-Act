from sqlalchemy.orm import Session
from app.models.rol_permiso import RolPermiso
from app.schemas.rol_permiso import RolPermisoCreate

def crear_rol_permiso(db: Session, datos: RolPermisoCreate):
    nuevo = RolPermiso(**datos.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_rol_permisos(db: Session):
    return db.query(RolPermiso).all()

def eliminar_rol_permiso(db: Session, permiso_id: int):
    permiso = db.query(RolPermiso).get(permiso_id)
    if permiso:
        db.delete(permiso)
        db.commit()
    return permiso