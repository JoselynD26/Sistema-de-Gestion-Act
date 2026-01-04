from app.core.config import SessionLocal
from app.models.usuario import Usuario
from sqlalchemy import func

db = SessionLocal()
roles_count = db.query(Usuario.rol, func.count(Usuario.id)).group_by(Usuario.rol).all()

print("Conteo de usuarios por rol:")
for rol, count in roles_count:
    print(f"- {rol}: {count}")

admins = db.query(Usuario).filter(Usuario.rol == "admin").all()
if admins:
    print("\nAdministradores encontrados:")
    for admin in admins:
        print(f"- {admin.correo} (Nombres: {admin.nombres})")
else:
    print("\nNo se encontraron administradores en la base de datos.")

db.close()
