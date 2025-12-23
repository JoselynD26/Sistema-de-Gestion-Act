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
    
    # Consultar estructura de la tabla materia
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'materia'
        ORDER BY ordinal_position;
    """)
    
    print("Estructura de la tabla 'materia':")
    print("-" * 50)
    for row in cursor.fetchall():
        print(f"Columna: {row[0]}, Tipo: {row[1]}, Nullable: {row[2]}, Default: {row[3]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")