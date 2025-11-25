from sqlalchemy.orm import Session
from app.models.usuario_rol import UsuarioRol
from app.schemas.usuario_rol import UsuarioRolCreate

def asignar_rol_a_usuario(db: Session, datos: UsuarioRolCreate):
    nuevo = UsuarioRol(**datos.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_roles_por_usuario(db: Session, usuario_id: int):
    return db.query(UsuarioRol).filter_by(id_usuario=usuario_id).all()