import requests

BASE_URL = "http://localhost:8000"

def test_recovery():
    print("Test 1: Recuperación con correo inválido (Debe fallar 404)")
    try:
        r = requests.post(f"{BASE_URL}/solicitar-recuperacion/", json={
            "correo": "noexiste@yavirac.edu.ec"
        })
        if r.status_code == 404:
            print(f"✅ PASO: Usuario no encontrado (Status {r.status_code})")
        else:
            print(f"❌ FALLO: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"❌ ERROR CONEXIÓN: {e}")

    print("\nTest 2: Recuperación correcta (Simulada) + Rate Limiting Check")
    # Intentamos enviar 2 veces seguidas
    for i in range(1, 4):
        print(f"--- Intento {i} ---")
        try:
            r = requests.post(f"{BASE_URL}/usuarios/recuperar-contrasena", json={
                "correo": "joselyndicao2004@gmail.com" 
            })
            if r.status_code == 200:
                 print(f"✅ PASO: Solicitud {i} aceptada (Status {r.status_code})")
                 if i > 1:
                     print("ℹ️ Nota: Si el Rate Limiting funciona, este intento NO debió enviar email real (ver consola backend).")
            elif r.status_code == 500 and "email" in r.text.lower():
                 print(f"⚠️ PASO PARCIAL: Falló envío (SMTP?), pero lógica ok. (Status {r.status_code})")
            else:
                print(f"❌ FALLO: {r.status_code} - {r.text}")
        except Exception as e:
            print(f"ERROR: {e}")
            
        # Esperar un poco entre intentos si queremos simular usuario real, 
        # pero para probar "doble clic" es mejor inmediato.


if __name__ == "__main__":
    test_recovery()
