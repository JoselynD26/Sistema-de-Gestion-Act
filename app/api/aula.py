from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.aula import AulaCreate, AulaOut
from app.crud import aula as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear aula
@router.post("/aulas/", response_model=AulaOut)
def crear_aula(aula: AulaCreate, db: Session = Depends(get_db)):
    return crud.crear_aula(db, aula)

# Listar todas las aulas
@router.get("/aulas/", response_model=list[AulaOut])
def listar_aulas(db: Session = Depends(get_db)):
    return crud.listar_aulas(db)

# Obtener aula por ID
@router.get("/aulas/{id_aula}", response_model=AulaOut)
def obtener_aula(id_aula: int, db: Session = Depends(get_db)):
    return crud.obtener_aula(db, id_aula)

# Actualizar aula
@router.put("/aulas/{id_aula}", response_model=AulaOut)
def actualizar_aula(id_aula: int, aula: AulaCreate, db: Session = Depends(get_db)):
    aula_actualizada = crud.actualizar_aula(db, id_aula, aula)
    
    if aula_actualizada is None:
        return {"mensaje": "Aula no encontrada"}

    return aula_actualizada

# Eliminar aula
@router.delete("/aulas/{id_aula}")
def eliminar_aula(id_aula: int, db: Session = Depends(get_db)):
    aula = crud.eliminar_aula(db, id_aula)
    if aula:
        return {"mensaje": "Aula eliminada correctamente"}
    return {"mensaje": "Aula no encontrada"}