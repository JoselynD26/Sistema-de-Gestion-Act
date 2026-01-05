from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date, time
from app.core.config import SessionLocal
from app.models.horario import Horario
from app.models.materia import Materia
from app.models.aula import Aula
from app.models.docente import Docente
from app.models.curso import Curso

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/mis-materias/{docente_id}")
def obtener_mis_materias(docente_id: int, db: Session = Depends(get_db)):
    """Obtiene las materias asignadas al docente"""
    
    docente = db.query(Docente).filter(Docente.id == docente_id).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    
    materias = []
    for materia in docente.materias:
        materias.append({
            "id": materia.id,
            "nombre": materia.nombre,
            "carreras": [{"id": c.id, "nombre": c.nombre} for c in materia.carreras]
        })
    
    return materias

@router.get("/mi-horario/{docente_id}")
def obtener_mi_horario(docente_id: int, db: Session = Depends(get_db)):
    """Obtiene el horario del docente"""
    
    horarios = db.query(Horario).filter(Horario.id_docente == docente_id).all()
    
    resultado = []
    for horario in horarios:
        materia = db.query(Materia).filter(Materia.id == horario.id_materia).first()
        aula = db.query(Aula).filter(Aula.id == horario.id_aula).first()
        curso = db.query(Curso).filter(Curso.id == horario.id_curso).first() if horario.id_curso else None
        
        # Mostrar rango de horas si existen ambas, sino solo inicio
        hora_display = str(horario.hora_inicio) if horario.hora_inicio else "N/A"
        if horario.hora_inicio and horario.hora_fin:
            hora_display = f"{horario.hora_inicio} - {horario.hora_fin}"
        
        resultado.append({
            "id": horario.id,
            "dia": horario.dia,
            "fecha": horario.fecha,
            "hora_inicio": str(horario.hora_inicio) if horario.hora_inicio else None,
            "hora_fin": str(horario.hora_fin) if horario.hora_fin else None,
            "hora": hora_display,
            "estado": horario.estado,
            "materia_nombre": materia.nombre if materia else "N/A",
            "aula_nombre": aula.nombre if aula else "N/A",
            "aula_capacidad": aula.capacidad if aula else 0,
            "curso_nombre": curso.nombre if curso else "N/A",
            "curso_nivel": curso.nivel if curso else "N/A",
            "curso_paralelo": curso.paralelo if curso else "N/A"
        })
    
    return resultado

@router.post("/crear-horario")
def crear_horario_profesor(
    fecha: date,
    hora_inicio: time,
    hora_fin: time,
    materia_id: int,
    aula_id: int,
    docente_id: int,
    recurrente: bool = True,  # Por defecto crear horarios recurrentes
    semanas: int = 16,  # Número de semanas a crear (un semestre)
    db: Session = Depends(get_db)
):
    """Crear horario de clase (recurrente por defecto)"""
    from datetime import timedelta
    
    # Verificar que el docente tenga asignada la materia
    docente = db.query(Docente).filter(Docente.id == docente_id).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    
    materia_asignada = any(m.id == materia_id for m in docente.materias)
    if not materia_asignada:
        raise HTTPException(status_code=400, detail="No tienes asignada esta materia")
    
    # Obtener el día de la semana de la fecha inicial
    dia_semana = fecha.strftime("%A")
    # Traducir al español
    dias_es = {
        "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
        "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
    }
    dia_es = dias_es.get(dia_semana, dia_semana)
    
    horarios_creados = []
    
    if recurrente:
        # Crear horarios para las próximas semanas
        for i in range(semanas):
            fecha_clase = fecha + timedelta(weeks=i)
            
            # Verificar que el aula esté disponible en cada fecha
            conflicto = db.query(Horario).filter(
                and_(
                    Horario.id_aula == aula_id,
                    Horario.fecha == fecha_clase,
                    Horario.estado == "activo",
                    Horario.hora_inicio < hora_fin,
                    Horario.hora_fin > hora_inicio
                )
            ).first()
            
            if not conflicto:
                nuevo_horario = Horario(
                    dia=dia_es,
                    fecha=fecha_clase,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    estado="activo",
                    id_docente=docente_id,
                    id_materia=materia_id,
                    id_aula=aula_id,
                    id_curso=None,  # Permitir curso nulo temporalmente
                    id_sede=docente.sede_id
                )
                
                db.add(nuevo_horario)
                horarios_creados.append(fecha_clase.strftime("%Y-%m-%d"))
    else:
        # Crear solo un horario
        conflicto = db.query(Horario).filter(
            and_(
                Horario.id_aula == aula_id,
                Horario.fecha == fecha,
                Horario.estado == "activo",
                Horario.hora_inicio < hora_fin,
                Horario.hora_fin > hora_inicio
            )
        ).first()
        
        if conflicto:
            raise HTTPException(status_code=400, detail="Aula ocupada en ese horario")
        
        nuevo_horario = Horario(
            dia=dia_es,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            estado="activo",
            id_docente=docente_id,
            id_materia=materia_id,
            id_aula=aula_id,
            id_curso=None,  # Permitir curso nulo temporalmente
            id_sede=docente.sede_id
        )
        
        db.add(nuevo_horario)
        horarios_creados.append(fecha.strftime("%Y-%m-%d"))
    
    db.commit()
    
    return {
        "message": f"Horario{'s' if len(horarios_creados) > 1 else ''} creado{'s' if len(horarios_creados) > 1 else ''} exitosamente",
        "fechas_creadas": horarios_creados,
        "total": len(horarios_creados)
    }

