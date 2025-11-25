from sqlalchemy.orm import Session
from app.models.notificacion import Notificacion
from app.schemas.notificacion import NotificacionCreate

def crear_notificacion(db: Session, datos: NotificacionCreate):
    nueva = Notificacion(**datos.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def obtener_notificaciones_por_usuario(db: Session, usuario_id: int):
    return db.query(Notificacion).filter_by(destinatario_id=usuario_id).order_by(Notificacion.fecha.desc()).all()

def marcar_notificacion_como_leida(db: Session, notificacion_id: int):
    noti = db.query(Notificacion).get(notificacion_id)
    if not noti:
        return None
    noti.leido = True
    db.commit()
    return noti