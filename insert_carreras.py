from app.core.config import engine
from sqlalchemy import text

# Datos de las carreras
carreras = [
    'Marketing',
    'Desarrollo de Software',
    'Arte Culinario',
    'Diseño de Modas',
    'Idiomas'
]

# Insertar carreras
with engine.connect() as conn:
    for nombre in carreras:
        conn.execute(
            text("INSERT INTO carrera (nombre) VALUES (:nombre)"),
            {"nombre": nombre}
        )
    conn.commit()
    print("✅ Carreras insertadas correctamente")