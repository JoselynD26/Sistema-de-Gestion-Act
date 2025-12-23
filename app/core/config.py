from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# -------------------
# Cargar variables de entorno desde .env
# -------------------
load_dotenv()

# -------------------
# URL de conexión a la base de datos
# -------------------
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

if not all([DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD]):
    raise ValueError("Faltan variables de configuración de base de datos en .env")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=disable"

print("="*80)
print("DEBUG: Configuración de Base de Datos")
print("="*80)
print(f"HOST: {DB_HOST}")
print(f"PORT: {DB_PORT}")
print(f"DATABASE: {DB_NAME}")
print(f"USER: {DB_USER}")
print("="*80)

# -------------------
# Crear motor y sesión
# -------------------
try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    print("\u2705 Motor de base de datos creado exitosamente")
except Exception as e:
    print(f"\u274c ERROR al crear motor de base de datos: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -------------------
# Base para modelos
# -------------------
Base = declarative_base()

# -------------------
# Dependencia para obtener sesión de base de datos
# -------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------
# Crear tablas si no existen
# -------------------
def crear_tablas():
    from app.models import sala_profesores, sede  # importa todos tus modelos aquí
    Base.metadata.create_all(bind=engine)