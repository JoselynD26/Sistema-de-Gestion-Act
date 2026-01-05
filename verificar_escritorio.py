"""
Script para verificar si un docente tiene escritorio asignado
"""
from app.core.config import SessionLocal
from app.models.escritorio import Escritorio
from app.models.sala_profesores import SalaProfesores
from app.models.carrera import Carrera

def verificar_escritorio_docente(docente_id: int):
    db = SessionLocal()
    try:
        print(f"\n🔍 Buscando escritorio para docente ID: {docente_id}")
        
        # Buscar escritorio
        escritorio = db.query(Escritorio).filter(Escritorio.docente_id == docente_id).first()
        
        if escritorio:
            print(f"✅ Escritorio encontrado:")
            print(f"   ID: {escritorio.id}")
            print(f"   Código: {escritorio.codigo}")
            print(f"   Sala ID: {escritorio.sala_id}")
            print(f"   Carrera ID: {escritorio.carrera_id}")
            print(f"   Estado: {escritorio.estado}")
            print(f"   Jornada: {escritorio.jornada}")
            
            # Buscar sala
            sala = db.query(SalaProfesores).filter(SalaProfesores.id == escritorio.sala_id).first()
            if sala:
                print(f"   Sala: {sala.nombre}")
            
            # Buscar carrera
            carrera = db.query(Carrera).filter(Carrera.id == escritorio.carrera_id).first()
            if carrera:
                print(f"   Carrera: {carrera.nombre}")
        else:
            print(f"❌ No se encontró escritorio asignado para el docente {docente_id}")
            
            # Mostrar escritorios disponibles
            print(f"\n📋 Escritorios sin asignar:")
            escritorios_libres = db.query(Escritorio).filter(Escritorio.docente_id == None).all()
            if escritorios_libres:
                for esc in escritorios_libres[:5]:  # Mostrar solo los primeros 5
                    sala = db.query(SalaProfesores).filter(SalaProfesores.id == esc.sala_id).first()
                    print(f"   - {esc.codigo} (Sala: {sala.nombre if sala else 'N/A'})")
            else:
                print("   No hay escritorios disponibles")
                
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Verificar para el docente 116 (Joselyn)
    verificar_escritorio_docente(116)
    
    # También verificar para el docente 4 (Michelle)
    print("\n" + "="*50)
    verificar_escritorio_docente(4)
