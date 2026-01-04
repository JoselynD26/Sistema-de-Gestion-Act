from app.core.config import SessionLocal
from app.models.usuario import Usuario

db = SessionLocal()
users = db.query(Usuario).all()

print("Usuarios y roles (raw):")
for u in users:
    print(f"ID: {u.id}, Correo: '{u.correo}', Rol: '{u.rol}'")
db.close()
