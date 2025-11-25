from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.dependencies.roles import obtener_usuario_actual
from app.models.usuario import Usuario
from app.models.docente import Docente
from app.models.reserva import Reserva
from app.models.notificacion import Notificacion
from app.models.sede import Sede
from app.core.seguridad import solo_admin 
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/panel-admin/")
def ver_panel_admin(usuario=Depends(solo_admin)):
    return {
        "mensaje": f"Acceso concedido al panel de administración, {usuario.nombres}"
    }

@router.get("/panel/inicio/")
def panel_inicio(db: Session = Depends(get_db), usuario: Usuario = Depends(obtener_usuario_actual)):
    if usuario.rol == "admin":
        return {
            "total_docentes": db.query(Docente).count(),
            "reservas_pendientes": db.query(Reserva).filter_by(estado="pendiente").count(),
            "usuarios_registrados": db.query(Usuario).count(),
            "total_sedes": db.query(Sede).count()
        }
    elif usuario.rol == "docente":
        return {
            "mis_reservas_activas": db.query(Reserva).filter_by(id_usuario=usuario.id_usuario, estado="aprobada").count(),
            "notificaciones_no_leidas": db.query(Notificacion).filter_by(id_usuario=usuario.id_usuario, leido=False).count(),
            "sedes_con_croquis": db.query(Sede).count()
        }
    else:
        return {"mensaje": "Rol no reconocido"}