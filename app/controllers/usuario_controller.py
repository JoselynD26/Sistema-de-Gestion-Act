from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.schemas.usuario import UsuarioCreate
from app.schemas.usuario_rol import UsuarioRolCreate
from app.crud.usuario_rol import asignar_rol_a_usuario
from passlib.hash import bcrypt

def registrar_docente(db: Session, datos: UsuarioCreate):
    hashed = bcrypt.hash(datos.contrasena)
    nuevo = Usuario(
        nombres=datos.nombres,
        apellidos=datos.apellidos,
        correo=datos.correo,
        contrasena=hashed,
        rol="docente"
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    rol = db.query(Rol).filter_by(nombre="docente").first()
    if rol:
        asignar_rol_a_usuario(db, UsuarioRolCreate(id_usuario=nuevo.id, id_rol=rol.id))

    return nuevo