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
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está definida en el archivo .env")

# -------------------
# Crear motor y sesión
# -------------------
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -------------------
# Base para modelos
# -------------------
Base = declarative_base()

# -------------------
# Crear tablas si no existen
# -------------------
def crear_tablas():
    from app.models import sala, sede  # importa todos tus modelos aquí
    Base.metadata.create_all(bind=engine)