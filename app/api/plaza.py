from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.plaza import PlazaCreate, PlazaOut
from app.crud import plaza as crud
import os
import shutil

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/plazas/", response_model=PlazaOut)
def crear_plaza(datos: PlazaCreate, db: Session = Depends(get_db)):
    return crud.crear_plaza(db, datos)

@router.get("/plazas/sede/{sede_id}", response_model=list[PlazaOut])
def listar_plazas_por_sede(sede_id: int, db: Session = Depends(get_db)):
    return crud.listar_plazas_por_sede(db, sede_id)

@router.post("/plazas/{plaza_id}/croquis")
def subir_croquis_plaza(plaza_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Crear directorio si no existe
        upload_dir = "uploads/croquis/plazas"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Guardar archivo
        file_path = f"{upload_dir}/plaza_{plaza_id}_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Actualizar URL en base de datos
        croquis_url = f"/uploads/croquis/plazas/plaza_{plaza_id}_{file.filename}"
        plaza = crud.actualizar_croquis_plaza(db, plaza_id, croquis_url)
        
        if plaza:
            return {"mensaje": "Croquis subido correctamente", "croquis_url": croquis_url}
        else:
            return {"error": "Plaza no encontrada"}
            
    except Exception as e:
        return {"error": f"Error al subir croquis: {str(e)}"}

@router.get("/plazas/{plaza_id}/croquis")
def obtener_croquis_plaza(plaza_id: int, db: Session = Depends(get_db)):
    plaza = crud.obtener_plaza(db, plaza_id)
    if plaza and plaza.croquis_url:
        return {"croquis_url": plaza.croquis_url}
    return {"error": "Croquis no encontrado"}