from app.core.seguridad import obtener_hash_contrasena

password = "password123"
hashed = obtener_hash_contrasena(password)

print(f"Password: {password}")
print(f"Hash: {hashed}")
print(f"Hash Length: {len(hashed)}")
print(f"Is Bcrypt?: {hashed.startswith('$2b$')}")
