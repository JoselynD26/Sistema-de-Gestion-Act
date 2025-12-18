from app.core.config import engine
from sqlalchemy import text

with engine.connect() as conn:
    # Eliminar la sala de prueba
    conn.execute(text("DELETE FROM sala WHERE nombre = 'Sala de Prueba Backend'"))
    conn.commit()
    print("Sala de prueba eliminada")
    
    # Verificar salas restantes
    salas = conn.execute(text("SELECT id, nombre, sede_id FROM sala")).fetchall()
    print("\nSalas restantes:")
    for sala in salas:
        print(f"ID: {sala[0]}, Nombre: {sala[1]}, Sede ID: {sala[2]}")