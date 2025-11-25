from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.usuario import UsuarioCreate, UsuarioOut
from app.crud.usuario import (
    crear_usuario,
    autenticar_usuario,
    listar_usuarios,
    obtener_usuario,
    eliminar_usuario,
    crear_usuario_para_docente,
    docentes_sin_usuario
)
from app.dependencies.roles import verificar_rol, obtener_usuario_actual
from app.models.usuario import Usuario
from app.auth.jwt_handler import crear_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear usuario (solo admin)
@router.post("/usuarios/", response_model=UsuarioOut, dependencies=[Depends(verificar_rol("admin"))])
def registrar(data: UsuarioCreate, db: Session = Depends(get_db)):
    return crear_usuario(db, data)

# Login y generación de token
@router.post("/usuarios/login/")
def login(correo: str, contrasena: str, db: Session = Depends(get_db)):
    usuario = autenticar_usuario(db, correo, contrasena)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = crear_token(usuario.id_usuario)
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": usuario.correo,
        "rol": usuario.rol
    }

# Listar todos los usuarios (solo admin)
@router.get("/usuarios/", response_model=list[UsuarioOut], dependencies=[Depends(verificar_rol("admin"))])
def listar(db: Session = Depends(get_db)):
    return listar_usuarios(db)

# Obtener usuario por ID (solo admin)
@router.get("/usuarios/{usuario_id}", response_model=UsuarioOut, dependencies=[Depends(verificar_rol("admin"))])
def obtener(usuario_id: int, db: Session = Depends(get_db)):
    return obtener_usuario(db, usuario_id)

# Eliminar usuario (solo admin)
@router.delete("/usuarios/{usuario_id}", dependencies=[Depends(verificar_rol("admin"))])
def eliminar(usuario_id: int, db: Session = Depends(get_db)):
    return eliminar_usuario(db, usuario_id)

# Crear cuenta para docente (solo admin)
@router.post("/usuarios/docente/", response_model=UsuarioOut, dependencies=[Depends(verificar_rol("admin"))])
def crear_para_docente(data: UsuarioCreate, db: Session = Depends(get_db)):
    return crear_usuario_para_docente(db, data)

# Listar docentes sin cuenta (solo admin)
@router.get("/usuarios/docentes-sin-cuenta/", dependencies=[Depends(verificar_rol("admin"))])
def listar_docentes_sin_usuario(db: Session = Depends(get_db)):
    return docentes_sin_usuario(db)

# Editar perfil (solo docente)
@router.put("/usuarios/editar/", response_model=UsuarioOut, dependencies=[Depends(verificar_rol("docente"))])
def editar_mi_perfil(data: UsuarioCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(obtener_usuario_actual)):
    actual = db.query(Usuario).get(usuario.id_usuario)
    if not actual:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for campo, valor in data.dict(exclude_unset=True).items():
        setattr(actual, campo, valor)
    db.commit()
    db.refresh(actual)
    return actual