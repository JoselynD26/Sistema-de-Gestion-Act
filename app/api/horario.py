from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.orm import Session
from datetime import date
import os
from app.core.config import SessionLocal
from supabase import create_client, Client
from app.schemas.horario import HorarioCreate, HorarioOut
from app.models.horario import Horario
from app.crud import horario as crud

router = APIRouter()

# -------------------
# Dependencia DB
# -------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------
# Endpoints CRUD
# -------------------

# ✅ Listar todos los horarios
@router.get("/", response_model=list[HorarioOut])
def listar_todos_horarios(db: Session = Depends(get_db)):
    return db.query(Horario).all()

# ✅ Listar horarios por sede
@router.get("/sede/{sede_id}")
def listar_horarios_por_sede(sede_id: int, db: Session = Depends(get_db)):
    horarios = db.query(Horario).filter(Horario.id_sede == sede_id).all()
    
    resultado = []
    for horario in horarios:
        # Mostrar rango de horas si existen ambas, sino solo inicio
        hora_display = str(horario.hora_inicio) if horario.hora_inicio else "N/A"
        if horario.hora_inicio and horario.hora_fin:
            hora_display = f"{horario.hora_inicio} - {horario.hora_fin}"
        
        resultado.append({
            "id": horario.id,
            "fecha": horario.fecha,
            "hora": hora_display,  # Campo para compatibilidad
            "hora_inicio": horario.hora_inicio,
            "hora_fin": horario.hora_fin,
            "estado": horario.estado,
            "id_docente": horario.id_docente,
            "id_materia": horario.id_materia,
            "id_aula": horario.id_aula,
            "id_sede": horario.id_sede
        })
    
    return resultado

# ✅ Crear horario
@router.post("/", response_model=HorarioOut)
def crear_horario(datos: HorarioCreate, db: Session = Depends(get_db)):
    # Para admin: crear horarios recurrentes sin validar asignación de materia
    from datetime import datetime, timedelta
    
    # Obtener el día de la semana de la fecha inicial
    fecha = datos.fecha if hasattr(datos, 'fecha') else datetime.now().date()
    hora_inicio = datos.hora_inicio if hasattr(datos, 'hora_inicio') else datetime.strptime('08:00', '%H:%M').time()
    hora_fin = datos.hora_fin if hasattr(datos, 'hora_fin') else datetime.strptime('10:00', '%H:%M').time()
    
    dia_semana = fecha.strftime("%A")
    dias_es = {
        "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
        "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
    }
    dia_es = dias_es.get(dia_semana, dia_semana)
    
    # Crear horarios recurrentes para 16 semanas
    horarios_creados = []
    for i in range(16):
        fecha_clase = fecha + timedelta(weeks=i)
        
        # Verificar disponibilidad del aula
        conflicto = db.query(Horario).filter(
            Horario.id_aula == datos.id_aula,
            Horario.fecha == fecha_clase,
            Horario.estado == "activo",
            Horario.hora_inicio < hora_fin,
            Horario.hora_fin > hora_inicio
        ).first()
        
        if not conflicto:
            nuevo_horario = Horario(
                dia=dia_es,
                fecha=fecha_clase,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                estado="activo",
                id_docente=datos.id_docente,
                id_materia=datos.id_materia,
                id_aula=datos.id_aula,
                id_curso=4,  # Usar curso existente
                id_sede=datos.id_sede
            )
            
            db.add(nuevo_horario)
            horarios_creados.append(nuevo_horario)
    
    db.commit()
    
    # Retornar el primer horario creado
    if horarios_creados:
        db.refresh(horarios_creados[0])
        return horarios_creados[0]
    else:
        # Si no se pudo crear ninguno, usar el CRUD normal
        return crud.crear_horario(db, datos)

# ✅ Obtener horario por ID
@router.get("/{horario_id}", response_model=HorarioOut)
def obtener_horario(horario_id: int, db: Session = Depends(get_db)):
    horario = crud.obtener_horario(db, horario_id)
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario

# ✅ Actualizar horario
@router.put("/{horario_id}", response_model=HorarioOut)
def actualizar_horario(horario_id: int, datos: HorarioCreate, db: Session = Depends(get_db)):
    horario = crud.actualizar_horario(db, horario_id, datos)
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario

# ✅ Eliminar horario
@router.delete("/{horario_id}")
def eliminar_horario(horario_id: int, db: Session = Depends(get_db)):
    ok = crud.eliminar_horario(db, horario_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return {"msg": f"Horario {horario_id} eliminado"}

# ✅ Registrar excepción (cancelación) para horario recurrente
from app.schemas.horario_cancelado import HorarioCanceladoCreate, HorarioCancelado
from app.crud import horario_cancelado as crud_cancelado

@router.post("/cancelados/", response_model=dict)
def registrar_cancelacion(datos: HorarioCanceladoCreate, db: Session = Depends(get_db)):
    nuevo = crud_cancelado.create_horario_cancelado(db, datos)
    return {"mensaje": "Cancelación registrada exitosamente", "id": nuevo.id}

# ✅ Listar cancelados por sede y fecha
@router.get("/cancelados/", response_model=list[HorarioOut])
def ver_horarios_cancelados(sede_id: int, fecha: date, db: Session = Depends(get_db)):
    return crud.listar_horarios_cancelados(db, sede_id, fecha)

# ✅ Cancelar horario (solo cambiar estado)
@router.put("/{horario_id}/cancelar")
def cancelar_horario(horario_id: int, db: Session = Depends(get_db)):
    horario = db.query(Horario).filter(Horario.id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    
    horario.estado = "cancelado"
    db.commit()
    db.refresh(horario)
    
    return {"message": "Horario cancelado exitosamente", "id": horario_id}

# ✅ Subir PDF de horario
@router.post("/pdf/{sede_id}")
async def subir_pdf_horario(sede_id: int, file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    
    # Configurar Supabase
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    supabase: Client = create_client(supabase_url, supabase_key)
    
    # Leer contenido del archivo
    content = await file.read()
    
    # Subir a Supabase Storage
    file_path = f"horario_sede_{sede_id}.pdf"
    
    try:
        result = supabase.storage.from_("horarios-pdf").upload(file_path, content)
        return {"message": "PDF subido exitosamente", "filename": file.filename}
    except Exception as e:
        # Si el archivo ya existe, actualizarlo
        try:
            result = supabase.storage.from_("horarios-pdf").update(file_path, content)
            return {"message": "PDF actualizado exitosamente", "filename": file.filename}
        except Exception as e2:
            raise HTTPException(status_code=500, detail=f"Error al subir PDF: {str(e2)}")

# ✅ Obtener PDF de horario
@router.get("/pdf/{sede_id}")
def obtener_pdf_horario(sede_id: int):
    # Configurar Supabase
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    supabase: Client = create_client(supabase_url, supabase_key)
    
    file_path = f"horario_sede_{sede_id}.pdf"
    
    try:
        # Descargar archivo de Supabase Storage
        result = supabase.storage.from_("horarios-pdf").download(file_path)
        
        return Response(
            content=result,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=horario_sede_{sede_id}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="PDF no encontrado")