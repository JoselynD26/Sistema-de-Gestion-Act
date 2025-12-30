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

    from sqlalchemy.exc import IntegrityError
    try:
        return crud.crear_horario_docente(db, data)
    except IntegrityError as e:
        db.rollback()
        # Parseando el error para dar un mensaje útil de qué FK falló es complejo,
        # pero para optimización general, retornar 400 o 404 genérico es mucho más rápido.
        # Si se desea detalle, se puede inspeccionar e.orig.pgcode o similar.
        raise HTTPException(status_code=400, detail="Error de integridad: Docente, Curso, Materia o Aula no válidos.")

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
