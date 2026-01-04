from app.core.config import SessionLocal
from app.models.docente import Docente

db = SessionLocal()
docentes = db.query(Docente).all()

print("Verificando correos de docentes:")
for d in docentes:
    correo_raw = f"'{d.correo}'" if d.correo else "NULL"
    print(f"ID: {d.id}, Nombre: {d.nombres} {d.apellidos}, Correo: {correo_raw}")
db.close()
