from sqlalchemy.orm import Session
from app.models.horario_docente import HorarioDocente

def crear_horario_docente(db: Session, data):
    nuevo = HorarioDocente(
        docente_id=data.docente_id,
        curso_id=data.curso_id,
        materia_id=data.materia_id,
        aula_id=data.aula_id,
        dia=data.dia,
        hora_inicio=data.hora_inicio,
        hora_fin=data.hora_fin,
        estado="activo"
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def listar_por_docente(db: Session, docente_id: int):
    return db.query(HorarioDocente)\
        .filter(HorarioDocente.docente_id == docente_id)\
        .order_by(HorarioDocente.dia, HorarioDocente.hora_inicio)\
        .all()
