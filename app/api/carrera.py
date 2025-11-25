from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.carrera import CarreraCreate, CarreraOut
from app.crud import carrera as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear carrera
@router.post("/carreras/", response_model=CarreraOut)
def crear_carrera(carrera: CarreraCreate, db: Session = Depends(get_db)):
    return crud.crear_carrera(db, carrera)

# Listar todas las carreras
@router.get("/carreras/", response_model=list[CarreraOut])
def listar_carreras(db: Session = Depends(get_db)):
    return crud.listar_carreras(db)

# Obtener carrera por ID
@router.get("/carreras/{id_carrera}", response_model=CarreraOut)
def obtener_carrera(id_carrera: int, db: Session = Depends(get_db)):
    return crud.obtener_carrera(db, id_carrera)

# Eliminar carrera
@router.delete("/carreras/{id_carrera}")
def eliminar_carrera(id_carrera: int, db: Session = Depends(get_db)):
    carrera = crud.eliminar_carrera(db, id_carrera)
    if carrera:
        return {"mensaje": "Carrera eliminada correctamente"}
    return {"mensaje": "Carrera no encontrada"}