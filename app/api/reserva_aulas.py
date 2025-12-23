from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from app.core.config import SessionLocal
from app.models.reserva import Reserva
from app.models.aula import Aula
from app.models.horario import Horario
from app.models.docente import Docente
from app.models.sede import Sede

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/aulas-disponibles")
def obtener_aulas_disponibles(
    fecha: str,
    hora: str,
    sede_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene aulas disponibles en fecha/hora específica"""
    
    # Obtener todas las aulas de la sede
    aulas = db.query(Aula).filter(Aula.id_sede == sede_id).all()
    
    aulas_disponibles = []
    
    for aula in aulas:
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
            hora_obj = datetime.strptime(hora, "%H:%M").time()
        except ValueError:
            continue
            
        # Verificar si hay horario regular en esa fecha/hora
        horario_ocupado = db.query(Horario).filter(
            and_(
                Horario.id_aula == aula.id,
                Horario.fecha == fecha_obj,
                Horario.estado == "activo",
                # Verificar si la hora solicitada cae dentro del rango del horario
                Horario.hora_inicio <= hora_obj,
                Horario.hora_fin > hora_obj
            )
        ).first()
        
        # Verificar si hay reserva aprobada en esa fecha/hora
        reserva_ocupada = db.query(Reserva).filter(
            and_(
                Reserva.id_aula == aula.id,
                Reserva.fecha == fecha_obj,
                Reserva.estado == "aprobada",
                # Verificar si la hora solicitada cae dentro del rango de la reserva
                Reserva.hora_inicio <= hora_obj,
                Reserva.hora_fin > hora_obj
            )
        ).first()
        
        # Si no hay horario ni reserva, el aula está disponible
        if not horario_ocupado and not reserva_ocupada:
            aulas_disponibles.append({
                "id": aula.id,
                "nombre": aula.nombre,
                "capacidad": aula.capacidad,
                "sede_id": aula.id_sede
            })
    
    return aulas_disponibles

@router.post("/crear-reserva")
def crear_reserva(request: dict, db: Session = Depends(get_db)):
    """Crear nueva reserva (estado pendiente)"""
    
    # Extraer datos del request
    aula_id = request.get("aula_id")
    docente_id = request.get("docente_id")
    fecha = request.get("fecha")
    hora_inicio = request.get("hora_inicio")
    hora_fin = request.get("hora_fin")
    motivo = request.get("motivo", "")
    
    # Convertir strings a objetos date y time
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
        hora_inicio_obj = datetime.strptime(hora_inicio, "%H:%M").time()
        hora_fin_obj = datetime.strptime(hora_fin, "%H:%M").time()
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha u hora inválido")
    
    # Verificar que hora_fin sea mayor que hora_inicio
    if hora_fin_obj <= hora_inicio_obj:
        raise HTTPException(status_code=400, detail="La hora de fin debe ser mayor que la hora de inicio")
    
    # Verificar que el aula esté disponible
    aula = db.query(Aula).filter(Aula.id == aula_id).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    
    # Verificar disponibilidad en todo el rango de horas
    conflictos = db.query(Reserva).filter(
        and_(
            Reserva.id_aula == aula_id,
            Reserva.fecha == fecha_obj,
            or_(Reserva.estado == "aprobada", Reserva.estado == "pendiente"),
            # Verificar solapamiento de horarios
            or_(
                and_(Reserva.hora_inicio < hora_fin_obj, Reserva.hora_fin > hora_inicio_obj)
            )
        )
    ).all()
    
    if conflictos:
        raise HTTPException(status_code=400, detail="Aula no disponible en ese rango horario")
    
    # Crear reserva
    nueva_reserva = Reserva(
        fecha=fecha_obj,
        hora_inicio=hora_inicio_obj,
        hora_fin=hora_fin_obj,
        estado="pendiente",
        id_docente=docente_id,
        id_aula=aula_id,
        motivo=motivo
    )
    
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)
    
    return {"message": "Reserva creada exitosamente", "id": nueva_reserva.id}

@router.get("/mis-reservas/{docente_id}")
def obtener_mis_reservas(docente_id: int, db: Session = Depends(get_db)):
    """Obtiene reservas del docente"""
    
    reservas = db.query(Reserva).filter(Reserva.id_docente == docente_id).all()
    
    resultado = []
    for reserva in reservas:
        aula = db.query(Aula).filter(Aula.id == reserva.id_aula).first()
        
        # Mostrar rango de horas
        hora_display = "N/A"
        if reserva.hora_inicio and reserva.hora_fin:
            hora_display = f"{reserva.hora_inicio} - {reserva.hora_fin}"
        elif reserva.hora_inicio:
            hora_display = str(reserva.hora_inicio)
        
        resultado.append({
            "id": reserva.id,
            "fecha": reserva.fecha,
            "hora": hora_display,
            "estado": reserva.estado,
            "aula_nombre": aula.nombre if aula else "N/A",
            "aula_capacidad": aula.capacidad if aula else 0,
            "motivo": reserva.motivo or "Sin motivo especificado"
        })
    
    return resultado

@router.post("/cancelar-reserva/{reserva_id}")
def cancelar_reserva(reserva_id: int, docente_id: int, db: Session = Depends(get_db)):
    """Cancelar reserva propia"""
    
    reserva = db.query(Reserva).filter(
        and_(
            Reserva.id == reserva_id,
            Reserva.id_docente == docente_id
        )
    ).first()
    
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    if reserva.estado == "aprobada":
        raise HTTPException(status_code=400, detail="No se puede cancelar una reserva aprobada")
    
    reserva.estado = "cancelada"
    db.commit()
    
    return {"message": "Reserva cancelada exitosamente"}

@router.get("/reservas-pendientes")
def obtener_reservas_pendientes(db: Session = Depends(get_db)):
    """Obtiene todas las reservas pendientes (para admin)"""
    
    reservas = db.query(Reserva).filter(Reserva.estado == "pendiente").all()
    
    resultado = []
    for reserva in reservas:
        aula = db.query(Aula).filter(Aula.id == reserva.id_aula).first()
        docente = db.query(Docente).filter(Docente.id == reserva.id_docente).first()
        
        # Mostrar rango de horas
        hora_display = "N/A"
        if reserva.hora_inicio and reserva.hora_fin:
            hora_display = f"{reserva.hora_inicio} - {reserva.hora_fin}"
        elif reserva.hora_inicio:
            hora_display = str(reserva.hora_inicio)
        
        resultado.append({
            "id": reserva.id,
            "fecha": reserva.fecha,
            "hora": hora_display,
            "aula_nombre": aula.nombre if aula else "N/A",
            "docente_nombre": f"{docente.nombres} {docente.apellidos}" if docente else "N/A",
            "estado": reserva.estado,
            "motivo": reserva.motivo or "Sin motivo especificado"
        })
    
    return resultado

@router.post("/aprobar-reserva/{reserva_id}")
def aprobar_reserva(reserva_id: int, db: Session = Depends(get_db)):
    """Aprobar reserva (solo admin)"""
    
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    reserva.estado = "aprobada"
    db.commit()
    
    return {"message": "Reserva aprobada exitosamente"}

@router.post("/rechazar-reserva/{reserva_id}")
def rechazar_reserva(reserva_id: int, db: Session = Depends(get_db)):
    """Rechazar reserva (solo admin)"""
    
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    reserva.estado = "rechazada"
    db.commit()
    
    return {"message": "Reserva rechazada exitosamente"}