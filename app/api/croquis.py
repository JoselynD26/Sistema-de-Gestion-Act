from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
import uuid
import os
from supabase import create_client, Client

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configurar Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # Usar service key
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

print(f"SUPABASE_URL: {SUPABASE_URL}")
print(f"SERVICE_KEY existe: {bool(SUPABASE_SERVICE_KEY)}")
print(f"ANON_KEY existe: {bool(SUPABASE_ANON_KEY)}")

if SUPABASE_URL and SUPABASE_SERVICE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)  # Service key bypassa RLS
    print("✅ Supabase configurado con service key")
elif SUPABASE_URL and SUPABASE_ANON_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    print("✅ Supabase configurado con anon key")
else:
    supabase = None
    print("⚠️ Supabase no configurado correctamente")

@router.post("/aula/{aula_id}/croquis")
async def subir_croquis_aula(
    aula_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Solo admin puede subir croquis"""
    # Validar tipo de archivo
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.pdf')):
        raise HTTPException(status_code=400, detail="Tipo de archivo no válido")
    
    # Generar nombre único
    file_extension = file.filename.split('.')[-1]
    unique_filename = f"aula_{aula_id}_{uuid.uuid4()}.{file_extension}"
    
    # Leer contenido del archivo
    content = await file.read()
    
    # Subir a Supabase Storage
    try:
        result = supabase.storage.from_("croquis").upload(
            unique_filename, content, {"content-type": file.content_type}
        )
        
        # Obtener URL pública
        public_url = supabase.storage.from_("croquis").get_public_url(unique_filename)
        
        # Actualizar base de datos
        from app.models.aula import Aula
        aula = db.query(Aula).filter(Aula.id == aula_id).first()
        if not aula:
            raise HTTPException(status_code=404, detail="Aula no encontrada")
        
        aula.croquis_url = public_url
        db.commit()
        
        return {"message": "Croquis subido exitosamente", "url": public_url}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error subiendo archivo: {str(e)}")

@router.post("/sala/{sala_id}/croquis")
async def subir_croquis_sala(
    sala_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Solo admin puede subir croquis"""
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.pdf')):
        raise HTTPException(status_code=400, detail="Tipo de archivo no válido")
    
    # Generar nombre único
    file_extension = file.filename.split('.')[-1]
    unique_filename = f"sala_{sala_id}_{uuid.uuid4()}.{file_extension}"
    
    # Leer contenido del archivo
    content = await file.read()
    
    # Verificar configuración de Supabase
    if not SUPABASE_URL or (not SUPABASE_SERVICE_KEY and not SUPABASE_ANON_KEY):
        raise HTTPException(status_code=500, detail="Configuración de Supabase no encontrada")
    
    # Subir a Supabase Storage
    try:
        print(f"Subiendo archivo: {unique_filename}")
        result = supabase.storage.from_("croquis").upload(
            unique_filename, content, {"content-type": file.content_type}
        )
        print(f"Resultado upload: {result}")
        
        # Obtener URL pública
        public_url = supabase.storage.from_("croquis").get_public_url(unique_filename)
        print(f"URL pública: {public_url}")
        
        # Actualizar base de datos
        from app.models.sala_profesores import SalaProfesores
        sala = db.query(SalaProfesores).filter(SalaProfesores.id == sala_id).first()
        if not sala:
            raise HTTPException(status_code=404, detail="Sala no encontrada")
        
        sala.croquis_url = public_url
        db.commit()
        
        return {"message": "Croquis subido exitosamente", "url": public_url}
        
    except Exception as e:
        print(f"Error completo: {e}")
        print(f"Tipo de error: {type(e)}")
        raise HTTPException(status_code=500, detail=f"Error subiendo archivo: {str(e)}")

@router.get("/aula/{aula_id}/croquis")
async def obtener_croquis_aula(aula_id: int, db: Session = Depends(get_db)):
    """Admin y docente pueden ver croquis"""
    from app.models.aula import Aula
    aula = db.query(Aula).filter(Aula.id == aula_id).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    
    return {"croquis_url": aula.croquis_url}
@router.get("/sala/sede/{sede_id}")
def listar_salas_por_sede(sede_id: int, db: Session = Depends(get_db)):
    from app.models.sala_profesores import SalaProfesores

    salas = db.query(SalaProfesores)\
        .filter(SalaProfesores.id_sede == sede_id)\
        .all()

    return salas

@router.get("/sala/{sala_id}/croquis")
async def obtener_croquis_sala(sala_id: int, db: Session = Depends(get_db)):
    """Admin y docente pueden ver croquis"""
    from app.models.sala_profesores import SalaProfesores
    sala = db.query(SalaProfesores).filter(SalaProfesores.id == sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    
    return {"croquis_url": sala.croquis_url}