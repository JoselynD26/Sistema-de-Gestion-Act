from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.plaza import PlazaCreate, PlazaOut
from app.crud import plaza as crud
import os
import shutil
import uuid
import os
from supabase import create_client, Client
from app.schemas.plaza import PlazaCreate, PlazaOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 Configurar Supabase (MISMO PATRÓN)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if SUPABASE_URL and SUPABASE_SERVICE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
elif SUPABASE_URL and SUPABASE_ANON_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
else:
    supabase = None


@router.post("/plazas/{plaza_id}/croquis")
async def subir_croquis_plaza(
    plaza_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 🔹 Validar archivo
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.pdf')):
        raise HTTPException(status_code=400, detail="Tipo de archivo no válido")

    # 🔹 Nombre único
    ext = file.filename.split('.')[-1]
    unique_filename = f"plaza_{plaza_id}_{uuid.uuid4()}.{ext}"

    # 🔹 Leer archivo
    content = await file.read()

    try:
        # 🔹 Subir a Supabase Storage
        supabase.storage.from_("croquis-plazas").upload(
            unique_filename,
            content,
            {"content-type": file.content_type}
        )

        # 🔹 Obtener URL pública
        public_url = supabase.storage.from_("croquis-plazas").get_public_url(
            unique_filename
        )

        # 🔹 Guardar en DB
        from app.models.plaza import Plaza
        plaza = db.query(Plaza).filter(Plaza.id == plaza_id).first()
        if not plaza:
            raise HTTPException(status_code=404, detail="Plaza no encontrada")

        plaza.croquis_url = public_url
        db.commit()

        return {
            "message": "Croquis subido exitosamente",
            "croquis_url": public_url
        }

    except Exception as e:
        print("❌ ERROR SUBIENDO CROQUIS PLAZA:", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/plazas/{plaza_id}/croquis")
def obtener_croquis_plaza(plaza_id: int, db: Session = Depends(get_db)):
    from app.models.plaza import Plaza
    plaza = db.query(Plaza).filter(Plaza.id == plaza_id).first()
    if not plaza:
        raise HTTPException(status_code=404, detail="Plaza no encontrada")

    return {"croquis_url": plaza.croquis_url}

@router.post("/plazas/", response_model=PlazaOut)
def crear_plaza(datos: PlazaCreate, db: Session = Depends(get_db)):
    return crud.crear_plaza(db, datos)

@router.get("/plazas/sede/{sede_id}", response_model=list[PlazaOut])
def listar_plazas_por_sede(sede_id: int, db: Session = Depends(get_db)):
    return crud.listar_plazas_por_sede(db, sede_id)

@router.put("/plazas/{plaza_id}", response_model=PlazaOut)
def actualizar_plaza(
    plaza_id: int,
    datos: PlazaCreate,
    db: Session = Depends(get_db)
):
    plaza_actualizada = crud.actualizar_plaza(db, plaza_id, datos)
    if plaza_actualizada is None:
        raise HTTPException(status_code=404, detail="Plaza no encontrada")
    return plaza_actualizada
@router.delete("/plazas/{plaza_id}")
def eliminar_plaza(plaza_id: int, db: Session = Depends(get_db)):
    plaza = crud.eliminar_plaza(db, plaza_id)
    if not plaza:
        raise HTTPException(status_code=404, detail="Plaza no encontrada")
    return {"message": "Plaza eliminada correctamente"}
