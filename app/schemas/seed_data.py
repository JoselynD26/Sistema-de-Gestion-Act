from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.models import Rol, Usuario, Sede
from passlib.hash import bcrypt

db: Session = SessionLocal()

# Crear rol admin
rol_admin = Rol(nombre="admin", descripcion="Administrador del sistema")
db.add(rol_admin)
db.commit()
db.refresh(rol_admin)

# Crear sede inicial
sede_quito = Sede(nombre="Cdla. Reino de Quito", ubicacion="Mena Dos, Quito")
db.add(sede_quito)
db.commit()
db.refresh(sede_quito)

# Crear usuario admin
usuario_admin = Usuario(
    correo="admin@correo.com",
    contrasena=bcrypt.hash("admin123"),
    rol="admin"
)
db.add(usuario_admin)
db.commit()

print("✅ Datos iniciales creados correctamente.")