from sqlalchemy.orm import Session
from app.models.horario import Horario
from app.models.curso import Curso
from app.schemas.horario import HorarioCreate
from datetime import date

def crear_horario(db: Session, datos: HorarioCreate):
    datos_dict = datos.dict()
    
    # Verificar si hay cursos disponibles
    primer_curso = db.query(Curso).first()
    
    if primer_curso:
        # Si hay cursos, usar el primero
        datos_dict['id_curso'] = primer_curso.id
        campos_validos = {'dia', 'hora_inicio', 'hora_fin', 'id_materia', 'id_docente', 'id_aula', 'id_curso', 'id_sede', 'fecha', 'estado'}
    else:
        # Si no hay cursos, omitir completamente el campo
        datos_dict.pop('id_curso', None)
        campos_validos = {'dia', 'hora_inicio', 'hora_fin', 'id_materia', 'id_docente', 'id_aula', 'id_sede', 'fecha', 'estado'}
    
    datos_filtrados = {k: v for k, v in datos_dict.items() if k in campos_validos}
    
    nuevo = Horario(**datos_filtrados)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_horario(db: Session, horario_id: int):
    return db.query(Horario).filter(Horario.id == horario_id).first()

def actualizar_horario(db: Session, horario_id: int, datos: HorarioCreate):
    horario = db.query(Horario).filter(Horario.id == horario_id).first()
    if not horario:
        return None
    
    datos_dict = datos.dict()
    
    # Mapear id_sede a sede_id si existe
    if 'id_sede' in datos_dict:
        datos_dict['sede_id'] = datos_dict.pop('id_sede')
    
    # Filtrar solo campos que existen en el modelo
    campos_validos = {'fecha', 'hora_inicio', 'hora_fin', 'estado', 'id_docente', 'id_materia', 'id_aula', 'sede_id'}
    
    for key, value in datos_dict.items():
        if key in campos_validos and value is not None:
            setattr(horario, key, value)
    
    db.commit()
    db.refresh(horario)
    return horario

def eliminar_horario(db: Session, horario_id: int):
    horario = db.query(Horario).filter(Horario.id == horario_id).first()
    if not horario:
        return None
    db.delete(horario)
    db.commit()
    return True

def listar_horarios_cancelados(db: Session, sede_id: int, fecha: date):
    return db.query(Horario).filter(
        Horario.id_sede == sede_id,
        Horario.fecha == fecha,
        Horario.estado == "cancelado"
    ).all()