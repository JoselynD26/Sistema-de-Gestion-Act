from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.dependencies.roles import verificar_rol, obtener_usuario_actual
from app.models.notificacion import Notificacion
from app.models.usuario import Usuario

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/notificaciones/mis/", dependencies=[Depends(verificar_rol("docente"))])
def mis_notificaciones(db: Session = Depends(get_db), usuario: Usuario = Depends(obtener_usuario_actual)):
    return db.query(Notificacion).filter_by(id_usuario=usuario.id_usuario).all()