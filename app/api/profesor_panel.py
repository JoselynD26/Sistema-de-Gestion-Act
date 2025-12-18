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
        
        # Mostrar rango de horas si existen ambas, sino solo inicio
        hora_display = str(horario.hora_inicio) if horario.hora_inicio else "N/A"
        if horario.hora_inicio and horario.hora_fin:
            hora_display = f"{horario.hora_inicio} - {horario.hora_fin}"
        
        resultado.append({
            "id": horario.id,
            "fecha": horario.fecha,
            "hora": hora_display,
            "estado": horario.estado,
            "materia_nombre": materia.nombre if materia else "N/A",
            "aula_nombre": aula.nombre if aula else "N/A",
            "aula_capacidad": aula.capacidad if aula else 0
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
    db: Session = Depends(get_db)
):
    """Crear horario de clase"""
    
    # Verificar que el docente tenga asignada la materia
    docente = db.query(Docente).filter(Docente.id == docente_id).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    
    materia_asignada = any(m.id == materia_id for m in docente.materias)
    if not materia_asignada:
        raise HTTPException(status_code=400, detail="No tienes asignada esta materia")
    
    # Verificar que el aula esté disponible en el rango de horas
    conflicto = db.query(Horario).filter(
        and_(
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
    
    # Crear horario
    nuevo_horario = Horario(
        fecha=fecha,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        estado="activo",
        id_docente=docente_id,
        id_materia=materia_id,
        id_aula=aula_id,
        id_sede=docente.sede_id
    )
    
    db.add(nuevo_horario)
    db.commit()
    db.refresh(nuevo_horario)
    
    return {"message": "Horario creado exitosamente", "id": nuevo_horario.id}

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
    """Obtiene el escritorio asignado al docente"""
    from app.models.escritorio import Escritorio
    
    escritorio = db.query(Escritorio).filter(Escritorio.docente_id == docente_id).first()
    
    if escritorio:
        return {
            "id": escritorio.id,
            "numero": escritorio.numero,
            "sala_id": escritorio.sala_id,
            "carrera_id": escritorio.carrera_id,
            "asignado": True
        }
    else:
        return {"asignado": False}

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
            "numero": escritorio.numero,
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