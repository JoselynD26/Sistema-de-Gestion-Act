from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.models.rol import Rol
from app.models.permiso import Permiso
from app.crud.usuario_rol import roles_por_usuario

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verificar_rol(requerido: str):
    def wrapper(usuario_id: int, db: Session = Depends(get_db)):
        roles = roles_por_usuario(db, usuario_id)
        ids = [r.id_rol for r in roles]
        nombres = db.query(Rol).filter(Rol.id.in_(ids)).all()
        nombres_texto = [r.nombre for r in nombres]

        if requerido not in ["admin", "docente"]:
            raise HTTPException(status_code=400, detail="Rol no permitido")
        if requerido not in nombres_texto:
            raise HTTPException(status_code=403, detail="Acceso denegado para este rol")
    return wrapper

def verificar_permiso_db(accion: str):
    def wrapper(usuario_id: int, db: Session = Depends(get_db)):
        roles = roles_por_usuario(db, usuario_id)
        ids_rol = [r.id_rol for r in roles]

        permisos = db.query(Permiso).filter(Permiso.id_rol.in_(ids_rol)).all()
        acciones_permitidas = [p.accion for p in permisos]

        if accion not in acciones_permitidas:
            raise HTTPException(status_code=403, detail=f"No tienes permiso para {accion}")
    return wrapper