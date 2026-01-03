from app.core.config import SessionLocal
from app.models.usuario import Usuario

db = SessionLocal()
users = db.query(Usuario).limit(5).all()
print("Usuarios encontrados:")
for u in users:
    print(f"- {u.correo} (ID: {u.id})")
db.close()
