from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.core.config import SessionLocal
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
@router.get("/sede/{id_sede}")
def listar_horarios_por_sede(id_sede: int, db: Session = Depends(get_db)):
    horarios = db.query(Horario).filter(Horario.id_sede == id_sede).all()
    
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