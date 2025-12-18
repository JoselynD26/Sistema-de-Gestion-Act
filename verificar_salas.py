from app.core.config import engine
from sqlalchemy import text

with engine.connect() as conn:
    # Verificar todas las salas
    salas = conn.execute(text("SELECT id, nombre, sede_id FROM sala")).fetchall()
    print("Todas las salas en la base de datos:")
    for sala in salas:
        print(f"ID: {sala[0]}, Nombre: {sala[1]}, Sede ID: {sala[2]}")
    
    # Verificar sedes
    sedes = conn.execute(text("SELECT id, nombre FROM sede")).fetchall()
    print("\nSedes disponibles:")
    for sede in sedes:
        print(f"ID: {sede[0]}, Nombre: {sede[1]}")