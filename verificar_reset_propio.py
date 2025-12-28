
import requests

BASE_URL = "http://localhost:8000"

def verificar_reset_propio():
    print("--- Verificando Reset Propio y Permisos ---")
    
    from app.core.config import SessionLocal
    from app.models.usuario import Usuario
    import hashlib

    db = SessionLocal()
    
    # Datos de prueba
    admin_email = "admin_reset@test.com"
    user1_email = "user1_reset@test.com"
    user2_email = "user2_reset@test.com"
    pass_base = "123456"
    pass_nueva = "nueva123"

    try:
        # Limpieza previa
        db.query(Usuario).filter(Usuario.correo.in_([admin_email, user1_email, user2_email])).delete(synchronize_session=False)
        db.commit()

        # Crear usuarios
        def crear(nombre, correo, rol):
            u = Usuario(
                nombres=nombre, apellidos="Test", correo=correo,
                contrasena=hashlib.sha256(pass_base.encode()).hexdigest(),
                rol=rol
            )
            db.add(u)
            db.commit()
            db.refresh(u)
            return u

        admin = crear("Admin", admin_email, "admin")
        user1 = crear("User1", user1_email, "docente")
        user2 = crear("User2", user2_email, "docente")
        
        print(f"Usuarios: Admin({admin.id}), User1({user1.id}), User2({user2.id})")

        # Helper para login
        def get_token(correo):
            resp = requests.post(f"{BASE_URL}/login/", json={"correo": correo, "contrasena": pass_base}) # endpoint auth
            if resp.status_code == 200:
                return resp.json()["access_token"]
            # Intento con api/auth si falla
            resp = requests.post(f"{BASE_URL}/api/auth/login/", json={"correo": correo, "contrasena": pass_base})
            if resp.status_code == 200:
                return resp.json()["access_token"]
            print(f"Login failed for {correo}")
            return None

        # 1. Admin resetea a User1 (Debe funcionar)
        token_admin = get_token(admin_email)
        headers_admin = {"Authorization": f"Bearer {token_admin}"}
        
        print("\n1. Admin resetea a User1...")
        resp = requests.put(f"{BASE_URL}/usuarios/reset/{user1.id}", headers=headers_admin, json={"nueva_contrasena": pass_nueva})
        if resp.status_code == 200:
            print("✅ OK: Admin pudo resetear.")
        else:
            print(f"❌ FALLO: Admin no pudo resetear. Status {resp.status_code}")
            print(resp.text)

        # 2. User2 intenta resetear a User1 (Debe fallar 403)
        token_user2 = get_token(user2_email)
        headers_user2 = {"Authorization": f"Bearer {token_user2}"}
        
        print("\n2. User2 intenta resetear a User1 (Esperamos 403)...")
        resp = requests.put(f"{BASE_URL}/usuarios/reset/{user1.id}", headers=headers_user2, json={"nueva_contrasena": "hacker"})
        if resp.status_code == 403:
            print("✅ OK: User2 fue bloqueado correctamente (403).")
        else:
            print(f"❌ FALLO: User2 no recibió 403. Recibió {resp.status_code}")

        # 3. User2 se resetea a SÍ MISMO (Debe funcionar - Nuevo requerimiento)
        print("\n3. User2 se resetea a SÍ MISMO (Debe funcionar)...")
        resp = requests.put(f"{BASE_URL}/usuarios/reset/{user2.id}", headers=headers_user2, json={"nueva_contrasena": pass_nueva})
        if resp.status_code == 200:
            print("✅ OK: User2 pudo resetear su propia contraseña.")
        else:
            print(f"❌ FALLO: User2 no pudo resetearse a sí mismo. Status {resp.status_code}")
            print(resp.text)

    except Exception as e:
        print(f"EXCEPCIÓN: {e}")
    finally:
        db.query(Usuario).filter(Usuario.correo.in_([admin_email, user1_email, user2_email])).delete(synchronize_session=False)
        db.commit()
        db.close()

if __name__ == "__main__":
    verificar_reset_propio()
