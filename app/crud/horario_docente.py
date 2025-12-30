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


def actualizar_horario_docente(db: Session, horario_id: int, data):
    horario = db.query(HorarioDocente).filter(HorarioDocente.id == horario_id).first()
    if not horario:
        return None
    
    # Si viene como objeto Pydantic, convertir a dict
    if hasattr(data, "dict"):
        update_data = data.dict(exclude_unset=True)
    elif isinstance(data, dict):
        update_data = data
    else:
        # Fallback básico si es otro tipo de objeto
        update_data = {k: v for k, v in data.__dict__.items() if v is not None}
    
    for key, value in update_data.items():
        if hasattr(horario, key):
             setattr(horario, key, value)
    
    db.commit()
    db.refresh(horario)
    return horario


def eliminar_horario_docente(db: Session, horario_id: int):
    horario = db.query(HorarioDocente).filter(HorarioDocente.id == horario_id).first()
    if not horario:
        return False
    
    db.delete(horario)
    db.commit()
    return True
