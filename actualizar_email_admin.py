"""
Script para actualizar el email del administrador a jmr.dicao@yavirac.edu.ec
"""
from app.core.config import SessionLocal
from app.models.usuario import Usuario

db = SessionLocal()

try:
    # Buscar todos los administradores
    admins = db.query(Usuario).filter(Usuario.rol == "admin").all()
    
    print(f"📊 Encontrados {len(admins)} administradores:")
    for admin in admins:
        print(f"  - {admin.nombres} {admin.apellidos} ({admin.correo})")
    
    # Actualizar todos los admins a jmr.dicao@yavirac.edu.ec
    print("\n🔄 Actualizando emails de administradores...")
    for admin in admins:
        old_email = admin.correo
        admin.correo = "jmr.dicao@yavirac.edu.ec"
        print(f"  ✅ {old_email} -> jmr.dicao@yavirac.edu.ec")
    
    db.commit()
    print("\n✅ Todos los administradores ahora usan jmr.dicao@yavirac.edu.ec")
    print("📧 Ahora Resend podrá enviarles emails correctamente")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