@router.put("/actualizar-horario/{horario_id}")
def actualizar_horario_profesor(
    horario_id: int,
    fecha: date,
    hora_inicio: time,
    hora_fin: time,
    materia_id: int,
    aula_id: int,
    docente_id: int,
    db: Session = Depends(get_db)
):
    """Actualizar horario propio"""
    
    horario = db.query(Horario).filter(
        and_(
            Horario.id == horario_id,
            Horario.id_docente == docente_id
        )
    ).first()
    
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    
    # Verificar disponibilidad del aula (excluyendo el horario actual)
    conflicto = db.query(Horario).filter(
        and_(
            Horario.id != horario_id,
            Horario.id_aula == aula_id,
            Horario.fecha == fecha,
            Horario.estado == "activo",
            # Verificar solapamiento de horarios
            Horario.hora_inicio < hora_fin,
            Horario.hora_fin > hora_inicio
        )
    ).first()
    
    if conflicto:
        raise HTTPException(status_code=400, detail="Aula ocupada en ese horario")
    
    # Actualizar horario
    horario.fecha = fecha
    horario.hora_inicio = hora_inicio
    horario.hora_fin = hora_fin
    horario.id_materia = materia_id
    horario.id_aula = aula_id
    
    db.commit()
    
    return {"message": "Horario actualizado exitosamente"}

@router.delete("/eliminar-horario/{horario_id}")
def eliminar_horario_profesor(horario_id: int, docente_id: int, db: Session = Depends(get_db)):
    """Eliminar horario propio"""
    
    horario = db.query(Horario).filter(
        and_(
            Horario.id == horario_id,
            Horario.id_docente == docente_id
        )
    ).first()
    
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    
    db.delete(horario)
    db.commit()
    
    return {"message": "Horario eliminado exitosamente"}

@router.get("/cursos-disponibles/{sede_id}")
def obtener_cursos_disponibles(sede_id: int, db: Session = Depends(get_db)):
    """Obtiene cursos disponibles en la sede"""
    
    cursos = db.query(Curso).filter(Curso.sede_id == sede_id).all()
    
    resultado = []
    for curso in cursos:
        resultado.append({
            "id": curso.id,
            "nombre": curso.nombre,
            "carrera_id": curso.carrera_id
        })
    
    return resultado

@router.get("/mi-escritorio/{docente_id}")
def obtener_mi_escritorio(docente_id: int, db: Session = Depends(get_db)):
    """Obtiene el escritorio asignado al docente con información completa"""
    from app.models.escritorio import Escritorio
    from app.models.sala_profesores import SalaProfesores
    from app.models.carrera import Carrera
    
    escritorio = db.query(Escritorio).filter(Escritorio.docente_id == docente_id).first()
    
    if not escritorio:
        return {"asignado": False}
    
    # Obtener información de la sala
    sala = db.query(SalaProfesores).filter(SalaProfesores.id == escritorio.sala_id).first()
    
    # Obtener información de la carrera
    carrera = db.query(Carrera).filter(Carrera.id == escritorio.carrera_id).first()
    
    return {
        "id": escritorio.id,
        "codigo": escritorio.codigo,
        "sala_id": escritorio.sala_id,
        "sala_nombre": sala.nombre if sala else "N/A",
        "carrera_id": escritorio.carrera_id,
        "carrera_nombre": carrera.nombre if carrera else "N/A",
        "estado": escritorio.estado,
        "jornada": escritorio.jornada,
        "asignado": True
    }

