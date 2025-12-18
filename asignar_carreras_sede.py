from app.core.config import engine
from sqlalchemy import text

# Primero verificar qué sedes existen
with engine.connect() as conn:
    sedes = conn.execute(text("SELECT id, nombre FROM sede")).fetchall()
    print("Sedes disponibles:")
    for sede in sedes:
        print(f"ID: {sede[0]}, Nombre: {sede[1]}")
    
    if sedes:
        sede_id = sedes[0][0]  # Usar la primera sede
        print(f"\nAsignando carreras a la sede ID: {sede_id}")
        
        # Asignar carreras 1-5 a la primera sede
        for carrera_id in range(1, 6):
            conn.execute(
                text("INSERT INTO carrera_sede (carrera_id, sede_id) VALUES (:carrera_id, :sede_id) ON CONFLICT DO NOTHING"),
                {"carrera_id": carrera_id, "sede_id": sede_id}
            )
        
        conn.commit()
        print("Carreras asignadas a la sede correctamente")
    else:
        print("No hay sedes disponibles. Crea una sede primero.")