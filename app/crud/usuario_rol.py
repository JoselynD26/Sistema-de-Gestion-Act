from sqlalchemy.orm import Session
from app.models.usuario_rol import UsuarioRol
from app.schemas.usuario_rol import UsuarioRolCreate

# -------------------
# Asignar rol a usuario
# -------------------
def asignar_rol_a_usuario(db: Session, datos: UsuarioRolCreate) -> UsuarioRol:
    """
    Asigna un rol a un usuario en la tabla UsuarioRol.
    """
    nuevo = UsuarioRol(**datos.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# -------------------
# Listar roles por usuario
# -------------------
def listar_roles_por_usuario(db: Session, usuario_id: int):
    """
    Devuelve todos los registros UsuarioRol asociados a un usuario.
    """
    return db.query(UsuarioRol).filter(UsuarioRol.id_usuario == usuario_id).all()

# -------------------
# Alias para compatibilidad con dependencias
# -------------------
def roles_por_usuario(db: Session, usuario_id: int):
    """
    Alias de listar_roles_por_usuario, usado en dependencias de seguridad.
    """
    return listar_roles_por_usuario(db, usuario_id)