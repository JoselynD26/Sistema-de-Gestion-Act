from app.core.config import engine
from sqlalchemy import text

# Crear una sala de prueba
with engine.connect() as conn:
    # Verificar sedes disponibles
    sedes = conn.execute(text("SELECT id, nombre FROM sede")).fetchall()
    print("Sedes disponibles:")
    for sede in sedes:
        print(f"ID: {sede[0]}, Nombre: {sede[1]}")
    
    if sedes:
        sede_id = sedes[0][0]
        
        # Crear sala de prueba
        conn.execute(
            text("INSERT INTO sala (nombre, sede_id) VALUES (:nombre, :sede_id)"),
            {"nombre": "Sala de Prueba Backend", "sede_id": sede_id}
        )
        conn.commit()
        print(f"Sala creada en la sede ID: {sede_id}")
        
        # Verificar salas
        salas = conn.execute(text("SELECT id, nombre, sede_id FROM sala")).fetchall()
        print("\nSalas en la base de datos:")
        for sala in salas:
            print(f"ID: {sala[0]}, Nombre: {sala[1]}, Sede ID: {sala[2]}")
    else:
        print("No hay sedes disponibles")