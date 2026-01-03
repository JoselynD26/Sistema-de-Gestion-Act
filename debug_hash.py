from app.core.seguridad import obtener_hash_contrasena, verificar_contrasena
from app.core.config import SessionLocal
from app.models.usuario import Usuario

# 1. Test Generate and Verify in memory
pwd = "TestPassword123"
hashed = obtener_hash_contrasena(pwd)
print(f"Password: {pwd}")
print(f"Hash: {hashed}")
print(f"Hash Length: {len(hashed)}")
if len(hashed) > 100:
    print("⚠️ WARNING: Hash length exceeds 100 characters! DB truncation likely.")
else:
    print("✅ Hash length is within limits.")

if verificar_contrasena(pwd, hashed):
    print("✅ In-memory verification PASSED")
else:
    print("❌ In-memory verification FAILED")

# 2. Test DB Update and Verify
db = SessionLocal()
# Usamos el usuario de prueba
user = db.query(Usuario).filter(Usuario.correo == "joselyndicao2004@gmail.com").first()

if user:
    print(f"\nUpdating user {user.correo} with new hash...")
    user.contrasena = hashed
    db.commit()
    db.refresh(user)
    
    print(f"Stored Hash: {user.contrasena}")
    
    if verificar_contrasena(pwd, user.contrasena):
        print("✅ DB Round-trip verification PASSED")
    else:
        print("❌ DB Round-trip verification FAILED")
        
    # Test Legacy/Alternative scenarios
    # Verify if spaces triggers the issue? (Already patched, but good to check)
else:
    print("User not found for DB test")

db.close()
