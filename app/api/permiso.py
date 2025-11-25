from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.permiso import PermisoCreate, PermisoOut
from app.crud import permiso as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/permisos/", response_model=PermisoOut)
def crear_permiso(data: PermisoCreate, db: Session = Depends(get_db)):
    return crud.crear_permiso(db, data)

@router.get("/permisos/rol/{rol_id}", response_model=list[PermisoOut])
def ver_permisos_por_rol(rol_id: int, db: Session = Depends(get_db)):
    return crud.permisos_por_rol(db, rol_id)

@router.delete("/permisos/{permiso_id}")
def borrar_permiso(permiso_id: int, db: Session = Depends(get_db)):
    eliminado = crud.eliminar_permiso(db, permiso_id)
    if not eliminado:
        return {"mensaje": "Permiso no encontrado"}
    return {"mensaje": "Permiso eliminado correctamente"}

@router.delete("/permisos/rol/")
def borrar_por_rol_y_accion(rol_id: int, accion: str, db: Session = Depends(get_db)):
    eliminado = crud.eliminar_por_rol_y_accion(db, rol_id, accion)
    if not eliminado:
        return {"mensaje": "Permiso no encontrado"}
    return {"mensaje": f"Permiso '{accion}' eliminado del rol {rol_id}"}