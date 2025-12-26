from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.materia import MateriaOut, MateriaCreate


from app.core.config import get_db
from app.crud import materia as crud_materia
from app.schemas.materia import (
    MateriaOut,
    MateriaCreate  # ✅ IMPORTANTE
)

router = APIRouter()


@router.get("/", response_model=List[MateriaOut])
def listar_materias(db: Session = Depends(get_db)):
    return crud_materia.get_materias(db)


@router.get("/sede/{sede_id}", response_model=List[MateriaOut])
def listar_materias_por_sede(sede_id: int, db: Session = Depends(get_db)):
    return crud_materia.get_materias_por_sede(db, sede_id)


@router.get("/{materia_id}", response_model=MateriaOut)
def obtener_materia(materia_id: int, db: Session = Depends(get_db)):
    materia = crud_materia.get_materia(db, materia_id)
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return materia


@router.post("/", response_model=MateriaOut)
def crear_materia(materia: MateriaCreate, db: Session = Depends(get_db)):
    return crud_materia.create_materia(db, materia)


@router.put("/{materia_id}", response_model=MateriaOut)
def actualizar_materia(
    materia_id: int,
    materia: MateriaCreate,
    db: Session = Depends(get_db),
):
    db_materia = crud_materia.update_materia(db, materia_id, materia)
    if not db_materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return db_materia


@router.delete("/{materia_id}")
def eliminar_materia(materia_id: int, db: Session = Depends(get_db)):
    if not crud_materia.delete_materia(db, materia_id):
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return {"message": "Materia eliminada"}
