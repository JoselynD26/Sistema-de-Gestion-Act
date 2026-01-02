from sqlalchemy.orm import Session
from app.models.horario_cancelado import HorarioCancelado
from app.schemas.horario_cancelado import HorarioCanceladoCreate

def create_horario_cancelado(db: Session, obj_in: HorarioCanceladoCreate) -> HorarioCancelado:
    db_obj = HorarioCancelado(
        horario_id=obj_in.horario_id,
        fecha=obj_in.fecha,
        motivo=obj_in.motivo,
        estado=obj_in.estado
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_cancelaciones_by_horario(db: Session, horario_id: int):
    return db.query(HorarioCancelado).filter(HorarioCancelado.horario_id == horario_id).all()
