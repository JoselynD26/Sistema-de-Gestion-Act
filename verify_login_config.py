from app.core.seguridad import EXPIRACION_MINUTOS, crear_token, verificar_contrasena, obtener_hash_contrasena
from datetime import datetime, timedelta
import jwt
from app.core.seguridad import SECRET_KEY, ALGORITHM

print(f"EXPIRACION_MINUTOS configurado: {EXPIRACION_MINUTOS}")

if EXPIRACION_MINUTOS == 10080:
    print("✅ La expiración está correctamente configurada a 7 días (10080 minutos).")
else:
    print(f"❌ ERROR: La expiración es {EXPIRACION_MINUTOS}, se esperaba 10080.")

# Simular creación de token
token = crear_token(1, "admin")
decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
exp_timestamp = decoded["exp"]
exp_date = datetime.utcfromtimestamp(exp_timestamp)
now = datetime.utcnow()
diff = exp_date - now

print(f"Token generado expira en: {exp_date}")
print(f"Diferencia de tiempo: {diff}")

if diff > timedelta(days=6, hours=23): # Aprox 7 días
    print("✅ El token generado tiene una validez correcta de ~7 días.")
else:
    print("❌ El token generado NO tiene la validez esperada.")

# Prueba rápida de hashing (opcional, para ver si demora mucho)
import time
start = time.time()
h = obtener_hash_contrasena("prueba123")
end = time.time()
print(f"Tiempo de hashing (Argon2/Bcrypt): {end - start:.4f} segundos")
