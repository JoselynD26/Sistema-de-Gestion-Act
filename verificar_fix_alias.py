
import requests

BASE_URL = "http://localhost:8000"

def verificar_fix_alias():
    print("--- Verificando Fix: Reset usando ID Docente como Alias ---")
    
    from app.core.config import SessionLocal
    from app.models.usuario import Usuario
    import hashlib

    db = SessionLocal()
    
    # Usuario de prueba con ID Usuario != ID Docente
    # Para esto, necesitamos crear un escenario donde ID Usuario sea ej. 100 y ID Docente sea 50.
    # Como los autoincrements son globales en la tabla, difícil forzarlo, pero podemos asumir que serán diferentes.
    # Vamos a crear primero el usuario
    
    user_email = "test_alias@yavirac.edu.ec"
    pass_base = "123456"
    pass_reset_alias = "alias123"

    try:
        # Limpieza
        db.query(Usuario).filter(Usuario.correo == user_email).delete(synchronize_session=False)
        db.commit()

        # Crear Usuario "Docente"
        # Simulamos ID Docente con un valor X.
        # En la BD real, el id_docente es una FK a tabla docente.
        # Necesitamos un ID que NO sea igual al ID de usuario para probar bien.
        
        # 1. Crear usuario normal
        u = Usuario(
            nombres="Alias", apellidos="Test", correo=user_email,
            contrasena=hashlib.sha256(pass_base.encode()).hexdigest(),
            rol="docente",
            id_docente=99999 # Fake ID docente (asumimos que no valida FK estricta o creamos docente si falla)
        )
        db.add(u)
        db.commit()
        db.refresh(u)
        
        print(f"Usuario creado. ID Usuario: {u.id}, ID Docente (simulado): {u.id_docente}")
        
        if u.id == u.id_docente:
            print("⚠️ ADVERTENCIA: ID Usuario == ID Docente. La prueba no será conclusiva sobre el alias.")
        
        # Login
        resp = requests.post(f"{BASE_URL}/login/", json={"correo": user_email, "contrasena": pass_base})
        # Try fallback
        if resp.status_code != 200:
             resp = requests.post(f"{BASE_URL}/api/auth/login/", json={"correo": user_email, "contrasena": pass_base})
        
        if resp.status_code != 200:
            print("FALLO LOGIN")
            return
            
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Intentar resetear usando el ID DE DOCENTE en la URL
        # El endpoint es /usuarios/reset/{id}.
        # Si mandamos 99999 (el id_docente), debería funcionar gracias al fix.
        print(f"\n1. Intentando reset usando ID Docente ({u.id_docente}) en URL...")
        resp_alias = requests.put(f"{BASE_URL}/usuarios/reset/{u.id_docente}", headers=headers, json={"nueva_contrasena": pass_reset_alias})
        
        if resp_alias.status_code == 200:
            print("✅ ÉXITO: El sistema aceptó el ID de Docente como alias válido.")
        else:
            print(f"❌ FALLO: El sistema rechazó el ID de Docente. Status {resp_alias.status_code}")
            print(resp_alias.text)
            return

        # 2. Verificar que la contraseña REALMENTE cambió
        print("\n2. Verificando login con nueva contraseña...")
        resp_login = requests.post(f"{BASE_URL}/login/", json={"correo": user_email, "contrasena": pass_reset_alias})
        if resp_login.status_code != 200:
             resp_login = requests.post(f"{BASE_URL}/api/auth/login/", json={"correo": user_email, "contrasena": pass_reset_alias})
             
        if resp_login.status_code == 200:
            print("✅ ÉXITO TOTAL: La contraseña se actualizó correctamente.")
        else:
            print("❌ FALLO: No se puede loguear con la nueva contraseña.")

    except Exception as e:
        print(f"EXCEPCIÓN: {e}")
    finally:
        db.query(Usuario).filter(Usuario.correo == user_email).delete(synchronize_session=False)
        db.commit()
        db.close()

if __name__ == "__main__":
    verificar_fix_alias()
