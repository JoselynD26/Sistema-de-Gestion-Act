from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.sede import SedeCreate, SedeOut
from app.crud import sede as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/sedes/", response_model=SedeOut)
def crear_sede(data: SedeCreate, db: Session = Depends(get_db)):
    return crud.crear_sede(db, data)

@router.get("/sedes/", response_model=list[SedeOut])
def listar_sedes(db: Session = Depends(get_db)):
    return crud.listar_sedes(db)

@router.get("/sedes/{id_sede}", response_model=SedeOut)
def obtener_sede(id_sede: int, db: Session = Depends(get_db)):
    return crud.obtener_sede(db, id_sede)

@router.delete("/sedes/{id_sede}")
def eliminar_sede(id_sede: int, db: Session = Depends(get_db)):
    sede = crud.eliminar_sede(db, id_sede)
    if sede:
        return {"mensaje": "Sede eliminada correctamente"}
    return {"mensaje": "Sede no encontrada"}