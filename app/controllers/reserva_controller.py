from sqlalchemy.orm import Session
from app.models.reserva import Reserva
from app.schemas.reserva import ReservaCreate
from app.schemas.notificacion import NotificacionCreate
from app.crud.reserva import crear_reserva, obtener_reserva, actualizar_estado_reserva, listar_reservas
from app.crud.notificacion import crear_notificacion

def crear_reserva_controller(db: Session, datos: ReservaCreate):
    return crear_reserva(db, datos)

def listar_reservas_controller(db: Session):
    return listar_reservas(db)

def aprobar_reserva_controller(db: Session, reserva_id: int):
    reserva = obtener_reserva(db, reserva_id)
    if not reserva:
        return None
    reserva.estado = "aprobada"
    db.commit()
    db.refresh(reserva)
    notificar_reserva(db, reserva.id_usuario, "aprobada")
    return reserva

def cancelar_reserva_controller(db: Session, reserva_id: int):
    reserva = obtener_reserva(db, reserva_id)
    if not reserva:
        return None
    reserva.estado = "cancelada"
    db.commit()
    db.refresh(reserva)
    notificar_reserva(db, reserva.id_usuario, "cancelada")
    return reserva

def notificar_reserva(db: Session, usuario_id: int, estado: str):
    if estado == "aprobada":
        mensaje = "Tu reserva ha sido aprobada exitosamente."
        tipo = "reserva"
    elif estado == "cancelada":
        mensaje = "Tu reserva ha sido cancelada por el administrador."
        tipo = "cancelacion"
    else:
        mensaje = "Actualización de estado de reserva."
        tipo = "general"

    noti = NotificacionCreate(
        mensaje=mensaje,
        tipo=tipo,
        destinatario_id=usuario_id
    )
    crear_notificacion(db, noti)