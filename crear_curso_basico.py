import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

# Configuración de la base de datos
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'aws-0-us-east-1.pooler.supabase.com'),
    'port': os.getenv('DB_PORT', '6543'),
    'database': os.getenv('DB_NAME', 'postgres'),
    'user': os.getenv('DB_USER', 'postgres.mxsppfefemshxotsspbz'),
    'password': os.getenv('DB_PASSWORD')
}

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Insertar un curso básico si no existe
    cursor.execute("""
        INSERT INTO curso (nombre, nivel, paralelo, carrera_id, sede_id) 
        VALUES ('Curso General', '1', 'A', 5, 1)
        ON CONFLICT DO NOTHING
        RETURNING id;
    """)
    
    result = cursor.fetchone()
    if result:
        print(f"Curso creado con ID: {result[0]}")
    else:
        print("Curso ya existe o no se pudo crear")
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Curso básico insertado exitosamente")
    
except Exception as e:
    print(f"Error: {e}")