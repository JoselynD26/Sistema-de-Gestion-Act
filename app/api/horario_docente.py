from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.horario_docente import (
    HorarioDocenteCreate,
    HorarioDocenteOut
)
from app.crud import horario_docente as crud

router = APIRouter(prefix="/horario-docente", tags=["Horario Docente"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 ADMIN CREA HORARIO
@router.post("/", response_model=HorarioDocenteOut)
def crear_horario(
    data: HorarioDocenteCreate,
    db: Session = Depends(get_db)
):
    if data.hora_inicio >= data.hora_fin:
        raise HTTPException(
            status_code=400,
            detail="Hora inicio debe ser menor a hora fin"
        )

    return crud.crear_horario_docente(db, data)

# 🔹 DOCENTE VE SU HORARIO
@router.get("/docente/{docente_id}", response_model=list[HorarioDocenteOut])
def obtener_horario_docente(
    docente_id: int,
    db: Session = Depends(get_db)
):
    return crud.listar_por_docente(db, docente_id)
