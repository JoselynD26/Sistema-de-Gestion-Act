from app.core.seguridad import obtener_hash_contrasena
pwd = "test"
h = obtener_hash_contrasena(pwd)
with open("hash_len.txt", "w") as f:
    f.write(f"Len: {len(h)}\n")
    f.write(f"Hash: {h}\n")
