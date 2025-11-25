from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.sala import SalaCreate
from app.crud import sala as crud
from app.dependencies.roles import verificar_roles
from app.dependencies.permisos import verificar_permiso_db

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/salas/")
def crear_sala(data: SalaCreate, db: Session = Depends(get_db)):
    return crud.crear_sala(db, data)

@router.get("/salas/sede/{sede_id}")
def listar_por_sede(sede_id: int, db: Session = Depends(get_db)):
    return crud.listar_salas_por_sede(db, sede_id)

@router.get("/salas/{sala_id}")
def obtener_sala(sala_id: int, db: Session = Depends(get_db)):
    return crud.obtener_sala(db, sala_id)

# Alternativas protegidas por roles o permisos
@router.post("/salas/roles/")
def crear_sala_por_rol(
    usuario_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(verificar_roles(["admin", "coordinador"]))
):
    # lógica de creación aquí
    pass

@router.post("/salas/permisos/")
def crear_sala_por_permiso(
    usuario_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(verificar_permiso_db("crear_sala"))
):
    # lógica de creación aquí
    pass