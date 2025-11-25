from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.models.usuario_rol import UsuarioRol
from app.schemas.usuario_rol import UsuarioRolCreate
from passlib.hash import bcrypt

def crear_usuario(db: Session, datos: UsuarioCreate):
    hashed = bcrypt.hash(datos.contrasena)
    nuevo = Usuario(
        nombres=datos.nombres,
        apellidos=datos.apellidos,
        correo=datos.correo,
        contrasena=hashed,
        rol=datos.rol,
        id_docente=datos.id_docente
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def autenticar_usuario(db: Session, correo: str, contrasena: str):
    usuario = db.query(Usuario).filter_by(correo=correo).first()
    if not usuario or not bcrypt.verify(contrasena, usuario.contrasena):
        return None
    return usuario

def listar_usuarios(db: Session):
    return db.query(Usuario).all()

def obtener_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).get(usuario_id)

def eliminar_usuario(db: Session, usuario_id: int):
    usuario = db.query(Usuario).get(usuario_id)
    if usuario:
        db.delete(usuario)
        db.commit()
    return usuario

def crear_usuario_para_docente(db: Session, datos: UsuarioCreate):
    hashed = bcrypt.hash(datos.contrasena)
    nuevo = Usuario(
        correo=datos.correo,
        contrasena=hashed,
        rol="docente",
        id_docente=datos.id_docente
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def docentes_sin_usuario(db: Session):
    from app.models.docente import Docente
    return db.query(Docente).filter(~Docente.id.in_(
        db.query(Usuario.id_docente).filter(Usuario.id_docente.isnot(None))
    )).all()

def asignar_rol(db: Session, data: UsuarioRolCreate):
    nuevo = UsuarioRol(**data.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def roles_por_usuario(db: Session, usuario_id: int):
    return db.query(UsuarioRol).filter_by(id_usuario=usuario_id).all()