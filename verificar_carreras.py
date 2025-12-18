from app.core.config import engine
from sqlalchemy import text

# Verificar carreras insertadas
with engine.connect() as conn:
    result = conn.execute(text("SELECT id, nombre FROM carrera"))
    carreras = result.fetchall()
    
    print("Carreras en la base de datos:")
    for carrera in carreras:
        print(f"ID: {carrera[0]}, Nombre: {carrera[1]}")