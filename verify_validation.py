import requests

BASE_URL = "http://localhost:8000"

def test_login_validation():
    print("Test 1: Login con espacios en correo (Debe fallar)")
    try:
        r = requests.post(f"{BASE_URL}/login/", json={
            "correo": "admin @yavirac.edu.ec", 
            "contrasena": "admin123"
        })
        if r.status_code == 400 and "espacios" in r.text:
            print(f"✅ PASO: Rechazó correctamente (Status {r.status_code})")
        else:
            print(f"❌ FALLO: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"❌ ERROR CONEXIÓN: {e}")

    print("\nTest 2: Login con espacios en password (Debe fallar)")
    try:
        r = requests.post(f"{BASE_URL}/login/", json={
            "correo": "admin@yavirac.edu.ec", 
            "contrasena": "admin 123"
        })
        if r.status_code == 400 and "espacios" in r.text:
            print(f"✅ PASO: Rechazó correctamente (Status {r.status_code})")
        else:
            print(f"❌ FALLO: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"ERROR: {e}")

    print("\nTest 3: Login correcto (Debe pasar)")
    # Nota: Usamos credenciales que sabemos existen o esperamos 401 si no, pero NO 400
    try:
        r = requests.post(f"{BASE_URL}/login/", json={
            "correo": "admin@yavirac.edu.ec", 
            "contrasena": "admin123" # Asumiendo credencial default
        })
        if r.status_code != 400:
             print(f"✅ PASO: No dio error de validación (Status {r.status_code})")
             if r.status_code == 200:
                 return r.json().get("access_token")
        else:
            print(f"❌ FALLO: Dio error de validación incorrecto: {r.text}")
    except Exception as e:
        print(f"ERROR: {e}")
    return None

def test_change_password(token):
    if not token:
        print("Saltando test de password por falta de token")
        return

    print("\nTest 4: Cambiar contraseña con espacios (Debe fallar)")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = requests.put(f"{BASE_URL}/cambiar-contrasena/", json={
            "contrasena_actual": "admin123",
            "nueva_contrasena": "nueva clave" # Con espacio
        }, headers=headers)
        
        if r.status_code == 400 and "espacios" in r.text:
            print(f"✅ PASO: Rechazó cambio de contraseña con espacios")
        else:
             print(f"❌ FALLO: {r.status_code} - {r.text}")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    token = test_login_validation()
    test_change_password(token)
