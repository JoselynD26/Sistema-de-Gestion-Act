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
@router.get("/horarios/", response_model=list[HorarioOut])
def listar_todos_horarios(db: Session = Depends(get_db)):
    return db.query(Horario).all()

# ✅ Listar horarios por sede
@router.get("/horarios/sede/{id_sede}", response_model=list[HorarioOut])
def listar_horarios_por_sede(id_sede: int, db: Session = Depends(get_db)):
    return db.query(Horario).filter(Horario.id_sede == id_sede).all()

# ✅ Crear horario
@router.post("/horarios/", response_model=HorarioOut)
def crear_horario(datos: HorarioCreate, db: Session = Depends(get_db)):
    return crud.crear_horario(db, datos)

# ✅ Obtener horario por ID
@router.get("/horarios/{horario_id}", response_model=HorarioOut)
def obtener_horario(horario_id: int, db: Session = Depends(get_db)):
    horario = crud.obtener_horario(db, horario_id)
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario

# ✅ Actualizar horario
@router.put("/horarios/{horario_id}", response_model=HorarioOut)
def actualizar_horario(horario_id: int, datos: HorarioCreate, db: Session = Depends(get_db)):
    horario = crud.actualizar_horario(db, horario_id, datos)
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario

# ✅ Eliminar horario
@router.delete("/horarios/{horario_id}")
def eliminar_horario(horario_id: int, db: Session = Depends(get_db)):
    ok = crud.eliminar_horario(db, horario_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return {"msg": f"Horario {horario_id} eliminado"}

# ✅ Listar cancelados por sede y fecha
@router.get("/horarios/cancelados/", response_model=list[HorarioOut])
def ver_horarios_cancelados(sede_id: int, fecha: date, db: Session = Depends(get_db)):
    return crud.listar_horarios_cancelados(db, sede_id, fecha)