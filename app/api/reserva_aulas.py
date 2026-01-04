from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import datetime
from app.core.config import SessionLocal
from app.models.reserva import Reserva
from app.models.aula import Aula
from app.models.horario import Horario
from app.models.docente import Docente
from app.models.sede import Sede
from app.models.usuario import Usuario
from app.schemas.reserva import CancelarReservaSchema
from app.utils.email import send_admin_notification, send_status_update_email, send_cancellation_notification

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
def crear_reserva(request: dict, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
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
    
    # Notificar a los administradores (Background Task)
    try:
        docente = db.query(Docente).filter(Docente.id == docente_id).first()
        docente_nombre = f"{docente.nombres} {docente.apellidos}" if docente else "Desconocido"
        aula = db.query(Aula).filter(Aula.id == aula_id).first()
        aula_nombre = aula.nombre if aula else "Desconocido"

        # Obtener todos los administradores para notificarles
        admins = db.query(Usuario).filter(Usuario.rol == "admin").all()
        admin_emails = [admin.correo for admin in admins] if admins else []
        
        if admin_emails:
            print(f"DEBUG: Agregando tarea de notificacion admin para reserva {nueva_reserva.id} a {admin_emails}")
            background_tasks.add_task(
                send_admin_notification,
                admin_emails=admin_emails,
                reserva_id=nueva_reserva.id,
                docente_nombre=docente_nombre,
                aula_nombre=aula_nombre,
                fecha=fecha,
                hora=f"{hora_inicio} - {hora_fin}"
            )
        else:
            print("DEBUG: No se enviaron notificaciones porque no hay administradores registrados.")
    except Exception as e:
        print(f"Error al enviar notificación al admin: {e}")

    return {"message": "Reserva creada exitosamente", "id": nueva_reserva.id}

@router.get("/mis-reservas/{docente_id}")
def obtener_mis_reservas(docente_id: int, db: Session = Depends(get_db)):
    """Obtiene reservas del docente (Optimizado)"""
    
    # Consulta con JOIN para traer datos del Aula en una sola query
    resultados = (
        db.query(Reserva, Aula)
        .join(Aula, Reserva.id_aula == Aula.id)
        .filter(Reserva.id_docente == docente_id)
        .order_by(Reserva.fecha.desc(), Reserva.hora_inicio.desc())
        .all()
    )
    
    lista_reservas = []
    
    for reserva, aula in resultados:
        # Formato de hora
        hora_display = "N/A"
        if reserva.hora_inicio and reserva.hora_fin:
            hora_display = f"{reserva.hora_inicio.strftime('%H:%M')} - {reserva.hora_fin.strftime('%H:%M')}"
        elif reserva.hora_inicio:
            hora_display = str(reserva.hora_inicio)
        
        lista_reservas.append({
            "id": reserva.id,
            "fecha": reserva.fecha,
            "hora": hora_display,
            "estado": reserva.estado,
            "aula_nombre": aula.nombre,
            "aula_capacidad": aula.capacidad,
            "motivo": reserva.motivo or "Sin motivo especificado"
        })
    
    return lista_reservas

@router.post("/cancelar-reserva/{reserva_id}")
def cancelar_reserva(
    reserva_id: int,
    data: CancelarReservaSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    reserva = db.query(Reserva).filter(
        and_(
            Reserva.id == reserva_id,
            Reserva.id_docente == data.docente_id
        )
    ).first()

    if not reserva:
        raise HTTPException(
            status_code=404,
            detail="Reserva no encontrada"
        )

    if reserva.estado == "aprobada":
        raise HTTPException(
            status_code=400,
            detail="No se puede cancelar una reserva aprobada"
        )

    reserva.estado = "cancelada"
    db.commit()

    # Notificar a los administradores sobre la cancelación
    try:
        docente = db.query(Docente).filter(Docente.id == reserva.id_docente).first()
        aula = db.query(Aula).filter(Aula.id == reserva.id_aula).first()
        
        # Obtener todos los administradores
        admins = db.query(Usuario).filter(Usuario.rol == "admin").all()
        admin_emails = [admin.correo for admin in admins] if admins else []
        
        if admin_emails:
            background_tasks.add_task(
                send_cancellation_notification,
                admin_emails=admin_emails,
                reserva_id=reserva.id,
                docente_nombre=f"{docente.nombres} {docente.apellidos}" if docente else "Desconocido",
                aula_nombre=aula.nombre if aula else "Desconocido",
                fecha=reserva.fecha.strftime("%Y-%m-%d")
            )
    except Exception as e:
        print(f"Error al enviar notificación de cancelación: {e}")

    return {"message": "Reserva cancelada exitosamente"}


@router.get("/reservas-pendientes")
def obtener_reservas_pendientes(db: Session = Depends(get_db)):
    """Obtiene todas las reservas pendientes (Optimizado)"""
    
    resultados = (
        db.query(Reserva, Aula, Docente)
        .join(Aula, Reserva.id_aula == Aula.id)
        .join(Docente, Reserva.id_docente == Docente.id)
        .filter(Reserva.estado == "pendiente")
        .order_by(Reserva.fecha.asc())
        .all()
    )
    
    lista_reservas = []
    for reserva, aula, docente in resultados:
        # Formato de hora
        hora_display = "N/A"
        if reserva.hora_inicio and reserva.hora_fin:
            hora_display = f"{reserva.hora_inicio.strftime('%H:%M')} - {reserva.hora_fin.strftime('%H:%M')}"
        elif reserva.hora_inicio:
            hora_display = str(reserva.hora_inicio)
        
        lista_reservas.append({
            "id": reserva.id,
            "fecha": reserva.fecha,
            "hora": hora_display,
            "aula_nombre": aula.nombre,
            "docente_nombre": f"{docente.nombres} {docente.apellidos}",
            "estado": reserva.estado,
            "motivo": reserva.motivo or "Sin motivo especificado"
        })
    
    return lista_reservas

@router.post("/aprobar-reserva/{reserva_id}")
def aprobar_reserva(reserva_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Aprobar reserva (solo admin)"""
    
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    reserva.estado = "aprobada"
    db.commit()
    
    # Notificar al docente
    try:
        docente = db.query(Docente).filter(Docente.id == reserva.id_docente).first()
        aula = db.query(Aula).filter(Aula.id == reserva.id_aula).first()
        if docente and docente.correo:
            background_tasks.add_task(
                send_status_update_email,
                email_docente=docente.correo,
                docente_nombre=f"{docente.nombres} {docente.apellidos}",
                aula_nombre=aula.nombre if aula else "Aula desconocida",
                fecha=reserva.fecha.strftime("%Y-%m-%d"),
                nuevo_estado="APROBADA"
            )
    except Exception as e:
        print(f"Error al enviar notificación al docente: {e}")
    
    return {"message": "Reserva aprobada exitosamente"}

@router.post("/rechazar-reserva/{reserva_id}")
def rechazar_reserva(reserva_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Rechazar reserva (solo admin)"""
    
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    reserva.estado = "rechazada"
    db.commit()
    
    # Notificar al docente
    try:
        docente = db.query(Docente).filter(Docente.id == reserva.id_docente).first()
        aula = db.query(Aula).filter(Aula.id == reserva.id_aula).first()
        if docente and docente.correo:
            background_tasks.add_task(
                send_status_update_email,
                email_docente=docente.correo,
                docente_nombre=f"{docente.nombres} {docente.apellidos}",
                aula_nombre=aula.nombre if aula else "Aula desconocida",
                fecha=reserva.fecha.strftime("%Y-%m-%d"),
                nuevo_estado="RECHAZADA"
            )
    except Exception as e:
        print(f"Error al enviar notificación al docente: {e}")
    
    return {"message": "Reserva rechazada exitosamente"}

@router.get("/historial")
def obtener_historial(db: Session = Depends(get_db)):
    """
    Retorna todo el historial de reservas (Optimizado y ordenado)
    """
    resultados = (
        db.query(Reserva, Aula, Docente)
        .join(Aula, Reserva.id_aula == Aula.id)
        .join(Docente, Reserva.id_docente == Docente.id)
        .order_by(Reserva.fecha.desc(), Reserva.hora_inicio.desc())
        .all()
    )
    
    lista_reservas = []
    for reserva, aula, docente in resultados:
        # Formato de hora
        hora_display = "N/A"
        if reserva.hora_inicio and reserva.hora_fin:
            hora_display = f"{reserva.hora_inicio.strftime('%H:%M')} - {reserva.hora_fin.strftime('%H:%M')}"
        elif reserva.hora_inicio:
            hora_display = str(reserva.hora_inicio)
        
        lista_reservas.append({
            "id": reserva.id,
            "fecha": reserva.fecha,
            "hora": hora_display,
            "aula_nombre": aula.nombre,
            "docente_nombre": f"{docente.nombres} {docente.apellidos}",
            "estado": reserva.estado,
            "motivo": reserva.motivo or "Sin motivo especificado"
        })
    
    return lista_reservas
@router.get("/profesor/mi-croquis/{docente_id}")
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

@router.delete("/{reserva_id}")
def eliminar_reserva(reserva_id: int, db: Session = Depends(get_db)):
    """
    Elimina una reserva de la base de datos.
    Standard REST DELETE.
    """
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    # Opcional: Validar si se puede eliminar según reglas de negocio
    # Por ejemplo, si es una reserva pasada o si ya fue aprobada
    # if reserva.estado == 'aprobada':
    #     raise HTTPException(status_code=400, detail="No se puede eliminar una reserva aprobada")

    db.delete(reserva)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
