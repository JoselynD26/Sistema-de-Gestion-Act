from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, time
from app.core.config import SessionLocal
from app.controllers import croquis_controller

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/croquis/aulas-disponibles/")
def aulas(sede_id: int, fecha: date, hora: time, db: Session = Depends(get_db)):
    return croquis_controller.aulas_disponibles_por_sede(db, sede_id, fecha, hora)

@router.get("/croquis/escritorios-disponibles/")
def escritorios(sede_id: int, fecha: date, hora: time, db: Session = Depends(get_db)):
    return croquis_controller.escritorios_disponibles_por_sede(db, sede_id, fecha, hora)

@router.get("/croquis/docentes/")
def docentes(sede_id: int, db: Session = Depends(get_db)):
    return croquis_controller.docentes_por_sede(db, sede_id)

@router.get("/croquis/aulas-filtradas/")
def aulas_filtradas(sede_id: int, jornada: str, nivel: str, paralelo: str, fecha: date, hora: time, db: Session = Depends(get_db)):
    return croquis_controller.aulas_filtradas(db, sede_id, jornada, nivel, paralelo, fecha, hora)

@router.get("/croquis/escritorios-filtrados/")
def escritorios_filtrados(sede_id: int, jornada: str, sala_id: int, fecha: date, hora: time, db: Session = Depends(get_db)):
    return croquis_controller.escritorios_filtrados(db, sede_id, jornada, sala_id, fecha, hora)

@router.get("/croquis/sala/{sala_id}")
def ver_croquis(sala_id: int, db: Session = Depends(get_db)):
    resultado = croquis_controller.croquis_por_sala(db, sala_id)
    if not resultado:
        return {"mensaje": "Sala no encontrada"}
    return resultado

@router.get("/croquis/sede/{sede_id}")
def ver_croquis_sede(sede_id: int, db: Session = Depends(get_db)):
    return croquis_controller.croquis_por_sede(db, sede_id)

@router.get("/croquis/sede-filtrado/")
def ver_croquis_filtrado(sede_id: int, jornada: str, carrera_id: int, db: Session = Depends(get_db)):
    return croquis_controller.croquis_por_sede_filtrado(db, sede_id, jornada, carrera_id)