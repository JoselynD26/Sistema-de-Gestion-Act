from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.horario_docente import (
    HorarioDocenteCreate,
    HorarioDocenteOut,
    HorarioDocenteUpdate
)
from app.crud import horario_docente as crud
from app.models.docente import Docente
from app.models.curso import Curso
from app.models.materia import Materia
from app.models.aula import Aula

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

    # Validar existencia de las entidades relacionadas
    if not db.query(Docente).filter(Docente.id == data.docente_id).first():
        raise HTTPException(status_code=404, detail=f"Docente con ID {data.docente_id} no encontrado")
    if not db.query(Curso).filter(Curso.id == data.curso_id).first():
        raise HTTPException(status_code=404, detail=f"Curso con ID {data.curso_id} no encontrado")
    if not db.query(Materia).filter(Materia.id == data.materia_id).first():
        raise HTTPException(status_code=404, detail=f"Materia con ID {data.materia_id} no encontrado")
    if not db.query(Aula).filter(Aula.id == data.aula_id).first():
        raise HTTPException(status_code=404, detail=f"Aula con ID {data.aula_id} no encontrado")

    return crud.crear_horario_docente(db, data)

# 🔹 DOCENTE VE SU HORARIO
@router.get("/docente/{docente_id}", response_model=list[HorarioDocenteOut])
def obtener_horario_docente(
    docente_id: int,
    db: Session = Depends(get_db)
):
    return crud.listar_por_docente(db, docente_id)


@router.patch("/{horario_id}", response_model=HorarioDocenteOut)
@router.patch("/{horario_id}/", response_model=HorarioDocenteOut, include_in_schema=False)
def actualizar_horario(
    horario_id: int,
    data: HorarioDocenteUpdate,
    db: Session = Depends(get_db)
):
    horario = crud.actualizar_horario_docente(db, horario_id, data)
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario


@router.delete("/{horario_id}")
@router.delete("/{horario_id}/", include_in_schema=False)
def eliminar_horario(
    horario_id: int,
    db: Session = Depends(get_db)
):
    success = crud.eliminar_horario_docente(db, horario_id)
    if not success:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return {"message": "Horario eliminado correctamente"}
