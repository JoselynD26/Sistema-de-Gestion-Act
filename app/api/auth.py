from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.usuario import UsuarioCreate, UsuarioLogin
from app.crud.usuario import crear_usuario, autenticar_usuario
from app.core.config import SessionLocal
from app.core.seguridad import crear_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/registro-admin/")
def registrar_admin(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if usuario.rol != "admin":
        raise HTTPException(status_code=400, detail="Solo se permite registrar admins desde aquí")
    return crear_usuario(db, usuario)

@router.post("/login/")
def login(datos: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = autenticar_usuario(db, datos.correo, datos.contrasena)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = crear_token(usuario.id, usuario.rol)
    return {
        "access_token": token,
        "token_type": "bearer",
        "rol": usuario.rol,
        "id": usuario.id,
        "nombres": usuario.nombres,
        "apellidos": usuario.apellidos
    }