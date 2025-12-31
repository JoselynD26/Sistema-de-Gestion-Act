from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# -------------------
# Cargar variables de entorno (solo para local)
# -------------------
load_dotenv()

# -------------------
# URL de conexión (Render o local)
# -------------------
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada")

# -------------------
# Crear motor y sesión
# -------------------
try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    print("✅ Motor de base de datos creado exitosamente")
except Exception as e:
    print(f"❌ ERROR al crear motor de base de datos: {e}")
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
