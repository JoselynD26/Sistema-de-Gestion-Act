from app.core.config import engine
from sqlalchemy import text

with engine.connect() as conn:
    # Verificar docentes existentes
    docentes = conn.execute(text("SELECT id, nombres, apellidos, sede_id FROM docente")).fetchall()
    print("Docentes en la base de datos:")
    for docente in docentes:
        print(f"ID: {docente[0]}, Nombre: {docente[1]} {docente[2]}, Sede ID: {docente[3]}")
    
    if not docentes:
        print("\nNo hay docentes. Creando docentes de prueba...")
        
        # Crear docentes de prueba
        docentes_prueba = [
            ("Juan", "Pérez", "juan.perez@email.com", "123456789", 1),
            ("María", "González", "maria.gonzalez@email.com", "987654321", 1),
            ("Carlos", "Rodríguez", "carlos.rodriguez@email.com", "456789123", 1)
        ]
        
        for nombres, apellidos, correo, telefono, sede_id in docentes_prueba:
            conn.execute(
                text("INSERT INTO docente (nombres, apellidos, correo, telefono, sede_id) VALUES (:nombres, :apellidos, :correo, :telefono, :sede_id)"),
                {"nombres": nombres, "apellidos": apellidos, "correo": correo, "telefono": telefono, "sede_id": sede_id}
            )
        
        conn.commit()
        print("Docentes de prueba creados")
        
        # Verificar docentes creados
        docentes = conn.execute(text("SELECT id, nombres, apellidos, sede_id FROM docente")).fetchall()
        print("\nDocentes creados:")
        for docente in docentes:
            print(f"ID: {docente[0]}, Nombre: {docente[1]} {docente[2]}, Sede ID: {docente[3]}")