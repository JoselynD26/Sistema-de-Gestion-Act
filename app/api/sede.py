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
        
@router.get("/modulos-sede/{id_sede}")
def modulos_por_sede(id_sede: int, db: Session = Depends(get_db)):
    # Aquí puedes decidir dinámicamente qué módulos tiene cada sede
    return [
        {"titulo": "Carreras", "icono": "school"},
        {"titulo": "Aulas", "icono": "meeting_room"},
        {"titulo": "Escritorios", "icono": "desktop_windows"},
        {"titulo": "Docentes", "icono": "person"},
        {"titulo": "Cursos", "icono": "class"}, 
        {"titulo": "Materias", "icono": "book"},
        {"titulo": "Horarios", "icono": "schedule"}, 
         {"titulo": "Salas", "icono": "business"},   # ✅ nuevo módulo

    ]

@router.post("/sedes/", response_model=SedeOut)
def crear_sede(data: SedeCreate, db: Session = Depends(get_db)):
    return crud.crear_sede(db, data)

@router.get("/sedes/", response_model=list[SedeOut])
def listar_sedes(db: Session = Depends(get_db)):
    return crud.listar_sedes(db)

@router.get("/sedes/{id_sede}", response_model=SedeOut)
def obtener_sede(id_sede: int, db: Session = Depends(get_db)):
    return crud.obtener_sede(db, id_sede)

@router.put("/sedes/{id_sede}", response_model=SedeOut)
def actualizar_sede(id_sede: int, data: SedeCreate, db: Session = Depends(get_db)):
    sede_actualizada = crud.actualizar_sede(db, id_sede, data)

    if sede_actualizada is None:
        return {"mensaje": "Sede no encontrada"}

    return sede_actualizada

@router.delete("/sedes/{id_sede}")
def eliminar_sede(id_sede: int, db: Session = Depends(get_db)):
    sede = crud.eliminar_sede(db, id_sede)
    if sede:
        return {"mensaje": "Sede eliminada correctamente"}
    return {"mensaje": "Sede no encontrada"}