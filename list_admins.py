from app.core.config import SessionLocal
from app.models.usuario import Usuario

db = SessionLocal()
admins = db.query(Usuario).filter(Usuario.rol == "admin").all()
print("Administradores en el sistema:")
for a in admins:
    print(f"- {a.correo} ({a.nombres} {a.apellidos})")
db.close()
