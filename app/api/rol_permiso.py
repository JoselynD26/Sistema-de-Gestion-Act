from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.controllers.rol_permiso_controller import vista_roles_con_permisos

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/panel/roles-permisos/")
def ver_roles_y_permisos(db: Session = Depends(get_db)):
    return vista_roles_con_permisos(db)