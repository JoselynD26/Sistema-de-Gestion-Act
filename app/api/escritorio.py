from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.escritorio import EscritorioCreate, EscritorioOut, EscritorioUpdate
from app.crud import escritorio as crud
from pydantic import BaseModel

router = APIRouter()

# ---------------------------
#   DB SESSION
# ---------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------
#   SCHEMA EXTRA
# ---------------------------

class AsignarDocente(BaseModel):
    docente_id: int

# ---------------------------
#   ENDPOINTS
# ---------------------------

# 1️⃣ → Rutas específicas PRIMERO (para evitar conflictos)
@router.get("/escritorios/sede/{id_sede}", response_model=list[EscritorioOut])
def listar_escritorios_por_sede(id_sede: int, db: Session = Depends(get_db)):
    return crud.listar_escritorios_por_sede(db, id_sede)

@router.get("/escritorios/sala/{sala_id}", response_model=list[EscritorioOut])
def escritorios_por_sala(sala_id: int, db: Session = Depends(get_db)):
    return crud.listar_por_sala(db, sala_id)

@router.get("/escritorios/carrera/{carrera_id}", response_model=list[EscritorioOut])
def escritorios_por_carrera(carrera_id: int, db: Session = Depends(get_db)):
    return crud.listar_por_carrera(db, carrera_id)

# 2️⃣ → CRUD general
@router.post("/escritorios/", response_model=EscritorioOut)
def crear_escritorio(data: EscritorioCreate, db: Session = Depends(get_db)):
    try:
        return crud.crear_escritorio(db, data)
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/escritorios/", response_model=list[EscritorioOut])
def listar_escritorios(db: Session = Depends(get_db)):
    return crud.listar_escritorios(db)

@router.get("/escritorios/{escritorio_id}", response_model=EscritorioOut)
def obtener_escritorio(escritorio_id: int, db: Session = Depends(get_db)):
    return crud.obtener_escritorio(db, escritorio_id)

@router.put("/escritorios/{escritorio_id}", response_model=EscritorioOut)
def actualizar_escritorio(escritorio_id: int, data: EscritorioUpdate, db: Session = Depends(get_db)):
    esc = crud.actualizar_escritorio(db, escritorio_id, data)
    if not esc:
        return {"mensaje": "Escritorio no encontrado"}
    return esc

@router.delete("/escritorios/{escritorio_id}")
def eliminar_escritorio(escritorio_id: int, db: Session = Depends(get_db)):
    esc = crud.eliminar_escritorio(db, escritorio_id)
    if esc:
        return {"mensaje": "Escritorio eliminado correctamente"}
    return {"mensaje": "Escritorio no encontrado"}

# 3️⃣ → Asignar docente (corregido)
@router.post("/escritorios/asignar/{escritorio_id}")
def asignar_docente(escritorio_id: int, data: AsignarDocente, db: Session = Depends(get_db)):
    esc = crud.asignar_docente(db, escritorio_id, data.docente_id)
    if not esc:
        return {"mensaje": "Escritorio no encontrado"}
    return {"mensaje": "Docente asignado correctamente"}
