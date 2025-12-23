from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import text
import os
from app.core.config import get_db
from supabase import create_client, Client

router = APIRouter()

# ✅ Subir PDF de horario por tipo con nombre personalizado
@router.post("/subir/{sede_id}/{tipo}")
async def subir_pdf_horario(sede_id: int, tipo: str, nombre: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Validar tipo de horario
    tipos_validos = ["aulas", "cursos", "docentes"]
    if tipo not in tipos_validos:
        raise HTTPException(status_code=400, detail="Tipo debe ser: aulas, cursos o docentes")
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    
    # Configurar Supabase
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    supabase: Client = create_client(supabase_url, supabase_key)
    
    # Leer contenido del archivo
    content = await file.read()
    
    # Subir a Supabase Storage con nombre personalizado
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"horario_{tipo}_sede_{sede_id}_{nombre}_{timestamp}.pdf"
    
    try:
        result = supabase.storage.from_("horarios-pdf").upload(file_path, content)
        
        # Guardar en base de datos
        db.execute(text("""
            INSERT INTO pdf_horarios (nombre, tipo, archivo, sede_id) 
            VALUES (:nombre, :tipo, :archivo, :sede_id)
        """), {"nombre": nombre, "tipo": tipo, "archivo": file_path, "sede_id": sede_id})
        db.commit()
        
        return {"message": f"PDF de horario de {tipo} subido exitosamente", "filename": file.filename, "nombre": nombre}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir PDF: {str(e)}")

# ✅ Obtener PDF de horario por nombre de archivo
@router.get("/ver/{sede_id}/{archivo}")
def obtener_pdf_horario(sede_id: int, archivo: str):
    # Configurar Supabase
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    supabase: Client = create_client(supabase_url, supabase_key)
    
    try:
        # Descargar archivo de Supabase Storage
        result = supabase.storage.from_("horarios-pdf").download(archivo)
        
        return Response(
            content=result,
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename={archivo}"}
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"PDF no encontrado")

# ✅ Listar PDFs disponibles por sede con detalles
@router.get("/listar/{sede_id}")
def listar_pdfs_horarios(sede_id: int, db: Session = Depends(get_db)):
    try:
        result = db.execute(text("""
            SELECT nombre, tipo, archivo, fecha_subida 
            FROM pdf_horarios 
            WHERE sede_id = :sede_id 
            ORDER BY fecha_subida DESC
        """), {"sede_id": sede_id}).fetchall()
        
        pdfs = []
        for row in result:
            pdfs.append({
                "tipo": row.tipo,
                "sede_id": sede_id,
                "nombre": row.nombre,
                "archivo": row.archivo,
                "titulo": f"Horario de {row.tipo.capitalize()}: {row.nombre}",
                "fecha_subida": str(row.fecha_subida)
            })
        
        return pdfs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar PDFs: {str(e)}")

# ✅ Eliminar PDF de horario por nombre de archivo
@router.delete("/eliminar/{sede_id}/{archivo}")
def eliminar_pdf_horario(sede_id: int, archivo: str, db: Session = Depends(get_db)):
    # Configurar Supabase
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    supabase: Client = create_client(supabase_url, supabase_key)
    
    try:
        result = supabase.storage.from_("horarios-pdf").remove([archivo])
        
        # Eliminar de base de datos
        db.execute(text("DELETE FROM pdf_horarios WHERE archivo = :archivo"), {"archivo": archivo})
        db.commit()
        
        return {"message": f"PDF eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar PDF: {str(e)}")