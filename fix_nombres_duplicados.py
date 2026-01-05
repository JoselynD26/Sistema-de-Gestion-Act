"""
Script para corregir nombres duplicados en la tabla docente
"""
from app.core.config import SessionLocal
from app.models.docente import Docente

def corregir_nombres_duplicados():
    """
    Corrige nombres que tienen apellidos duplicados
    Ejemplo: 'MICHELLE KATHERINE AGUIRRE PINTADO' -> 'MICHELLE KATHERINE'
    """
    db = SessionLocal()
    try:
        # Obtener todos los docentes
        docentes = db.query(Docente).all()
        
        corregidos = 0
        
        for docente in docentes:
            # Verificar si el nombre contiene los apellidos
            if docente.apellidos and docente.apellidos in docente.nombres:
                # Remover los apellidos del campo nombres
                nombres_corregidos = docente.nombres.replace(docente.apellidos, "").strip()
                
                print(f"\n🔧 Corrigiendo docente ID {docente.id}:")
                print(f"   Antes: nombres='{docente.nombres}', apellidos='{docente.apellidos}'")
                print(f"   Después: nombres='{nombres_corregidos}', apellidos='{docente.apellidos}'")
                
                # Actualizar
                docente.nombres = nombres_corregidos
                corregidos += 1
        
        # Guardar cambios
        if corregidos > 0:
            db.commit()
            print(f"\n✅ Se corrigieron {corregidos} registros de docentes")
        else:
            print("\n✅ No se encontraron nombres duplicados")
            
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Iniciando corrección de nombres duplicados...")
    corregir_nombres_duplicados()
    print("\n✅ Proceso completado")
