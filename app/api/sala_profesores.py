from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.sala_profesores import SalaProfesoresCreate, SalaProfesoresOut
from app.crud.sala_profesores import crear_sala, listar_salas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SalaProfesoresOut)
def crear_sala_profesores(sala: SalaProfesoresCreate, db: Session = Depends(get_db)):
    return crear_sala(db, sala)

@router.get("/", response_model=list[SalaProfesoresOut])
def listar_salas_profesores(db: Session = Depends(get_db)):
    return listar_salas(db)

@router.get("/sede/{sede_id}", response_model=list[SalaProfesoresOut])
def listar_salas_por_sede(sede_id: int, db: Session = Depends(get_db)):
    from app.crud.sala_profesores import listar_salas_por_sede
    return listar_salas_por_sede(db, sede_id)

@router.put("/{sala_id}", response_model=SalaProfesoresOut)
def actualizar_sala_profesores(sala_id: int, sala: SalaProfesoresCreate, db: Session = Depends(get_db)):
    from app.crud.sala_profesores import actualizar_sala
    sala_actualizada = actualizar_sala(db, sala_id, sala)
    if not sala_actualizada:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return sala_actualizada

@router.delete("/{sala_id}")
def eliminar_sala_profesores(sala_id: int, db: Session = Depends(get_db)):
    from app.crud.sala_profesores import eliminar_sala
    sala_eliminada = eliminar_sala(db, sala_id)
    if not sala_eliminada:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return {"mensaje": "Sala eliminada correctamente"}