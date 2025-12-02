from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.materia import MateriaCreate, MateriaOut
from app.crud import materia as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/materias/sede/{id_sede}", response_model=list[MateriaOut])
def listar_materias_por_sede(id_sede: int, db: Session = Depends(get_db)):
    materias = crud.listar_materias_por_sede(db, id_sede)
    return [MateriaOut.from_orm(m) for m in materias]

@router.post("/materias/", response_model=MateriaOut)
def crear_materia(materia: MateriaCreate, db: Session = Depends(get_db)):
    return MateriaOut.from_orm(crud.crear_materia(db, materia))

@router.get("/materias/", response_model=list[MateriaOut])
def listar_materias(db: Session = Depends(get_db)):
    return [MateriaOut.from_orm(m) for m in crud.listar_materias(db)]

@router.get("/materias/{id_materia}", response_model=MateriaOut)
def obtener_materia(id_materia: int, db: Session = Depends(get_db)):
    materia = crud.obtener_materia(db, id_materia)
    if materia:
        return MateriaOut.from_orm(materia)
    return {"mensaje": "Materia no encontrada"}

@router.put("/materias/{id_materia}", response_model=MateriaOut)
def actualizar_materia(id_materia: int, materia: MateriaCreate, db: Session = Depends(get_db)):
    materia_actualizada = crud.actualizar_materia(db, id_materia, materia)
    if materia_actualizada is None:
        return {"mensaje": "Materia no encontrada"}
    return MateriaOut.from_orm(materia_actualizada)   # ✅ aquí está la clave

@router.delete("/materias/{id_materia}")
def eliminar_materia(id_materia: int, db: Session = Depends(get_db)):
    materia = crud.eliminar_materia(db, id_materia)
    if materia:
        return {"mensaje": "Materia eliminada correctamente"}
    return {"mensaje": "Materia no encontrada"}