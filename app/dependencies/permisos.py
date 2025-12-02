from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.models.permiso import Permiso
from app.crud.usuario_rol import roles_por_usuario

# -------------------
# Conexión a la base
# -------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------
# Verificación de permisos
# -------------------
def verificar_permiso_db(accion: str):
    """
    Dependencia que valida si el usuario tiene permiso para ejecutar una acción.
    Se basa en los roles asociados al usuario y los permisos definidos en la BD.
    """
    def wrapper(usuario_id: int, db: Session = Depends(get_db)):
        # Obtener roles del usuario
        roles = roles_por_usuario(db, usuario_id)
        ids_rol = [r.id_rol for r in roles]

        # Obtener permisos asociados a esos roles
        permisos = db.query(Permiso).filter(Permiso.id_rol.in_(ids_rol)).all()
        acciones_permitidas = [p.accion for p in permisos]

        # Validar si la acción está permitida
        if accion not in acciones_permitidas:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tienes permiso para {accion}"
            )
    return wrapper