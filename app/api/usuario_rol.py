from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.usuario_rol import UsuarioRolCreate, UsuarioRolOut
from app.crud import usuario_rol as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/usuario-rol/", response_model=UsuarioRolOut)
def asignar_rol_usuario(data: UsuarioRolCreate, db: Session = Depends(get_db)):
    return crud.asignar_rol(db, data)

@router.get("/usuario-rol/{usuario_id}", response_model=list[UsuarioRolOut])
def ver_roles_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return crud.roles_por_usuario(db, usuario_id)