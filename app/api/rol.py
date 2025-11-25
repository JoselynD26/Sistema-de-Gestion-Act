from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.rol import RolCreate, RolOut
from app.schemas.usuario_rol import UsuarioRolCreate, UsuarioRolOut
from app.crud import rol as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/roles/", response_model=RolOut)
def crear_rol(data: RolCreate, db: Session = Depends(get_db)):
    return crud.crear_rol(db, data)

@router.get("/roles/", response_model=list[RolOut])
def listar_roles(db: Session = Depends(get_db)):
    return crud.listar_roles(db)

@router.get("/roles/{rol_id}", response_model=RolOut)
def obtener_rol(rol_id: int, db: Session = Depends(get_db)):
    return crud.obtener_rol(db, rol_id)

@router.post("/usuario-rol/", response_model=UsuarioRolOut)
def asignar_rol(data: UsuarioRolCreate, db: Session = Depends(get_db)):
    return crud.asignar_rol(db, data)

@router.get("/usuario-rol/{usuario_id}", response_model=list[UsuarioRolOut])
def ver_roles_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return crud.roles_por_usuario(db, usuario_id)