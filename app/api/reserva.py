from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.config import get_db
from app.schemas.reserva import ReservaCreate, ReservaOut
from app.core.seguridad import verificar_rol, obtener_usuario_actual
from app.controllers.reserva_controller import (
    crear_reserva_controller,
    aprobar_reserva_controller,
    cancelar_reserva_controller,
    listar_reservas_controller
)
from app.models.reserva import Reserva
from app.models.usuario import Usuario

router = APIRouter()


@router.post("/reservas/", response_model=ReservaOut, dependencies=[Depends(verificar_rol("docente"))])
def crear(data: ReservaCreate, db: Session = Depends(get_db)):
    return crear_reserva_controller(db, data)

@router.get("/reservas/", response_model=list[ReservaOut], dependencies=[Depends(verificar_rol("admin"))])
def listar(db: Session = Depends(get_db)):
    return listar_reservas_controller(db)

@router.post("/reservas/aprobar/{id_reserva}", dependencies=[Depends(verificar_rol("admin"))])
def aprobar(id_reserva: int, db: Session = Depends(get_db)):
    return aprobar_reserva_controller(db, id_reserva)

@router.post("/reservas/cancelar/{reserva_id}", dependencies=[Depends(verificar_rol("admin"))])
def cancelar(reserva_id: int, db: Session = Depends(get_db)):
    return cancelar_reserva_controller(db, reserva_id)

@router.get("/reservas/mis/", response_model=list[ReservaOut], dependencies=[Depends(verificar_rol("docente"))])
def mis_reservas(db: Session = Depends(get_db), usuario: Usuario = Depends(obtener_usuario_actual)):
    if not usuario.id_docente:
        raise HTTPException(status_code=400, detail="El usuario no tiene un docente asociado")
    return db.query(Reserva).filter_by(id_docente=usuario.id_docente).all()