@router.get("/escritorios-disponibles/{sede_id}")
def obtener_escritorios_disponibles(sede_id: int, db: Session = Depends(get_db)):
    """Obtiene escritorios disponibles (sin docente asignado) en la sede"""
    from app.models.escritorio import Escritorio
    from app.models.sala import Sala
    
    escritorios = db.query(Escritorio).join(Sala).filter(
        and_(
            Sala.sede_id == sede_id,
            Escritorio.docente_id == None
        )
    ).all()
    
    resultado = []
    for escritorio in escritorios:
        resultado.append({
            "id": escritorio.id,
            "codigo": escritorio.codigo,
            "sala_id": escritorio.sala_id,
            "carrera_id": escritorio.carrera_id
        })
    
    return resultado

@router.post("/solicitar-escritorio")
def solicitar_escritorio(
    escritorio_id: int,
    docente_id: int,
    motivo: str = "Solicitud de cambio de escritorio",
    db: Session = Depends(get_db)
):
    """Crear solicitud de asignación de escritorio (pendiente de aprobación)"""
    from app.models.reserva import Reserva
    
    # Crear solicitud como reserva de escritorio
    nueva_solicitud = Reserva(
        estado="pendiente",
        id_docente=docente_id,
        id_escritorio=escritorio_id
    )
    
    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud)
    
    return {"message": "Solicitud de escritorio enviada", "id": nueva_solicitud.id}

@router.get("/horario-aulas")
def obtener_horario_aulas(sede_id: int = Query(...), fecha: str = Query(...), db: Session = Depends(get_db)):
    """Obtiene el horario de ocupación de todas las aulas en una fecha específica"""
    from app.models.reserva import Reserva
    from datetime import datetime
    
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido")
    
    # Obtener todas las aulas de la sede
    aulas = db.query(Aula).filter(Aula.id_sede == sede_id).all()
    
    resultado = []
    
    for aula in aulas:
        # Obtener horarios regulares del aula para esa fecha
        horarios = db.query(Horario).filter(
            and_(
                Horario.id_aula == aula.id,
                Horario.fecha == fecha_obj,
                Horario.estado == "activo"
            )
        ).all()
        
        # Obtener reservas aprobadas del aula para esa fecha
        reservas = db.query(Reserva).filter(
            and_(
                Reserva.id_aula == aula.id,
                Reserva.fecha == fecha_obj,
                Reserva.estado == "aprobada"
            )
        ).all()
        
        ocupaciones = []
        
        # Procesar horarios regulares
        for horario in horarios:
            docente = db.query(Docente).filter(Docente.id == horario.id_docente).first()
            materia = db.query(Materia).filter(Materia.id == horario.id_materia).first()
            
            ocupaciones.append({
                "tipo": "clase",
                "hora_inicio": str(horario.hora_inicio) if horario.hora_inicio else "N/A",
                "hora_fin": str(horario.hora_fin) if horario.hora_fin else "21:10",
                "profesor": f"{docente.nombres} {docente.apellidos}" if docente else "N/A",
                "materia": materia.nombre if materia else "N/A",
                "estado": "ocupada"
            })
        
        # Procesar reservas
        for reserva in reservas:
            docente = db.query(Docente).filter(Docente.id == reserva.id_docente).first()
            
            ocupaciones.append({
                "tipo": "reserva",
                "hora_inicio": str(reserva.hora_inicio) if reserva.hora_inicio else "N/A",
                "hora_fin": str(reserva.hora_fin) if reserva.hora_fin else "21:10",
                "profesor": f"{docente.nombres} {docente.apellidos}" if docente else "N/A",
                "materia": reserva.motivo or "Reserva",
                "estado": "reservada"
            })
        
        # Ordenar ocupaciones por hora
        ocupaciones.sort(key=lambda x: x["hora_inicio"])
        
        resultado.append({
            "id": aula.id,
            "nombre": aula.nombre,
            "capacidad": aula.capacidad,
            "ocupaciones": ocupaciones,
            "disponible": len(ocupaciones) == 0
        })
    
    return resultado
@router.get("/mi-croquis/{docente_id}")
def obtener_mi_croquis(docente_id: int, db: Session = Depends(get_db)):
    from app.models.escritorio import Escritorio
    from app.models.sala_profesores import SalaProfesores

    escritorio = (
        db.query(Escritorio)
        .filter(Escritorio.docente_id == docente_id)
        .first()
    )

    if not escritorio:
        return {"croquis_url": None}

    sala = (
        db.query(SalaProfesores)
        .filter(SalaProfesores.id == escritorio.sala_id)
        .first()
    )

    if not sala:
        return {"croquis_url": None}

    return {
        "escritorio": escritorio.codigo,
        "sala": sala.nombre,
        "croquis_url": sala.croquis_url
    }