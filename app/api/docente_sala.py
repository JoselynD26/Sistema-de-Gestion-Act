from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.docente_sala import DocenteSalaCreate, DocenteSalaOut
from app.crud import docente_sala as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/docente-sala/", response_model=DocenteSalaOut)
def crear_docente_sala(relacion: DocenteSalaCreate, db: Session = Depends(get_db)):
    return crud.crear_relacion(db, relacion)

@router.get("/docente-sala/", response_model=list[DocenteSalaOut])
def listar_docente_sala(db: Session = Depends(get_db)):
    return crud.listar_relaciones(db)

@router.delete("/docente-sala/{id}")
def eliminar_docente_sala(id: int, db: Session = Depends(get_db)):
    relacion = crud.eliminar_relacion(db, id)
    if relacion:
        return {"mensaje": "Relación eliminada correctamente"}
    return {"mensaje": "Relación no encontrada"}