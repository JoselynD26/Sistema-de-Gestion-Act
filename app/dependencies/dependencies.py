from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.models.rol import Rol
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
# Verificación por rol
# -------------------
def verificar_rol(requerido: str):
    """
    Dependencia que valida si el usuario tiene un rol específico.
    Ejemplo: Depends(verificar_rol("admin"))
    """
    def wrapper(usuario_id: int, db: Session = Depends(get_db)):
        # Obtener roles asociados al usuario
        roles = roles_por_usuario(db, usuario_id)
        ids = [r.id_rol for r in roles]

        # Buscar nombres de roles en la BD
        nombres = db.query(Rol).filter(Rol.id.in_(ids)).all()
        nombres_texto = [r.nombre for r in nombres]

        # Validar rol requerido
        if requerido not in ["admin", "docente"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rol no permitido"
            )
        if requerido not in nombres_texto:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado para este rol"
            )
    return wrapper

# -------------------
# Verificación por permiso
# -------------------
def verificar_permiso_db(accion: str):
    """
    Dependencia que valida si el usuario tiene permiso para ejecutar una acción.
    Ejemplo: Depends(verificar_permiso_db("crear_sala"))
    """
    def wrapper(usuario_id: int, db: Session = Depends(get_db)):
        # Obtener roles asociados al usuario
        roles = roles_por_usuario(db, usuario_id)
        ids_rol = [r.id_rol for r in roles]

        # Buscar permisos asociados a esos roles
        permisos = db.query(Permiso).filter(Permiso.id_rol.in_(ids_rol)).all()
        acciones_permitidas = [p.accion for p in permisos]

        # Validar acción requerida
        if accion not in acciones_permitidas:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tienes permiso para {accion}"
            )
    return wrapper