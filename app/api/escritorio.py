from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.escritorio import EscritorioCreate, EscritorioOut
from app.crud import escritorio as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/escritorios/", response_model=EscritorioOut)
def crear_escritorio(data: EscritorioCreate, db: Session = Depends(get_db)):
    return crud.crear_escritorio(db, data)

@router.get("/escritorios/", response_model=list[EscritorioOut])
def listar_escritorios(db: Session = Depends(get_db)):
    return crud.listar_todos(db)

@router.get("/escritorios/{escritorio_id}", response_model=EscritorioOut)
def obtener_escritorio(escritorio_id: int, db: Session = Depends(get_db)):
    return crud.obtener_por_id(db, escritorio_id)

@router.delete("/escritorios/{escritorio_id}")
def eliminar_escritorio(escritorio_id: int, db: Session = Depends(get_db)):
    esc = crud.eliminar_escritorio(db, escritorio_id)
    if esc:
        return {"mensaje": "Escritorio eliminado correctamente"}
    return {"mensaje": "Escritorio no encontrado"}

@router.get("/escritorios/sala/{sala_id}", response_model=list[EscritorioOut])
def escritorios_por_sala(sala_id: int, db: Session = Depends(get_db)):
    return crud.listar_por_sala(db, sala_id)

@router.get("/escritorios/carrera/{carrera_id}", response_model=list[EscritorioOut])
def escritorios_por_carrera(carrera_id: int, db: Session = Depends(get_db)):
    return crud.listar_por_carrera(db, carrera_id)

@router.post("/escritorios/asignar/{escritorio_id}")
def asignar_docente(escritorio_id: int, docente_id: int, db: Session = Depends(get_db)):
    esc = crud.asignar_docente(db, escritorio_id, docente_id)
    if not esc:
        return {"mensaje": "Escritorio no encontrado"}
    return {"mensaje": "Docente asignado correctamente"}